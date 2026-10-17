#!/usr/bin/env python3
"""Independent exact replay using sparse products and residue-prefix windows."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

@lru_cache(None)
def coords(k):
    if k == 0: return (-1,0,1)
    shift=2**k
    previous=coords(k-1)
    left=tuple(x-shift for x in previous)
    right=tuple(x+shift for x in previous)
    if set(left)&set(right): raise RuntimeError('overlapping children')
    return left+right

@lru_cache(None)
def poly(ks):
    p={0:1}
    for k in ks:
        out={}
        for x,v in p.items():
            for y in coords(k):
                out[x+y]=out.get(x+y,0)+v
        p=out
    return tuple(sorted(p.items()))

@lru_cache(None)
def direct_window(ks,k):
    items=poly(ks); low=items[0][0]; high=items[-1][0]
    values=dict(items); size=high-low+1
    sums=[0]; residues=[[0] for _ in range(4)]
    for x in range(low,high+1):
        v=values.get(x,0);sums.append(sums[-1]+v)
        for r in range(4):residues[r].append(residues[r][-1]+(v if x%4==r else 0))
    radius=2*(2**k)-1
    best=0
    for center in range(low-radius,high+radius+1):
        lo=max(low,center-radius)-low
        hi=min(high,center+radius)-low+1
        value=sums[hi]-sums[lo]
        if k:
            row=residues[center%4]
            value-=row[hi]-row[lo]
        best=max(best,value)
    return best

@lru_cache(None)
def tail_window(ks):
    totals=[0,0,0,0]
    for x,v in poly(ks):totals[x%4]+=v
    return sum(totals)-min(totals)


def C(family,k):
    return max(Q(direct_window(shape,k)**2,9*4**k)/den for shape,den in family)


def smooth(family,k):
    scale=2**k
    charged=sum((2**(j+1)*C(family,j) for j in range(k+1)),Q(0))
    divisor=9*scale*scale*(1-charged)
    if divisor<=0:raise RuntimeError(('nonpositive divisor',k,divisor))
    result=[((),Q(1))]
    result += [(tuple(sorted(shape+(k,))),den*divisor) for shape,den in family]
    return result,divisor


def infinite_cost(family):
    longest=max(poly(shape)[-1][0]-poly(shape)[0][0]+1 for shape,den in family)
    K=1
    while 4*2**K-1 < longest+3:K+=1
    for shape,den in family:
        expected=tail_window(shape)
        for j in (K,K+1):
            if direct_window(shape,j)!=expected:
                raise RuntimeError(('tail identity mismatch',shape,j))
    prefix=sum((2**(j+1)*C(family,j) for j in range(K)),Q(0))
    mass=max(Q(tail_window(shape)**2)/den for shape,den in family)
    return prefix+Q(4,9*2**K)*mass


def main():
    producer=Path(__file__).parents[1]/'pass3_deadlines'
    table=json.loads((producer/'FOUR_DEADLINES_CERTIFICATE.json').read_text())
    claimed={tuple(r['gap_scales']):r for r in table['cases']}
    largest=(Q(0),None);rows=[]
    for ka,kb,kc in product(range(5),range(6),range(6)):
        family=[((),Q(1))];ds=[]
        for k in (kc,kb,ka):
            family,d=smooth(family,k);ds.append(str(d))
        value=infinite_cost(family)
        scales=(2**ka,2**kb,2**kc)
        if value>=1:raise RuntimeError(('cost not below one',scales,value))
        if scales not in claimed:raise RuntimeError(('missing row',scales))
        old=claimed[scales]
        if str(value)!=old['infinite_cost'] or ds!=old['denominators_last_to_first']:
            raise RuntimeError(('producer disagreement',scales,value,ds,old))
        if value>largest[0]:largest=(value,scales)
        rows.append({'scales':scales,'cost':str(value),'divisors':ds})
    if len(rows)!=180 or len(claimed)!=180:raise RuntimeError('wrong row count')
    expected=(Q(34777,50976),(2,2,2))
    if largest!=expected:raise RuntimeError(('wrong maximum',largest))
    result={'status':'PASS','case_count':len(rows),'maximum_cost':str(largest[0]),
        'maximizing_scales':largest[1],
        'method':'Independent sparse integer products and residue-prefix translated windows; exact Fraction arithmetic',
        'all_producer_costs_and_divisors_match':True,
        'tail_checked_directly_at_two_scales_per_kernel':True,
        'proof_sha256':sha256((producer/'FOUR_DEADLINES.md').read_bytes()).hexdigest(),
        'producer_certificate_sha256':sha256((producer/'FOUR_DEADLINES_CERTIFICATE.json').read_bytes()).hexdigest(),
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(__file__).with_name('four_deadlines_independent_replay.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
