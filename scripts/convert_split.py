import json
import random
from pathlib import Path

DATA = Path("..") / "data"
VAL_SHARE = 0

system = (DATA / "system_prompt.txt").read_text(encoding="utf-8").strip()
rows = [json.loads(l) for l in open(DATA / "merged.jsonl", encoding="utf-8") if l.strip()]

chats = []
for row in rows:
    answer = json.dumps({"category": row["category"], "urgency": row["urgency"], "needs_human": row["needs_human"]})
    chats.append({"messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": row["message"]},
        {"role": "assistant", "content": answer},
    ]})

random.seed(42)
random.shuffle(chats)
n_val = round(len(chats) * VAL_SHARE)
val, train = chats[:n_val], chats[n_val:]
for name, part in (("train.jsonl", train), ("val.jsonl", val)):
    if part:
        with open(DATA / name, "w", encoding="utf-8") as f:
            for chat in part:
                f.write(json.dumps(chat, ensure_ascii=False) + "\n")
print(f"{len(rows)} rows -> train.jsonl: {len(train)}, val.jsonl: {len(val)}")
