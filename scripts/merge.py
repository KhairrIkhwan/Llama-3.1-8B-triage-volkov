import json
from pathlib import Path
from openpyxl import load_workbook

DATA = Path("..") / "data"
FIXES = {"T013": {"urgency": "low"}}
EXCLUDE = {f"N{i}" for i in range(361, 406)}

rows = []
with open(DATA / "train_raw.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            rows.append(json.loads(line))

for path in (DATA / "data_starter.xlsx", DATA / "new_rows.xlsx"):
    ws = load_workbook(path).worksheets[0]
    table = list(ws.iter_rows(values_only=True))
    header = table[0]
    for values in table[1:]:
        row = dict(zip(header, values))
        if not row["message"] or row["id"] in EXCLUDE:
            continue
        row["needs_human"] = str(row["needs_human"]).strip().upper() == "TRUE"
        rows.append(row)

for row in rows:
    row.update(FIXES.get(row["id"], {}))

with open(DATA / "merged.jsonl", "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(len(rows), "rows written to data/merged.jsonl")
