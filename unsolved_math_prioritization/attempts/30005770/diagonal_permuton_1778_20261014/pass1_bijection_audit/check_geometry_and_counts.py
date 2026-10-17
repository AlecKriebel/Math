#!/usr/bin/env python3
"""Independent finite regression checks; not an asymptotic proof."""
from collections import Counter
from functools import lru_cache
from itertools import permutations, combinations
from fractions import Fraction
from math import factorial
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

@lru_cache(None)
def comps(n):
    if n == 0:
        return ((),)
    return tuple((k,) + rest for k in range(1,n+1) for rest in comps(n-k))

@lru_cache(None)
def shapes(n):
    if n == 1: return ((),)
    ans=[]
    def products(ns, children=()):
        if not ns:
            ans.append(children); return
        for t in shapes(ns[0]): products(ns[1:], children+(t,))
    for ns in comps(n-1): products(ns)
    return tuple(ans)

def conv(a,b):
    c=Counter()
    for x,v in a.items():
        for y,w in b.items(): c[x+y]+=v*w
    return c

@lru_cache(None)
def general_labels(t):
    if not t: return ((0,1),)
    sums=Counter({0:1})
    for child in t: sums=conv(sums,dict(general_labels(child)))
    ans=Counter()
    for s,c in sums.items():
        for l in range(s+2): ans[l]+=c
    return tuple(sorted(ans.items()))

@lru_cache(None)
def proper_labels(t):
    if not t: return ((0,1),)
    sums=Counter({0:1})
    for child in t: sums=conv(sums,dict(general_labels(child)))
    return tuple(sorted(sums.items()))

def height(t): return 0 if not t else 1+max(map(height,t))

def standard(p):
    ranks={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(ranks[v] for v in p)

def blocks(p):
    ans=[]; prev=0;n=len(p);mini=n+1
    for i,v in enumerate(p,1):
        mini=min(mini,v)
        if mini==n-i+1:
            ans.append(standard(p[prev:i]));prev=i
    if prev!=n: raise RuntimeError('Incomplete skew decomposition')
    return ans

def normalize(p):
    mins=[];curr=len(p)+1
    for i,v in enumerate(p):
        if v<curr: mins.append((i,v));curr=v
    md=dict(mins);unused=set(p);q=[];curr=None
    for i in range(len(p)):
        if i in md: v=md[i];curr=v
        else: v=min(v for v in unused if v>curr)
        q.append(v);unused.remove(v)
    return tuple(q)

def tree(q):
    n=len(q)
    if q[-1]!=n: raise RuntimeError('Normalized skew block does not end at maximum')
    if n==1:return ()
    return tuple(tree(b) for b in blocks(q[:-1]))

def avoids1342(p):
    return not any(p[a]<p[d]<p[b]<p[c] for a,b,c,d in combinations(range(len(p)),4))

rows=[]
for n in range(1,9):
    trees=shapes(n)
    counts=sum(sum(dict(proper_labels(t)).values()) for t in trees)
    exact=1 if n==1 else 3*2**(n-2)*factorial(2*n-2)//(factorial(n+1)*factorial(n-1))
    if counts!=exact:raise RuntimeError(('tree count',n,counts,exact))
    byheight=Counter()
    relaxed=Fraction(0)
    for t in trees:
        byheight[height(t)]+=sum(dict(proper_labels(t)).values())
        relaxed+=sum(Fraction(c)*Fraction(3,2)**l for l,c in general_labels(t))
    rows.append({'n':n,'plane_shapes':len(trees),'proper_labeled_trees':counts,
                 'height_counts':dict(sorted(byheight.items())),
                 'relaxed_root_weighted_u_3_over_2':str(relaxed)})

geom=[]
for n in range(1,8):
    avoider_count=0; indecomp_count=0
    for p in permutations(range(1,n+1)):
        if not avoids1342(p): continue
        avoider_count+=1
        bs=blocks(p)
        if len(bs)==1: indecomp_count+=1
        hs=[]
        for b in bs:
            q=normalize(b);t=tree(q);h=height(t);hs.append(h)
            # The deterministic one-sided bound is what the proof needs.
            if min(i+v for i,v in enumerate(b,1))<len(b)+1-h:
                raise RuntimeError(('block geometry',p,b,q,t))
            # Independently validate every vertex identity, including leaves.
            def walk(t, depth=0):
                out=[]
                for child in t:out+=walk(child,depth+1)
                out.append((1+sum(size(c) for c in t),depth))
                return out
            def size(t):return 1+sum(size(c) for c in t)
            for i,((sv,d),v) in enumerate(zip(walk(t),q),1):
                if i+v != len(b)+sv-d:
                    raise RuntimeError(('vertex formula',p,b,q,t,i,sv,d,v))
        if min(i+v for i,v in enumerate(p,1))<n+1-max(hs):
            raise RuntimeError(('forest geometry',p,hs))
    if indecomp_count!=rows[n-1]['proper_labeled_trees']:
        raise RuntimeError(('indecomposable count',n,indecomp_count))
    geom.append({'n':n,'all_1342_avoiders_checked':avoider_count,'skew_indecomposable':indecomp_count})

result={'purpose':'Finite independent regression checks, not asymptotic proof',
        'tree_counts':rows,'geometry_checks':geom,'all_checks_passed':True}
(OUT/'finite_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
