import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "static" / "data" / "tempering.json"
OUT = ROOT / "static" / "data" / "tempering_affixes_structured.json"


def normalize_affix(text: str) -> str:
    return (
        text.replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("\u2212", "-")
            .replace("\u00a0", " ")
            .replace(" %", "%")
            .strip()
    )


SKILL_PERCENT_PATTERN = re.compile(
    r"\+\[(?P<value>[\d\.\s\-]+)\]%\s+(?P<skill>.+?)\s+"
    r"(?P<type>Duration|Damage|Effect|Size|Radius)\."
)

SKILL_RANK_PATTERN = re.compile(
    r"\+\[(?P<value>[\d\s\-]+)\]\s+to\s+(?P<skill>.+?)\."
)

IMBUEMENT_PATTERN = re.compile(
    r"\+\[(?P<value>[\d\s\-]+)\]\s+(?P<element>\w+)\s+Imbuement Count\."
)


def parse_affix(raw: str):
    text = normalize_affix(raw)

    if m := SKILL_PERCENT_PATTERN.match(text):
        return {
            "raw": raw,
            "kind": f"skill_{m.group('type').lower()}",
            "skill": m.group("skill"),
            "value_range": m.group("value"),
        }

    if m := SKILL_RANK_PATTERN.match(text):
        return {
            "raw": raw,
            "kind": "skill_rank",
            "skill": m.group("skill"),
            "value_range": m.group("value"),
        }

    if m := IMBUEMENT_PATTERN.match(text):
        return {
            "raw": raw,
            "kind": "imbuement_count",
            "element": m.group("element"),
            "value_range": m.group("value"),
        }

    return None


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    parsed = {}
    unparsed = set()

    for item in data:
        for affix in item.get("affixes", []):
            if affix in parsed:
                continue

            result = parse_affix(affix)
            if result:
                parsed[affix] = result
            else:
                unparsed.add(affix)

    OUT.write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Parsed affixes: {len(parsed)}")
    print(f"⚠️ Unparsed affixes: {len(unparsed)}")

    for i, a in enumerate(sorted(unparsed)):
        print("-", a)
        if i >= 5:
            break


if __name__ == "__main__":
    main()
