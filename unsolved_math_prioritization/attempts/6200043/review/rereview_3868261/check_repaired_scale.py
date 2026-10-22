"""Exact checks of the repaired porosity constants; geometry still needs prose proof."""
from fractions import Fraction as F
from itertools import product
import json
count=0;small_cases=0;large_cases=0;branches=set()
for A,D,rho,c0,N in product((F(1,10),F(1),F(5)),(F(1,4),F(1),F(10)),(F(1,3),F(2,3),F(3,4)),(F(1,100),F(1),F(100)),range(1,7)):
 r0=min(A,D);K=c0*rho**(N+1)/(2*A);c=min(F(1,4),K/2)
 branches.add('cap' if c==F(1,4) else 'geometric')
 for q in (F(1),F(1,2),F(1,10),F(1,1000)):
  r=r0*q;k=0
  while A*rho**k>r/2:k+=1
  assert k>=1
  assert A*rho**k<=r/2<A*rho**(k-1)
  assert rho**k>rho*r/(2*A)
  for ell in range(1,N+1):
   R=c0*rho**(k+ell)
   assert R>K*r and K*r>=2*c*r
   count+=2
  count+=3;small_cases+=1
 cp=min(c,c*r0/(2*D))
 for r in (r0,(r0+D)/2,D):
  assert cp>0 and cp<=c
  assert c*r0/2>=cp*r
  count+=2;large_cases+=1
assert branches=={'cap','geometric'}
print(json.dumps({'status':'pass','assertions':count,'small_scale_cases':small_cases,'large_scale_cases':large_cases,'constant_branches':sorted(branches),'scope':'Exact repaired-constant arithmetic only; does not check metric balls or prove the conjecture.'},sort_keys=True))
