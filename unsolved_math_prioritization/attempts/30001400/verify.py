#!/usr/bin/env python3
"""Exact finite diagnostics for the credited fixed-dimensional closure reduction."""
from fractions import Fraction as F
from itertools import product
from math import prod,isqrt
from pathlib import Path
import hashlib,json
C={}
def ck(v,k):
 assert v,k
 C[k]=C.get(k,0)+1

def compositions(n,d):
 if d==1:
  if n>=1:yield (n,)
  return
 for a in range(1,n-d+2):
  for tail in compositions(n-a,d-1):yield (a,)+tail

def N(a,p):return sum((x**p for x in a),F(0))
def tensor(a,b):return tuple(x*y for x in a for y in b)
def major(a,b):
 a=sorted(a,reverse=True);b=sorted(b,reverse=True)
 if len(a)!=len(b) or sum(a)!=sum(b):return False
 sa=sb=F(0)
 for x,y in zip(a,b):
  sa+=x;sb+=y
  if sa>sb:return False
 return True

def sqrt_interval(a):
 scale=10**12;k=isqrt(a.numerator*scale*scale//a.denominator)
 return F(k,scale),F(k+1,scale)

def root_sum_bounds(a,inverse=False):
 ints=[sqrt_interval(x) for x in a]
 if inverse:ints=[(1/hi,1/lo) for lo,hi in ints]
 return sum((lo for lo,_ in ints),F(0)),sum((hi for _,hi in ints),F(0))

vectors=0;perturbations=0
for d in range(1,6):
 u=(F(1,d),)*d
 for comp in compositions(8,d):
  x=tuple(F(c,8) for c in comp);vectors+=1
  ck(major(u,x),'uniform_branch')
  for eps in [F(1,5),F(1,2),F(4,5)]:
   z=tuple((1-eps)*a+eps/d for a in x);perturbations+=1
   ck(len(z)==d and sum(z)==1 and min(z)>0,'fixed_dimension')
   ck(sum(abs(a-b) for a,b in zip(z,x))==eps*sum(abs(a-b) for a,b in zip(u,x)),'l1_approximation')
   B=[[(1-eps)*F(i==j)+eps/d for j in range(d)] for i in range(d)]
   ck(all(sum(row)==1 for row in B),'bistochastic')
   ck(all(sum(B[i][j] for i in range(d))==1 for j in range(d)),'bistochastic')
   ck(tuple(sum(B[i][j]*x[j] for j in range(d)) for i in range(d))==z,'bistochastic')
   ck(major(z,x),'ordinary_smoothing')
   ck(N(z,0)==d and N(z,1)==1,'zero_one_orders')
   if x==u:
    ck(z==x,'uniform_branch');continue
   ck(max(z)<max(x) and min(z)>min(x),'extreme_strictness')
   ck(prod(z)>prod(x),'log_product_derivative')
   for p in [-4,-3,-2,-1,2,3,4,5]:
    ck(N(z,p)<N(x,p),'integer_power_strictness')
    ck(N(z,p)<(1-eps)*N(x,p)+eps*N(u,p),'strict_convexity_control')
   loz,hiz=root_sum_bounds(z);lox,hix=root_sum_bounds(x)
   ck(loz>hix,'positive_fractional_power')
   loz,hiz=root_sum_bounds(z,True);lox,hix=root_sum_bounds(x,True)
   ck(hiz<lox,'negative_fractional_power')
   # The reversed-experiment raw power sum, before applying log/(alpha-1).
   for p in [-3,-2,-1,2,3]:
    direct=sum((F(1,d)**(1-p)*a**p for a in z),F(0))
    ck(direct==F(d)**(p-1)*N(z,p),'renyi_conversion_raw_sums')
   ck(max(d*a for a in z)<max(d*a for a in x),'likelihood_extrema')
   ck(min(d*a for a in z)>min(d*a for a in x),'likelihood_extrema')
  # Multiplicativity is checked against literal products, not used as a shortcut.
  for p in [-2,-1,0,1,2,3]:
   xx=tensor(x,x)
   ck(N(xx,p)==N(x,p)**2,'tensor_power_sums')

# A positive example separates ordinary and multiple-copy order.
x=tuple(F(a,100) for a in (39,39,11,11));y=tuple(F(a,100) for a in (50,25,24,1))
ck(not major(x,y),'nontrivial_order_control')
for n in range(2,5):
 xn=tuple(prod(z) for z in product(x,repeat=n));yn=tuple(prod(z) for z in product(y,repeat=n))
 ck(major(xn,yn),'nontrivial_order_control')
 ck(min(xn)>=min(yn),'last_majorization_inequality')
# Exact telescoping catalyst for the two-copy certificate.
c=tuple(a/2 for a in x+y)
ck(sum(c)==1 and min(c)>0,'catalyst_control')
ck(major(tensor(x,c),tensor(y,c)),'catalyst_control')
for eps in [F(1,7),F(1,3),F(2,3)]:
 z=tuple((1-eps)*a+eps/4 for a in x)
 ck(major(tensor(z,z),tensor(y,y)),'smoothing_certificate')
 ck(max(z)<max(y) and min(z)>min(y),'genericity_certificate')
 ck(prod(z)>prod(y),'derivative_certificate')

# Polynomial curvature signs and algebraic derivative normalization.
for p in [F(-5),F(-1,2),F(1,4),F(1,2),F(3,4),F(3,2),F(5)]:
 ck((p*(p-1)>0)==(p<0 or p>1),'curvature_sign')
for d in range(1,9):
 # At the uniform vector log d + average log(1/d) = 0 exactly at the
 # product level, and the zero-order power sum is d, not log d.
 ck(F(d)**d*F(1,d)**d==1,'zero_derivative_normalization')
 ck(N((F(1,d),)*d,0)==d,'zero_derivative_normalization')

b=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':C,'positive_test_vectors':vectors,'same_dimension_perturbations':perturbations,'artifact_sha256':hashlib.sha256((b/'KNOWN_CONSEQUENCE.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact rational and certified square-root bounds for finite diagnostics; the continuum of orders follows from convexity/concavity in the proof. Eventual tensor majorization is imported from the credited published theorem, not inferred from these checks.'}
(b/'verification.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
