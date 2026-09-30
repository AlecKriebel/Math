"""Exact graph-construction controls, not evidence for higher-dimensional realization."""
import random,json,hashlib
from pathlib import Path
from itertools import combinations
from construct_graph import realize_graph,persistence
rng=random.Random(30000991);checks=0;cases=0;moves=0
def check(x):
 global checks
 assert x
 checks+=1

def elder(order):
    parent={};born={};pairs=set();cycles=set()
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    for i,c in enumerate(order):
        if len(c)==1:parent[c]=c;born[c]=i
        else:
            a,b=root((c[0],)),root((c[1],))
            if a==b:cycles.add(c);continue
            old,young=sorted([a,b],key=born.get)
            pairs.add((young,c));parent[young]=old
    return pairs,cycles

def one(order):
    global cases,moves
    r=realize_graph(order);cases+=1;moves+=len(r['moves'])
    check(persistence(order)==elder(order))
    check(persistence(r['order'])==elder(r['order'])==elder(order))
    check(set(r['order'])==set(order) and len(r['order'])==len(order))
    check(set(r['matching'])=={(v,e) for v,e in r['pairs'] if v[0] in e})
    for v,e in r['matching']:check(r['order'].index(e)==r['order'].index(v)+1)
    for e in order:
        if len(e)==2:
            for x in e:
                v=(x,)
                check((r['function'][v]>r['function'][e]) if (v,e) in r['matching'] else (r['function'][e]>r['function'][v]))
    entry={c:min(r['function'][d] for d in order if set(c)<=set(d)) for c in order}
    check(entry==r['entry'])
    refinement=sorted(order,key=lambda c:(entry[c],r['order'].index(c)))
    check(refinement==r['order'])
    check(elder(refinement)==elder(order))
    check(not r['function'] or min(r['function'].values())==0)
    return r

def random_order(vertices,edges):
    remaining={(v,) for v in vertices}|set(edges);order=[]
    while remaining:
        available=[c for c in remaining if len(c)==1 or all((v,) in order for v in c)]
        c=rng.choice(sorted(available));remaining.remove(c);order.append(c)
    return order

one([])
for n in range(1,5):
    E=list(combinations(range(n),2))
    for mask in range(1<<len(E)):
        edges=[e for i,e in enumerate(E) if mask>>i&1]
        for _ in range(5):one(random_order(range(n),edges))
for n in [5,6,7]:
    E=list(combinations(range(n),2))
    for _ in range(30):one(random_order(range(n),[e for e in E if rng.randrange(3)]))
# Credited prior Conjecture2 counterexample is a positive control for Conjecture3.
prior=[(0,),(1,),(2,),(3,),(2,3),(1,3),(0,2)]
r=one(prior)
check(r['pairs']=={((3,),(2,3)),((2,),(1,3)),((1,),(0,2))})
check([r['function'][c] for c in prior]==[0,2,4,7,6,10,12])
P=Path(__file__).parent
out={'status':'pass','assertions':checks,'graph_filtrations':cases,'component_postponements':moves,
     'sampling':'All labeled simple graphs on1–4 vertices, five deterministic random simplex orders each;90 further sampled graphs on5–7 vertices; empty and credited prior controls.',
     'scope':'Graph theorem only; finite controls do not prove or disprove higher-dimensional realization.',
     'artifact_sha256':hashlib.sha256((P/'GRAPH_CASE.md').read_bytes()).hexdigest() if (P/'GRAPH_CASE.md').exists() else 'pending'}
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
