#!/usr/bin/env python3
"""Integrity plus finite-check runner. Trust the external manifest digest."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

MAX_FILE = 2_000_000

def fail(message):
    raise ValueError(message)

def pairs(items):
    d={}
    for k,v in items:
        if k in d:
            fail('duplicate JSON key')
        d[k]=v
    return d

def read_regular(p, limit):
    info=p.lstat()
    if not stat.S_ISREG(info.st_mode) or p.is_symlink():
        fail('not a regular nonsymlink file')
    if info.st_size>limit:
        fail('file size limit')
    return p.read_bytes()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    root=Path(args.packet)
    manifest=Path(args.manifest)
    if root.is_symlink() or not root.is_dir():
        fail('invalid packet root')
    if not re.fullmatch('[0-9a-f]{64}',args.manifest_sha256):
        fail('invalid manifest pin')
    raw=read_regular(manifest,100_000)
    if hashlib.sha256(raw).hexdigest()!=args.manifest_sha256:
        fail('manifest pin mismatch')
    data=json.loads(raw,object_pairs_hook=pairs)
    if type(data) is not dict or set(data)!={'schema','files'} or data['schema']!='boundary-twist-packet-v1':
        fail('invalid manifest schema')
    files=data['files']
    if type(files) is not dict or not 1<=len(files)<=20:
        fail('invalid file map')
    if set(files)!={'REPORT.md','STATUS.json','SOURCES.json','README.md','proof_checks.py','verify.py'}:
        fail('unexpected manifest paths')
    if {p.name for p in root.iterdir()}!=set(files):
        fail('extra or missing packet files')
    for name,rec in files.items():
        if not re.fullmatch('[A-Za-z_][A-Za-z_0-9.]*',name) or '..' in name:
            fail('unsafe path')
        if type(rec) is not dict or set(rec)!={'bytes','sha256'}:
            fail('invalid file record')
        if type(rec['bytes']) is not int or not 0<=rec['bytes']<=MAX_FILE:
            fail('invalid byte count')
        if type(rec['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',rec['sha256']):
            fail('invalid digest')
        content=read_regular(root/name,MAX_FILE)
        if len(content)!=rec['bytes'] or hashlib.sha256(content).hexdigest()!=rec['sha256']:
            fail('file content mismatch: '+name)
    status=json.loads(read_regular(root/'STATUS.json',100_000),object_pairs_hook=pairs)
    if status.get('problem_id')!=11000156 or status.get('turns')!=5 or status.get('main_problem_resolved') is not False or status.get('formal_certification') is not False:
        fail('status scope mismatch')
    flags=['-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize==1 else [])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    out=subprocess.run([sys.executable,*flags,str(root/'proof_checks.py')],capture_output=True,text=True,timeout=30,env=env,check=False)
    if out.returncode:
        fail('finite checks failed')
    result=json.loads(out.stdout,object_pairs_hook=pairs)
    if result.get('main_problem_resolved') is not False or result.get('formal_certification') is not False:
        fail('finite check scope mismatch')
    print(json.dumps({'integrity':'pass','finite_checks':result,'uid':os.geteuid(),'optimize':sys.flags.optimize,'no_formal_certification':True},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,UnicodeError,json.JSONDecodeError,subprocess.SubprocessError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
