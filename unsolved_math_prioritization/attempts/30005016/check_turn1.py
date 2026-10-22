#!/usr/bin/env python3
"""Finite exact controls; not a proof of infinite-domain assertions."""
from fractions import Fraction as F
from itertools import combinations,permutations
import json
B=[[(0,0),(1,0),(2,0),(3,0)],[(0,0),(1,0),(0,1),(2,0)],[(0,0),(1,0),(0,1),(1,1)],[(0,0),(1,0),(0,1),(0,2)],[(0,0),(0,1),(0,2),(0,3)]]
def det(a):
 a=[[F(v) for v in row] for row in a];z=F(1)
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return F(0)
  if k!=j:a[k],a[j]=a[j],a[k];z=-z
  v=a[j][j];z*=v
  for k in range(j+1,len(a)):
   c=a[k][j]/v
   for l in range(j+1,len(a)):a[k][l]-=c*a[j][l]
 return z
n=0
for pts in combinations([(x,y) for x in range(-2,3) for y in range(-2,3)],4):
 ds=[det([[x**i*y**j for i,j in b] for x,y in pts]) for b in B]
 assert any(ds);n+=1
w=[[(i,0) for i in range(4)],[(0,0),(1,0),(2,0),(0,1)],[(0,0),(0,1),(1,0),(1,1)],[(0,0),(0,1),(0,2),(1,0)],[(0,i) for i in range(4)]]
for k,pts in enumerate(w):
 flags=[bool(det([[x**i*y**j for i,j in b] for x,y in pts])) for b in B]
 assert flags==[j==k for j in range(5)];n+=1
for aa in permutations(range(-3,4),4):
 d=det([[F(a)**i for i in range(4)] for a in aa]);v=F(1)
 for i in range(4):
  for j in range(i+1,4):v*=aa[j]-aa[i]
 assert d==v and d!=0;n+=1
assert 449%2==1 and 449>64*(2+max(5,3));n+=1
print(json.dumps({'assertions':n,'grid_subsets':12650,'exclusive_staircase_witnesses':5,'vandermonde_controls':840,'scope':'Finite exact controls only; Cornelissen theorem and continuous sign obstruction require analytic review.'},sort_keys=True,indent=2))
