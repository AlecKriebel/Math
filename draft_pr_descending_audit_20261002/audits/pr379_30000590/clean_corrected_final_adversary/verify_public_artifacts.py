#!/usr/bin/env python3
"""Quiet, read-only validation of the explicit owned artifact whitelist."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).absolute().parent
m=json.loads((HERE/'ARTIFACT_MANIFEST.json').read_bytes())
assert m['candidate_head']=='4ee3016a755bb3553e712716dcd26b3d031836d0'
paths=set()
for e in m['files']:
    rel=Path(e['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    assert rel.parts[0] not in {'raw_sources','private_replay'}
    assert rel.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.gif','.webp'}
    assert e['path'] not in paths
    paths.add(e['path'])
    b=(HERE/rel).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).parts[0] not in {'raw_sources','private_replay'}}
assert actual==paths|{'ARTIFACT_MANIFEST.json'},sorted(actual^(paths|{'ARTIFACT_MANIFEST.json'}))
assert len(paths)==m['file_count']
for filename,key in [('SOURCE_FIRST_SEAL.json','sealed_files')]:
    seal=json.loads((HERE/filename).read_bytes())
    for name,sha in seal[key].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha
seal=json.loads((HERE/'MATHEMATICAL_VERDICT_SEAL.json').read_bytes())
assert hashlib.sha256((HERE/'MATHEMATICAL_VERDICT_SEALED.md').read_bytes()).hexdigest()==seal['sha256']
for name in ['exact_head.stdout.json','replay_all.stdout.json','replay_old_objects.stdout.json','fresh_adversarial_controls.stdout.json']:
    assert json.loads((HERE/name).read_bytes())['status']=='PASS'
assert not (HERE/'exact_head.stderr.txt').read_bytes()
assert not (HERE/'replay_all.stderr.txt').read_bytes()
assert not (HERE/'replay_old_objects.stderr.txt').read_bytes()
assert not (HERE/'fresh_adversarial_controls.stderr.txt').read_bytes()
