#!/usr/bin/env python3
"""Independent exact controls for the frozen AMR-039-0010 partial-results package.

Standard library only. Writes only independent_results.json beside this script.
The accompanying audit gives the analytic arguments; finite checks are not proofs
of infinite-state assertions. The original verifier is called without its writer.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import json
import runpy

EXPECTED = 'b287f898f2dafe79381e57132f8fe6f476c3b0b7d73dc6e9d9852de095dc710b'

# Polynomials in one indeterminate, coefficients in increasing degree order.
def poly(*cs):
    cs = list(map(F, cs)) or [F(0)]
    while len(cs) > 1 and not cs[-1]:
        cs.pop()
    return tuple(cs)

def add(a, b):
    return poly(*( (a[i] if i < len(a) else 0) +
                   (b[i] if i < len(b) else 0)
                   for i in range(max(len(a), len(b))) ))

def scale(a, c):
    return poly(*(x*c for x in a))

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    cs = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            cs[i+j] += x*y
    return poly(*cs)

def total(ps):
    ans = poly(0)
    for p in ps:
        ans = add(ans,p)
    return ans

def check():
    public = Path(__file__).resolve().parent.parent / 'public'
    raw = (public/'FROZEN_MANIFEST.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED
    manifest = json.loads(raw)
    for entry in manifest['files']:
        b = (public/entry['path']).read_bytes()
        assert len(b) == entry['bytes']
        assert hashlib.sha256(b).hexdigest() == entry['sha256']
    assert {p.name for p in public.iterdir()} == {
        e['path'] for e in manifest['files']} | {'FROZEN_MANIFEST.json'}
    original = runpy.run_path(str(public/'verify.py'))['check']()
    assert original == json.loads((public/'verification_results.json').read_text())

    one, k = poly(1), poly(0,1)
    assert sub(one,mul(sub(one,k),sub(one,k))) == poly(0,2,-1)
    a = poly(1,F(-1,2))
    assert sub(one,mul(a,a)) == poly(0,1,F(-1,4))

    # For n>=6 successive terms of exp(2/3) have ratio <=2/21.
    x = F(2,3)
    exp_upper = sum((x**n/factorial(n) for n in range(6)),F(0))
    exp_upper += (x**6/factorial(6))/(1-F(2,21))
    assert exp_upper < 2

    # Two-point quantities are obtained directly, independently of the verifier.
    A, L, eps = F(1,3), F(2,3), F(1,16)
    join = 2*A*L
    assert join == F(4,9)
    cost = L-A*L**2
    transported = cost*eps
    chi2 = sum((z*z/F(1,2) for z in (eps,-eps)),F(0))
    assert cost == F(14,27)
    assert transported == F(7,216)
    assert transported-chi2 == F(29,1728)
    assert eps**2/(4*A) == F(3,1024)

    # Exact polynomial identities for every 0<h<=1, not sampled h values.
    P = [[F(3,4),F(1,4),F(0)],
         [F(1,8),F(3,4),F(1,8)],
         [F(0),F(1,4),F(3,4)]]
    pi = [F(1,4),F(1,2),F(1,4)]
    Ph = [[poly(int(i==j),P[i][j]-int(i==j)) for j in range(3)]
          for i in range(3)]
    assert all(total(row)==one for row in Ph)
    assert [total(scale(Ph[i][j],pi[i]) for i in range(3))
            for j in range(3)] == [poly(p) for p in pi]
    assert all(scale(Ph[i][j],pi[i])==scale(Ph[j][i],pi[j])
               for i in range(3) for j in range(3))
    def variance(row):
        mean = total(scale(row[i],i) for i in range(3))
        second = total(scale(row[i],i*i) for i in range(3))
        return sub(second,mul(mean,mean))
    v = [variance(row) for row in Ph]
    assert v == [poly(0,F(1,4),F(-1,16)),poly(0,F(1,4)),
                 poly(0,F(1,4),F(-1,16))]
    expected_cum = {(0,1):[poly(1,F(-3,8)),poly(0,F(1,8))],
                    (1,2):[poly(0,F(1,8)),poly(1,F(-3,8))],
                    (0,2):[poly(1,F(-1,4)),poly(1,F(-1,4))]}
    for (i,j), expected in expected_cum.items():
        diffs = [sub(total(Ph[i][:r]),total(Ph[j][:r])) for r in (1,2)]
        assert diffs == expected
        # All listed linear polynomials are >=0 on [0,1].
        assert all(p[0]>=0 and sum(p)>=0 for p in diffs)
        assert scale(total(diffs),F(1,j-i)) == poly(1,F(-1,4))
    kh = poly(0,F(1,4))
    v_over_k = [scale(poly(*p[1:]),4) for p in v]
    assert sub(v_over_k[1],v_over_k[0]) == kh
    assert sub(v_over_k[1],v_over_k[2]) == kh
    pi_v = total(scale(p,w) for p,w in zip(v,pi))
    assert pi_v == mul(kh,poly(1,F(-1,8)))
    denom = mul(kh,poly(1,F(-1,16)))
    assert mul(pi_v,poly(1,F(-1,16))) == mul(denom,poly(1,F(-1,8)))

    # Recheck the freeze after executing all controls.
    assert hashlib.sha256((public/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()==EXPECTED
    for entry in manifest['files']:
        assert hashlib.sha256((public/entry['path']).read_bytes()).hexdigest()==entry['sha256']
    return {
      'problem_id':'4000010',
      'candidate_manifest_sha256':digest,
      'frozen_files_match':True,
      'frozen_public_tree_unchanged':True,
      'original_results_exactly_reproduced_without_writer':True,
      'independent_exact_controls':{
        'geometric_denominators_symbolic':True,
        'exp_two_thirds_rational_upper_bound':str(exp_upper),
        'exp_two_thirds_upper_bound_less_than_two':True,
        'two_point_cost':str(cost),
        'two_point_transport':str(transported),
        'two_point_entropy_chi_squared_upper_bound':str(chi2),
        'two_point_gap_lower_bound':str(transported-chi2),
        'lazification_all_h_polynomial_identities':True,
        'lazification_domain':'0 < h <= 1',
        'lazification_W1_sign_conditions':'Exact affine endpoint checks on [0,1]',
        'lazification_curvature':'h/4',
        'lazification_A':'(1-h/8)/(1-h/16)',
        'lazification_C':'h/4',
        'lazification_L':'1/3'},
      'analytic_checks_in_report':[
        'Entropy orientation and finite-first-moment implication',
        'Stationary limits and Fatou extension',
        'Finite Laplace window and nonlinear iteration',
        'Jensen direction and small-mass obstruction',
        'Exact entropy-defect conjugacy',
        'Product-coupling defect and mean-jump radius bound',
        'Polynomial and Poisson tail obstructions'],
      'limitation':'Analytic and source-scope conclusions are justified in AUDIT.md; finite tests are not universal proofs.',
      'overall_passed':True}

if __name__ == '__main__':
    result = check()
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
