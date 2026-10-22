#!/usr/bin/env python3
"""Verify an externally anchored package, then replay its exact diagnostics."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def demand(ok,message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-manifest',required=True)
    args=parser.parse_args()
    demand(re.fullmatch(r'[0-9a-f]{64}',args.expected_manifest) is not None,'Invalid external manifest hash')
    manifest=ROOT/'MANIFEST.json'
    demand(manifest.is_file() and not manifest.is_symlink(),'Missing or symlinked manifest')
    raw=manifest.read_bytes()
    demand(sha(raw)==args.expected_manifest,'Externally pinned manifest mismatch')
    spec=json.loads(raw)
    demand(set(spec)=={'schema','files'} and spec['schema']=='ricci-dimension-30000789-v1','Unexpected manifest schema')
    files=spec['files']; demand(isinstance(files,list),'Manifest file list required')
    names=[]
    for item in files:
        demand(isinstance(item,dict) and set(item)=={'path','bytes','sha256'},'Unexpected file-entry schema')
        name=item['path'];demand(isinstance(name,str) and '/' not in name and '\\' not in name and name not in ('','.','..','MANIFEST.json'),'Unsafe filename')
        demand(isinstance(item['bytes'],int) and item['bytes']>=0,'Invalid byte count')
        demand(isinstance(item['sha256'],str) and re.fullmatch(r'[0-9a-f]{64}',item['sha256']) is not None,'Invalid hash')
        names.append(name)
    demand(names==sorted(set(names)),'Unsorted or duplicate members')
    actual={p.name for p in ROOT.iterdir()}
    demand(actual==set(names)|{'MANIFEST.json'},'Missing or extra package member')
    for item in files:
        p=ROOT/item['path']
        demand(p.is_file() and not p.is_symlink(),'Non-regular or symlinked member')
        data=p.read_bytes()
        demand(len(data)==item['bytes'] and sha(data)==item['sha256'],'Payload integrity mismatch: '+item['path'])
    cmd=[sys.executable,'-B']
    if sys.flags.optimize:
        cmd.append('-O')
    cmd.append(str(ROOT/'math_check.py'))
    run=subprocess.run(cmd,cwd=ROOT.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    demand(run.returncode==0,'Mathematical replay failed: '+run.stderr.decode('utf8','replace'))
    demand(run.stdout==(ROOT/'results.json').read_bytes(),'Exact replay output differs from saved results')
    print(json.dumps({'status':'PASS','members_verified':len(files),'mathematical_results_sha256':sha(run.stdout)},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
