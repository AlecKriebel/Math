#!/usr/bin/env python3
from itertools import combinations

def inter(words):
    z=set(words[0])
    for w in words[1:]: z &= set(w)
    return frozenset(z)

def maxima(C):
    return {w for w in C if not any(w < v for v in C)}

def core(C):
    M=sorted(maxima(C),key=lambda x:(len(x),sorted(x)))
    out={frozenset()}
    for r in range(1,len(M)+1):
        for A in combinations(M,r): out.add(inter(A))
    return out

C={frozenset(),frozenset({1,2,3}),frozenset({1,2,4}),frozenset({1,3,4}),
   frozenset({1,2}),frozenset({1,3}),frozenset({1,4}),frozenset({1})}
B=core(C)
assert B <= C
assert maxima(B)==maxima(C)
# Delete missing core words by nondecreasing cardinality from C union B.
# Calibration where the missing word 1 is an intersection of strict survivors 12 and 13.
E={frozenset(),frozenset({1,2}),frozenset({1,3}),frozenset({1,2,4}),frozenset({1,3,5})}
sigma=frozenset({1}); tau=frozenset({1,2}); ups=frozenset({1,3})
assert tau in E and ups in E and tau & ups == sigma and sigma not in E
# Inclusion-minimal family check.
M=[frozenset({1,2,4}),frozenset({1,3,5})]
assert inter(M)==sigma
for m in M: assert m > sigma
print('MAXIMAL-INTERSECTION CORE PASS')
print('BINARY-MEET IDENTITY PASS')
print('STRICT SURVIVING SUPERWORDS PASS')
