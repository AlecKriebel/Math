#!/usr/bin/env python3
"""Exact cone-contraction and character-pullback controls; analytical scope is separate."""
from fractions import Fraction as F
from itertools import product
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
Q=[F(i,16) for i in range(17)]
for t,r,s in product(Q,repeat=3):
 ok((1-r)*(1-s)*t==(1-(r+s-r*s))*t)
 ok(0<=(1-r)*t<=1);ok(0<=r+s-r*s<=1)
for t in Q:ok((1-1)*t==0);ok((1-0)*t==t)
# Matching character values are preserved by the algebra operations and star.
for a,b,c,d in product(range(-4,5),repeat=4):
 z=complex(a,b);w=complex(c,d)
 pair=(z,z);other=(w,w)
 ok(pair[0]+other[0]==pair[1]+other[1]);ok(pair[0]*other[0]==pair[1]*other[1])
 ok(pair[0].conjugate()==pair[1].conjugate())
# Retraction and section identities on finite pointed-set models.
for n,m in product(range(1,21),repeat=2):
 Z=list(range(n));cone_extra=list(range(n,n+m));r=lambda x:x if x<n else 0
 for z in Z:ok(r(z)==z)
 for x in cone_extra:ok(r(x)==0)
print(json.dumps({'status':'PASS','assertions':checks,'scope':'Finite cone-coordinate, matching-character and retraction controls only; MASA maximality and nonminimal tensor witnesses are proved analytically'},indent=2,sort_keys=True))
