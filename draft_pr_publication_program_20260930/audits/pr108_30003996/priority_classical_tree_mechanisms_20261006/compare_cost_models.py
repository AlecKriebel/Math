"""Finite checks of failed classical objective identifications; no hardness search."""
from itertools import combinations
from collections import deque
import json,hashlib,datetime,os
from pathlib import Path
V=range(4); E=list(combinations(V,2))
def adj(edges):
    a={v:[] for v in V}
    for u,v in edges:a[u].append(v);a[v].append(u)
    return a
def reach(a,r):
    seen={r};q=[r]
    for u in q:
        for v in a[u]:
            if v not in seen:seen.add(v);q.append(v)
    return seen
def oriented(a,r):
    seen={r};q=[r];out=[]
    for u in q:
        for v in a[u]:
            if v not in seen:seen.add(v);q.append(v);out.append((u,v))
    return out
def route_cost(edges):
    a=adj(edges);s=0
    for r in V:
        d={r:0};q=[r]
        for u in q:
            for v in a[u]:
                if v not in d:d[v]=d[u]+1;q.append(v)
        s+=sum(d[v] for v in V if v>r)
    return s
C={(r,u,v):(17*r+11*u+5*v)%3 for r in V for u,v in E+[(v,u) for u,v in E]}
checks=0
for edges in combinations(E,3):
    a=adj(edges)
    if len(reach(a,0))!=4:continue
    direct=sum(C[r,u,v] for r in V for u,v in oriented(a,r))
    cuts=0
    for u,v in edges:
        a2=adj([e for e in edges if e!=(u,v)])
        S=reach(a2,u)
        cuts+=sum(C[r,u,v] if r in S else C[r,v,u] for r in V)
    if direct!=cuts:raise RuntimeError('Cut identity mismatch')
    checks+=1
star=[(0,1),(0,2),(0,3)];path=[(0,1),(1,2),(2,3)]
values=[len(S)*(4-len(S)) for S in [{0},{0,2},{0,3},{0,2,3}]]
res={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'trees_checked':checks,'exact_cut_identity_checked':True,'naive_symmetric_unit_cost_map':{'literal_star':12,'literal_path':12,'routing_star':route_cost(star),'routing_path':route_cost(path),'ranking_preserved':False},'fixed_edge_four_cut_routing_loads':values,'routing_mixed_difference':values[3]-values[1]-values[2]+values[0],'any_linear_root_membership_mixed_difference':0,'limitation':'Disproves these direct cost identifications, not all polynomial reductions or global reformulations.'}
# Fixed core 0--1 and 0--2; leaves 3,4 independently choose 1 or 2.
# This is the threshold-forced structural family in JLRK Theorem2.
V=range(5); E=list(combinations(V,2))
C={(r,u,v):(17*r+11*u+5*v)%3 for r in V for u,v in E+[(v,u) for u,v in E]}
directs=[];separables=[];routes=[]
core=[(0,1),(0,2)]; H=[0,1,2]; leaves=[3,4]
core_a={v:[] for v in H}
for u,v in core:core_a[u].append(v);core_a[v].append(u)
constant=sum(C[r,u,v] for r in H for u,v in oriented(core_a,r))
for a3,a4 in [(1,1),(1,2),(2,1),(2,2)]:
    edges=core+[(a3,3),(a4,4)]; a=adj(edges)
    directs.append(sum(C[r,u,v] for r in V for u,v in oriented(a,r)))
    val=constant
    for x,s in [(3,a3),(4,a4)]:
        val+=C[x,x,s]+sum(C[r,s,x] for r in V if r!=x)
        val+=sum(C[x,u,v] for u,v in oriented(core_a,s))
    separables.append(val);routes.append(route_cost(edges))
if directs!=separables:raise RuntimeError('Fixed-core leaf separability mismatch')
mixed=lambda a:a[3]-a[1]-a[2]+a[0]
if mixed(directs)!=0 or mixed(routes)!=-4:raise RuntimeError('Mixed difference mismatch')
res['fixed_core_leaf_comparison']={'core_edges':core,'attachment_pairs':[[1,1],[1,2],[2,1],[2,2]],'literal_costs':directs,'separable_identity_costs':separables,'literal_mixed_difference':mixed(directs),'unit_all_pair_routing_costs':routes,'routing_mixed_difference':mixed(routes),'identity_verified':True}
print(json.dumps(res,indent=2))
