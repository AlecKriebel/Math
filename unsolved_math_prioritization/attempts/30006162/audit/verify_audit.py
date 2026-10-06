#!/usr/bin/env python3
"""Externally pinned, strict flat-inventory audit replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

def require(ok, message):
    if not ok:
        raise RuntimeError(message)
def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',required=True)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    root=Path(args.root).absolute()
    require(stat.S_ISDIR(root.lstat().st_mode),'root is not a regular directory')
    require(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256) is not None,'invalid manifest pin')
    inventory={}
    for entry in os.scandir(root):
        require(stat.S_ISREG(entry.stat(follow_symlinks=False).st_mode),'nonregular entry: '+entry.name)
        require(re.fullmatch(r'[A-Za-z0-9_]+\.(md|json|py)',entry.name) is not None,'invalid filename')
        inventory[entry.name]=entry.stat(follow_symlinks=False).st_size
    require('MANIFEST.json' in inventory,'missing manifest')
    raw=(root/'MANIFEST.json').read_bytes()
    require(sha(raw)==args.manifest_sha256,'external manifest pin mismatch')
    manifest=json.loads(raw)
    require(manifest['schema']==1 and manifest['problem_id']==30006162,'manifest schema mismatch')
    records=manifest['files']
    require(isinstance(records,dict) and bool(records),'invalid records')
    require('MANIFEST.json' not in records,'self-manifest record forbidden')
    require(set(inventory)==set(records)|{'MANIFEST.json'},'exact inventory mismatch')
    verified={}
    for name,record in records.items():
        require(re.fullmatch(r'[A-Za-z0-9_]+\.(md|json|py)',name) is not None,'unsafe manifest name')
        data=(root/name).read_bytes()
        require(len(data)==record['bytes'] and sha(data)==record['sha256'],'payload mismatch: '+name)
        verified[name]=data
    require(verified['verify_audit.py']==Path(__file__).read_bytes(),'running verifier source mismatch')
    summary=json.loads(verified['SUMMARY.json'])
    require(summary['verdict']=='PASS_SCOPED_PARTIAL_RESULTS','verdict mismatch')
    require(summary['target_answers']=={'sphere':'unresolved','real_projective_plane':'unresolved'},'answer mismatch')
    require(summary['mandatory_corrections']==[],'unexpected correction state')
    require(summary['approaches_used']==5,'approach count mismatch')
    command=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
    command+=['-c',"exec(compile(bytes.fromhex("+repr(verified['independent_checks.py'].hex())+"), '<verified-independent-checks>', 'exec'), {'__name__':'__main__'})"]
    with tempfile.TemporaryDirectory(prefix='surface-audit-replay-') as td:
        result=subprocess.run(command,cwd=td,text=True,capture_output=True,timeout=90)
    require(result.returncode==0,'verified source execution failed: '+result.stderr)
    actual=json.loads(result.stdout)
    require(actual==json.loads(verified['INDEPENDENT_RESULTS.json']),'independent replay mismatch')
    print(json.dumps({'problem_id':30006162,'status':'PASS','manifest_sha256':args.manifest_sha256,
        'regular_files':len(inventory),'verified_source_execution':True,'exact_inventory':True,
        'independent_results':actual,'scope':'Integrity and finite diagnostics only; both GPP questions unresolved.'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (OSError,ValueError,TypeError,KeyError,RuntimeError,subprocess.TimeoutExpired) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
