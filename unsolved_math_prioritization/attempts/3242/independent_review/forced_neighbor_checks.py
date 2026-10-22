"""Independently build canonical forced-neighbor completions from Turn5."""
from itertools import combinations
from collections import Counter
import json

C=Counter();maxima={}
def graph(n,edges):
    a=[set() for _ in range(n)]
    for u,v in edges:a[u].add(v);a[v].add(u)
    return a
def inspect(label,n,edges,parts):
    a=graph(n,edges);degree=[len(x) for x in a];w=len(set(degree))
    assert all(not(a[u]&set(part)) for part in parts for u in part)
    assert w<n-2,(label,degree)
    C[label]+=1;maxima[label]=max(maxima.get(label,0),w)
for c in (5,6,7):
    n=c+6;A=[0,1];B=[2,3,4,5];Cs=list(range(6,n))
    # v=0 universal outsideA, u=1 misses low z=3, saturated b*=2,
    # low b0=4 has exactlyA neighbors; only B5-to-C remains free.
    fixed=[(0,v) for v in B+Cs]+[(1,v) for v in B+Cs if v!=3]+[(2,v) for v in Cs]
    for mask in range(1<<c):
        edges=fixed+[(5,v) for j,v in enumerate(Cs) if mask>>j&1]
        inspect('B4_C'+str(c),n,edges,[A,B,Cs])

n=11;A=[0,1];B=[2,3,4];Cs=list(range(5,11))
base=[(0,v) for v in B+Cs]+[(2,1)]+[(2,v) for v in Cs]
# SaturatedB case with lowu: the two remainingB vertices have arbitraryC edges.
free=[(b,v) for b in (3,4) for v in Cs]
for mask in range(1<<len(free)):
    inspect('B3_saturated_low_u',n,base+[e for j,e in enumerate(free) if mask>>j&1],[A,B,Cs])
# SaturatedB case with lowB3: u-to-C,B4-to-C,and u-to-B4 remain free.
free=[(1,v) for v in Cs]+[(4,v) for v in Cs]+[(1,4)]
for mask in range(1<<len(free)):
    inspect('B3_saturated_low_B',n,base+[e for j,e in enumerate(free) if mask>>j&1],[A,B,Cs])
# NonsaturatedB, z=B4: B2 andB3 have degrees6 and7, hence4 and5C neighbors.
base=[(0,v) for v in B+Cs]+[(1,v) for v in B+Cs if v!=4]
for s6 in combinations(Cs,4):
    for s7 in combinations(Cs,5):inspect('B3_nonsaturated_zB',n,base+[(2,v) for v in s6]+[(3,v) for v in s7],[A,B,Cs])
# NonsaturatedB,z=C5: B3 hits all otherC, B2 hits four of them;B4 onlyA.
base=[(0,v) for v in B+Cs]+[(1,v) for v in B+Cs if v!=5]+[(3,v) for v in Cs if v!=5]
for s6 in combinations(Cs[1:],4):inspect('B3_nonsaturated_zC',n,base+[(2,v) for v in s6],[A,B,Cs])
print(json.dumps({'status':'PASS','canonical_graph_completions':sum(C.values()),'counts':dict(C),'maximum_degree_varieties':maxima,
 'scope':'Independent finite completions only after the written forced-neighbor reductions; not a full graph enumeration above6 and not a proof of the unrestricted conjecture.'},indent=2,sort_keys=True))
