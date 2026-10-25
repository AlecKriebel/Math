"""Independent finite controls; no published checker or archived review imported.
Exhaustive arbitrary-edit weighted repairs for all 3-colorable tails of order <=4;
full edge-pattern cover check for H=K3; and a triangle-free 4-chromatic boundary.
"""
from itertools import combinations,product
from fractions import Fraction
from pathlib import Path
from collections import Counter
import hashlib,json
out=Path(__file__).resolve().parent
stats=Counter()

def edges(n):return tuple(combinations(range(n),2))
def frommask(n,mask):return {e for i,e in enumerate(edges(n)) if mask>>i&1}
def colorable(n,E,removed=None):
    vs=[v for v in range(n) if v!=removed]
    neighbors={v:{w for w in vs if tuple(sorted((v,w))) in E} for v in vs}
    colors={}
    def rec():
        if len(colors)==len(vs):return True
        v=max((w for w in vs if w not in colors),key=lambda w:(len({colors[u] for u in neighbors[w] if u in colors}),len(neighbors[w])))
        banned={colors[u] for u in neighbors[v] if u in colors}
        for c in range(3):
            if c not in banned:
                colors[v]=c
                if rec():return True
                del colors[v]
        return False
    return rec()
def tri(n,E):return [frozenset(combinations(t,2)) for t in combinations(range(n),3) if all(e in E for e in combinations(t,2))]
def P(n,E):
    if any(all(e in E for e in combinations(q,2)) for q in combinations(range(n),4)):return False
    return colorable(n,E) or any(colorable(n,E,v) for v in range(n))
def mindel(n,E):
    ee=tuple(E)
    for k in range(len(ee)+1):
        for remove in combinations(ee,k):
            if not tri(n,E-set(remove)):return k

for n in range(1,5):
    ps=edges(n+1)
    targets=[frommask(n+1,m) for m in range(1<<len(ps)) if P(n+1,frommask(n+1,m))]
    for mask in range(1<<len(edges(n))):
        H=frommask(n,mask)
        if not colorable(n,H):continue
        J=H|{(i,n) for i in range(n)}
        costs=[sum(n if n in e else 1 for e in J^F) for F in targets]
        optimum=min(costs)
        t=mindel(n,H)
        assert optimum==t
        assert Fraction(optimum,4*n*n)==Fraction(t,n*n)/4
        stats['3_colorable_tail_cases']+=1
        stats['arbitrary_target_repairs_considered']+=len(targets)
        if tri(n,H):stats['positive_distance_cases']+=1
# Brute force every retained-edge subset of tripartite cover of K3.
n=3; H=set(edges(n)); L={tuple(sorted((i*n+u,j*n+v))) for i in range(3) for j in range(i+1,3) for u,v in H for u,v in ((u,v),(v,u))}
le=tuple(sorted(L));alltri=tri(9,L);masks=[sum(1<<le.index(e) for e in t) for t in alltri]
best=len(le);repair_count=0
for mask in range(1<<len(le)):
    if any(mask&t==t for t in masks):continue
    kept={le[i] for i in range(len(le)) if mask>>i&1}
    removed=L-kept;proj={tuple(sorted((u%n,v%n))) for u,v in removed}
    assert len(proj)<=len(removed) and not tri(3,H-proj)
    best=min(best,len(removed));repair_count+=1
assert best>=1
stats['K3_cover_triangle_free_deletion_repairs']=repair_count
stats['K3_cover_exact_min_deletions']=best
# Mycielski(C5): triangle-free, but not 3-colorable. It shows the heavy-apex
# equality cannot be extended to an arbitrary non-3-colorable tail.
cycle={tuple(sorted((i,(i+1)%5))) for i in range(5)}
M=set(cycle)
for u,v in cycle:M.add(tuple(sorted((u,v+5))));M.add(tuple(sorted((v,u+5))))
M|={(i+5,10) for i in range(5)}
assert not tri(11,M) and not colorable(11,M)
JM=M|{(i,11) for i in range(11)}
assert not P(12,JM)
# Its right-hand triangle distance is zero; the finite positive-weight graph
# is not P, so its weighted distance is positive. This rejects omitted premise.
stats['non3colorable_tail_negative_control']=1
# Two disjoint obstructions are necessary: sharing the exceptional apex lets
# one deletion erase both coloring violations.
wheel={(0,i) for i in range(1,6)}|{tuple(sorted((i,1+i%5))) for i in range(1,6)}
shared=wheel|{tuple(sorted((u+5 if u else 0,v+5 if v else 0))) for u,v in wheel}
disjoint=wheel|{(u+6,v+6) for u,v in wheel}
assert P(6,wheel) and not colorable(6,wheel)
assert P(11,shared) and not P(12,disjoint)
stats['disjoint_witness_negative_controls']=2
# Explicit rational hard-parameter scaling from the supporting proof.
for d in range(4,101):
    m=2**(d*(d+1));K=2**(d*d-2*d)//d;eps=Fraction(K,1152*m)
    assert Fraction(1,2304*d*2**(3*d))<=eps<=Fraction(1,1152*d*2**(3*d))
    assert Fraction(216*m*m,96*K)>=m
    assert K>0 and m*K>=128 # stronger than 32 log 4
    stats['exact_rational_parameter_cases']+=1
result={'status':'PASS','counts':dict(stats),'scope':__doc__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'negative_controls':['Omitting 3-colorable-tail premise fails for Mycielski(C5).','Two non3colorable witnesses sharing one exceptional vertex do not force failure of P.'],'arithmetic':'Exact integers and fractions; finite exhaustive search.'}
(out/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
