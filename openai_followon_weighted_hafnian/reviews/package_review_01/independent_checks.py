"""Independent package-review checks; never mutate the reviewed payload."""
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib, json, random, sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'reviews/package_review_01/extracted/code'))
from gadget import integer_gadget, expand_rational_matrix
from sampling import Graph, sample_perfect_matching, Stats

def pm(vertices, edges):
    adj={v:set() for v in vertices}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    @lru_cache(None)
    def rec(rem):
        if not rem: return ((),)
        if len(rem)%2: return ()
        a=rem[0]; rest=set(rem[1:]); ans=[]
        for b in sorted(adj[a]&rest):
            for tail in rec(tuple(sorted(rest-{b}))):
                ans.append(tuple(sorted(((min(a,b),max(a,b)),*tail))))
        return tuple(ans)
    return rec(tuple(sorted(vertices)))

def bipartite_permanent(vertices, edges):
    vertices=set(vertices); adj={v:set() for v in vertices}
    for a,b in edges:
        if a in vertices and b in vertices: adj[a].add(b); adj[b].add(a)
    colors={}
    for v in sorted(vertices):
        if v in colors: continue
        colors[v]=0; todo=deque([v])
        while todo:
            a=todo.popleft()
            for b in adj[a]:
                if b in colors: assert colors[b]!=colors[a]
                else: colors[b]=1-colors[a]; todo.append(b)
    left=[v for v in vertices if colors[v]==0]; right=[v for v in vertices if colors[v]==1]
    if len(left)!=len(right): return 0
    pos={v:i for i,v in enumerate(right)}
    left.sort(key=lambda v:len(adj[v]))
    @lru_cache(None)
    def dp(i,used):
        if i==len(left): return 1
        return sum(dp(i+1,used|(1<<pos[v])) for v in adj[left[i]] if not used&(1<<pos[v]))
    return dp(0,0)

signatures=[]
for w in range(1,129):
    g=integer_gadget(w).graph
    sig=[bipartite_permanent(set(range(g.order))-set(rem),g.edges) for rem in [(),(0,1),(0,),(1,)]]
    assert sig==[w,1,0,0],(w,sig)
    signatures.append({'W':w,'signature':sig})

rng=random.Random(79301); pairs=list(combinations(range(4),2)); matrix_cases=[]
for trial in range(50):
    vals=[Fraction(rng.randrange(4),rng.choice([1,1,2,3])) for _ in pairs]
    mat=[[0]*4 for _ in range(4)]
    for (a,b),v in zip(pairs,vals): mat[a][b]=mat[b][a]=v
    e=expand_rational_matrix(mat)
    # Original answer is the explicit three-pairing formula, independent of any recursion.
    z=mat[0][1]*mat[2][3]+mat[0][2]*mat[1][3]+mat[0][3]*mat[1][2]
    # Independent minimum-label subset recurrence, without candidate counting helpers.
    adj=[set() for _ in range(e.graph.order)]
    for a,b in e.graph.edges: adj[a].add(b); adj[b].add(a)
    @lru_cache(None)
    def count(rem):
        if not rem: return 1
        a=rem[0]; rest=set(rem[1:])
        return sum(count(tuple(sorted(rest-{b}))) for b in adj[a]&rest)
    c=count(tuple(range(e.graph.order)))
    assert c==z*e.denominator**2,(trial,vals,c,z)
    matrix_cases.append({'weights':[str(v) for v in vals],'hafnian':str(z),'expanded_count':c})

sampler=[]
for n in (4,6):
    vertices=tuple(range(n)); edges=tuple(combinations(vertices,2)); g=Graph.make(vertices,edges)
    exact=pm(vertices,edges); k=n//2; b=(4*k*k*2-1).bit_length(); R=1<<b
    # Fixed eta=1/2 and complete n=6 can use at most two categorical draws.
    law=Counter(); trials=0
    def witness(x):
        out=pm(x.vertices,x.edges); return out[0] if out else None
    def countoracle(x,a,d): return Fraction(len(pm(x.vertices,x.edges)))
    for bits in product(range(R),repeat=k-1):
        draw=iter(bits); stats=Stats()
        out=sample_perfect_matching(g,Fraction(1,2),countoracle,witness,lambda _:next(draw),stats)
        assert out in exact and stats.count_calls<=k*k and stats.witness_calls<=k*k+1
        law[out]+=1; trials+=1
    tv=sum(abs(Fraction(law[m],trials)-Fraction(1,len(exact))) for m in exact)/2
    assert tv<Fraction(1,2)
    sampler.append({'vertices':n,'draw_sequences':trials,'TV':str(tv),'matching_count':len(exact)})

report={'status':'passed','scope':'independent bipartite permanents, global closed-form hafnians, executed finite-bit sampler laws; no upstream FPRAS implementation','signatures':signatures,'independent_rational_K4':matrix_cases,'executed_sampler_laws':sampler}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'passed','signatures':len(signatures),'rational_K4':len(matrix_cases),'sampler_laws':sampler}))
