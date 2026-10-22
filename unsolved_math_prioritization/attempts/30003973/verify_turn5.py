#!/usr/bin/env python3
"""Exact labeled-graph verification; no imports from author search scripts."""
from pathlib import Path
import itertools,json
C=json.loads((Path(__file__).parent/'TURN_5_CERTIFICATE.json').read_text());counts={}
def ck(x,k):
    assert x,k
    counts[k]=counts.get(k,0)+1

def capacities(edges):
    adj={}
    for a,b in edges:adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
    remain=set(adj);out=[]
    while remain:
        todo=[min(remain)];V=set()
        while todo:
            v=todo.pop()
            if v in V:continue
            V.add(v);todo.extend(adj[v]-V)
        remain-=V;ec=sum(len(adj[v]) for v in V)//2
        if len(V)==3 and ec==3:
            ck(all(len(adj[v])==2 for v in V),'component_triangle');out.append(2)
        else:
            ck(len(V)==ec+1 and max(len(adj[v]) for v in V)==ec,'component_star');out.append(ec)
    return sorted(out,reverse=True)

def contains(caps,target):return len(caps)>=len(target) and all(a>=b for a,b in zip(caps,target))
def colored_caps(edges,colors):return [capacities([e for e,c in zip(edges,colors) if c==i]) for i in [0,1]]

E=C['edges'];H=C['target_H_star_sizes'];J=C['target_Hprime_star_sizes']
ck(C['vertices']==53 and len(E)==45,'graph_order_size')
ck(len({tuple(sorted(e)) for e in E})==45 and all(a!=b for a,b in E),'simple_graph')
ck(set(sum(E,[]))==set(range(53)),'no_isolated_vertices')
ck((sum(H),sum(k+1 for k in H),sum(J),sum(k+1 for k in J))==(14,19,15,20),'target_orders_sizes')
orig=capacities(E);ck(orig==[9,8,7,6,5,4,2,2,1],'original_component_capacities')
# Reconstruct the full source of the positive Ramsey certificate independently.
star_sizes=[9,8,7,6,5,4,2,1];z=1;tau={t:sum(k>=t for k in H) for t in set(H)}
rows=[]
for u,v in itertools.combinations_with_replacement(sorted(tau),2):
    forced=sum(d>=u+v-1 for d in star_sizes)+z*(u<=2 and v<=2);required=tau[u]+tau[v]-1
    rows.append({'u':u,'v':v,'forced':forced,'required':required})
    ck(forced==required,'positive_all_thresholds_tight')
ck(rows==C['H_threshold_table'],'threshold_certificate_table')
colors=C['Hprime_avoiding_colors'];ck(len(colors)==45 and set(colors)<={0,1},'Hprime_coloring_valid')
for cc in colored_caps(E,colors):ck(not contains(cc,J),'Hprime_absent_in_witness_color')
ck({r['deleted_edge_index'] for r in C['H_edge_deletion_avoiding_colorings']}==set(range(45)),'all_deletions_present')
for rec in C['H_edge_deletion_avoiding_colorings']:
    i=rec['deleted_edge_index'];F=E[:i]+E[i+1:];co=rec['colors']
    ck(len(co)==44 and set(co)<={0,1},'deletion_coloring_valid')
    for cc in colored_caps(F,co):ck(not contains(cc,H),'H_absent_after_deletion')

# Compare exact color enumeration against the extended theorem on small hosts.
def partitions(n,cap=None):
    if not n:yield ();return
    if cap is None:cap=n
    for i in range(min(n,cap),0,-1):
        for p in partitions(n-i,i):yield(i,)+p

def make_graph(stars,z):
    ee=[];v=0
    for d in stars:
        ee.extend((v,j) for j in range(v+1,v+d+1));v+=d+1
    for _ in range(z):ee.extend(itertools.combinations(range(v,v+3),2));v+=3
    return ee

def criterion(stars,z,k):
    tt=sorted(set(k));tau={t:sum(a>=t for a in k) for t in tt}
    return all(sum(d>=u+v-1 for d in stars)+z*(u<=2 and v<=2)>=tau[u]+tau[v]-1 for u in tt for v in tt)
small_hosts=[(s,z) for n in range(6) for s in partitions(n) for z in range(3) if n+3*z<=9]
small_targets=[p for n in range(1,6) for p in partitions(n)]
num_colorings=0
for stars,z in small_hosts:
    F=make_graph(stars,z);allcaps=[]
    for mask in range(1<<len(F)):
        cs=[(mask>>i)&1 for i in range(len(F))];allcaps.append(colored_caps(F,cs));num_colorings+=1
    for k in small_targets:
        direct=all(any(contains(cc,k) for cc in pair) for pair in allcaps)
        ck(direct==criterion(stars,z,k),'small_direct_vs_extended_criterion')

# All-q proof uses the elementary sumset identity, checked here throughq20.
def conv(a,b):return tuple(max(a[i]+b[j-i] for i in range(max(0,j-len(b)+1),min(len(a)-1,j)+1)) for j in range(len(a)+len(b)-1))
a=tuple(k-1 for k in H);b=tuple(k-1 for k in J);ca=cb=(0,);sums={0}
for q in range(1,21):
    ca=conv(ca,a);cb=conv(cb,b);sums={x+y for x in sums for y in [0,1,3,4]}
    if q>=2:
        ck(sums==set(range(4*q+1)),'sumset_interval_control')
        ck(ca==cb==tuple(range(4*q,-1,-1)),'all_q_profile_control_bounded')
print(json.dumps({'problem_id':30003973,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'separator_vertices':53,'separator_edges':45,'edge_deletion_colorings':45,'small_host_profiles':len(small_hosts),'small_target_profiles':len(small_targets),'small_edge_colorings':num_colorings,'small_host_edges_max':9,'scope':'Exact positive threshold certificate, explicit negative coloring, and every edge-deletion witness. The targets are already2-nonequivalent; no counterexample to the original2-to3 implication is claimed.'},indent=2,sort_keys=True))
