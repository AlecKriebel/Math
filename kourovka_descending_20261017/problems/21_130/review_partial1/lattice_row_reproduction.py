#!/usr/bin/env python3
"""Independent row-Hermite collision-cover search without SymPy.

Integer Euclidean row operations preserve the generated lattice. Reduction
above each positive pivot makes its row-Hermite representative canonical.
Only the n-1 difference coordinates are retained. All arithmetic is integer.
"""
from itertools import combinations, permutations
from pathlib import Path
import datetime,json,time,random

HERE=Path(__file__).resolve().parent

def row_hnf(rows,dimension):
    a=[list(r) for r in rows if any(r)];k=0
    for j in range(dimension):
        if k==len(a):break
        nz=[i for i in range(k,len(a)) if a[i][j]]
        if not nz:continue
        p=min(nz,key=lambda i:abs(a[i][j]));a[k],a[p]=a[p],a[k]
        while True:
            for i in range(k+1,len(a)):
                if a[i][j]:
                    q=a[i][j]//a[k][j]
                    a[i]=[u-q*v for u,v in zip(a[i],a[k])]
            nz=[i for i in range(k+1,len(a)) if a[i][j]]
            if not nz:break
            p=min(nz,key=lambda i:abs(a[i][j]));a[k],a[p]=a[p],a[k]
        if a[k][j]<0:a[k]=[-x for x in a[k]]
        for i in range(k):
            q=a[i][j]//a[k][j];a[i]=[u-q*v for u,v in zip(a[i],a[k])]
        k+=1
    return tuple(tuple(r) for r in a[:k])

def member(H,v):
    v=list(v)
    for row in H:
        j=next(j for j,z in enumerate(row) if z)
        q,r=divmod(v[j],row[j])
        if r:return False
        v=[x-q*y for x,y in zip(v,row)]
    return not any(v)

def check_normal_form():
    rng=random.Random(20261024);checked=0
    for d in range(1,7):
        for _ in range(100):
            rows=[tuple(rng.randrange(-5,6) for _ in range(d)) for _ in range(rng.randrange(1,d+3))]
            H=row_hnf(rows,d)
            if not all(member(H,r) for r in rows):raise ValueError('generator excluded')
            rows2=[list(r) for r in rows]
            for step in range(20):
                i=rng.randrange(len(rows2));j=rng.randrange(len(rows2))
                if i==j:rows2[i]=[-x for x in rows2[i]]
                else:
                    q=rng.randrange(-3,4);rows2[i]=[x+q*y for x,y in zip(rows2[i],rows2[j])]
            rng.shuffle(rows2)
            if H!=row_hnf(rows2,d):raise ValueError('unimodular invariance failure')
            checked+=1
    return checked

def saturation_at_two(rows,dimension):
    H=row_hnf(rows,dimension)
    while True:
        parity=[sum((x%2)*2**i for i,x in enumerate(row)) for row in H]
        relation=None
        # Exhaust all subsets, independently from binary Gaussian elimination.
        xors=[0]
        for mask in range(1,2**len(H)):
            bit=mask & -mask;j=bit.bit_length()-1
            x=xors[mask^bit]^parity[j];xors.append(x)
            if x==0:relation=mask;break
        if relation is None:return H
        half=tuple(sum(row[j] for i,row in enumerate(H) if relation>>i&1)//2 for j in range(dimension))
        if member(H,half):raise ValueError('saturation did not enlarge lattice')
        H=row_hnf((*H,half),dimension)

def explore(n,saturate=False,time_limit=None):
    start=time.monotonic();scale=2**(n-1);dimension=n-1
    if saturate:scale=1
    relations=[]
    def relation(a,b,c,d):
        v=[int(i in (a,b))-int(i in (c,d)) for i in range(n)]
        if next(x for x in v if x)<0:v=[-x for x in v]
        return tuple(v[1:])
    for a,b,c,d in combinations(range(n),4):
        relations += [relation(a,b,c,d),relation(a,c,b,d),relation(a,d,b,c)]
    index={r:i for i,r in enumerate(relations)};cycles=[]
    for tail in permutations(range(1,n)):
        if tail[0]>tail[-1]:continue
        c=(0,)+tail;E=[(c[i],c[(i+1)%n]) for i in range(n)]
        cycles.append(frozenset(index[relation(a,b,c,d)] for (a,b),(c,d) in combinations(E,2) if len({a,b,c,d})==4))
    scaled=[tuple(scale*x for x in r) for r in relations]
    differences=[tuple(scale*(int(k==i)-int(k==j)) for k in range(1,n)) for i,j in combinations(range(n),2)]
    seen=set();counts={'states':0,'collapsed_branches':0,'counterexample_modules':0,'cached_states':0,'maximum_rank':0}
    def visit(H):
        if time_limit is not None and time.monotonic()-start>time_limit:raise TimeoutError
        if H in seen:counts['cached_states']+=1;return
        seen.add(H);counts['states']+=1;counts['maximum_rank']=max(counts['maximum_rank'],len(H))
        if any(member(H,d) for d in differences):counts['collapsed_branches']+=1;return
        closed={i for i,r in enumerate(scaled) if member(H,r)}
        uncovered=next((c for c in cycles if not c&closed),None)
        if uncovered is None:counts['counterexample_modules']+=1;return
        for i in sorted(uncovered):
            visit(saturation_at_two((*H,relations[i]),dimension) if saturate else row_hnf((*H,relations[i]),dimension))
    complete=True
    try:visit(())
    except TimeoutError:complete=False
    return {'n':n,'relation_count':len(relations),'hamiltonian_cycles':len(cycles),
            'counts':counts,'complete':complete,'saturated_at_two':saturate,'seconds':time.monotonic()-start}

if __name__=='__main__':
    r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_form_invariance_checks':check_normal_form(),
       'method':'Euclidean row operations in n-1 coordinates; integer back substitution; no external dependencies or author imports',
       'results':[explore(n) for n in (5,6)]}
    for result in r['results']:
        source=HERE/'snapshot/relation_cover'/f"result_n{result['n']}.json"
        if source.exists():
            old=json.loads(source.read_text())
            if result['counts']!=old['counts']:raise ValueError(('source count mismatch',result,old))
            result['matches_frozen_author_counts']=True
    r['passed']=True;(HERE/'lattice_row_reproduction_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
