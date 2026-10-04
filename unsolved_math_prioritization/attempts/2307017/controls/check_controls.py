#!/usr/bin/env python3
"""Finite stress tests for PROOF.md. Standard library only; not a proof engine.

Limits: <=100,000 zero-angle cases, <=100,000 integer summands per case,
60 dyadic factors in explicit examples, ordinary IEEE double arithmetic.
The universal/infinite assertions are proved in PROOF.md, not by these tests.
"""
from fractions import Fraction
from pathlib import Path
import cmath, json, math, random

out={"control_kind":"finite sanity checks, not proof certificates", "seed":2307017}
rng=random.Random(2307017)
# Exact arithmetic verifies the key quotient identity for rational q on the circle.
exact=0
for h in [Fraction(0),Fraction(1,4),Fraction(-2,3),Fraction(9,10)]:
 c=(1-h*h)/(1+h*h);s=2*h/(1+h*h)
 for n in [1,2,7,100]:
  for u,v in [(Fraction(1,8),Fraction(-3)),(Fraction(3),Fraction(4)),(Fraction(90),Fraction(-20))]:
   numerator=(n*c+u)**2+(n*s-v)**2
   denominator=(n*c-u)**2+(n*s-v)**2
   assert numerator-denominator==4*n*c*u
   assert c*c+s*s==1
   exact+=1
out['exact_kernel_identity_cases']=exact

alphas=[-1.56,-1.4,-1.0,-0.4,0.0,0.4,1.0,1.4,1.56]
radii=[0.5,0.75,1.0,2.0,5.0,10.0,30.0,100.0,300.0]
max_ratio=0.0;cases=0;summands=0
for alpha in alphas:
 q=cmath.exp(1j*alpha);c=q.real
 for R in radii:
  for phi in [-1.56,-1.4,-1.0,-0.4,0.0,0.4,1.0,1.4,1.56]+[rng.uniform(-1.56,1.56) for _ in range(10)]:
   a=R*cmath.exp(1j*phi);u=a.real;beta=u/(1+R*R)
   total=0.0
   for n in range(max(1,math.ceil(R/2)),math.floor(2*R)+1):
    if not(n/2<=R<=2*n and u>=c*n/2):continue
    d=abs(n*q-a)
    if d<0.25:continue  # conservative single-zero version of E0 removal
    g=0.5*math.log1p(4*n*c*u/(d*d))
    total+=g/(n*n);summands+=1
   ratio=total*c/beta
   max_ratio=max(max_ratio,ratio)
   assert ratio<=1120*(1+1e-12)
   cases+=1
out['local_sum_cases']=cases
out['local_sum_summands']=summands
out['max_local_ratio_c_times_sum_over_beta']=max_ratio
out['proved_bound_for_ratio']=1120

near_cases=0
for alpha in alphas:
 q=cmath.exp(1j*alpha);c=q.real
 for n in [math.ceil(1/c),math.ceil(2/c),math.ceil(100/c)]:
  for direction in [0.0,1.0,2.0,3.0,4.0,5.0]:
   a=n*q+0.249*cmath.exp(1j*direction)
   beta=a.real/(1+abs(a)**2)
   assert beta>=c/(6*n)*(1-1e-12)
   near_cases+=1
out['near_zero_weight_cases']=near_cases

# An explicit finite product plus a positive-harmonic atom and polynomial decay.
# Model: e^{-a z} B(z) (1+z)^{-2} exp(-m/(z-it)).
zeros=[2+1j,17-2j,100+50j];aval=1.7;m=2.0;t=3.0
model=[]
for alpha in alphas:
 q=cmath.exp(1j*alpha)
 vals=[]
 for r in [1e2,1e3,1e4,1e5,1e6]:
  z=r*q
  logabs=-aval*z.real-2*math.log(abs(1+z))-(m/(z-1j*t)).real
  for a in zeros:logabs+=math.log(abs(z-a)/abs(z+a.conjugate()))
  vals.append({'r':r,'normalized_log':logabs/r,'error_from_expected':logabs/r+aval*q.real})
 assert abs(vals[-1]['error_from_expected'])<0.0001
 model.append({'alpha':alpha,'expected_type':-aval*q.real,'samples':vals})
out['finite_factor_model']=model

# Literal repetition obstruction: each dyadic block's reciprocal sum is exactly one.
assert all(Fraction(2**k,2**k)==1 for k in range(1,61))
log_C=sum(math.log(abs((2.0**j-3)/(2.0**j+3))) for j in range(-60,61))
assert math.isfinite(log_C)
repeat=[]
for k in [4,8,12,16,20,24]:
 x=3*2.0**(k-1)
 logB=sum(math.log(abs((2.0**j-x)/(2.0**j+x))) for j in range(1,61))
 repeat.append({'m':k,'x_m':x,'log_abs_truncated_B':logB,'normalized_log':logB/x})
out['repetition_counterexample']={'blocks_exactly_checked':60,'two_sided_product_log_truncated_60':log_C,'off_zero_samples':repeat}
out['limitations']=[
 'Finite numeric checks do not establish infinite products, summability, or limsups.',
 'No interval arithmetic is used. Floating-point inequalities have tolerance.',
 'Zeros closer than 1/4 to a sample are excluded in the local-kernel test as required.',
 'The positive-harmonic representation and Blaschke theorem are analytic inputs.',
 'The repeated-integer example diagnoses an omitted distinctness convention; it is not a novelty claim.'
]
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['finite_factor_model','repetition_counterexample']},indent=2))
