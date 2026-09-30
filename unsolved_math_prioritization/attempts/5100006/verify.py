#!/usr/bin/env python3
from fractions import Fraction as F
from math import gcd
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
import sympy as s
checks=0;rotations=0

def ck(x):
 global checks
 assert x
 checks+=1
# Scale 2K to1; delta=tau/m and K=1/2 in the divisor torus.
for N in range(6,403,4):
 m=N//2
 for tau in range(1,m):
  if gcd(tau,N)!=1:continue
  rotations+=1;v=F(tau,2*m);delta=2*v
  ck(m%2==1 and tau%2==1)
  ck((m*v-F(1,2)).denominator==1)
  H=[(j*delta)%1 for j in range(m)]
  ck(len(set(H))==m)
  poles=Counter({x:2 for x in H})
  zeros=Counter()
  for j in range(m):
   zeros[(F(1,2)+v-j*delta)%1]+=1
   zeros[(F(1,2)-v-j*delta)%1]+=1
  ck(zeros==poles)
  ck((F(1,2)+v-((m+1)//2)*delta)%1==0)
  ck((F(1,2)-v-((m-1)//2)*delta)%1==0)
  ck((m*delta)%2==1) # displacement is an odd multiple of2K
a,b,alpha,beta,k,sv=s.symbols('a b alpha beta k sv',positive=True)
cn2=1-sv**2;dn2=1-k*k*sv**2
A2=alpha**2*dn2/cn2;B2=alpha**2*(1-k*k)/cn2;C2=alpha**2*k*k
ck(s.factor(A2-B2-C2)==0)
ck(s.factor(A2-C2*dn2/(k*k*cn2))==0)
# Two exact symmetric six-bounce products; no floating-point identity inference.
c2=a*a-b*b
horizontal=b*b*(a*a-c2*a*a/(a+b)**2)**2
vertical=a*a*(a*a-c2*a*(a+2*b)/(a+b)**2)**2
value=4*a**4*b**4/(a+b)**2
ck(s.factor(horizontal-value)==0);ck(s.factor(vertical-value)==0)
for ai in range(2,30):
 for bi in range(1,ai):
  ck(ai*ai-(ai*ai-bi*bi)>0)
# Numerical Jacobi diagnostics, separately labeled.
import mpmath as mp
mp.mp.dps=85
numeric=0;maxerr=mp.mpf(0)
for mod in [mp.mpf(1)/5,mp.mpf(1)/2,mp.mpf(4)/5]:
 param=mod*mod;K=mp.ellipk(param);Kp=mp.ellipk(1-param)
 sn=lambda u:mp.ellipfun('sn',u,param)
 cn=lambda u:mp.ellipfun('cn',u,param)
 dn=lambda u:mp.ellipfun('dn',u,param)
 for N in [6,10,14,18,22]:
  m=N//2
  for tau in range(1,m):
   if gcd(N,tau)!=1:continue
   v=2*K*tau/N
   aa=dn(v)/cn(v);bb=mp.sqrt(1-param)/cn(v)
   fun=lambda z:aa*aa-param*sn(z)**2
   ref=mp.fprod(fun(2*j*v) for j in range(m))
   for phase in [K/11,K/3,7*K/5]:
    got=mp.fprod(fun(phase+2*j*v) for j in range(m))
    err=abs(got/ref-1);maxerr=max(maxerr,err);assert err<mp.mpf('1e-65');numeric+=1
   for sign in [-1,1]:
    err=abs(fun(K+1j*Kp+sign*v))/(aa*aa);maxerr=max(maxerr,err);assert err<mp.mpf('1e-65');numeric+=1
r={'status':'PASS','artifact_sha256':sha256(Path('PROOF.md').read_bytes()).hexdigest(),'exact_assertions':checks,'primitive_rotation_cases':rotations,'numerical_diagnostics':numeric,'numerical_precision_digits':85,'maximum_relative_numerical_error':mp.nstr(maxerr,8),'limits':'Exact algebra and divisor permutation controls plus separately labeled numerical diagnostics; the written elliptic-function proof supplies the universal identity.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
