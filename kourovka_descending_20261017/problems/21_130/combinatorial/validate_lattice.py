#!/usr/bin/env python3
"""Independent minors/order checks for the relation-lattice implementation."""
import random,itertools,math,json
from fractions import Fraction
from pathlib import Path
from universal_small import canonical,contains,row_hnf

def rank(A,d):
 A=[[Fraction(x) for x in r] for r in A];k=0
 for j in range(d):
  q=next((i for i in range(k,len(A)) if A[i][j]),None)
  if q is None:continue
  A[q],A[k]=A[k],A[q];z=A[k][j];A[k]=[x/z for x in A[k]]
  for i in range(k+1,len(A)):
   z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[k])]
  k+=1
  if k==len(A):break
 return k

def det(A):
 if not A:return 1
 return sum((-1)**j*A[0][j]*det([r[:j]+r[j+1:] for r in A[1:]]) for j in range(len(A)))

def delta(A,r,d):
 if not r:return 1
 g=0
 for I in itertools.combinations(range(len(A)),r):
  for J in itertools.combinations(range(d),r):
   g=math.gcd(g,abs(det([[A[i][j] for j in J] for i in I])))
   if g==1:return 1
 return g

def independent_contains(A,v,d):
 r=rank(A,d)
 if rank(A+[v],d)!=r:return False
 order=delta(A,r,d)//delta(A+[v],r,d)
 return order&(order-1)==0

random.seed(21130);checks=0
for d in range(1,7):
 for trial in range(30):
  A=[[random.randrange(-2,3) for _ in range(d)] for _ in range(random.randrange(1,d+2))]
  H=canonical(A,d)
  assert canonical(H,d)==H
  for _ in range(15):
   v=[random.randrange(-2,3) for _ in range(d)]
   got=contains(H,v);expected=independent_contains(A,v,d)
   assert got==expected,(A,H,v,got,expected)
   checks+=1
  # Multiplying relations by powers of 2 does not change the saturated lattice.
  A2=[]
  for row in A:
   factor=2**random.randrange(1,4);A2.append([x*factor for x in row])
  assert canonical(A2,d)==H
  # Relation generating-set changes preserve the lattice.
  A3=[row[:] for row in A]
  for _ in range(10):
   if len(A3)>1:
    i,j=random.sample(range(len(A3)),2);z=random.randrange(-3,4)
    A3[i]=[x+z*y for x,y in zip(A3[i],A3[j])]
  assert canonical(A3,d)==H
result={'minors_membership_checks':checks,'dimensions':list(range(1,7)),'all_passed':True,'independent_mechanism':'rational rank plus determinantal divisors; element order is delta(L)/delta(L+Zv), accepted iff a power of 2'}
Path('validate_lattice_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
