"""Independent bounded controls for graph lemmas, not a universal proof.
Generate binary trees and at most two reticulations by ordered edge subdivisions.
No paper code, catalogue, certificate, or verdict is imported.
Only rooted-tree-child graphs with two ordinary root children are retained;
this is a sufficient strong-tree-child subdomain, not full class exhaustion.
"""
from itertools import combinations, permutations
from collections import Counter
import json, hashlib
from pathlib import Path
import networkx as nx

OUT=Path(__file__).resolve().parent
stats=Counter()

def trees(labels):
    if len(labels)==1:
        yield labels[0]; return
    first=labels[0]
    for k in range(1,len(labels)):
        for rest in combinations(labels[1:],k-1):
            a=(first,)+rest; b=tuple(x for x in labels if x not in a)
            for aa in trees(a):
                for bb in trees(b):yield (aa,bb)

def graph(tree):
    g=nx.DiGraph(); count=[0]
    def add(t):
        if isinstance(t,int):g.add_node('L'+str(t));return 'L'+str(t)
        u='T'+str(count[0]);count[0]+=1
        for t1 in t:g.add_edge(u,add(t1))
        return u
    add(tree);return g

def augment(g,depth):
    for e,f in permutations(list(g.edges),2):
        h=g.copy();h.remove_edges_from((e,f))
        u='A'+str(depth);r='R'+str(depth)
        h.add_edges_from(((e[0],u),(u,e[1]),(f[0],r),(r,f[1]),(u,r)))
        if nx.is_directed_acyclic_graph(h):yield h

def strong_subset(g):
    if any(g.out_degree(u)>0 and not any(g.in_degree(v)==1 for v in g.successors(u)) for u in g):return False
    root=next(v for v in g if g.in_degree(v)==0)
    return all(g.in_degree(c)==1 for c in g.successors(root))

def inspect(g):
    leaves={v for v in g if g.out_degree(v)==0}
    desc={v:nx.descendants(g,v) for v in g}
    C={v:({v} if v in leaves else desc[v]&leaves) for v in g}
    retics={v for v in g if g.in_degree(v)==2}
    for u,v in combinations(g,2):
        if v not in desc[u] and u not in desc[v]:assert not C[u]<=C[v] and not C[v]<=C[u]
    for v in g:
        if g.out_degree(v)==2:assert len(C[v])>=2
    for u,v in combinations(retics,2):
        assert C[u]!=C[v]
        if v not in desc[u] and u not in desc[v]:assert not C[u]&C[v]
    blocks=list(nx.biconnected_components(g.to_undirected()))
    bridges={frozenset(e) for e in nx.bridges(g.to_undirected())}
    for v in retics:
        for r in retics-{v}:
            if v in desc[r] and any({v,r}<=b for b in blocks):
                assert frozenset((v,next(g.successors(v)))) in bridges
                stats['lower_sink_bridge_checks']+=1
    # One sample/taxon; all pairs exposed; and each singly doubled taxon.
    for doubled in [set(),leaves,*({l} for l in sorted(leaves))]:
        sc={v:frozenset((x,i) for x in C[v] for i in range(2 if x in doubled else 1)) for v in g}
        H=g.copy()
        for r in retics:
            if len(sc[r])==1:
                leaf=next(g.successors(r));assert leaf in leaves
                H.add_edges_from((p,leaf) for p in g.predecessors(r));H.remove_node(r)
        tr=nx.transitive_reduction(H)
        for v in H:
            if g.out_degree(v)!=2:continue
            a,b=g.successors(v)
            supp={frozenset((x,y)) for x in sc[a] for y in sc[b] if x!=y}
            assert set().union(*supp)==set(sc[v])
            if tr.out_degree(v)==2:continue
            assert tr.out_degree(v)==1
            w=next(tr.successors(v));assert g.in_degree(w)==1 and sc[v]==sc[w]
            missing=set(H.successors(v))-set(tr.successors(v));assert len(missing)==1
            actual=next(iter(missing))
            candidates=[]
            for h in H:
                if h not in retics and not (h in leaves and len(sc[h])==1):continue
                if h not in nx.descendants(H,v) or tr.in_degree(h)!=1:continue
                d=sc[h];c=sc[v]
                if not d<c:continue
                candidate_supp={frozenset(p) for p in combinations(c,2) if set(p)&d}
                if candidate_supp==supp:candidates.append(h)
            assert actual in candidates
            if len(sc[v])>=3:assert candidates==[actual],(list(g.edges),v,candidates)
            elif len(candidates)>1:
                assert len(sc[v])==2 and len(C[v])==2
                assert all(len(sc[x])==1 for x in C[v])
                stats['bi_unary_ambiguous_completions']+=1
            stats['shortcut_checks']+=1
        stats['sampling_cases']+=1
    stats['accepted_graph_presentations']+=1
    stats['reticulations_'+str(len(retics))]+=1

for n in range(2,5):
    for t in trees(tuple(range(n))):
        g=graph(t);inspect(g)
        for h in augment(g,0):
            if not strong_subset(h):continue
            inspect(h)
            for j in augment(h,1):
                if strong_subset(j):inspect(j)
# A deliberate level-three control: two incomparable reticulations reconverge.
g=nx.DiGraph([('S','P'),('S','Q'),('P','A'),('P','R1'),('A','a'),('A','R1'),('Q','B'),('Q','R2'),('B','b'),('B','R2'),('R1','C'),('C','c'),('C','R3'),('R2','D'),('D','d'),('D','R3'),('R3','e')])
assert strong_subset(g)
assert not nx.has_path(g,'R1','R2') and not nx.has_path(g,'R2','R1')
assert (nx.descendants(g,'R1') & nx.descendants(g,'R2'))=={'R3','e'}
assert any({'R1','R2','R3'}<=b for b in nx.biconnected_components(g.to_undirected()))
stats['level_three_negative_controls']=1
result={'status':'PASS','stats':dict(stats),'scope':__doc__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'negative_control':'Level-three tree-child network has incomparable reticulations with overlapping descendant clusters; level-two hypothesis is material.'}
(OUT/'independent_graph_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
