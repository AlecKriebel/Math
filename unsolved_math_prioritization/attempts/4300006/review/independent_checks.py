#!/usr/bin/env python3
"""Independent exact orbit-normal-form and compact-period diagnostics."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import sympy as s
counts={}
def ck(t,g):
 assert bool(t),g
 counts[g]=counts.get(g,0)+1
def vp(x,p):
 x=F(x)
 if not x:return None
 n,d=abs(x.numerator),x.denominator;v=0
 while n%p==0:n//=p;v+=1
 while d%p==0:d//=p;v-=1
 return v
# Normalize by repeated scalar operations, independently of the submitted floor formula.
def normal(x,lam,p):
 if not x:return 0,F(0)
 a=vp(lam,p);k=0;z=F(x)
 if a>0:
  while vp(z,p)>=a:z/=lam;k+=1
  while vp(z,p)<0:z*=lam;k-=1
 else:
  while vp(z,p)<=a:z/=lam;k+=1
  while vp(z,p)>0:z*=lam;k-=1
 return k,z
def conj(x,lam,mu,p):
 k,z=normal(x,lam,p);return mu**k*z
for p in [2,3,7]:
 for a in [-4,-1,1,3]:
  lam=F(p)**a*(1+p);mu=lam*(1+p*p)
  points=[F(0)]+[F(p)**k*u for k in range(-5,6) for u in [F(1),F(-1),F(1,1+p)]]
  for x in points:
   q,z=normal(x,lam,p);hx=conj(x,lam,mu,p)
   ck(lam**q*z==x,'orbit representative reconstruction')
   ck(hx== (F(0) if not x else (mu/lam)**(vp(x,p)//a)*x),'independent orbit formula')
   ck(conj(hx,mu,lam,p)==x,'surjective inverse')
   ck(conj(lam*x,lam,mu,p)==mu*hx,'intertwining all signs')
   ck(vp(hx,p)==vp(x,p),'valuation preservation')
  for i,x in enumerate(points):
   for j in [i,(i+1)%len(points),(i+7)%len(points)]:
    y=points[j]
    ck(vp(conj(x,lam,mu,p)-conj(y,lam,mu,p),p)==vp(x-y,p),'exact isometry controls')
 # Infinite-log argument is analytic; verify finite leading terms and denominators exactly.
 total=F(0)
 for n in range(1,65):
  term=F((-1)**(n+1)*p**(2*n),n);total+=term
  ck(vp(total,p)==2,'logarithm partial-sum valuation')
  if n>=2:ck(vp(term,p)>=n+1,'uniform logarithm tail bound')
 u=1+p*p
 ck(conj(F(1),F(p),F(p*u),p)+conj(F(p-1),F(p),F(p*u),p)!=conj(F(p),F(p),F(p*u),p),'nonadditive witness')
 # For the compact system f=p t-u, n-periodic configurations form the
 # kernel of the torus endomorphism p*cyclic_shift-u*I.
 for n in range(1,9):
  S=s.zeros(n)
  for i in range(n):S[i,(i+1)%n]=1
  M=p*S-u*s.eye(n)
  ck(abs(M.det())==u**n-p**n,'compact periodic point count')
  ck(vp(F(u**n-p**n),p)==0,'compact count is p-adic unit')
  for scalar in [F(p),F(p*u),F(1,p),F(1,p*u)]:
   ck(scalar**n!=1,'local fixed point uniqueness')
 for n in range(2,34):
  z=F(p,u)**n
  # The first logarithm term has valuation n; every subsequent term is higher.
  for j in range(2,9):ck(vp(z**j/F(j),p)>n,'compact log remainder leading valuation')
  ck(n-vp(F(n),p)>=n//2,'normalized periodic logarithm decay')
root=Path(__file__).resolve().parent
result={'verdict':'PASS','assertions':sum(counts.values()),'categories':counts,'artifact_sha256':sha256((root/'author_replay/OBSTRUCTION.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact bounded rational/residue diagnostics plus compact fixed-point determinant controls. The all-prime statements and limiting claims are audited in the written report.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
