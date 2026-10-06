#!/usr/bin/env python3
"""Check exact-optimum language and a naive arc-cost aggregation against the source."""
from itertools import product
from pathlib import Path
import json
from independent_scope_checks import graph,path

signed_parents=[{'a':'r','b':'r'},{'a':'r','b':'a'}]
signed_costs={'a':{('r','a'):0,('r','b'):0,('a','b'):0},'b':{('r','a'):0,('r','b'):0,('a','b'):-1}}
signed_values=[sum(signed_costs[v][e] for v in parent for e in path(parent,v)) for parent in signed_parents]
assert signed_values==[0,-1]
verts,arcs,inc,costs=graph(2,[(1,),(-1,),(1,2)])
scalar={a:sum(costs[v][a] for v in costs) for a in arcs}
source_values=[]
aggregated_values=[]
for choices in product(*(inc[v] for v in inc)):
    parent=dict(zip(inc,choices))
    source_values.append(sum(costs[v][e] for v in inc for e in path(parent,v)))
    aggregated_values.append(sum(scalar[(u,v)] for v,u in parent.items()))
assert sorted(set(source_values))==[1,2]
assert set(aggregated_values)=={4}
result={'all_checks_passed':True,'signed_exact_optimum_guard':{'graph_arcs':[['r','a'],['r','b'],['a','b']],'nonzero_coefficient':'c^b_(a,b)=-1','all_other_coefficients':0,'feasible_tree_costs':signed_values,'has_zero_cost_witness':True,'optimum':-1,'conclusion':'A zero-cost certificate alone does not certify exact optimum zero with signed costs; frozen candidate does not claim that.'},'naive_arc_vector_sum_guard':{'clauses':[[1],[-1],[1,2]],'distinct_source_tree_costs':sorted(set(source_values)),'distinct_tree_arc_costs_after_summing_all_destination_vectors':sorted(set(aggregated_values)),'conclusion':'Summing vectors then solving ordinary minimum arborescence changes the objective.'}}
Path(__file__).with_name('guard_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
