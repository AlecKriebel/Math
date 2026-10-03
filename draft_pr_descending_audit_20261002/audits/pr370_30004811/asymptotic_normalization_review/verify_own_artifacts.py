#!/usr/bin/env python3
"""Verify the exact own-root allowlist; never walk or publish sibling/private files."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
assert manifest['root']=='.'
assert manifest['self_excluded']=='PUBLIC_MANIFEST.json'
seen=set()
for entry in manifest['files']:
    rel=Path(entry['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    assert len(rel.parts)==1 and rel.name!='PUBLIC_MANIFEST.json'
    assert rel.name not in seen;seen.add(rel.name)
    path=root/rel
    assert not path.is_symlink() and path.is_file()
    data=path.read_bytes()
    assert len(data)==entry['bytes']
    assert hashlib.sha256(data).hexdigest()==entry['sha256']
for path in root.iterdir():
    if path.name in ('private','__pycache__','PUBLIC_MANIFEST.json'):
        continue
    assert path.is_file() and not path.is_symlink() and path.name in seen
for sealname in ('SOURCE_FIRST_BASELINE_SEAL.json','INDEPENDENT_VERDICT_SEAL.json'):
    seal=json.loads((root/sealname).read_text())
    assert hashlib.sha256((root/seal['artifact']).read_bytes()).hexdigest()==seal['sha256']
print(json.dumps({'status':'PASS','own_root_only':True,'self_excluded':True,'manifest_file_count':len(seen),'private_sources_and_replay_excluded':True,'independence_seals_unchanged':True},indent=2))
