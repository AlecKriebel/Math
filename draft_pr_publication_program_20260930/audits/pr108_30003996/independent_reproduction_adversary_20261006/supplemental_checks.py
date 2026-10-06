#!/usr/bin/env python3
"""After-freeze checks: exact author-suite cross-census, inward convention, boundaries."""
from collections import Counter
from fractions import Fraction
import datetime,hashlib,itertools,json,random,sys
from pathlib import Path
import independent_model as M
HERE=Path(__file__).resolve().parent
suite=[]
for n in (1,2):
 C=[]
 for size in range(1,n+1):
  for vs in itertools.combinations(range(1,n+1),size):
   C.extend(tuple(v*s for v,s in zip(vs,signs)) for signs in itertools.product((-1,1),repeat=size))
 for m in (1,2,3):
  suite.extend((n,cs) for cs in itertools.combinations_with_replacement(C,m))
C=[tuple((i+1)*s for i,s in enumerate(signs)) for signs in itertools.product((-1,1),repeat=3)]
suite.extend((3,cs) for cs in itertools.combinations_with_replacement(C,2))
suite.extend((3,cs) for cs in [((1,),(-1,),(1,2,3)),((1,2,3),(-1,-2,-3),(1,-2,3)),((1,),(-2,),(2,3))])
counts=Counter();graphs=set()
for n,clauses in suite:
 model=M.cnf_model(tuple(range(1,n+1)),clauses)
 V,E,C,K=(model[k] for k in ('vertices','edges','costs','K'))
 ix={v:i for i,v in enumerate(V)}
 graphs.add((len(V),tuple(sorted(M.edge(ix[u],ix[v]) for u,v in E))))
 feasible=0
 for tree in M.all_subset_trees(V,E):
  F=M.cut_total(V,tree,C)
  M.require(F==M.rooted_total(V,tree,C),'author-suite root/cut mismatch')
  feasible+=F<=K
  counts['actual_spanning_tree_formula_cases']+=1
 M.require(bool(feasible)==M.sat(tuple(range(1,n+1)),clauses),'author-suite SAT threshold mismatch')
 counts['formulas']+=1
original=json.loads((HERE.parent/'original_source_authentication_20261006/original_attempt/verification.json').read_text())
M.require(counts['formulas']==original['formulas_checked']==212,'author formula count mismatch')
M.require(counts['actual_spanning_tree_formula_cases']==original['spanning_tree_formula_cases']==37629,'author tree count mismatch')
M.require(len(graphs)==original['distinct_graphs']==26,'author graph count mismatch')

# Singleton tree and arbitrary signed rational dense source-cost vectors.
V=('singleton',); C={'singleton':{}}
M.require(M.rooted_total(V,(),C)==M.cut_total(V,(),C)==0,'singleton objective mismatch')
vertices=('a','b','c','d');E=tuple(itertools.combinations(vertices,2))
rng=random.Random(108)
C={r:{(u,v):Fraction(rng.randrange(-10**5,10**5),rng.randrange(1,17)) for u,v in E}|{(v,u):Fraction(rng.randrange(-10**5,10**5),rng.randrange(1,17)) for u,v in E} for r in vertices}
inward_count=0
for word in itertools.product(vertices,repeat=2):
 tree=M.prufer_tree(vertices,word);adj=M.adjacency(vertices,tree)
 reverse={r:{(u,v):vec[v,u] for u,v in vec} for r,vec in C.items()}
 # Direct inward traversal with reversed cost entries, using all roots.
 inward=0
 for root in vertices:
  seen={root};todo=[root]
  while todo:
   u=todo.pop()
   for v in adj[u]:
    if v not in seen:
     seen.add(v);todo.append(v);inward+=reverse[root][v,u]
 M.require(inward==M.rooted_total(vertices,tree,C)==M.cut_total(vertices,tree,C),'signed rational inward-reversal mismatch')
 inward_count+=1
# Explicit encoding rejection controls.
m=M.cnf_model((7,10**100+267),((7,10**100+267),(-7,)))
blob=M.serialize(m);data=json.loads(blob)
failures=0
for bad in [dict(data,costs=data['costs'][:-1]),dict(data,costs=data['costs'][:-1]+[data['costs'][0]])]:
 try:M.deserialize(json.dumps(bad).encode())
 except RuntimeError:failures+=1
 else:raise RuntimeError('malformed dense cost encoding accepted')
M.require(failures==2,'missing dense encoding failures')
result={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'author_suite_independent_actual_census':dict(counts),'author_suite_distinct_graphs':len(graphs),'signed_rational_dense_inward_and_cut_checks':inward_count,'singleton_tree_checks':1,'sparse_id_example':{'max_literal_bit_length':max(i.bit_length() for i in m['variable_ids']),'N':len(m['vertices']),'dense_cost_entry_count':len(m['vertices'])*2*len(m['edges']),'json_encoding_bytes':len(blob)},'malformed_dense_encodings_rejected':failures,'scope':'Finite supplemental audit. Author dataset read after the original independent model freeze; no original check functions used.'}
(HERE/('supplemental_results_optimized.json' if sys.flags.optimize else 'supplemental_results.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
