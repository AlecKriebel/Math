#!/usr/bin/env python3
from collections import Counter
from graph_helpers import graphs,chromatic,core_property,split,union,join
import json
counts=Counter();split_counts=Counter()
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]+=1
for n in range(1,7):
 for a in graphs(n):
  if split(a):
   split_counts[n]+=1;ck('all_small_split_graphs_core_property',core_property(a))
   k=chromatic(a);w=len({x.bit_count() for x in a});d=n-w
   ck('split_source_integer_form',n-1<=(2*k-1)*d)

base=[a for n in range(1,5) for a in graphs(n) if core_property(a)]
for a in base:
 for b in base:
  u=union(a,b);j=join(a,b);ka=chromatic(a);kb=chromatic(b)
  ck('disjoint_union_chromatic_identity',chromatic(u)==max(ka,kb))
  ck('join_chromatic_identity',chromatic(j)==ka+kb)
  ck('disjoint_union_property_closure',core_property(u))
  ck('complete_join_property_closure',core_property(j))
for k in range(2,101):
 ck('split_critical_cut_gap',k*(k+1)//2-(k-1)*(k+2)//2==1)
 for d in range(2,16):ck('split_noncritical_deficit',2*k-1+d<=(2*k-1)*d)
for k1 in range(1,16):
 for k2 in range(1,16):
  for d1 in range(8):
   for d2 in range(8):
    if d1+d2:ck('join_algebra_residual',2*k2*d1+2*k1*d2-2>=0)
print(json.dumps({'problem_id':3242,'author_turn':3,'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'split_graphs_by_order':dict(split_counts),'small_composition_input_graphs':len(base),'scope':'Finite graph-composition, split-partition and arithmetic controls. General structural theorems are proved in TURN_3.md; arbitrary graphs remain outside the result.'},indent=2,sort_keys=True))
