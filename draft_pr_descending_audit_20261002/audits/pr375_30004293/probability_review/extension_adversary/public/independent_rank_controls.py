#!/usr/bin/env python3
"""Fresh exhaustive controls for the rank-restriction extension; exact arithmetic."""
from fractions import Fraction as F
from itertools import combinations,product
from collections import defaultdict
from math import prod
import json

def rank(rows):
    if not rows:return 0
    a=[list(map(F,v)) for v in rows];r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][j]
            if v:a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def fibers(a):
    d=defaultdict(list)
    for mask in range(1<<len(a)):
        b=frozenset(x for j,x in enumerate(a) if mask>>j&1)
        d[sum(b)].append(b)
    return d

def validate_family(a,f,counters):
    k=len(f);one=(1,)*k
    columns={x:tuple(int(x in b) for b in f) for x in a}
    fullrank=rank([one]+list(columns.values()))-1
    assert k<=2**fullrank;counters['rank_signature_bound']+=1
    for r in range(1,fullrank+1):
        selected=[one]
        for v in columns.values():
            if rank(selected+[v])>len(selected):selected.append(v)
            if len(selected)==r+1:break
        matrix=list(zip(*selected));chosen=[];indices=[]
        for i,row in enumerate(matrix):
            if rank(chosen+[row])>len(chosen):chosen.append(row);indices.append(i)
            if len(chosen)==r+1:break
        assert rank(chosen)==r+1;counters['invertible_row_restriction']+=1
        reduced=[f[i] for i in indices]
        assert len(set(reduced))==r+1 and len({sum(b) for b in reduced})==1
        rc={x:tuple(int(x in b) for b in reduced) for x in a}
        assert rank([(1,)*(r+1)]+list(rc.values()))==r+1
        counters['reduced_equal_full_rank_family']+=2
        # Re-greedy the entire restricted family, not merely the originally
        # chosen independent columns; residual support must use these pivots.
        spaces=[[(1,)*(r+1)]];pivots=[];pivotvectors=[]
        for x in sorted(a,reverse=True):
            if rank(spaces[-1]+[rc[x]])>len(spaces[-1]):
                pivots.append(x);pivotvectors.append(rc[x]);spaces.append(spaces[-1]+[rc[x]])
        assert len(pivots)==r;counters['regreedy_exact_rank']+=1
        z=[x.bit_length()-1 for x in pivots]
        residual=set(a)-set(pivots)
        for x in residual:
            if x>=2**(z[0]+1):
                assert rank(spaces[0]+[rc[x]])==1;counters['above_first_diagonal']+=1
            for j in range(r):
                low=2**(z[j+1]+1) if j+1<r else min(a)
                high=2**(z[j]+1)
                if low<=x<high:
                    assert rank(spaces[j+1]+[rc[x]])==j+2
                    counters['rounded_support_with_ties']+=1
        qcols=[tuple(v[i]-v[0] for i in range(1,r+1)) for v in pivotvectors]
        assert rank(qcols)==r;counters['quotient_reconstruction_injective']+=1
        residualsum=tuple(sum(x*(rc[x][i]-rc[x][0]) for x in residual) for i in range(1,r+1))
        assert all(residualsum[i]+sum(x*v[i] for x,v in zip(pivots,qcols))==0 for i in range(r))
        counters['quotient_equation_exact']+=1
        # Verify the full cube-section class bound, not only partition spaces.
        for j in range(1,r+1):
            cube=[v for v in product((0,1),repeat=r+1) if rank(spaces[j]+[v])==j+1]
            classes={tuple(v[i]-v[0] for i in range(1,r+1)) for v in cube}
            assert len(cube)<=2**(j+1)
            assert len(classes)==len(cube)-1<=2**(j+1)-1
            counters['general_cube_diagonal_class_bound']+=2
        if min(a)>=2:
            ground=list(range(2,max(a)+1))
            def prob(b):return prod(F(1,x) if x in b else F(x-1,x) for x in ground)
            assert prob(set(a))==prob(residual)*prod(F(1,x-1) for x in pivots)
            counters['exact_distinct_pivot_deletion']+=1

def main():
    counts=defaultdict(int);familycases=0
    # All subfamilies of every equal-sum fiber on [1,6] (arbitrary families).
    a=list(range(1,7))
    for vv in fibers(a).values():
        for sz in range(2,len(vv)+1):
            for f in combinations(vv,sz):validate_family(a,f,counts);familycases+=1
    # Every realization on [2,9], every entire equal-sum fiber.
    for mask in range(1<<8):
        a=[x for j,x in enumerate(range(2,10)) if mask>>j&1]
        for vv in fibers(a).values():
            if len(vv)>=2:validate_family(a,vv,counts);familycases+=1
    # Direct existential event inclusion, with no row-choice union factor.
    event_records=[]
    for n in range(3,8):
        for r in (1,2,3):
            highmass=F();rankmass=F()
            for mask in range(1<<(n-1)):
                a=[x for j,x in enumerate(range(2,n+1)) if mask>>j&1]
                ff=fibers(a);m=max(map(len,ff.values()))
                exists=False
                for vv in ff.values():
                    for family in combinations(vv,r+1):
                        k=r+1;columns=[(1,)*k]+[tuple(int(x in b) for b in family) for x in a]
                        if rank(columns)==k:exists=True;break
                    if exists:break
                assert m<=2**(r-1) or exists;counts['direct_large_to_rank_event_inclusion']+=1
                pp=prod(F(1,x) if x in a else F(x-1,x) for x in range(2,n+1))
                if m>2**(r-1):highmass+=pp
                if exists:rankmass+=pp
            assert highmass<=rankmass;counts['weighted_event_inclusion_no_row_factor']+=1
            event_records.append({'maximum_ground':n,'rank':r,'large_fiber_probability':str(highmass),'full_rank_witness_probability':str(rankmass)})
    # Certified coefficient signs for the actual epsilon=1/20.
    def logs(x,steps=80):
        z=(x-1)/(x+1)
        lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(steps)),F())
        hi=lo+2*z**(2*steps+1)/((2*steps+1)*(1-z*z))
        return lo,hi
    l3,u3=logs(F(3));l73,u73=logs(F(7,3))
    assert F(21,20)*l3-1>0 and F(21,20)*u73<1;counts['certified_coefficient_signs']+=2
    for j in range(2,100):
        assert F(2**(j+1)-1,2**j-1)<=F(7,3);counts['uniform_ratio_bound']+=1
    print(json.dumps({'all_passed':True,'assertions':sum(counts.values()),'categories':dict(counts),'family_cases':familycases,'weighted_event_records':event_records,'limitations':'Exact finite controls supplement the universal argument; logarithmic parameter limits and Borel-Cantelli are proved in writing, not simulated.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
