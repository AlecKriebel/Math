"""Exact finite test of the graph sign equivalence in mixed.tex 676-729.
Every simple graph on <=4 vertices, all torus subsets and all edge signs.
The general proof remains the path-product argument in the audit.
"""
import itertools, json
from pathlib import Path

def cycle_path_condition(n, edges, bits, torus):
    adj=[[] for _ in range(n)]
    for (u,v),b in zip(edges,bits): adj[u].append((v,b)); adj[v].append((u,b))
    for start in range(n):
        def visit(v, seen, product):
            if v != start and start in torus and v in torus and product:
                return False
            for w,b in adj[v]:
                if w == start and len(seen)>=3 and product^b:
                    return False
                if w not in seen and not visit(w,seen|{w},product^b):
                    return False
            return True
        if not visit(start,{start},0):return False
    return True

def has_vertex_signs(n,edges,bits,torus):
    for vertex in itertools.product([0,1],repeat=n):
        if any(vertex[t] for t in torus):continue
        if all(vertex[u]^vertex[v]==b for (u,v),b in zip(edges,bits)):return True
    return False

count=0
for n in range(1,5):
    possible=list(itertools.combinations(range(n),2))
    for mask in itertools.product([0,1],repeat=len(possible)):
        edges=[e for e,x in zip(possible,mask) if x]
        for torusmask in itertools.product([0,1],repeat=n):
            torus={i for i,x in enumerate(torusmask) if x}
            for bits in itertools.product([0,1],repeat=len(edges)):
                left=cycle_path_condition(n,edges,bits,torus)
                right=has_vertex_signs(n,edges,bits,torus)
                assert left==right,(n,edges,torus,bits,left,right)
                count+=1
# Parallel-edge 2-cycle: products must agree with the vertex formula.
parallel=0
for bits in itertools.product([0,1],repeat=2):
    for torus in [set(),{0},{1},{0,1}]:
        required = bits[0]==bits[1] and (torus!={0,1} or bits[0]==0)
        assert required == has_vertex_signs(2,[(0,1),(0,1)],bits,torus)
        parallel+=1
result={'simple_graph_cases':count,'parallel_edge_cases':parallel,'result':'all passed',
        'scope':'finite checks only; algebraicity inputs and general graph proof not certified by this enumeration'}
print(json.dumps(result,indent=2))
Path(__file__).with_name('graph_sign_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
