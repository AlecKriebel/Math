#!/usr/bin/env python3
"""Finite contraction regression plus closed-form sign certificates.

The all-dimensional recurrence-to-cubic bridge is checked separately by
``verify_generic_cubic_recurrence.py``.
"""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import sympy as sp
from common import Avec,selected,B,w0,w2,Hsum,ellr_formula,N_formula,Q3
m,u=sp.symbols('m u',integer=True,positive=True)
def shifted(poly):
 P=sp.Poly(sp.expand(poly.subs(m,u+3)),u);return [P.coeff_monomial(u**k) for k in range(P.degree(),-1,-1)]
polys=[
 Q3(m),
 633906000*m**2-2491895430*m+2448652733,
 2729945147827667886720*m**5-27755132420474170999952*m**4+112813395868533457497683*m**3-229153280695458887386228*m**2+232620996871721820873517*m-94412163900120968220300]
for p in polys: assert all(c>0 for c in shifted(p))
for k in [3,4,5,6,8,10]:
 A=Avec(k);r,d,ell=selected(k);N=(ell.T*(B(k,r,w0(k))+sp.Rational(1,2)*B(k,r,w2(k))))[0]
 H=Hsum(k)
 assert sp.factor(N-N_formula(k,H))==0
 c=sp.factor(N/ellr_formula(k,H));assert c<0
print('CUBIC_SIGN_PASS')
