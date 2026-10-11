#!/usr/bin/env python3
"""Independent surface-Euler arithmetic, not a proof of the signature theorem."""
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
surface_types=[(g,r) for g in range(4) for r in range(1,5)]
for b0 in range(1,4):
 for data in product(surface_types,repeat=b0):
  chi=sum(2-2*g-r for g,r in data)
  beta=sum(2*g+r-1 for g,r in data)
  boundary=sum(r for g,r in data)
  ck(chi==b0-beta,'componentwise_Euler_identity')
  ck(chi<=boundary,'Euler_upper_bound')
  for constant in (24,48):
   least_sigma=(beta+constant-1)//constant
   ck(chi>=1-constant*least_sigma,'published_bound_implication')
   ck(chi>=-constant*abs(least_sigma),'empty_compatible_weaker_bound')
for k in range(1,101):
 ck(k>=1 and k!=1-0 if k>1 else k==1-0,'unlink_identity_trap')
 # Connected spanning surfaces for the unlink could have Euler 2-k:
 # this would have no lower bound at fixed signature if connectivity were imposed.
 ck((2-k)<1 if k>1 else (2-k)==1,'connected_unlink_convention_countercontrol')
# The elementary implication only needs one beta-minimizing admissible surface;
# it does not postulate that Euler and beta attain their extrema together.
for beta in range(41):
 for b0 in range(1,7):
  chi_witness=b0-beta
  for extra_euler in range(4):
   chi_max=chi_witness+extra_euler
   ck(chi_max>=1-beta,'separate_optimizers_suffice')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Conditional integer bookkeeping and convention countercontrols only. All topology and the all-positive-link signature bound remain credited primary-source inputs.'},indent=2))
