#!/usr/bin/env python3
"""Verify all review bindings and the authoritative frozen snapshot, then replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

p = Path(__file__).resolve().parent
manifest = json.loads((p / "OUTPUT_MANIFEST.json").read_text())
for x in manifest["files"]:
    b = (p / x["path"]).read_bytes()
    assert len(b) == x["bytes"] and hashlib.sha256(b).hexdigest() == x["sha256"], x["path"]
frozen = json.loads((p.parent / "snapshot_manifest.json").read_text())
assert frozen["head"] == "682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6"
assert len(frozen["files"]) == 52
for x in frozen["files"]:
    b = (p.parent / "snapshot" / x["path"]).read_bytes()
    assert len(b) == x["bytes"] and hashlib.sha256(b).hexdigest() == x["sha256"], x["path"]
out = subprocess.check_output([sys.executable, str(p / "independent_controls.py")], cwd=p)
assert out == (p / "INDEPENDENT_CONTROLS.json").read_bytes()
adversarial = subprocess.check_output([sys.executable, str(p / "adversary" / "full_split_controls.py")], cwd=p)
assert adversarial == (p / "adversary" / "FULL_SPLIT_CONTROLS.json").read_bytes()
print(json.dumps({"all_review_bindings_match": True, "review_files": len(manifest["files"]),
                  "all_frozen_bindings_match": True, "frozen_files": 52,
                  "independent_replay_byte_exact": True,
                  "independent_assertions": json.loads(out)["total_exact_assertions"],
                  "adversarial_replay_byte_exact": True,
                  "adversarial_assertions": json.loads(adversarial)["exact_assertions"],
                  "original_universal_status": "unsolved 5/5"}, indent=2))
