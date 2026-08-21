"""Independent graph-class membership checks for rooted binary networks."""
from __future__ import annotations
from typing import Any,Dict,List,Mapping,Sequence,Tuple
import networkx as nx
from .compiler import Network

def classify(net:Network)->Dict[str,Any]:
    net.validate();G=nx.DiGraph([(e.tail,e.head,{'id':e.id}) for e in net.edges])
    if not nx.is_directed_acyclic_graph(G):raise ValueError('network is not acyclic')
    indeg=dict(G.in_degree());outdeg=dict(G.out_degree())
    roots=[v for v in G if indeg[v]==0];leaves=[v for v in G if outdeg[v]==0]
    ret=[v for v in G if indeg[v]==2 and outdeg[v]==1]
    tree=[v for v in G if indeg[v] in (0,1) and outdeg[v]==2]
    degree2=[v for v in G if indeg[v]==1 and outdeg[v]==1]
    binary=all((indeg[v],outdeg[v]) in {(0,2),(1,2),(2,1),(1,0),(1,1)} for v in G)
    omnians=[v for v in G if outdeg[v]>0 and all(indeg[w]==2 for w in G.successors(v))]
    tree_child=all(outdeg[v]==0 or any(indeg[w]<=1 for w in G.successors(v)) for v in G)
    blocks=list(nx.biconnected_components(G.to_undirected()))
    block_retics=[sum(v in ret for v in b) for b in blocks]
    level=max(block_retics or [0])
    cyclomatic=[G.to_undirected().subgraph(b).number_of_edges()-len(b)+1 for b in blocks]
    return {'roots':roots,'leaves':leaves,'reticulations':ret,'tree_vertices':tree,'subdivision_vertices':degree2,
            'binary':binary,'omnians':omnians,'tree_child':tree_child,'level':level,
            'block_reticulation_counts':block_retics,'block_cyclomatic_numbers':cyclomatic}
