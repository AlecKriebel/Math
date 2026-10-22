#!/usr/bin/env python3
"""Independent finite probability/cut controls; analytic proof is in REPORT.md."""
import collections, datetime as dt, decimal, hashlib, itertools, json, math, platform
from fractions import Fraction as F
from pathlib import Path
OUT=Path(__file__).resolve().parent
counts=collections.Counter()
def check(condition,label):
 if not condition:raise AssertionError(label)
 counts[label]+=1
D=decimal.Decimal
decimal.getcontext().prec=100

# Count rectangles by direct integer size pairs, then independently by (minimum,
# complement-of-maximum). No import from author or historical reviewer code.
size_pairs=0
for k in range(1,161):
 by_q=collections.Counter();positive=0
 for a in range(k+1):
  for d in range(k+1):
   if a+d<=k:continue
   area=a*d; rhs=k*(a+d-k);size_pairs+=1
   check(area-rhs==(k-a)*(k-d),'exact_rectangular_surplus_identity')
   q=min(a,d);ell=k-max(a,d)
   check(0<=ell<q,'positive_cut_parameter_range')
   check(area==q*(k-ell),'area_reparameterization')
   multiplicity=math.comb(k,a)*math.comb(k,d);positive+=multiplicity
   by_q[q]+=multiplicity
   if 2*q<=k:check(2*area>=q*k,'small_cut_area_bound')
   else:check(4*area>k*k,'large_cut_area_bound')
 check(positive==(4**k-math.comb(2*k,k))//2,'total_positive_cut_count')
 for q in range(1,k//2+1):
  independent=sum((1 if q==k-ell else 2)*math.comb(k,q)*math.comb(k,ell) for ell in range(q))
  check(by_q[q]==independent,'independent_minimum_size_multiplicity')
  check(by_q[q]<=2*q*k**(2*q),'small_cut_count_majorant')
# Actually enumerate ALL subset pairs for small k, independently of binomials.
for k in range(1,7):
 sets=[{i for i in range(k) if m&(1<<i)} for m in range(1<<k)]
 direct=collections.Counter((len(A),len(B)) for A in sets for B in sets if len(A)+len(B)>k)
 for (a,d),value in direct.items():check(value==math.comb(k,a)*math.comb(k,d),'literal_subset_count')

# High-precision controls supplement derivative/integral inequalities proved in
# the report. The smallest delta values expose cancellation if evaluated naively.
tail_cases=[]
for frac in [F(1,10**12),F(1,10**8),F(1,10000),F(1,100),F(1,10),F(1,4),F(1,2),F(3,4),F(99,100),F(999999,1000000)]:
 delta=D(frac.numerator)/D(frac.denominator)
 upper=delta/(1-delta)+(1-delta).ln()
 lower=(1+delta).ln()-delta/(1+delta)
 check(upper>=delta*delta/2,'upper_gamma_tail_rate_constant')
 check(lower>=delta*delta/8,'lower_gamma_tail_rate_constant')
 tail_cases.append({'delta':str(frac),'upper_I':str(upper),'lower_I':str(lower)})
# Mutation: confusing the lower-tail constant with the upper one is invalid.
delta=D('0.5');lower=(1+delta).ln()-delta/(1+delta)
check(lower<delta*delta/2,'reject_wrong_lower_tail_half_constant')
# The generic elementary Chernoff bound is also independently recovered from
# a Poisson upper-tail MGf, using the Gamma-Poisson identity for integer shapes.
# P(Gamma(n)<=x)=P(Poisson(x)>=n) <= exp(-n log(n/x)+n-x).
poisson_cases=[]
for n in [1,2,3,8,16,64]:
 for frac in [F(1,10),F(1,2),F(9,10)]:
  a=D(frac.numerator)/D(frac.denominator);x=D(n)*a
  gamma_rate=D(n)*(a-1-a.ln())
  poisson_rate=D(n)*(D(n)/x).ln()-D(n)+x
  check(abs(gamma_rate-poisson_rate)<D('1e-95'),'independent_Poisson_Gamma_rate_identity')
  # Positive Poisson tail summation avoids subtracting two nearly equal numbers.
  term=(-x).exp()*x**n/D(math.factorial(n));tail=term;j=n
  while True:
   j+=1;term*=x/D(j);tail+=term
   if term<tail*D('1e-90'):break
   check(j<10000,'positive_series_termination')
  bound=(-gamma_rate).exp()
  check(tail<=bound,'Poisson_positive_series_below_Chernoff')
  poisson_cases.append({'shape':n,'a':str(frac),'gamma_lower_tail_approx':str(tail),'chernoff_bound':str(bound)})
# Candidate constants obtained algebraically, with exact integer arithmetic.
check(1-8**2//2==-31,'subcritical_power_exponent')
check(F(2)-F(8**2,16)==-2,'small_cut_power_exponent')
windows=[]
for p in range(1,24):
 k=2**p;delta=8*math.sqrt(math.log(k)/k)
 if delta<1:
  log_large=k*(math.log(4)-2*math.log(k))
  epsilon=2*k**(-31)+2*k**(-2)/(1-k**(-2))**2+(math.exp(log_large) if log_large>-745 else 0)
  windows.append({'k':k,'delta':delta,'explicit_failure_bound_float':epsilon,'large_term_log':log_large,'large_term_may_underflow_in_display':log_large<=-745})
check(windows[0]['k']==512,'first_power_of_two_with_delta_below_one')
# Finite root/leaf capacities and microscopic variance are separately checkable.
for H in range(2,14):
 k=2**(H-1)
 check(4*k-1==2**(H+1)-1,'physical_vertex_count')
 check(2*k*k>=2*k,'top_versus_terminal_capacity')
# Critical finite controls: identical positive slopes x force a kink at 1+1/x,
# which need not be2. This prevents an accidental universal finite critical claim.
for x in [F(1,3),F(1),F(3)]:
 tau=1+1/x
 check(1+(tau-1)*x==2,'finite_synchronized_kink_location')
check(1+1/F(3)!=2,'reject_universal_finite_kink_at_two')
result={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'python':platform.python_version(),'independent_of_author_and_historical_reviewer_code':True,'all_assertions_passed':True,'size_pairs_checked':size_pairs,'check_counts':dict(counts),'assertions':sum(counts.values()),'tail_rate_cases':tail_cases,'Poisson_Gamma_controls':poisson_cases,'window_diagnostics':windows,'scope':'Finite and high-precision controls supplement the analytic proof. Decimal probability sums and floats are diagnostics, not validated interval certificates or proof of an asymptotic theorem. No critical-window exponent or novelty conclusion.'}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_assertions_passed':True,'assertions':result['assertions'],'size_pairs_checked':size_pairs,'check_counts':dict(counts),'first_window':windows[0]},indent=2))
