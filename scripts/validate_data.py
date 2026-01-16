import json
from pathlib import Path

DATA = Path("static/data/tempering_final.json")

data = json.loads(DATA.read_text(encoding="utf-8"))

assert isinstance(data, list)
assert len(data) > 10

for item in data:
    assert "manualId" in item
    assert "affixes" in item
    assert len(item["affixes"]) > 0

print("✅ Data validation passed")
