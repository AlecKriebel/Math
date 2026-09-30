"""Construct Knudson's descending integer function for a finite filtered graph.

Cells are tuples: a vertex is (v,), an edge is a sorted pair (v,w).
The input order adds one simplex at a time. Only graph inputs are accepted.
"""
from itertools import combinations

def persistence(order):
    """Independent F2 column reduction; return labeled pairs and cycle-birth edges."""
    pos={cell:i for i,cell in enumerate(order)}
    pivots={};pairs=set();cycles=set()
    for cell in order:
        col={tuple([v]) for v in cell} if len(cell)==2 else set()
        while col:
            pivot=max(col,key=pos.get)
            if pivot not in pivots:break
            col ^= pivots[pivot]
        if col:
            pivots[pivot]=col;pairs.add((pivot,cell))
        elif len(cell)==2:cycles.add(cell)
    return pairs,cycles

def validate(order):
    seen=set()
    for cell in order:
        if len(cell) not in (1,2) or len(set(cell))!=len(cell):
            raise ValueError('Expected nonempty simplices of dimension at most one')
        if cell in seen:raise ValueError('Repeated simplex')
        if len(cell)==2 and any((v,) not in seen for v in cell):
            raise ValueError('An edge precedes an endpoint')
        seen.add(cell)

def component_before(order,edge,vertex):
    prefix=order[:order.index(edge)]
    vertices={c for c in prefix if len(c)==1}
    parent={v:v for v in vertices}
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    for c in prefix:
        if len(c)==2:
            a,b=(c[0],),(c[1],);parent[root(a)]=root(b)
    return {v for v in vertices if root(v)==root(vertex)}

def realize_graph(original):
    order=list(original);validate(order)
    target,cycle_births=persistence(order)
    matching=sorted((v,e) for v,e in target if v[0] in e)
    locked=[];moves=[]
    for vertex,edge in matching:
        if order.index(edge)!=order.index(vertex)+1:
            i=order.index(edge);prefix=order[:i]
            comp=component_before(order,edge,vertex)
            removed=[c for c in prefix if all((v,) in comp for v in c)]
            remaining=[c for c in prefix if c not in set(removed)]
            replay=[c for c in removed if c!=vertex]
            order=remaining+[vertex,edge]+replay+order[i+1:]
            moves.append({'vertex':vertex,'edge':edge,'postponed':replay})
        locked.append((vertex,edge))
        validate(order)
        assert all(order.index(e)==order.index(v)+1 for v,e in locked)
        assert persistence(order)==(target,cycle_births)
    pos={c:i for i,c in enumerate(order)}
    f={c:2*i for i,c in enumerate(order)}
    for v,e in matching:
        i=pos[v];f[v]=2*i+1;f[e]=2*i
    if f:
        minimum=min(f.values());f={c:a-minimum for c,a in f.items()}
    # Entry times in the source's generated-subcomplex filtration.
    entry={c:min(f[d] for d in order if set(c)<=set(d)) for c in order}
    refinement=sorted(order,key=lambda c:(entry[c],pos[c]))
    assert refinement==order
    return {'order':order,'function':f,'entry':entry,'matching':set(matching),
            'pairs':target,'cycle_births':cycle_births,'moves':moves}
