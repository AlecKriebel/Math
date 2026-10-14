#!/usr/bin/env python3
"""Exact finite algebra controls, not a PDE solver or proof of analytic bounds.
Requires SymPy; tested with version 1.14.0.
"""
from fractions import Fraction as F
from collections import Counter
import random,json
import sympy as S
checks=Counter()
def check(ok,kind):
    assert bool(ok),kind
    checks[kind]+=1
h,a,rho,A,C,eps,r,s=S.symbols('h a rho A C eps r s',positive=True)
p=S.pi
rad=S.sin(p*r)/(S.sqrt(2*p)*r)
check(S.simplify(S.diff(rad,r,2)+2/r*S.diff(rad,r)+p*p*rad)==0,'ball_eigenfunction')
check(S.simplify(4*p*S.integrate(rad**2*r*r,(r,0,1)))==1,'eigenfunction_normalization')
check(S.limit(rad,r,0)==p/S.sqrt(2*p),'regular_origin')
end=S.simplify(a/p*S.integrate(S.cos(p*s),(s,-h,h)))
vel=S.simplify(a*S.integrate(S.sin(p*s),(s,-h,h)))
check(end==2*a*S.sin(p*h)/p**2,'linear_endpoint')
check(vel==0,'linear_velocity_cancellation')
gap=S.simplify(a*S.integrate(1-S.cos(p*s),(s,-h,h)))
check(S.simplify(gap-(2*a*h-2*a*S.sin(p*h)/p))==0,'first_order_gap')
check(S.limit(gap.subs(a,h)/h**4,h,0)==p**2/3,'vanishing_amplitude_gap')
check(S.limit(end.subs(a,h)/h**2,h,0)==2/p,'vanishing_amplitude_endpoint')
check(S.limit((gap.subs(a,h)+end.subs(a,h)**2/2)/(2*h**3),h,0)==0,'quadratic_growth_ratio')
# Stable target perturbation comparison uses fixed a and h=pi*eps/(2a).
trial=S.simplify((gap+end**2/2-eps*end).subs(h,p*eps/(2*a)))
check(S.limit(trial/eps**2,eps,0)==-S.Rational(1,2),'target_perturbation_leading_term')
check(S.simplify((2*a*h).subs(h,p*eps/(2*a)))==p*eps,'target_pulse_mass')
check(S.simplify(2*rho*(A/(2*rho))**3/3-A**3/(12*rho**2))==0,'bathtub_exact_minimum')
check(S.simplify((A**3/(6*rho**2)-C*A**5)-A**3*(1/(6*rho**2)-C*A**2))==0,'global_gap_factorization')
check(S.simplify((eps/p)**2*S.sqrt(2*eps/p)-(2**S.Rational(1,4)*p**(-S.Rational(5,4))*eps**S.Rational(5,4))**2)==0,'positive_part_L2_bound')
check(S.Rational(5,4)+1>S.Integer(2),'stability_exponent_separation')
# Exact piecewise-constant density tests of the bathtub inequality.
rng=random.Random(30004630)
for N in range(2,31):
    for case in range(25):
        cap=F(rng.randrange(1,10),rng.randrange(1,10))
        vals=[cap*F(rng.randrange(11),10) for _ in range(N)]
        mass=sum(vals,F(0))/N
        moment=F(0)
        for j,v in enumerate(vals):
            left=F(j,N)-F(1,2);right=F(j+1,N)-F(1,2)
            moment+=v*(right**3-left**3)/3
        check(moment>=mass**3/(12*cap**2),'rational_bathtub_controls')
        check(F(0)<=mass<=cap,'admissible_mass')
        for power in (4,5,10):
            check((F(2)*F(1,N)**2)**power==F(2)**power*F(1,N)**(2*power),'pulse_remainder_exponents')
for denom in range(2,101):
    hh=F(1,denom)
    check((2*hh**2)**4/(2*hh**3)==8*hh**5,'quartic_cost_ratio')
    check((2*hh**2)**5/(2*hh**3)==16*hh**7,'quintic_cost_ratio')
    check((2*hh**2)**10/(2*hh**3)==512*hh**17,'velocity_cost_ratio')
print(json.dumps({'status':'PASS','assertions':sum(checks.values()),'categories':dict(checks),
                 'sympy_version':S.__version__,
                 'limits':'Exact eigenmode, pulse, exponent, and finite bathtub controls only. No discretized PDE, simulation, certified numerical PDE constant, or replacement for the analytic proof.'},indent=2))
