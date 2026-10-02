#!/usr/bin/env python3
"""Modest exact graph/rounding controls for TURN_1.md; analytic proof is separate."""
from fractions import Fraction as Q
from collections import Counter
import json

counts=Counter();sizes=Counter();chromatics=Counter()
def ck(group,test):
 if not test:raise AssertionError(group)
 counts[group]+=1

def color(adj):
 n=len(adj);order=sorted(range(n),key=lambda v:adj[v].bit_count(),reverse=True)
 for k in range(1,n+1):
  classes=[0]*k;assignment=[-1]*n
  def rec(i,used):
   if i==n:return True
   v=order[i]
   for col in range(min(used+1,k)):
    if adj[v]&classes[col]:continue
    classes[col]|=1<<v;assignment[v]=col
    if rec(i+1,max(used,col+1)):return True
    classes[col]^=1<<v
   return False
  if rec(0,0):return k,assignment

for n in range(2,7):
 edges=[(u,v) for u in range(n) for v in range(u+1,n)]
 for mask in range(1<<len(edges)):
  adj=[0]*n
  for bit,(u,v) in enumerate(edges):
   if mask>>bit&1:adj[u]|=1<<v;adj[v]|=1<<u
  deg=[a.bit_count() for a in adj];w=len(set(deg));d=n-w;k,assignment=color(adj)
  sizes[n]+=1;chromatics[k]+=1
  ck('simple_degree_deficit_positive',d>=1)
  ck('proper_coloring_certificate',all(assignment[u]!=assignment[v] for u,v in edges if adj[u]>>v&1))
  ck('universal_capacity_bound',n-1<=(2**k-1)*d)
  if 0 not in deg:ck('no_isolate_stronger_bound',n<=(2**k-1)*d)
  if k<=2:ck('complete_bipartite_subcase',n-1<=(2*k-1)*d)
  # This last check is finite evidence only, not a proof beyond order six.
  ck('finite_full_conjecture_control',n-1<=(2*k-1)*d)
  if 0 not in deg:
   cls=sorted(Counter(assignment).values());prefix=0
   for a in cls:
    ck('individual_color_capacity',a<=prefix+d);prefix+=a

for n in range(2,36):
 for w in range(1,n):
  d=n-w;num=w//2;ceiling=(num+d-1)//d
  for k in range(1,n+1):
   ck('rounding_equivalence',(k>ceiling)==(n-1<=(2*k-1)*d))

for d in range(1,31):
 for m in range(2,10):
  vals=[2**i*d for i in range(m)];prefix=0
  for a in vals:ck('capacity_relaxation_equality',a==prefix+d);prefix+=a
  ck('capacity_relaxation_sum',prefix==(2**m-1)*d)
 for d0 in [d]:
  sets=[list(range(5*d0+1,6*d0+1)),list(range(3*d0+1,5*d0+1)),list(range(1,3*d0+1))+[3*d0]*d0]
  ck('formal_non_graph_variety',len(set(sum(sets,[])))==6*d0)
  ck('formal_non_graph_order',sum(map(len,sets))==7*d0)
  ck('formal_non_graph_capacity',all(max(s)<=7*d0-len(s) for s in sets))
  ck('formal_non_graph_violates_target',7*d0-1>5*d0)
ck('d_one_cut_balance_countercontrol',(4-1)+(5-1)!=sum(t-1 for t in [1,2,3,3]))

print(json.dumps({'problem_id':3242,'author_turn':1,'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'labelled_graphs_by_order':dict(sorted(sizes.items())),'total_graphs':sum(sizes.values()),'chromatic_distribution':dict(sorted(chromatics.items())),'scope':'Exact full enumeration only through order six, rounding and formal relaxation controls. The general bound and full bipartite case are proved in TURN_1.md; no full general solution is certified.'},indent=2,sort_keys=True))
