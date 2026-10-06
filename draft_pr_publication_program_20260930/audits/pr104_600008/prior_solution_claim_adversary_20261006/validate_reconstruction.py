#!/usr/bin/env python3
"""Exact polynomial and rational checks; standard library only, no source files or network."""
import json
from fractions import Fraction
from math import comb

class Poly:
 def __init__(self, terms=None): self.terms={k:Fraction(v) for k,v in (terms or {}).items() if v}
 @staticmethod
 def cast(x): return x if isinstance(x,Poly) else Poly({(0,)*5:Fraction(x)})
 @staticmethod
 def var(i):
  k=[0]*5; k[i]=1; return Poly({tuple(k):1})
 def __add__(self,other):
  other=self.cast(other); out=self.terms.copy()
  for k,v in other.terms.items(): out[k]=out.get(k,0)+v
  return Poly(out)
 __radd__=__add__
 def __neg__(self): return Poly({k:-v for k,v in self.terms.items()})
 def __sub__(self,other): return self+-self.cast(other)
 def __rsub__(self,other): return self.cast(other)+-self
 def __mul__(self,other):
  other=self.cast(other); out={}
  for k,v in self.terms.items():
   for j,u in other.terms.items():
    e=tuple(x+y for x,y in zip(k,j)); out[e]=out.get(e,0)+v*u
  return Poly(out)
 __rmul__=__mul__
 def __pow__(self,n):
  out=self.cast(1)
  for _ in range(n): out=out*self
  return out
 def zero(self): return not self.terms

a,b,c,v,h=[Poly.var(i) for i in range(5)]
w=a*h+b*(1-h); D=(a+c)*(b+c)
# Each expression is the numerator after multiplying the stated metric
# residual by its nonzero common denominator on a>b>0,c>0,0<v<c,0<h<1.
metric_checks={
 "gtt_numerator_over_D_times_c_plus_w": (a*(a+v)*h*(b+c)*(c+w)+b*(b+v)*(1-h)*(a+c)*(c+w)-c*(c-v)*(a-b)**2*h*(1-h)-(v+w)*w*D).zero(),
 "gtv_numerator_over_2D_sin_t_cos_t": (-a*(b+c)+b*(a+c)+c*(a-b)).zero(),
 "gvv_numerator_over_4D_times_a_plus_v_times_b_plus_v_times_c_minus_v": (a*(1-h)*(b+c)*(b+v)*(c-v)+b*h*(a+c)*(a+v)*(c-v)-c*(c+w)*(a+v)*(b+v)+(v+w)*v*D).zero(),
 "scalar_w_differential_squared_numerator": (4*w*((a-b)**2*h*(1-h)-(a-w)*(w-b))).zero(),
}
# Exact top-square leading Hankel minors after gamma row/column scaling.
# c_j is minus the coefficient of u^j in sqrt(1-u); d_j is the coefficient
# in 1/sqrt(1-u). Their positive moment representations prove all sizes.
def det(A):
 A=[list(row) for row in A]; d=Fraction(1)
 for i in range(len(A)):
  if A[i][i]==0:
   j=next(j for j in range(i+1,len(A)) if A[j][i])
   A[i],A[j]=A[j],A[i]; d=-d
  pivot=A[i][i]; d*=pivot
  for j in range(i+1,len(A)):
   ratio=A[j][i]/pivot
   for k in range(i+1,len(A)): A[j][k]-=ratio*A[i][k]
 return d
def ca(j): return Fraction(comb(2*j,j),(2*j-1)*4**j)
def cb(j): return Fraction(comb(2*j,j),4**j)
minors={}
for size in range(1,11):
 da=det([[ca(4+i+j) for j in range(size)] for i in range(size)])
 db=det([[cb(3+i+j) for j in range(size)] for i in range(size)])
 assert da>0 and db>0
 minors[str(size)]={"even_leading_minor":str(da),"odd_leading_minor":str(db)}
assert all(metric_checks.values())
print(json.dumps({"metric_and_scalar_checks":metric_checks,"leading_hankel_minors":minors,"scope":"Exact rational identities and finite illustrative minors; the report supplies the all-size moment proof and global closure argument."},indent=2))
