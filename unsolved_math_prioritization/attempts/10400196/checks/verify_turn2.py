#!/usr/bin/env python3
"""Exact odd-primary arithmetic and explicit absorption matrix controls."""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
C=Counter()
def ck(v,n):
 assert v,n
 C[n]+=1
def eta(x):
 x=x%1;n=x.denominator;assert n%2
 return F(2*((pow(2,-1,n)*x.numerator)%n),n)%2 if n>1 else F(0)
values={F(m,n)%1 for n in range(1,40,2) for m in range(n)}
for x in values:
 e=eta(x);ck(e%1==x,'odd_section_reduction');ck((x.denominator*e)%2==0,'odd_section_odd_order')
 ck(eta(-x)==(-e)%2,'odd_section_negation')
 ck(eta(x+1)==e,'odd_section_presentation_independence')
 for y in [F(0),F(1,3),F(2,5),F(4,7)]:ck(eta(x+y)==(eta(x)+eta(y))%2,'odd_section_additive')
# Every cyclic odd nonsingular linking form, with its unique homogeneous refinement.
for n in range(3,34,2):
 half=pow(2,-1,n)
 for b in range(1,n):
  if gcd(b,n)!=1:continue
  q=lambda x:(F(b*half*x*x,n))%1
  pairing=lambda x,y:F(b*x*y,n)%1
  for a in range(n):
   qa=q(a);ck(qa.denominator%2==1,'odd_quadratic_value_domain')
   for x in range(n):
    ck((q(x)+pairing(a,x))%1==(q(x+a)-qa)%1,'exact_square_completion')
   for r in [0,1,7,8,15]:
    lift=(F(r)-8*eta(qa))%16
    ck(lift%8==(F(r)-8*qa)%8,'mod16_lift_reduces_to_Brown')
# Nonsplitting on the two-primary scalar subgroup.
for e in [F(1,2),F(3,2)]:
 ck(e%1==F(1,2),'all_order_two_scalar_preimages')
 ck((2*e)%2==1,'no_order_two_section')
# Full matrix, not only characteristic-label arithmetic.
def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A):return list(map(list,zip(*A)))
B=[[0,0],[0,2]];P=[[1,1],[0,1]]
ck(mul(mul(transpose(P),B),P)==B,'absorption_preserves_full_linking_matrix')
for k in range(1,20,2):
 for c in [0,2]:
  new=mul(transpose(P),[[2*k],[c]])
  ck(new[0][0]==2*k,'absorption_free_Chern_unchanged')
  ck(new[1][0]%4==(c+2)%4,'absorption_torsion_label_swapped')
for x in [1,9]:
 for y in [7,15]:ck((x-y)%8!=0,'absorbed_RP3_lifts_cannot_be_equal')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Exact canonical odd-primary section, quadratic translation, normalization and Kirby-label controls. Topological naturality and finite-type conclusions use the explicitly cited primary theorems; no full original-target claim.'},indent=2))
