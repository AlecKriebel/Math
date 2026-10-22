#!/usr/bin/env python3
"""Finite exact algebra/bookkeeping controls, not stochastic convergence certificates."""
from fractions import Fraction as Q
from pathlib import Path
import json,random
R=random.Random(30005454);counts={}
def ck(name,v):
 assert v,name;counts[name]=counts.get(name,0)+1
# Harmonic generator: a jump from n to n+1 has increment 1/n.
for n in range(1,101):
 for left,right in [(1,1),(2,5),(19,3)]:
  lam=Q(n,left+n)+Q(n,n+right)
  ck('harmonic_generator',lam/Q(n)==Q(1,left+n)+Q(1,n+right))
# Spatially averaged algebra on even cycles checks the identities under a
# stationary law. The general stochastic arguments remain in the turn files.
for L in range(4,22,2):
 for trial in range(20):
  z=[Q(R.randrange(1,10),R.randrange(1,8)) for _ in range(L)];mean=sum(z)/L;z=[v/mean for v in z]
  T=[z[i]+z[(i+1)%L] for i in range(L)];r=[1/T[i-1]+1/T[i] for i in range(L)];lam=[z[i]*r[i] for i in range(L)];g=[v-1 for v in r];u=[(-1)**i*(z[i]-1) for i in range(L)];flux=[(-1)**i*(1/T[i]-Q(1,2)) for i in range(L)]
  ck('mean_intensity_one',sum(lam)==L)
  ck('pair_mean_two',sum(T)==2*L)
  ck('log_pair_dissipation',sum((lam[i]+lam[(i+1)%L])/T[i] for i in range(L))-L==sum(z[i]*g[i]**2 for i in range(L)))
  ck('harmonic_entropy_identity',2*sum(1/v for v in T)-L==sum((v-2)**2/(2*v) for v in T))
  for i in range(L):
   heat=z[i]*(u[i-1]-u[i])/(2*T[i-1])+z[i]*(u[(i+1)%L]-u[i])/(2*T[i])
   ck('staggered_diffusion',(-1)**i*z[i]*g[i]==heat)
   ck('conservative_log_flux',(-1)**i*g[i]==flux[i]-flux[i-1])
   ck('paired_directed_coefficients',z[i]/(2*T[i])+z[(i+1)%L]/(2*T[i])==Q(1,2))
# Every interior reciprocal cancels from an even alternating harmonic block.
for L in range(2,102,2):
 coefficients={i:0 for i in range(-1,L)}
 for i in range(L):
  coefficients[i-1]+=(-1)**i;coefficients[i]+=(-1)**i
 ck('even_block_flux_telescopes',coefficients[-1]==1 and coefficients[L-1]==-1 and all(coefficients[i]==0 for i in range(L-1)))
# Count bookkeeping for arbitrary prescribed firings, not a stochastic sample.
N={i:1 for i in range(-21,22)};P={i:0 for i in range(-20,22)}
for step in range(600):
 v=R.randrange(-20,22);P[v]+=1;e=v-R.randrange(2);N[e]+=1
 for i in range(-19,20):
  ck('individual_clock_upper',N[i]<=1+P[i]+P[i+1])
  ss=N[i]+N[i+1]
  ck('own_clock_pair_lower',ss>=2+P[i+1])
  ck('three_clock_pair_upper',ss<=2+P[i]+P[i+1]+P[i+2])
# Symbolic exponent arithmetic underlying the selected-time summable estimates.
ck('martingale_summable_exponent',3+Q(2,2)==4)
ck('local_error_summable_exponent',3-Q(16,2)==-5)
ck('rounding_error_summable_exponent',-Q(16,2)-1==-9)
ck('boundary_summable_exponent',-3<-1)
result={'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'method':'Rational local-generator, finite-cycle averaged identities, telescoping, and deterministic count bookkeeping','limits':'These finite controls do not prove infinite-volume martingale convergence, asymptotic continuity, or the a.s. subsequence theorem. Those arguments are written explicitly and require independent review. No WARM simulation or numerical evidence is used as a proof.'}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
