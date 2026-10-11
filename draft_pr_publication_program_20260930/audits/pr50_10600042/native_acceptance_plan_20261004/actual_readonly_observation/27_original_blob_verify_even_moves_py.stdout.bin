#!/usr/bin/env python3
"""Exact word-level diagnostics for the even-strand Markov formulation.
No knot-equivalence oracle or braid word-problem solver is used.
The completeness proof and the established Markov theorems are external
mathematical inputs. This script checks their stated edge conversion.
"""
from collections import Counter
from dataclasses import dataclass
import json
import random

assertions=0
coverage=Counter()
def check(ok,label):
    global assertions
    assert ok,label
    assertions+=1

def sigma(i,sign=1):return (('s',i,sign),)
def virt(i):return (('v',i,1),)
def inverse(w):return tuple((t,i,-e if t=='s' else 1) for t,i,e in reversed(w))
def shift(w):return tuple((t,i+1,e) for t,i,e in w)
@dataclass(frozen=True)
class Braid:
    n:int
    w:tuple

def valid(b,virtual=True):
    return b.n>=1 and all(1<=i<b.n and e in [-1,1] and
        (t=='s' or (virtual and t=='v' and e==1)) for t,i,e in b.w)
def pad(b):
    return b if b.n%2==0 else Braid(b.n+1,b.w+sigma(b.n))
def components(b):
    labels=list(range(b.n))
    for _,i,_ in b.w:labels[i-1],labels[i]=labels[i],labels[i-1]
    seen=set();count=0
    for i in range(b.n):
        if i in seen:continue
        count+=1
        while i not in seen:seen.add(i);i=labels[i]
    return count

# Explicit even endpoint patterns, separate from the unrestricted generator.
def pattern(name,N,a,b,g=()):
    if name=='C':out=(Braid(N,b),Braid(N,a+b+inverse(a)))
    elif name=='BC':out=(Braid(N,b+sigma(N-1)),Braid(N,a+b+inverse(a)+sigma(N-1)))
    elif name=='T':out=(Braid(N,b+sigma(N-1)),Braid(N,b+g))
    elif name=='D':out=(Braid(N,b),Braid(N+2,b+g+sigma(N+1)))
    elif name=='R':out=(Braid(N,a+sigma(N-1,-1)+b+sigma(N-1)),Braid(N,a+virt(N-1)+b+virt(N-1)))
    elif name=='L':out=(Braid(N,shift(a)+sigma(1,-1)+shift(b)+sigma(1)),Braid(N,shift(a)+virt(1)+shift(b)+virt(1)))
    elif name=='BR':out=(Braid(N,a+sigma(N-2,-1)+b+sigma(N-2)+sigma(N-1)),Braid(N,a+virt(N-2)+b+virt(N-2)+sigma(N-1)))
    elif name=='BL':out=(Braid(N,shift(a)+sigma(1,-1)+shift(b)+sigma(1)+sigma(N-1)),Braid(N,shift(a)+virt(1)+shift(b)+virt(1)+sigma(N-1)))
    else:raise ValueError(name)
    limits={'C':N-1,'BC':N-2,'T':N-2,'D':N-1,'R':N-2,'L':N-2,'BR':N-3,'BL':N-3}
    check(N%2==0 and N>=2,'even pattern tag')
    check(all(i<=limits[name] for _,i,_ in a+b),'block support')
    if name in ['BR','BL']:check(N>=4,'buffered exchange minimum')
    return out

# Unrestricted classical/virtual Markov edges.
def original(kind,n,a,b,g=()):
    if kind=='conjugation':return (Braid(n,b),Braid(n,a+b+inverse(a)))
    if kind=='stabilization':return (Braid(n,b),Braid(n+1,b+g))
    # n is the TOTAL strand count for exchanges.
    if kind=='right_exchange':return (Braid(n,a+sigma(n-1,-1)+b+sigma(n-1)),Braid(n,a+virt(n-1)+b+virt(n-1)))
    if kind=='left_exchange':return (Braid(n,shift(a)+sigma(1,-1)+shift(b)+sigma(1)),Braid(n,shift(a)+virt(1)+shift(b)+virt(1)))
    raise ValueError(kind)

def test_edge(kind,n,a,b,g=(),virtual=True):
    old=original(kind,n,a,b,g)
    check(all(valid(x,virtual) for x in old),'original words valid')
    new=tuple(map(pad,old))
    if kind=='conjugation':name='C' if n%2==0 else 'BC';N=n+n%2
    elif kind=='stabilization':name='D' if n%2==0 else 'T';N=n+n%2
    elif kind=='right_exchange':name='R' if n%2==0 else 'BR';N=n+n%2
    elif kind=='left_exchange':name='L' if n%2==0 else 'BL';N=n+n%2
    expected=pattern(name,N,a,b,g)
    check(new==expected,'literal endpoint match')
    check(new[::-1]==expected[::-1],'inverse endpoint match')
    check(all(x.n%2==0 and valid(x,virtual) for x in new),'valid even endpoints')
    check(components(old[0])==components(old[1]),'original closure component count')
    check(all(components(x)==components(pad(x)) for x in old),'padding component count')
    check(max(x.n for x in new)==2*((max(x.n for x in old)+1)//2),'height rounding')
    coverage[('virtual_' if virtual else 'classical_')+name]+=1

rng=random.Random(10600042)
def word(k,virtual,length):
    if k<=0:return ()
    alphabet=[('s',i,e) for i in range(1,k+1) for e in [-1,1]]
    if virtual:alphabet += [('v',i,1) for i in range(1,k+1)]
    return tuple(rng.choice(alphabet) for _ in range(length))
for virtual in [False,True]:
    for n in range(1,9):
        for length in [0,1,3,6]:
            a=word(n-1,virtual,length);b=word(n-1,virtual,6-length)
            test_edge('conjugation',n,a,b,virtual=virtual)
            gs=[sigma(n),sigma(n,-1)]+([virt(n)] if virtual else [])
            for g in gs:test_edge('stabilization',n,(),b,g,virtual)
            if virtual and n>=2:
                a=word(n-2,True,length);b=word(n-2,True,6-length)
                for kind in ['right_exchange','left_exchange']:test_edge(kind,n,a,b,virtual=True)

# Braid relation lifts at both parities, with explicit valid contexts.
relation_cases=0
for n in range(2,9):
    pairs=[]
    for i in range(1,n):
        pairs += [(sigma(i)+sigma(i,-1),()),(virt(i)+virt(i),())]
    for i in range(1,n-1):
        pairs += [(sigma(i)+sigma(i+1)+sigma(i),sigma(i+1)+sigma(i)+sigma(i+1)),
                  (virt(i)+virt(i+1)+virt(i),virt(i+1)+virt(i)+virt(i+1)),
                  (sigma(i)+virt(i+1)+virt(i),virt(i+1)+virt(i)+sigma(i+1))]
    for i in range(1,n):
        for j in range(i+2,n):
            pairs += [(sigma(i)+sigma(j),sigma(j)+sigma(i)),
                      (virt(i)+virt(j),virt(j)+virt(i)),
                      (sigma(i)+virt(j),virt(j)+sigma(i))]
    for lhs,rhs in pairs:
        pre=word(n-1,True,2);post=word(n-1,True,2)
        old=(Braid(n,pre+lhs+post),Braid(n,pre+rhs+post))
        new=tuple(map(pad,old));N=n+n%2;tail=sigma(n) if n%2 else ()
        check(new==(Braid(N,pre+lhs+post+tail),Braid(N,pre+rhs+post+tail)),'relation in retained context')
        check(all(valid(x) and x.n%2==0 for x in new),'relation even support')
        check(components(new[0])==components(new[1]),'relation permutations')
        relation_cases+=1
check(set(coverage)=={'classical_'+x for x in ['C','BC','T','D']}|{'virtual_'+x for x in ['C','BC','T','D','R','L','BR','BL']},'all families covered')
check(pad(Braid(1,()))==Braid(2,sigma(1)),'one-strand unknot endpoint')
check(components(Braid(2,()))==2 and components(Braid(4,()))==4,'strand tags cannot be erased')
print(json.dumps({'status':'PASS','exact_assertions':assertions,'edge_cases':sum(coverage.values()),
    'relation_cases':relation_cases,'coverage':dict(sorted(coverage.items())),
    'boundary_checks':['one-strand representative lifts to two','even tags retained',
       'both virtual exchange directions and both parities','positive negative virtual stabilization'],
    'limits':['Finite diagnostics, not formal verification','No link-equivalence oracle',
       'No braid word-problem solver','No novelty claim']},indent=2))
