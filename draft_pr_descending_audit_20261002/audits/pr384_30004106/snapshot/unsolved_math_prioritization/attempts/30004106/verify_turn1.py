#!/usr/bin/env python3
"""Exact finite controls for the reductions; not an infinite species test."""
from fractions import Fraction as F
from itertools import product
import json,random
rng=random.Random(300041061);checks=0
# Gaussian rationals as pairs; star-compatible two-element witness criterion.
def add(z,w):return(z[0]+w[0],z[1]+w[1])
def sub(z,w):return(z[0]-w[0],z[1]-w[1])
def conj(z):return(z[0],-z[1])
def I(z):return(-z[1],z[0])
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
vals=[(F(a,3),F(b,4)) for a in range(-6,7) for b in range(-5,6)]
for z in vals:
 for w in vals:
  real1=add(z,w)[1]==0;real2=I(sub(z,w))[1]==0
  assert (real1 and real2)==(w==conj(z));checks+=1
# Finite cyclic ordinary Green-ring characters, inverse duality and products.
units=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
for k in range(4):
 for a,b in product(range(4),repeat=2):
  assert mul(units[(k*a)%4],units[(k*b)%4])==units[(k*(a+b))%4];checks+=1
  assert units[(-k*a)%4]==conj(units[(k*a)%4]);checks+=1
# Actual splitting pattern for F3[C4] -> F9[C4]:
# basis 1,sign,V over F3, with V splitting into the two fourth-root characters.
def ext(v):return [v[0],v[1],v[2],v[2]]
def res(w):return [2*w[0],2*w[1],w[2]+w[3]]
for _ in range(1000):
 v=[rng.randrange(-8,9) for j in range(3)]
 w=[rng.randrange(-8,9) for j in range(4)]
 assert sum(abs(x) for x in ext(v))==abs(v[0])+abs(v[1])+2*abs(v[2]);checks+=1
 assert res(ext(v))==[2*x for x in v];checks+=1
 rw=res(w)
 assert abs(rw[0])+abs(rw[1])+2*abs(rw[2])<=2*sum(abs(x) for x in w);checks+=1
# Tensor multiplication after extension, with character exponents ordered 0,2,1,3.
exp=[0,2,1,3]
def cmul(a,b):
 out=[0]*4
 for i in range(4):
  for j in range(4):out[exp.index((exp[i]+exp[j])%4)]+=a[i]*b[j]
 return out
basis=[[1,0,0],[0,1,0],[0,0,1]]
table={(0,0):[1,0,0],(0,1):[0,1,0],(0,2):[0,0,1],
       (1,1):[1,0,0],(1,2):[0,0,1],(2,2):[2,2,0]}
for i,j in product(range(3),repeat=2):
 assert cmul(ext(basis[i]),ext(basis[j]))==ext(table[tuple(sorted((i,j)))]);checks+=1
# Laurent convolution under the deliberately nonstandard involution.
def conv(a,b):
 out={}
 for i,z in a.items():
  for j,w in b.items():out[i+j]=add(out.get(i+j,(F(0),F(0))),mul(z,w))
 return {i:z for i,z in out.items() if z!=(0,0)}
x={0:(F(1),F(0)),1:(F(0),F(1))}
xs={n:conj(z) for n,z in x.items()}
assert conv(xs,x)=={0:(F(1),F(0)),2:(F(1),F(0))};checks+=1
# Values at u=-i attain |1+i u|=2; values at u=1 attain |1+u²|=2.
assert add((1,0),mul((0,1),(0,-1)))==(2,0);checks+=1
assert add((1,0),mul((1,0),(1,0)))==(2,0);checks+=1
print(json.dumps({'exact_assertions':checks,'gaussian_witness_pairs':len(vals)**2,'infinite_character_compactness_tested':False,'actual_group_counterexample_found':False},indent=2))
