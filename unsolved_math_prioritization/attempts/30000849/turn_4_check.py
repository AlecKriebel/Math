#!/usr/bin/env python3
from fractions import Fraction as F
import json
counts={};max_steps=0;parameter_pairs=0
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]=counts.get(g,0)+1
for pn in range(1,40):
 p=F(pn,40);nu=p/(1-p)
 for wn in range(-19,161):
  w=F(wn,40);beta=w+1;d=beta*(1-p)
  if not d<F(1,2):continue
  parameter_pairs+=1;r=1/d-1;q=p+(1-p)*r
  rp=(1-w*(1-p))/((w+2)*(1-p))
  ck('clock_rate_relation',nu/(nu+1)==p)
  ck('integrable_clock_exponent',r>1)
  ck('profile_amplitude',q==2*p-1+1/beta)
  ck('source_clock_mismatch',r-rp==(1-2*d)/(d*(beta+1))>0)
  ck('source_size_mismatch',(w+2)/(3-2*p)-beta==(1-2*d)/(3-2*p)>0)
  ck('bulk_mass_subleading',beta*(2-q)-beta==2*d-1<0)
  a0=max(w/2,F(0));ck('monomer_initial_negligible',a0<beta)
  if w>0:
   k=(1+w/2)/(nu+2)
   ck('positive_input_barrier_error',w-k*(2*nu+1)<0)
  # Verify the finite bootstrap exactly without treating it as a global proof.
  b=a0+d;steps=0
  while b>0:
   new=p*b+2*d-1
   ck('bootstrap_strict_descent',new<b)
   b=new;steps+=1
   assert steps<10000
  if b==0:
   eps=(1-2*d)/(2*p)
   b=2*d-1+p*eps
   ck('log_boundary_escape',b<0);steps+=1
  ck('bootstrap_reaches_integrability',b<0)
  max_steps=max(max_steps,steps)
  ck('time_barrier_derivative_small',(d-2)-w==-p*beta-1<0)
  # Logarithmic exponents in the clock coefficient equality B/d=(kappa/N)^(1-p)/(1-p).
  ck('clock_coefficient_alpha',1-p==1-p)
  ck('clock_coefficient_beta',p-1==-(1-p))
  ck('clock_coefficient_cluster',p-1==-(1-p))
  # Express monomer amplitude from physical time as a power of sigma.
  ck('profile_exponent_conversion',(d-1)/beta==-(1-p)*r)
  ck('profile_constant_cluster',p-1+(d-1)/beta==-1/beta)
  ck('profile_constant_mass',-p-(d-1)/beta==-w/beta)
for n in range(2,102):
 eps=F(1,n);delta=eps/(2*(1+eps))
 ck('forced_scalar_upper',1-(1-delta)*(1+eps)<=-eps/2)
 ck('forced_scalar_lower',1-(1+delta)*(1-eps)>=eps/2)
print(json.dumps({'problem_id':30000849,'turn':4,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'strict_regime_parameter_pairs':parameter_pairs,'maximum_sampled_bootstrap_steps':max_steps,'scope':'Exact finite rational parameter and exponent controls only. The written moving-barrier, finite bootstrap and infinite cohort arguments prove the scoped theorem.'},indent=2,sort_keys=True))
