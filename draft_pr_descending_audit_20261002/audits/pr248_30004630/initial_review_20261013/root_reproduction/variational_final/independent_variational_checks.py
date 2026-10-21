#!/usr/bin/env python3
"""Independent controls: continuous pulses, exact threshold geometry and edge mass.
This is not a PDE solver and does not estimate a numerical PDE constant.
"""
import json, math, hashlib, sys
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import sympy as S
import mpmath as mp

checks=Counter()
def check(test,name):
    assert bool(test),name
    checks[name]+=1
h,a,eps,theta,delta,A,rho=S.symbols('h a eps theta delta A rho',positive=True)
s,x=S.symbols('s x',real=True)
p=S.pi
# Continuous triangular controls independently replace rectangular author controls.
tri=a*(1-s/h)
tri_mass=2*S.integrate(tri,(s,0,h))
tri_sq=2*S.integrate(tri**2,(s,0,h))
tri_q=S.simplify(2/p*S.integrate(tri*S.cos(p*s),(s,0,h)))
tri_vel=S.integrate(a*(1-S.Abs(s)/h)*S.sin(p*s),(s,-h,h))
check(tri_mass==a*h,'triangle_mass')
check(tri_sq==2*a*a*h/3,'triangle_squared_norm')
check(S.simplify(tri_q-2*a*(1-S.cos(p*h))/(h*p**3))==0,'triangle_exact_position')
check(S.simplify(tri_vel)==0,'triangle_exact_velocity')
tri_gap=S.simplify((tri_mass-p*tri_q+tri_q**2/2).subs(a,h))
check(S.simplify(S.limit(tri_gap/h**4,h,0)-p**2/12-1/(2*p**2))==0,'triangle_leading_gap')
check(S.limit(tri_gap/(2*h**3/3),h,0)==0,'triangle_growth_failure')
# Exact threshold integral in support angle theta=acos(1/(1+delta)).
g2theta=S.simplify(2*S.integrate((S.cos(p*s)/S.cos(theta)-1)**2,(s,0,theta/p)))
exact_formula=((1/S.cos(theta)**2+2)*theta-3*S.tan(theta))/p
check(S.trigsimp(g2theta-exact_formula)==0,'threshold_exact_norm_formula')
check(S.limit(g2theta/(1/S.cos(theta)-1)**S.Rational(5,2),theta,0)==16*S.sqrt(2)/(15*p),'threshold_asymptotic_constant')
parabola=S.integrate((delta-2*s*s)**2,(s,-S.sqrt(delta/2),S.sqrt(delta/2)))
check(S.simplify(parabola-16*delta**S.Rational(5,2)/(15*S.sqrt(2)))==0,'threshold_parabola_exact_integral')
# Independent exact sharp sine bathtub comparator and both mass endpoints.
b=A/(2*rho)
sharp=S.simplify(2*rho*S.integrate(1-S.cos(p*s),(s,0,b)))
check(S.simplify(sharp-(A-2*rho*S.sin(p*A/(2*rho))/p))==0,'sharp_sine_bathtub')
check(S.limit(sharp,A,0)==0,'zero_mass_boundary')
check(S.simplify(sharp.subs(A,rho)-rho*(1-2/p))==0,'full_mass_boundary')
check(S.limit(sharp/A**3,A,0)==p**2/(24*rho**2),'small_mass_sharp_constant')
# Nonrectangular exact rational densities; comparison proven analytically, finite cases
# probe zero/full mass, asymmetry, boundary concentration and alternating controls.
for n in (2,3,4,5,7,11,17,31,47):
    cap=F(3,7)
    patterns=[[F(0)]*n,[cap]*n,[cap if j==0 else F(0) for j in range(n)],
              [cap if j==n-1 else F(0) for j in range(n)],
              [cap if j%2 else F(0) for j in range(n)],
              [cap*F(j,n-1) for j in range(n)],
              [cap*F(min(j,n-1-j),max(1,(n-1)//2)) for j in range(n)]]
    for vals in patterns:
        mass=sum(vals,F(0))/n
        moment=sum((v*((F(j+1,n)-F(1,2))**3-(F(j,n)-F(1,2))**3)/3 for j,v in enumerate(vals)),F(0))
        sq=sum((v*v for v in vals),F(0))/n
        check(moment>=mass**3/(12*cap**2),'boundary_and_asymmetric_bathtub')
        check(sq<=cap*mass,'mass_to_L2_bound')
        check(mass*mass<=sq,'L1_to_L2_bound')
# Quantifier exponent gap and strengthened optimizer rate from A=O(sqrt eps).
check(S.Rational(5,4)+1>2,'fixed_Lipschitz_ratio_contradiction')
check(S.Rational(1,2)*5>2,'optimizer_nonlinear_error_negligible')
check(2-S.Rational(5,4)==S.Rational(3,4),'uniform_optimizer_lower_rate')
# Independent L1 growth strengthening: scalar monotonicity and exact absorption.
D,Q=S.symbols('D Q',positive=True)
b=A/p+D*A**5
scalar=A-p*x+x*x/2
at_bound=S.expand(scalar.subs(x,b))
check(S.simplify(at_bound-(A*A/(2*p*p)-p*D*A**5+D*A**6/p+D*D*A**10/2))==0,'L1_growth_exact_scalar_expansion')
check(S.simplify(S.diff(scalar,x).subs(x,p/2-Q))==-p/2-Q,'L1_growth_scalar_monotonicity')
check(S.simplify((A*A/(2*p*p)-p*D*A**5)-A*A*(1/(2*p*p)-p*D*A**3))==0,'L1_growth_absorption_factorization')
check(S.simplify(1/(2*p*p)-p*(1/(4*p**3))-1/(4*p*p))==0,'L1_growth_threshold_constant')
check(S.simplify((4*p*p*Q*eps)**2/(4*p*p)-eps*Q*(4*p*p*Q*eps))==0,'basepoint_L1_target_upper_bound_constant')
# High precision diagnostic (not certified numerical inequalities).
mp.mp.dps=80
samples=[]
for k in (2,3,4,6,8):
    hh=mp.mpf(10)**(-k)
    qq=2*(1-mp.cos(mp.pi*hh))/mp.pi**3
    gg=hh**2-mp.pi*qq+qq**2/2
    th=mp.mpf(10)**(-k)
    dd=1/mp.cos(th)-1
    norm2=((1/mp.cos(th)**2+2)*th-3*mp.tan(th))/mp.pi
    ratio=norm2/dd**mp.mpf('2.5')
    check(abs(ratio-16*mp.sqrt(2)/(15*mp.pi))<mp.mpf('0.001'),'threshold_high_precision_sanity')
    samples.append({'h':str(hh),'triangle_gap_over_h4':mp.nstr(gg/hh**4,30),'threshold_norm2_over_delta2_5':mp.nstr(ratio,30)})
receipt={'status':'PASS','assertions':sum(checks.values()),'categories':dict(checks),'sympy':S.__version__,'mpmath':mp.__version__,'python':sys.version.split()[0],'diagnostic_samples':samples,'limits':'Exact symbolic/rational finite controls plus noncertified high precision diagnostic; no PDE discretization, PDE numerical constant, novelty or full beta2=0 theory certification.'}
print(json.dumps(receipt,indent=2))
