#!/usr/bin/env python3
"""Externally anchor the complete delivery and the REQUIRED actual repository QUEUE.
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

MANIFEST_SHA256 = '3d1271b79f8542a4259e6a04ba4b1a612dc2362322a6376abcd58151430e36ba'
VERIFIER_PIN = {'bytes': 11063, 'sha256': 'bad609cd584d7cfafb562f815536574538576d7f06b2c62fbb008eb9692f072f', 'git_blob': 'd72fb769bf4991b2d02b0f928a81e16268afca79'}
QUEUE_BEFORE = {'bytes': 397331, 'git_blob': '6f68342c8f57a413ba2535d8b20fb49915d5898c', 'sha256': '25fdcea7fdcb23109e4b46ba2b560dcff02c18aeed35899c4d89375e3de6cdfe'}
QUEUE_AFTER = {'bytes': 397786, 'git_blob': '89db795fac69bc39e92568609e9d23414062640c', 'sha256': 'f82735eaa207d37bebd31bbe011b4e34caa506f669e266a0352cbfd2033db4cd'}

def need(ok, label):
    if not ok: raise ValueError(label)

def pin(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

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
    need(m['schema']=='duflo-socle-delivery-v1' and type(m['problem_id']) is int and m['problem_id']==30004018,'manifest identity')
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

def queue_check(queue,files):
    need(queue.parts[-2:]==('unsolved_math_prioritization','QUEUE.md'),'actual repository QUEUE path required')
    b=read(queue);need(pin(b)==QUEUE_AFTER,'actual QUEUE after pin')
    proof=load(files['QUEUE_PROOF.json'])
    need(type(proof) is dict and set(proof)=={'schema','repository_path','base_commit','before','after','before_row_utf8','after_row_utf8','changed_raw_split_cells','preserved_raw_split_cells','all_other_bytes_preserved','leading_literal_sha_preserved'},'queue proof exact schema')
    for key,expected in [('before',QUEUE_BEFORE),('after',QUEUE_AFTER)]:
        value=proof[key];need(type(value) is dict and set(value)==set(expected),'queue pin schema')
        need(all(type(value[k]) is type(expected[k]) and value[k]==expected[k] for k in expected),'queue pin exact type/value')
    need(type(proof['changed_raw_split_cells']) is list and all(type(x) is int for x in proof['changed_raw_split_cells']) and proof['changed_raw_split_cells']==[8,9,11],'queue changed cells')
    need(type(proof['preserved_raw_split_cells']) is list and all(type(x) is int for x in proof['preserved_raw_split_cells']) and proof['preserved_raw_split_cells']==[10,12],'queue preserved cells')
    need(proof['all_other_bytes_preserved'] is True and proof['leading_literal_sha_preserved'] is True,'queue preservation declarations')
    need(proof['schema']=='duflo-socle-queue-proof-v1' and proof['repository_path']=='unsolved_math_prioritization/QUEUE.md','queue proof identity')
    need(proof['before']==QUEUE_BEFORE and proof['after']==QUEUE_AFTER,'fixed queue before and after pins')
    before=proof['before_row_utf8'].encode();after=proof['after_row_utf8'].encode()
    lines=b.splitlines(keepends=True);hits=[i for i,line in enumerate(lines) if b'| 30004018 / OWR-16635-003 |' in line]
    need(len(hits)==1 and lines[hits[0]]==after,'unique exact queue target row')
    a=before.split(b'|');z=after.split(b'|')
    need(len(a)==len(z)==14,'queue raw split width')
    need([i for i,(x,y) in enumerate(zip(a,z)) if x!=y]==[8,9,11],'only Status Turns Findings changed')
    need(z[8]==b' exhausted ' and z[9]==b' 5/5 ','queue disposition')
    lines[hits[0]]=before;reconstructed=b''.join(lines)
    need(pin(reconstructed)==QUEUE_BEFORE,'exact before reconstruction; unrelated bytes preserved')
    need(b.splitlines(keepends=True)[0]==reconstructed.splitlines(keepends=True)[0],'leading literal content preserved')
    return b

def readonly(root,queue,files,dirs):
    need(os.getuid()==os.geteuid()==1000,'UID and EUID 1000 required')
    denied_dirs=denied_files=0
    for n in sorted(dirs):
        d=root/n;need(not os.access(d,os.W_OK),'directory writable')
        probe=d/('.write_probe_'+str(os.getpid()))
        try:fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        except PermissionError:denied_dirs+=1
        else:
            os.close(fd);probe.unlink();raise ValueError('directory create unexpectedly permitted')
    for p in [*(root/n for n in sorted(files)),queue]:
        need(not os.access(p,os.W_OK),'file writable')
        try:fd=os.open(p,os.O_WRONLY|os.O_NOFOLLOW)
        except PermissionError:denied_files+=1
        else:os.close(fd);raise ValueError('file write-open unexpectedly permitted')
    return {'directory_create_denials':denied_dirs,'existing_file_write_open_denials':denied_files,'includes_actual_queue':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--queue',type=Path,required=True);a=parser.parse_args()
    root=ordinary_path(a.root,'dir');queue=ordinary_path(a.queue,'file');external=ordinary_path(Path(__file__),'file')
    need(root not in external.parents and external!=root,'bootstrap must run from outside delivery')
    anchor=read(external);files,dirs=authenticate(root,anchor);qb=queue_check(queue,files);ro=readonly(root,queue,files,dirs)
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    command=[sys.executable,'-I','-S','-B',*flags,str(root/'verify_publication.py'),str(root),'--queue',str(queue)]
    run=subprocess.run(command,capture_output=True,timeout=120,cwd=root)
    need(run.returncode==0 and run.stderr==b'','authenticated replay failed: '+run.stderr.decode('utf-8','replace'))
    result=load(run.stdout);need(result['status']=='PASS_SCOPED_PARTIAL_RESULTS','replay disposition')
    need(authenticate(root,anchor)==(files,dirs) and read(queue)==qb,'tested inputs changed')
    # Full nested stdout/stderr bytes, without truncation or summary substitution.
    return {'schema':'duflo-socle-bootstrap-v1','status':'PASS_COMPLETE_DELIVERY','uid':os.geteuid(),'optimization':sys.flags.optimize,'delivery_manifest_sha256':MANIFEST_SHA256,'delivered_files':len(files),'delivered_directories':len(dirs),'queue':pin(qb),'readonly':ro,'unchanged_before_after':True,'replay':{'exit_code':run.returncode,'stdout':{'type':'inline_utf8','bytes':len(run.stdout),'sha256':hashlib.sha256(run.stdout).hexdigest(),'text':run.stdout.decode('utf-8')},'stderr':{'type':'inline_utf8','bytes':len(run.stderr),'sha256':hashlib.sha256(run.stderr).hexdigest(),'text':run.stderr.decode('utf-8')}}}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+(os.strerror(e.errno) if isinstance(e,OSError) and e.errno else str(e)),file=sys.stderr);sys.exit(1)
