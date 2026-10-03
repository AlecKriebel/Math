#!/usr/bin/env python3
"""Handwritten audit controls: no imported/copied candidate or historical helper."""
from fractions import Fraction as R
from itertools import product
from datetime import datetime, timezone
from pathlib import Path
import os, sys, json

checks=[]
def require(tag, condition, detail=None):
    if not condition:
        raise AssertionError({'tag':tag,'detail':detail})
    checks.append(tag)

def propagated_pair(n, end):
    # Start the pair (sign at n, current sign) on its diagonal.
    mass={(a,a):R(1,2) for a in (-1,1)}
    for t in range(n,end):
        nxt={}
        for (a,b),w in mass.items():
            for c,prob in [(b,R(t+1,t+2)),(-b,R(1,t+2))]:
                nxt[a,c]=nxt.get((a,c),R(0))+w*prob
        mass=nxt
    return mass

pair_rows=[]
for start,end in [(0,1),(0,37),(1,73),(3,41),(7,89),(11,123),(50,137),(101,401)]:
    law=propagated_pair(start,end)
    corr=sum(a*b*w for (a,b),w in law.items())
    mismatch=sum(w for (a,b),w in law.items() if a!=b)
    require(f'pair_recurrence_{start}_{end}',corr==R(start*(start+1),end*(end+1)))
    require(f'pair_mismatch_{start}_{end}',mismatch==(1-corr)/2)
    pair_rows.append({'start':start,'end':end,'correlation':str(corr),'mismatch':str(mismatch)})

# Test every deterministic fair selector at short horizons via antipodal symmetry.
# Unlike a test restricted to Walsh monomials, this includes nonlinear selectors.
def prefix_mass(h):
    mass={(a,):R(1,2) for a in (-1,1)}
    for t in range(h):
        nxt={}
        for x,w in mass.items():
            nxt[x+(x[-1],)]=w*R(t+1,t+2)
            nxt[x+(-x[-1],)]=w*R(1,t+2)
        mass=nxt
    return mass

selector_rows=[]
for horizon in range(4):
    law=prefix_mass(horizon)
    reps=sorted(x for x in law if x[0]==1)
    correlations=[]
    for choices in product((-1,1),repeat=len(reps)):
        selector={}
        for x,value in zip(reps,choices):
            selector[x]=value;selector[tuple(-a for a in x)]=-value
        mean=sum(law[x]*selector[x] for x in law)
        require(f'fair_selector_{horizon}_{len(correlations)}',mean==0)
        correlations.append(sum(law[x]*selector[x]*x[-1] for x in law))
    for end in [horizon+1,horizon+5,101]:
        rho=sum(a*b*w for (a,b),w in propagated_pair(horizon,end).items())
        extrema=[c*rho for c in correlations]
        require(f'full_selector_envelope_{horizon}_{end}',max(extrema)==rho and min(extrema)==-rho)
        selector_rows.append({'history_end':horizon,'selector_count':len(correlations),'time':end,'max_correlation':str(max(extrema)),'min_mismatch':str((1-max(extrema))/2)})

# Fixed B=X_H versus a new B_n=X_n at each n: same stationary limit marginal,
# different quantifier. Truncated expectations have a rigorous geometric tail.
metric_rows=[]
for n in [1,5,50,500]:
    truncation=32
    changing=sum(R(1,2**(j+1))*sum(w for (a,b),w in propagated_pair(n,n+j).items() if a!=b) for j in range(truncation))
    fixed=sum(R(1,2**(j+1))*sum(w for (a,b),w in propagated_pair(0,n+j).items() if a!=b) for j in range(truncation))
    remainder=R(1,2**truncation)
    require(f'changing_vs_fixed_{n}',fixed==R(1,2)*(1-remainder) and changing+remainder<=R(1,n+1)+remainder)
    metric_rows.append({'n':n,'new_Bn_metric_interval':[str(changing),str(changing+remainder)],'fixed_B0_metric_interval':[str(fixed),str(fixed+remainder)]})

# A dependent growing offset: independent fair B, then wait to first equality.
# Compare direct absorbing recurrence with the closed tail formula.
first_hit_rows=[]
for n in [0,2,17,151,1000]:
    unmatched=R(1,2)
    hit={0:R(1,2)}
    for offset in range(1,41):
        time=n+offset-1
        hit[offset]=unmatched*R(1,time+2)
        unmatched*=R(time+1,time+2)
        require(f'first_hit_tail_{n}_{offset}',unmatched==R(n+1,2*(n+offset+1)))
        require(f'first_hit_mass_{n}_{offset}',sum(hit.values())+unmatched==1)
    first_hit_rows.append({'n':n,'P_offset_greater_40':str(unmatched),'P_offset_zero':str(hit[0])})

# Summable flips expose the global-decorrelation assumption: the product here
# has a positive tail limit, allowing an eventual-sign coupling.
summable_rows=[]
for n,last in [(0,0),(0,23),(4,37),(9,101),(27,301)]:
    noflip=R(1)
    for k in range(n,last+1):noflip*=1-R(1,(k+2)**2)
    formula=R(n+1,n+2)*R(last+3,last+2)
    require(f'summable_noflip_{n}_{last}',noflip==formula)
    summable_rows.append({'n':n,'last':last,'no_flip':str(noflip),'infinite_tail_limit':str(R(n+1,n+2))})

# Independent long-duplicate-block mechanism: exact variable labels suffice
# to check whether a finite window has the iid law, without simulation.
labels=[];pairs=[];fresh=0
for exponent in range(10):
    length=2**exponent
    block=list(range(fresh,fresh+length));base=len(labels)
    labels.extend(block+block)
    pairs.extend((base+j,base+length+j) for j in range(length))
    fresh+=length
for width in [1,2,3,5,8,16]:
    cutoff=2*(2**(width-1).bit_length()-1) if width>1 else 0
    # Explicit conservative cutoff: the first block whose half-length >=width.
    half=1;cutoff=0
    while half<width:cutoff+=2*half;half*=2
    for start in range(cutoff,len(labels)-width+1):
        window=labels[start:start+width]
        require(f'iid_block_window_{width}_{start}',len(set(window))==width)
for a,b in pairs:
    require(f'duplicate_identity_{a}_{b}',labels[a]==labels[b])
# All sign triples imply the coupling-independent endpoint union bound.
for a,b,w in product((-1,1),repeat=3):
    require(f'pair_union_{a}_{b}_{w}',int(a!=b)<=int(a!=w)+int(b!=w))
# Exact sharp endpoint joining, with disjoint iid Y pairs plus independent coin.
pa=pb=R(0);mean=R(0)
for a,b,coin in product((-1,1),repeat=3):
    w=a if coin==-1 else b
    pa+=R(a!=w,8);pb+=R(b!=w,8);mean+=R(w,8)
require('iid_duplicate_bound_sharpness',pa==pb==R(1,4) and mean==0)

result={'runtime_identity':{'pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'utc':datetime.now(timezone.utc).isoformat()},'status':'completed_all_controls','control_count':len(checks),'scope':'Finite exact controls only; universal coupling and infinite limits require REPORT.md. No candidate/old helper imported or executed.','pair_rows':pair_rows,'fair_selector_rows':selector_rows,'coupling_quantifier_rows':metric_rows,'non_tight_first_hit_rows':first_hit_rows,'summable_boundary_rows':summable_rows,'iid_duplicate_bound':{'lower_coordinate_limsup':'1/4','attained_endpoint_mismatch':str(pa)},'check_tags':checks}
print(json.dumps(result,indent=2))
