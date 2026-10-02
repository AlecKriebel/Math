#!/usr/bin/env python3
"""Finite controls for the feedback/menu distinction; no infinite reduction tested by sampling."""
from itertools import product,combinations
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1

def belongs(x,a,b):return a%2==0 and b==a+1 and a//2<len(x) and x[a//2]==1
patterns=list(product((0,1),repeat=6))
for x in patterns:
 for a,b,c in combinations(range(16),3):ok(not belongs(x,a,c))
 for i,j in combinations(range(10),2):ok(not belongs(x,2*i,2*j))
for x,y in combinations(patterns,2):
 i=next(i for i in range(6) if x[i]!=y[i]);ok(belongs(x,2*i,2*i+1)!=belongs(y,2*i,2*i+1))
# Index feedback can be driven by earlier answer prefixes, while every tail is preavailable.
for seed in range(81):
 h=lambda n:3*n+seed+1
 history=[];idx=seed%29
 for step in range(43):
  answer=tuple(h(idx+j) for j in range(8));ok(all(z!=idx for z in answer))
  history.append((idx,answer));idx=(sum(answer[:3])+step+seed)%57
 for idx,answer in history:ok(answer==tuple(h(idx+j) for j in range(8)))
# Prefix information decides finitely many P_x cylinders, not the full member of the family.
for n in range(6):
 x=(0,)*6;y=(0,)*n+(1,)+(0,)*(5-n)
 ok(x[:n]==y[:n]);ok(belongs(x,2*n,2*n+1)!=belongs(y,2*n,2*n+1))
print(json.dumps(dict(status='PASS',assertions=checks,finite_binary_parameters=len(patterns),indexed_protocols=81,scope='finite checks of distinct clopen instances, common avoidance and tail-index simulation'),sort_keys=True,indent=2))
