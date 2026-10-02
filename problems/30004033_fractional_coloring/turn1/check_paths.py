#!/usr/bin/env python3
"""Exact supplementary checks; no graph library or floating-point arithmetic."""
from fractions import Fraction as F
from itertools import combinations
import json

def interval(length,r):
    k=length//2
    return (max(F(0),(2*k+1)*r-k),r) if length%2==0 else (F(0),min(r,k*(1-2*r)))

def check():
    counts={'palette_reachability_assertions':0,'rational_recurrence_assertions':0}
    configs=0; terminal_tests=0
    for m in range(2,11):
        for a in range(1,m//2+1):
            masks=[sum(1<<i for i in c) for c in combinations(range(m),a)]
            origin=masks[0]
            adjacency={b:[c for c in masks if not b&c] for b in masks}
            reached={origin}; configs+=1
            for length in range(1,13):
                reached={c for b in reached for c in adjacency[b]}
                lo,hi=interval(length,F(a,m))
                expected={b for b in masks if lo<=F((origin&b).bit_count(),m)<=hi}
                assert reached==expected,(m,a,length,lo,hi)
                counts['palette_reachability_assertions']+=1
                terminal_tests+=len(masks)
    for denominator in range(2,51):
        for numerator in range(denominator//2+1):
            r=F(numerator,denominator); lo=hi=F(0)
            for length in range(1,31):
                assert (lo,hi)==interval(length,r)
                counts['rational_recurrence_assertions']+=1
                lo,hi=max(F(0),3*r-1-hi),r-lo
    for length,expected in [(1,(0,0)),(2,(F(1,8),F(3,8))),(3,(0,F(1,4))),(4,(0,F(3,8))),(5,(0,F(3,8)))]:
        assert interval(length,F(3,8))==expected
    counts['target_signature_assertions']=5
    return {'status':'pass','assertions':sum(counts.values()),'breakdown':counts,'palette_configurations':configs,'individual_terminal_comparisons':terminal_tests,'limits':'Palettes 2..10; lengths 1..12; rational denominators 2..50 and lengths 1..30. Universal claim rests on the written induction.'}

if __name__=='__main__': print(json.dumps(check(),indent=2,sort_keys=True))
