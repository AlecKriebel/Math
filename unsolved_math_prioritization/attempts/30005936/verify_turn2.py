#!/usr/bin/env python3
"""Exact algebra for the quantitative high-moment/cutoff estimates; no SPDE simulation."""
from fractions import Fraction as F
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1
for p in range(2,65):
 ok(F(p*(p-1),2)*F(2,p)==p-1)
 for n in range(2,33):
  h=F(1,n);tau=h*h;sites=(n*n+1)*(n+1);ok(sites<=4*n**3)
  if p>6:ok(F(1,2)-F(3,p)>0)
for j in range(1,1001):
 z=F(1,j);ok((1-z)**2<=1-z);ok(j*(j-1)>=(j-1)**2)
for den in range(1,31):
 for num in range(101):
  x=F(num,den);ok(min(F(1),x)**2<=x)
for K in range(1,101):
 tau=F(1,K*K)
 near=tau*tau*sum(j*j for j in range(1,K+1));ok(near<=F(1,K))
 far=sum(F(1,j*j) for j in range(K+1,5*K+1));ok(far<=F(1,K))
# Generic weighted-Volterra contraction arithmetic on finite rational kernels.
for B in [F(1,8),F(1,4),F(1,3)]:
 for A in [F(1),F(3,7)]:
  fs=[A]
  for m in range(1,41):
   fm=A+B*sum(fs[k]/(m-k) for k in range(m));fs.append(fm)
   rho=B*sum(F(1,j*2**j) for j in range(1,m+1));ok(rho<F(1,2))
   ok(max(fs[k]/2**k for k in range(m+1))<=A/(1-rho))
# The power cutoff has the claimed Lipschitz bound on fourth-power test values.
for b in range(1,21):
 R=b**4;L=F(5*b,4);ok(L**4==F(625,256)*R)
 vals=list(range(-5,0))+[a**4 for a in range(0,26)]
 g=lambda v:0 if v<=0 else min(next(a for a in range(26) if a**4==v),b)**5
 for x,y in zip(vals,vals[1:]):ok(abs(g(y)-g(x))<=L*abs(y-x))
 for N in range(2,31):
  tau=F(1,N*N);ok(N*L*L*tau==F(25,16)*N*tau*b*b)
ok(F(1,2)-F(3,64)==F(29,64))
print(json.dumps(dict(status='PASS',assertions=checks,scope='finite algebraic controls; BDG, kernel approximation and convolution proofs are analytical'),sort_keys=True,indent=2))
