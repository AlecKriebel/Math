#!/usr/bin/env python3
"""Exact algebra for corrected-square Foster and Lamperti calibrations."""
from __future__ import annotations
from dataclasses import dataclass
import sympy as sp

@dataclass(frozen=True,slots=True)
class SquareDriftCertificate:
    a:sp.Expr
    v:sp.Expr
    xi:sp.Expr
    strict:bool


def square_coefficient(a:sp.Expr,v:sp.Expr,assumptions:dict[sp.Symbol,str]|None=None)->SquareDriftCertificate:
    xi=sp.factor(2*sp.sympify(a)+sp.sympify(v))
    strict=False
    if xi.is_negative:strict=True
    return SquareDriftCertificate(sp.factor(a),sp.factor(v),xi,strict)


def birth_death_xi(lambda_n:sp.Expr,mu_n:sp.Expr,n:sp.Symbol)->sp.Expr:
    """Return lim coefficient of L(n^2) when rates have a finite limit form."""
    expr=sp.expand(lambda_n*((n+1)**2-n**2)+mu_n*((n-1)**2-n**2))
    return sp.factor(sp.limit(expr,n,sp.oo))


def verify_negative_rational(expr:sp.Expr,n:sp.Symbol,threshold:int)->bool:
    """Exact sufficient check: numerator has all coefficients <=0 after n=N0+t."""
    t=sp.symbols('_t',nonnegative=True)
    num,den=sp.fraction(sp.cancel(expr.subs(n,t+threshold)))
    P=sp.Poly(sp.expand(num),t)
    Q=sp.Poly(sp.expand(den),t)
    return all(c<=0 for c in P.all_coeffs()) and all(c>=0 for c in Q.all_coeffs()) and any(c<0 for c in P.all_coeffs())


def self_test()->None:
    n=sp.symbols('n',positive=True)
    # lambda=1-c/n, mu=1 gives a=-c,v=2 and Xi=2-2c.
    c=sp.symbols('c',positive=True)
    assert sp.simplify(birth_death_xi(1-c/n,1,n)-(2-2*c))==0
    assert verify_negative_rational(-1-1/n,n,1)

if __name__=='__main__':self_test();print('lamperti_verifier.py self-test: OK')
