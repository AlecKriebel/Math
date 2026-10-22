#!/usr/bin/env python3
"""Exact finite controls for the explicit table; not a replacement for Lazutkin."""
import json
import sympy as s

a = s.symbols('theta', real=True)
x, y = s.symbols('x y', real=True)
h = 1 + s.cos(3*a)/16
n = s.Matrix([s.cos(a), s.sin(a)])
t = s.Matrix([-s.sin(a), s.cos(a)])
X = h*n + s.diff(h, a)*t
r = s.simplify(h+s.diff(h,a,2))
checks = []
def check(name, expr):
    assert expr, name
    checks.append(name)
check('radius formula', s.simplify(r-(1-s.cos(3*a)/2)) == 0)
check('velocity x', s.simplify(s.diff(X[0],a)-r*t[0]) == 0)
check('velocity y', s.simplify(s.diff(X[1],a)-r*t[1]) == 0)
check('support projection', s.trigsimp(s.expand(X.dot(n)-h)) == 0)
check('tangent norm', s.trigsimp(t.dot(t)-1) == 0)
check('normal orthogonal tangent', s.trigsimp(n.dot(t)) == 0)
check('radius lower endpoint', r.subs(a,0) == s.Rational(1,2))
check('radius upper endpoint', s.simplify(r.subs(a,s.pi/3)) == s.Rational(3,2))
check('support positive global lower bound', 1-s.Rational(1,16)>0)
check('third harmonic difference', s.trigsimp(h-h.subs(a,a+s.pi)-s.cos(3*a)/8) == 0)
check('noncentral third harmonic', s.integrate((h-h.subs(a,a+s.pi))*s.cos(3*a),(a,0,2*s.pi)) == s.pi/8)
check('translation has zero third harmonic', s.integrate((2*x*s.cos(a)+2*y*s.sin(a))*s.cos(3*a),(a,0,2*s.pi)) == 0)
check('width two', s.trigsimp(h+h.subs(a,a+s.pi)-2) == 0)
print(json.dumps({'status':'PASS','exact_assertions':len(checks),'checks':checks,
 'scope':'Support-function identities and noncentral symmetry only. KAM existence and infinite-sequence selection are written/theorem arguments, not computed.'},indent=2))
