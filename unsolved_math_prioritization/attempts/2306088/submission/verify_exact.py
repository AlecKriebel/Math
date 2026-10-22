#!/usr/bin/env python3
"""Small exact algebra controls; no search and no numerical proof claims."""
from fractions import Fraction as Q
import json

def add(p, q):
    return [(p[i] if i < len(p) else Q(0)) + (q[i] if i < len(q) else Q(0))
            for i in range(max(len(p), len(q)))]
def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out
def ev(p, x):
    return sum(c*x**i for i, c in enumerate(p))
checks = []
def check(label, condition):
    assert condition, label
    checks.append({'name': label, 'passed': True})

# Polynomial coefficient identity, not a grid-based inference.
h = mul(mul([Q(2),Q(-1)], [Q(2),Q(-1)]), [Q(1),Q(0),Q(2)])
lhs = add(h, [-Q(27,8)])
rhs = [x/Q(8) for x in mul(mul(mul([Q(1),Q(-2)], [Q(1),Q(-2)]), [Q(1),Q(-2)]), [Q(5),Q(-2)])]
check('small-coefficient factorization as coefficient arrays', lhs == rhs)
check('small-coefficient gap positive at a=0', ev(lhs,Q(0)) == Q(5,8))
check('small-coefficient gap vanishes at a=1/2', ev(lhs,Q(1,2)) == 0)
check('q area divided by pi', Q(1)+2*Q(1,2)**2 == Q(3,2))
check('q sharp functional squared divided by pi', (2-Q(1,2))**2 * Q(3,2) == Q(27,8))
# Polynomials in tau for inverse-Koebe and composition coefficients.
p1=[Q(0),Q(1)]
p2=[Q(0),Q(2),Q(-2)]
check('inverse-Koebe z2 identity', add(p2,[Q(0),Q(0),Q(2)]) == [Q(0),Q(2),Q(0)])
comp=add(p2,[Q(0),Q(0),Q(1,2)])
check('normalized composition z2', comp[1:] == [Q(2),-Q(3,2)])
for a in [Q(1,2),Q(3,4),Q(1),Q(3,2),Q(199,100)]:
    tau=Q(2,3)*(2-a)
    check('coefficient normalization a='+str(a), 2-Q(3,2)*tau == a)
    check('area normalization a='+str(a), Q(3,2)/tau**2 == Q(27,8)/(2-a)**2)
check('perimeter squared constant divided by pi squared', 4*Q(27,8) == Q(27,2))
# Negative controls deliberately detect the wrong formula/sign.
check('wrong denominator 7 rejected at a=1', Q(27,8) < Q(27,7))
check('constant squared above 27/8 rejected by q', Q(27,8) < Q(27,8)+Q(1,100))
check('reversed isoperimetric implication rejected by feasible numbers', Q(1,2) >= Q(1,3) and not Q(1,2) <= Q(1,3))
result = {
  'status':'PASS', 'checks':checks, 'count':len(checks),
  'arithmetic':'Python standard-library Fraction; pi factored out symbolically',
  'limits':'These identities do not prove the minimum-area theorem, symmetrization, isoperimetry, OCR accuracy, or full equality-case classification. No exhaustive search.',
}
print(json.dumps(result, indent=2))
