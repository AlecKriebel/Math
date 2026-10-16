#!/usr/bin/env python3
"""Separate read-only check of frozen adjacent inputs; not portable custody."""
import hashlib,json,stat
from pathlib import Path

root=Path(__file__).absolute().parent
receipt=json.loads((root/'ADJACENT_INPUTS.json').read_text())
base=root.parent
checked=[]
for item in receipt['inputs']:
    rel=Path(item['relative_to_adjacent_base'])
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('unsafe input reference')
    path=base/rel
    current=base
    for part in rel.parts:
        current=current/part
        if stat.S_ISLNK(current.lstat().st_mode):
            raise ValueError('symlink in adjacent input path')
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('not a regular adjacent input')
    body=path.read_bytes()
    if len(body)!=item['bytes'] or hashlib.sha256(body).hexdigest()!=item['sha256']:
        raise ValueError('adjacent input mismatch: '+str(rel))
    checked.append(str(rel))
print(json.dumps({'status':'PASS','checked':checked},sort_keys=True))
