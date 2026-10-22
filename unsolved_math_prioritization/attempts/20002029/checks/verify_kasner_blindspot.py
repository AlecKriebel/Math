#!/usr/bin/env python3
"""Exact nonzero Weyl-quartic invariant invisible to diagonal curvature tests."""
from itertools import product, combinations
from fractions import Fraction as Q
import json
n=8; ids=range(n)
omega=[]
for terms in [[(0,1,1),(2,3,1)],[(0,2,1),(1,3,-1)],[(0,3,1),(1,2,1)]]:
    a=[[0]*n for _ in ids]
    for i,j,v in terms:a[i][j]=v;a[j][i]=-v
    omega.append(a)
lam=(1,1,-2)
W={(a,b,c,d):sum(lam[s]*omega[s][a][b]*omega[s][c][d] for s in range(3)) for a,b,c,d in product(ids,repeat=4)}
assert all(W[a,b,c,d]==-W[b,a,c,d] and W[a,b,c,d]==W[c,d,a,b] and W[a,b,c,d]+W[a,c,d,b]+W[a,d,b,c]==0 for a,b,c,d in W)
assert all(sum(W[a,b,a,d] for a in ids)==0 for b,d in product(ids,repeat=2))
def fourform(R,i,j,k,l):
    return sum(R[a,b,i,j]*R[a,b,k,l]-R[a,b,i,k]*R[a,b,j,l]+R[a,b,i,l]*R[a,b,j,k] for a,b in product(ids,repeat=2))
values={q:fourform(W,*q) for q in combinations(ids,4)}
assert values[0,1,2,3]==24
assert sum(v*v for v in values.values())==576
# A symbolic diagonal tensor argument is in the proof; this finite exact test checks its implementation.
K={(a,b):Q((a+1)*(b+1)) if a!=b else Q(0) for a,b in product(ids,repeat=2)}
D={(a,b,c,d):K[a,b]*((a==c)*(b==d)-(a==d)*(b==c)) for a,b,c,d in product(ids,repeat=4)}
assert all(fourform(D,*q)==0 for q in combinations(ids,4))
print(json.dumps({'dimension':8,'nonzero_fourform_components':{str(q):v for q,v in values.items() if v},'norm_squared':576,'weyl_symmetries_and_traces_verified':True,'diagonal_test_zero':True},indent=2))
