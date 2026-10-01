#!/usr/bin/env python3
"""Independent exact p=1 band check on infinitely many moving-cut fibers.
The loops are finite sanity checks; the displayed formulas establish the model.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def rho(n,k):return F(2)**(k-abs(n-k))
# W=N_0 with nu{k}=2^(-k-1); rho(0,k)=1. All adjacent density ratios
# lie between 1/2 and 2. The stable band is n<=k.
comparisons=0
for k in range(25):
 for n in range(-25,51):
  assert rho(0,k)==1
  assert F(1,2)<=rho(n+1,k)/rho(n,k)<=2
  assert min(rho(n-1,k),rho(n+1,k))<=rho(n,k)/2
  A=(rho(n-1,k)<=rho(n,k)/2)
  assert A==(n<=k)
  for m in range(9):
   ratio=rho(n-m,k)/rho(n,k) if A else rho(n+m,k)/rho(n,k)
   assert ratio==F(1,2)**m
   comparisons+=1
# At level n>=1, rho(n,0)=2^-n and rho(n,n)=2^n.
# Their ratio is 4^n, so bounded distortion cannot hold uniformly.
for n in range(1,20):assert rho(n,n)/rho(n,0)==4**n
out={'status':'passed','model':'countably many fibers with unbounded measurable cut k; nu{k}=2^(-k-1), rho(n,k)=2^(k-|n-k|)', 'exact_comparisons':comparisons,'p1_band_norm_ratio':'2^-m exactly','bounded_distortion_ratio':'4^n unbounded','scope':'finite sanity checks of a closed-form model; not a certificate for the general theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
