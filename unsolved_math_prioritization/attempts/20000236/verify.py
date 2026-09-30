#!/usr/bin/env python3
import sympy as s
from itertools import combinations,permutations
from math import comb,prod,factorial
from pathlib import Path
from hashlib import sha256
import json
count=0

def ck(p):
 global count
 assert p
 count+=1
w,u1,u2,u3,v1,v2,v3,t=s.symbols('w u1 u2 u3 v1 v2 v3 t')
u=[u1,u2,u3];v=[v1,v2,v3]
M=[u1*v2-u2*v1,u1*v3-u3*v1,u2*v3-u3*v2]
p={(1,2):w,**{(1,j+3):u[j] for j in range(3)},**{(2,j+3):v[j] for j in range(3)},(3,4):0,(3,5):0,(4,5):0}
rels=[]
for a,b,c,d in combinations(range(1,6),4):
 rel=s.expand(p[a,b]*p[c,d]-p[a,c]*p[b,d]+p[a,d]*p[b,c]);rels.append(rel)
 ck(rel==0 or any(s.expand(rel-z)==0 or s.expand(rel+z)==0 for z in M))
for z in M:ck(any(s.expand(rel-z)==0 or s.expand(rel+z)==0 for rel in rels))
ck(s.expand(u1*M[2]-u2*M[1]+u3*M[0])==0)
ck(s.expand(v1*M[2]-v2*M[1]+v3*M[0])==0)
ck(s.cancel((1-3*t*t+2*t**3)/(1-t)**7-(1+2*t)/(1-t)**5)==0)
ck(s.cancel((1-t)**3*(1+2*t)/(1-t)**5-(1+2*t)/(1-t)**2)==0)
# Independent Segre bidegree monomial count, then free cone variable.
def h(m):return sum((j+1)*comb(j+2,2) for j in range(m+1)) if m>=0 else 0
for m in range(0,101):
 hb=comb(m+4,4)+(2*comb(m+3,4) if m>=1 else 0)
 ck(h(m)==hb)
 section=sum((-1)**j*comb(3,j)*h(m-j) for j in range(4))
 ck(section==(1 if m==0 else 3*m+1))
for n in range(5,201):
 lam=(n-3,n-5);N=2*(n-2)
 ck(lam[0]>=lam[1]>=0 and lam[0]<=n-2)
 ck(sum(lam)+3==N-1)
 ck((n-2+1-lam[0],n-2+2-lam[1])==(2,5))
 ck((n-2-lam[1],n-2-lam[0])==(3,1))
# Standard Young tableaux of shape(3,1), independently enumerated.
syts=[]
for p in permutations(range(1,5)):
 if p[0]<p[1]<p[2] and p[0]<p[3]:syts.append(p)
ck(len(syts)==3);ck(factorial(4)//(4*2*1*1)==3)
# Characteristic-zero Wronskian leading coefficient.
wr_cases=0
for n in range(3,13):
 for k in range(1,min(n,4)+1):
  for degrees in combinations(range(n),k):
   D=s.Matrix([[prod(range(d-j+1,d+1)) if j else 1 for d in degrees] for j in range(k)])
   want=prod(degrees[b]-degrees[a] for a in range(k) for b in range(a+1,k))
   ck(D.det()==want and want!=0);wr_cases+=1
x,y,z=s.symbols('x y z');f=z*(x*x+y*y+z*z)
for a in [s.I,-s.I]:
 at={x:a,y:1,z:0};ck(f.subs(at)==0)
 for var in (x,y,z):ck(s.diff(f,var).subs(at)==0)
# Normalization arithmetic alternatives behind the degree-three theorem.
for r in (1,2):
 for chi in range(1,5):
  for g in range(5):
   delta=r-g-chi
   if delta>=0 and delta%2==0:ck(delta==0)
receipt={'status':'PASS','assertions':count,'Wronskian_degree_cases':wr_cases,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Exact algebraic controls, not enumeration of real Schubert configurations'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
