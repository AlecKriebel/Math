#!/usr/bin/env python3
"""Verify an externally bound manifest and replay arithmetic in ordinary and -O mode."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    allowed=set(manifest['files']) | {'MANIFEST.json'}
    present={p.name for p in ROOT.iterdir() if p.is_file()}
    require(present==allowed,'Release file set differs from manifest')
    for name,meta in manifest['files'].items():
        require(Path(name).name==name,'Nonlocal manifest path')
        b=(ROOT/name).read_bytes()
        require(len(b)==meta['bytes'],'Byte count mismatch: '+name)
        require(hashlib.sha256(b).hexdigest()==meta['sha256'],'Hash mismatch: '+name)
    claims=json.loads((ROOT/'CLAIMS.json').read_text())
    require(claims['problem_id']=='30003230' and claims['general_status']=='unresolved','Target/status changed')
    require(claims['approaches_completed']==5 and claims['novelty_claim'] is False,'Scope changed')
    expected=(ROOT/'RESULTS.json').read_bytes()
    modes=[]
    for flags in ([],['-O']):
        child=subprocess.run([sys.executable,*flags,str(ROOT/'verify.py')],capture_output=True,check=True)
        require(child.stdout==expected,'Replay bytes changed in mode '+str(flags))
        require(not child.stderr,'Verifier emitted stderr')
        modes.append('optimized' if flags else 'ordinary')
    result=json.loads(expected)
    require(result['general_result']=='unresolved' and result['formal_proof_certificate'] is False,'Verifier scope changed')
    print(json.dumps({'packet_verified':True,'file_count':len(manifest['files']),'modes':modes,'exact_checks':result['total_exact_checks'],'negative_controls':result['negative_control_count'],'general_status':claims['general_status']},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
