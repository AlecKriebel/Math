#!/usr/bin/env python3
"""Verify this immutable, separate v2 delta acceptance package."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'ACCEPTANCE_MANIFEST.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='ACCEPTANCE_MANIFEST.json'}
expected={x['path'] for x in m['files']}
assert actual==expected
for item in m['files']:
 p=root/item['path'];assert not p.is_symlink()
 b=p.read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
assert m['decision']=='accepted_exact_v2_delta'
assert m['accepted_author_archive_sha256']=='897360dd152d57c8d3ac10043fdb28b889e7206509eec56f6cb9a1dadbd71823'
print(json.dumps({'ok':True,'decision':m['decision'],'file_count':len(expected)+1},sort_keys=True))
