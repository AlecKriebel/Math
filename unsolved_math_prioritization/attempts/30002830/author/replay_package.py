#!/usr/bin/env python3
"""Fail-closed local integrity and symbolic replay. No remote actions."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser();p.add_argument('--integrity-only',action='store_true');args=p.parse_args()
root=Path(__file__).resolve().parent

def require(condition, message):
    if not condition:raise RuntimeError(message)

sha_line=(root/'MANIFEST.sha256').read_text().strip().split()
require(len(sha_line)==2 and sha_line[1]=='MANIFEST.json','invalid manifest checksum binding')
manifest_bytes=(root/'MANIFEST.json').read_bytes()
require(hashlib.sha256(manifest_bytes).hexdigest()==sha_line[0],'manifest hash mismatch')
manifest=json.loads(manifest_bytes)
require(manifest['target_id']=='30002830','wrong target')
names=[]
for item in manifest['allowlisted_files']:
    name=item['path'];require(Path(name).name==name and name not in names,'invalid manifest path')
    names.append(name);f=root/name
    require(f.is_file() and not f.is_symlink(),'missing or nonregular file: '+name)
    b=f.read_bytes()
    require(len(b)==item['bytes'],'byte count mismatch: '+name)
    require(hashlib.sha256(b).hexdigest()==item['sha256'],'file hash mismatch: '+name)
require(set(q.name for q in root.iterdir())==set(names)|{'MANIFEST.json','MANIFEST.sha256'},'unmanifested or missing entries')
if not args.integrity_only:
    result=subprocess.run([sys.executable,str(root/'verify_exact.py')],capture_output=True,text=True,check=True)
    require(json.loads(result.stdout)==json.loads((root/'verification_results.json').read_text()),'symbolic replay differs')
print(json.dumps({'target_id':'30002830','integrity_passed':True,'symbolic_replay_passed':not args.integrity_only,'files_verified':len(names)}))
