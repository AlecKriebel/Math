#!/usr/bin/env python3
"""Exhaust exact necessary quotient spectra for the normalized tensor root."""
from itertools import product
from math import lcm
import json

D={1:1,16:1,17:3,30:2,34:1}
order=sum(d*d*m for d,m in D.items())
degrees=[16,17,30,34]
candidates=[]
examined=0
for multiplicities in product(*(range(D[d]+1) for d in degrees)):
    examined+=1
    quotient_order=1+sum(m*d*d for d,m in zip(degrees,multiplicities))
    present=[1]+[d for d,m in zip(degrees,multiplicities) if m]
    if order % quotient_order == 0 and quotient_order % lcm(*present)==0:
        candidates.append({'order':quotient_order,
                           'spectrum':{'1':1,**{str(d):m for d,m in
                              zip(degrees,multiplicities) if m}}})
assert examined==48
assert [x['order'] for x in candidates]==[1,order]
print(json.dumps({'input':D,'order':order,'submultisets_checked':examined,
                  'necessary_quotient_candidates':candidates,
                  'conditional_deduction':'Any finite group realizing the input spectrum is simple.',
                  'realizability':'Not established by this computation.'},indent=2,sort_keys=True))
