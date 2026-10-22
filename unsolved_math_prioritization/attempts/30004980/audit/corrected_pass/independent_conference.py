#!/usr/bin/env python3
"""Independent conference check including the omitted boundary k=2, Paley(9).
No author imports. Standard library. Writes adjacent audit_conference_results.json.
"""
from itertools import combinations
from pathlib import Path
import json

def require(x):
    if not x:raise RuntimeError('Conference audit assertion failed')

def paley(n):
    if n==9:
        # F_3[t]/(t^2+1); t^2=2. Integer a+3b represents a+b*t.
        def square(x):
            a,b=x%3,x//3
            return (a*a+2*b*b)%3+3*((2*a*b)%3)
        def subtract(x,y):return (x%3-y%3)%3+3*((x//3-y//3)%3)
    else:
        square=lambda x:x*x%n
        subtract=lambda x,y:(x-y)%n
    squares={square(x) for x in range(1,n)}
    return tuple(frozenset(y for y in range(n) if subtract(y,x) in squares) for x in range(n))

def mixed(graph,part,other):
    colors={int(v in graph[u]) for u in part for v in other}
    return len(colors)>1

def check(n):
    a=paley(n); k=(n-1)//4; vertices=set(range(n)); safe_counts=set(); triple_counts={}
    require(all(len(row)==2*k for row in a))
    for u,v in combinations(range(n),2):
        require((v in a[u])==(u in a[v]))
        common=len(a[u]&a[v]);require(common==(k-1 if v in a[u] else k))
        require(len((a[u]^a[v])-{u,v})==2*k)
        first={u,v}; remaining=vertices-first; safe=0
        A=a[u]&a[v]; B=remaining-(a[u]|a[v]); C=(a[u]-a[v])-{u,v}; E=(a[v]-a[u])-{u,v}
        require(sorted([len(A),len(B)])==[k-1,k] and len(C)==len(E)==k)
        for x,y in combinations(sorted(remaining),2):
            second={x,y}; rest=remaining-second
            shared=int(mixed(a,first,second))
            rfirst=shared+sum(mixed(a,first,{z}) for z in rest)
            rsecond=shared+sum(mixed(a,second,{z}) for z in rest)
            # All remaining singleton red degrees are at most 2 <= 2k.
            ok=max(rfirst,rsecond)<=2*k
            bad=(second<=C or second<=E or bool(second&A) and bool(second&B))
            require(ok==not_bad(bad)); safe+=ok
        require(safe==6*k*k-4*k+1);safe_counts.add(safe)
    for triple in combinations(range(n),3):
        t=set(triple); edges=sum(v in a[u] for u,v in combinations(triple,2))
        value=sum(mixed(a,t,{z}) for z in vertices-t)
        require(value==3*k-int(edges in (1,2)))
        if k>=2:require(value>2*k)
        triple_counts[value]=triple_counts.get(value,0)+1
    return {'n':n,'k':k,'safe_counts':sorted(safe_counts),'triple_counts':triple_counts,'passed':True}

def not_bad(bad):return not bad

if __name__=='__main__':
    result=[check(n) for n in (5,9,13,17,29)]
    Path(__file__).with_name('audit_conference_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
