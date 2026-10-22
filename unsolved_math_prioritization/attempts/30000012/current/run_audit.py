#!/usr/bin/env python3
"""Run all original CLI modes and independent semantic tests in a read-only packet.
Stdout only. No network or third-party source bytes are required.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from audit_exact import MUTANTS

def require(value,message):
    if not value: raise RuntimeError(message)

def snapshot():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(BASE.iterdir()) if p.is_file()}

def run(flags,file,*args):
    return subprocess.run([sys.executable,'-B',*flags,str(BASE/file),*args],cwd=BASE,capture_output=True,text=True)

require(os.getuid()==1000 and os.geteuid()==1000,'genuine UID/EUID 1000 required')
before=snapshot(); runs=[]; reference=None
for name,flags in (('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])):
    originals=[]
    for mode in ('exact','negative','all'):
        for forced in (False,True):
            extra=['--mode',mode]+(['--inject-failure'] if forced else [])
            p=run(flags,'check_exact.py',*extra)
            data=json.loads(p.stdout)
            expected=1 if forced else 0
            require(p.returncode==expected,name+' original exit mismatch')
            require(data['status']==('FAIL' if forced else 'PASS'),name+' original status mismatch')
            if forced: require(data.get('error')=='Deliberately injected failure',name+' original failure mechanism')
            require(data['checks']=={'exact':600,'negative':12,'all':612}[mode],name+' original check count')
            originals.append({'mode':mode,'injected_failure':forced,'exit_code':p.returncode,'result':data})
    p=run(flags,'audit_exact.py','--require-readonly')
    require(p.returncode==0,name+' independent positive suite: '+p.stderr)
    positive=json.loads(p.stdout)
    if reference is None: reference=positive
    else: require(positive==reference,name+' optimization changed independent results')
    mutants=[]
    for mutation,family in sorted(MUTANTS.items()):
        p=run(flags,'audit_exact.py','--require-readonly','--mutant',mutation)
        marker='CHECK_FAILED['+family+']:'
        require(p.returncode==1 and marker in p.stderr,name+' semantic mutation survived or failed unexpectedly: '+mutation+'\n'+p.stdout+p.stderr)
        mutants.append({'mutation':mutation,'family':family,'exit_code':p.returncode,'reason':p.stderr.strip()})
    invalid=run(flags,'check_exact.py','--mode','not-a-mode')
    require(invalid.returncode==2 and 'invalid choice' in invalid.stderr,name+' invalid CLI mode not rejected')
    runs.append({'python_mode':name,'original_modes':originals,'independent':positive,'semantic_mutations':mutants,'invalid_cli_exit_code':invalid.returncode})
after=snapshot()
require(before==after,'packet content changed during checks')
print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'read_only_existing_file_open_denied':True,'read_only_new_file_create_denied':True,'files_unchanged':True,'runs':runs,'semantic_mutant_count':len(MUTANTS),'semantic_rejections':3*len(MUTANTS),'original_mode_failure_runs':18,'packet_hashes_at_run':before,'scope':'Exact finite identities and documentary contract guards; analytic geometry remains a written proof review.'},indent=2))
