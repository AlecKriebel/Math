#!/usr/bin/env python3
"""Exact algebra checks for WIP notes; no geometric instability is certified."""
import json
import sympy as S

mu, lam, n = S.symbols('mu lam n', nonzero=True)
tests = {}
def check(name, expression):
    value = S.factor(S.together(expression))
    assert value == 0, (name, value)
    tests[name] = 'PASS'

q_ein = n*lam-(n-2)*mu/2-mu**2/(2*(mu-lam))
check('Einstein conformal factorization', q_ein-(2*lam-mu)*((n-1)*mu-n*lam)/(2*(mu-lam)))
k = mu*(mu-2)/(2*(mu-1))
check('Polarized gradient divergence correction', mu-mu**2/(2*(mu-1))-k)
check('Pure Hessian gauge cancellation', (1-mu/2)*mu*(mu-1)+k*(1-mu)**2)
check('Ricci multiplier scalar coefficient', k/4-mu*(mu-2)/(8*(mu-1)))
check('Resolvent decomposition', mu**2/(mu-lam)-(mu+lam+lam**2/(mu-lam)))

m2, m3, m4, z = S.symbols('m2 m3 m4 z')
r = lam*(n-2*m2)
check('Constant conformal scaling cancellation', n*lam-2*lam*m2-r)
potential = 2*m3-S.Rational(1,8)*(S.Rational(11,3)*m4-m2**2+z)-(2*m2-m3)**2/(n-2*m2)
potential_alternate = 2*m3-S.Rational(1,3)*m4-S.Rational(1,8)*(m4-m2**2+z)-(2*m2-m3)**2/(n-2*m2)
check('Potential resolvent rearrangement', potential-potential_alternate)

M1, M2, D2 = S.symbols('M1 M2 D2')
exp1=n*M2-(n-2)*D2/2-n**2*M1**2/(n-2*m2)
exp2=n*(M2-M1**2)-(n-2)*D2/2-2*n*m2*M1**2/(n-2*m2)
check('Exponential variance rearrangement',exp1-exp2)

p,q,c = S.symbols('p q c')
check('Coupled Ricci penalty rank one', 4*c**2*p**2+4*c**2*p*q+c**2*q**2-c**2*(2*p+q)**2)

print(json.dumps({'tests':tests,'count':len(tests),
 'scope':'algebraic identities only; no compact soliton is constructed and no universal Hessian sign is certified'}, indent=2))
