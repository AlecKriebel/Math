#!/usr/bin/env python3
"""Independent verification of the frozen graph construction and source objective.
Verification only; does not invoke or import the submitted verifier or reviews.
"""
from itertools import product, combinations
from pathlib import Path
import json


def graph(n, clauses, shift=0):
    verts=['r']+[f'{s}{i}' for i in range(1,n+1) for s in ('t','f')]+[f'v{i}' for i in range(1,n+1)]+[f'z{j}' for j in range(len(clauses))]
    layer={'r':0,**{f'{s}{i}':1 for i in range(1,n+1) for s in ('t','f')},**{f'v{i}':2 for i in range(1,n+1)},**{f'z{j}':3 for j in range(len(clauses))}}
    arcs=[('r',f'{s}{i}') for i in range(1,n+1) for s in ('t','f')]+[(f'{s}{i}',f'v{i}') for i in range(1,n+1) for s in ('t','f')]+[(f'v{abs(lit)}',f'z{j}') for j,c in enumerate(clauses) for lit in c]
    assert len(arcs)==len(set(arcs))
    assert all(layer[b]==layer[a]+1 for a,b in arcs)
    incoming={v:[a for a,b in arcs if b==v] for v in verts if v!='r'}
    assert all(1<=len(ps)<=3 for ps in incoming.values())
    costs={v:{a:shift for a in arcs} for v in incoming}
    for j,c in enumerate(clauses):
        for lit in c:
            costs[f'z{j}'][('r',f'f{lit}' if lit>0 else f't{-lit}')]+=1
    assert all(x in {shift,shift+1} for tab in costs.values() for x in tab.values())
    return verts, arcs, incoming, costs


def path(parent, dest):
    visited=set()
    p=[]
    while dest!='r':
        assert dest not in visited
        visited.add(dest)
        assert dest in parent
        a=(parent[dest],dest)
        p.append(a)
        dest=parent[dest]
    return p[::-1]


def scan(n, clauses):
    verts,arcs,incoming,costs=graph(n,clauses)
    order=list(incoming)
    brute_sat=[]
    for truth in product((False,True),repeat=n):
        brute_sat.append(sum(not any(truth[abs(lit)-1]==(lit>0) for lit in c) for c in clauses))
    optimum=min(brute_sat)
    best=None
    trees=0
    for ps in product(*(incoming[v] for v in order)):
        parent=dict(zip(order,ps))
        # Reconstruct all directed root paths and count costs literally.
        paths={v:path(parent,v) for v in order}
        assert all(len(paths[v]) in (1,2,3) for v in order)
        cost=sum(costs[v][a] for v,p in paths.items() for a in p)
        truth={i:parent[f'v{i}']==f't{i}' for i in range(1,n+1)}
        selected_false=0
        for j,c in enumerate(clauses):
            i=int(parent[f'z{j}'][1:])
            lit=next(l for l in c if abs(l)==i)
            selected_false+=truth[i]!=(lit>0)
        assert cost==selected_false
        # +1 per coefficient charges each path once for each arc.
        positive=sum(costs[v][a]+1 for v,p in paths.items() for a in p)
        assert positive==cost+4*n+3*len(clauses)
        assert len(verts)==1+3*n+len(clauses)
        assert len(arcs)<=4*n+3*len(clauses)
        assert 4*n+3*len(clauses)<=3*(len(verts)-1)
        assert len(order)==len(verts)-1
        trees+=1
        best=cost if best is None else min(best,cost)
    assert best==optimum
    return {'n':n,'clauses':clauses,'optimum':optimum,'trees_checked':trees}


def all_clauses(n):
    return [tuple(sign*i for i,sign in zip(vars,signs)) for size in range(1,min(3,n)+1) for vars in combinations(range(1,n+1),size) for signs in product((-1,1),repeat=size)]


def preprocessing(raw):
    out=[]
    for c in raw:
        c=set(c)
        if not c: return 'empty_clause'
        if any(-l in c for l in c): continue
        out.append(tuple(sorted(c,key=lambda l:(abs(l),l))))
    return out


def main():
    results=[]
    for n in range(1,4):
        cs=all_clauses(n)
        for m in range(3):
            for clauses in combinations(cs,m): results.append(scan(n,clauses))
    results.append(scan(3,all_clauses(3)[-8:]))
    # Frozen proof's constant-input clause can use ordinary gadgets already specified.
    results.append(scan(1,[(1,)]))
    results.append(scan(1,[(1,),(-1,)]))
    assert preprocessing([(1,1),(-1,1),(2,-3,-3)])==[(1,),(2,-3)]
    assert preprocessing([(1,),()])=='empty_clause'
    # Source-objective counterexample to independent shortest paths: unit x and not x.
    v,a,inc,costs=graph(1,[(1,),(-1,)])
    individual_minima={}
    for dest in inc:
        individual_minima[dest]=min(sum(costs[dest][e] for e in path(dict(zip(inc,ps)),dest)) for ps in product(*(inc[w] for w in inc)))
    assert sum(individual_minima.values())==0
    assert scan(1,[(1,),(-1,)])['optimum']==1
    report={'verification_family':'independent literal source-objective parent enumeration','all_checks_passed':True,'formula_cases':len(results),'arborescences_checked':sum(r['trees_checked'] for r in results),'per_tree_checks':['simple four-layer DAG','successive layer arcs','indegree<=3 and reachable','binary costs','selected-literal objective equality','positive costs constant offset','optimum=minimum unsatisfied clauses','vertex/arc/numerical bounds'],'independent_shortest_path_counterexample':{'clauses':[[1],[-1]],'minimum_sum_of_independent_destination_path_costs':0,'minimum_common_arborescence_cost':1},'boundary_cases':{'unit_and_binary_clauses':'passed','unused_variables':'passed','no_clauses':'passed; empty terminal layer irrelevant to hard family','duplicate_literals_and_tautology_preprocessing':'passed','empty_clause':'must take the candidate stated trivial-input branch before graph construction','fixed_yes_gadget_optimum':0,'fixed_no_gadget_optimum':1},'case_results':results}
    Path(__file__).with_name('checks_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='case_results'},indent=2))

if __name__=='__main__': main()
