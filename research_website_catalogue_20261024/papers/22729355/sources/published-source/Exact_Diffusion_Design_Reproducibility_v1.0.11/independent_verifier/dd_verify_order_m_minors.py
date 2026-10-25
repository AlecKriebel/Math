#!/usr/bin/env python3
"""Duplicate finite exact regression for the closed-form omission minors."""

if not __debug__:
 raise SystemExit('Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O')

import sympy as sp
from common import signed_omissions
for m in [3,4,5,6,8,10]:
 a=sp.Rational(3,2);b=sp.Rational(5,3);got=signed_omissions(m,a,b)
 want=[0]+[16*a**(m-1)*b]*(m-2)+[0,-2*a**(m-1)*b]
 assert got==want,(m,got,want)
print('ORDER_M_MINORS_PASS')
