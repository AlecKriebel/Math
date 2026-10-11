#!/usr/bin/env python3
"""Targeted read-only reproduction of historical Git content bindings."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
REPO = BASE.parents[2]
P = BASE / "snapshot" / "problems" / "30004656_robustness"
ROOT_RECEIPT = BASE / "root_historical_git_verification.json"
bindings = []

def check(tag, head, row, blob_key, size_key):
    path = "problems/30004656_robustness/" + row["path"]
    blob = subprocess.check_output(["git", "rev-parse", head + ":" + path], cwd=REPO).decode().strip()
    data = subprocess.check_output(["git", "show", head + ":" + path], cwd=REPO)
    assert blob == row[blob_key] and len(data) == row[size_key]
    assert data == (P / row["path"]).read_bytes()
    bindings.append([tag, row["path"], blob])

for turn in range(1, 5):
    receipt = json.loads((P / f"TURN_{turn}_REMOTE_RECEIPT.json").read_text())
    for row in receipt["files"]:
        check(turn, receipt["head"], row, "sha", "size")
receipt = json.loads((P / "review" / "REMOTE_BINDING.json").read_text())
for tag, head in [("original_files", receipt["author_head"]), ("all_corrected_tree_files", receipt["corrected_head"])]:
    for row in receipt[tag]:
        check(tag, head, row, "git_blob_sha", "bytes")
root = json.loads(ROOT_RECEIPT.read_text())
assert len(bindings) == root["historical_git_bindings_reproduced"] == 136
assert bindings == root["bindings"]
result = {"status": "PASS", "completed_at_utc": datetime.now(timezone.utc).isoformat(),
          "historical_git_objects_reproduced": len(bindings), "equal_root_binding_list": True,
          "root_input_sha256": hashlib.sha256(ROOT_RECEIPT.read_bytes()).hexdigest(),
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "historical_search_recreated": False, "historical_png_recreated": False,
          "limit": "Confirms content at immutable Git object IDs. Does not certify historical remote access, historical mutable-ref search coverage, priority or novelty."}
(OUT / "HISTORICAL_OBJECTS_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
