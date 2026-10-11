#!/usr/bin/env python3
"""Exact controls for the odd-Chern canonical origin and scalar-lift bookkeeping."""
from math import gcd
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json
C=Counter()
def ck(v,n):
 assert v,n
 C[n]+=1
# Abstract finite cyclic Spin^c torsors, including nontrivial even primary parts.
for two_power in [1,2,4,8,16,32]:
 for odd in range(1,22,2):
  N=two_power*odd
  for sigma in range(N):
   chern=(2*sigma)%N
   chern_order=N//gcd(N,chern)
   if chern_order%2: 
    choices=[a for a in range(N) if (N//gcd(N,a))%2 and 2*a%N==chern]
    ck(len(choices)==1,'unique_odd_half_of_odd_Chern_class')
    a=choices[0];s=(sigma-a)%N
    ck(2*s%N==0,'canonical_origin_is_spin')
    for h in [0,N//2] if N%2==0 else [0]:
     ck(((sigma+h-a)%N)==((s+h)%N),'spin_translation_equivariance_on_valid_domain')
    ck(((-sigma+a)%N)==s,'conjugation_preserves_canonical_spin_origin')
   else:
    ck(all(2*a%N!=chern for a in range(N) if (N//gcd(N,a))%2),'nonzero_even_Chern_has_no_odd_half')
  if two_power<=2:ck(all((N//gcd(N,2*j))%2 for j in range(N)),'exponent_two_component_entirely_covered')
# No retraction in the stated extra affine/conjugation-natural Z4 model.
found=0
for r1,r3 in product([0,2],repeat=2):
 r=[0,r1,2,r3]
 conjugation=all(r[(-j)%4]==(-r[j])%4 for j in range(4))
 translation=all(r[(j+2)%4]==(r[j]+2)%4 for j in range(4))
 ck(not(conjugation and translation),'no_full_Z4_natural_spin_retraction');found+=int(conjugation and translation)
ck(found==0,'all_retractions_exhausted')
# Any two mod16 lifts of a fixed phase differ by exactly kernel element0 or8.
for den in range(1,13):
 for num in range(8*den):
  b=F(num,den)
  for d in [0,1]:
   f=(b+8*d)%16;ck(f%8==b,'kernel_lift_reduction');ck((f-b)%16==8*d,'kernel_parameter_unique')
# Four-term finite type equivalence for every binary correction pattern.
for d in product([0,1],repeat=4):
 derivative=d[0]-d[1]-d[2]+d[3]
 for den in [1,3,5]:
  base=F(1,den)
  f=[base+8*x for x in d]
  ck(((f[0]-f[1]-f[2]+f[3])%16==0)==(derivative%2==0),'finite_type_relation_injective_kernel')
# Explicit failure of the weak principal-branch construction's additional properties.
branch=lambda b:b%8
ck(branch(F(1))==1 and branch(F(-1))==7,'RP3_principal_values')
ck((branch(F(-1))+branch(F(1)))%16==8,'weak_branch_not_orientation_odd')
ck(branch(F(-4))==4 and 4*branch(F(-1))%16==12,'weak_branch_not_connected_sum_additive')
ck(branch(F(-1))!=15,'weak_branch_does_not_recover_negative_Rochlin')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Canonical finite-group odd-Chern origin, restricted extra-naturality obstruction and scalar finite-type bookkeeping. The genuine topological domain theorem uses the source-checked classical inputs; no unrestricted solution is asserted.'},indent=2))
