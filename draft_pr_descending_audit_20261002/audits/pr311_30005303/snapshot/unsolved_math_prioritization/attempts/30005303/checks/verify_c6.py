#!/usr/bin/env python3
"""Exact, exhaustive checks for the six-cycle distribution. Standard library only."""
from itertools import product, combinations
from collections import Counter
import json
V=range(6)
E=[(i,(i+1)%6) for i in V]
X=list(product((0,1),repeat=6))
W={x:(1+int(all(x))) if x[0]==x[1] and x[2]==x[3] and x[4]==x[5] else 0 for x in X}
S=[x for x in X if W[x]]
counts=Counter()
assert sum(W.values())==9 and len(S)==8
counts['normalization_support']=2
for x,y in product(X,repeat=2):
    lo=tuple(min(a,b) for a,b in zip(x,y)); hi=tuple(max(a,b) for a,b in zip(x,y))
    assert W[lo]*W[hi]>=W[x]*W[y]
    counts['MTP2_pairs']+=1
for labels in product(range(4), repeat=6):
    A=tuple(i for i in V if labels[i]==0); B=tuple(i for i in V if labels[i]==1); C=tuple(i for i in V if labels[i]==2)
    if not A or not B: continue
    reached=set(A); stack=list(A)
    while stack:
        u=stack.pop()
        for v in ((u-1)%6,(u+1)%6):
            if v not in C and v not in reached: reached.add(v); stack.append(v)
    if reached.intersection(B): continue
    counts['separations']+=1
    ac=Counter();bc=Counter();cc=Counter();abc=Counter()
    for x in X:
        a=tuple(x[i] for i in A);b=tuple(x[i] for i in B);c=tuple(x[i] for i in C)
        ac[a,c]+=W[x];bc[b,c]+=W[x];cc[c]+=W[x];abc[a,b,c]+=W[x]
    for a,b,c in product(product((0,1),repeat=len(A)),product((0,1),repeat=len(B)),product((0,1),repeat=len(C))):
        assert abc[a,b,c]*cc[c]==ac[a,c]*bc[b,c]
        counts['CI_equalities']+=1
# Cubic contrast on the three equality blocks, written on six-variable probabilities.
embed=lambda z:tuple(t for b in z for t in (b,b))
even=[embed(z) for z in product((0,1),repeat=3) if sum(z)%2==0]
odd=[embed(z) for z in product((0,1),repeat=3) if sum(z)%2==1]
for clique in [()] + [(i,) for i in V] + E:
    assert Counter(tuple(x[i] for i in clique) for x in even)==Counter(tuple(x[i] for i in clique) for x in odd)
    counts['clique_exponent_balances']+=1
mul=lambda xs:__import__('math').prod(W[x] for x in xs)
assert mul(even)==1 and mul(odd)==2
counts['nonfactorization_witness']=1
print(json.dumps({'status':'PASS','assertions':sum(v for k,v in counts.items() if k!='separations'),'counts':dict(counts),'weights_on_support':{''.join(map(str,x)):W[x] for x in S},'toric_products_unnormalized':[mul(even),mul(odd)]},indent=2,sort_keys=True))
