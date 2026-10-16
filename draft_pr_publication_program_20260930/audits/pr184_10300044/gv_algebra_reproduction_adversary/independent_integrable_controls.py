#!/usr/bin/env python3
"""Exact local Frobenius/GV/rescaling tests with rational Taylor jets.
A symbolic derivation, not these finitely many tests, supplies general identities.
This does not construct a global compact-support suspension or certify tautness.
"""
from fractions import Fraction as Q
from math import factorial
import json
D=4
IND=[(i,j,k) for i in range(D+1) for j in range(D+1-i) for k in range(D+1-i-j)]
ZERO=(0,0,0)
def plus(a,b):return {m:a.get(m,Q(0))+b.get(m,Q(0)) for m in IND if a.get(m,Q(0))+b.get(m,Q(0))}
def neg(a):return {m:-v for m,v in a.items()}
def times(a,b):
 r={}
 for m,v in a.items():
  for n,w in b.items():
   z=tuple(m[i]+n[i] for i in range(3))
   if sum(z)<=D:r[z]=r.get(z,Q(0))+v*w
 return {m:v for m,v in r.items() if v}
def const(a):return {ZERO:Q(a)} if a else {}
def inv(a):
 c=a.get(ZERO,Q(0))
 if c==0:raise ZeroDivisionError('Taylor reciprocal has zero denominator')
 u=times(plus(a,neg(const(c))),const(-1/c));r={};p=const(1)
 for k in range(D+1):r=plus(r,p);p=times(p,u)
 return times(r,const(1/c))
def power(a,n):
 r=const(1)
 for k in range(n):r=times(r,a)
 return r
def var(i,v):
 r=const(v);m=[0,0,0];m[i]=1;r[tuple(m)]=Q(1);return r
def derivative(a,i):
 r={}
 for m,v in a.items():
  if m[i]:n=list(m);n[i]-=1;r[tuple(n)]=v*m[i]
 return r
def value(a):return a.get(ZERO,Q(0))
def curl(a):return [plus(derivative(a[2],1),neg(derivative(a[1],2))),plus(derivative(a[0],2),neg(derivative(a[2],0))),plus(derivative(a[1],0),neg(derivative(a[0],1)))]
def dot(a,b):
 r={}
 for i in range(3):r=plus(r,times(a[i],b[i]))
 return r
def cross(a,b):return [plus(times(a[1],b[2]),neg(times(a[2],b[1]))),plus(times(a[2],b[0]),neg(times(a[0],b[2]))),plus(times(a[0],b[1]),neg(times(a[1],b[0])))]
checks=[]
def check(label,b):
 checks.append(label)
 if not b:raise RuntimeError(label)
def block(x,y,z):
 den=plus(const(1),plus(times(const(2),times(x,z)),times(const(3),times(y,power(z,2)))))
 return [times(power(z,2),inv(den)),times(power(z,3),inv(den)),const(1)]
for xv in [Q(0),Q(1,4)]:
 for yv in [Q(0),Q(1,4)]:
  for zv in [Q(1,10),Q(1,3)]:
   x,y,z=[var(i,v) for i,v in enumerate([xv,yv,zv])]
   a=block(x,y,z);e=[derivative(a[0],2),derivative(a[1],2),{}]
   check('actual integrable alpha: Frobenius',value(dot(a,curl(a)))==0)
   check('actual integrable alpha: dalpha=alpha wedge eta',all(value(plus(curl(a)[i],neg(cross(a,e)[i])))==0 for i in range(3)))
   den=1+2*xv*zv+3*yv*zv*zv
   rho=(-6*zv**2-16*xv*zv**3-(8*xv*xv+18*yv)*zv**4-12*xv*yv*zv**5)/den**4
   check('independently derived rational GV density',value(dot(e,curl(e)))==rho)
   for off,ell in [(Q(1,7),Q(1,11)),(Q(2,9),Q(3,17))]:
    t=var(2,off+ell*zv);u=times(plus(t,neg(const(off))),const(1/ell))
    aa=block(x,y,u);aa[0]=times(aa[0],const(ell));aa[1]=times(aa[1],const(ell))
    ee=[derivative(aa[0],2),derivative(aa[1],2),{}]
    check('compressed integrability',value(dot(aa,curl(aa)))==0)
    check('density scales by reciprocal positive length',value(dot(ee,curl(ee)))==rho/ell)
x,y,z=[var(i,Q(0)) for i in range(3)]
check('negative control nonintegrable dz+x dy',value(dot([{},x,const(1)],curl([{},x,const(1)])))==1)
try:inv({})
except ZeroDivisionError:check('zero denominator rejected',True)
else:check('zero denominator rejected',False)
print(json.dumps({'status':'PASS','checks':len(checks),'mechanism':'exact rational Taylor coefficients of normalized dF for F=z+x*z^2+y*z^3','parameter_domain':'8 rational points with positive D and two positive compressions; identities separately derived in FIRST_ASSESSMENT.md','global_foliation_certificate':False,'tautness_certificate':False},indent=2))
