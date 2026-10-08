#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
for item in manifest['files']:
    p=root/item['path']; data=p.read_bytes()
    assert len(data)==item['bytes'],(item['path'],'size')
    assert hashlib.sha256(data).hexdigest()==item['sha256'],(item['path'],'sha256')
print(json.dumps({'status':'PASS','verified_files':len(manifest['files'])},sort_keys=True))
