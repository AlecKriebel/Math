#!/usr/bin/env python3
"""Independent finite adversarial checks. No candidate or repair imports.

Exact physical pair counts include arbitrary rectangle crops, motif collisions,
finite imbalance, both displacement signs, and half-open edge conventions.
Infinite RS/ergodicity claims are analytic, not certified by this finite script.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import hashlib, json, math

SLOTS = ((0,0),(3,3),(10,0),(0,10))
WEIGHTS = (F(1),F(1),F(1,2),F(1,2))

def binary_rs(n):
    if n == 0: return 1
    if n == -1: return -1
    q,r=divmod(n,4)
    return binary_rs(q)*(1 if r<2 else (-1)**(q+r))

def points_in(crop, xs, ys):
    L,R,B,T=crop
    ans=set()
    # Deliberately construct a superset then crop the ACTUAL physical points.
    for i,j in product(range(L//30-2,R//30+3),range(B//30-2,T//30+3)):
        for c,(dx,dy) in enumerate(SLOTS):
            p=(30*i+dx,30*j+dy)
            if L<=p[0]<R and B<=p[1]<T and (c!=2 or xs[i]==1) and (c!=3 or ys[j]==1):
                ans.add(p)
    return ans

def independent_pair_count(crop, r, xs, ys):
    # Reconstruct ordered compatible motif pairs in CELL coordinates,
    # with independent x/y axis bounds from BOTH physical endpoints.
    L,R,B,T=crop
    ans=0
    for c,d in product(range(4),repeat=2):
        rem=tuple(r[h]-(SLOTS[d][h]-SLOTS[c][h]) for h in range(2))
        if any(z%30 for z in rem):continue
        m,n=(z//30 for z in rem)
        counts=[]
        for axis,(lo,hi,shift,seq) in enumerate(((L,R,m,xs),(B,T,n,ys))):
            cslot=2 if axis==0 else 3
            zc,zd=SLOTS[c][axis],SLOTS[d][axis]
            # integer ceil/floor bounds avoid numerical rounding.
            first=max(-( -(lo-zc)//30), -(-(lo-zd)//30)-shift)
            last=min((hi-1-zc)//30,(hi-1-zd)//30-shift)
            counts.append(sum((c!=cslot or seq[i]==1) and (d!=cslot or seq[i+shift]==1) for i in range(first,last+1)))
        ans+=counts[0]*counts[1]
    return ans

def limiting_coefficient(r):
    coeff=F(0)
    for c,d in product(range(4),repeat=2):
        rem=tuple(r[h]-(SLOTS[d][h]-SLOTS[c][h]) for h in range(2))
        if all(z%30==0 for z in rem):
            coeff+=WEIGHTS[c]*WEIGHTS[d]
            if c==d==2 and rem[0]==0:coeff+=F(1,4)
            if c==d==3 and rem[1]==0:coeff+=F(1,4)
    return coeff

def triangle_partition(t):
    # Derive floor partitions rather than assuming the overlap answer.
    cuts={F(0),F(1)}
    zlo=math.floor(t)-2;zhi=math.floor(t)+4
    cuts.update(F(z)-t for z in range(zlo,zhi) if 0<F(z)-t<1)
    cuts=sorted(cuts)
    return sum((b-a) for a,b in zip(cuts,cuts[1:]) if math.floor((a+b)/2+t)==0)

def main():
    xs={i:binary_rs(i) for i in range(-400,401)}
    ys={i:binary_rs(i+37) for i in range(-400,401)}
    residue_pairs=[(c,d) for c,d in product(range(4),repeat=2) if tuple((SLOTS[d][h]-SLOTS[c][h])%30 for h in range(2))==(3,3)]
    assert residue_pairs==[(0,1)]
    pair_multiplicities=Counter(tuple((SLOTS[d][h]-SLOTS[c][h])%30 for h in range(2)) for c,d in product(range(4),repeat=2))
    assert pair_multiplicities[(0,0)]==4
    shifts=sorted({tuple(30*z[h]+SLOTS[d][h]-SLOTS[c][h] for h in range(2)) for c,d in product(range(4),repeat=2) for z in product(range(-2,3),repeat=2)})
    crops=[(-119,277,-81,251),(-240,241,-240,241),(0,960,0,990),(7,307,13,313),(10,340,10,310)]
    records=[]
    for crop in crops:
        points=points_in(crop,xs,ys)
        error=F(0);area=F((crop[1]-crop[0])*(crop[3]-crop[2]),900)
        for r in shifts:
            direct=sum((p[0]+r[0],p[1]+r[1]) in points for p in points)
            exact=independent_pair_count(crop,r,xs,ys)
            assert direct==exact,(crop,r,direct,exact)
            error=max(error,abs(F(direct)/area-limiting_coefficient(r)))
        records.append({'crop_grid30':crop,'point_count':len(points),'physical_displacements':len(shifts),'all_pair_counts_match':True,'max_difference_from_infinite_limit':str(error)})
    # Boundary convention negative control. Closed right edges add points.
    crop=(0,60,0,60)
    halfopen=points_in(crop,xs,ys)
    edge_added=points_in((0,61,0,61),xs,ys)-halfopen
    assert edge_added
    # Same-cell coefficient collisions cannot be discarded as duplicate slots.
    assert limiting_coefficient((0,0))==3
    incorrect_zero=sum(w*w for w in WEIGHTS)
    assert incorrect_zero!=limiting_coefficient((0,0))
    # Marker mutant adds a false directed pair.
    badslots=((0,0),(5,0),(10,0),(0,10))
    badpairs=[(c,d) for c,d in product(range(4),repeat=2) if tuple((badslots[d][h]-badslots[c][h])%30 for h in range(2))==(5,0)]
    assert badpairs==[(0,1),(1,2)]
    nflow=0
    for q in range(1,31):
        for p in range(-5*q,5*q+1):
            t=F(p,q)
            assert triangle_partition(t)==max(F(0),1-abs(t))
            nflow+=1
    # Piecewise source recurrence signs independently match substitution prefix.
    rho={'a':'ab','b':'ac','c':'db','d':'dc'}
    word='a'
    for _ in range(16):word=''.join(rho[c] for c in word)
    assert [1 if c in 'ab' else -1 for c in word]==[binary_rs(n) for n in range(len(word))]
    negatives={'closed_right_crop_adds_physical_points':len(edge_added),'missing_exception_zero_coefficient':str(incorrect_zero),'marker_mutant_extra_pair':badpairs[1]}
    result={'status':'PASS','finite_only':True,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'actual_crop_records':records,'flow_partition_cases':nflow,'source_substitution_sites':len(word),'negative_controls':negatives,'limits':'Finite tests do not establish the infinite RS theorem, hull conjugacy, or priority; these are separately assessed in proof/source review.'}
    Path(__file__).with_name('independent_whole_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
