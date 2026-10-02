#!/usr/bin/env python3
"""Exact controls for the stated identities, not a proof of the remaining inequality."""
from fractions import Fraction as F
import json
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
class D:
 def __init__(self,x,y=0):self.x=F(x);self.y=F(y)
 def __add__(self,b):
  if not isinstance(b,D):b=D(b)
  return D(self.x+b.x,self.y+b.y)
 __radd__=__add__
 def __neg__(self):return D(-self.x,-self.y)
 def __sub__(self,b):return self+-b
 def __rsub__(self,b):return -self+b
 def __mul__(self,b):
  if not isinstance(b,D):b=D(b)
  return D(self.x*b.x,self.y*b.x+self.x*b.y)
 __rmul__=__mul__
 def __truediv__(self,b):
  if not isinstance(b,D):b=D(b)
  return D(self.x/b.x,(self.y*b.x-self.x*b.y)/b.x**2)
 def __rtruediv__(self,b):return D(b)/self
 def __pow__(self,n):
  if n==0:return D(1)
  return D(self.x**n,n*self.x**(n-1)*self.y)
for den in range(3,100):
 for num in range(1,den):
  r=F(num,den)
  ck((r*r/(1-r*r)**2)/(r/(1+r)**2)==r/(1-r)**2)
  ck((2*r*(1+r*r)/(1-r*r)**3)/((1-r)/(1+r)**3)==2*r*(1+r*r)/(1-r)**4)
  ck((1-r)**4-2*r*(1+r*r)==r**4-6*r**3+6*r*r-6*r+1)
  ck((r**4-6*r**3+6*r*r-6*r+1)/r**2==(r+1/r)**2-6*(r+1/r)+4)
  a=D(1,1);w=r*(a+r)/(1+a*r);wp=(a+2*r+a*r*r)/(1+a*r)**2
  H=wp*(1-w)/(1+w)**3/((1-r)/(1+r)**3)
  ck(H.x==1);ck(H.y==(r*r-6*r+1)/(1+r)**2)
  ck(((1+r)/(1-r))**4>1)
# Exact bracket of the zero-initial-derivative sharp radius.
p=lambda r:r**4-6*r**3+6*r*r-6*r+1
ck(p(F(19,100))>0);ck(p(F(1,5))<0)
# Derivative of a Schur transform, at rational real values; full complex formula is analytic.
for den in range(3,18):
 for i in range(den):
  a=F(i,den)
  for j in range(-den+1,den):
   r=F(1,5);c=r*F(j,den);cp=F(j,den)
   z=D(r,1);om=D(c,cp);ph=z*(a+om)/(1+a*om)
   ck(ph.x==r*(a+c)/(1+a*c))
   ck(ph.y==(a+c)/(1+a*c)+r*(1-a*a)*cp/(1+a*c)**2)
   center=(a+2*c+a*c*c)/(1+a*c)**2
   ck(center==((a+c)/(1+a*c)+r*(1-a*a)*(c/r)/(1+a*c)**2))
print(json.dumps({'status':'PASS','exact_assertions':checks,'floating_diagnostics':0,'scope':'Endpoint and Schur-jet identities, sharpness derivative; no certification of the remaining all-parameter inequality'},indent=2))

