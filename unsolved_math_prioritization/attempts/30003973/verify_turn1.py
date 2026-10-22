#!/usr/bin/env python3
"""Exact bounded graph checks; finite agreement is not Ramsey equivalence."""
from itertools import combinations,permutations
import json

counts={}
def ck(x,k):
    assert x,k
    counts[k]=counts.get(k,0)+1

def edges(n):return list(combinations(range(n),2))

# Explicit core graphs, all without isolated vertices. Empty targets are separate.
cores=[('K2',2,[(0,1)]),('P3',3,[(0,1),(1,2)]),('K3',3,[(0,1),(0,2),(1,2)]),('2K2',4,[(0,1),(2,3)]),('P4',4,[(0,1),(1,2),(2,3)]),('C4',4,[(0,1),(1,2),(2,3),(0,3)]),('K1_3',4,[(0,1),(0,2),(0,3)]),('P3_plus_K2',5,[(0,1),(1,2),(3,4)])]


def occurrence_masks(n,v,ee):
    if n<v:return []
    ix={e:i for i,e in enumerate(edges(n))};out=set()
    for a in permutations(range(n),v):
        out.add(sum(1<<ix[tuple(sorted((a[i],a[j])))] for i,j in ee))
    return sorted(out)

def ramsey_table(n,v,ee,qmax=4):
    m=n*(n-1)//2;size=1<<m
    pats=occurrence_masks(n,v,ee)
    free=[not any(M&p==p for p in pats) for M in range(size)]
    # bad[q][M] means there exists a partition into q H-free color classes.
    bad=[None,free]
    for q in range(2,qmax+1):
        nxt=[False]*size
        for M in range(size):
            A=M
            while True:
                if free[A] and bad[-1][M^A]:nxt[M]=True;break
                if A==0:break
                A=(A-1)&M
        bad.append(nxt)
    return {q:[not b for b in bad[q]] for q in range(1,qmax+1)}

cache={}
for n in range(0,6):
    for name,v,ee in cores:
        core=ramsey_table(n,v,ee);cache[n,name]=core
        for s in [0,1,2]:
            padded=ramsey_table(n,v+s,ee)
            for q in [2,3,4]:
                for M,x in enumerate(padded[q]):
                    ck(x==((n>=v+s) and core[q][M]),'padding_identity')

# Host isolate padding, with no alteration to its edge colors or core targets.
for n in range(0,5):
    ix={e:i for i,e in enumerate(edges(n+1))}
    for name,v,ee in cores:
        for M in range(1<<(n*(n-1)//2)):
            bigger=sum(1<<ix[e] for i,e in enumerate(edges(n)) if M>>i&1)
            for q in [2,3,4]:ck(cache[n,name][q][M]==cache[n+1,name][q][bigger],'host_isolate_invariance')

# Concrete small Ramsey threshold and negative-direction certificate.
ck(cache[3,'P3'][2][-1],'K3_two_colors_P3')
ck(not ramsey_table(3,4,[(0,1),(1,2)])[2][-1],'K3_too_small_for_padded_P3')
ck(not cache[4,'P3'][3][-1],'K4_three_colors_avoids_P3')
ck(cache[5,'P3'][3][-1],'K5_three_colors_forces_P3')
# Exhibit the actual three matching classes of K4.
matching_classes=[[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
ck(set(sum(matching_classes,[]))==set(edges(4)),'K4_partition_covers')
for E in matching_classes:
    ck(len(set(sum(([u,v] for u,v in E),[])))==4,'K4_color_is_matching')
# Non-induced warning: K3 contains an ordinary K2+K1, but no induced one.
ck(ramsey_table(3,3,[(0,1)])[2][-1],'noninduced_padding_control')
ck(len(edges(3))!=1,'induced_interpretation_rejected')
# At any fixed order, edgeless target behavior depends only on vertex count.
for n in range(6):
    for v in range(7):
        tab=ramsey_table(n,v,[])
        for q in [2,3,4]:
            for x in tab[q]:ck(x==(n>=v),'edgeless_boundary')
print(json.dumps({'problem_id':30003973,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'host_order_max':5,'host_graphs_per_target':sum(1<<(n*(n-1)//2) for n in range(6)),'core_targets':[x[0] for x in cores],'isolated_target_padding':[0,1,2],'colors':[2,3,4],'method':'Exact edge-subset partition dynamic programming; ordinary subgraph copies by all injective vertex maps','scope':'Bounded consistency checks only. Universal statements are proved in TURN_1.md; no finite signature is called Ramsey equivalence.'},indent=2,sort_keys=True))
