import sympy as S
from datetime import datetime,timezone
B=S.symbols('beta')
b2=B**2-6*B+1;b4=B**2-B;b6=B**2;b8=-B**3
print('UTC_START',datetime.now(timezone.utc).isoformat())
discriminant=-b2**2*b8-8*b4**3-27*b6**2+9*b2*b4*b6
assert S.expand(discriminant-B**5*(B**2-11*B-1))==0
print('EXACT ZERO: generalized Weierstrass discriminant equals beta^5(beta^2-11beta-1)')
print('UTC_END',datetime.now(timezone.utc).isoformat())
