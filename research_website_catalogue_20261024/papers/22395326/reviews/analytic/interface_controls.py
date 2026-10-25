#!/usr/bin/env python3
"""Execute only five fully inspected pure graph functions, not archive entrypoints."""
import ast,json,hashlib
from pathlib import Path
import networkx as nx
E=Path(__file__).absolute().parent
P=E.parents[3]
src=P/'papers/22395326/reviews/scope/tmp/primary/interfaces/22168797-k2p_atlas_core.py'
names={'sd0_mixed','_mixed_triangle_edges','mixed_incidence_graph','mixed_exact_isomorphic','mixed_relation_exact'}
tree=ast.parse(src.read_text()); selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
assert len(selected)==5
# Every selected function's complete body was read before this execution.
space={'nx':nx};exec(compile(ast.Module(body=selected,type_ignores=[]),str(src),'exec'),space)
census=json.loads((E/'embedded-rooting-census.json').read_text())
def graph(row):
 G=nx.DiGraph();G.add_edges_from(map(tuple,row['arcs']))
 for v in G:
  G.nodes[v]['role']='root' if v=='root' else 'leaf' if v in 'RXYZ' else 'retic' if G.in_degree(v)==2 else 'tree'
  G.nodes[v]['label']=v if v in 'RXYZ' else None
 return G
L=graph(census['first'][0]);R=graph(census['second'][0]);A=space['sd0_mixed'](L);B=space['sd0_mixed'](R)
assert space['mixed_relation_exact'](L,R)=='triangle'
assert not space['mixed_exact_isomorphic'](A,B)
assert space['mixed_exact_isomorphic'](A,B,True)
corrupt=B.copy();corrupt.nodes['R']['label']='changed-label'
assert not space['mixed_exact_isomorphic'](A,corrupt,True)
corrupt=B.copy();corrupt.edges['x','y']['heads']=frozenset({'x'})
assert not space['mixed_exact_isomorphic'](A,corrupt,True)
r={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'executed_fully_inspected_functions':sorted(names),'embedded_theta_relation':'triangle','without_erasure_isomorphic':False,'label_corruption_rejected':True,'offsite_head_corruption_rejected':True,'scope':'Two controlled graph endpoints and negative mutations; no full finite-atlas or probe replay.'}
(E/'interface-controls-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
