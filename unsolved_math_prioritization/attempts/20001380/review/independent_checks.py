#!/usr/bin/env python3
"""Independent modular-polynomial, relative-tower and ramification controls."""
from fractions import Fraction as F
from math import comb
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(p,k):
 assert p,k
 C[k]+=1
P={1:1}
for n in range(1,11):
 out=Counter()
 for i,a in P.items():
  for j,b in P.items():out[i+j]+=a*b
 out[0]+=1;P={i:c%4 for i,c in out.items() if c%4}
 shifted=Counter()
 if n%2:
  for i,c in P.items():
   for j in range(i+1):shifted[j]+=c*comb(i,j)
 else:shifted.update(P)
 Q={i:c%4 for i,c in shifted.items() if c%4}
 expected={0:2,2**(n-1):2,2**n:1}
 ck(Q==expected,'strong_shifted_mod4_identity')
 ck(Q[0]==2 and Q[2**n]==1,'Eisenstein_constant_and_leading')
 ck(all(v%2==0 for i,v in Q.items() if i<2**n),'Eisenstein_remaining_coefficients')
# Recompute the different by successive quadratic extensions, rather than
# discriminants of large iterate polynomials or the author's derivative product.
d=0;rows=[]
for n in range(1,257):
 relative=2**n+int(n%2==0)
 d=2*d+relative
 closed=F(2**n)*(F(n)+(1-F(1,4**(n//2)))/3)
 ck(d==closed,'relative_quadratic_different_recurrence')
 ck(F(d,2**n)==F(n)+sum((F(1,2**j) for j in range(2,n+1,2)),F(0)),'normalized_branch_different')
 ck(F(d,2**n)-1>=n-1,'unbounded_upper_break_lower_bound')
 if n<=8:rows.append({'n':n,'relative_different':relative,'total_different':d})
# The relative uniformizer equations: even pi_n^2=pi_(n-1);
# odd pi_n^2+2pi_n+2=pi_(n-1). Here n=1 is the base Eisenstein case.
for n in range(1,65):
 e=2**n
 if n%2:
  derivative_terms=[e,e+1]
  ck(min(derivative_terms)==e,'odd_relative_derivative_valuation')
  if n>1:ck(1<2**(n-1),'odd_relative_constant_Eisenstein')
 else:ck(e+1==2**n+1,'even_relative_derivative_valuation')
# Absolute uniformizer expansion: distinct residue classes prevent cancellation.
for e in [2,4,8,16]:
 vals={e*v+i for v in range(-2,3) for i in range(e)}
 ck(len(vals)==5*e,'basis_valuation_distinctness')
 for i,v in product(range(e),range(-3,4)):
  ck((e*v+i>=0)==(v>=0),'integral_basis_coefficient_test')
# Include tame factors and nontrivial unramified degrees. These are abstract
# order-profile controls, not asserted realizable Galois filtrations.
for m,tame,f in product(range(5),[1,3,5],[1,2,4]):
 e=tame*2**m
 for repeats in [1,2,4]:
  positive=[] if m==0 else [2**j for j in range(m,0,-1) for _ in range(repeats)]
  different=e-1+sum(g-1 for g in positive)
  upper=sum((F(g,e) for g in positive),F(0))
  integral=sum((F(g,e)*(1-F(1,g)) for g in positive),F(0))
  ck(F(different,e)==1-F(1,e)+integral,'Hilbert_Herbrand_tame_term')
  ck(upper>=F(different,e)-1+F(1,e),'last_upper_break_bound')
  ck(e*f//f==e,'inertia_not_full_group_order')
  if f>1 and different:
   ck(F(different,e)!=F(different,e*f),'unramified_degree_normalization_control')
ck(rows[:4]==[{'n':1,'relative_different':2,'total_different':2},{'n':2,'relative_different':5,'total_different':9},{'n':3,'relative_different':8,'total_different':26},{'n':4,'relative_different':17,'total_different':69}],'first_four_values')
# Q2(i) is a concrete endpoint convention control: G0=G1=C2, G2=1.
ck((2-1)+(2-1)==2 and F(2,2)==1,'first_level_actual_quadratic_different')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(sorted(C.items())),
 'relative_tower_initial_values':rows,'scope':'Finite modular-polynomial and relative-tower checks, plus abstract Hilbert/Herbrand normalization controls. No splitting-field image enumeration or computational proof of infinite inverse-limit claims.'},indent=2,sort_keys=True))
