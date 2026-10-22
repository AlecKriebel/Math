#!/usr/bin/env python3
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
assert expected==actual, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for e in manifest['files']:
    b=(root/e['path']).read_bytes()
    assert len(b)==e['bytes'],e['path']
    assert hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
print(json.dumps({'passed':True,'files_checked':len(expected)},sort_keys=True))
