#!/usr/bin/env python3
"""Check every release file, excluding the manifest itself and bytecode caches."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root/'SHA256SUMS.json').read_text())
actual = {str(p.relative_to(root)) for p in root.rglob('*')
          if p.is_file() and '__pycache__' not in p.parts
          and p.name != 'SHA256SUMS.json'}
assert actual == set(manifest), {'missing':sorted(set(manifest)-actual),
                                 'extra':sorted(actual-set(manifest))}
for name, expected in manifest.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == expected, name
print(json.dumps({'result':'passed', 'file_count':len(manifest)}, sort_keys=True))
