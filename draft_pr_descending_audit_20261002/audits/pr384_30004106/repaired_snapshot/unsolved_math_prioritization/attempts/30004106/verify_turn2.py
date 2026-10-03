#!/usr/bin/env python3
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import random,json
rng=random.Random(300041062);checks=0
# A polynomial Beurling weight on Z: symmetry and submultiplicativity.
for power in range(1,6):
 for a,b in product(range(-30,31),repeat=2):
  w=lambda n:(1+abs(n))**power
  assert w(a+b)<=w(a)*w(b);checks+=1
  assert w(-a)==w(a);checks+=1
# Exact p-group-type extension of a weighted group basis by P.
# Dimension d(n)=1+q|n| gives integral projective multiplicities.
for q in [2,3,4,5,8,9]:
 d=lambda n:1+q*abs(n)
 def basisprod(i,j):
  mult=(d(i)*d(j)-d(i+j))//q
  assert q*mult==d(i)*d(j)-d(i+j) and mult>=0
  return i+j,mult
 for i,j,k in product(range(-7,8),repeat=3):
  ij,pij=basisprod(i,j);jk,pjk=basisprod(j,k)
  left=basisprod(ij,k)[1]+pij*d(k)
  right=basisprod(i,jk)[1]+pjk*d(i)
  assert left==right;checks+=1
 for _ in range(100):
  xs={n:F(rng.randrange(-5,6),3) for n in range(-8,9)}
  norm=sum(abs(a)*d(n) for n,a in xs.items());D=sum(a*d(n) for n,a in xs.items())
  assert norm<=norm+abs(D)<=2*norm;checks+=1
# Unit-circle Gaussian characters and endotrivial defect rotation.
units=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def conj(z):return(z[0],-z[1])
def sub(z,w):return(z[0]-w[0],z[1]-w[1])
for u in units:
 for _ in range(400):
  z=(F(rng.randrange(-8,9),3),F(rng.randrange(-8,9),5))
  w=(F(rng.randrange(-8,9),7),F(rng.randrange(-8,9),2))
  lhs=sub(mul(conj(u),w),conj(mul(u,z)))
  rhs=mul(conj(u),sub(w,conj(z)))
  assert lhs==rhs;checks+=1
  assert sum(a*a for a in lhs)==sum(a*a for a in sub(w,conj(z)));checks+=1
print(json.dumps({'exact_assertions':checks,'abstract_weighted_basis_controls_only':True,'endotrivial_gamma_one_used_as_credited_input':True,'full_symmetry_claimed':False},indent=2))
