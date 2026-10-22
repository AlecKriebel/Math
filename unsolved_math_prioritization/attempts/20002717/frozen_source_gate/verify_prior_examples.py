#!/usr/bin/env python3
"""Exact finite controls for credited imported examples; no novelty or general proof claim."""
from collections import deque
from itertools import permutations, product
import json

checks = 0

def check(c):
    global checks
    assert c
    checks += 1

def comp(a,b):
    return tuple(a[b[i]] for i in range(3))

E=(0,1,2)
F=list(permutations(range(3)))

def group(n):
    elements=list(product(F,range(n)))
    identity=(E,0)
    def mul(a,b):return (comp(a[0],b[0]),(a[1]+b[1])%n)
    def inv(a):return (tuple(a[0].index(i) for i in range(3)),(-a[1])%n)
    generators={(x,0) for x in F if x!=E}|{(E,1),(E,n-1)}
    return elements,identity,mul,inv,generators


def lattice(vertices,le):
    bad=[]
    for i,a in enumerate(vertices):
        for b in vertices[i:]:
            upper=[x for x in vertices if le(a,x) and le(b,x)]
            lower=[x for x in vertices if le(x,a) and le(x,b)]
            mins=[x for x in upper if all(x==y or not le(y,x) for y in upper)]
            maxs=[x for x in lower if all(x==y or not le(x,y) for y in lower)]
            if len(mins)!=1 or len(maxs)!=1:bad.append((a,b))
    return not bad

positive_intervals=0
for n in range(2,13):
    elems,e,mul,inv,T=group(n)
    check(all(inv(t) in T for t in T))
    check(all(mul(mul(g,t),inv(g)) in T for g in elems for t in T))
    dist={e:0};q=deque([e])
    while q:
        x=q.popleft()
        for t in T:
            y=mul(x,t)
            if y not in dist:dist[y]=dist[x]+1;q.append(y)
    check(len(dist)==len(elems))
    delta=lambda j:min(j%n,(-j)%n)
    for f,j in elems:check(dist[(f,j)]==int(f!=E)+delta(j))
    # Verify the product-order criterion for every ordered pair.
    order={}
    for a in elems:
        for b in elems:
            value=dist[a]+dist[mul(inv(a),b)]==dist[b]
            finite=(int(a[0]!=E)+int(comp(tuple(a[0].index(i) for i in range(3)),b[0])!=E)==int(b[0]!=E))
            cyclic=(delta(a[1])+delta(b[1]-a[1])==delta(b[1]))
            check(value==(finite and cyclic))
            order[a,b]=value
    for g in elems:
        vertices=[x for x in elems if order[x,g]]
        check(lattice(vertices,lambda a,b:order[a,b]))
        positive_intervals+=1

# Z^2: BFS inside a box containing every walk of length <= 3, not an unproved formula.
T2=[x for x in product((-1,0,1),repeat=2) if x!=(0,0)]
d={(0,0):0};q=deque([(0,0)])
while q:
    x=q.popleft()
    if d[x]==3:continue
    for t in T2:
        y=(x[0]+t[0],x[1]+t[1])
        if y not in d:d[y]=d[x]+1;q.append(y)
check(all(k==max(abs(x),abs(y)) for (x,y),k in d.items()))
g=(3,0)
I=sorted(x for x,k in d.items() if (g[0]-x[0],-x[1]) in d and k+d[(g[0]-x[0],-x[1])]==3)
expected=[(0,0),(1,-1),(1,0),(1,1),(2,-1),(2,0),(2,1),(3,0)]
check(I==expected)
def king_le(a,b):
    step=(b[0]-a[0],b[1]-a[1])
    return step in d and d[a]+d[step]==d[b]
a,b,x,y=(1,0),(1,1),(2,0),(2,1)
check(all(king_le(lo,hi) for lo in (a,b) for hi in (x,y)))
check(d[a]==d[b]==1 and d[x]==d[y]==2)
check(not king_le(x,y) and not king_le(y,x))
upper=[u for u in I if king_le(a,u) and king_le(b,u)]
minimal=[u for u in upper if not any(v!=u and king_le(v,u) for v in upper)]
check(set(minimal)=={x,y})
check(not lattice(I,king_le))
print(json.dumps({"status":"PASS_FINITE_REPLAY_OF_CREDITED_EXAMPLES","assertions":checks,"positive_intervals":positive_intervals,"finite_marked_groups":"S3 x C_n, 2 <= n <= 12, coarse finite factor plus axial cycle generators","king_interval":I,"king_common_minimal_upper_bounds":minimal,"scope":"Finite transcription/hypothesis controls only; not an independent proof of all-endpoint or published classification theorems; no new author turn."},indent=2))
