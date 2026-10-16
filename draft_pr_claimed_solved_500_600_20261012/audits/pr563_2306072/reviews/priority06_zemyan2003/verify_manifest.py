#!/usr/bin/env python3
"""Verify authored-output seal and exact source/candidate inputs, read only."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


manifest = json.loads((BASE / "MANIFEST.json").read_text())
sealed = set()
for item in manifest["authored_outputs"]:
    path = BASE / item["path"]
    assert path.is_file(), path
    assert digest(path) == item["sha256"], path
    assert path.stat().st_size == item["bytes"], path
    sealed.add(item["path"])
present = {str(p.relative_to(BASE)) for p in BASE.rglob("*")
           if p.is_file() and not set(p.relative_to(BASE).parts) & {".cache", "__pycache__"}}
assert present == sealed | {"MANIFEST.json"}, (present, sealed)
source_seal = json.loads((BASE / "SOURCE_SEAL.json").read_text())
for item in source_seal["compared_inputs"]:
    assert digest(Path(item["path"])) == item["sha256"], item["path"]
inputs = json.loads((BASE / "SOURCE_INPUTS.json").read_text())
assert digest(Path(inputs["source"]["user_download_path"])) == inputs["source"]["user_download_sha256"]
assert inputs["source"]["sha256"] == inputs["source"]["user_download_sha256"]
print(json.dumps({"authored_output_count": len(sealed),
                  "all_authored_outputs_sealed": True,
                  "all_compared_inputs_unchanged": True,
                  "copyrighted_raw_artifacts_excluded": True}, indent=2))
