"""Additional audit, independent Floyd-Warshall phase feasibility check."""
import json
import sys
from itertools import product
from pathlib import Path
import networkx as nx
base=Path(__file__).parent
sat=json.loads((base/'computation/dodecahedron_20_7.json').read_text())
unsat=json.loads((base/'computation/dodecahedron_17_6_unsat.json').read_text())
canon=lambda es:{tuple(sorted(e)) for e in es}
assert canon(sat['edges'])==canon(unsat['edges'])
g=nx.Graph();g.add_nodes_from(sat['vertices']);g.add_edges_from(sat['edges'])
p=nx.Graph()
p.add_edges_from((i,(i+1)%10) for i in range(10))
p.add_edges_from((i,10+i) for i in range(10))
p.add_edges_from((10+i,10+(i+2)%10) for i in range(10))
assert nx.is_isomorphic(g,p) and nx.is_isomorphic(g,nx.dodecahedral_graph())
assert nx.check_planarity(g)[0] and set(dict(g.degree()).values())=={3}
assert sum(nx.triangles(g).values())==0

def matchings(vertices):
    if not vertices:
        yield set();return
    u=min(vertices)
    for v in sorted(set(p[u]) & vertices):
        for rest in matchings(vertices-{u,v}):
            yield rest | {tuple(sorted((u,v)))}
count=systems=0
for matching in matchings(set(p)):
    f=p.copy();f.remove_edges_from(matching)
    if not nx.is_bipartite(f):continue
    assert nx.is_connected(f)
    b=nx.bipartite.color(f)
    long=[e for e in sorted(matching) if b[e[0]]==b[e[1]]]
    assert len(long)==6
    count+=1
    for flips in product((0,1),repeat=len(long)):
        d=[[10**6]*21 for _ in range(21)]
        for i in range(21):d[i][i]=0
        for u,v in p.edges:
            if b[u]!=b[v]:d[u][v]=d[v][u]=3
        for (u,v),flip in zip(long,flips):
            if flip:u,v=v,u
            d[u][v]=-7
        for i in range(20):d[20][i]=8;d[i][20]=0
        for k in range(21):
            for i in range(21):
                for j in range(21):
                    d[i][j]=min(d[i][j],d[i][k]+d[k][j])
        assert any(d[i][i]<0 for i in range(21))
        systems+=1
assert count==30 and systems==1920
print('PASS: identical SAT/UNSAT graph, isomorphic G(10,2), planar cubic triangle-free.')
print('PASS: independently enumerated 30 even factors, 1920 negative-cycle systems by Floyd-Warshall.')
