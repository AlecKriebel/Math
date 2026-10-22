#!/usr/bin/env python3
"""Portable subprocess and corruption controls; safe to run from any directory."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
EXPECTED_AUTHOR_OUTPUT='40f8e13e7b45317c3125632059c8a9ee98d7b2ac870decc9fc1f40fc5e9b3e3e'
EXPECTED_AUTHOR_SCRIPT='f6f36748d0eebca2605703dc509527efddb159e5cb4f73b689ee47fa03754db0'
rows=[]
def demand(value,label):
    if not value:raise RuntimeError('CONTROL FAILURE: '+label)
def execute(path,optimized,args=()):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    return subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(path),*args],cwd=path.parent,env=env,capture_output=True)
def h(data):return hashlib.sha256(data).hexdigest()
expected=(BASE/'independent_results.json').read_bytes()
with tempfile.TemporaryDirectory(prefix='braid-independent-relocation-') as td:
    temporary=Path(td)
    copy=temporary/'independent_verify.py';shutil.copyfile(BASE/'independent_verify.py',copy)
    for location,path in [('packet',BASE/'independent_verify.py'),('relocated',copy)]:
        for optimized in [False,True]:
            p=execute(path,optimized)
            demand(p.returncode==0 and p.stdout==expected,location+' replay')
            rows.append({'test':location+'_independent_replay','optimized':optimized,'exit_code':p.returncode,'stdout_sha256':h(p.stdout),'byte_identical':True})
    for tamper in ['polynomial','word','edge','metabolizer','movie']:
        for optimized in [False,True]:
            p=execute(copy,optimized,['--tamper',tamper])
            demand(p.returncode!=0 and b'AUDIT FAILURE' in p.stderr,'reject '+tamper)
            rows.append({'test':'reject_'+tamper,'optimized':optimized,'exit_code':p.returncode,'rejected':True})
    corrected=(BASE/'corrections'/'verify.py').read_text()
    fixed=temporary/'fixed.py';fixed.write_text(corrected)
    replacement='    if not b:\n        raise AssertionError("verification check failed")'
    original=corrected.replace(replacement,'    assert b')
    demand(h(original.encode())==EXPECTED_AUTHOR_SCRIPT,'exact author reconstruction')
    for optimized in [False,True]:
        p=execute(fixed,optimized)
        demand(p.returncode==0 and h(p.stdout)==EXPECTED_AUTHOR_OUTPUT,'corrected author replay')
        rows.append({'test':'hardened_author_replay','optimized':optimized,'exit_code':p.returncode,'stdout_sha256':h(p.stdout),'byte_identical_to_author_results':True})
    for name,code in [('original',original),('hardened',corrected)]:
        changed=code.replace('check(determinant(S)==-243)','check(determinant(S)==-242)')
        demand(changed!=code,'effective corruption')
        path=temporary/(name+'_corrupt.py');path.write_text(changed)
        for optimized in [False,True]:
            p=execute(path,optimized)
            expected_rejection=name=='hardened' or not optimized
            demand((p.returncode!=0)==expected_rejection,'documented author corruption behavior')
            if not expected_rejection:demand(h(p.stdout)==EXPECTED_AUTHOR_OUTPUT,'original optimized false positive output')
            rows.append({'test':name+'_false_determinant','optimized':optimized,'exit_code':p.returncode,'rejected':p.returncode!=0,'expected_behavior':True})
print(json.dumps({'status':'pass','control_count':len(rows),'controls':rows},sort_keys=True,indent=2))
