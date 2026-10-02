#!/usr/bin/env python3
"""Exact model subarc and first-exit controls; no effective Baire claim."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
def arc(t,d):return (t,t**d)
def dist2(x,y):return sum((a-b)**2 for a,b in zip(x,y))
models=0
for degree in range(1,6):
    for den in range(2,9):
        for i,j in combinations(range(den+1),2):
            a,b=F(i,den),F(j,den);u=a+(b-a)/3;q=(a+u)/2
            x,y=arc(a,degree),arc(b,degree);exitpoint=arc(u,degree);witness=arc(q,degree)
            radius2=dist2(x,exitpoint)
            ck('nondegenerate_chart_interval',a<q<u<b)
            ck('injective_chart_first_coordinate',witness[0]==q and x[0]!=exitpoint[0])
            ck('strict_exit_radius',0<radius2<dist2(x,y))
            # Parameter path waits until time1/2, then traverses the arc;
            # it first reaches parameter u at time2/3.
            tt=F(2,3);param=a+(b-a)*max(F(0),2*tt-1)
            ck('plateau_path_exit_time',param==u)
            for k in range(8):
                time=F(k,12)
                if time<tt:
                    v=a+(b-a)*max(F(0),2*time-1)
                    ck('earlier_path_inside_ball',dist2(x,arc(v,degree))<radius2)
            ck('rational_chart_witness_inside',dist2(x,witness)<radius2)
            ck('witness_in_unit_square',all(0<=z<=1 for z in witness))
            if degree>=2:
                chordmid=tuple((l+r)/2 for l,r in zip(x,exitpoint))
                ck('arc_not_confused_with_straight_chord',witness[1]<chordmid[1])
            models+=1
print(json.dumps({'problem_id':30003661,'turn':5,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'rational_curved_arc_models':models,'arithmetic':'exact rational arithmetic only',
    'scope':'Model subarc/first-exit controls only. Countable-cover and residual conclusions use the separate classical Baire proof; no computable selection of an arc index, path or Baire witness is claimed.'},indent=2,sort_keys=True))
