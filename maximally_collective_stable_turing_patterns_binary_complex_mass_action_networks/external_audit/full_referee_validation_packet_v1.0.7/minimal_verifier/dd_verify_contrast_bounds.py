#!/usr/bin/env python3
if not __debug__:
 raise SystemExit('Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O')

import sympy as sp
for m in range(3,21):
 d=[sp.Rational(23,63)]+[sp.Rational(1,91*m-181-i) for i in range(2,m)]+[sp.Rational(1,7),sp.Rational(16,45)]
 assert min(d)==sp.Rational(1,91*m-183)
 assert max(d)==sp.Rational(23,63)
 assert sp.factor(max(d)/min(d)-sp.Rational(23,63)*(91*m-183))==0
 assert sp.Rational(23,63)*(91*m-183)>8*(m-2)
print('CONTRAST_BOUNDS_PASS')
