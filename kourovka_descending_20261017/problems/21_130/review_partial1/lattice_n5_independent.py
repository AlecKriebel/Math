#!/usr/bin/env python3
"""HNF-free exhaustive n=5 audit of odd-group collision covers.

Enumerates all 4^5 permissible four-tuple relation patterns, rather than the
author's lattice branch/cache traversal. Uses exact rational row reduction and
gcds of determinant minors, implemented here with no third-party dependency.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
from math import gcd
from pathlib import Path
import json,datetime

HERE=Path(__file__).resolve().parent

def rank(rows):
    a=[[Fraction(x) for x in row] for row in rows];r=0
    for j in range(4):
        i=next((i for i in range(r,len(a)) if a[i][j]),None)
        if i is None:continue
        a[i],a[r]=a[r],a[i];z=a[r][j];a[r]=[x/z for x in a[r]]
        for i in range(r+1,len(a)):
            z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def determinant(a):
    # Leibniz formula independently checks all signs without a normal form.
    n=len(a);total=0
    for p in permutations(range(n)):
        term=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        for i in range(n):term*=a[i][p[i]]
        total+=term
    return total

def divisor(rows,r):
    if r==0:return 1
    result=0
    for I in combinations(range(len(rows)),r):
        for J in combinations(range(4),r):
            result=gcd(result,determinant([[rows[i][j] for j in J] for i in I]))
    return result

def verify():
    cycles=[(0,)+p for p in permutations(range(1,5)) if p[0]<p[-1]]
    E=[{frozenset((c[i],c[(i+1)%5])) for i in range(5)} for c in cycles]
    relations=[];groups=[]
    for Q in combinations(range(5),4):
        a,b,c,d=Q;g=[]
        for left,right in (((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))):
            row=[int(i in left)-int(i in right) for i in range(1,5)]
            covered=sum(2**j for j,edges in enumerate(E) if frozenset(left) in edges and frozenset(right) in edges)
            g.append(len(relations));relations.append({'row':row,'covered':covered})
        groups.append(g)
    full=2**len(cycles)-1;allcovers=[];minimal=[];patterns=0;coverage_histogram={};maxcovered=0
    for choices in product(range(4),repeat=5):
        patterns+=1;ids=[groups[q][c-1] for q,c in enumerate(choices) if c]
        covered=0
        for i in ids:covered|=relations[i]['covered']
        k=covered.bit_count();coverage_histogram[k]=coverage_histogram.get(k,0)+1;maxcovered=max(maxcovered,k)
        if covered!=full:continue
        rows=[relations[i]['row'] for i in ids];r=rank(rows);D=divisor(rows,r)
        forced=[]
        for i,j in combinations(range(5),2):
            d=[int(k==i)-int(k==j) for k in range(1,5)]
            if rank(rows+[d])!=r:continue
            Dplus=divisor(rows+[d],r)
            if D%Dplus:raise ValueError('nonintegral lattice index')
            order=D//Dplus
            if order>0 and order&(order-1)==0:forced.append({'pair':[i,j],'2_primary_order':order})
        if not forced:raise ValueError(('potential odd-group cover',ids))
        record={'ids':ids,'rank':r,'torsion_order':D,'forced_equalities':forced}
        allcovers.append(record)
        isminimal=True
        for omit in ids:
            mask=0
            for i in ids:
                if i!=omit:mask|=relations[i]['covered']
            if mask==full:isminimal=False;break
        if isminimal:minimal.append(record)
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'n':5,'method':'4^5 four-tuple patterns; Fraction rank and Leibniz determinant minors; no HNF or author imports',
            'patterns':patterns,'cover_patterns':len(allcovers),'minimal_cover_patterns':len(minimal),
            'coverage_histogram':dict(sorted(coverage_histogram.items())),'max_covered_cycles':maxcovered,
            'min_uncovered_cycles':len(cycles)-maxcovered,'lattice_minor_arithmetic_needed':bool(allcovers),
            'all_cover_patterns_force_vertex_equality_in_odd_groups':True,
            'minimal_patterns':minimal,'passed':True}

if __name__=='__main__':
    r=verify();(HERE/'lattice_n5_independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
