#!/usr/bin/env python3
"""Portable exact-binding and replay audit; no external data or network needed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

EXPECTED_AUTHOR_MANIFEST='05a9835d5c4c302afe24c47d6143096301ce658e7bd29e4fef884f2c2a2705c8'
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--author',type=Path,default=root.parent/'author',help='Directory of the unchanged original 12-file author packet')
args=parser.parse_args()
author=args.author.resolve()

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(folder,excluded=()):
    out={}
    for p in folder.iterdir():
        assert not p.is_symlink(),f'Symlink is not allowed: {p.name}'
        assert p.is_file(),f'Unexpected non-file: {p.name}'
        if p.name not in excluded:out[p.name]={'sha256':digest(p),'bytes':p.stat().st_size}
    return out

binding=json.loads((root/'AUTHOR_BINDING.json').read_text())
assert binding['author_manifest_sha256']==EXPECTED_AUTHOR_MANIFEST
assert digest(author/'SHA256SUMS.json')==EXPECTED_AUTHOR_MANIFEST
assert inventory(author)==binding['files'],'Original author packet changed'
assert len(binding['files'])==12
own=json.loads((root/'AUDIT_SHA256SUMS.json').read_text())
assert own['author_manifest_sha256']==EXPECTED_AUTHOR_MANIFEST
assert inventory(root,('AUDIT_SHA256SUMS.json',))==own['files'],'Audit payload changed'
status=json.loads((root/'AUDIT_STATUS.json').read_text())
assert status['author_status']=='unsolved' and status['attempt_turns']==5
assert status['prior_announcement_hold'] and not status['exact_resolution']
assert not status['target_counterexample'] and not status['expert_peer_review']
assert status['independent_finite_controls']==655
for p in root.iterdir():
    assert p.suffix not in {'.pdf','.html','.sqlite','.zip','.tar','.gz'},'Excluded source/archive file'

results=[]
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
for directory,script in [(author,'verify_manifest.py'),(author,'verify_controls.py'),(root,'independent_controls.py')]:
    run=subprocess.run([sys.executable,'-B',script],cwd=directory,env=env,text=True,capture_output=True,check=True)
    results.append({'script':script,'exit_code':run.returncode,'stdout':run.stdout.strip(),'stderr':run.stderr})
assert {'all_replays_pass':True,'runs':results}==json.loads((root/'REPLAY_RESULTS.json').read_text())
assert inventory(author)==binding['files'],'Replay mutated author packet'
assert inventory(root,('AUDIT_SHA256SUMS.json',))==own['files'],'Replay mutated audit packet'
print(json.dumps({'audit_manifest_valid':True,'author_manifest_sha256':EXPECTED_AUTHOR_MANIFEST,'author_files_checked':12,'audit_payload_files_checked':len(own['files']),'all_replays_pass':True,'independent_controls':655,'verdict':'pass_unresolved_checkpoint'},sort_keys=True))
