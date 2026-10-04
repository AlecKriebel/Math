#!/usr/bin/env python3
"""Exact constants plus noncertifying numerical diagnostics for Hayman's example.

Python 3 standard library. The analytic proof, not the sampled checks, establishes
subharmonicity and the two continuum quantifiers. No network calls or source PDFs.
"""
from fractions import Fraction as F
import json
import math
from pathlib import Path

a, c, eps = F(1,100), F(90), F(1,1_000_000)
eta = c*eps
checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name

check('eta_equals_9_over_100000',eta==F(9,100000))
check('epsilon_positive',eps>0)
check('epsilon_less_one',eps<1)
check('eta_positive',eta>0)
check('eta_less_half',eta<F(1,2))
check('gap_radii_above_nine_tenths',1-eps>F(9,10))
check('sine_lower_ratio_at_least_nine_tenths',1-eta**2/6>=F(9,10))
check('nine_tenths_squared_less_nine_tenths',F(9,10)**2<F(9,10))
check('horizontal_coordinate_lower_bound',F(9,10)**2>F(4,5))
check('green_numerator_lower_bound',2*F(9,10)**2>1)
check('e_power_four_upper_bound',3**4<c)
check('gap_deficit_below_log_lower_bound',eta+F(5,2)/c<4*a)
check('axis_green_coefficient_smaller',a*c/(1-eta**2)<1/(1+eps**2))
check('cross_multiplied_axis_inequality',a*c*(1+eps**2)<1-eta**2)
check('all_cross_multipliers_positive',(1-eta**2)*(1+eps**2)>0)
# Symbolic polynomial identity in r and s=sin(eta), encoded sparsely.
# No sampled values are being used to certify this identity.
def add(*polys):
    result={}
    for poly in polys:
        for power, coeff in poly.items():
            result[power]=result.get(power,F(0))+coeff
    return {p:v for p,v in result.items() if v}
def mul(p,q):
    result={}
    for (r1,s1),v1 in p.items():
        for (r2,s2),v2 in q.items():
            power=(r1+r2,s1+s2)
            result[power]=result.get(power,F(0))+v1*v2
    return {p:v for p,v in result.items() if v}
R={(1,0):F(1)}
ONE={(0,0):F(1)}
MINUS_ONE={(0,0):F(-1)}
S2={(0,2):F(1)}
plus_square=mul(add(R,ONE),add(R,ONE))
minus_square=mul(add(R,MINUS_ONE),add(R,MINUS_ONE))
lhs=add(mul(plus_square,S2),mul(minus_square,add(ONE,{(0,2):F(-1)})))
rhs=add(minus_square,{(1,2):F(4)})
check('green_identity_as_symbolic_polynomial',lhs==rhs)

A,C,E,T=map(float,[a,c,eps,eta])
zeta=complex(math.sin(T),math.cos(T))
def h(z):
    x,y=z.real,z.imag
    return (math.atan2(y,x)+math.pi/2
            -math.atan2(y-1+E,x)-math.atan2(1+E-y,x))/math.pi

def green(z):
    return math.log(abs(z+zeta.conjugate())/abs(z-zeta))

def v(z):
    return h(z)+(A/math.pi)*green(z)

axis_samples=[]
for x in [0.001,0.01,0.1,0.5,1,2,10,100,1000]:
    q=2*x/(1+x*x)
    stable=0.5+(A*math.atanh(q*math.sin(T))
                -math.atan(2*E*x/(x*x+1-E*E)))/math.pi
    direct=v(complex(x,0))
    assert 0<stable<0.5
    assert abs(stable-direct)<2e-15
    axis_samples.append({'x':x,'V':stable,'half_minus_V':0.5-stable,
                         'direct_formula_error':abs(stable-direct)})
gap_samples=[]
for j in [-1,-0.5,-0.25,0.25,0.5,1]:
    r=1+j*E
    value=v(r*zeta)
    assert value>1
    gap_samples.append({'radius_minus_one_over_epsilon':j,'V':value})
# Singular radius r=1 is handled analytically, not evaluated numerically.
output={
    'exact_assertions':checks,
    'exact_assertions_passed':len(checks),
    'gap_surplus_lower_bound_over_pi':str(4*a-eta-F(5,2)/c),
    'axis_coefficient_margin':str(1/(1+eps**2)-a*c/(1-eta**2)),
    'axis_samples_noncertifying':axis_samples,
    'gap_samples_noncertifying':gap_samples,
    'limitations':['No finite grid proves a universal quantifier.',
                  'Floating-point diagnostics are not interval arithmetic.',
                  'Subharmonicity and boundary limits require PROOF.md.',
                  'No optimal Hall constant is determined.']}
print(json.dumps(output,indent=2,sort_keys=True))
