#!/usr/bin/env python3
"""Validate the audit freeze, then replay its independent arithmetic reconstruction."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise ValueError(msg)

def sha(raw): return hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author',type=Path,default=HERE.parent/'root_unity_30004334')
    ap.add_argument('--expected-audit-manifest')
    ap.add_argument('--integrity-only',action='store_true')
    args=ap.parse_args()
    path=HERE/'AUDIT_MANIFEST.json'
    need(not path.is_symlink(),'audit manifest symlink')
    raw=path.read_bytes(); pin=sha(raw)
    if args.expected_audit_manifest: need(pin==args.expected_audit_manifest.lower(),'audit manifest pin mismatch')
    manifest=json.loads(raw)
    need(manifest['schema']=='root-unity-independent-audit-manifest-v1','audit manifest schema')
    names=[f['path'] for f in manifest['files']]
    need(len(names)==len(set(names)) and all('/' not in n and '\\' not in n and n not in ('.','..','AUDIT_MANIFEST.json') for n in names),'unsafe or duplicated audit path')
    actual=set()
    for p in HERE.rglob('*'):
        need(not p.is_symlink(),'audit symlink')
        if p.is_file(): actual.add(p.relative_to(HERE).as_posix())
    need(actual==set(names)|{'AUDIT_MANIFEST.json'},'audit inventory mismatch')
    for f in manifest['files']:
        b=(HERE/f['path']).read_bytes()
        need(len(b)==f['bytes'] and sha(b)==f['sha256'],'audit payload hash mismatch: '+f['path'])
    result={'status':'PASS','audit_manifest_sha256':pin,'audit_inventory_and_hashes_verified':True}
    if not args.integrity_only:
        p=subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),str(HERE/'independent_verify.py'),'--author',str(args.author.resolve())],capture_output=True,text=True,timeout=180)
        need(p.returncode==0,'independent replay failed: '+p.stderr)
        observed=json.loads(p.stdout)
        need(observed==json.loads((HERE/'INDEPENDENT_RESULTS.json').read_text()),'independent results differ')
        result['independent_reconstruction']='PASS'
        result['author_manifest_sha256']=observed['author_manifest_sha256']
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
