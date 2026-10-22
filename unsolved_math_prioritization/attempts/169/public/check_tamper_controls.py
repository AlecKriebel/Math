#!/usr/bin/env python3
"""Independent negative tests for byte inventory and exact-status enforcement."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[]),('O',['-O']),('OO',['-OO'])]
def require(b,s):
    if not b:raise RuntimeError(s)
def update_pin(work,path):
    data=json.loads((work/'MANIFEST.json').read_text());b=(work/path).read_bytes()
    for row in data['files']:
        if row['path']==path:row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    (work/'MANIFEST.json').write_text(json.dumps(data))
def mutate(work,case):
    path=work/'MANIFEST.json';data=json.loads(path.read_text())
    if case=='changed_proof':
        p=work/'proofs/05_FINAL_COLLECTIVE_CONSTRUCTION.md';p.write_bytes(p.read_bytes()+b'Changed.\n')
    elif case=='missing_file':(work/'fixtures/moment_4.json').unlink()
    elif case=='extra_file':(work/'UNEXPECTED.txt').write_text('unmanifested')
    elif case=='duplicate_path':data['files'].append(data['files'][0]);path.write_text(json.dumps(data))
    elif case=='path_traversal':data['files'][0]['path']='../escape';path.write_text(json.dumps(data))
    elif case=='false_solution_status':data['problem_status']='SOLVED';data['resolution_claimed']=True;path.write_text(json.dumps(data))
    elif case in ('cap_changed_rehashed','constant_changed_rehashed','adaptivity_changed_rehashed'):
        f=work/'FORMULATION.json';obj=json.loads(f.read_text())
        if case=='cap_changed_rehashed':obj['cap']='100*floor(sqrt(p))'
        elif case=='constant_changed_rehashed':obj['final_residual_tail_denominator']='8*k*m^2'
        else:obj['centres']='predetermined before A'
        f.write_text(json.dumps(obj));update_pin(work,'FORMULATION.json')
    elif case in ('law_changed_rehashed','event_changed_rehashed','affirmative_changed_rehashed','negative_changed_rehashed'):
        f=work/'FORMULATION.json';obj=json.loads(f.read_text())
        field=case.removesuffix('_changed_rehashed')
        variants={'law':'independent Bernoulli inclusion with probability 1/sqrt(p)',
                  'event':'there exists T with |T|<=cap and at most one hole',
                  'affirmative':'success probability tends to one along some primes',
                  'negative':'positive failure probability at one fixed prime'}
        obj[field]=variants[field];f.write_text(json.dumps(obj));update_pin(work,'FORMULATION.json')
    elif case=='binding_changed_rehashed':
        f=work/'AUDIT_BINDINGS.json';obj=json.loads(f.read_text());obj['audit_stages'][0]['proof_bindings'][0]['public_sha256']='0'*64;f.write_text(json.dumps(obj));update_pin(work,'AUDIT_BINDINGS.json')
    elif case=='symbolic_link':
        p=work/'fixtures/moment_4.json';p.unlink();p.symlink_to('moment_10.json')
    else:raise RuntimeError('unknown case')
def main():
    cases=['changed_proof','missing_file','extra_file','duplicate_path','path_traversal','false_solution_status','cap_changed_rehashed','constant_changed_rehashed','adaptivity_changed_rehashed','law_changed_rehashed','event_changed_rehashed','affirmative_changed_rehashed','negative_changed_rehashed','binding_changed_rehashed','symbolic_link'];results=[]
    before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
    with tempfile.TemporaryDirectory(prefix='random-cover-tamper-') as tmp:
        for case in cases:
            work=Path(tmp)/case;shutil.copytree(ROOT,work);mutate(work,case)
            for mode,flags in MODES:
                env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
                cp=subprocess.run([sys.executable,'-I','-B',*flags,str(work/'verify_package.py')],cwd=work,env=env,capture_output=True,timeout=60)
                require(cp.returncode!=0 and b'ValueError:' in cp.stderr,'tamper accepted or wrong failure: '+case)
                if case in ('law_changed_rehashed','event_changed_rehashed','affirmative_changed_rehashed','negative_changed_rehashed'):
                    field=case.removesuffix('_changed_rehashed')
                    require(('exact formulation mismatch: '+field).encode() in cp.stderr,'semantic mutation rejected at wrong guard: '+case)
                results.append({'case':case,'mode':mode,'rejected':True})
    after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
    require(before==after,'tamper controls changed original files')
    print(json.dumps({'status':'PASS','cases':len(cases),'rejections':len(results),'source_tree_modified':False,'results':results},sort_keys=True,indent=2))
if __name__=='__main__':main()
