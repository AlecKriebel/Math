#!/usr/bin/env python3
"""Source-first independent exact control; reads no candidate artifacts."""
from itertools import product
from collections import defaultdict
import json
from pathlib import Path

V=tuple(range(6)); edges=((0,1),(1,2),(2,3),(3,4),(4,5),(5,0))
states=list(product((0,1), repeat=6))
weights={x:(2 if x==(1,)*6 else 1) if x[0]==x[1] and x[2]==x[3] and x[4]==x[5] else 0 for x in states}

def separated(A,B,C):
    todo=list(A); seen=set(A)
    while todo:
        v=todo.pop()
        for u,w in edges:
            z=w if u==v else u if w==v else None
            if z is not None and z not in C and z not in seen:
                seen.add(z); todo.append(z)
    return not bool(seen & set(B))

def project(x,A): return tuple(x[i] for i in A)

mtp_failures=[]
for x,y in product(states,repeat=2):
    lo=tuple(min(a,b) for a,b in zip(x,y)); hi=tuple(max(a,b) for a,b in zip(x,y))
    if weights[lo]*weights[hi] < weights[x]*weights[y]: mtp_failures.append((x,y))

separation_count=0; ci_failures=[]; minor_count=0
for labels in product(range(4),repeat=6):
    A=tuple(i for i,t in enumerate(labels) if t==1)
    B=tuple(i for i,t in enumerate(labels) if t==2)
    C=tuple(i for i,t in enumerate(labels) if t==3)
    if not A or not B or not separated(A,B,C): continue
    separation_count+=1
    tables=defaultdict(lambda:defaultdict(int))
    for x,w in weights.items(): tables[project(x,C)][project(x,A),project(x,B)]+=w
    for c,table in tables.items():
        aa=sorted({a for a,b in table}); bb=sorted({b for a,b in table})
        for a0,a1,b0,b1 in product(aa,aa,bb,bb):
            minor_count+=1
            if table[a0,b0]*table[a1,b1] != table[a0,b1]*table[a1,b0]:
                ci_failures.append((A,B,C,c,a0,a1,b0,b1))

p_even=p_odd=1
for a,b,c in product((0,1),repeat=3):
    w=weights[(a,a,b,b,c,c)]
    if (a+b+c)%2: p_odd*=w
    else: p_even*=w
result={
    'vertices':list(V),'edges':[list(e) for e in edges],
    'weight_total':sum(weights.values()),'support_size':sum(w>0 for w in weights.values()),
    'mtp2_pair_checks':len(states)**2,'mtp2_failures':mtp_failures,
    'ordered_nonempty_global_separations':separation_count,
    'exact_ci_minors_checked':minor_count,'ci_failures':ci_failures,
    'edge_factorization_even_product':p_even,'edge_factorization_odd_product':p_odd,
    'factorization_binomial_residual_unnormalized':p_even-p_odd,
    'factorization_binomial_residual_normalized':'-1/6561',
    'interpretation':'Global Markov and MTP2 exactly; clique-factorization obstruction nonzero (C6 has no triangles).'
}
assert not mtp_failures and not ci_failures
assert sum(weights.values())==9 and p_even==1 and p_odd==2
out=Path(__file__).with_name('source_control_result.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
