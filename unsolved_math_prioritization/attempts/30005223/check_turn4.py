#!/usr/bin/env python3
"""Exact Jacobi-Trudi row-assignment fiber polynomials, independent of MN evaluation."""
from character_tools import parts,character,strip,types
from fractions import Fraction as F
from collections import Counter,defaultdict
from itertools import permutations,product
from math import factorial
import json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
def mul(a,b):
 out=defaultdict(F)
 for i,x in a.items():
  for j,y in b.items():out[i+j]+=x*y
 return dict(out)
def hermite_complete(n):
 if n<0:return {}
 return {r:F(1,2**r*factorial(r)*factorial(n-2*r)) for r in range(n//2+1)}
def determinant_shift(lam,shifts):
 ell=len(lam);out=defaultdict(F)
 for pi in permutations(range(ell)):
  sgn=(-1)**sum(pi[i]>pi[j] for i in range(ell) for j in range(i+1,ell))
  poly={0:F(sgn)}
  for i in range(ell):poly=mul(poly,hermite_complete(lam[i]-i+pi[i]-shifts[i]))
  for r,c in poly.items():out[r]+=c
 return {r:c for r,c in out.items() if c}
def residual_polynomial(lam,nu):
 out=defaultdict(F);ell=len(lam)
 for assignment in product(range(ell),repeat=len(nu)):
  shifts=[0]*ell
  for row,t in zip(assignment,nu):shifts[row]+=t
  for r,c in determinant_shift(lam,shifts).items():out[r]+=c
 return {r:c for r,c in out.items() if c}
for n in range(1,11):
 for lam in parts(n):
  if len(lam)>4:continue
  for size in range(n+1):
   for nu in parts(size):
    if any(t<3 for t in nu):continue
    R=n-size;pol=residual_polynomial(lam,nu)
    for r in range(R//2+1):
     mu=tuple(sorted(nu+(2,)*r+(1,)*(R-2*r),reverse=True))
     expected=F(character(lam,mu),2**r*factorial(r)*factorial(R-2*r))
     ck(pol.get(r,F(0))==expected,'row_assignment_coefficient_vs_character')
lam=(5,2,2,2);nu=(3,3);R=5
ck(residual_polynomial(lam,nu)=={},'actual_irreducible_zero_fiber_polynomial')
for r in range(3):
 mu=nu+(2,)*r+(1,)*(5-2*r)
 ck(character(lam,mu)==0 and not any(types(lam,mu)),'whole_fiber_outside_three_types')
# Full residual Schur expansion, not just specialization to involutions.
v={lam:1}
for t in nu:
 out=defaultdict(int)
 for l,c in v.items():
  for eta,sign in strip(l,t):out[eta]+=c*sign
 v={k:x for k,x in out.items() if x}
ck(v=={(2,2,1):-2,(2,1,1,1):2,(5,):2},'full_residual_Schur_expansion')
for mu in parts(5):
 val=sum(c*character(eta,mu) for eta,c in v.items())
 ck(val==(6 if mu in ((3,2),(3,1,1)) else 0),'residual_power_sum_identity')
# Induction with a positive character preserves vanishing on involutions,
# but this gives a virtual character, not a new irreducible source example.
for n in range(5,26):
 for r in range(n//2+1):
  mu=(2,)*r+(1,)*(n-2*r)
  # Every selected invariant five-letter subset of an involution has only 1/2 cycles.
  for j in range(3):
   if 2*j<=5 and j<=r and 5-2*j<=n-2*r:
    sub=(2,)*j+(1,)*(5-2*j)
    ck(sum(c*character(eta,sub) for eta,c in v.items())==0,'induced_virtual_involution_annihilator')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'witness':{'lambda':lam,'fixed_large_cycles':nu,'remaining_size':R,'residual_Schur_coefficients':{str(k):v for k,v in v.items()},'residual_power_sum':'p3*(p1^2+p2)=2*p3*h2'},'scope':'Exact special-fiber annihilator and algebraic reduction, with no frequency estimate for bulk irreducible rows.'},indent=2))
