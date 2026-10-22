#!/usr/bin/env python3
"""Exact symbolic identities only; does not certify geometric-analysis inputs."""
import json
import sympy as s

r, c, K, x, A0, t = s.symbols('r c K x A0 t', positive=True)
checks = []
def check(label, expression):
    result = s.simplify(expression)
    assert result == 0, (label, result)
    checks.append(label)

f = 4*s.pi*r**2 - 4*s.pi*c*r**3/3
check('ball energy derivative', s.diff(f,r) - 4*s.pi*r*(2-c*r))
check('critical radius value', f.subs(r,2/c)-16*s.pi/(3*c**2))
check('negative endpoint at radius 4/c', f.subs(r,4/c)+64*s.pi/(3*c**2))
# x = V^(1/3), avoiding branch assumptions on fractional powers.
F = K*x**2-c*x**3
xs = 2*K/(3*c)
check('volume-root critical point', s.diff(F,x).subs(x,xs))
check('volume profile maximum', F.subs(x,xs)-4*K**3/(27*c**2))
check('profile to width constant', (4*K**3/(27*c**2)).subs(K**3,36*s.pi)-16*s.pi/(3*c**2))
check('volume threshold normalization', (8*K**3/(27*c**3)).subs(K**3,36*s.pi)-32*s.pi/(3*c**3))
check('zero-energy volume-root threshold', F.subs(x,K/c))
# Equality-case cone coordinates: area = A0 exp(t), r=sqrt(area/(4pi)).
r_t=s.sqrt(A0*s.exp(t)/(4*s.pi))
H=2/r_t
check('equality-case radial metric', H**(-2) / s.diff(r_t,t)**2-1)
check('area differential factor', s.diff((A0*s.exp(t))**s.Rational(3,2),t)-s.Rational(3,2)*(A0*s.exp(t))**s.Rational(3,2))
# Generic two-dimensional-fiber warped-product scalar formula.
Rg=s.symbols('R_gamma')
warp=r
Rcone=Rg/warp**2-4*s.diff(warp,r,2)/warp-2*s.diff(warp,r)**2/warp**2
check('cone scalar formula', Rcone-(Rg-2)/r**2)
# Symbolic nonnegativity of f(max)-f(V) on x>=0: exact factorization.
check('global profile maximum factorization', F.subs(x,xs)-F-c*(x-xs)**2*(x+K/(3*c)))
print(json.dumps({'status':'PASS','checks':len(checks),'labels':checks,
 'scope':'Exact algebra identities only; geometric theorems and analytic arguments are not computationally verified.',
 'sympy_version':s.__version__},indent=2))
