#!/usr/bin/env python3
"""Independent exact checks for Livingston's published slicing obstruction."""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
import json
C=Counter()
def ck(test,name):
 assert test,name
 C[name]+=1
# Work in Q[t]/(4t^2-7t+4), using coordinates 1,t, rather than sqrt(-15).
def mul(x,y):
 a,b=x;c,d=y
 return (a*c-b*d,a*d+b*c+Q(7,4)*b*d)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def scale(a,x):return (a*x[0],a*x[1])
def conj(x):return (x[0]+Q(7,4)*x[1],-x[1])
t=(Q(0),Q(1));one=(Q(1),Q(0));zero=(Q(0),Q(0))
ck(add(add(scale(4,mul(t,t)),scale(-7,t)),scale(4,one))==zero,'quadratic_field')
ck(mul(t,conj(t))==one,'quadratic_field')
# The printed /4 root equals 2t in this presentation.
bad=scale(2,t)
ck(add(add(scale(4,mul(bad,bad)),scale(-7,bad)),scale(4,one))!=zero,'printed_root_negative_control')
ck(mul(bad,conj(bad))==(Q(4),Q(0)),'printed_root_negative_control')
for a,b in product(range(-12,13),repeat=2):
 z=(Q(a),Q(b));n=mul(z,conj(z))
 ck(n[1]==0 and n[0]==Q(a*a)+Q(7,4)*a*b+b*b,'field_norm')
 ck(n[0]>0 or a==b==0,'field_norm')
# Exhaustive mod25 residue proof, then an independent mod125 lifting control:
# any solution of a^2+15b^2= +/-2c^2 mod25 has all coordinates divisible by5.
for sign in (-1,1):
 for a,b,c in product(range(25),repeat=3):
  if (a*a+15*b*b-sign*2*c*c)%25==0:
   ck(a%5==b%5==c%5==0,'primitive_norm_obstruction')
 for b,a,c in product(range(25),range(5),range(5)):
  aa=5*a;cc=5*c
  if (aa*aa+15*b*b-sign*2*cc*cc)%125==0:
   ck(b%5==0,'norm_hensel_control')
# Seifert matrix V=[[2,1],[0,2]] has determinant polynomial4t²-7t+4.
for value in [Q(i,j) for i in range(-10,11) for j in range(1,6)]:
 a=2-2*value;b=1;c=-value;d=2-2*value
 ck(a*d-b*c==4*value*value-7*value+4,'genus_one_seifert_matrix')
ck(4*(-1)**2-7*(-1)+4==15,'determinant_not_square')
ck(all(i*i!=15 for i in range(5)),'determinant_not_square')
# Rational tangle[4,-4] has numerator15. Changing two crossings in its
# four-crossing twist box reduces it to[0,-4], of numerator-1.
ck(Q(4)+Q(1,-4)==Q(15,4),'ordinary_two_change_upper_bound')
ck(Q(0)+Q(1,-4)==Q(-1,4),'ordinary_two_change_upper_bound')
# The local slide algebra preserves half-integral odd denominator data.
for r,p in product(range(-8,9),range(-39,40,2)):
 a=Q(15,4);b=15*r;d=Q(p,2);slide=-4*r
 ck(b+slide*a==0,'null_homologous_slide_algebra')
 new=d+2*slide*b+slide*slide*a
 ck(new==Q(p-120*r*r,2) and new.denominator==2,'null_homologous_slide_algebra')
# Abstract square-class version of the full primary linking-form argument:
# all possible second coefficients have square residue modulo5.
units=[a for a in range(1,25) if a%5 in (1,4)]
for j,q,sign in product(range(8),range(1,30),(-1,1)):
 if q%5 and q%3 and q%2:
  ck((sign*2*3**(2*j+1)*q*q)%5 in (1,4),'second_primary_square_class')
for k in range(3):
 M=5**(2*k+1);P=5**(2*k)
 for u in units:
  isotropic=0
  for a,b in product(range(5),range(M)):
   hit=(2*a*a*P+u*b*b)%M==0
   expected=a==0 and b%(5**(k+1))==0
   ck(hit==expected,'all_primary_isotropic_vectors')
   isotropic+=hit
  ck(isotropic==5**k and isotropic<5**(k+1),'metabolizer_too_small')
# Reduce the lift polynomial directly in Z[t]/(t²-1), represented by(even,odd).
def cmul(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0])
F=(8,-7);tm1=(-1,1)
ck(cmul(F,tm1)==(-15,15),'two_cover_reduction')
for even,odd in product(range(-20,21),repeat=2):
 value=cmul(cmul(F,tm1),(even,odd))
 ck(value==(-15*(even-odd),15*(even-odd)),'two_cover_reduction')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'groups':dict(sorted(C.items())),'scope':'Exact field, norm, rational-slide, parity and complete finite primary-form controls. Published arbitrary-crossing surgery topology was checked in the full primary text and figure; it is not established by finite arithmetic tests.'},indent=2,sort_keys=True))
