#!/usr/bin/env python3
"""Replay this audit in a relocated directory, with immutable author hashes."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
AUTHOR=HERE/'author'


def require(ok, message):
    if not ok: raise RuntimeError(message)


def main():
    manifest=json.loads((HERE/'author_external_manifest.json').read_text())
    require(hashlib.sha256((HERE/'author_external_manifest.json').read_bytes()).hexdigest()==
            '0fcc1d4e600a73113c40b708df26f9aa4d754a7d493af61f499a0c09f6e32342', 'author manifest hash')
    require({p.name for p in AUTHOR.iterdir() if p.is_file()}=={f['path'] for f in manifest['files']},'author file allowlist')
    files=[]
    for f in manifest['files']:
        b=(AUTHOR/f['path']).read_bytes()
        require(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'author hash: '+f['path'])
        files.append({'path':'author/'+f['path'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'match':True})
    output={'outcome':'PASS','problem_id':8500009,'author_members':files,'runs':[]}
    with tempfile.TemporaryDirectory(prefix='rational_audit_replay_') as td:
        work=Path(td)
        shutil.copytree(AUTHOR,work/'author')
        shutil.copy2(HERE/'independent_exact.py',work/'independent_exact.py')
        env={'PATH':os.environ.get('PATH',''),'HOME':td,'LANG':'C.UTF-8'}
        controls=[]
        for flags in ([],['-O'],['-I'],['-I','-O']):
            for label,script,args in [('author_tests','author/verify_exact.py',['--test']),('author_certificate','author/verify_exact.py',[]),('independent_exact','independent_exact.py',[])]:
                p=subprocess.run([sys.executable,*flags,str(work/script),*args],cwd=work,env=env,capture_output=True,text=True)
                log=(p.stdout+p.stderr).replace(td,'RELOCATED')
                require(p.returncode==0,label+' failed: '+log)
                if label=='author_certificate':
                    require(p.stdout.encode()==(AUTHOR/'exact_certificate.json').read_bytes(),'certificate parity')
                if label=='independent_exact':controls.append(p.stdout)
                output['runs'].append({'label':label,'flags':flags,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'log':log})
        require(len(set(controls))==1,'independent control parity')
        p=subprocess.run([sys.executable,'-I','-O',str(work/'author/run_mutations.py')],cwd=work,env=env,text=True,capture_output=True)
        require(p.returncode==0,'mutations execution failed')
        mutations=json.loads(p.stdout)
        require(len(mutations['mutations'])==8 and all(x['killed'] for x in mutations['mutations']),'mutation coverage')
        output['author_mutation_replay']=mutations
    return output


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
