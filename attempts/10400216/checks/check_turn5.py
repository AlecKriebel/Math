#!/usr/bin/env python3
"""Exact Euler and inequality-direction controls for the conditional guts route."""
from collections import Counter
from itertools import product
from fractions import Fraction as F
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
# Arbitrary formal characteristic Euler data satisfying a nonnegative guts deficit.
for guts_deficit in range(0,31):
 for betas in product(range(0,9),repeat=3):
  beta=sum(betas);chiS=-guts_deficit-beta;chiSigma=-beta;chiG=-guts_deficit
  ck(chiS==chiG+chiSigma,'annular_frontier_Euler_additivity')
  ck(-chiG==-chiS-beta,'correct_product_subtraction')
  for a_loss,b_extra in [(0,0),(1,0),(0,1),(3,4)]:
   a=-chiS-a_loss;b=beta+b_extra
   ck(max(0,a-b)<=guts_deficit,'one_sided_safe_lower_bound')
# General nonzero-frontier Euler identity, keeping its sign explicit.
for chiS in range(-30,1):
 for chiSigma in range(-20,1):
  for chiA in range(-3,5):
   chiG=chiS-chiSigma+chiA
   ck(-chiG==-chiS+chiSigma-chiA,'general_frontier_correction_sign')
# Exact parallel-fiber padding cancellation.
for fiber_deficit in range(1,21):
 for m in range(1,101):
  surface_deficit=m*fiber_deficit;product_mass=m*fiber_deficit
  ck(surface_deficit-product_mass==0,'parallel_fibers_empty_guts')
  ck((m+1)*fiber_deficit>surface_deficit,'raw_Euler_unbounded_padding')
# Separate checkerboard bounds require the factor 1/2 when averaged.
for rB in range(2,102):
 for rW in range(2,102):
  t=rB+rW-2;dB=rW-2;dW=rB-2
  ck(dB+dW==t-2,'twist_reduced_guts_sum')
  ck(max(dB,dW)>=F(t-2,2),'correct_half_factor')
  # Doubling the cutting surface adds a product copy, not a second guts copy.
  for raw_deficit in [max(dB,dW),max(dB,dW)+7]:
   beta=raw_deficit-dB
   ck(2*raw_deficit-(beta+raw_deficit)==dB,'frontier_I_bundle_no_spurious_factor_two')
# A simple positive/negative direction control: partial product deletion can overestimate guts.
for true_product in range(1,51):
 raw=true_product+2
 ck(raw-(true_product-1)>raw-true_product,'underestimated_products_overestimate_deficit')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Euler identities, padding and inequality directions only. No program certifies an essential surface, a characteristic decomposition, or general-shadow coverage.'},indent=2))
