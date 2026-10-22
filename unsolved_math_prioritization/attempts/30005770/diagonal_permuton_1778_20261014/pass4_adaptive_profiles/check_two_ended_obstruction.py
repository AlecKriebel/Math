#!/usr/bin/env python3
"""Finite regression only; the all-size proof is in the companion note."""
from math import log, log1p
from pathlib import Path
import hashlib
import json
import sys
P=Path(__file__).resolve().parent

def require(ok, data):
    if not ok:
        raise RuntimeError(data)

def e(x,y):
    return x*log1p(y/x)+y*log1p(x/y) if x and y else 0.0

def T(K):
    h=K//2
    return 2*(2**h-1) if K%2==0 else 3*2**h-2

gamma=log(2); H=e(1,.5)
for K in range(1,121):
    z=[2**(min(j,K+1-j)-1) for j in range(1,K+1)]
    require(sum(z)==T(K),('T',K))
    z=[0]+z+[0]
    penalties=[gamma*z[j]-e(z[j],z[j+d]) for j in range(1,K+1) for d in [-1,1]]
    require(abs(max(penalties)-gamma)<1e-12,('certificate_envelope',K,max(penalties)))

windows=0; min_ratio=float('inf'); true_gap_width_checks=0
for m in range(2,61):
    sizes=[2**j for j in range(1,m+1)]+[2**j for j in range(m-1,0,-1)]
    for K in range(1,min(m-1,30)+1):
        cap=gamma/T(K)
        for lo in range(len(sizes)-K+1):
            hi=lo+K-1
            mass=sum(sizes[lo:hi+1])
            left=sizes[lo-1] if lo else 0
            right=sizes[hi+1] if hi+1<len(sizes) else 0
            ratio=(e(sizes[lo],left)+e(sizes[hi],right))/mass
            require(ratio>cap,('window',m,K,lo,ratio,cap))
            if lo<=m-1<=hi:
                require(ratio>=2*H/T(K)-1e-12,('balanced_lower',m,K,lo,ratio))
            min_ratio=min(min_ratio,ratio/cap); windows+=1
            if K==1:
                require(ratio>=log(27/8)+log(2)-1e-12,('true_delta1',m,lo,ratio))
                true_gap_width_checks+=1
            if K==2:
                require(ratio>=H-1e-12 and ratio>log(2),('true_delta2',m,lo,ratio))
                true_gap_width_checks+=1

names=['TWO_ENDED_CERTIFICATE_OBSTRUCTION.md','SMALL_WINDOW_TRUE_GAPS.md',Path(__file__).name]
result={'status':'passed','scope':'Finite floating-point regression, not a growth or probability proof',
        'test_vectors':120,'mountain_windows':windows,'true_small_gap_window_checks':true_gap_width_checks,
        'minimum_boundary_to_two_ended_upper_certificate_ratio':min_ratio,
        'pins':{name:{'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':(P/name).stat().st_size} for name in names}}
output=P/(sys.argv[1] if len(sys.argv)>1 else 'TWO_ENDED_CHECK_NORMAL.json')
output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
