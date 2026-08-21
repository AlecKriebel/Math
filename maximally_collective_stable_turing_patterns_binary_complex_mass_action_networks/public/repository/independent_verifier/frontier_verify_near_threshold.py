#!/usr/bin/env python3
from __future__ import annotations
import sympy as sp
from pareto_core import A

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )


def verify_affine_ansatz(m: int) -> None:
    """Reconstruct every printed affine-vector diffusion identity exactly."""
    u0, v0, p0, q0 = sp.symbols("u v p q", nonzero=True)
    r_aff = sp.Matrix(
        [1]
        + [
            -(u0 + v0 * sp.Rational(m - 1 - i, m - 2))
            for i in range(2, m)
        ]
        + [-p0, q0]
    )
    d = [
        -2 + u0 + p0 + 2 * q0,
        sp.factor(
            (
                1
                + 2 * p0
                - u0
                - v0 * sp.Rational(m - 3, m - 2)
            )
            / (u0 + v0 * sp.Rational(m - 3, m - 2))
        ),
    ]
    d += [
        sp.factor(v0 / ((m - 2) * u0 + v0 * (m - 1 - i)))
        for i in range(3, m)
    ]
    d += [
        sp.factor((2 * u0 - 5 * p0 - 2 * q0 - 1) / p0),
        sp.factor((2 - 2 * p0 - 4 * q0) / q0),
    ]
    residual = (A(m) - sp.diag(*d)) * r_aff
    assert all(sp.factor(entry) == 0 for entry in residual)


for dimension in (3, 4, 5, 6, 8, 10):
    verify_affine_ansatz(dimension)

e,t,M,theta,nu,k=sp.symbols('epsilon t M theta nu k',positive=True)
p=e;u=1+(2-t)*e+theta*e**2;v=t*e-theta*e**2
q=sp.Rational(1,2)-(sp.Rational(1,2)+t)*e+(theta-M/sp.Integer(2))*e**2
d1=sp.factor(-2+u+p+2*q);dm=sp.factor((2*u-5*p-2*q-1)/p);dz=sp.factor((2-2*p-4*q)/q)
di=sp.factor(v/(nu*u+v*k))
assert sp.expand(d1-(e*(2-3*t)+(3*theta-M)*e**2))==0
assert sp.expand(dm-M*e)==0
sum2=sp.factor(sp.summation(sp.series(di,e,0,3).removeO(),(k,0,nu-1)))
delta=sp.factor(sp.series(dz-8*sum2,e,0,3).removeO())
assert sp.factor(delta-4*e**2*(M*nu+3*nu*t**2+6*nu*t-t**2)/nu)==0
# Exact m=3 prescribed path control.
N=(18718533*e**12+746773020*e**11+6223086873*e**10+19157763816*e**9+12668661720*e**8-49876101168*e**7-103878539968*e**6-37609207926*e**5+68189826636*e**4+62316267192*e**3+9680484312*e**2-3464522928*e-238085568)
D1=81*e**4+531*e**3+708*e**2-1102*e-1182
D2=243*e**6+2133*e**5+7431*e**4+5047*e**3-10329*e**2-17415*e-3402
cubic=-N/(13608*D1*D2)
assert sp.limit(cubic,e,0,dir='+')==sp.Rational(6,1379)
E=sp.Rational(1,1000)
Nupper=(18718533*E**12+746773020*E**11+6223086873*E**10+19157763816*E**9+12668661720*E**8+68189826636*E**4+62316267192*E**3+9680484312*E**2-238085568)
D1upper=81*E**4+531*E**3+708*E**2-1182
D2upper=243*E**6+2133*E**5+7431*E**4+5047*E**3-3402
assert Nupper<0 and D1upper<0 and D2upper<0
print('VERIFY_NEAR_THRESHOLD_PASS')
