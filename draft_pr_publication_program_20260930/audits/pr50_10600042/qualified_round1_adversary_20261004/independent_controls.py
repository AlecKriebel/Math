"""Distinct adversary implementation: modular linear algebra and union-find.
Does not import or copy the portable checker. Finite necessary invariants only.
"""
from itertools import product, permutations
from collections import Counter
import json

def words(k, virtual):
    alphabet=[(i,e) for i in range(1,k+1) for e in (-1,1)]
    if virtual: alphabet += [(i,0) for i in range(1,k+1)]
    return [()] + [tuple(w) for length in (1,2) for w in product(alphabet,repeat=length)]

def inverse(w): return tuple((i,-e) for i,e in w[::-1])
def inc(w): return tuple((i+1,e) for i,e in w)

def fox_nullity(n, w):
    mat=[[int(i==j) for j in range(n)] for i in range(n)]
    for index,e in w:
        assert e in (-1,1) and 1 <= index < n
        a,b=mat[index-1][:],mat[index][:]
        if e==1: mat[index-1]=[(2*x-y)%3 for x,y in zip(a,b)]; mat[index]=a
        else: mat[index-1]=b;mat[index]=[(2*y-x)%3 for x,y in zip(a,b)]
    mat=[[(x-int(i==j))%3 for j,x in enumerate(row)] for i,row in enumerate(mat)]
    pivot=0
    for column in range(n):
        found=next((j for j in range(pivot,n) if mat[j][column]),None)
        if found is None: continue
        mat[pivot],mat[found]=mat[found],mat[pivot]
        mul=pow(mat[pivot][column],-1,3)
        mat[pivot]=[(x*mul)%3 for x in mat[pivot]]
        for j in range(n):
            if j==pivot: continue
            mul=mat[j][column]
            mat[j]=[(x-mul*y)%3 for x,y in zip(mat[j],mat[pivot])]
        pivot+=1
    return n-pivot

def canonical_crossings(n,w):
    labels=list(range(n)); events=[]; parent=list(range(n))
    def root(i):
        while parent[i]!=i: i=parent[i]
        return i
    for index,e in w:
        assert 1 <= index < n and e in (-1,0,1)
        i=index-1; a,b=labels[i],labels[i+1]
        if e: events.append((a,b,e) if e>0 else (b,a,e))
        labels[i:i+2]=[b,a]
    for i,label in enumerate(labels): parent[root(i)]=root(label)
    reps=sorted({root(i) for i in range(n)}); groups={r:j for j,r in enumerate(reps)}
    k=len(reps);matrix=[[0]*k for _ in range(k)]
    for over,under,e in events:
        a,b=groups[root(over)],groups[root(under)]
        if a!=b:matrix[a][b]+=e
    signature=min(tuple(matrix[p[i]][p[j]] for i in range(k) for j in range(k)) for p in permutations(range(k)))
    return k,signature

checks=Counter()
def check(kind,n,x,y,virtual):
    if virtual: assert canonical_crossings(n,x)==canonical_crossings(n,y),(kind,n,x,y)
    else: assert fox_nullity(n,x)==fox_nullity(n,y),(kind,n,x,y)
    checks[('virtual_' if virtual else 'classical_')+kind]+=1

for n in (2,4):
    for virtual in (False,True):
        for a in words(n-1,virtual):
            for b in words(n-1,virtual): check('C',n,b,a+b+inverse(a),virtual)
        for a in words(n-2,virtual):
            for b in words(n-2,virtual): check('BC',n,b+((n-1,1),),a+b+inverse(a)+((n-1,1),),virtual)
        for b in words(n-2,virtual):
            for e in (-1,1,0) if virtual else (-1,1):
                check('T',n,b+((n-1,1),),b+((n-1,e),),virtual)
        for b in words(n-1,virtual):
            for e in (-1,1,0) if virtual else (-1,1):
                if virtual:
                    assert canonical_crossings(n,b)==canonical_crossings(n+2,b+((n,e),(n+1,1)))
                else: assert fox_nullity(n,b)==fox_nullity(n+2,b+((n,e),(n+1,1)))
                checks[('virtual_' if virtual else 'classical_')+'D']+=1
    for a in words(n-2,True):
        for b in words(n-2,True):
            check('R',n,a+((n-1,-1),)+b+((n-1,1),),a+((n-1,0),)+b+((n-1,0),),True)
            check('L',n,inc(a)+((1,-1),)+inc(b)+((1,1),),inc(a)+((1,0),)+inc(b)+((1,0),),True)
    if n>=4:
        for a in words(n-3,True):
            for b in words(n-3,True):
                tail=((n-1,1),)
                check('BR',n,a+((n-2,-1),)+b+((n-2,1),)+tail,a+((n-2,0),)+b+((n-2,0),)+tail,True)
                check('BL',n,inc(a)+((1,-1),)+inc(b)+((1,1),)+tail,inc(a)+((1,0),)+inc(b)+((1,0),)+tail,True)

assert 3**fox_nullity(2,((1,1),)*3)==9
assert 3**fox_nullity(2,((1,1),))==3
assert canonical_crossings(2,((1,1),(1,1)))!=canonical_crossings(2,((1,1),(1,0),(1,1),(1,0)))
assert canonical_crossings(4,((1,1),(1,-1),(1,1),(1,1)))!=canonical_crossings(4,((1,1),(1,0),(1,1),(1,0)))
print(json.dumps({'status':'PASS_DISTINCT_BOUNDED_NECESSARY_INVARIANT_CONTROLS','checks':sum(checks.values()),
 'coverage':dict(sorted(checks.items())),'classical_method':'rank over F3 of coloring monodromy minus identity',
 'virtual_method':'strand event tracing, union-find closure, ordered matrices canonicalized under all relabelings',
 'independent_of_portable_checker':True,'maximum_unshifted_block_length':2,'initial_even_levels':[2,4],
 'limits':'Necessary invariants are not sufficient for closure equivalence; universal proof and imported theorems remain essential'},indent=2))
