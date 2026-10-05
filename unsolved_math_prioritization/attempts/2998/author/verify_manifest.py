#!/usr/bin/env python3
"""Verify the exact authored packet, excluding the manifest's own hash."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "AUTHOR_MANIFEST.json").read_text())
expected = {x["path"]: x for x in manifest["files"]}
actual = {str(x.relative_to(root)) for x in root.rglob("*") if x.is_file()
          and x.name != "AUTHOR_MANIFEST.json"}
assert actual == set(expected), (sorted(actual - set(expected)), sorted(set(expected) - actual))
for name, rec in expected.items():
    path = root / name
    assert not path.is_symlink(), name
    data = path.read_bytes()
    assert len(data) == rec["bytes"], name
    assert hashlib.sha256(data).hexdigest() == rec["sha256"], name
    assert path.suffix in {".md", ".json", ".py"}, name
print(json.dumps({"status": "PASS", "files_verified": len(expected),
                  "full_solution_claimed": manifest["full_solution_claimed"]}, sort_keys=True))
