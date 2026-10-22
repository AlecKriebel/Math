#!/usr/bin/env python3
"""Exact bounded controls, not a proof of Problem 6.40. Python 3 stdlib only."""
from fractions import Fraction as F
from math import comb, isqrt
import json, platform
from pathlib import Path

def padd(a,b):
 r=[F(0)]*max(len(a),len(b))
 for i,v in enumerate(a):r[i]+=v
 for i,v in enumerate(b):r[i]+=v
 return r

def pmul(a,b):
 r=[F(0)]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):r[i+j]+=u*v
 return r

def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def us(m):
 a,b=[F(1)],[F(0),F(2)]
 if m==0:return a
 for k in range(1,m): a,b=b,padd([0]+[2*x for x in b],[-x for x in a])
 return b
identities=0
for n in range(1,21):
 left=[F(0)]
 for j in range(n):left=padd(left,us(2*j))
 assert trim(left)==trim(pmul(us(n-1),us(n-1)))
 identities+=1
# Robertson-only control: B(w)=1+w^2-w^4/2; f(z)=z B(z)^2.
B=[F(1),F(0),F(1),F(0),-F(1,2)]
a=[F(0)]+pmul(B,B)
assert a==[F(0),F(1),F(0),F(2),F(0),F(0),F(0),-F(1),F(0),F(1,4)]
assert sum(abs(a[j]) for j in [1,3,5])-a[3]**2==-1
for m in range(1,21):assert sum(v*v for v in B[:m])<=m
# For all m>=5 the LHS is 9/4, so finite verification has a stated universal tail.
assert sum(v*v for v in B)==F(9,4)
# derivative f'(iy) is 1-6t+7t^3+9t^4/4, t=y^2.
t=F(1,4)
assert 1-6*t+7*t**3+F(9,4)*t**4<0
# Symmetrization control derivative (1-6z^2+z^4)/(1+z^2)^3.
assert 1-6*F(1,4)+F(1,16)<0
# Gaussian-rational power series to degree 9.
N=9
Z=(F(0),F(0));O=(F(1),F(0))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return(a[0]*c,a[1]*c)
def powg(a,n):
 r=O
 for _ in range(n):r=mul(r,a)
 return r

def conv(a,b):
 r=[Z]*(N+1)
 for i,x in enumerate(a):
  if x==Z:continue
  for j,y in enumerate(b[:N+1-i]):
   if y!=Z:r[i+j]=add(r[i+j],mul(x,y))
 return r

def compose(a,b):
 r=[Z]*(N+1)
 for j in range(N,-1,-1):r=conv(r,b);r[0]=add(r[0],a[j])
 return r

def slit(q,u):
 y=[Z]+[scale(powg(u,j-1),q*j) for j in range(1,N+1)]
 inv=[Z]+[scale(powg(u,j-1),F((-1)**(j-1)*comb(2*j,j),j+1)) for j in range(1,N+1)]
 return compose(inv,y)

def coeff(q,u):
 return [scale(x,1/q) for x in compose([Z]+[(F(j),F(0)) for j in range(1,N+1)],slit(q,u))]

def norm2(z):return z[0]*z[0]+z[1]*z[1]
def norm_bounds(z):
 if z[1]==0:return(abs(z[0]),abs(z[0]))
 if z[0]==0:return(abs(z[1]),abs(z[1]))
 x=norm2(z);den=10**40;r=isqrt(x.numerator*den**2//x.denominator)
 lo=F(r,den);hi=lo if lo*lo==x else F(r+1,den)
 assert lo*lo<=x<=hi*hi
 return lo,hi
phases=[O,(-F(1),F(0)),(F(0),F(1)),(F(0),-F(1)),(F(3,5),F(4,5)),(F(3,5),-F(4,5)),(-F(3,5),F(4,5)),(-F(3,5),-F(4,5))]
results=[]
for q in [F(1,4),F(1,2),F(3,4)]:
 for u in phases:
  aa=coeff(q,u);assert aa[1]==O
  if u==O:assert aa==[Z]+[(F(j),F(0)) for j in range(1,N+1)]
  if u==(-F(1),F(0)):
   c=2*q-1; prev,cur=F(0),F(1)
   for j in range(1,N+1):assert aa[j]==(cur,F(0));prev,cur=cur,2*c*cur-prev
  for n in range(1,6):
   bounds=[norm_bounds(aa[j]) for j in range(1,2*n,2)]
   lo=sum(x[0] for x in bounds)-norm2(aa[n]);hi=sum(x[1] for x in bounds)-norm2(aa[n])
   assert lo>=0,(q,u,n,lo,hi)
   results.append({'q':str(q),'u':[str(x) for x in u],'n':n,'lower':str(lo),'upper':str(hi)})
out={'python':platform.python_version(),'chebyshev_polynomial_identities':identities,'Robertson_control_deficit':-1,'exact_slit_instances':24,'exact_slit_inequalities':len(results),'certified':True,'scope':'Degree 9, 24 exact one-switch parameters, n=1..5 only; no global theorem and no interval parameter coverage.','results':results}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
