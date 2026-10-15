#!/usr/bin/env python3
"""Portable read-only replay of the independent second-audit controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def need(condition,message):
    if not condition:
        raise ValueError(message)

def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}

def run(packet):
    here=Path(__file__).resolve().parent
    outputs=[];accepted=[]
    modes=[('normal',[],{}),('O',['-O'],{}),('OO',['-OO'],{}),('env_2',[],{'PYTHONOPTIMIZE':'2'})]
    with tempfile.TemporaryDirectory(prefix='independent_braid_second_') as tmp:
        tmp=Path(tmp); audit=tmp/'audit'; audit.mkdir()
        author=tmp/'author'; shutil.copytree(packet,author)
        for name in ['independent_check.py','recovery_controls.py','INDEPENDENT_RESULTS.json']:
            shutil.copy2(here/name,audit/name)
        for root in (audit,author):
            for p in root.rglob('*'):
                p.chmod(0o555 if p.is_dir() else 0o444)
            root.chmod(0o555)
        before=hashes(tmp)
        try:
            for label,flags,extra in modes:
                env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.update(extra);env['PYTHONDONTWRITEBYTECODE']='1'
                result=subprocess.run([sys.executable,'-B',*flags,str(audit/'recovery_controls.py'),'--author-packet',str(author)],cwd=tmp,env=env,capture_output=True,text=True,timeout=180)
                need(result.returncode==0 and result.stderr=='',label+' failed: '+result.stderr)
                need(json.loads(result.stdout)['status']=='PASS_SECOND_AUDIT_RECOVERY_CONTROLS','missing valid status')
                outputs.append(result.stdout);accepted.append(label)
            after=hashes(tmp)
            need(before==after,'read-only replay changed files')
        finally:
            for root in (audit,author):
                root.chmod(0o755)
                for p in root.rglob('*'):
                    if p.is_dir():p.chmod(0o755)
    need(len(set(outputs))==1,'optimization-dependent independent result')
    need(outputs[0].encode()==(here/'RECOVERY_CONTROLS.json').read_bytes(),'saved independent controls differ')
    return {'status':'PASS_SECOND_AUDIT_PORTABLE_REPLAY','valid_modes':accepted,'read_only_permission_relocation':True,'different_working_directory':True,'all_relocated_bytes_unchanged':True,'outputs_identical':True,'output_sha256':hashlib.sha256(outputs[0].encode()).hexdigest(),'sympy_required':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--author-packet',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.author_packet.resolve()),sort_keys=True,indent=2))
