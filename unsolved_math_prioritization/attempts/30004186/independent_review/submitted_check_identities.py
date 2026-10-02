#!/usr/bin/env python3
"""Small exact identity checks. These do not establish the nonlinear PDE theorem."""
from pathlib import Path
import json
import sympy as s
x=s.symbols('x',real=True);L=2*s.pi;k=s.pi/3;c=k*k
phi=(x-s.pi)**2/6-s.pi**2/18
P=((x-s.pi)**3-s.pi**2*(x-s.pi))/18
checks={}
def check(name,b):
    assert b,name
    checks[name]='PASS'
check('mean_zero_profile',s.integrate(phi,(x,0,L))==0)
check('endpoint_values',s.simplify(phi.subs(x,0)-c)==0 and s.simplify(phi.subs(x,L)-c)==0)
check('right_slope',s.diff(phi,x).subs(x,0)==-k)
check('left_slope',s.diff(phi,x).subs(x,L)==k)
check('primitive_derivative',s.simplify(s.diff(P,x)-phi)==0)
check('primitive_mean_zero',s.integrate(P,(x,0,L))==0)
check('traveling_identity',s.simplify((phi-c)*s.diff(phi,x)-P)==0)
check('primitive_crest_values',P.subs(x,0)==0 and P.subs(x,L)==0)
K=s.Rational(1,2)-x/L
check('primitive_kernel_mean',s.integrate(K,(x,0,L))==0)
check('primitive_kernel_L1',s.integrate(K,(x,0,s.pi))-s.integrate(K,(x,s.pi,L))==s.pi/2)
J,Z,V,y,F=s.symbols('J Z V y F',nonzero=True)
check('slope_ODE',s.simplify((V*J*J-Z*Z)/(J*J)-(V-(Z/J)**2))==0)
check('shifted_Riccati',s.expand((c+F)-(-k+y)**2-(F+2*k*y-y*y))==0)
A=k+s.pi/2
check('amplitude_rate',s.simplify(A-s.Rational(5,2)*k)==0)
check('forcing_constant',s.simplify(1+k/(A-k)-s.Rational(5,3))==0)
check('forcing_growth_gap',s.simplify(A-2*k-k/2)==0)
check('error_power',s.Rational(3)-s.Rational(1,4)==s.Rational(11,4))
check('relative_error_power_positive',s.Rational(11,4)-1==s.Rational(7,4))
# A compactly supported C1 proxy tests the scale calculation, not the smooth cutoff choice.
d,eta=s.symbols('delta eta',positive=True)
bump=-d*x*(1-x/eta)**2
check('proxy_right_slope',s.diff(bump,x).subs(x,0)==-d)
check('proxy_join',bump.subs(x,eta)==0 and s.diff(bump,x).subs(x,eta)==0)
check('proxy_mass',s.integrate(bump,(x,0,eta))==-d*eta**2/12)
r={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact identities and scaling checks only. Local well-posedness, continuation, and nonlinear departure are justified in the written candidate and require independent review.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
