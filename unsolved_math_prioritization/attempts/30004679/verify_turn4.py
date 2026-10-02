#!/usr/bin/env python3
"""Finite controls for variable lookahead, sparse avoidance and fusion bookkeeping."""
from itertools import combinations
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1

def member(f):return f[f[0]+1]==f[f[0]]+1
for m in range(1,101):
 n=m+3;negative=[n+2*i for i in range(n+5)];positive=negative[:]
 positive[n+1]=positive[n]+1
 ok(positive[:m]==negative[:m]);ok(member(positive));ok(not member(negative))
 ok(all(a<b for a,b in zip(positive,positive[1:])))
 ok(n+2>m)
# Every sampled sparse sequence and its sufficiently long subsequences avoid (10).
for n in range(5):
 f=tuple(2*i+n for i in range(25))
 for inds in combinations(range(12),7):
  g=tuple(f[i] for i in inds)
  if g[0]+1<len(g):ok(not member(g))
# Finite version of nested homogeneous reservoirs with varying finite arities.
for seed in range(31):
 R=list(range(1,151));X=[];reservoirs=[];colors=[];levels=[1]
 for s in range(12):
  x=R[0];X.append(x);r=(x+seed)%5
  R=[y for y in R if y>x]
  if r:R=[y for y in R if y%2==0]
  reservoirs.append(tuple(R));colors.append(x%2);levels.append(levels[-1]+2*r)
 for s,x in enumerate(X):
  ok(set(X[s+1:])<=set(reservoirs[s]));ok(levels[s+1]>=levels[s])
  r=(x+seed)%5
  for t in list(combinations(X[s+1:],r))[:100]:
   if r:ok((sum(t)+x)%2==colors[s])
 H=[x for x,a in zip(X,colors) if a==0]
 for i,x in enumerate(H):
  r=(x+seed)%5
  for t in list(combinations(H[i+1:],r))[:100]:ok((sum(t)+x)%2==0)
print(json.dumps(dict(status='PASS',assertions=checks,unbounded_arity_examples=100,finite_fusion_runs=31,scope='finite geometry-free controls; no finite test certifies the hyperarithmetical basis theorem'),sort_keys=True,indent=2))
