#!/usr/bin/env python3
"""Exploratory floating-point search; no finite scan certifies an upper bound."""
import json
from pathlib import Path
import numpy as np

rng=np.random.default_rng(30004563)
grid=np.geomspace(1e-20,1e30,1001)[None,:]
best=0
hist={}
records=[]
for batch in range(120):
    count=1000
    # Reorder foci so that the common focus has the smallest radius;
    # rescale lengths so that the larger additive level is one.
    p=rng.uniform(.06,1.96,(count,1))
    lam=10**rng.uniform(-12,0,(count,1))
    B=10**rng.uniform(-2.5,2.5,(count,1))
    cx=rng.normal(0,1,(count,1))*10**rng.uniform(-2.5,2.5,(count,1))
    cy=10**rng.uniform(-3,2.5,(count,1))
    z=grid**p
    dl=z*np.expm1(p*np.log1p(lam/grid))
    dm=z*np.expm1(p*np.log1p(1/grid))
    x=(B*B-dl)/(2*B)
    y=(cx*cx+cy*cy-dm-2*cx*x)/(2*cy)
    # Normalized residual has the same sign and avoids enormous powers.
    g=(x*x+y*y)/z-1
    changes=(np.signbit(g[:,1:])!=np.signbit(g[:,:-1])).sum(axis=1)
    for value,n in zip(*np.unique(changes,return_counts=True)):
        hist[int(value)]=hist.get(int(value),0)+int(n)
    for row in np.where(changes>best)[0]:
        val=int(changes[row])
        if val<=best:continue
        best=val
        roots=np.where(np.signbit(g[row,1:])!=np.signbit(g[row,:-1]))[0]
        rec={'sample':batch*count+int(row),'sign_changes':best,
             'p':float(p[row,0]),'alpha':float(2/p[row,0]),
             'lambda':float(lam[row,0]),'mu':1.,
             'B':float(B[row,0]),'cx':float(cx[row,0]),'cy':float(cy[row,0]),
             'brackets':[[float(grid[0,j]),float(grid[0,j+1])] for j in roots]}
        records.append(rec)
        print('NEW BEST',json.dumps(rec),flush=True)
    if best>=5:break
    if batch%20==0:print('PROGRESS',batch,dict(sorted(hist.items())),flush=True)
out={'samples':sum(hist.values()),'maximum_detected_sign_changes':best,
     'histogram':hist,'record_candidates':records,
     'seed':30004563,'method':'1001 logarithmic samples s in [1e-20,1e30]',
     'status':'Exploration only; sign changes need high-precision/exact validation',
     'limitations':'Can miss close, tangent, or out-of-range roots; no upper-bound conclusion'}
Path(__file__).with_name('turn2_numerical_search.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2),flush=True)
