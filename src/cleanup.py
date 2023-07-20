#!/usr/bin/env python3
"""Clean CSV/JSON datasets and flag records needing manual correction."""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path
from typing import Any

def load(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return [data] if isinstance(data, dict) else list(data)
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def clean(records: list[dict[str, Any]], required: list[str]) -> dict[str, Any]:
    cleaned, flagged = [], []
    seen = set()
    for i, row in enumerate(records, start=1):
        item = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        missing = [f for f in required if not str(item.get(f, "")).strip()]
        key = tuple(str(item.get(f, "")).lower() for f in required) if required else tuple(item.items())
        duplicate = key in seen
        seen.add(key)
        if missing or duplicate:
            flagged.append({"row": i, "missing": missing, "duplicate": duplicate, "record": item})
        else:
            cleaned.append(item)
    return {"cleaned": cleaned, "flagged": flagged, "stats": {"input": len(records), "cleaned": len(cleaned), "flagged": len(flagged)}}

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--required", nargs="+", default=["id", "name"])
    p.add_argument("--out", default="samples/cleaned.json")
    args = p.parse_args()
    result = clean(load(Path(args.input)), args.required)
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["stats"]))

if __name__ == "__main__":
    main()
