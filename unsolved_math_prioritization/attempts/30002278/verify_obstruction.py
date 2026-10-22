#!/usr/bin/env python3
"""Exact algebraic checks for the scoped variable-profile Lyapunov obstruction.

No discretized unstable eigenvalue or PDE instability is inferred. The function
space smoothing, high-frequency necessity and short-time solution arguments are
proved in OBSTRUCTION.md; these finite controls check their algebraic inputs.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
checks=Counter()
def req(v,label):
 assert v,label
 checks[label]+=1

def dot(a,b):return sum(x*y for x,y in zip(a,b))
vals=[F(-2),F(-1,2),F(0),F(1),F(3,2)]
for sigma,ds,p,pt,a,b in product((F(1,4),F(1),F(2)),(-1,0,2),vals,vals,(-1,0,1),(-1,1)):
 dp=[F(a),F(b),p];dpt=[pt,F(a-b),F(b)];u=[F(b),pt,F(a)]
 lap=F(a+2*b);divu=p-pt
 utt=[-sigma*(u[0]+dp[0]),sigma*dp[1],sigma*dp[2]]
 ptt=lap+divu-sigma*pt
 # Derivative of the displayed eta with delta=sigma, F=diag(2,1,1).
 deriv=pt*ptt+dot(dp,dpt)+dot([2*u[0],u[1],u[2]],utt)+sigma*sigma*p*pt+dot(utt,dp)+dot(u,dpt)+sigma*(pt*pt+p*ptt)
 q=pt+sigma*p;r=[dp[i]+u[i] for i in range(3)]
 dq=[dpt[i]+sigma*dp[i]+(ds*p if i==0 else 0) for i in range(3)]
 flux=q*(lap+divu)+dot(r,dq)
 req(deriv-flux==-2*sigma*r[0]**2-ds*p*r[0],'exact_face_energy_balance')
 for delta in (F(0),sigma/2,sigma):
  ptt0=lap-sigma*pt;ut0=[-sigma*dp[0],sigma*dp[1],sigma*dp[2]]
  d0=pt*ptt0+dot(dp,dpt)+dot(ut0,dp)+sigma*delta*p*pt+delta*(pt*pt+p*ptt0)
  rhs=(delta-sigma)*pt*pt-sigma*dp[0]**2+sigma*dp[1]**2+sigma*dp[2]**2+delta*p*lap
  req(d0-(pt*lap+dot(dp,dpt))==rhs,'zero_auxiliary_initial_derivative')
 # Pointwise source inequalities at the conventional face parameters.
 for A,B,weight in ((sigma,sigma,F(2)),(F(0),-sigma,F(1)),(F(0),-sigma,F(1))):
  req(4*weight*A*(sigma+B)-(sigma+A+weight*B)**2==0,'face_algebraic_conditions_saturated')

# Laurent polynomials with half-integer powers, all coefficients rational.
def clean(p):return {e:c for e,c in p.items() if c}
def add(p,q):
 r=dict(p)
 for e,c in q.items():r[e]=r.get(e,F(0))+c
 return clean(r)
def sc(p,c):return clean({e:c*v for e,v in p.items()})
def shift(p,e):return {k+e:c for k,c in p.items()}
def mult(p,q):
 r={}
 for i,a in p.items():
  for j,b in q.items():r[i+j]=r.get(i+j,F(0))+a*b
 return clean(r)
def diff(p):return clean({e-1:e*c for e,c in p.items()})
def evaluate(p,x):
 # All evaluation in this verifier is of integral-exponent polynomials.
 req(all(e.denominator==1 for e in p),'integral_power_evaluation')
 return sum(c*x**int(e) for e,c in p.items())
def integrate(p,eps):
 A=F(0);B=F(0)
 for e,c in p.items():
  req(e.denominator==1,'integral_laurent_exponent')
  if e==-1:B+=c
  else:A+=c*(1-eps**int(e+1))/(e+1)
 return A,B  # A+B log(1/eps)

controls=[]
for k in (2,4,8,10,12,16,20):
 eps=F(1,2**k)
 p={F(-1,2):1+eps,F(1,2):-1,F(-3,2):-eps}
 d=diff(p);integrand=add(mult(p,p),sc(shift(mult(d,d),2),-2))
 expected={F(-3):-F(7,2)*eps**2,F(-2):eps**2+eps,F(-1):eps**2/2+6*eps+F(1,2),F(0):-3*eps-3,F(1):F(1,2)}
 req(integrand==expected,'exact_witness_integrand')
 A,B=integrate(integrand,eps)
 req(A==F(7,2)*(eps**2-1),'witness_rational_integral')
 req(B==eps**2/2+6*eps+F(1,2),'witness_logarithmic_integral')
 # Bound log(2) by the first terms of 2*atanh(1/3), with a geometric tail.
 L=sum(F(2,(2*j+1)*3**(2*j+1)) for j in range(12))
 U=L+F(2,25*3**25)*F(9,8)
 req(L>F(2,3) and U>L,'log_two_rational_interval')
 lower=A+B*k*L;upper=A+B*k*U
 if k>=10:req(lower>0,'positive_witness_integral')
 if k==16:
  req(A+B*k*F(2,3)>F(11,6),'large_exact_positive_margin')
 controls.append(dict(k=k,epsilon=str(eps),rational_part=str(A),log_one_over_epsilon_coefficient=str(B),lower_bound=str(lower),upper_bound=str(upper)))
 # Endpoint values of x^(3/2)*p are zero, without irrational arithmetic.
 poly=shift(p,F(3,2))
 req(evaluate(poly,eps)==evaluate(poly,F(1))==0,'witness_zero_traces')

p=Path(__file__).resolve().parent
out=dict(status='PASS',exact_assertions=sum(checks.values()),checks=dict(sorted(checks.items())),witness_integral_controls=controls,
 artifact_sha256=hashlib.sha256((p/'OBSTRUCTION.md').read_bytes()).hexdigest(),
 scope='Exact energy-balance and witness-integral algebra only. No general PDE instability, nonexistence of all Lyapunov functions, or full-source resolution is certified.')
print(json.dumps(out,indent=2,sort_keys=True))
