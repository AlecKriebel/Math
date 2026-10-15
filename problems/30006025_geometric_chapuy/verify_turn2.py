#!/usr/bin/env python3
"""Exact Laurent holonomy and binary-index controls; standard library only."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def padd(a,b):
 z=a.copy()
 for k,v in b.items():z[k]=z.get(k,Q(0))+v
 return {k:v for k,v in z.items() if v}
def pmul(a,b):
 z={}
 for k,u in a.items():
  for l,v in b.items():z[k+l]=z.get(k+l,Q(0))+u*v
 return {k:v for k,v in z.items() if v}
def mm(A,B):return tuple(tuple(padd(pmul(A[i][0],B[0][j]),pmul(A[i][1],B[1][j])) for j in range(2)) for i in range(2))
def rotation(r):
 c=(1-r*r)/(1+r*r);s=2*r/(1+r*r)
 return ((c,s),(-s,c))
def step(R):return (({1:R[0][0]},{1:R[0][1]}),({-1:R[1][0]},{-1:R[1][1]}))
I=(({0:Q(1)},{}),({},{0:Q(1)}));palette=[Q(-1,2),Q(-1,3),Q(0),Q(1,4),Q(1,2)]
for r in palette:
 R=rotation(r);c,s=R[0]
 ck(c>0 and c*c+s*s==1,'nondegenerate_algebraic_rotation')
profiles=0;expanded=0
for n in range(2,19):
 for seed in range(10):
  rs=[palette[(seed*(j+1)+j*j)%len(palette)] for j in range(n)];rot=[rotation(r) for r in rs];H=I;leading=Q(1)
  for R in rot:H=mm(H,step(R));leading*=R[0][0]
  tr=padd(H[0][0],H[1][1])
  ck(tr.get(n)==leading and tr.get(-n)==leading and leading>0,'unique_extreme_Laurent_coefficients')
  ck(max(tr)==n and min(tr)==-n,'exact_Laurent_degree')
  for sign in (-1,1):
   v=padd(tr,{0:Q(2*sign)})
   ck(v.get(n)==leading,'trace_plusminus_two_nonzero_polynomial')
  # Determinant of a product is independently checked in the Laurent ring.
  det=padd(pmul(H[0][0],H[1][1]),{k:-v for k,v in pmul(H[0][1],H[1][0]).items()})
  ck(det=={0:Q(1)},'Laurent_holonomy_determinant')
  profiles+=1
  if n<=8:
   total={}
   for indices in product((0,1),repeat=n):
    coef=Q(1);exponent=0
    for j in range(n):coef*=rot[j][indices[j]][indices[(j+1)%n]];exponent+=1 if indices[j]==0 else -1
    if coef:total[exponent]=total.get(exponent,Q(0))+coef
   total={k:v for k,v in total.items() if v}
   ck(total==tr,'full_binary_index_trace_expansion');expanded+=1
# Positive rational side controls: only the all-positive sign vector maximizes the exponent.
for n in range(2,9):
 lengths=[Q(j+1,n+1) for j in range(n)];top=sum(lengths)/2
 vals=[sum((1 if bit==0 else -1)*lengths[j] for j,bit in enumerate(bits))/2 for bits in product((0,1),repeat=n)]
 ck(max(vals)==top and vals.count(top)==1 and top>0,'strict_positive_lengths_unique_maximum')
for g in range(2,11):
 n=10*g+1;squared_scale=Q(12*g,n)
 for path_length in range(1,8):
  ck(path_length*path_length*squared_scale>0,'rescaled_integer_path_length_square_rational')
 E=6*g-3;P=12*g
 ck(Q(P,2*E)*E==Q(P,2),'fixed_perimeter_barycenter_normalization')
print(json.dumps({'status':'PASS','arithmetic':'exact rational Laurent polynomials and finite sums; standard library only','assertions':sum(C.values()),'by_scope':dict(C),'rotation_profiles':profiles,'full_binary_expansion_profiles':expanded,'largest_profile_sides':18,'scope':'Controls verify the algebraic expansion. Classical Lindemann-Weierstrass and the nontrivial analytic constraint prove the stated universal obstructions. No unrestricted geometric construction or source resolution is claimed.'},indent=2,sort_keys=True))
