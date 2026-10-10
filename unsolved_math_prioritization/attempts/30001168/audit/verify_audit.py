#!/usr/bin/env python3
"""Strict regular-file audit package verifier; no writes or bundle imports."""
from pathlib import Path
import argparse
import hashlib
import json
import stat
import subprocess
import sys

AUTHOR_FILES={
 'APPROACH_LOG.md','MANIFEST.json','PROOF.md','README.md','RESULTS.json',
 'SOURCE_METADATA.json','certificate.py','verify_bundle.py'
}
ROOT_FILES={
 'AUDIT.md','README.md','SOURCE_VERIFICATION.json','INDEPENDENT_RESULTS.json',
 'CONTROL_RESULTS.json','independent_certificate.py','run_audit_controls.py',
 'verify_audit.py'
}
EXPECTED=ROOT_FILES|{'author/'+p for p in AUTHOR_FILES}
AUTHOR_MANIFEST='d7f0d673dce90072e3e5b4fec31a5b002cbbeb9ba885468878ca9d27abe6b33a'


def require(condition,message):
    if not condition:
        raise ValueError(message)


def verify(root):
    require(stat.S_ISDIR(root.lstat().st_mode),'Audit root must be a nonsymlink directory')
    entries=list(root.iterdir())
    require({p.name for p in entries}==ROOT_FILES|{'author','AUDIT_MANIFEST.json'},'Root strict inventory mismatch')
    for p in entries:
        mode=p.lstat().st_mode
        require(stat.S_ISDIR(mode) if p.name=='author' else stat.S_ISREG(mode),'Root nonregular entry: '+p.name)
    children=list((root/'author').iterdir())
    require({p.name for p in children}==AUTHOR_FILES,'Author strict inventory mismatch')
    for p in children:
        require(stat.S_ISREG(p.lstat().st_mode),'Author nonregular entry: '+p.name)
    manifest=json.loads((root/'AUDIT_MANIFEST.json').read_bytes())
    require(set(manifest)=={'schema','problem_id','files'},'Audit manifest keys')
    require(manifest['schema']=='weighted-yamabe-independent-audit-v1','Audit schema')
    require(manifest['problem_id']==30001168,'Audit problem ID')
    records=manifest['files']
    require(isinstance(records,list) and len(records)==len(EXPECTED),'Manifest count')
    require({r['path'] for r in records}==EXPECTED,'Manifest inventory')
    for r in records:
        require(set(r)=={'path','bytes','sha256'},'Manifest record keys')
        b=(root/r['path']).read_bytes()
        require(len(b)==r['bytes'],'Audit byte mismatch: '+r['path'])
        require(hashlib.sha256(b).hexdigest()==r['sha256'],'Audit hash mismatch: '+r['path'])
    require(hashlib.sha256((root/'author/MANIFEST.json').read_bytes()).hexdigest()==AUTHOR_MANIFEST,'Frozen author manifest mismatch')
    base=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
    for script in ['author/verify_bundle.py','independent_certificate.py']:
        p=subprocess.run(base+[str(root/script)],cwd=root.parent,capture_output=True,text=True,timeout=60)
        require(p.returncode==0,'Child verifier failed: '+p.stderr)
        require(not p.stderr,'Child stderr')
        if script=='independent_certificate.py':
            require(p.stdout==(root/'INDEPENDENT_RESULTS.json').read_text(),'Independent output mismatch')
        else:
            author_result=json.loads(p.stdout)
            require(author_result['verified'] and author_result['arithmetic_checks']==613,'Author output mismatch')
    return {'verified':True,'optimized':bool(sys.flags.optimize),'problem_id':30001168,
      'payload_files':len(EXPECTED),'author_arithmetic_checks':613,'independent_round_cells':200,
      'manifest_sha256':hashlib.sha256((root/'AUDIT_MANIFEST.json').read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).absolute().parent)
    a=p.parse_args()
    print(json.dumps(verify(a.root.absolute()),indent=2,sort_keys=True))
