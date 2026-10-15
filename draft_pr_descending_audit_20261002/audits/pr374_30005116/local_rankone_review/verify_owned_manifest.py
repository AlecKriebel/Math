#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).absolute().parent
manifest=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
assert manifest['frozen_head']=='c683fc4b84266a6a153c087e182cf427ed502d6c'
for item in manifest['public_files']:
    p=Path(item['path'])
    assert p.name==item['path'] and p.name!='PUBLIC_MANIFEST.json'
    assert p.suffix not in ('.pdf','.png','.pyc')
    data=(root/p).read_bytes()
    assert len(data)==item['bytes']
    assert hashlib.sha256(data).hexdigest()==item['sha256'],p
assert not (root/'__pycache__').exists()
print('PASS:',len(manifest['public_files']),'owned public files; all hashes match; raw/private tmp excluded')
