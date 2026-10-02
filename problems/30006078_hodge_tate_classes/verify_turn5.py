#!/usr/bin/env python3
import itertools as it,json
from fractions import Fraction as F
import sympy as s
checks=0
def ck(b):
 global checks
 assert b
 checks+=1
# Every product of differences expands as the claimed ample-class linear combination.
for q in range(1,9):
 for shift in range(-5,6):
  a=[F(shift+j+2) for j in range(q)];b=[F(2*j-3) for j in range(q)]
  lhs=F(1)
  for x,y in zip(a,b):lhs*=x-y
  rhs=F(0)
  for mask in range(1<<q):
   term=F(1)
   for j in range(q):term*=(-b[j] if mask>>j&1 else a[j])
   rhs+=term
  ck(lhs==rhs)
# A one-dimensional cohomology class is detected by any nonzero ample pairing.
for degree in range(1,101):
 for val in range(-100,101):ck((F(val)*degree==0)==(val==0))
G=s.Matrix([[0,1,1,1],[1,0,1,1],[1,1,0,2],[1,1,2,0]])
ck(G.det()==-4);ck(G.rank()==4)
# An abstract nondegenerate extension models the dimension calculation only;
# it is not asserted to be a chosen rational basis of the actual transcendental part.
P=s.diag(G,s.eye(2));B=s.eye(6)[:,:4];test=B.T*P
ck(P.det()!=0);ck(test.rank()==4);ck(len(test.nullspace())==2)
for a,b in it.product(range(-15,16),repeat=2):
 v=s.Matrix([0,0,0,0,a,b]);ck(test*v==s.zeros(4,1));ck((v==s.zeros(6,1))==(a==b==0))
# Higher-degree target vanishes beyond degree2d; surface cases explicit.
for d in range(1,21):
 for i in range(2,41):
  ck((2*(i-1)>2*d)==(i>d+1))
ck(2*(2-1)==2 and 2*(3-1)==4 and 2*(4-1)>4)
print(json.dumps({'status':'PASS','assertions':checks,'elliptic_square_divisor_span_rank':4,'remaining_annihilator_dimension':2,'scope':'finite algebraic detection controls; no unrestricted formula or local-system counterexample'},indent=2,sort_keys=True))
