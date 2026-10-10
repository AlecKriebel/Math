#!/usr/bin/env python3
"""Run the two independent audit programs and original frozen checker read-only.
Usage: python -B rerun_audit.py SUBJECT_DIRECTORY EXTERNAL_OUTPUT_DIRECTORY
Requires real/effective UID 1000 and mode-protected subject and audit-code directories.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
sys.dont_write_bytecode=True


def require(ok,msg):
    if not ok:raise RuntimeError(msg)


def digest(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def snapshot(path):
    return {p.name:digest(p) for p in sorted(path.iterdir()) if p.is_file()}


def probes(base):
    require(stat.S_IMODE(base.stat().st_mode)==0o555,'directory mode must be 0555')
    require(not os.access(base,os.W_OK),'directory writable')
    trial=base/('.audit_write_probe_'+str(os.getpid()))
    require(not trial.exists(),'probe collision')
    try:
        fd=os.open(trial,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError as e:
        create_errno=e.errno
    else:
        os.close(fd)
        raise RuntimeError('creation unexpectedly succeeded')
    denied=[]
    for p in sorted(base.iterdir()):
        require(p.is_file() and not p.is_symlink(),'unexpected entry')
        require(stat.S_IMODE(p.stat().st_mode)==0o444,'file mode must be 0444')
        try:
            fd=os.open(p,os.O_WRONLY)
        except PermissionError as e:
            denied.append({'file':p.name,'errno':e.errno})
        else:
            os.close(fd)
            raise RuntimeError('write-open unexpectedly succeeded')
    return {'directory_create_errno':create_errno,'file_write_open_denials':denied}


def main():
    require(len(sys.argv)==3,'subject and output required')
    require(os.getuid()==os.geteuid()==1000,'real/effective UID 1000 required')
    subject=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();code=Path(__file__).resolve().parent
    require(out!=subject and subject not in out.parents and out!=code and code not in out.parents,'external output required')
    out.mkdir(parents=True,exist_ok=True)
    before={'subject':snapshot(subject),'audit_code':snapshot(code)}
    receipt={'schema':1,'uid':os.getuid(),'euid':os.geteuid(),'python':sys.version,
             'platform':platform.system()+' '+platform.release(),
             'probes':{'subject':probes(subject),'audit_code':probes(code)},'runs':[]}
    for name in ('check_claims.py',):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((subject/name).read_text()))),'native assert')
    for name in ('independent_check.py','semantic_controls.py','rerun_audit.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((code/name).read_text()))),'audit assert')
    require(len(before['subject'])==8,'eight author subject files expected')
    for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        tasks=[('native',subject/'check_claims.py',['--require-readonly']),
               ('independent',code/'independent_check.py',[]),
               ('semantic',code/'semantic_controls.py',[str(subject/'check_claims.py')])]
        for kind,script,args in tasks:
            cmd=[sys.executable,'-B']+flags+[str(script)]+args
            result=subprocess.run(cmd,cwd=subject,capture_output=True,check=False,timeout=60)
            prefix=kind+'_'+mode
            stdout=out/(prefix+'.stdout.json');stderr=out/(prefix+'.stderr.txt')
            stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
            row={'kind':kind,'mode':mode,'exit_code':result.returncode,
                 'stdout':{'path':stdout.name,**digest(stdout)},'stderr':{'path':stderr.name,**digest(stderr)}}
            receipt['runs'].append(row)
            require(result.returncode==0,prefix+' failed: '+result.stderr.decode())
            data=json.loads(result.stdout)
            require(data['status'] in ('PASS','passed'),'run did not pass')
            require(data['uid']==1000,'run did not report uid 1000')
            if kind=='native':
                require(data['readonly']['directory_create_denied'] and data['readonly']['existing_file_write_open_denials']==8,'native denied writes')
            else:require(data['euid']==1000,'audit euid')
    after={'subject':snapshot(subject),'audit_code':snapshot(code)}
    require(before==after,'subject or audit code changed')
    receipt['files_unchanged']=True;receipt['status']='PASS'
    receipt['subject_files']=before['subject'];receipt['audit_code_files']=before['audit_code']
    (out/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    (out/'SUBJECT_MANIFEST.json').write_text(json.dumps({'schema':1,'files':before['subject']},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','runs':len(receipt['runs']),'uid':os.getuid(),'euid':os.geteuid(),'unchanged':True},sort_keys=True))


if __name__=='__main__':main()
