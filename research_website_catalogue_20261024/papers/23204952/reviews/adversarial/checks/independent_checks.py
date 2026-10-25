"""Exact finite sanity checks; theorem proofs are in REVIEW.md, not this script."""
from fractions import Fraction as F
from math import comb
import json

results=[]
for n in range(2,129):
    b=2*F(n-1,n)**n
    nxt=2*F(n,n+1)**(n+1)
    assert F(1,2)<=b<nxt<1
    assert (n+1)**n<3*n**n
    r=n-1
    ambient_coefficient=r**(n+1)-3*(n+1)*r**n
    assert -ambient_coefficient==2*(n+2)*(n-1)**n
    if n>=5:assert 2*(r-1)>n
results.append({'check':'ODP density monotonicity, cubic threshold, CM coefficient and n>=5 index','dimensions':[2,128],'passed':True})

# Exact equality case: (-J_1,J_2) squares to -Id, is orthogonal and commutes with J, but is neither global sign.
def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return list(map(list,zip(*a)))
J=[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]
I=[[0,1,0,0],[-1,0,0,0],[0,0,0,-1],[0,0,1,0]]
identity=[[int(i==j) for j in range(4)] for i in range(4)]
neg_identity=[[-x for x in row] for row in identity]
assert matmul(I,I)==neg_identity
assert matmul(tr(I),I)==identity
assert matmul(I,J)==matmul(J,I)
assert I!=J and I!=[[-x for x in row] for row in J]
results.append({'check':'mixed factor complex structure at excluded equality','passed':True})

# Cartier factor bound cannot support two positive-dimensional factors above strict threshold.
for m in range(1,129):
    for r in range(2,m+2):
        if 2*(r-1)>m:
            assert not any(d>=r-1 and m-d>=r-1 for d in range(1,m))
results.append({'check':'integer boundary of factor-dimension obstruction','dimensions':[1,128],'passed':True})
print(json.dumps({'scope':'Finite exact arithmetic and matrix sanity checks only; no validation of cited external theorems','results':results,'passed':True},indent=2))
