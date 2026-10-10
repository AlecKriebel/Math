#!/usr/bin/env python3
"""Offline manifest integrity and exact finite-control replay."""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
manifest_path=ROOT/'MANIFEST.json'
expected_hash=(ROOT/'MANIFEST.sha256').read_text().strip().split()[0]
assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==expected_hash, 'manifest hash mismatch'
manifest=json.loads(manifest_path.read_text())
assert manifest['release_kind']=='new_reconstruction_not_historical_recovery'
assert manifest['original_problem_status']=='unsolved'
assert manifest['independent_review_status']=='pending'
assert manifest['historical_attempt_budget']=='5/5_reported_not_replayed'
expected=set()
for item in manifest['files']:
    path=ROOT/item['path']
    assert path.is_file() and not path.is_symlink(), item['path']
    assert path.resolve().is_relative_to(ROOT), 'unsafe manifest path'
    data=path.read_bytes()
    assert len(data)==item['bytes'], (item['path'],'byte count')
    assert hashlib.sha256(data).hexdigest()==item['sha256'], (item['path'],'SHA-256')
    expected.add(item['path'])
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
assert actual==expected|{'MANIFEST.json','MANIFEST.sha256'}, ('unexpected file set',actual^expected)
out=subprocess.check_output([sys.executable,str(ROOT/'replay_controls.py')],cwd=ROOT)
assert out==(ROOT/'REPLAY_EXPECTED.json').read_bytes(), 'finite replay receipt differs'
result={'status':'PASS_MANIFEST_AND_FINITE_REPLAY','manifest_sha256':expected_hash,
        'verified_payload_files':len(expected),
        'finite_control_status':json.loads(out)['status'],
        'finite_control_assertions':json.loads(out)['total_assertions'],
        'mathematical_review':'pending; not mechanically certified',
        'original_problem':'unsolved'}
print(json.dumps(result,indent=2,sort_keys=True))
