#!/usr/bin/env python3
"""Locally authored arithmetic checks supporting a credited source audit, not new topology."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json,sympy as s
C=Counter()
def ck(x,key):assert bool(x),key;C[key]+=1
# Quadratic field represented as a+b*sqrt(-15).
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def scale(c,x):return(c*x[0],c*x[1])
def mul(x,y):return(x[0]*y[0]-15*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
a=(F(7,8),F(1,8));ab=(a[0],-a[1]);bad=(F(7,4),F(1,4))
poly=lambda x:add(add(scale(4,mul(x,x)),scale(-7,x)),(F(4),F(0)))
ck(poly(a)==(0,0),'correct_quadratic_root');ck(mul(a,ab)==(1,0),'reciprocal_conjugates');ck(poly(bad)!=(0,0),'printed_denominator_negative_control')
ck((-7)**2-4*4*4==-15,'irreducible_discriminant');ck(4+7+4==15,'nonsquare_determinant')
for sign in (-1,1):
 for a,c in product(range(5),repeat=2):
  if (sign*2*c*c-a*a)%5==0:ck(a==0 and c==0,'mod5_norm_forces_two_divisibilities')
 for a,b,c in product(range(25),repeat=3):
  if (sign*2*c*c-a*a-15*b*b)%25==0:ck(a%5==b%5==c%5==0,'mod25_norm_primitive_obstruction')
t,f,g,gb=s.symbols('t f g gb',nonzero=True);A=s.Matrix([[-2*t+3-2/t,1,g],[1,-2,0],[gb,0,f]])
ck(s.cancel(A.det()-f*(4*t-7+4/t)-2*g*gb)==0,'equivariant_matrix_determinant')
# Laurent polynomial parity sums, allowing arbitrary shifts and integral coefficients.
for coeff in product(range(-2,3),repeat=3):
 for shift in range(-3,4):
  h={shift+i:F(c) for i,c in enumerate(coeff)}
  def pmul(x,y):
   z={}
   for i,a in x.items():
    for j,b in y.items():z[i+j]=z.get(i+j,F(0))+a*b
   return z
  gg=pmul(pmul({1:F(1),0:F(-1)},{2:F(4),1:F(-7),0:F(4)}),h)
  hv=sum(c*(1 if i%2==0 else -1) for i,c in h.items());even=sum(c for i,c in gg.items() if i%2==0);odd=sum(c for i,c in gg.items() if i%2)
  ck(even==-15*hv and odd==15*hv,'lift_linking_parity_multiple_15')
# Entire small primary groups, both surgery signs; all isotropic elements are forced into a too-small group.
for k in range(3):
 mod=5**(2*k+1)
 for coeff in (-6,6):
  isotropic=[]
  for x in range(5):
   for y in range(mod):
    iso=(2*x*x*5**(2*k)+coeff*y*y)%mod==0
    expected=(x==0 and y%(5**(k+1))==0)
    ck(iso==expected,'complete_small_primary_isotropy')
    if iso:isotropic.append((x,y))
  ck(len(isotropic)==5**k<5**(k+1),'metabolizer_order_obstruction')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'sympy_version':s.__version__,'scope':'Arithmetic validation of a published proof and its printed root-denominator typo. No new proof turn or claim to rederive the geometric surgery construction.'},indent=2))
