"""Exact finite controls for C4 and C5; universal proofs are in CERTIFICATES.md."""
from fractions import Fraction as F
import json

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def unit(n,i,j):
    return [[F(int((r,c)==(i,j))) for c in range(n)] for r in range(n)]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(s,a): return [[s*x for x in r] for r in a]
def prod(*xs):
    a=xs[0]
    for b in xs[1:]: a=mul(a,b)
    return a

n=4
e00=unit(n,0,0)
xs={i:add(unit(n,0,i),unit(n,i,0)) for i in range(1,n)}
checks=0
for i,x in xs.items():
    assert prod(x,x,x)==x; checks+=1
    assert prod(x,x)[0][0]==1; checks+=1
    for j,y in xs.items():
        if i==j:continue
        assert prod(x,x,y,y)==e00; checks+=1
        assert prod(x,e00)==unit(n,i,0); checks+=1
        assert prod(e00,y)==unit(n,0,j); checks+=1
        assert prod(x,e00,y)==unit(n,i,j); checks+=1
        assert prod(x,y,x,y)[0][0]==0; checks+=1
z=[[F(1),F(0)],[F(0),F(-1)]]
rho=[[F(1,2),F(1,6)],[F(1,6),F(1,2)]]
assert sum(rho[i][i] for i in range(2))==1; checks+=1
assert rho[0][0]*rho[1][1]-rho[0][1]*rho[1][0]==F(2,9); checks+=1
for i in range(2):
    for j in range(2):
        u=unit(2,i,j)
        expectation=scale(F(1,3),add(scale(2,u),prod(z,u,z)))
        assert expectation==scale(F(1) if i==j else F(1,3),u); checks+=1
print(json.dumps({'status':'PASS','exact_finite_controls':checks,'scope':'C4 matrix-unit identities; C5 faithful density and conditional expectation. No infinite-quantifier or novelty certification.'},indent=2))
