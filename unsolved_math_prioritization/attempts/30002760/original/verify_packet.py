#!/usr/bin/env python3
"""Validate the frozen allowlist, bytes, mathematical receipt and negative controls."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def need(ok,label):
    if not ok:
        raise ValueError(label)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:
            raise ValueError('Duplicate JSON key: '+k)
        out[k]=v
    return out

def main(integrity_only):
    mp=ROOT/'FROZEN_MANIFEST.json'
    manifest=json.loads(mp.read_text(),object_pairs_hook=unique_object)
    need(set(manifest)=={'schema','files'},'Unexpected manifest schema')
    need(manifest['schema']=='sha256-byte-manifest-v1','Wrong manifest version')
    need(isinstance(manifest['files'],dict) and len(manifest['files'])>0,'Empty manifest')
    expected=set(manifest['files'])|{'FROZEN_MANIFEST.json'}
    actual=set()
    for p in ROOT.iterdir():
        need(p.is_file() and not p.is_symlink(),'Unexpected directory or symlink: '+p.name)
        actual.add(p.name)
    need(actual==expected,'Manifest allowlist mismatch')
    for name,binding in sorted(manifest['files'].items()):
        need(name==Path(name).name and name not in {'.','..'},'Unsafe manifest name')
        need(set(binding)=={'bytes','sha256'},'Wrong file binding schema')
        need(type(binding['bytes']) is int and binding['bytes']>=0,'Invalid byte count')
        need(isinstance(binding['sha256'],str) and len(binding['sha256'])==64,'Invalid digest')
        data=(ROOT/name).read_bytes()
        need(len(data)==binding['bytes'],'Byte count mismatch: '+name)
        need(hashlib.sha256(data).hexdigest()==binding['sha256'],'Digest mismatch: '+name)
        need(Path(name).suffix in {'.md','.json','.py'},'Non-source-free artifact type: '+name)
    for name in ['verify_math.py','test_fail_closed.py','verify_packet.py','test_integrity.py']:
        tree=ast.parse((ROOT/name).read_text())
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'Optimizable assertion in '+name)
    if integrity_only:
        print(json.dumps({'status':'PASS_INTEGRITY_ONLY','files':len(manifest['files'])},sort_keys=True))
        return
    math_controls = None
    for program,receipt in [('verify_math.py','CHECK_RESULTS.json'),('test_fail_closed.py','FAIL_CLOSED_RESULTS.json'),('test_integrity.py','INTEGRITY_RESULTS.json')]:
        result=subprocess.run([sys.executable,str(ROOT/program)],capture_output=True,text=True)
        need(result.returncode==0,program+' failed: '+result.stderr)
        need(result.stdout==(ROOT/receipt).read_text(),program+' receipt mismatch')
        if program == 'verify_math.py':
            parsed = json.loads(result.stdout, object_pairs_hook=unique_object)
            math_controls = parsed['total_checks']
            need(type(math_controls) is int and math_controls == sum(parsed['counts'].values()), 'Control count mismatch')
    print(json.dumps({'status':'PASS_FROZEN_PACKET','bound_files':len(manifest['files']),'mathematical_controls':math_controls,'full_resolution':False,'external_source_retrieval_replayed':False},indent=2,sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--integrity-only',action='store_true')
    args=parser.parse_args()
    try:
        main(args.integrity_only)
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(1)
