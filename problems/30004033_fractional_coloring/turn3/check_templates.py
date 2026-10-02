#!/usr/bin/env python3
"""Exact seven-template certificates and finite-palette path reconstruction."""
from itertools import combinations,permutations,product
from collections import Counter
import json
EDGES=list(combinations(range(4),2))
TEMPLATES=[
 ('empty',[],[(1,2,3),(1,4,5),(1,6,7),(1,2,8)]),
 ('one_edge',[(0,1)],[(1,2,3),(4,5,6),(1,4,7),(2,4,8)]),
 ('two_adjacent',[(0,1),(0,2)],[(1,2,3),(4,5,6),(4,5,7),(1,4,6)]),
 ('matching',[(0,1),(2,3)],[(1,2,3),(4,5,6),(1,4,7),(2,5,8)]),
 ('star',[(0,1),(0,2),(0,3)],[(1,2,3),(4,5,6),(4,5,7),(4,6,7)]),
 ('path',[(0,1),(1,2),(2,3)],[(1,2,3),(4,5,6),(1,2,7),(3,4,8)]),
 ('cycle',[(0,1),(1,2),(2,3),(0,3)],[(1,2,3),(5,6,7),(1,2,4),(5,6,8)])]

def path_extend(A,C,L):
    """Construct a path in the disjointness graph by exact backwards recursion."""
    if L==1:
        assert A.isdisjoint(C);return [A,C]
    for B in map(frozenset,combinations(set(range(1,9))-C,3)):
        t=len(A&B);k=(L-1)//2
        low,high=(max(0,3-2*k),3) if (L-1)%2==0 else (0,min(3,2*k))
        if low<=t<=high:return path_extend(A,B,L-1)+[C]
    raise AssertionError('infeasible endpoint data')

def check():
    c=Counter();types=Counter();maps=[]
    for name,E,S in TEMPLATES:
        E=set(E);S=list(map(frozenset,S))
        for a,b in EDGES:
            assert (len(S[a]&S[b])==0 if (a,b) in E else 1<=len(S[a]&S[b])<=2);c['template_pair_constraints']+=1
    for mask in range(64):
        E={e for i,e in enumerate(EDGES) if mask>>i&1}
        if any(all(tuple(sorted(e)) in E for e in combinations(T,2)) for T in combinations(range(4),3)):continue
        found=None
        for name,TE,S in TEMPLATES:
            for p in permutations(range(4)):
                image={tuple(sorted((p[a],p[b]))) for a,b in TE}
                if image==E:
                    coloring=[None]*4
                    for i in range(4):coloring[p[i]]=frozenset(S[i])
                    found=(name,coloring);break
            if found:break
        assert found;c['labeled_trianglefree_core_classification']+=1
        name,S=found;types[name]+=1;maps.append({'edge_mask':mask,'template':name,'sets':[sorted(x) for x in S]})
        for a,b in EDGES:
            lengths=[1] if (a,b) in E else range(2,16)
            for L in lengths:
                P=path_extend(S[a],S[b],L)
                assert len(P)==L+1 and P[0]==S[a] and P[-1]==S[b];c['path_endpoints']+=1
                assert all(len(x)==3 for x in P) and all(P[j].isdisjoint(P[j+1]) for j in range(L));c['path_vertex_and_edge_constraints']+=1
    assert sum(types.values())==41;c['classification_total']+=1
    return {'status':'pass','assertions':sum(c.values()),'breakdown':dict(c),'labeled_core_types':dict(types),'classification_certificate':maps,'scope':'All 41 labeled triangle-free four-vertex core graphs; path constructions checked through length 15. The proof handles every finite length by integer induction.'}
if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
