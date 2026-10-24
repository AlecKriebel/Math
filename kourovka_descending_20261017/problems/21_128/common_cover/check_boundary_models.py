#!/usr/bin/env python3
"""Rank2/3 independent integer controls for the log-intersection formula."""
from itertools import combinations
from collections import Counter
from math import gcd
from functools import reduce
from pathlib import Path
import json

def canon(v):
    g=reduce(gcd,map(abs,v))
    if not g:return None
    v=tuple(x//g for x in v)
    if next(x for x in v if x)<0:v=tuple(-x for x in v)
    return v
def cross(a,b):return canon((a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]))
def model(typ):
    rs={(1,0,0),(0,1,0),(0,0,1)}
    for i,j in combinations(range(3),2):
        for s in ((-1,) if typ=='A3' else (-1,1)):
            rs.add(tuple(1 if k==i else s if k==j else 0 for k in range(3)))
    rs=sorted(rs);points={}
    for a,b in combinations(rs,2):
        v=cross(a,b)
        points[v]={i for i,r in enumerate(rs) if sum(x*y for x,y in zip(v,r))==0}
    n=len(rs);hist=Counter(map(len,points.values()))
    volume=(n-3)**2-sum((len(p)-2)**2 for p in points.values())
    euler=3-2*n+sum(len(p)-1 for p in points.values())
    return {'N':n,'point_multiplicities':dict(sorted(hist.items())),
            'log_divisor_square':volume,'euler':euler}

out={'rank3':{t:model(t) for t in ('A3','B3')},
     'rank2':{'N_values':list(range(2,11)),'log_degrees':[n-2 for n in range(2,11)]}}
assert out['rank3']['A3']['log_divisor_square']==5
assert out['rank3']['B3']['log_divisor_square']==20
assert out['rank3']['B3']['euler']==4*out['rank3']['A3']['euler']
Path(__file__).with_name('boundary_model_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
