#!/usr/bin/env python3
from itertools import product
from math import comb
from fractions import Fraction
import random,json
rng=random.Random(230205502);checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def pmul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def poly(vals):
 a=[1]
 for v in vals:a=pmul(a,[-v,1])
 return a
lattices=0
for _ in range(600):
 d1,d2=rng.randrange(1,7),rng.randrange(1,7)
 u=(rng.randrange(-d2,d2+1),rng.randrange(-d1,d1+1));v=(rng.randrange(-d2,d2+1),rng.randrange(-d1,d1+1))
 D=abs(u[0]*v[1]-u[1]*v[0])
 if not D:continue
 ck(1<=D<=2*d1*d2)
 # Index of the two-generator lattice computed by its finite quotient.
 S={(0,0)};todo=[(0,0)]
 while todo:
  x=todo.pop()
  for w in (u,v):
   y=((x[0]+w[0])%D,(x[1]+w[1])%D)
   if y not in S:S.add(y);todo.append(y)
 ck(D*D//len(S)==D);lattices+=1
monodromy=0
for d1,d2 in product(range(1,8),repeat=2):
 # Independent transitive cycle actions on the two root coordinates.
 S={(0,0)};todo=[(0,0)]
 while todo:
  i,j=todo.pop()
  for y in (((i+1)%d1,j),(i,(j+1)%d2)):
   if y not in S:S.add(y);todo.append(y)
 ck(len(S)==d1*d2);monodromy+=1
symcases=0
for q in range(1,21):
 for _ in range(15):
  vals=[Fraction(rng.randrange(-20,21),rng.randrange(1,11))for _ in range(q)];p=poly(vals);M=max(map(abs,vals));vs=list(vals);rng.shuffle(vs)
  ck(poly(vs)==p)
  for k in range(1,q+1):ck(abs(p[q-k])<=comb(q,k)*M**k)
  # Every component value is a root, even when values repeat.
  for v in set(vals):
   t=Fraction(0)
   for a in reversed(p):t=t*v+a
   ck(t==0)
  symcases+=1
print(json.dumps({'exact_assertions':checks,'lattice_cases':lattices,'product_monodromy_cases':monodromy,'symmetric_component_cases':symcases,'analytic_claims_tested':False},indent=2))
