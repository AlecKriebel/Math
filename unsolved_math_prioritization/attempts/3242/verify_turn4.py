#!/usr/bin/env python3
from graph_helpers import graphs,chromatic,core,core_property,induced,join,union
from collections import Counter
import json
counts=Counter();trianglefree=0;deficitone=0
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]+=1
for n in range(2,7):
 for a in graphs(n):
  deg=[x.bit_count() for x in a];w=len(set(deg));d=n-w
  tri=any(a[u]&a[v] for u in range(n) for v in range(u+1,n) if a[u]>>v&1)
  if not tri:trianglefree+=1;ck('triangle_free_core_property',core_property(a))
  if d==1:
   deficitone+=1;k=chromatic(a)
   ck('deficit_one_exact_chromatic',k==(n//2+1 if max(deg)==n-1 else (n+1)//2))
   if n>=3:
    extreme=0 if 0 in deg else n-1
    ck('unique_endpoint',deg.count(extreme)==1)
    v=deg.index(extreme);sm=induced(a,[u for u in range(n) if u!=v])
    ck('endpoint_reduction_variety',len(set(x.bit_count() for x in sm))==n-2)
  h=core(a)
  if h:
   N=len(h);ds=[x.bit_count() for x in h];W=len(set(ds));D=N-W;Delta=max(ds);k=chromatic(h)
   for v in range(N):
    if ds[v]!=Delta:continue
    ng=induced(h,[u for u in range(N) if h[v]>>u&1]);q=chromatic(ng)
    ck('local_neighborhood_bound',N<=(2**(q+1)-1)*D)
    if k>=2**q:ck('local_to_source_criterion',N<=(2*k-1)*D)

U=[2,1];I=[0,0]
for n in range(2,81):
 if n>2:U,I=join([0],I),union([0],U)
 for typ,a in [('U',U),('I',I)]:
  d=[x.bit_count() for x in a]
  ck('recursive_family_order',len(a)==n)
  ck('recursive_family_variety',len(set(d))==n-1)
  # Check the actual degree endpoint and the polynomial target, with chromatic
  # values justified analytically by the universal/isolate recurrence.
  k=n//2+1 if typ=='U' else (n+1)//2
  ck('recursive_family_endpoint',(n-1 in d) if typ=='U' else (0 in d))
  ck('recursive_family_source',n-1<=(2*k-1))
  if n<=10:ck('recursive_family_exact_coloring',chromatic(a)==k)

print(json.dumps({'problem_id':3242,'author_turn':4,'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'triangle_free_labelled_graphs_through_six':trianglefree,'deficit_one_labelled_graphs_through_six':deficitone,'scope':'Exact local-coloring, triangle-free and recursive antiregular controls. The analytic theorems are in TURN_4.md; the general target is not certified.'},indent=2,sort_keys=True))
