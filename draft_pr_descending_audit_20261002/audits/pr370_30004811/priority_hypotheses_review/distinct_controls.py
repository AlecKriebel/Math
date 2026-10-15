#!/usr/bin/env python3
"""Distinct audit controls: exact radial volume tail and boundary flux.

The smooth core is represented by its fixed volume C. These symbolic identities
supplement MATH_RECONSTRUCTION.md; they neither determine the global m_CV nor
certify any credited geometric-analysis theorem.
"""
import sympy as s
import json
R,r,z=s.symbols('R r z',positive=True)
C=s.symbols('C',real=True)
m=s.symbols('m',real=True)
d=R/2
u=1-1/r
N=0

def check(v):
 global N
 assert bool(v)
 N+=1

# Derive volume directly from the radial solid angle of the displaced sphere.
# For r<R-d all directions are inside; for R-d<r<R+d the area fraction
# follows from |r*omega-d*e1|^2<=R^2.
angular_shell= s.pi*r*(R**2-(r-d)**2)/d
check(s.simplify(angular_shell.subs(r,R-d)-4*s.pi*(R-d)**2)==0)
check(s.simplify(angular_shell.subs(r,R+d))==0)

# Full rational tail u^6 is integrated without dropping conformal terms.
F1=s.integrate(s.expand(4*s.pi*r**2*u**6),r)
F2=s.integrate(s.expand(angular_shell*u**6),r)
V=s.simplify(C + F1.subs(r,R/2)-F1.subs(r,3)
            + F2.subs(r,3*R/2)-F2.subs(r,R/2))
check(s.simplify(s.limit(V/R**3,R,s.oo)-4*s.pi/3)==0)
check(s.simplify(s.limit((V-4*s.pi*R**3/3)/R**2,R,s.oo)+11*s.pi)==0)
next_coefficient=s.simplify(s.limit((V-4*s.pi*R**3/3+11*s.pi*R**2)/R,R,s.oo))
check(s.simplify(next_coefficient-(30*s.pi+s.Rational(45,2)*s.pi*s.log(3)))==0)
# Different core volumes change volume-radius only at inverse-square order.
check(s.diff(V,C)==1)
check(s.simplify(s.limit(R**2*s.diff((3*V/(4*s.pi))**s.Rational(1,3),C),R,s.oo)-1/(4*s.pi))==0)
check(s.simplify(s.limit((3*V/(4*s.pi))**s.Rational(1,3)-(R-1),R,s.oo)+s.Rational(7,4))==0)

# Compute metric flux on the displaced boundary itself, independently of
# the far-field quotient expansion. Since f=0 there, u^2*d_n(f/u)=u/R.
# dA=R^2*domega, giving capacity R times the boundary average of u.
U_boundary=1+m/(2*s.sqrt(R**2+d**2+2*R*d*z))
cap_boundary=s.simplify(R*s.integrate(U_boundary,(z,-1,1))/2)
check(s.simplify(cap_boundary-R-m/2)==0)
check(s.simplify(cap_boundary.subs(m,-2)-(R-1))==0)

# Positive/zero/negative mass controls and the forbidden boundary hypothesis.
lam=s.symbols('lam',real=True)
deficit=m*(1-lam**2/2)
check(deficit.subs({m:0,lam:s.Rational(1,2)})==0)
check(deficit.subs({m:2,lam:s.Rational(1,2)})<2)
check(deficit.subs({m:-2,lam:s.Rational(1,2)})>-2)
U=1+m/(2*r)
H=s.simplify(U**-2*(2/r+4*s.diff(U,r)/U))
check(s.simplify(H-(2*r-m)/(r*r*U**3))==0)
t=s.symbols('t',positive=True)
check(s.simplify(H.subs({m:-2,r:1+t})).is_positive)

print(json.dumps({'status':'PASS','assertions':N,'control_family':'exact radial integration of all conformal volume terms; local metric boundary flux; missing-global-hypothesis controls','volume_linear_remainder_coefficient':str(next_coefficient),'capacity_boundary_flux':str(cap_boundary),'deficit_limit':'-7/4','core_dependence_of_volume':'additive constant C; radius dependence O(R^-2)','scope':'Independent audit controls; not an evaluation of global capacity-volume mass.'},indent=2,sort_keys=True))
