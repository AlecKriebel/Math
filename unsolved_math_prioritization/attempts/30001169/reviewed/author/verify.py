#!/usr/bin/env python3
"""Fail-closed flat inventory, SHA-256 checks, and exact certificate replay."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

EXPECTED={'README.md','proof.md','certificate.py','claim.json','RESULTS.json','PUBLIC_METADATA.json','exploratory.py','EXPLORATORY_RESULTS.json','verify.py','MANIFEST.json'}

def require(value,message):
    if not value:
        raise ValueError(message)

def main():
    root=Path(__file__).resolve().parent
    nodes=list(os.scandir(root))
    require({x.name for x in nodes}==EXPECTED,'unexpected or missing inventory node')
    for node in nodes:
        require(stat.S_ISREG(node.stat(follow_symlinks=False).st_mode),'nonregular node rejected')
        require(not node.name.endswith(('.pyc','.pyo')),'bytecode rejected')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(manifest['schema']=='flat-sha256-v1','manifest schema')
    require(set(manifest['files'])==EXPECTED-{'MANIFEST.json'},'manifest inventory')
    for name,entry in manifest['files'].items():
        raw=(root/name).read_bytes()
        require(len(raw)==entry['bytes'],'byte count: '+name)
        require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'hash: '+name)
    flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
    run=subprocess.run([sys.executable,*flags,str(root/'certificate.py')],capture_output=True,text=True,check=True)
    result=json.loads(run.stdout)
    require(result==json.loads((root/'RESULTS.json').read_text()),'result replay mismatch')
    require(result['status']=='partial_unresolved','forbidden resolution claim')
    require(json.loads((root/'EXPLORATORY_RESULTS.json').read_text())['certified_signs'] is False,'exploration overclaim')
    print(json.dumps({'inventory_files':len(EXPECTED),'status':'PASS','optimized':bool(sys.flags.optimize),'mathematical_status':'partial_unresolved'},sort_keys=True))

if __name__=='__main__':
    main()
