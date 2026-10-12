#!/usr/bin/env python3
"""Exact control of each algebraic inequality used in universal union proof."""
from fractions import Fraction as Q
from itertools import product
import json

def main():
    count=0; high=0; degenerate=0
    for denom in range(1,19):
        for numer in range(denom+1):
            w=Q(numer,denom);s=1-w
            for p,z in product((Q(i,12) for i in range(13)),repeat=2):
                # p is dominant child's density; z aggregates the other-child cap.
                x=w*w*p+s*s*z
                count+=1
                if x<=Q(1,2):continue
                # For binary masses the dominant is max(w,s); retain the w-largest controls.
                if w<s:continue
                high+=1
                assert w>=x and w>Q(1,2)
                assert p >= (x-s*s)/(w*w) >= x
                q=1-x
                assert s<=q
                # Symbolically replacing F(x) by its smallest permitted value.
                flo=Q(3,2)*q*q
                gap=(1-w**4)*flo-Q(3,8)*s**4
                claimed=Q(3,8)*s*q*q*(4-q)
                assert gap>=claimed
                if s>0 and q>0:assert claimed>0
                else:degenerate+=1
    # Deterministic asymptotic degeneration: positive strict gap can approach zero.
    seq=[]
    x=Q(3,5);q=1-x
    for m in (4,8,16,64,256,1024):
        w=1-Q(1,m)
        # A single large child plus a completely empty small child has feasible p=x/w².
        p=x/w**2
        if p>1:continue
        gap=Q(3,8)*(1-w)*q*q*(4-q)
        assert gap>0
        seq.append({'m':m,'mass':str(w),'internal_edge':str(p),'certified_gap':str(gap)})
    print(json.dumps({'status':'PASS','parameter_tuples':count,'high_density_largest_child_tuples':high,'degenerate_endpoint_tuples':degenerate,'varying_mass_gap_sequence':seq,'scope':'exact union algebra; no universal claim inferred from finite grid'},indent=2))
if __name__=='__main__':main()
