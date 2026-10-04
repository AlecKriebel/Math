#!/usr/bin/env python3
"""Acquire only the three explicitly released first-candidate inputs."""
import hashlib
import json
import pathlib
import shutil

root = pathlib.Path(__file__).resolve().parents[1]
source = root.parent / "preprint" / "qualification_v02" / "inputs"
destination = root / "evidence" / "candidate_stage1" / "inputs"
destination.mkdir(parents=True, exist_ok=True)
rows = []
for name in ("manuscript.tex", "manuscript.pdf", "zenodo-deposit.json"):
    src = source / name
    dst = destination / name
    if dst.exists():
        raise SystemExit(f"Refusing overwrite: {dst}")
    before = src.read_bytes()
    shutil.copyfile(src, dst)
    after = src.read_bytes()
    copied = dst.read_bytes()
    assert before == after == copied, f"Byte mismatch: {name}"
    row = {"name": name, "source": str(src), "copy": str(dst),
           "bytes": len(copied), "sha256": hashlib.sha256(copied).hexdigest()}
    rows.append(row)
    print(json.dumps(row, sort_keys=True))
(destination.parent / "exact_three_input_pins.json").write_text(json.dumps(rows, indent=2) + "\n")
