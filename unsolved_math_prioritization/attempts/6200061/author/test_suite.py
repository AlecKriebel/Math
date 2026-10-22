#!/usr/bin/env python3
"""Relocation and negative controls; all outputs are outside the frozen package."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(value,message):
    if not value:
        raise RuntimeError(message)

def refresh(root,name):
    path=root/'MANIFEST.json';m=json.loads(path.read_text());b=(root/name).read_bytes()
    m['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    path.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')

def edit_json(root,name,fn,rehash=True):
    p=root/name;v=json.loads(p.read_text());fn(v);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
    if rehash:refresh(root,name)

def run(root,optimized):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'verify.py')]
    return subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=30)

def main():
    require(len(sys.argv)==1,'unexpected arguments')
    original=Path(__file__).resolve().parent
    passed=[]
    with tempfile.TemporaryDirectory(prefix='problem61_relocation_') as tmp:
        tmp=Path(tmp)
        baseline=tmp/'relocated_author';shutil.copytree(original,baseline)
        for optimized in (False,True):
            p=run(baseline,optimized);require(p.returncode==0,p.stderr)
            require(json.loads(p.stdout)['verification']=='PASS','invalid success output')
            passed.append('relocated_optimized' if optimized else 'relocated_normal')
        cases=[
          ('raw_proof_corruption',lambda r:(r/'PROOF.md').write_text((r/'PROOF.md').read_text()+'\ncorruption\n')),
          ('missing_results',lambda r:(r/'RESULTS.json').unlink()),
          ('copied_pdf_extra',lambda r:(r/'source.pdf').write_bytes(b'%PDF-forbidden')),
          ('claim_inflation_rehashed',lambda r:edit_json(r,'IDENTITY.json',lambda v:v.update(general_conjecture_solved=True))),
          ('wrong_problem_rehashed',lambda r:edit_json(r,'IDENTITY.json',lambda v:v.update(problem_id=6200014))),
          ('wrong_review_hash_rehashed',lambda r:edit_json(r,'IDENTITY.json',lambda v:v.update(full_review_sha256='0'*64))),
          ('bernstein_mutation_rehashed',lambda r:edit_json(r,'RESULTS.json',lambda v:v['certificate']['polynomial_bernstein_coefficients'].__setitem__(0,[-1,1]))),
          ('bound_mutation_rehashed',lambda r:edit_json(r,'RESULTS.json',lambda v:v['certificate'].update(squared_growth_lower_bound=[100,1]))),
          ('sample_mutation_rehashed',lambda r:edit_json(r,'RESULTS.json',lambda v:v['dyadic_samples'][0].update(ratio_squared=[1,1]))),
          ('unmarked_claim_rehashed',lambda r:edit_json(r,'IDENTITY.json',lambda v:v['scope_flags'].update(existential_attainment_disproved=True))),
          ('source_inclusion_rehashed',lambda r:edit_json(r,'SOURCES.json',lambda v:v['sources'][0].update(included_in_package=True))),
          ('manifest_status_mutation',lambda r:edit_json(r,'MANIFEST.json',lambda v:v.update(status='SOLVED'),False)),
        ]
        for name,mutate in cases:
            root=tmp/name;shutil.copytree(original,root);mutate(root)
            for optimized in (False,True):
                p=run(root,optimized)
                require(p.returncode!=0 and 'VERIFICATION FAILED:' in p.stderr,'accepted mutation '+name)
            passed.append(name)
    print(json.dumps({'test_suite':'PASS','relocation_modes':2,'negative_controls':12,
                      'negative_control_runs':24,'checks':passed},sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('TEST SUITE FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
