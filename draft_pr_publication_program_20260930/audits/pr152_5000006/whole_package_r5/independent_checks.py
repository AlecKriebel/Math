#!/usr/bin/env python3
"""Fresh exact partition, lifted cone and marked-lattice diagnostics.

No imports of the authored checker or any external-source programs.
The universal deductions are in INDEPENDENT_FIRST_ASSESSMENT.md.
"""
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import json, hashlib

counts={}
def check(name, value):
    if not value: raise RuntimeError(name)
    counts[name]=counts.get(name,0)+1

def literal(n,a,b,odd):
    h=n//2; result=set()
    for k in range(n-1):
        if n%2:
            ok=(k<=h-1 and a>=Q(n-2*k-2,n) or k>=h and a<=Q(2*(n-k-2),n)) if odd else (k<=h+1 and a<=Q(n-2*k-2,n) or k>=h and a>=Q(2*(n-k-2),n))
        else:
            ok=(k<=h-1 and a>=Q(h-k-1,h) or k>=h-1 and a<=Q(n-k-2,h)) if odd else (k<=h-1 and a<=Q(h-k-1,h) or k>=h-1 and a>=Q(n-k-2,h))
        if not ok: continue
        if odd and a+b==Q(2*(n-k-1),n): result.add(k%(n-2))
        if not odd and b-a in (Q(2*(k+1),n),Q(2*(k+3-n),n)): result.add(k%(n-2))
    return result

for n in range(3,97):
    d=Q(n-2,n); modulus=n-2
    # Complete rational interval partitions of all possible integral s.
    for odd in (False,True):
        for s in range(-n,n+1):
            lo=max(Q(0),Q(2,n)-Q(2*s,n) if not odd else Q(2*s,n)-1)
            hi=min(d,1-Q(2*s,n) if not odd else Q(2*s,n)-Q(2,n))
            if lo>hi: continue
            for a in {lo,hi,(lo+hi)/2}:
                b=Q(2*s,n)-a if odd else a+Q(2*s,n)
                k=(n-1-s if odd else s-1)%modulus
                check('source_interval_partition',literal(n,a,b,odd)=={k})
                check('physical_parity_reverse',literal(n,1-b,1-a,odd)=={(-k if odd else k)%modulus})
                check('physical_chart_reflection',literal(n,d-a,1+Q(2,n)-b,odd)=={(-k)%modulus})
    # General cone arithmetic includes every terminal corner and full lifts.
    r=modulus if n%2 else modulus//2
    for e in (0,) if n%2 else (0,1):
        for t in range(2*n if n%2 else n):
            odd=(t+e)%2==0
            # s follows from the exact developed corner/cone equation.
            for m in (0,r-1):
                for lift in (-3,-1,0,1,3):
                    angle=(1-e)+2*m+2*r*lift
                    if odd:
                        s=Q(n,2)*(t*d+1-angle)
                        k=n-1-s
                    else:
                        s=Q(n,2)*(angle-t*d+Q(2,n))
                        k=s-1
                    check('lifted_corner_integrality',s.denominator==1)
                    check('full_lift_intrinsic_dictionary',k%modulus==(2*m+1-e)%modulus)
    for k in range(modulus):
        j=(-k)%modulus
        check('canonical_weight_sign',j==0 if k==0 else j+1==n-k-1)

weights={0:Q(1,4),1:Q(3,4),2:Q(1),3:Q(3,4)}
def norm(p,q):return p*p-p*q+q*q
def endpoint_type(p,q):
    mult=2 if (p+q)%3==2 else 1
    x,y=mult*p,mult*q
    if x%3==1 and y%3==2:k=1
    elif x%2==0 and y%2==0:k=2
    elif x%3==2 and y%3==1:k=3
    else:k=0
    return mult,k,Q(norm(x,y))/weights[k]

for p in range(-36,37):
    for q in range(-36,37):
        if gcd(p,q)!=1:continue
        mult,k,ratio=endpoint_type(p,q)
        check('hex_marked_endpoint',(mult*(p+q))%3!=2)
        if mult==2:check('hex_halfpoint_unmarked',(p+q)%3==2)
        for x,y in ((q,p),(p-q,p),(-p,-q)):
            check('hex_primitive_isometry',gcd(x,y)==1 and norm(x,y)==norm(p,q))
            check('hex_same_family',((x+y)%3==0)==((p+q)%3==0))
            check('hex_L_squared_over_w_squared',endpoint_type(x,y)[2]==ratio)
            check('square_parity_isometry',(p%2==q%2==1)==((-q)%2==p%2==1))

receipt={'status':'PASS','n_range':[3,96],'lattice_box':[-36,36],
 'full_lift_offsets':[-3,-1,0,1,3],'counts':counts,'checks':sum(counts.values()),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitation':'Finite exact diagnostics; universal affine/cusp/model claims are separately deduced, not inferred from these controls.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
