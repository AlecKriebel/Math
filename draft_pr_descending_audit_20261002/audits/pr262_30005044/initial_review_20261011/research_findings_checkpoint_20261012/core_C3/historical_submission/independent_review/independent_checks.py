#!/usr/bin/env python3
"""Independent exact finite controls. Infinite conditioning/limit steps are reviewed in prose."""
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
import json
C=Counter()
def ck(p,k):
 C[k]+=1
 if not p:raise AssertionError(k)
# Root event and all-stage scaling are exact at fourth powers.
ck(F(1,4)**4*256==1,'root_tail_fourth_power')
for n in range(160):
 D=2**(4*n+8); nextD=2**(4*n+12); tail=F(1,2**(n+3));x=F(1,2**(n+2))
 ck(tail**4*nextD==1,'child_tail')
 lower=tail*x/2
 ck(D*lower==2**(2*n+2),'stage_success_intensity')
 ck(2**(2*n+2)>=4*(n+1),'geometric_failure_majorant')
 ck(0<x<=1 and x-x*x/2>=x/2,'exponential_lower_bound_polynomial')
# Exact Taylor-polynomial majorization step for the whole unit interval grid.
for j in range(1,513):
 x=F(j,512)
 ck(1-x+x*x/2<1 and x-x*x/2>=x/2,'Taylor_algebra_control')
# Finite sums plus their exact infinite remainder, not a numerical truncation.
for L in range(1,161):
 fail=sum((F(1,16**j) for j in range(1,L+1)),F(0));rem=F(1,15*16**L)
 ck(fail+rem==F(1,15),'failure_series_with_exact_remainder')
 ck(F(1,4)*(1-fail-rem)==F(7,30),'ray_probability_constant')
 # E xi >= M*P(xi>=M) at M=16^L; the resulting lower bounds diverge.
 M=16**L;tail=F(1,2**L)
 ck(tail**4*M==1 and M*tail==8**L,'infinite_mean_lower_bound')
# Explore tree/arrow/recovery toy cylinders by exact enumeration.
# State=(large degree, incoming arrow, outgoing fresh probe, recovery-free flag).
states=list(product((0,1),repeat=4));enumerated=0;selected_histories=0
for D in range(1,5):
 tab=defaultdict(Counter);success=0
 for config in product(states,repeat=D):
  enumerated+=1
  index=next((i for i,s in enumerate(config) if s[0] and s[1]),None)
  if index is None:continue
  success+=1
  # Condition on all data actually used to select, not only on success.
  observed=tuple((s[0],s[1]) for s in config)
  tab[(observed,index)][(config[index][2],config[index][3])]+=1
 ck(F(success,16**D)==1-F(3,4)**D,'first_eligible_selection_probability')
 for (history,index),outcomes in tab.items():
  selected_histories+=1;total=sum(outcomes.values())
  ck(history[index]==(1,1),'selected_degree_bias')
  ck(all(F(outcomes[outcome],total)==F(1,4) for outcome in product((0,1),repeat=2)),'fresh_outgoing_and_recovery_conditioning')
# Different positive rates share the same dimensionless arrow schedule.
for rate in [F(1,37),F(2,9),F(1),F(9,4),F(101)]:
 tau=1/(2*rate);times=[tau*(1-F(1,2**n)) for n in range(65)]
 for depth in (1,2,3,8,16,32,64):
  guards=[(F(0),tau)]+[(times[n-1],tau) for n in range(1,depth+1)]
  total=sum((b-a for a,b in guards),F(0))
  ck(total+2*tau/F(2**depth)==3*tau,'recovery_product_exact_tail')
  # Choose varying rational arrow locations within their deterministic windows.
  arrow=[]
  for n in range(depth):
   fraction=F((n%5)+1,7)
   t=times[n]+fraction*(times[n+1]-times[n]);arrow.append(t)
   ck(rate*(times[n+1]-times[n])==F(1,2**(n+2)),'dimensionless_arrow_window')
   ck(times[n]<t<times[n+1],'arrow_inside_stage')
  arrival=[F(0)]+arrow
  for n in range(depth+1):
   a,b=guards[n]
   ck(a<=arrival[n]<b==tau,'arrival_guarded_until_common_horizon')
   if n<depth:ck(arrival[n]<=arrow[n]<tau,'finite_infection_path_order')
# Negative control: a fast infinite ray alone need not leave any infection at its limit.
# For finite prefixes choose a recovery after the outgoing arrow but before tau.
tau=F(1);t=[1-F(1,2**(n+1)) for n in range(130)]
for n in range(128):
 recovery=(t[n+1]+tau)/2
 ck(t[n]<t[n+1]<recovery<tau,'fast_ray_without_simultaneous_survival_control')
# Quenched inheritance strictly contracts the bad probability for a nontrivial positive law.
# Test arbitrary finite mixtures; the proof uses the same pointwise bound for the full law.
for denom in range(2,41):
 for num in range(1,denom):
  bad=F(num,denom)
  for law in [{1:F(1,2),2:F(1,2)},{1:F(1,7),3:F(2,7),8:F(4,7)},{2:F(1)}]:
   ck(sum(p*bad**d for d,p in law.items())<bad,'quenched_bad_probability_strictness')
ck(F(1,4)*(1-F(1,15))==F(7,30),'final_annealed_coefficient')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'toy_cylinders_enumerated':enumerated,'conditioned_selection_histories':selected_histories,'result_coefficient':'7/30','horizon':'1/(2 lambda)','recovery_exponent':'3/(2 lambda)','scope':'Finite rational and cylinder controls only. No stochastic simulation, and no computational replacement for countable conditional products, infinite ray construction, or the hereditary quenched proof.'},indent=2,sort_keys=True))
