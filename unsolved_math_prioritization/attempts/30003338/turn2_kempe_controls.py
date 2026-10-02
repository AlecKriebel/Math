#!/usr/bin/env python3
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json
n=9;nb=[25,14,22,6];edges=[(a,5+b) for b,mask in enumerate(nb) for a in range(5) if mask>>a&1]
adj=[[] for _ in range(n)]
for a,b in edges:adj[a].append(b);adj[b].append(a)
colorings=[c for c in product(range(3),repeat=n) if all(c[a]!=c[b] for a,b in edges)]
def kempe(c,v,other):
 allowed={0,other};seen={v};todo=[v]
 while todo:
  x=todo.pop()
  for y in adj[x]:
   if y not in seen and c[y] in allowed:seen.add(y);todo.append(y)
 return seen
def force(c,v):
 other=c[v]
 if other==0:return c
 comp=kempe(c,v,other);return tuple((0 if c[x]==other else other) if x in comp else c[x] for x in range(n))
def zeros(c):return frozenset(v for v in range(5) if c[v]==0)
count=0
for v in range(5):
 target=[c for c in colorings if c[v]==0]
 for color in range(3):
  inp=[c for c in colorings if c[v]==color];out=[force(c,v) for c in inp]
  assert sorted(out)==sorted(target);count+=1
  for c,d in zip(inp,out):assert zeros(c)<=zeros(d);count+=1
# Pin v (A index1) to0, then force w (A index2) to0.
S={1};v=2;inp=[c for c in colorings if c[1]==0];target=[c for c in inp if c[v]==0]
push=Counter(force(c,v) for c in inp);hist=Counter()
for c in target:
 r=1+sum(not(kempe(c,v,t)&S) for t in (1,2))
 assert push[c]==r;count+=1;hist[(r,c[0]==0)]+=1
p_u=F(sum(c[0]==0 for c in inp),len(inp));p_w=F(len(target),len(inp));p_uw=F(sum(c[0]==0 for c in target),len(inp))
cov=p_uw-p_u*p_w
assert cov==F(-1,784);count+=1
# Known ordinary positive covariance before conditioning is not a counterexample.
uncond=F(sum(c[0]==c[2]==0 for c in colorings),len(colorings))-F(1,9)
assert uncond>=0;count+=1
# The two-copy component-sorting obstruction on a five-vertex path.
f=(0,2,1,0,2);g=(1,0,2,1,0);valid=[]
for mask in range(32):
 a=tuple(g[i] if mask>>i&1 else f[i] for i in range(5))
 b=tuple(f[i] if mask>>i&1 else g[i] for i in range(5))
 ok=all(a[i]!=a[i+1] and b[i]!=b[i+1] for i in range(4))
 assert ok==(mask in (0,31));count+=1
 if ok:valid.append(mask)
assert valid==[0,31];count+=1
assert {i for i in (0,2,4) if f[i]==0}=={0} and {i for i in (0,2,4) if g[i]==0}=={4};count+=1
print(json.dumps({'status':'PASS','exact_assertions':count,'two_copy_path_valid_swap_masks':valid,'full_colorings':len(colorings),'pinned_v_colorings':len(inp),'pinned_v_w_colorings':len(target),'u_given_v':str(p_u),'w_given_v':str(p_w),'u_w_given_v':str(p_uw),'conditional_cov_u_w_given_v_zero':str(cov),'unconditional_cov_u_w':str(uncond),'u_given_v_w':str(p_uw/p_w),'forced_pushforward_u_mean':str(F(sum(mult*(c[0]==0) for c,mult in push.items()),len(inp))),'multiplicity_histogram':[{'multiplicity':r,'u_zero':z,'colorings':a} for (r,z),a in sorted(hist.items())],'scope':'Verifies an unconditional monotone Kempe coupling and the exact multiplicity bias after a positive pin; conditional failure is not a full-target counterexample.'},indent=2))
