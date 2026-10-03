from pathlib import Path
"""Independent audit: edge-matchings and union components; no release imports."""
from itertools import combinations, permutations
from collections import Counter, defaultdict
from math import lcm, comb
import json,time

def matchings(n,k):
    # Iterate unordered k-subsets of graph edges, then reject shared endpoints.
    edges=list(combinations(range(n),2))
    return [frozenset(m) for m in combinations(edges,k) if len(set(sum((tuple(e) for e in m),())))==2*k]

def color(x,y):
    # Shared edges cancel. The remaining union is a disjoint union of alternating
    # paths/cycles: path v vertices gives a v-cycle; cycle v gives two v/2-cycles.
    unique=x^y
    adj=defaultdict(set)
    for u,v in unique:adj[u].add(v);adj[v].add(u)
    left=set(adj);ans=1
    while left:
        start=next(iter(left));stack=[start];component=set()
        while stack:
            u=stack.pop()
            if u in component:continue
            component.add(u);stack.extend(adj[u]-component)
        left-=component
        cycle=all(len(adj[u])==2 for u in component)
        ans=lcm(ans,len(component)//2 if cycle else len(component))
    return ans

def conjugate(a,x):
    rho={u:v for u,v in a}|{v:u for u,v in a}
    return frozenset(tuple(sorted((rho.get(u,u),rho.get(v,v)))) for u,v in x)

def check(n,k,refine=False):
    start=time.monotonic();D=matchings(n,k);a=D[0];S=[s for s in D if color(a,s)<=2]
    F=defaultdict(list)
    for x in D:
        if color(a,x)>2:F[tuple(color(x,s) for s in S)].append(x)
    hist=dict(sorted(Counter(map(len,F.values())).items()))
    pairgood=all(len(f)==2 and conjugate(a,f[0])==f[1] for f in F.values())
    expected=comb(n,2*k)
    for i in range(1,2*k,2):expected*=i
    assert len(D)==expected and len(set(D))==expected
    r={'degree':n,'k':k,'size':len(D),'commuting':len(S),'raw_fibers':hist,'pairs':pairgood}
    assert all(color(x,x)==1 for x in D)
    assert all(conjugate(a,conjugate(a,x))==x for x in D)
    if refine:
        P=[[s] for s in S]+list(F.values());rounds=0
        # Deliberately use per-cell sorted multisets, not the release count vector.
        while True:
            Q=[]
            for cell in P:
                pieces=defaultdict(list)
                for x in cell:
                    sig=tuple(tuple(sorted(color(x,y) for y in target)) for target in P)
                    pieces[sig].append(x)
                Q+=pieces.values()
            if len(P)==len(Q):break
            P=Q;rounds+=1
        other=[c for c in P if c[0] not in S]
        r.update(refinement_rounds=rounds,stable_fibers=dict(Counter(map(len,other))),refined_pairs=all(len(c)==2 and conjugate(a,c[0])==c[1] for c in other))
        assert all({conjugate(a,x) for x in cell}==set(cell) for cell in P)
    r['seconds']=round(time.monotonic()-start,3)
    print(r,flush=True);return r

if __name__=='__main__':
    result=[check(n,2,True) for n in (5,6,7)]
    result += [check(n,2) for n in range(8,13)]
    result += [check(n,4) for n in (8,9,10)]
    for r in result:
        if r['k']==2 and r['degree']>=8:assert r['pairs']
    assert result[2]['refinement_rounds']==1 and result[2]['stable_fibers']=={2:48}
    assert result[-2]['raw_fibers']=={2:68,4:196}
    assert result[-1]['raw_fibers']=={2:272,4:1032}
    json.dump(result,open(Path(__file__).resolve().parent/'independent_results.json','w'),indent=2)
