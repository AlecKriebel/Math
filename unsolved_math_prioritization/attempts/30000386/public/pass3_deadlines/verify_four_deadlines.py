#!/usr/bin/env python3
"""Pure-integer/rational certificate checker for the finite reduction in FOUR_DEADLINES.md."""
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from hashlib import sha256
import json


def multiply(p,q):
    result=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        if x:
            for j,y in enumerate(q):
                if y:result[i+j]+=x*y
    return tuple(result)

@lru_cache(None)
def mask(k):
    if k==0:return (1,1,1)
    a=2**k
    return tuple(int(x%4!=0) for x in range(-2*a+1,2*a))

@lru_cache(None)
def polynomial(ks):
    p=(1,)
    for k in ks:p=multiply(p,mask(k))
    return p

@lru_cache(None)
def window(ks,k):
    p=polynomial(ks);b=2**k
    if k>=1 and 4*b-1>=len(p)+3:
        # Every shift omits one residue class modulo four. A window
        # covering all support exists with each of the four residues.
        return sum(p)-min(sum(p[r::4]) for r in range(4))
    return max(multiply(p,mask(k)))


def concentration(kernels,k):
    n=9*4**k
    return max(Q(window(ks,k)**2,1)/(den*n) for ks,den in kernels)


def prepare(k,kernels):
    a=2**k;n=9*a*a
    # w<=2a-1, and one boundary announcement is additionally reserved.
    charge=2*a*concentration(kernels,k)
    charge+=sum((2**(j+1)*concentration(kernels,j) for j in range(k)),Q(0))
    denominator=n*(1-charge)
    assert denominator>0,(k,kernels,denominator)
    output=[((),Q(1))]
    for ks,den in kernels:
        output.append((tuple(sorted(ks+(k,))),den*denominator))
    return output,denominator


def infinite_cost(kernels):
    support=max(len(polynomial(ks)) for ks,den in kernels)
    K=max(1,(support+3).bit_length())
    assert 4*2**K-1>=support+3
    cost=sum((2**(k+1)*concentration(kernels,k) for k in range(K)),Q(0))
    mass=concentration(kernels,K)*(9*4**K)
    # For all scales >=K, exact maximal endpoint-set mass is constant.
    return cost+Q(4,9*2**K)*mass,K


def main():
    # Check coordinate masks against the geometric recursion.
    A={-1,0,1}
    for k in range(8):
        a=2**k
        expected=tuple(int(x in A) for x in range(-2*a+1,2*a))
        assert mask(k)==expected and len(A)==3*a
        shift=2*a
        left={x-shift for x in A};right={x+shift for x in A}
        assert left.isdisjoint(right)
        A=left|right
    # Check the large-window optimization against direct correlation.
    for ks in [(),(0,),(1,),(0,0),(0,1),(1,2),(0,0,0),(1,1,1),(0,1,2)]:
        for k in range(6):
            assert window(ks,k)==max(multiply(polynomial(ks),mask(k)))
    rows=[];maximum=(Q(0),None)
    for ka,kb,kc in product(range(5),range(6),range(6)):
        kernels=[((),Q(1))];denominators=[]
        for k in (kc,kb,ka):
            kernels,D=prepare(k,kernels)
            denominators.append(str(D))
        F,tail_start=infinite_cost(kernels)
        assert F<1,(ka,kb,kc,F)
        scales=[2**ka,2**kb,2**kc]
        if F>maximum[0]:maximum=F,scales
        rows.append({'gap_scales':scales,'denominators_last_to_first':denominators,
                     'infinite_cost':str(F),'tail_start_scale':2**tail_start})
    assert len(rows)==180
    assert maximum==(Q(34777,50976),[2,2,2]),maximum
    here=Path(__file__).parent
    certificate={'status':'PASS','method':'Exact Python integers and fractions; no floating-point arithmetic',
      'case_count':len(rows),'max_infinite_cost':str(maximum[0]),'maximizing_gap_scales':maximum[1],
      'cases':rows}
    (here/'FOUR_DEADLINES_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    summary={k:v for k,v in certificate.items() if k!='cases'}
    proof=here/'FOUR_DEADLINES.md'
    if proof.exists():summary['proof_sha256']=sha256(proof.read_bytes()).hexdigest()
    summary['checker_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    summary['certificate_sha256']=sha256((here/'FOUR_DEADLINES_CERTIFICATE.json').read_bytes()).hexdigest()
    (here/'FOUR_DEADLINES_CHECK.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
