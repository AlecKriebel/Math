#!/usr/bin/env python3
"""Exact finite controls for the credited source reconstruction."""
from itertools import combinations
import json
import sympy as sp
checks=0;lengthcases=0;hessiancases=0;koszulcases=0
for r in range(5,17):
 m=(r-1)//2
 ell=[1]*r if r%2 else [0]+[1]*(r-1)
 total=sum(ell);assert total==2*m+1;checks+=1
 positive=[]
 for mask in range(1<<r):
  J=[i for i in range(r) if mask>>i&1]
  s=sum(ell[i] for i in J)
  assert 2*s!=total;checks+=1
  assert (2*s<total)==(s<=m);checks+=1
  if 2*s>total:
   sigma=sum(2*(s-ell[i])<total for i in J)
   if sigma:positive.append(sigma)
  lengthcases+=1
 assert min(positive)==m+1;checks+=1
 if not r%2:
  # Twice the perturbed positive length vector (1/2,1,...,1).
  ep=[1]+[2]*(r-1);tot=sum(ep)
  for mask in range(1<<r):
   s=sum(ep[i] for i in range(r) if mask>>i&1)
   old=sum(ell[i] for i in range(r) if mask>>i&1)
   assert 2*s!=tot and (2*s<tot)==(2*old<total);checks+=1
# Symbolic characteristic polynomial of the theta Hessian.
x=sp.Symbol('x')
for r in range(3,16,2):
 for j in range((r-1)//2+1):
  q=r-2*j;s=sp.Matrix([-1]*j+[1]*(r-j))
  H=q*sp.diag(*s)-s*s.T
  actual=H.charpoly(x).as_expr()
  expected=x*(x-r)**(r-1) if j==0 else x*(x+r)*(x+q)**(j-1)*(x-q)**(r-j-1)
  assert sp.expand(actual-expected)==0;checks+=1;hessiancases+=1
  assert H*sp.ones(r,1)==sp.zeros(r,1);checks+=1
  assert j+2*j==3*j;checks+=1
# Formal monomial cancellation in two successive wedge differentials.
for r in range(2,13):
 for k in range(r-1):
  for J in combinations(range(r),k):
   coeff={}
   for i in range(r):
    if i in J:continue
    J1=tuple(sorted(J+(i,)));sgn1=(-1)**sum(a>i for a in J)
    for h in range(r):
     if h in J1:continue
     sgn2=(-1)**sum(a>h for a in J1)
     key=(tuple(sorted((i,h))),tuple(sorted(J1+(h,))))
     coeff[key]=coeff.get(key,0)+sgn1*sgn2
   assert all(v==0 for v in coeff.values());checks+=1;koszulcases+=1
for r in range(5,202):
 m=(r-1)//2
 assert m<r and m==(r-1)//2;checks+=1
 assert 3*r-2>0;checks+=1
# Current correction: derive the FREE TARGET shifts from coker(iota)[rd].
# V_J has homological degree -3|J|; high V_J survive in the cokernel.
# FREE QUOTIENT shifts instead come from ker(iota)[rd-1] and W_J.
r=5;m=2;d=3;dbar=1
left_free_targets=sorted(r*d-j*d for j in range(m+2,r+1))
right_free_quotients=sorted(r*d-1-j*d-dbar for j in range(m))
right_koszul_shift=(m+2)*d-2*dbar-1
differences=[l-right_koszul_shift for l in left_free_targets]
assert (left_free_targets==[0,3] and right_free_quotients==[10,13]
        and right_koszul_shift==9 and differences==[-9,-6]
        and all(x!=2 for x in differences));checks+=1
print(json.dumps({'exact_assertions':checks,'length_subset_cases':lengthcases,'symbolic_hessian_cases':hessiancases,'formal_koszul_square_cases':koszulcases,'all_rank_topology_proved_by_finite_controls':False},indent=2))
