"""Exact scope/arithmetic controls, not a proof of connected-component classification."""
from fractions import Fraction
from itertools import permutations
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
rows=[]
for sig in [(-1,9),(-1,3,6),(-1,3,3,3),(12,)]:
 g=1+sum(sig)//4;positive=tuple(x for x in sig if x>0);third=tuple(x//3 for x in positive)
 check(sum(sig)==4*g-4);check(all(x%3==0 for x in positive));check(sum(third)==g)
 check(all(x>=-1 and x!=0 for x in sig));check(g in (3,4))
 for perm in set(permutations(sig)):
  check(sorted(x//3 for x in perm if x>0)==sorted(third))
 if -1 in sig:check(Fraction(-1,3).denominator!=1)
 # The published invariant has values1 and2; arithmetic labels only.
 check({h%2 for h in [1,2]}=={0,1})
 rows.append(dict(signature=sig,genus=g,zero_divisor_third_coefficients=third,degree=sum(third),credited_values=[1,2]))
# Hirzebruch surface convention: e^2=-r, e.f=1, f^2=0.
def inter(r,A,B):return -r*A[0]*B[0]+A[0]*B[1]+A[1]*B[0]
def h0(r,a,b):return sum(max(0,b-i*r+1) for i in range(a+1))
for r in range(1,7):
 for a in range(4):
  for b in range(10):
   check(h0(r,a,b)>=0)
   if a==0:check(h0(r,a,b)==b+1)
check(h0(4,1,3)==4);check(h0(4,1,4)==6);check(h0(5,1,4)==5);check(h0(5,1,5)==7)
check(h0(2,1,2)==4);check(h0(2,1,2)!=2)
check(h0(2,2,4)-1==8);check(h0(2,3,6)==16)
r=2;X=(3,6);R=(2,4);K=(-2,-4)
check(inter(r,X,(1,0))==0)
check((inter(r,R,R)+inter(r,R,K))//2+1==1)
check((inter(r,X,X)+inter(r,X,K))//2+1==4)
check(inter(r,X,(0,4))==12);check(inter(r,X,(0,6))==18)
for zeros in range(1,6):
 check(8+zeros+2-7==zeros+3)
 check(8+zeros+4-7==zeros+5)
print(json.dumps(dict(assertions=checks,scope_rows=rows,appendix_B5={'printed_h0':2,'section_formula_h0':4,'printed_dimension':'n+3','dimension_if_only_h0_is_corrected':'n+5','required_stratum_dimension':'n+5','status':'unresolved verification issue; no repair or theorem disproof asserted'},scope='Finite source-alignment and arithmetic checks only; credited published component theorem is not independently recertified.'),indent=2,sort_keys=True))
