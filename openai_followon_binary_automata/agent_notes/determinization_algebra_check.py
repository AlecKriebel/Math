#!/usr/bin/env python3
"""Independent tiny Brauer-algebra falsification checks; no asymptotic claims."""
from functools import lru_cache
from itertools import combinations
import json

@lru_cache(None)
def pairings(m):
    def rec(vertices):
        if not vertices:
            yield ()
            return
        x,*tail = vertices
        for y in tail:
            rest=[z for z in tail if z != y]
            for pairs in rec(rest):
                yield ((x,y),)+pairs
    result=[]
    for pairs in rec(list(range(2*m))):
        mates=[None]*(2*m)
        for x,y in pairs: mates[x]=y; mates[y]=x
        result.append(tuple(mates))
    return tuple(result)

def identity(m): return tuple(range(m,2*m))+tuple(range(m))
def rank(a):
    m=len(a)//2
    return sum(a[x]>=m for x in range(m))
def support(a):
    m=len(a)//2
    return frozenset(x for x in range(m) if a[x] != m+x)

@lru_cache(None)
def mul(a,b):
    m=len(a)//2
    assert len(a)==len(b)
    adjacency=[[] for _ in range(3*m)]
    def add(x,y): adjacency[x].append(y); adjacency[y].append(x)
    for x,y in enumerate(a):
        if x<y: add(x,y)
    for x,y in enumerate(b):
        if x<y: add(m+x,m+y)
    answer=[None]*(2*m)
    outer=list(range(m))+list(range(2*m,3*m))
    for x in outer:
        prev=None; current=x
        while True:
            nxt=next(z for z in adjacency[current] if z != prev)
            if nxt in outer:
                ix=x if x<m else x-m
                iy=nxt if nxt<m else nxt-m
                answer[ix]=iy
                break
            prev,current=current,nxt
    return tuple(answer)

def reduce(e,z):
    m=len(e)//2
    X=[x for x in range(m) if e[x]>=m]
    p={x:e[x]-m for x in X}
    r=len(X)
    ports=X+[m+p[x] for x in X]
    index={v:i for i,v in enumerate(ports)}
    assert all(z[v] in index for v in ports)
    return tuple(index[z[v]] for v in ports)

def check(max_degree=4):
    report=[]
    for m in range(max_degree+1):
        diagrams=pairings(m)
        idem=[e for e in diagrams if mul(e,e)==e]
        count=0; common_count=0
        for e in idem:
            r=rank(e)
            assert len(support(e))<=2*(m-r),('idempotent-support',m,e)
            corner={mul(mul(e,a),e) for a in diagrams}
            reduced={z:reduce(e,z) for z in corner}
            assert reduced[e]==identity(r)
            assert len(set(reduced.values()))==len(corner)
            for z in corner:
                assert rank(reduced[z])==rank(z)
                for w in corner:
                    assert reduced[mul(z,w)]==mul(reduced[z],reduced[w]),('corner-hom',m,e,z,w)
                    count+=1
            for size in range(m+1):
                for J_tuple in combinations(range(m),size):
                    J=frozenset(J_tuple)
                    family=[a for a in diagrams if support(a)<=J]
                    K=frozenset().union(*(support(reduce(e,mul(mul(e,a),e))) for a in family))
                    assert len(K)<=len(J),('common-support',m,e,J,K)
                    common_count+=len(family)
        report.append({'degree':m,'diagrams':len(diagrams),'idempotents':len(idem),
                       'corner_products_checked':count,'sandwiches_checked':common_count})
    return report

if __name__=='__main__':
    print(json.dumps({'status':'PASS','checks':check()},indent=2))
