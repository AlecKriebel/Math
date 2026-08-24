#!/usr/bin/env python3
"""Finite exact regression for selected-profile normal-form signs and contrast."""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import sympy as sp
from common import Hsum,ellr_formula,ellDr_formula,N_formula
for m in [3,4,5,6,8,10,20,50]:
 H=Hsum(m);eta=sp.factor(ellDr_formula(m,H)/ellr_formula(m,H));cub=sp.factor(N_formula(m,H)/ellr_formula(m,H))
 assert eta>0 and cub<0
 contrast=sp.Rational(23,63)*(91*m-183)
 assert contrast>8*(m-2)
print('STABLE_CONTRAST_PASS')
