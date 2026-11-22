#!/usr/bin/env python3
from fractions import Fraction as F
import hashlib,json,pathlib
D=[1,2,3,5,6,7]; u=[1,-1,-1,-1,1,-1]
v=[a*int(d%2==0) for a,d in zip(u,D)]
def prime(n):return n>=2 and all(n%i for i in range(2,int(n**.5)+1))
def L(c,n):return sum(a for a,d in zip(c,D) if n*(n+2)%d==0)
def bil(c,t,sc=False):return sum(L(c,n)*L(t,n)*((prime(n)+prime(n+2)) if sc else 1) for n in range(10,50))
a=bil(u,u);rho=F(bil(u,u,True),a)
dr=2*(F(bil(u,v,True))-rho*bil(u,v))/a
c=[F(x)-F(y,2) for x,y in zip(u,v)]
results=[a,bil(u,u,True),rho,dr,bil(c,c),bil(c,c,True),F(bil(c,c,True),bil(c,c))]
expected=[35,15,F(3,7),F(-24,245),F(65,2),15,F(6,13)]
if results!=expected:raise RuntimeError((results,expected))
p=pathlib.Path(__file__).parent
print(json.dumps({'status':'PASS','results':list(map(str,results)),'sha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['FINITE_PRODUCT_EXAMPLE.md','verify_finite_product.py']}},indent=2))
