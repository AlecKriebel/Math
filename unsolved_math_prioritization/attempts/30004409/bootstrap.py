#!/usr/bin/env python3
"""Externally anchor the complete authored proof-and-audit delivery.
Copy to a trusted external location and verify its published SHA-256 before use.
Normal, -O and -OO all use explicit guards. No integrity-bypass mode exists.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

MANIFEST_SHA256 = '723ece0f5e26b04db0e6e4272b361f175ef17504833f89bafefaa4d0bc7aebd5'
VERIFIER_PIN = {'bytes': 11278, 'sha256': '0a49b2e77f254e7c1587b6c575900fc0d15e6cd797ea5b9d25a0a7c039cb492a', 'git_blob': '824dab8936a768a91411b28191aa70b2164cb241'}

def need(ok, label):
    if not ok: raise ValueError(label)

def pin(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def exact_types(a,b):
    need(type(a) is type(b),'JSON exact type mismatch')
    if type(b) is dict:
        need(set(a)==set(b),'JSON exact keys')
        for k in b:exact_types(a[k],b[k])
    elif type(b) is list:
        need(len(a)==len(b),'JSON exact list length')
        for x,y in zip(a,b):exact_types(x,y)
    else:need(a==b,'JSON exact value')

def object_pairs(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def load(b):
    return json.loads(b.decode('utf-8'),object_pairs_hook=object_pairs,parse_constant=lambda x:need(False,'nonfinite JSON value'))

def ordinary_path(path,kind):
    need('..' not in path.parts,'parent traversal in supplied path')
    path=path.absolute()
    for p in [*reversed(path.parents),path]:
        s=p.lstat()
        if p==path:
            need((stat.S_ISDIR if kind=='dir' else stat.S_ISREG)(s.st_mode),'ordinary '+kind+' required')
            if kind=='file':need(s.st_nlink==1,'single-link file required')
        else:need(stat.S_ISDIR(s.st_mode),'ordinary ancestor directory required')
    return path

def read(path):
    ordinary_path(path,'file')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'changed input type')
        with os.fdopen(fd,'rb',closefd=False) as f:return f.read()
    finally:os.close(fd)

def safe(name):
    return type(name) is str and re.fullmatch(r'[A-Za-z0-9_./-]+',name) is not None and not name.startswith('/') and all(p not in ('','.','..') for p in name.split('/'))

def inventory(root):
    ordinary_path(root,'dir');files={};dirs={''}
    for parent,ds,fs in os.walk(root,followlinks=False):
        parent=Path(parent)
        for name in ds:
            p=parent/name;ordinary_path(p,'dir');dirs.add(p.relative_to(root).as_posix())
        for name in fs:
            p=parent/name;files[p.relative_to(root).as_posix()]=read(p)
    return files,dirs

def authenticate(root,anchor):
    files,dirs=inventory(root)
    need(files.get('bootstrap.py')==anchor,'delivered bootstrap differs from fixed external copy')
    raw=files.get('DELIVERY_MANIFEST.json');need(raw is not None,'missing delivery manifest')
    need(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA256,'fixed delivery manifest pin')
    m=load(raw);need(type(m) is dict and set(m)=={'schema','problem_id','files'},'manifest exact keys')
    need(m['schema']=='hopf-tree-authored-delivery-v1' and type(m['problem_id']) is int and m['problem_id']==30004409,'manifest identity')
    need(type(m['files']) is list and len(m['files'])>0,'manifest list required')
    expected={'bootstrap.py','DELIVERY_MANIFEST.json'};expected_dirs={''}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256','git_blob'},'manifest entry schema')
        n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate manifest path');expected.add(n)
        need(type(e['bytes']) is int and e['bytes']>=0,'manifest byte count type')
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,'manifest sha256 type')
        need(type(e['git_blob']) is str and re.fullmatch('[0-9a-f]{40}',e['git_blob']) is not None,'manifest git blob type')
        need(n in files and pin(files[n])=={k:e[k] for k in ('bytes','sha256','git_blob')},'manifest file pin: '+n)
        expected_dirs.update(str(p) for p in PurePosixPath(n).parents if str(p)!='.')
    need(set(files)==expected and dirs==expected_dirs,'exact file and directory inventory')
    need(pin(files['verify_publication.py'])==VERIFIER_PIN,'independent verifier pin')
    return files,dirs

def readonly(root,files,dirs):
    need(os.getuid()==os.geteuid()==1000,'UID and EUID 1000 required')
    denied_dirs=denied_files=0
    for d in [root/n for n in sorted(dirs)]:
        need(not os.access(d,os.W_OK),'directory writable')
        probe=d/('.write_probe_'+str(os.getpid()))
        try:fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except PermissionError:denied_dirs+=1
        else:
            os.close(fd);probe.unlink();raise ValueError('directory create unexpectedly permitted')
    for p in [root/n for n in sorted(files)]:
        need(not os.access(p,os.W_OK),'file writable')
        try:fd=os.open(p,os.O_WRONLY|os.O_NOFOLLOW)
        except PermissionError:denied_files+=1
        else:os.close(fd);raise ValueError('file write-open unexpectedly permitted')
    return {'directory_create_denials':denied_dirs,'existing_file_write_open_denials':denied_files}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);a=parser.parse_args()
    root=ordinary_path(a.root,'dir');external=ordinary_path(Path(__file__),'file')
    need(root not in external.parents and external!=root,'bootstrap must run from outside delivery')
    anchor=read(external);files,dirs=authenticate(root,anchor);ro=readonly(root,files,dirs)
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    command=[sys.executable,'-I','-S','-B',*flags,str(root/'verify_publication.py'),str(root)]
    run=subprocess.run(command,capture_output=True,timeout=120,cwd=root)
    need(run.returncode==0 and run.stderr==b'','authenticated replay failed: '+run.stderr.decode('utf-8','replace'))
    result=load(run.stdout);need(result['status']=='PASS_PRIOR_KNOWN_LITERAL_NEGATIVE','replay disposition')
    need(authenticate(root,anchor)==(files,dirs),'tested inputs changed')
    # Full nested stdout/stderr bytes, without truncation or summary substitution.
    return {'schema':'hopf-tree-authored-bootstrap-v1','status':'PASS_COMPLETE_DELIVERY','uid':os.geteuid(),'optimization':sys.flags.optimize,'delivery_manifest_sha256':MANIFEST_SHA256,'delivered_files':len(files),'delivered_directories':len(dirs),'readonly':ro,'unchanged_before_after':True,'replay':{'exit_code':run.returncode,'stdout':{'type':'inline_utf8','bytes':len(run.stdout),'sha256':hashlib.sha256(run.stdout).hexdigest(),'text':run.stdout.decode('utf-8')},'stderr':{'type':'inline_utf8','bytes':len(run.stderr),'sha256':hashlib.sha256(run.stderr).hexdigest(),'text':run.stderr.decode('utf-8')}}}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+('errno='+str(e.errno) if isinstance(e,OSError) else str(e)),file=sys.stderr);sys.exit(1)
