#!/usr/bin/env python3
"""Validate the frozen, non-self-referential public SHA-256 manifest."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=set(manifest['files'])
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
assert actual==expected, {'missing':sorted(expected-actual),'unlisted':sorted(actual-expected)}
for name, wanted in manifest['files'].items():
    assert Path(name).name==name
    got=hashlib.sha256((root/name).read_bytes()).hexdigest()
    assert got==wanted, {'file':name,'actual':got,'expected':wanted}
print(json.dumps({'result':'passed','verified_public_files':len(expected)},sort_keys=True))
