#!/usr/bin/env python3
"""Read-only replay of the safe audit; optional original packet verification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--original-safe',type=Path)
args=parser.parse_args()
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
manifest_sha=hashlib.sha256((base/'MANIFEST.json').read_bytes()).hexdigest()
assert (base/'MANIFEST.sha256').read_text().split()[0]==manifest_sha
for entry in manifest['allowlisted_files']:
    payload=(base/entry['path']).read_bytes()
    assert len(payload)==entry['bytes'],entry['path']
    assert hashlib.sha256(payload).hexdigest()==entry['sha256'],entry['path']
actual={p.name for p in base.iterdir() if p.is_file()}
expected={e['path'] for e in manifest['allowlisted_files']}|{'MANIFEST.json','MANIFEST.sha256'}
assert actual==expected,(actual-expected,expected-actual)
assert not any(p.is_dir() for p in base.iterdir())
run=subprocess.run([sys.executable,str(base/'independent_controls.py')],capture_output=True,text=True,check=True)
assert not run.stderr
replayed=json.loads(run.stdout)
assert replayed==json.loads((base/'independent_results.json').read_text())
assert replayed['independent_check_count']==len(replayed['checks'])==115
assert all(c['passed'] for c in replayed['checks'])
original_verified=False
if args.original_safe:
    source=args.original_safe
    bindings=json.loads((base/'input_bindings.json').read_text())
    m=(source/'MANIFEST.json').read_bytes()
    assert hashlib.sha256(m).hexdigest()==bindings['frozen_manifest_sha256']
    for entry in bindings['files']:
        data=(source/entry['path']).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
    replay=subprocess.run([sys.executable,str(source/'verify_exact.py')],capture_output=True,text=True,check=True)
    expected_author=json.loads((base/'author_replay.json').read_text())['replay']
    assert json.loads(replay.stdout)==expected_author==json.loads((source/'verification_results.json').read_text())
    assert not replay.stderr
    original_verified=True
print(json.dumps({'status':'passed','manifest_sha256':manifest_sha,'safe_payload_count':len(manifest['allowlisted_files']),'independent_checks':115,'negative_controls':len(replayed['negative_controls']),'original_packet_reverified':original_verified,'writes_performed':False},indent=2))
