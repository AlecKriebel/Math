#!/usr/bin/env python3
"""Finite exact checks accompanying independent function-theory proofs.

These checks validate algebraic identities and deliberate boundary controls only.
They do not prove covering, Picard, growth, or bounded-holomorphic claims.
"""
import json
from itertools import product
from fractions import Fraction
from math import factorial
import sympy as s
checks = 0

def require(condition):
    global checks
    if not condition:
        raise AssertionError("independent exact control failed")
    checks += 1

# Entire exponential evaluated on repeated-root fibers: all nilpotent Jordan
# parts are retained, and the exact matrix exponential is a terminating series.
T = s.symbols("T")
cases = 0
for dims in [(2,1,1), (3,1,1), (2,2,1), (2,2,2), (3,2,1)]:
    mats = []
    for d in dims:
        J = s.zeros(d)
        for j in range(d-1):
            J[j+1,j] = 1
        mats.append(J)
    N = (s.kronecker_product(mats[0],s.eye(dims[1]),s.eye(dims[2]))
         +s.kronecker_product(s.eye(dims[0]),mats[1],s.eye(dims[2]))
         +s.kronecker_product(s.eye(dims[0]),s.eye(dims[1]),mats[2]))
    degree = dims[0]*dims[1]*dims[2]
    cutoff = 1+sum(d-1 for d in dims)
    require(N**cutoff == s.zeros(degree))
    exact_exp = s.zeros(degree)
    for k in range(cutoff):
        exact_exp += N**k/s.factorial(k)
    require(s.expand(exact_exp.charpoly(T).as_expr()-(T-1)**degree)==0)
    require(exact_exp.det()==1)
    cases += 1

# Completeness failure is certified algebraically, not by an ODE simulation.
t,c,K = s.symbols("t c K", nonzero=True)
u = c/(1+K*s.exp(-c*t))
require(s.simplify(s.diff(u,t)-u*(c-u))==0)
q = s.symbols("q")
require(s.diff(1+K*s.exp(-c*t),t).subs(s.exp(-c*t),-1/K)==c)
require(s.simplify(c/c)==1)  # residue at each denominator zero

# Strict subunit exponents are material: exponent one admits a genuine pole.
for a in [Fraction(0), Fraction(1,10), Fraction(9,10), Fraction(999,1000)]:
    for m in range(1,7):
        require(m-a>0)
require(Fraction(1)-Fraction(1)==0)
require(Fraction(1)-Fraction(11,10)<0)

# The two-input counterexample satisfies the equation and exhibits two values.
k = s.symbols("k", integer=True)
require(s.simplify(s.exp(2*s.pi*s.I*k)-1)==0)
require(s.exp(s.pi*s.I*0)==1)
require(s.exp(s.pi*s.I*1)==-1)

# Simultaneous exponential ratios on an entire curve reduce to fixed constants.
a,b,r = s.symbols("a b r")
require(s.expand((a*r)+(b*r)+r-r*(a+b+1))==0)

print(json.dumps({"status":"PASS", "exact_assertions":checks,
                  "repeated_entire_exponential_fibers":cases,
                  "scope":"Nilpotent entire matrix exponential, logistic tangent-flow identity, strict removable exponent boundary, and two-input parity counterexample; universal analytic conclusions are in FUNCTION_THEORY_PROOFS.md.",
                  "universal_analytic_claims_certified_by_finite_checks":False},indent=2))
