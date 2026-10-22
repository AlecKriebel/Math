#!/usr/bin/env python3
"""Independent exact audit controls; finite diagnostics only, not a proof."""
from fractions import Fraction as R
import json

def multiply(a, b):
    ans = {}
    for j, x in a.items():
        for k, y in b.items():
            ans[j+k] = ans.get(j+k, R(0)) + x*y
    return {j: x for j, x in ans.items() if x}

def length(p):
    return sum((abs(c) for c in p.values()), R(0))

def from_factors(spec, scale=R(1)):
    p, measure = {0: scale}, abs(scale)
    for a, m in spec:
        p = multiply(p, a)
        measure *= m
    return p, measure

linears = [({0:-r, 1:R(1)}, max(R(1),abs(r))) for r in map(R, [-3,-1,0,1,3])]
linears += [({0:-r, 1:R(1)}, max(R(1),abs(r))) for r in [R(-1,3),R(2,3),R(3,2)]]
pairs = [({0:r*r, 1:b, 2:R(1)}, max(R(1),r)**2) for r in [R(1,3),R(1),R(3)] for b in [R(0),r]]
factors = linears + pairs
ps = []
for n in range(32):
    spec = [factors[(n+5*j)%len(factors)] for j in range(n%7)]
    ps.append(from_factors(spec, [R(-5,7),R(2,11),R(4)][n%3]))
qs = []
for n in range(16):
    spec = [factors[(2*n+3*j)%len(factors)] for j in range(n%6)]
    qs.append(from_factors(spec))
ts = [R(-2),R(-19999,10000),R(-7,4),R(-4,3),R(-1),R(-1,11),R(0),R(1,13),R(1),R(4,3),R(7,4),R(19999,10000),R(2)]
checked = 0
for t in ts:
    for p, mp in ps:
        for q, mq in qs:
            assert q[max(q)] == 1
            assert length(multiply(multiply({0:R(1),1:t,2:R(1)},p),q)) >= 2*mp*mq >= 2*mp
            checked += 1
# Exact endpoint approximants. Q_n is monic; L((x-1)^2 Q_n)=2n/(n-1).
endpoint = 0
for n in range(2,65):
    q = {k:R(k+1,n-1) for k in range(n-1)}
    expected = {n:R(1),n-1:R(-n,n-1),0:R(1,n-1)}
    f = multiply({2:R(1),1:R(-2),0:R(1)},q)
    assert f == expected
    assert length(f) == R(2*n,n-1) > 2
    # Transform x -> -x and rescale to keep Q monic.
    qplus = {k:c*(-1)**(k+n-2) for k,c in q.items()}
    assert qplus[max(qplus)] == 1
    assert length(multiply({2:R(1),1:R(2),0:R(1)},qplus)) == R(2*n,n-1)
    endpoint += 2
# Generic complex full-column-rank matrix whose ordinary Gram matrix is singular.
# M = [[1,0],[i,0],[0,1]]; M^T M=diag(0,1), M* M=diag(2,1).
assert 1 + (1j)**2 == 0 and abs(1)**2 + abs(1j)**2 == 2
print(json.dumps({"arithmetic":"exact rational polynomial arithmetic", "P_count":len(ps), "Q_count":len(qs), "parameter_count":len(ts), "product_checks":checked, "endpoint_approximant_checks":endpoint, "endpoint_max_degree":64, "all_checks_passed":True, "scope":"Independent supplementary diagnostics; no finite set certifies the external theorem."}, indent=2, sort_keys=True))
