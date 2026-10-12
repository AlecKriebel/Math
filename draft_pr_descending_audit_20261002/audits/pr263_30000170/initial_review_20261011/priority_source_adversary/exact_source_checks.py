"""Exact algebra for the source comparison; no provider or shared-tree writes.

Run with Python 3. Writes only this folder's EXACT_SOURCE_CHECKS.json.
These controls verify the displayed repairs/identities, not literature absence.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json


def add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, Q(0)) + v
    return {k: v for k, v in c.items() if v}


def scale(a, s):
    return {k: s*v for k, v in a.items() if s*v}


def mul(a, b):
    c = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x+y for x, y in zip(ka, kb))
            c[k] = c.get(k, Q(0)) + va*vb
    return {k: v for k, v in c.items() if v}


# Variables x,v,u. Bottema/Kirillov quartic boundary numerator.
x, v, u, one = ({(1,0,0):Q(1)}, {(0,1,0):Q(1)},
                 {(0,0,1):Q(1)}, {(0,0,0):Q(1)})
a1, a3, a2 = add(x,v), add(x,scale(v,-1)), add(u,scale(one,2))
lhs = add(mul(mul(a1,a2),a3), scale(add(mul(a1,a1),mul(a3,a3)),-1))
rhs = add(mul(u,mul(x,x)), scale(mul(add(u,scale(one,4)),mul(v,v)),-1))
assert lhs == rhs

# Cross finite gradient and the repaired support bound.
assert Q(5)**2-Q(4)**2 == Q(3)**2
g = (Q(5,3),Q(-4,3))
assert g[0]-Q(1,2) == Q(7,6) > Q(1)
assert g[0] > Q(1)
# For c>0 and 0<c<=1/rho, support/c >= 7/6 > h(c,0)/c=1.
# The parameter minimum is c^2/2+2*(x1-c/2)^2.
for c in [Q(1),Q(1,7),Q(5,13)]:
    targets = [(c/2,c/2),(c/2,-c/2)]
    assert len(set(targets)) == 2
    for p, q in targets:
        assert (c-p)**2+q**2 == c**2/2
        assert -p**2+q**2 == 0  # Both characteristic polynomials are z^2.
    for p in [Q(-3,7),Q(0),Q(7,12)]:
        assert (c-p)**2+p**2 == c**2/2+2*(p-c/2)**2

# Candidate support sign uses 2*sqrt(2)>5/2; squaring is valid for positives.
assert Q(2)**2*Q(2) > Q(5,2)**2

payload = {
    "schema": "pr263-priority-source-exact-checks-v1",
    "all_assertions_pass": True,
    "cross_5_38": {
        "correct_h_c_0": "c for c>0",
        "gradient_at_5_over_k_4_over_k": ["5/3","-4/3"],
        "support_over_c_lower_bound_rho_positive": "7/6 > 1",
        "conclusion_survives_printed_typo": True,
        "nearest_parameter_pair": ["(c/2,c/2)","(c/2,-c/2)"],
        "squared_distance": "c^2/2",
        "both_characteristic_polynomials": "z^2",
        "global_minimization_identity": "(c-x1)^2+x1^2=c^2/2+2*(x1-c/2)^2"
    },
    "classical_quartic_identity": "a1*a2*a3-a1^2-a3^2=u*x^2-(u+4)*v^2, a1=x+v,a3=x-v,a2=u+2",
    "complex_quadratic_chart": {"U":"Re(b)+Im(a)^2/4","V":"Im(b)-Re(a)*Im(a)/2","stable_solid":"x>=0,U>=0,V^2<=x^2*U"},
    "literature_absence_certified": False,
    "finite_function_prox_regular_lemma_assumed": False,
}
here = Path(__file__).resolve().parent
payload["check_script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(here/"EXACT_SOURCE_CHECKS.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps({"all_assertions_pass":True,"output":"EXACT_SOURCE_CHECKS.json"}))
