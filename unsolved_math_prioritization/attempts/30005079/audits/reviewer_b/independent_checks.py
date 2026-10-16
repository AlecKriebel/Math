"""Independent checks of the two moment equations, using exact rational arithmetic.
This file does not import or execute the construction author's checking scripts.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import sympy as S

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent.parent / 'authored' / 'PROOF_CANDIDATE_v4.md'
EXPECTED = '657f458cf3eece42eef9c8dfd46a7c20aaaf363e3a6744f396af3c7389fa43a3'
assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest() == EXPECTED

# Coefficients in ascending degree, before multiplication by the moment monomial.
A_PIECES = [(-1, 0, [4, 4, 1]), (0, 2, [4, -4, 1])]
B_PIECES = [(-1, 1, [2, 1])]

def moment(pieces, power):
    ans = F(0)
    for lo, hi, coefficients in pieces:
        for degree, c in enumerate(coefficients):
            n = power + degree + 1
            ans += F(c) * F(hi**n - lo**n, n)
    return ans

assert moment(A_PIECES, 0) == 5
assert moment(B_PIECES, 0) == 4
assert moment(A_PIECES, 1) == F(5, 12)
assert moment(B_PIECES, 1) == F(2, 3)

# Bound exp's Taylor remainder using exp(1)<3. The exact L1 norms of x*rho
# are 9/4 for A and 2 for B; |t*x|<1 holds at all four endpoints.
def exact_enclosure(pieces, t, radius, l1, n=32):
    assert 0 < t*radius < 1
    midpoint = sum(((-t)**k / factorial(k)) * moment(pieces, k+1)
                   for k in range(n+1))
    err = 3 * l1 * (t*radius)**(n+1) / factorial(n+1)
    return midpoint-err, midpoint+err

brackets = {}
for name, pieces, radius, l1, lo, hi in [
    ('a', A_PIECES, 2, F(9,4), F('0.27379184'), F('0.27379185')),
    ('b', B_PIECES, 1, F(2), F('0.52761951'), F('0.52761953')),
]:
    left, right = exact_enclosure(pieces,lo,radius,l1), exact_enclosure(pieces,hi,radius,l1)
    assert left[0] > 0
    assert right[1] < 0
    brackets[name] = {'lo':str(lo),'hi':str(hi),
        'left_moment_bounds':[str(v) for v in left],
        'right_moment_bounds':[str(v) for v in right],
        'left_positive':True,'right_negative':True}

x,t = S.symbols('x t',real=True,positive=True)
IA = S.integrate(x*(2+x)**2*S.exp(-t*x),(x,-1,0)) + S.integrate(x*(2-x)**2*S.exp(-t*x),(x,0,2))
IB = S.integrate(x*(2+x)*S.exp(-t*x),(x,-1,1))
PA = (t**3+t**2-2*t-6)*S.exp(3*t)+16*t*S.exp(2*t)+4*t+6
PB = (t*t-2)*S.exp(2*t)+3*t*t+4*t+2
assert S.simplify(IA + S.exp(-2*t)*PA/t**4) == 0
assert S.simplify(IB + S.exp(-t)*PB/t**3) == 0
assert S.gcd(t*t-2,3*t*t+4*t+2) == 1

normals = [(1,0),(0,1),(-1,1),(0,-1)]
dets = [u[0]*v[1]-u[1]*v[0] for u,v in zip(normals,normals[1:]+normals[:1])]
assert dets == [1,1,1,1]
# Integrating x on [-1,y+1] equals one-half y times the interval length.
y = S.symbols('y')
assert S.simplify(S.integrate(x,(x,-1,y+1))-y*(y+2)/2) == 0

result = {'candidate_sha256':EXPECTED,'exact_integral_identities':True,
          'density_masses':['5','4'],'unweighted_first_moments':['5/12','2/3'],
          'positive_root_brackets':brackets,'toric_consecutive_determinants':dets,
          'toric_barycenter_reduction':True,'B_coefficients_coprime':True,
          'irrationality':'Proved for every rational ratio by the separate valuation-at-infinity argument; not inferred from this computation.'}
(HERE/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact integration, independently bounded roots, fan and barycenter checks; candidate hash unchanged.')
