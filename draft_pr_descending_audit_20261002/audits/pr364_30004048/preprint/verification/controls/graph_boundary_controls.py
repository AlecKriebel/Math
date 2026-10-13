#!/usr/bin/env python3
"""Independent exact graph controls. Writes stdout only; no claim to enumerate psi."""
from fractions import Fraction as F
from itertools import product
import json

counts={}
def check(category, condition):
    if not condition:
        raise AssertionError(category)
    counts[category]=counts.get(category,0)+1

def graph(AB, CB, middle):
    """Neighborhood sets on actual vertex indices, with explicit two-edge unions."""
    BA=[{a for a,s in enumerate(AB) if b in s} for b in range(middle)]
    BC=[{c for c,s in enumerate(CB) if b in s} for b in range(middle)]
    reached_A=[set().union(*(BA[b] for b in s)) for s in CB]
    reached_C=[set().union(*(BC[b] for b in s)) for s in AB]
    return BA,BC,reached_A,reached_C

def verify(AB,CB,m,x,y,category):
    BA,BC,ra,rc=graph(AB,CB,m)
    for s in AB: check(category,F(len(s),m)>=x)
    for s in BA: check(category,F(len(s),len(AB))>=x)
    for s in CB: check(category,F(len(s),m)>=y)
    for s in BC: check(category,F(len(s),len(CB))>=y)
    for a,c in product(range(len(AB)),range(len(CB))):
        check('support_set_identity',(a in ra[c])==(c in rc[a])==bool(AB[a]&CB[c]))
    return max(F(len(s),len(AB)) for s in ra),max(F(len(s),len(CB)) for s in rc)

# Graph reversal preserves four minima, but not a particular directional maximum.
ab=[{0,1,2},{0},{1},{3}];cb=[{i} for i in range(4)]
check('directional_max',verify(ab,cb,4,F(1,4),F(1,4),'directional_degree')==(F(1,2),F(3,4)))
for k in range(1,9):
    ab=cb=[{i} for i in range(k)]
    check('reciprocal_endpoint',verify(ab,cb,k,F(1,k),F(1,k),'endpoint_degree')==(F(1,k),F(1,k)))

# Boundary at incompatible middle cardinality uses integer ceilings, never floats.
for m in range(2,16):
    for den in range(2,12):
        for numerator in range(1,den):
            theta=F(numerator,den)
            ka=(m*(1-theta)).__ceil__();kc=(m*theta).__ceil__()
            check('ceiling_partition',ka+kc==m+(int((m*theta).denominator!=1)))
            if ka+kc>m:
                ab=[{(a+j)%m for j in range(ka)} for a in range(m)]
                cb=[{(c+j)%m for j in range(kc)} for c in range(m)]
                check('incompatible_boundary_full',verify(ab,cb,m,1-theta,theta,'rounding_degree')==(F(1),F(1)))

# A zero middle type can carry a combinatorial path that disappears in a blowup.
P=[{0,1},{2}];Q=[{0,2},{1}];b=[F(0),F(1,2),F(1,2)]
for s in P+Q:check('zero_middle_weight',sum(b[j] for j in s)>=F(1,2))
for j in range(3):
    check('zero_middle_reverse_degree',sum(F(1,2) for s in P if j in s)>=F(1,2))
    check('zero_middle_reverse_degree',sum(F(1,2) for s in Q if j in s)>=F(1,2))
check('zero_middle_support_change',verify([{0},{1}],[{1},{0}],2,F(1,2),F(1,2),'zero_deletion_degree')==(F(1,2),F(1,2)))
_,_,before,_=graph(P,Q,3)
check('zero_middle_support_change',max(map(len,before))==2)

# Independent tracing of the PRIMARY source figure, without loading draft certificates.
rows=[{0,2,3,4},{1,2,3,4},{2,5,6},{3,5,6},{4,5,6},{0,1,5},{0,1,6}]
bs=[5,5,3,3,3,4,4];cs=[4,4,3,3,3,5,5]
seed_results=[]
for complement,numerator in [(False,13),(True,14)]:
    r=[set(range(7))-s if complement else s for s in rows]
    columns=[{i for i in range(7) if j in r[i]} for j in range(7)]
    for s in r:check('source_regularity',sum(cs[j] for j in s)==numerator)
    for s in columns:check('source_regularity',sum(bs[i] for i in s)==numerator)
    check('source_distinct',len(set(map(frozenset,columns)))==7)
    check('source_degree',max(map(len,r))==4)
    for i,j in product(range(7),repeat=2):
        if i!=j:check('source_incomparable',bool(columns[i]-columns[j]))
    bt=[j for j,n in enumerate(bs) for _ in range(n)]
    ct=[j for j,n in enumerate(cs) for _ in range(n)]
    at=[j for j in range(7) for _ in range(numerator)]+[7]*(108-7*numerator)
    ab=[{j for j,t in enumerate(bt) if a==7 or t not in columns[a]} for a in at]
    cb=[{j for j,t in enumerate(bt) if t in columns[c]} for c in ct]
    theta=F(numerator,27)
    forward,reverse=verify(ab,cb,27,1-theta,theta,'source_blowup_degree')
    check('source_blowup_reach',forward==F(108-numerator,108))
    BA,BC,ra,rc=graph(ab,cb,27)
    miss_sets=[set(range(108))-s for s in ra]
    check('grouping_is_essential',len(set(map(frozenset,cb)))==7)
    # Counting actual C copies as distinct types would falsely strengthen the bound.
    ungrouped_D=max(map(len,BC));t=F(min(map(len,miss_sets)),108)
    check('ungrouped_bound_rejected',t*ungrouped_D>theta)
    # Dropping the universal residual would violate a B-to-A minimum.
    without=[s for a,s in zip(at,ab) if a!=7]
    reduced_BA,_,_,_=graph(without,cb,27)
    check('residual_deletion_rejected',min(F(len(s),len(without)) for s in reduced_BA)<1-theta)
    seed_results.append({'theta':str(theta),'parts':[108,27,27],'forward':str(forward),'reverse':str(reverse),'grouped_columns':7,'ungrouped_degree':ungrouped_D})

# Materially different rectangular census: actual A=4, B=3, C=6.
# Exact regular Q is necessary for EVERY nonfull boundary case by the audited proof.
census=[]
for k in (1,2):
    m,na,nc=3,4,6
    pm=[v for v in range(1<<m) if v.bit_count()>=m-k]
    qm=[v for v in range(1<<m) if v.bit_count()==k]
    ps=[p for p in product(pm,repeat=na) if all(sum((v>>j)&1 for v in p)*m>=(m-k)*na for j in range(m))]
    qs=[q for q in product(qm,repeat=nc) if all(sum((v>>j)&1 for v in q)*m==k*nc for j in range(m))]
    full=nonfull=repeat=extra=0
    for p,q in product(ps,qs):
        reach=[sum(bool(v&w) for v in p) for w in q]
        if max(reach)==na:full+=1;continue
        nonfull+=1;types=set(q)
        missing={w:{i for i,v in enumerate(p) if not(v&w)} for w in types}
        for w,inds in missing.items():
            check('rectangular_missing',bool(inds))
            check('rectangular_complement',all(p[i]==((1<<m)-1)^w for i in inds))
        check('rectangular_disjoint',sum(map(len,missing.values()))==len(set().union(*missing.values())))
        D=max(sum((w>>j)&1 for w in types) for j in range(m))
        t=min(map(len,missing.values()))
        check('rectangular_integer_bound',t*D*m<=k*na)
        check('rectangular_fraction_bound',F(max(reach),na)==1-F(t,na))
        repeat+=len(types)<nc;extra+=sum(map(len,missing.values()))<na
    census.append({'parts':[na,m,nc],'theta':str(F(k,m)),'admissible_P':len(ps),'regular_Q':len(qs),'full_cases':full,'nonfull_cases':nonfull,'repeated_C_cases':repeat,'extra_A_cases':extra,'coverage':'All degree-admissible P and all exactly regular Q; nonregular Q necessarily full by analytic rigidity, not enumerated here.'})

gaps=[abs(F(13,27*d)-F(14,27*e)) for d,e in product(range(1,5),repeat=2)]
check('integer_gap',min(gaps)==F(1,108))
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'source_graphs':seed_results,'rectangular_census':census,'minimum_integer_gap':str(min(gaps)),'scope':'Independent finite set, rounding and support controls; universal boundary proof audited analytically; no true d minima or exact psi values/order evaluated.'},indent=2,sort_keys=True))
