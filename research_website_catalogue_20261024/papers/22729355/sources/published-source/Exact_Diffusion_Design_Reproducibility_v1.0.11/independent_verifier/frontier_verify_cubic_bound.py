#!/usr/bin/env python3
"""Independently check the all-r cubic-sign comparison certificate."""
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import sympy as sp
r,u,H,L,y=sp.symbols('r u H L y',positive=True)
m=r+2
# Reference numerator N0=R+C H.
q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
R=(68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700)/(sp.Integer(286118780220)*(8*m-17)*q)
Pc=652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400
C=-sp.Integer(215)*Pc/(sp.Integer(11645046)*(8*m-17)*q)
assert all(c>0 for c in sp.Poly(sp.expand(Pc.subs(r,u+1)),u).all_coeffs())
Hup=r/(90*r+1)
expr=sp.factor(R+C*Hup-sp.Rational(1,100)); num,den=sp.fraction(expr)
assert all(c>0 for c in sp.Poly(sp.expand(num.subs(r,u+1)),u).all_coeffs())
assert all(c>0 for c in sp.Poly(q,r).all_coeffs())
# S=-4(1760850H-10253)/462105 is in (-1/10,0) for H in [1/91,1/90).
assert sp.Rational(1760850,91)-10253>0
assert sp.Rational(4,462105)*(sp.Rational(1760850,90)-10253)<sp.Rational(1,10)
# Tau formula and monotonicity.
A=1494249120*H*L*r**2-69786990*H*L*r+108738630*L*r**2+1214388*L*r-8521*L-125249670*r**2+1031940*r
B=32760*H*L*r+32760*L*r**2+4*L-4095*r
tau=sp.factor(-A/(15876*(8*r-1)*B))
dH=sp.factor(sp.diff(tau,H))
dL=sp.factor(sp.diff(tau,L))
assert dH == -4225*L*r**2*(182448*L*r+1008*L-7513)/(2*B**2)
assert dL == -65*r*(-61531470*H*r+125249670*r**2+1031940*r-7513)/(252*B**2)
# The displayed derivative numerators are positive on L>=1/sqrt(3r), H<=1/90.
assert 91224-7513>0  # sqrt(3)<2 gives 182448 Lr > 91224 at r=1.
assert 125249670+1031940-sp.Rational(61531470,90)-7513>0
# Endpoint tau(1/91,1/sqrt(3r)) < 1/20.
# After y=sqrt(3r), denominator factor is negative since y<2r.
Dinner=-32760*r**2+4095*r*y-360*r-4
assert sp.expand(Dinner.subs(y,2*r))<0
P=-1040195520*r**3+756272790*r**2*y-507201030*r**2-21412755*r*y-935658*r+58481
# r=1: y=sqrt3<7/4.
assert sp.expand(P.subs({r:1,y:sp.Rational(7,4)}))<0
# r>=2: y<=5r/4, and dropping the negative y-term gives a strict negative upper bound.
Pupper=sp.expand((-1040195520+sp.Rational(5,4)*756272790)*r**3-507201030*r**2-935658*r+58481)
assert all(c<0 for c in sp.Poly(Pupper,r).all_coeffs()[:-1]) and Pupper.subs(r,2)<0
# Critical denominator is strictly negative.
dencrit=-sp.Rational(485873,924210)-sp.Rational(11180,1467)*L*r
assert dencrit.subs({L:sp.Rational(1,1000),r:1})<0
print('VERIFY_CUBIC_BOUND_PASS')
