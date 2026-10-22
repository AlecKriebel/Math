#!/usr/bin/env python3
"""Check a corrected release's entire safe inventory and bound historical archives."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'RELEASE_MANIFEST.json').read_text())
excluded={'RELEASE_MANIFEST.json','release-packet.zip','RELEASE_FREEZE.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in excluded}
expected={r['path'] for r in manifest['files']}
assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for row in manifest['files']:
    p=pathlib.Path(row['path'])
    assert not p.is_absolute() and '..' not in p.parts
    raw=(root/p).read_bytes()
    assert len(raw)==row['bytes'],row['path']
    assert hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
print(json.dumps({'passed':True,'files_checked':len(expected),'scope':'Integrity only; corrected independent audit confirmation remains a separate gate.'},sort_keys=True))
