#!/usr/bin/env python3
"""Verify final audit custody and the retained result's stable invariants."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
for entry in manifest["files"]:
    path = root / entry["path"]
    data = path.read_bytes()
    assert len(data) == entry["bytes"], entry["path"]
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
listed = {entry["path"] for entry in manifest["files"]}
actual = {str(path.relative_to(root)) for path in root.rglob("*")
          if path.is_file() and path.name != "MANIFEST.json"}
assert actual == listed, ("file_set_changed", actual ^ listed)
result = json.loads((root / "INDEPENDENT_CONTROLS.json").read_text())
assert result["assertion_count"] == 125930
assert result["exhaustive_F2"]["configuration_count"] == 59535
assert result["exhaustive_F2"]["classification_exceptions"] == []
assert result["exhaustive_F2"]["stream_sha256"] == "0f7a69ad8b6507feaf4108c7ad5b8eba50d8850ac1a6f1c285657a7bc04e7c52"
assert result["script_sha256"] == hashlib.sha256((root / "independent_controls.py").read_bytes()).hexdigest()
original = json.loads((root / "ORIGINAL_CONTROLS_REPRODUCED.json").read_text())
assert original["assertions"] == 3888
assert original["proof_sha256"] == hashlib.sha256((root / "FROZEN_PUBLIC_TURN_2.md").read_bytes()).hexdigest()
assert json.loads((root / "ORIGINAL_REPRODUCTION_COMPARISON.json").read_text())["exact_json_equality"]
print(json.dumps({"status": "PASS_CUSTODY_AND_RETAINED_RESULT", "files": len(listed),
                  "independent_assertions": 125930, "original_assertions": 3888}, sort_keys=True))
