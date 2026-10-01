#!/usr/bin/env python3
"""Exact finite checks for the first-turn scoped algebraic statements."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json
C=Counter()
def ck(v,n):
 assert v,n
 C[n]+=1
def mod(x,m=1):return x%m
def q(x,sgn=1):return mod(F(sgn*sum(x),4))
def A(x):return tuple((y+sum(x))%2 for y in x)
V=list(product([0,1],repeat=4))
for x in V:
 ck(A(A(x))==x,'explicit_isometry_involutive')
 ck(q(A(x))==q(x,-1),'explicit_quadratic_isometry')
 for y in V:
  ck(sum(a*b for a,b in zip(A(x),A(y)))%2==sum(a*b for a,b in zip(x,y))%2,'bilinear_pairing_preserved')
for e,f in product([0,1],repeat=2):
 plus=F(1+8*e);minus=F(-1+8*f)
 ck(mod(plus,8)==1 and mod(minus,8)==7,'all_possible_lifts_reduce_correctly')
 ck(mod(4*plus,16)==4 and mod(4*minus,16)==12,'fourfold_values_forced')
 ck(mod(4*plus-4*minus,16)==8,'isometry_lift_contradiction')
# The Z/3 quadratic function and its nondegenerate polarization.
q3=lambda x:mod(F(x*x-x,6))
for x in range(-9,10):
 ck(q3(x+3)==q3(x),'nonhomogeneous_Z3_well_defined')
 for y in range(-9,10):ck(mod(q3(x+y)-q3(x)-q3(y))==mod(F(x*y,3)),'nonhomogeneous_Z3_pairing')
ck([q3(x) for x in range(3)]==[F(0),F(0),F(1,3)],'Z3_gauss_exponents')
ck(mod(F(8,12),8)==F(2,3),'rational_Brown_value_not_integral')
# Discriminant f=diag(0,2), c=(2,0): exact quotient/radical and section checks.
Q=lambda r,j:mod(F(j*j,4)-r)
for den in range(1,18):
 for num in range(den):
  r=F(num,den)
  for j in range(2):
   ck(Q(r+1,j)==Q(r,j),'divisible_coordinate_well_defined')
   ck(Q(r,j+2)==Q(r,j),'finite_coordinate_well_defined')
   for s,k in [(F(0),0),(F(1,3),1),(F(1,2),0)]:ck(mod(Q(r+s,j+k)-Q(r,j)-Q(s,k))==mod(F(j*k,2)),'full_discriminant_polarization')
  ck(Q(r,0)==mod(-r),'nonzero_radical_restriction')
for j in range(2):
 ck(Q(F(0),j)==mod(F(j,4)),'section_zero_gives_q_plus')
 ck(Q(F(j,2),j)==mod(F(-j,4)),'section_half_gives_q_minus')
 for k in range(2):ck(mod(F((j+k)%2,2))==mod(F(j,2)+F(k,2)),'second_section_is_group_homomorphism')
# Exact Gaussian integer multiplication; avoids floating Gauss-sum phases.
mul=lambda z,w:(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
for gauss in [(1,1),(1,-1)]:
 square=mul(gauss,gauss);fourth=mul(square,square);ck(fourth==(-4,0),'fourfold_Gauss_sums_agree')
ck((1,1)!=(1,-1),'two_section_Gauss_sums_differ')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Finite quadratic isometry, lift arithmetic and section-dependence controls. The topological Y1 consequence uses the stated Deloup–Massuyeau theorem; the intended degree-one target is unresolved.'},indent=2))
