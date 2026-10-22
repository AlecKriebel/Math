#!/usr/bin/env python3
"""Authenticate this file externally before running; pinned source-free payload gate."""
import argparse
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import re
import stat
import subprocess
import sys
MANIFEST_SHA256='24e4e0b001028a38091b1293b490e36227fda8d2ee73f726ef316f2eb0fe4c96'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def no_constant(c):raise ValueError('nonfinite JSON constant')
def digest(p):
    b=p.read_bytes();return len(b),hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args()
    need(not args.root.is_symlink(),'symlink root');root=args.root.resolve();need(root.is_dir(),'missing root')
    files=set();dirs=set()
    for base,dd,ff in os.walk(root,followlinks=False):
        for name in dd+ff:
            p=Path(base)/name;mode=p.lstat().st_mode;rel=p.relative_to(root).as_posix();need(not stat.S_ISLNK(mode),'symlink member')
            if stat.S_ISDIR(mode):dirs.add(rel)
            elif stat.S_ISREG(mode):files.add(rel)
            else:raise ValueError('nonregular member')
    need(dirs=={'packet'},'directory inventory mismatch')
    mf=root/'MANIFEST.json';need(mf.is_file(),'manifest missing');raw=mf.read_bytes();need(len(raw)<1_000_000 and hashlib.sha256(raw).hexdigest()==MANIFEST_SHA256,'external manifest pin mismatch')
    m=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=no_constant)
    need(type(m) is dict and set(m)=={'schema','problem_id','files'},'manifest schema')
    need(m['schema']=='short-geodesics-author-manifest-v1' and type(m['problem_id']) is int and m['problem_id']==10300043,'manifest identity')
    need(type(m['files']) is dict and len(m['files'])>0,'manifest file list')
    need(files==set(m['files'])|{'MANIFEST.json','bootstrap.py'},'file inventory mismatch')
    need(digest(root/'bootstrap.py')==digest(Path(__file__).resolve()),'candidate bootstrap differs from authenticated launcher')
    for rel,pin in m['files'].items():
        parts=PurePosixPath(rel).parts
        need(type(rel) is str and ((len(parts)==2 and parts[0]=='packet') or rel=='controls.py') and str(PurePosixPath(rel))==rel and '..' not in parts and not PurePosixPath(rel).is_absolute(),'unsafe manifest path')
        need(type(pin) is dict and set(pin)=={'bytes','sha256'},'member pin schema')
        need(type(pin['bytes']) is int and pin['bytes']>=0 and type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}',pin['sha256']) is not None,'member pin value')
        need(digest(root/rel)==(pin['bytes'],pin['sha256']),'payload hash mismatch: '+rel)
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'packet/verify.py')],capture_output=True,text=True,timeout=90)
    need(p.returncode==0 and p.stderr=='','authenticated verifier failed')
    result=json.loads(p.stdout,object_pairs_hook=pairs,parse_constant=no_constant)
    need(result['status']=='PASS_SCOPED_REGRESSIONS' and result['general_solution'] is False and result['topological_proof_machine_verified'] is False,'verifier scope mismatch')
    print(json.dumps({'status':'PASS_AUTHENTICATED_SOURCE_FREE_PACKET','manifest_sha256':MANIFEST_SHA256,'authenticated_files':len(m['files']),'result':result},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError,subprocess.SubprocessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
