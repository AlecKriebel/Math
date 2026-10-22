#!/usr/bin/env python3
"""Verify audit consistency, pinned originals, correction replay, and exact controls.

Usage: python3 -B verify_audit.py ORIGINAL_RELEASE [EXPECTED_AUDIT_MANIFEST_SHA256]
The optional digest must come from a separately trusted record, not this bundle.
"""
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
AUTHOR_SHA='ce4ff19beb1fa50a1ba6f504bd1373943b355171e932f39ba1a4770ccbf7ad30'
PROOF_SHA='30d352188a97a117b29079ff714acdae753ef4f5bbdb5d350d80662f0cb08115'

def fail(message):
    raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root, manifest_name):
    path=root/manifest_name
    if path.is_symlink() or not path.is_file():
        fail('Manifest must be a regular nonsymlink file')
    raw=path.read_bytes()
    man=json.loads(raw)
    if set(p.name for p in root.iterdir())!=set(man['files'])|{manifest_name}:
        fail('Inventory mismatch')
    for name,meta in man['files'].items():
        if PurePosixPath(name).name!=name or name in ('.','..'):
            fail('Unsafe manifest filename')
        f=root/name
        if f.is_symlink() or not f.is_file():
            fail('Nonregular payload: '+name)
        b=f.read_bytes()
        if len(b)!=meta['bytes'] or digest(b)!=meta['sha256']:
            fail('Payload mismatch: '+name)
    return raw,man

if len(sys.argv) not in (2,3):
    fail('Supply the original release directory and optionally the trusted audit manifest digest')
audit_raw,audit=inventory(ROOT,'AUDIT_MANIFEST.json')
if len(sys.argv)==3 and digest(audit_raw)!=sys.argv[2]:
    fail('Audit manifest does not match trusted digest')
if audit.get('schema')!='borderline-soliton-independent-audit-v1':
    fail('Wrong audit schema')
original=Path(sys.argv[1]).resolve()
original_raw,author=inventory(original,'AUTHOR_MANIFEST.json')
if digest(original_raw)!=AUTHOR_SHA:
    fail('Original author manifest does not match pinned digest')
proof=(original/'PARTIAL_RESULTS.md').read_bytes()
if digest(proof)!=PROOF_SHA:
    fail('Original proof does not match pinned digest')
old=proof.decode().splitlines(True)
new=(ROOT/'PARTIAL_RESULTS.corrected.md').read_text().splitlines(True)
patch=''.join(difflib.unified_diff(old,new,fromfile='a/PARTIAL_RESULTS.md',tofile='b/PARTIAL_RESULTS.md'))
if patch.encode()!=(ROOT/'CORRECTION.patch').read_bytes():
    fail('Correction patch does not exactly describe the corrected proof')

env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
env.pop('PYTHONOPTIMIZE',None)
replays=[]
for root,script,result in [(original,'check_algebra.py','CHECK_RESULTS.json'),
                           (ROOT,'independent_controls.py','INDEPENDENT_RESULTS.json')]:
    for optimize in (False,True):
        command=[sys.executable,'-B']+(['-O'] if optimize else [])+[str(root/script)]
        run=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=120)
        if run.returncode or run.stdout!=(root/result).read_bytes():
            fail(f'Replay mismatch for {script}, optimized={optimize}: {run.stderr.decode()}')
        replays.append({'script':script,'optimized':optimize,'sha256':digest(run.stdout)})

print(json.dumps({'status':'PASS','audit_manifest_sha256':digest(audit_raw),
                  'audit_digest_authenticated':len(sys.argv)==3,
                  'author_manifest_sha256':AUTHOR_SHA,'original_proof_sha256':PROOF_SHA,
                  'corrected_proof_sha256':digest((ROOT/'PARTIAL_RESULTS.corrected.md').read_bytes()),
                  'replays':replays,'disposition':'unsolved','turns':'5/5',
                  'scope':'Consistency and exact-control replay; mathematical conclusions are conditional as stated in FULL_AUDIT.md.'},indent=2,sort_keys=True))
