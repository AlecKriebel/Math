#!/usr/bin/env python3
"""Independent finite controls, not an implementation of BDH's fast theorem."""
from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json

def distances(n, edges):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b);adj[b].append(a)
    out=[]
    for s in range(n):
        dd=[None]*n;dd[s]=0;q=deque([s])
        while q:
            a=q.popleft()
            for b in adj[a]:
                if dd[b] is None:dd[b]=dd[a]+1;q.append(b)
        if any(v is None for v in dd):return None
        out.append(dd)
    return out

def is_median(dd):
    n=len(dd)
    return all(sum(all(dd[a][x]+dd[x][b]==dd[a][b] for a,b in ((i,j),(i,k),(j,k))) for x in range(n))==1 for i,j,k in combinations(range(n),3))

def radius(dd,w):return [max(ww*d for ww,d in zip(w,row)) for row in dd]

def shift_feasible(dd,w,r):
    n=len(dd);d=n-1
    if r<0:return []
    # Bounded comparison search, including zero rows and clipping.
    b=[]
    for ww in w:
        lo,hi=0,d+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if mid*ww<=r:lo=mid
            else:hi=mid
        b.append(lo)
    aa=[d-bb for bb in b]
    assert all(0<=a<=d for a in aa)
    return [x for x,row in enumerate(dd) if max(v+a for v,a in zip(row,aa))<=d]

def optimize(dd,w):
    n=len(dd);d=n-1;rr=radius(dd,w)
    if n==1 or not any(w):return min(rr),[x for x,r in enumerate(rr) if r==min(rr)],0
    best=d*max(w);intervals=[[0,d] for _ in w];calls=0
    while True:
        active=[(w[i]*((lo+hi)//2),hi-lo+1) for i,(lo,hi) in enumerate(intervals) if lo<=hi]
        mass=sum(length for _,length in active)
        if not mass:break
        acc=0
        for q,length in sorted(active):
            acc+=length
            if 2*acc>=mass:break
        feas=bool(shift_feasible(dd,w,q));calls+=1
        if feas:best=min(best,q)
        for i,(lo,hi) in enumerate(intervals):
            if lo>hi:continue
            # First >=q when feasible; first >q otherwise.
            left,right=lo,hi+1
            while left<right:
                mid=(left+right)//2
                predicate=mid*w[i]>=q if feas else mid*w[i]>q
                if predicate:right=mid
                else:left=mid+1
            if feas:intervals[i][1]=left-1
            else:intervals[i][0]=left
        nxt=sum(max(0,hi-lo+1) for lo,hi in intervals)
        assert 4*nxt<=3*mass,(mass,nxt,w,q)
        assert best>=min(rr)
        assert best==min(rr) or any(lo<=hi and any(k*w[i]==min(rr) for k in range(lo,hi+1)) for i,(lo,hi) in enumerate(intervals))
    return best,shift_feasible(dd,w,best),calls

def run():
    counts={'graphs':0,'median_graphs':0,'profiles':0,'threshold_checks':0,'optimization_checks':0,'max_optimization_iterations':0}
    palette=[F(0),F(1,3),F(1),F(5,2)]
    for n in range(1,5):
        pairs=list(combinations(range(n),2))
        for bits in product([0,1],repeat=len(pairs)):
            edges=[e for e,bit in zip(pairs,bits) if bit];dd=distances(n,edges)
            if dd is None:continue
            counts['graphs']+=1;counts['median_graphs']+=is_median(dd)
            for w in product(palette,repeat=n):
                counts['profiles']+=1;rr=radius(dd,w)
                candidates=sorted(set(k*ww for ww in w for k in range(n)))
                thresholds=set(candidates)|{F(-1),F(n)*max(w)+1}
                thresholds.update((a+b)/2 for a,b in zip(candidates,candidates[1:]))
                for r in thresholds:
                    expected=[x for x,rad in enumerate(rr) if rad<=r]
                    assert shift_feasible(dd,w,r)==expected
                    counts['threshold_checks']+=1
                opt,centers,calls=optimize(dd,w)
                assert opt==min(rr)
                assert centers==[x for x,r in enumerate(rr) if r==min(rr)]
                counts['optimization_checks']+=1
                counts['max_optimization_iterations']=max(calls,counts['max_optimization_iterations'])
    dd=distances(6,[(i,i+1) for i in range(5)]);w=[F(1),F(0),F(0),F(0),F(0),F(3)]
    mult=radius(dd,w);add=[max(d+ww for d,ww in zip(row,w)) for row in dd]
    distinction={'graph':'path on vertices 0,...,5','profile':[str(x) for x in w],'multiplicative_radii':[str(x) for x in mult],'additive_eccentricities':[str(x) for x in add],'multiplicative_centers':[i for i,x in enumerate(mult) if x==min(mult)],'untransformed_additive_centers':[i for i,x in enumerate(add) if x==min(add)]}
    assert distinction['multiplicative_centers']!=distinction['untransformed_additive_centers']
    c4=distances(4,[(0,1),(1,2),(2,3),(3,0)]);balls=[{i for i,d in enumerate(row) if d<=1} for row in c4]
    assert all(a&b for a,b in combinations(balls,2)) and not set.intersection(*balls)
    for size in [2,7,13]:
        # Four corners of P_(size+1) x P_(size+1) give sums 4L,2L,2L.
        corners=[(0,0),(size,size),(0,size),(size,0)]
        man=lambda a,b:sum(abs(x-y) for x,y in zip(a,b))
        sums=[man(corners[0],corners[1])+man(corners[2],corners[3]),man(corners[0],corners[2])+man(corners[1],corners[3]),man(corners[0],corners[3])+man(corners[1],corners[2])]
        assert (max(sums)-sorted(sums)[-2])/2==size
    extreme_w=[F(0),F(1,2**256+1),F(2**256+1),F(0)]
    dd=distances(4,[(0,1),(1,2),(2,3)]);opt,cs,_=optimize(dd,extreme_w);rr=radius(dd,extreme_w)
    assert opt==min(rr) and cs==[i for i,r in enumerate(rr) if r==min(rr)]
    return {'status':'pass','scope':'Independent brute-force reference controls; do not validate the fast BDH implementation/asymptotic bound or historical priority. All connected labelled graphs through 4 vertices were included, thus covering median and nonmedian graph controls.','counts':counts,'additive_multiplicative_distinction':distinction,'c4_pairwise_balls_have_empty_total_intersection':True,'bounded_cube_dimension_does_not_bound_hyperbolicity':'P_(L+1) x P_(L+1), dimension 2, four-point hyperbolicity >=L; verified L=2,7,13','large_rational_profile':'pass, 257-bit denominator/numerator inputs','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    result=run();Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
