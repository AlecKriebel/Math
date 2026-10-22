#!/usr/bin/env python3
"""Exact symbolic/rational checks; no simulation and no claim to verify analysis."""
from fractions import Fraction as F
import json
import sympy as S

t, p, l, s, g, h, j = S.symbols('theta p lambda s g h j', real=True)
checks = []
def zero(name, expr):
    reduced = S.factor(expr)
    assert reduced == 0, (name, reduced)
    checks.append({'check': name, 'result': 'PASS'})
def truth(name, condition):
    assert condition, name
    checks.append({'check': name, 'result': 'PASS'})

# Laplace transform closes on the atom-exponential family.
L = p + (1-p)*l/(l+s)
pdot = (1-p)*(l-p)
ldot = -l*(1-p)
zero('atom-exponential Laplace generator',
     S.diff(L,p)*pdot + S.diff(L,l)*ldot - (L*L+(s-1)*L-s*p))
zero('phase invariant derivative',
     S.diff(p/l+S.log(l),p)*pdot + S.diff(p/l+S.log(l),l)*ldot)
a = S.symbols('a')
zero('critical q second-order coefficient',
     S.diff(1-(1+a)+(1+a)*S.log(1+a),a,2).subs(a,0)-1)
zero('critical q zero constant', (1-(1+a)+(1+a)*S.log(1+a)).subs(a,0))
zero('critical q zero linear coefficient',
     S.diff(1-(1+a)+(1+a)*S.log(1+a),a).subs(a,0))

# Exact moment-generator identities.
gd = g*g-(1+t)*g+t*p
hd = (2*g-1-t)*h-g+p
jd = (2*g-1-t)*j+2*h*h-2*h
b = 2*(1-t)
phi = g-t*h-b*j
zero('polynomial-exponential differential identity',
     gd-t*hd-b*jd-((2*g-1-t)*phi+2*b*(h-h*h)-g*g+t*g))
zero('theta-one sign-boundary derivative',
     (gd-hd).subs(t,1) - (2*(g-1)*(g-h)-g*(g-1)))
truth('Exp(2) sign-boundary derivative exactly -2',
      (gd-hd).subs({t:1,g:2,h:2,p:0}) == -2)
zero('Lyapunov scalar factorization', g*g-(1+t)*g+t-(g-1)*(g-t))
zero('second moment generator expansion',
     S.expand((S.Symbol('x')+S.Symbol('y'))**2-S.Symbol('x')**2)
     -(2*S.Symbol('x')*S.Symbol('y')+S.Symbol('y')**2))

# Exp(5/2), exact rational controls.
lambda0 = S.Rational(5,2)
M = l/(l-t)
phi_exp = M-t*S.diff(M,t)-2*(1-t)*S.diff(M,t,2)
certificate = l*((l-t)**2-t*(l-t)-4*(1-t))/(l-t)**3
zero('exponential test closed form',phi_exp-certificate)
num = ((l-t)**2-t*(l-t)-4*(1-t)).subs(l,lambda0)
zero('positive square certificate for all real theta',
     num-(2*(t-S.Rational(7,8))**2+S.Rational(23,32)))
truth('positive square residual', S.Rational(23,32)>0)
truth('denominator positive on theta in (0,1)', lambda0-1>0)
truth('initial first moment', 1/lambda0 == S.Rational(2,5))
truth('initial second moment', 2/lambda0**2 == S.Rational(8,25))
truth('second-moment necessary bound', S.Rational(8,25)<S.Rational(1,2))
truth('E exp X', M.subs({l:lambda0,t:1})==S.Rational(5,3))
truth('E X exp X', S.diff(M,t).subs({l:lambda0,t:1})==S.Rational(10,9))
truth('initial exponential moment difference',
      (M-S.diff(M,t)).subs({l:lambda0,t:1})==S.Rational(5,9))
truth('tail comparison coefficient', lambda0-1>0)

# e > sum_{k=0}^3 1/k! = 8/3; omitted terms are strictly positive.
partial = sum([F(1),F(1),F(1,2),F(1,6)],F(0))
truth('exact exponential series lower comparison',partial==F(8,3))
truth('lambda0/e < 15/16 via positive series remainder', F(5,2)/partial==F(15,16))
truth('explicit positive free-energy exponent bound',16*F(5,2)==40)

# Stationary quadratic discriminant controls.
z = S.symbols('z')
D = 1+2*(1-2*p)*z+z*z
zero('discriminant of stationary discriminant',S.discriminant(D,z)+16*p*(1-p))
zero('stationary discriminant at positive radius',D.subs(z,1)-4*(1-p))
truth('product of discriminant roots',S.Poly(D,z).all_coeffs()[-1]==1)

result = {
  'status':'PASS', 'check_count':len(checks), 'sympy_version':S.__version__,
  'checks':checks,
  'limitations':'Symbolic identities and exact rational controls only. Analytic proofs, source scope, and general extinction are not certified by this script.',
  'simulation_used':False,
}
print(json.dumps(result,indent=2))
