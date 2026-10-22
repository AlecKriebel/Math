#!/usr/bin/env python3
"""Read-only custody verification; this does not test mathematical correctness."""
from pathlib import Path
import hashlib,json,subprocess

base=Path(__file__).resolve().parent
r=json.loads((base/'READ_RECEIPT.json').read_text())
if r.get('schema')!='priority-family-read-receipt-v1':
    raise ValueError('Unexpected receipt schema')
seen=set()
for row in r['pins']:
    rel=row['path']
    if rel in seen or Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ValueError('Unsafe or duplicate pinned path: '+rel)
    seen.add(rel)
    f=base/rel
    if f.is_symlink() or not f.is_file() or not f.resolve().is_relative_to(base):
        raise ValueError('Pinned file missing or escaped: '+rel)
    data=f.read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise ValueError('Byte/hash mismatch: '+rel)
    if rel.startswith(('sources/private/','private/')):
        c=subprocess.run(['git','check-ignore','--no-index','-q',str(f)],cwd=base,capture_output=True)
        if c.returncode!=0:
            raise ValueError('External/private input is not ignored: '+rel)
print(json.dumps({'status':'PASS','pinned_files':len(seen),'custody_only':True},sort_keys=True))
