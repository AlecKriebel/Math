#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product,combinations
from math import prod
import json
C={}
def ck(x,s):
 assert x,s
 C[s]=C.get(s,0)+1
pairs=list(combinations(range(4),2))
matchings=[{(0,1),(2,3)},{(0,2),(1,3)},{(0,3),(1,2)}]
def R(p):return Q(3,16)*p*p if p<=Q(1,2) else 3*p**4*(1-p)**2

def direct(w,A):
 total=Q(0);n=len(w)
 for I in product(range(n),repeat=4):
  wt=prod(w[i] for i in I)
  for M in matchings:
   z=wt
   for i,j in pairs:z*=1-A[I[i]][I[j]] if (i,j) in M else A[I[i]][I[j]]
   total+=z
 return total

support_cases=integrals=0
for masses in [(i,j,6-i-j) for i in range(1,5) for j in range(1,6-i)]:
 w=[Q(m,6) for m in masses]
 for vals in product([Q(j,4) for j in range(5)],repeat=3):
  m1,m2,m3=[sum(wi*f**j for wi,f in zip(w,vals)) for j in(1,2,3)]
  p=m1*m1;c=3*(m2*m2-m3*m3)**2
  ck(m2>=p,'jensen_second_moment')
  ck(m2<=m1 and m3<=m2,'bounded_factor_moments')
  ck(m3*m1>=m2*m2,'cauchy_moment_bridge')
  ck(c<=R(p),'rank_one_profile_bound')
  if p:
   z=m2*m2/p
   ck(p<=z<=1,'reduced_moment_interval')
   ck(0<=m2*m2-m3*m3<=p*z*(1-z),'nonnegative_square_bound')
   if p>=Q(1,2) and c==R(p):ck(len(set(vals))==1,'high_density_equality_condition')
  if masses==(1,2,3):
   A=[[f*g for g in vals] for f in vals]
   ck(direct(w,A)==c,'independent_kernel_factorization');integrals+=1
  support_cases+=1
for j in range(1,11):
 alpha=Q(j,10);p=alpha*alpha/2
 c=direct([alpha,1-alpha],[[Q(1,2),Q(0)],[Q(0),Q(0)]])
 ck(c==R(p)==Q(3,64)*alpha**4,'low_density_optimizer_direct')
for j in range(8,17):
 p=Q(j,16);c=direct([Q(1)],[[p]])
 ck(c==R(p)==3*p**4*(1-p)**2,'high_density_optimizer_direct')
for j,k in product(range(1,11),repeat=2):
 alpha=Q(j,10);d=Q(k,10);p=(alpha*d)**2
 c=direct([alpha,1-alpha],[[d*d,Q(0)],[Q(0),Q(0)]])
 ck(c==3*p*p*d**4*(1-d*d)**2,'vertical_family_formula')
 ck(c<=R(p),'vertical_family_range')
ck(R(Q(1,2))==Q(3,64),'branch_junction')
ck((12,-30,18)==(6*2,6*(-5),6*3),'upper_branch_derivative_coefficients')
ck(R(Q(2,3))==Q(16,243),'restricted_inducibility_value')
ck(Q(3,4)**2*sum(Q(3,4)**j for j in range(4))-1==Q(551,1024),'high_gap_constant')
ck(Q(3,2)-3*Q(3,4)**4==Q(141,256),'middle_gap_constant')
for j in range(1,11):
 p=Q(j,20)
 ck(Q(3,2)*p*p-R(p)==Q(21,16)*p*p,'low_gap_exact')
gap_cases=0
for r in range(2,31):
 for j in range(1,10):
  t=Q(j,10);a=1/(r+t);b=t*a;q=r*a*a+b*b;p=1-q
  F=3*(q*q-r*a**4-b**4)
  ck(F>R(p),'strict_candidate_separation')
  if p<=Q(3,4):ck(F-R(p)>=Q(141,256)*q*q,'middle_gap_bound')
  else:
   ck(a<=Q(1,r)<=q/p,'maximal_part_bound')
   ck(F-R(p)>=Q(1653,1024)*q**3,'high_gap_bound')
  gap_cases+=1
print(json.dumps({'assertions':sum(C.values()),'by_scope':C,
 'arithmetic':'exact fractions; independent six-edge kernel integration',
 'rational_finite_support_cases':support_cases,'independent_product_kernel_integrals':integrals,
 'optimizer_kernel_controls':19,'vertical_family_controls':100,'explicit_gap_controls':gap_cases,
 'scope':'The exact rank-one family profile is proved by moment inequalities; the source-wide profile remains unresolved.'},indent=2)+'\n',end='')
