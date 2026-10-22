#!/usr/bin/env python3
"""Portable audit verification. Optional argument: frozen author archive path."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
entries=manifest['files']
assert manifest['format']=='audit-sha256-allowlist-v1'
names=[r['path'] for r in entries]
assert len(names)==len(set(names))
for r in entries:
 p=PurePosixPath(r['path'])
 assert not p.is_absolute() and '..' not in p.parts and str(p)==r['path']
 assert r['path']!='MANIFEST.json'
actual=set()
for p in root.rglob('*'):
 assert not p.is_symlink(),str(p)
 if p.is_file() and p!=root/'MANIFEST.json':actual.add(p.relative_to(root).as_posix())
assert actual==set(names)
for r in entries:
 d=(root/r['path']).read_bytes()
 assert len(d)==r['bytes'] and hashlib.sha256(d).hexdigest()==r['sha256'],r['path']
replay=subprocess.check_output([sys.executable,str(root/'independent_verify.py')])
assert replay==(root/'INDEPENDENT_RESULTS.json').read_bytes()
checked=False
if len(sys.argv)>1:
 binding=json.loads((root/'AUDIT_BINDING.json').read_text())['author_archive']
 d=Path(sys.argv[1]).read_bytes()
 assert len(d)==binding['bytes'] and hashlib.sha256(d).hexdigest()==binding['sha256']
 checked=True
print(json.dumps({'status':'PASS','files':len(entries),'independent_replay_byte_match':True,'author_archive_checked':checked},sort_keys=True))
