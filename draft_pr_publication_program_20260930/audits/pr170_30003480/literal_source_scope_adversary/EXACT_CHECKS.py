from fractions import Fraction as F
from itertools import product
from math import prod
import json

d=[F(2401,10000),F(81,625),F(81,625),F(1,10000)]
r=[F(49,100),F(36,100),F(36,100),F(1,100)]
assert all(0<x<F(1,4) for x in d)
assert [x*x for x in r]==d
polygon_factors=[sum(d)-2*x for x in d]
assert all(x>0 for x in polygon_factors)
q1=prod(polygon_factors)
all_sign_factors=[sum(e*x for e,x in zip(eps,r)) for eps in product([-1,1],repeat=4)]
assert len(all_sign_factors)==16
q2=F(1,2)*prod(all_sign_factors)
assert q1==F(168760917,305175781250)
assert q2==F(23632249608,2384185791015625)
assert q1-q2==F(2589624828909,4768371582031250)>0
assert d[0]>F(2,5)*(1-F(2,5))
assert d[1]<F(1,6)*(1-F(1,6))
assert d[2]<F(1,6)*(1-F(1,6))
assert d[3]<F(1,100)*(1-F(1,100))
assert F(1,3)+F(1,100)<F(2,5)

def diagonal_parity_check(t):
 a,b,c=t
 w=[1-(a+b+c)/2,(b+c-a)/2,(a+c-b)/2,(a+b-c)/2]
 assert all(x>=0 for x in w)
 assert sum(w)==1
 small=[w[2]+w[3],w[1]+w[3],w[1]+w[2]]
 assert small==list(t)
 assert all(0<=x<=F(1,2) for x in small)
 det=[x*(1-x) for x in small]
 return {'t':list(map(str,t)), 'weights':list(map(str,w)), 'determinants':list(map(str,det))}
parity=[diagonal_parity_check(t) for t in [(F(0),F(0),F(0)),(F(0),F(1,2),F(1,2)),(F(1,2),F(1,2),F(1,2)),(F(1,5),F(1,10),F(1,10)),(F(1,3),F(1,3),F(1,3))]]
for t in [(F(1,5),F(1,10),F(1,10)),(F(1,3),F(1,3),F(1,3))]:
 a,b,c=t;d3=[x*(1-x) for x in t]
 assert all(0<x<F(1,4) for x in d3)
 assert all(sum(d3)-2*x>0 for x in d3)
ghzq1=F(1,64)
ghzq2=F(1,2)*prod(sum(F(e,2) for e in eps) for eps in product([-1,1],repeat=3))
assert ghzq2==F(9,512)>ghzq1
assert F(1,4)>F(3,16)
print(json.dumps({'Q1':str(q1),'Q2':str(q2),'Q1_minus_Q2':str(q1-q2),'all_sign_factors':list(map(str,all_sign_factors)),'parity_support_boundary_checks':parity,'GHZ_Q1':str(ghzq1),'GHZ_Q2':str(ghzq2),'passed':True},indent=2))
