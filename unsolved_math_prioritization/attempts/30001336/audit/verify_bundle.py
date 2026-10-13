#!/usr/bin/env python3
"""Read-only strict inventory. Use an externally trusted manifest hash first."""
import hashlib,json,pathlib,stat

root=pathlib.Path(__file__).absolute().parent
manifest=root/'MANIFEST.json'
if not stat.S_ISREG(manifest.lstat().st_mode): raise RuntimeError('Nonregular manifest')
raw=manifest.read_bytes();data=json.loads(raw)
if data.get('format')!='rooted-tree-independent-audit-v1': raise RuntimeError('Wrong manifest format')
entries=data['files'];names=[e['path'] for e in entries]
if len(set(names))!=len(names): raise RuntimeError('Duplicate entries')
if any(not isinstance(n,str) or '/' in n or '\\' in n or n in ('','.','..','MANIFEST.json') for n in names): raise RuntimeError('Unsafe path')
if {p.name for p in root.iterdir()}!=set(names)|{'MANIFEST.json'}: raise RuntimeError('Strict inventory mismatch')
for entry in entries:
    path=root/entry['path']
    if not stat.S_ISREG(path.lstat().st_mode): raise RuntimeError('Nonregular entry')
    payload=path.read_bytes()
    if len(payload)!=entry['bytes'] or hashlib.sha256(payload).hexdigest()!=entry['sha256']: raise RuntimeError('Changed bytes '+entry['path'])
print(json.dumps({'status':'PASS_STRICT_AUDIT_INVENTORY','files':len(entries)+1,'manifest_sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True,indent=2))
