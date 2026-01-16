import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "static" / "data" / "tempering.json"
ZH_MAP = ROOT / "static" / "data" / "tempering_zh_map.json"
TODO = ROOT / "static" / "data" / "tempering_zh_todo.json"


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def main():
    tempering = load_json(SRC, [])
    zh_map = load_json(ZH_MAP, {"manual": {}, "affix": {}})

    todo_manual = {}
    todo_affix = {}

    for item in tempering:
        manual = item["manual"]
        if manual not in zh_map["manual"]:
            todo_manual[manual] = ""

        for affix in item.get("affixes", []):
            if affix not in zh_map["affix"]:
                todo_affix[affix] = ""

    result = {
        "manual": dict(sorted(todo_manual.items())),
        "affix": dict(sorted(todo_affix.items()))
    }

    TODO.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(
        f"✅ Found {len(todo_manual)} manuals "
        f"and {len(todo_affix)} affixes to translate."
    )


if __name__ == "__main__":
    main()
