"""Independent compressed-graph verifier of the authored finite certificate."""
import json
from collections import Counter
from itertools import product
from pathlib import Path

# Two-step transitions between unexpanded vertices; the middle label is a gadget.
vertices=[(t,i) for t in (0,1) for i in range(10)]
edges=set()
for i in range(10):
    j=(i+1)%10
    edges.update([((0,i),(0,j)),((0,j),(1,i)),((1,i),(1,j)),((1,j),(0,i))])
odd=sorted(v for v in vertices if v[1]%2==0)
gadgets=set(vertices)-set(odd)
transitions={u:sorted((g,w) for a,g in edges if a==u for b,w in edges if b==g) for u in odd}
trails=[]
for start in odd:
    def walk(at,seen,steps):
        for g,w in transitions[at]:
            nxt=steps+[(at,g,w)]
            if w==start:
                visits=Counter(x[1] for x in nxt)
                assert max(visits.values())<=2
                trails.append((nxt,visits))
            elif w>start and w not in seen:
                walk(w,seen|{w},nxt)
    walk(start,{start},[])
counts=Counter((list(v.values()).count(1),list(v.values()).count(2)) for _,v in trails)
expected={(0,2):10,(0,5):10,(2,0):30,(2,1):30,(2,2):40,(2,3):40,(2,4):30,(5,0):4,(5,1):20,(5,2):20,(7,0):140,(7,1):200,(9,0):100}
assert counts==expected
D,K=64,24
A=(D+1)**2*2**K-1
B=(D*D+D+1)**2*3**K-2*(D+1)**2*2**K+1
A0=(D+1)*2**K
B0=D*(D*D+D+1)*3**K-(D+1)*2**K
external={}
for u,g in sorted(edges):
    if u not in odd:continue
    destroyed=0
    for steps,visits in trails:
        if not any(a==u and b==g for a,b,_ in steps):continue
        term=1
        for h,r in visits.items():
            term*=((A0 if r==1 else B0) if h==g else (A if r==1 else B))
        destroyed+=term
    external[str((u,g))]=destroyed
    # A Hamiltonian base path is exactly a trail with all 10 odd vertices
    # and all 10 distinct gadgets, ending at g instead of closing.
    def ham(at,seen):
        if at==g:return len(seen)==20
        return any(ham(b,seen|{b}) for a,b in edges if a==at and b not in seen and (a,b)!=(u,g))
    assert ham(u,{u})
assert len(external)==20 and len(set(external.values()))==1
F=max(external.values());G=D**18*2**(9*K)
assert F<G
local=[(A0,B0)]+[((D+1)*2**(K-i),(D+1)*(D*D+D+1)*2**(i-1)*3**(K-i)-(D+1)*2**(K-i)) for i in range(1,K+1)]+[(1,D*(D+1)*2**K-1)]
assert all(a<=A0 and b<=B0 for a,b in local)

# Materialize this finite graph independently with vertex labels (base,layer,index).
groups={}
for v in vertices:
    groups[v]=[(v,0,0)] if v in odd else [(v,r,j) for r in range(K+2) for j in range(D if r in (0,K+1) else 1)]
V=set(sum(groups.values(),[]))
E={(p,q) for u,v in edges for p in groups[u] for q in groups[v]}
E.update((p,q) for v in gadgets for p in groups[v] for q in groups[v] if p[1]<q[1])
assert len(V)==1530 and len(E)==80520
assert all(p!=q and (q,p) not in E for p,q in E)
def reverse(p):
    (t,i),r,j=p
    return p if i%2==0 else ((1-t,i),K+1-r,j)
assert {reverse(p) for p in V}==V
assert {(reverse(q),reverse(p)) for p,q in E}==E
# Two reachability searches per deletion suffice for strong connectivity.
forward={p:[] for p in V};backward={p:[] for p in V}
for p,q in E:forward[p].append(q);backward[q].append(p)
for removed in V:
    start=next(p for p in V if p!=removed)
    for adjacency in (forward,backward):
        seen={start};todo=[start]
        while todo:
            for q in adjacency[todo.pop()]:
                if q!=removed and q not in seen:seen.add(q);todo.append(q)
        assert len(seen)==len(V)-1
# Direct local-path enumeration is separate from the closed-form derivation.
for d in (1,2,3):
    for k in range(5):
        layers=[list(range(d))]+[[d+i] for i in range(k)]+[list(range(d+k,2*d+k))]
        paths=[tuple(x for x in p if x is not None) for p in product(*[[None]+l for l in layers]) if any(x is not None for x in p)]
        pairs=[(p,q) for p in paths for q in paths if set(p).isdisjoint(q)]
        assert len(paths)==(d+1)**2*2**k-1
        assert len(pairs)==(d*d+d+1)**2*3**k-2*(d+1)**2*2**k+1
        for i,layer in enumerate(layers):
            x=layer[0]
            a=sum(p[0]==x for p in paths)
            b=sum(p[0]==x for p,q in pairs)
            expected=((d+1)*2**k,d*(d*d+d+1)*3**k-(d+1)*2**k) if i==0 else ((1,d*(d+1)*2**k-1) if i==k+1 else ((d+1)*2**(k-i),(d+1)*(d*d+d+1)*2**(i-1)*3**(k-i)-(d+1)*2**(k-i)))
            assert (a,b)==expected
result={'small_local_gadget_instances':15,'cycles':sum(n*A**a*B**b for (a,b),n in counts.items()),'trail_count':len(trails),'counts':{str(k):v for k,v in sorted(counts.items())},'checked_external_arcs':len(external),'max_destroyed_external_arc':F,'created_external_arc_lower_bound':G,'strict_margin':G-F,'ratio_approximation':F/G,'vertices':len(V),'arcs':len(E),'explicit_reverse_isomorphism':True,'explicit_all_vertex_deletions_strongly_connected':True}
saved=json.loads(Path(__file__).with_name('certificate.json').read_text())
for key in ('cycles','max_destroyed_external_arc','created_external_arc_lower_bound','strict_margin','vertices','arcs'):assert result[key]==saved[key]
print(json.dumps(result,indent=2))
