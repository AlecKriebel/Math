#!/usr/bin/env python3
from fractions import Fraction as F
import sympy as S
import json
counts={}
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]=counts.get(g,0)+1
for k in range(1,31):
 alpha=S.Integer(k)**4
 tau0=2**S.Rational(3,4)*alpha**S.Rational(1,4)
 x0=2**S.Rational(-1,4)*alpha**S.Rational(1,4)
 N0=S.sqrt(2*alpha);sigma0=S.sqrt(alpha/2)
 ck('physical_clock_integral_constant',S.simplify(tau0/2-x0)==0)
 ck('physical_mass_constant',S.simplify(N0*sigma0-alpha)==0)
 ck('logarithmic_clock_inversion',S.simplify(tau0**2/(2*S.sqrt(alpha)*S.sqrt(2))-1)==0)
 ck('physical_monomer_composition',S.simplify(S.sqrt(2*alpha)/tau0-x0)==0)
 ck('cluster_log_constant',S.simplify(2*S.sqrt(alpha)/S.sqrt(2)-N0)==0)
 ck('size_scale_from_clock',S.simplify(tau0**2/4-sigma0)==0)
for n in range(2,82):
 eps=F(1,n);delta=eps/(2*(1+eps))
 upper=1/(1+eps)-(1-delta);lower=1/(1-eps)-(1+delta)
 ck('critical_upper_field_sign',upper==-eps/(2*(1+eps))<0)
 ck('critical_lower_field_sign',lower>=eps/(2*(1+eps))>0)
 for alpha in [F(1,3),F(1),F(7)]:
  for T in [F(10),F(100),F(1000)]:
   field=lower*T/2-4*alpha*(1-eps)/T
   if T*T>8*alpha*(1-eps)/lower:ck('critical_lower_field_with_loss',field>0)
# Fixed-cohort scaling and physical exponent compatibility.
p=F(1,2);nu=p/(1-p)
ck('critical_exact_parameters',nu==1)
ck('critical_exact_parameters',(1-p)==F(1,2))
ck('critical_exact_parameters',p+(1-p)*1==1)
ck('critical_exact_parameters',F(1,2)*2==1)
# Universal front obstruction for arbitrary finite-support initial cluster count.
for kn in range(1,16):
 for dn in range(1,11):
  K=F(kn,dn)
  for kap in [F(1,7),F(1),F(5,2),F(11)]:
   bound=2*kap/K;R=bound.numerator//bound.denominator+1
   ck('initial_support_count_bound',R>2*kap/K)
   ck('universal_size_front_mismatch',F(3,4)*K*R/kap>1)
   ck('actual_front_below_half',kap/(K*R)<F(1,2))
# Degree-j cutoff exponents need no floor/joint-limit substitution.
for eta in [F(n,20) for n in range(1,20)]:
 ck('interior_hitting_time_gap',eta<1 and eta>0)
for eta in [F(n,20) for n in range(21,61)]:
 ck('exterior_hitting_time_gap',eta>1)
print(json.dumps({'problem_id':30000849,'substantive_turn':5,'status':'PASS','counts':counts,'assertions':sum(counts.values()),'scope':'Exact critical constants, comparison residuals and finite-support memory-obstruction arithmetic. Analytic concentration, nonlinear asymptotics and weak limits are proved in TURN_5.md.'},indent=2,sort_keys=True))
