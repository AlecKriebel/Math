#!/usr/bin/env python3
"""Fail-closed exact-file verifier; anchor must be supplied externally."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    args=parser.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.expected_manifest) is not None,'invalid anchor')
    root=Path(__file__).resolve().parent
    manifest=root/'MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(),'missing or symlink manifest')
    raw=manifest.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==args.expected_manifest,'manifest anchor mismatch')
    obj=json.loads(raw)
    require(set(obj)=={'schema','files'} and obj['schema']=='exact-file-manifest-v1','bad manifest schema')
    files=obj['files']
    require(isinstance(files,dict) and files,'empty manifest')
    require(set(p.name for p in root.iterdir())==set(files)|{'MANIFEST.json'},'unexpected or missing member')
    for name,entry in files.items():
        require(Path(name).name==name and name not in {'.','..','MANIFEST.json'},'unsafe member')
        require(set(entry)=={'bytes','sha256'},'bad member schema')
        p=root/name
        require(p.is_file() and not p.is_symlink(),'not regular member')
        b=p.read_bytes()
        require(len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'],'member hash mismatch: '+name)
    proc=subprocess.run([sys.executable,'-B',str(root/'math_check.py')],capture_output=True)
    require(proc.returncode==0,'mathematical checker failed')
    require(proc.stdout==(root/'results.json').read_bytes(),'result replay mismatch')
    metadata=json.loads((root/'PUBLIC_METADATA.json').read_text())
    require(metadata['problem_id']==30001006,'wrong problem')
    require(metadata['substantive_new_approaches']==1,'wrong approach count')
    require(metadata['problem_solved'] is False,'overstated solution status')
    require(metadata['independent_audit_status']=='pending','unexpected audit status')
    print(json.dumps({'status':'PASS','members':len(files)+1,'math_replay':'exact byte match'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
