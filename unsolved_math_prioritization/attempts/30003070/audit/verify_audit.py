#!/usr/bin/env python3
"""Strict independent audit inventory, exact mathematical replay, optional full replay."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def require(ok,message):
    if not ok:raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--author-dir',type=Path)
    p.add_argument('--archive',type=Path)
    p.add_argument('--source-dir',type=Path)
    p.add_argument('--negative-controls',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent
    m=json.loads((root/'MANIFEST.json').read_text())
    require(set(m)=={'schema_version','problem_id','verdict','files'},'unexpected manifest fields')
    require(m['schema_version']==1 and m['problem_id']=='30003070' and m['verdict']=='PASS','manifest identity')
    names=[]
    for item in m['files']:
        require(set(item)=={'name','bytes','sha256'},'bad inventory entry')
        name=item['name']
        require(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_.-]+',name) and name not in ('.','..','MANIFEST.json'),'unsafe inventory path')
        require(type(item['bytes']) is int and item['bytes']>=0,'invalid byte count')
        require(re.fullmatch(r'[a-f0-9]{64}',item['sha256']) is not None,'invalid digest')
        names.append(name)
    require(len(names)==len(set(names)),'duplicate inventory name')
    require(set(p.name for p in root.iterdir())==set(names)|{'MANIFEST.json'},'inventory mismatch')
    require(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),'nonregular member')
    for item in m['files']:
        b=(root/item['name']).read_bytes()
        require(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],'digest mismatch '+item['name'])
    for path in root.glob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(path.read_text()))),'optimization-sensitive assertion')
    flags=['-B']+(['-OO'] if sys.flags.optimize>1 else ['-O'] if sys.flags.optimize else [])
    def run(script,args,expected):
        done=subprocess.run([sys.executable,*flags,str(root/script),*args],capture_output=True,cwd='/tmp')
        require(done.returncode==0,'replay error: '+done.stderr.decode(errors='replace'))
        require(done.stdout==(root/expected).read_bytes(),'replay differs from frozen expected bytes')
    run('independent_verify.py',[],'independent_math.json')
    supplied=[a.author_dir,a.archive,a.source_dir]
    require(all(supplied) or not any(supplied),'provide all three external paths, or none')
    if all(supplied):
        args=['--author-dir',str(a.author_dir.resolve()),'--archive',str(a.archive.resolve()),'--source-dir',str(a.source_dir.resolve())]
        run('independent_verify.py',args,'independent_results.json')
        if a.negative_controls:run('negative_controls.py',args,'negative_results.json')
    else:require(not a.negative_controls,'negative controls need the three external paths')
    status=json.loads((root/'STATUS.json').read_text())
    require(status['verdict']=='PASS' and status['mathematical_status']=='unsolved' and status['approaches_used']==5,'scope drift')
    for flag in ['full_solution','full_counterexample','full_prior_resolution','novelty_claim','global_current_openness_claim','remote_writes']:
        require(status[flag] is False,'scope overclaim')
    print(json.dumps({'status':'PASS','scope':'audited partials; unsolved 5/5','audit_files':len(names)+1,
                      'independent_math_checks':json.loads((root/'independent_math.json').read_text())['checks'],
                      'optional_author_and_source_replay':bool(all(supplied)),
                      'optional_negative_replay':a.negative_controls},sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
