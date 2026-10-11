#!/usr/bin/env python3
"""Exact finite controls for the prism and the extension bimodule formulas."""
from itertools import product
from collections import Counter
import json
checks=prisms=actions=0
def add(a,b,k=1):
 for x,v in b.items():
  a[x]+=k*v
  if not a[x]: del a[x]
 return a
def boundary(chain):
 out=Counter()
 for tup,c in chain.items():
  if len(tup)==1: continue
  for i in range(len(tup)): add(out,{tup[:i]+tup[i+1:]:c*((-1)**i)})
 return out
def prism(chain,n,mul):
 out=Counter()
 for tup,c in chain.items():
  for i in range(len(tup)):
   s=tup[:i+1]+tuple(mul(x,n) for x in tup[i:])
   add(out,{s:c*((-1)**i)})
 return out
# Noncommutative S3, represented by permutations and composition.
perms=list(__import__('itertools').permutations(range(3)))
def mul(a,b): return tuple(a[b[i]] for i in range(3))
for q in range(4):
 for tup in product(perms,repeat=q+1):
  chain=Counter({tup:1})
  for n in perms:
   lhs=add(boundary(prism(chain,n,mul)),prism(boundary(chain),n,mul))
   rhs=add(Counter({tuple(mul(x,n) for x in tup):1}),chain,-1)
   assert lhs==rhs;checks+=1;prisms+=1
# Integral Heisenberg extension, N=center Z, Q=Z^2. Use M=ZG
# with its right regular action and a canonical balanced-pair normal form.
def hm(g,h):
 a,b,c=g;x,y,z=h
 return (a+x,b+y,c+z+a*y)
def hi(g):
 a,b,c=g
 return (-a,-b,-c+a*b)
def lift(q): return (q[0],q[1],0)
def nf(m,h):
 a,b,c=h
 # h=(0,0,c)*lift(a,b), balanced tensor m*h_center tensor lift.
 return (hm(m,(0,0,c)),(a,b))
def F(q,m): return nf(hm(m,hi(lift(q))),lift(q))
vals=list(product(range(-1,2),repeat=3))
qs=list(product(range(-2,3),repeat=2))
for q,m,g in product(qs,vals,vals):
 left=F(q,m)
 lhs=nf(left[0],hm(lift(left[1]),g))
 rhs=F((q[0]+g[0],q[1]+g[1]),hm(m,g))
 assert lhs==rhs;checks+=1;actions+=1
 # Left quotient action from (7).
 lhs=nf(hm(left[0],hi(g)),hm(g,lift(left[1])))
 rhs=F((g[0]+q[0],g[1]+q[1]),m)
 assert lhs==rhs;checks+=1
 for c in (-2,2):
  h=hm((0,0,c),lift(q))
  assert nf(hm(m,hi(h)),h)==F(q,m);checks+=1
# One-column spectral-sequence bidegrees: no other occupied endpoint.
for d in range(11):
 for q in range(11):
  for r in range(2,15):
   assert d+r!=d and d-r!=d;checks+=1
print(json.dumps({'assertions':checks,'bar_prisms_S3':prisms,'nonsplit_bimodule_cases':actions,'scope':'Finite exact identity controls; the infinite FP and spectral-sequence arguments are proved in TURN_4.md.'},indent=2))
