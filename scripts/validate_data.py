import json
from pathlib import Path

DATA = Path("static/data/tempering_affixes_structured.json")

data = json.loads(DATA.read_text(encoding="utf-8"))

assert isinstance(data, list)
assert len(data) > 10

for item in data:
    assert "affix_id" in item
    assert "text" in item

print("✅ Data validation passed")
