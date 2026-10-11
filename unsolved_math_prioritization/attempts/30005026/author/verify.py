#!/usr/bin/env python3
"""Exact finite controls for authored propositions; not an infinite-process proof."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

if not __debug__:
    raise SystemExit('Run without -O; assertions must be active.')
checks = 0

def check(ok, label):
    global checks
    if not ok:
        raise AssertionError(label)
    checks += 1

def w(k):
    return Q(4, k*(k+1)*(k+2))

s = Q(0)
m = Q(0)
for n in range(1, 501):
    s += w(n)
    m += n*w(n)
    check(w(n) == Q(2,n*(n+1))-Q(2,(n+1)*(n+2)), 'telescoping weight')
    check(s == 1-Q(2,(n+1)*(n+2)), 'normalization partial sum')
    check(m == 2-Q(4,n+2), 'first moment partial sum')
    check(w(n)/2**n > w(n+1)/2**(n+1), 'strictly decreasing atom groups')

# Exact optimal top-M marginal mass, using equal-probability groups.
def missed_mass(M):
    remaining = M
    covered = Q(0)
    k = 1
    while remaining:
        take = min(remaining, 2**k)
        covered += take*w(k)/2**k
        remaining -= take
        k += 1
    return 1-covered

def ceil_log2(M):
    return (M-1).bit_length()

for M in list(range(1,1001))+[2**k+i for k in range(11,41) for i in (-1,0,1)]:
    K = ceil_log2(M)+1
    check(2**K >= 2*M, 'half-group threshold')
    check(missed_mass(M) >= Q(1,K*(K+1)), 'optimal marginal missed-mass bound')

# Count words and geometric composition containment on small cubes.
for d in range(1,4):
    for r in range(4):
        cube = list(product(range(-r,r+1),repeat=d))
        check(len(cube)==(2*r+1)**d, 'cube cardinality')
        for x in cube:
            for y in cube:
                check(max(abs(a+b) for a,b in zip(x,y))<=2*r, 'B_r+B_r subset B_2r')
for d in range(1,4):
    for r in range(4):
        for b in range(1,5):
            M=b**((2*r+1)**d)
            K=ceil_log2(M)+1
            check(2**K>=2*M,'source-word support threshold')
            check(Q(1,K*(K+1))>0,'positive universal tail lower bound')

out={
    'status':'PASS',
    'assertions':checks,
    'arithmetic':'exact rational and integer',
    'claim_scope':'Finite controls for distribution identities, optimal omitted mass and composition geometry.',
    'not_proved_by_computation':['General finite-valued open problem','Compactness theorem','Markov coding theorem','Gabor equal-entropy obstruction'],
    'general_target_status':'unresolved',
    'literal_unrestricted_target_status':'counterexample proved in written argument',
}
print(json.dumps(out,indent=2))
if '--write' in __import__('sys').argv:
    Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
