#!/usr/bin/env python3
"""Independent boundary controls; no imported candidate verifier."""
from pathlib import Path
from itertools import product,combinations,combinations_with_replacement
import datetime,hashlib,json,math
HERE=Path(__file__).resolve().parent

def normalize(formula):
    clauses=[]
    for raw in formula:
        c=set(raw)
        if any(-literal in c for literal in c):continue
        if not c:return 'no',(),{}
        clauses.append(tuple(sorted(c,key=lambda l:(abs(l),l))))
    if not clauses:return 'yes',(),{}
    old=sorted({abs(l) for c in clauses for l in c})
    mapping={name:i+1 for i,name in enumerate(old)}
    dense=tuple(tuple(mapping[abs(l)]*(1 if l>0 else -1) for l in c) for c in clauses)
    return 'reduction',dense,mapping

def eval_formula(formula,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in c) for c in formula)

def orient(n,edges,r,inward=False):
    adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    seen={r};queue=[r];arcs=[]
    for u in queue:
        for v in adj[u]:
            if v not in seen:
                seen.add(v);queue.append(v);arcs.append((v,u) if inward else (u,v))
    assert len(seen)==n
    return arcs

def main():
    sparse=[1,7,2**80]
    signed=[i*s for i in sparse for s in [-1,1]]
    clauses=[p for k in range(4) for p in product(signed,repeat=k)]
    formulas=[(c,) for c in clauses]
    basis=[(),(1,),(-1,),(1,1),(1,-1),(7,),(1,7),(-1,-7),(1,7,2**80),(-1,-7,-2**80),(1,7,-7)]
    formulas+=list(combinations_with_replacement(basis,2))
    formulas+=[(),((),),((),(1,-1)),((1,),(-1,)),((2**80,),),((1,-1),(7,-7))]
    checks=0; branches={'yes':0,'no':0,'reduction':0}
    for formula in formulas:
        branch,dense,mapping=normalize(formula);branches[branch]+=1
        names=sorted({abs(l) for c in formula for l in c})
        for bits in product([False,True],repeat=len(names)):
            assignment=dict(zip(names,bits));oldtruth=eval_formula(formula,assignment)
            if branch in ('yes','no'):assert oldtruth==(branch=='yes')
            else:
                newassignment={new:assignment[old] for old,new in mapping.items()}
                assert oldtruth==eval_formula(dense,newassignment)
                assert set(mapping.values())==set(range(1,len(mapping)+1))
                assert len(mapping)<=sum(len(c) for c in dense)
                assert all(1<=len(c)<=3 and len(c)==len(set(c)) and not any(-l in c for l in c) for c in dense)
            checks+=1
    # The literal 2**80 requires one vertex, not a number indexed by its label.
    branch,dense,mapping=normalize(((2**80,),))
    assert branch=='reduction' and dense==((1,),) and len(mapping)==1
    n=4;edges=list(combinations(range(n),2));arcs=[a for u,v in edges for a in [(u,v),(v,u)]]
    table={(r,u,v):2**4096+(31*r+7*u+v)**2 for r in range(n) for u,v in arcs}
    transposed={(r,u,v):table[r,v,u] for r in range(n) for u,v in arcs}
    shifted={key:value+1 for key,value in table.items()}
    trees=0
    for candidate in combinations(edges,n-1):
        # Detect connectedness before invoking the orientation certificate checker.
        seen={0}
        while True:
            expanded=seen|{v for u,v in candidate if u in seen}|{u for u,v in candidate if v in seen}
            if expanded==seen:break
            seen=expanded
        if len(seen)!=n:continue
        trees+=1
        outward=sum(table[r,u,v] for r in range(n) for u,v in orient(n,candidate,r))
        inward_transposed=sum(transposed[r,u,v] for r in range(n) for u,v in orient(n,candidate,r,inward=True))
        shifted_outward=sum(shifted[r,u,v] for r in range(n) for u,v in orient(n,candidate,r))
        assert outward==inward_transposed
        assert shifted_outward-outward==n*(n-1)
        maxbits=max(v.bit_length() for v in table.values())
        assert outward.bit_length()<=maxbits+math.ceil(math.log2(n*(n-1)))
    assert trees==16
    # Every fixed endpoint is connected/simple and has all two root vectors.
    endpoints=[{'name':'yes','cost_per_arc_per_root':0,'K':0,'F':0},
               {'name':'no','cost_per_arc_per_root':1,'K':1,'F':2}]
    for endpoint in endpoints:
        assert endpoint['F']==2*endpoint['cost_per_arc_per_root']
        assert (endpoint['F']<=endpoint['K'])==(endpoint['name']=='yes')
    result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preprocessing_formula_cases':len(formulas),'preprocessing_assignment_checks':checks,'preprocessing_branches':branches,'sparse_label':str(2**80),'sparse_label_dense_variable_count':1,'arbitrary_cost_complete_K4_tree_cases':trees,'large_integer_cost_bitlength':4097,'orientation_transpose_all_pass':True,'positive_shift_all_pass':True,'binary_sum_bitlength_all_pass':True,'fixed_trivial_endpoints':endpoints,'all_pass':True,'scope':'Independent boundary controls supplement the written all-size model and encoding derivations; these finite controls do not establish hardness alone.'}
    (HERE/'BOUNDARY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
