"""Exact Dedekind reciprocity and lens-space controls; no quantum evaluation."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
from hashlib import sha256
import json

counts = {}
def check(category, value):
    assert value, category
    counts[category] = counts.get(category, 0)+1

def symbol(a,b):
    # Euclidean recursion from reciprocity, unlike the submitted finite sum.
    a %= b
    if b == 1:
        return F(0)
    assert a and gcd(a,b) == 1
    return F(a,b)+F(b,a)+F(1,a*b)-3-symbol(b,a)

def direct(a,b):
    return F(3, b*b)*sum((2*j-b)*(2*((a*j)%b)-b) for j in range(1,b))

for b in range(2,51):
    for a in range(1,b):
        if gcd(a,b) == 1:
            check('reciprocity_vs_integer_sum', symbol(a,b) == direct(a,b))
            check('orientation_sign', symbol(-a,b) == -symbol(a,b))
            check('inverse_invariance', symbol(pow(a,-1,b),b) == symbol(a,b))
for a in (4,9):
    check('witness_symbol', symbol(a,25) == F(48,25))
    check('witness_sum', symbol(a,25)/12 == F(4,25))
orbit4 = {s*pow(4,e,25)%25 for s in (-1,1) for e in (-1,1)}
orbit9 = {s*pow(9,e,25)%25 for s in (-1,1) for e in (-1,1)}
check('unoriented_orbits_disjoint', orbit4.isdisjoint(orbit9))
check('orbit4', orbit4 == {4,6,19,21})
check('orbit9', orbit9 == {9,11,14,16})

def matmul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
for q, chain in ((4,(7,2,2,2)),(9,(3,5,2))):
    m=((1,0),(0,1))
    for c in chain:
        m=matmul(m,((c,-1),(1,0)))
    check('surgery_word_first_column', (m[0][0],m[1][0]) == (25,q))
    check('surgery_word_determinant', m[0][0]*m[1][1]-m[0][1]*m[1][0] == 1)
check('shifted_level', 5-2 == 3 and 5 >= 3)

root=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((root/'author_replay/SOURCE_STATUS.md').read_bytes()).hexdigest(),
     'exact_assertions':sum(counts.values()),'categories':counts,
     'quantum_invariant_recomputed':False,
     'scope':'Dedekind symbols by reciprocity and integer sums; modular homeomorphism orbits; SL2 integer surgery words; permitted level. Full LMO and quantum separation remain credited primary-source results.'}
(root/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
