#!/usr/bin/env python3
"""Exact identities and tail controls for the conditional SIRSN argument.
These are not SIRSN simulations or evidence for the missing first-moment case.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math
import sympy as s
checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]='PASS'
n,r,lam,delta,eta,t=s.symbols('n r lam delta eta t', positive=True)
ck('strip_area',s.expand((n+2)**2-n**2)==4*n+4)
ck('dyadic_annular_area',s.expand((n+4*r)**2-(n+2*r)**2)==4*n*r+12*r*r)
ck('annular_intensity_cancellation',s.expand((4*n*r+12*r*r)/r)==4*n+12*r)
ck('far_tail_fourth_order_scaling',s.simplify(lam**2*n**5/s.sqrt(2)*eta/(s.sqrt(2)*delta*n)**3/n**2)==lam**2*eta/(4*delta**3))
for j in range(25):
    sm=sum(2**i for i in range(j+1))
    ck(f'dyadic_sum_{j}',sm==2**(j+1)-1)
    for a in [Fraction(1),Fraction(3,2),Fraction(7,4)]:
        R=2**j*a
        ck(f'cover_{j}_{a}',2**j<=R<2**(j+1) and sm<=2*R)
# Coefficientwise factorial-moment shift establishing the tail identity.
for m in range(2,82):
    ck(f'poisson_second_factorial_shift_{m}',Fraction(m*(m-1),math.factorial(m))==Fraction(1,math.factorial(m-2)))
for alpha in [s.Rational(2),s.Rational(3),s.Rational(4),s.Rational(5),s.Rational(7,2),s.Rational(9,2),s.Rational(8)]:
    h=alpha/(alpha-1)*t**(1-alpha)
    ck(f'pareto_layercake_{alpha}',s.simplify(t*t**(-alpha)+s.integrate(s.Symbol('u',positive=True)**(-alpha),(s.Symbol('u',positive=True),t,s.oo))-h)==0)
    ck(f'pareto_finite_mean_{alpha}',alpha/(alpha-1)>0)
    limit=s.limit(t**3*h,t,s.oo)
    ck(f'pareto_fourth_tail_control_{alpha}',(limit==0)==(alpha>4))
ck('finite_first_moment_does_not_imply_tail_condition',s.limit(t**4*t**(-2),t,s.oo)==s.oo)
ck('pareto_two_truncated_first_moment',s.simplify(s.Rational(2)*t**(-1)-2/t)==0)
# A Poisson exponential-Markov bound is genuinely exponentially decreasing
# at the upper tail of a lower-density count.
for eps in [s.Rational(1,10),s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
    theta=-s.log(1-eps)
    rate=s.simplify((1-eps)*(s.exp(theta)-1)-theta)
    ck(f'chernoff_rate_negative_{eps}',rate<0)
result={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'checks':checks,'scope':'Exact algebraic and distributional controls only; no generated SIRSN, no Monte Carlo theorem, no verification of the unconditional target.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'failed':0,'sympy_version':s.__version__,'proof_sha256':result['proof_sha256']}))
