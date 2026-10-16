#!/usr/bin/env python3
"""Independent exact checks via adjunction and polarized intersection products.
Finite algebra checks only; no complex surface is constructed or classified.
"""
from fractions import Fraction as F
from collections import Counter
from itertools import permutations,product
import json
checks=Counter()
combinations_pairs=[(0,1),(0,2),(1,2)]
def test(x,label):
 assert x,label
 checks[label]+=1
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def scaled(c,x):return tuple(c*a for a in x)
def intersect(x,y,z):
 # Independent multilinear evaluation, as a permanent, on a product of curves.
 return sum(x[i]*y[j]*z[k] for i,j,k in permutations(range(3)))
def basis(i,c=1):return tuple(c*int(i==j) for j in range(3))

# Adjunction: c2(TS)=c2(TY)-c1(TY)D+D^2 on S;
# c1(TY)=-sum K_i and K_S=D+sum K_i.
for coefficients in product((1,2,5),repeat=3):
 D=tuple(map(F,coefficients))
 for genera in product((2,3,6),repeat=3):
  K=[basis(i,2*genera[i]-2) for i in range(3)]
  Ksum=tuple(sum(x) for x in zip(*K))
  c2S=sum(intersect(D,K[i],K[j]) for i,j in combinations_pairs)
  c2S+=intersect(D,D,Ksum)+intersect(D,D,D)
  for i in range(3):
   j,k=[x for x in range(3) if x!=i]
   difference=c2S-intersect(D,K[i],plus(D,Ksum))
   direct=intersect(D,plus(D,K[j]),plus(D,K[k]))
   test(difference==direct,'adjunction_equals_vertical_top_chern')
   a,b,c=coefficients[i],coefficients[j],coefficients[k]
   u,v=2*genera[j]-2,2*genera[k]-2
   test(direct==a*(6*b*c+2*c*u+2*b*v+u*v),'exact_mixed_intersection_expansion')
   test(direct>0,'ample_product_class_positive')
# Canonical-sign controls, and a genuine nonample boundary case.
D=(F(1),F(1),F(1))
K=[basis(i,2) for i in range(3)]
test(intersect(D,plus(D,K[1]),plus(D,K[2]))==18,'displayed_value')
Kbad=[basis(0,2),basis(1,4),basis(2,2)]
wrong=intersect(D,plus(D,scaled(-1,Kbad[1])),plus(D,Kbad[2]))
correct=intersect(D,plus(D,Kbad[1]),plus(D,Kbad[2]))
test(wrong==-6 and correct==26,'cotangent_sign_negative_control')
D=basis(0)
test(intersect(D,plus(D,K[0]),plus(D,K[2]))==0,'nonample_projection_not_excluded')
test(intersect(D,plus(D,K[1]),plus(D,K[2]))==4,'constant_other_projection_obstructed')
# On a hyperbolic target, the pullback tangent line degree is strictly negative.
for g,d in product(range(2,10),range(1,8)):
 test(d*(2-2*g)<0,'negative_tangent_pullback_degree')
# Numerical conditions: H1 lower/upper intervals and genus bounds are equivalent.
for b in product((2,3,5),repeat=3):
 for g in [(4,4,4),(7,8,9),(12,11,10),(3,8,6)]:
  lo=2*sum(b);up=[2*(b[i]+g[i]) for i in range(3)]
  test((lo<=min(up))==all(g[i]>=sum(b)-b[i] for i in range(3)),
       'betti_genus_inequality_equivalence')
b=(2,2,2);g=(4,4,4)
test([4*(b[i]-1)*(g[i]-1) for i in range(3)]==[12,12,12],'euler_tuple')
test(2*sum(b)==min(2*(b[i]+g[i]) for i in range(3))==12,'betti_tuple')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
                  'checks_by_category':dict(sorted(checks.items())),
                  'method':'Independent adjunction computation and multilinear permanent evaluation; exact rational arithmetic.',
                  'limitation':'Algebraic consistency and necessary conditions only; no surface existence, ampleness classification, or nonnormal extension is certified.'},indent=2,sort_keys=True))
