import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


OUTPUT_PATH = Path(__file__).resolve().parent.parent / "static" / "data" / "tempering.json"


CHARLIE_URL = "https://www.charlieintel.com/diablo/diablo-4-all-temper-manuals-affixes-for-every-class-325441/"
GAME8_URL = "https://game8.co/games/Diablo-4/archives/454071"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; D4ToolBot/1.0)"
}


def fetch_html(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_charlieintel(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # 以 h2 / h3 为职业分段（站点结构偶尔会变）
    for header in soup.find_all(["h2", "h3"]):
        class_name = header.get_text(strip=True)

        table = header.find_next("table")
        if not table:
            continue

        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            manual = cols[0].get_text(strip=True)
            affixes = [
                a.strip()
                for a in cols[1].get_text("\n").split("\n")
                if a.strip()
            ]

            results.append({
                "class": class_name,
                "manual": manual,
                "category": None,
                "affixes": affixes,
                "source": ["charlieintel"]
            })

    return results


def parse_game8(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    table = soup.find("table")
    if not table:
        return results

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        manual = cols[0].get_text(strip=True)
        category = cols[1].get_text(strip=True)
        cls = cols[3].get_text(strip=True)

        results.append({
            "class": cls,
            "manual": manual,
            "category": category,
            "affixes": [],
            "source": ["game8"]
        })

    return results


def merge_data(charlie, game8):
    merged = {}

    for item in charlie + game8:
        key = (item["class"], item["manual"])
        if key not in merged:
            merged[key] = item
        else:
            merged[key]["source"] = list(
                set(merged[key]["source"] + item["source"])
            )
            if not merged[key]["category"]:
                merged[key]["category"] = item["category"]

    return list(merged.values())


def main():
    print("▶ Fetching Charlie INTEL...")
    charlie_html = fetch_html(CHARLIE_URL)
    charlie_data = parse_charlieintel(charlie_html)

    time.sleep(2)

    print("▶ Fetching Game8...")
    game8_html = fetch_html(GAME8_URL)
    game8_data = parse_game8(game8_html)

    print("▶ Merging data...")
    final_data = merge_data(charlie_data, game8_data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Done. {len(final_data)} manuals saved.")


if __name__ == "__main__":
    main()
