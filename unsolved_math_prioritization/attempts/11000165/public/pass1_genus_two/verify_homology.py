#!/usr/bin/env python3
"""Standard-library exact genus-two replay; universal polynomial and 121 integer checks."""
import json
import runpy
from pathlib import Path
HERE=Path(__file__).resolve().parent
ns=runpy.run_path(str(HERE.parent/'pass1_exact_validation/verify_exact_formulas.py'))
ns['genus_two_checks']()
def need(ok):
    if not ok: raise RuntimeError('Exact genus-two check failed')
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def U(r,s,t):return [[1,0,r,s],[0,1,s,t],[0,0,1,0],[0,0,0,1]]
for p in range(-5,6):
    for q in range(-5,6):
        e0,e1,e2=p*q-p*p,p*q-q*q,-p*q
        need(mm(U(p*p,p*q,q*q),U(e0+e2,e2,e1+e2))==U(0,0,0))
        need((p*q-p*p,p*q-q*q,-p*q)==((-p)*(-q)-(-p)**2,(-p)*(-q)-(-q)**2,-(-p)*(-q)))
result={'symbolic_rank_one_correction':'PASS','integral_basis_determinant':-1,'integer_samples_checked':121,'homology_identity_samples':'PASS','orientation_independence_samples':'PASS','topological_proof':'See GENUS_TWO_GENERATORS.md; not a computational claim'}
HERE.joinpath('ALGEBRA_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
