#!/usr/bin/env python3
"""Independent finite boundary checks for the semigroup volume note.
Uses elementary exact integer sets, no candidate code or external dependencies.
Not a normality certificate or an all-configuration proof.
"""
from itertools import combinations_with_replacement
from math import gcd
from functools import reduce
from pathlib import Path
import json

checks=0
families=[]
# Direct multiset sums, independently of the author's iterative sumset algorithm.
for m in range(4,11):
    A=(0,1,m-1,m)
    last_hole=-1
    for k in range(m+1):
        actual={sum(t) for t in combinations_with_replacement(A,k)}
        union={j*(m-1)+offset for j in range(k+1) for offset in range(k+1)}
        assert actual==union
        checks+=1
        covered=(actual==set(range(k*m+1)))
        assert covered==(k==0 or k>=m-2)
        checks+=1
        if not covered:last_hole=k
    assert last_hole==m-3
    checks+=1
    families.append({'m':m,'last_hole':last_hole})

# Direct two-dimensional enumeration of a genuine pyramid negative control.
base=((0,0),(1,0),(3,0),(4,0))
apex=(0,1)
for j in range(9):
    k=j+1
    actual={(sum(v[0] for v in t),sum(v[1] for v in t))
            for t in combinations_with_replacement(base+(apex,),k)}
    assert (2,j) not in actual
    # Saturated triangle inequalities and full generated lattice.
    assert 0<=j<=k and 0<=2<=4*(k-j)
    checks+=2

# Ambient-lattice direction: intrinsic interval [0,1] from A={0,2}
# has no intrinsic holes, but infinitely many ambient odd holes.
for k in range(1,10):
    actual={sum(t) for t in combinations_with_replacement((0,2),k)}
    assert actual==set(range(0,2*k+1,2))
    assert 1 not in actual and 1<=2*k
    checks+=2
assert gcd(0,2)==2
checks+=1

# Unimodular simplex has no holes. All integer points in k times the triangle.
simplex=((0,0),(1,0),(0,1))
for k in range(9):
    actual={(sum(v[0] for v in t),sum(v[1] for v in t))
            for t in combinations_with_replacement(simplex,k)}
    assert actual=={(x,y) for x in range(k+1) for y in range(k+1-x)}
    checks+=1

receipt={'status':'passed','independent_assertions':checks,'families':families,
 'degree_zero_correction':'Coverage holds at k=0 as well as k>=m-2',
 'controls':['pyramid gives holes in arbitrarily high tested degrees','larger ambient lattice introduces holes','unimodular simplex has no tested holes'],
 'scope':'Finite exact checks supplement, but do not prove, the general theorem or infinite negative controls'}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
