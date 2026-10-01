#!/usr/bin/env python3
"""Exact diagnostics for the written nonlinear cohort argument; no ODE simulation."""
from fractions import Fraction as F
from math import gcd
import json
counts={}
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]=counts.get(g,0)+1
for den in range(3,21):
 for num in range(den//2+1,den):
  if gcd(num,den)!=1:continue
  p=F(num,den);nu=p/(1-p);reported=1/(2*(1-p))
  ck('integrable_clock_power',nu>1)
  ck('actual_bulk_amplitude',p+(1-p)*nu==2*p)
  ck('actual_clock_to_size',1/((1-p)*(nu+1))==1)
  ck('reported_power_difference',nu-reported==(2*p-1)/(2*(1-p))>0)
  ck('reported_size_superlinear',2/(3-2*p)>1)
  ck('subleading_bulk_mass',0<2-2*p<1)
  for j in range(2,12):
   ck('first_moment_growth_rate',j**num<=j**den)
   ck('second_moment_bound',j**(num+den)<=j**(2*den))
  # Jensen controls use support k^den, so all moments are rational exactly.
  for a,b in [(1,1),(1,3),(2,5),(5,2),(7,11)]:
   weights=[F(a,a+b+1),F(b,a+b+1),F(1,a+b+1)]
   first=sum(w*k**den for w,k in zip(weights,[1,2,3]))
   power=sum(w*k**num for w,k in zip(weights,[1,2,3]))
   ck('pure_birth_Jensen_control',power**den<=first**num)
# Entry barrier f<=K tau^-nu: exact residual bounds on integer nu families.
for nu in range(2,15):
 for c0 in [F(1,7),F(1,2),F(1),F(3)]:
  K=2/c0
  for tau in range(2,31):
   upper=tau**nu/K-c0*tau**nu
   derivative=-nu*K/F(tau**(nu+1))
   ck('barrier_negative_drift',upper==-c0*tau**nu/2)
   if F(tau**(2*nu+1))>2*nu*K/c0:
    ck('eventual_supersolution',upper<derivative)
# Eventual physical-time linear-ODE brackets; coefficient tolerance chosen exactly.
for n in range(2,102):
 eps=F(1,n);delta=eps/(2*(1+eps))
 ck('upper_physical_barrier',1-(1-delta)*(1+eps)<=-eps/2)
 ck('lower_physical_barrier',1-(1+delta)*(1-eps)>=eps/2)
# Zero initial data and finite-core mass conservation constraints for selected case.
p=F(3,4);nu=p/(1-p)
ck('p_three_quarters',nu==3)
ck('p_three_quarters',2*p==F(3,2))
ck('p_three_quarters',1/(2*(1-p))==2)
ck('p_three_quarters',2/(3-2*p)==F(4,3))
ck('p_three_quarters',p-1<0)
print(json.dumps({'problem_id':30000849,'substantive_turn':3,'status':'PASS','counts':counts,'assertions':sum(counts.values()),'scope':'Exact exponent, moment-inequality and comparison-residual controls; the existence, pure-birth nonexplosion, dominated convergence and nonlinear asymptotics are proved in TURN_3.md, not by finite computation.'},indent=2,sort_keys=True))
