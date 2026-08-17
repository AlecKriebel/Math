#!/usr/bin/env python3
"""Exact checks for the generalized principal-minor diffusion-ray theorem.

This verifier checks the coefficient expansion and derivative decomposition on
independently reconstructed matrix families.  The human proof is algebraic and
is printed in the manuscript/supplement; these checks are mutation-sensitive
interfaces, not a finite substitute for that proof.
"""
from __future__ import annotations
from itertools import combinations
import sympy as sp
from core import Avec


def signed_minor(J: sp.Matrix, I: tuple[int, ...]) -> sp.Expr:
    if not I:
        return sp.Integer(1)
    return sp.factor((-1) ** len(I) * J.extract(I, I).det())


def betas(J: sp.Matrix, d: list[sp.Expr]) -> list[sp.Expr]:
    n = J.rows
    out=[]
    for k in range(1,n+1):
        total=0
        for I in combinations(range(n),n-k):
            comp=[j for j in range(n) if j not in I]
            total += signed_minor(J,I)*sp.prod(d[j] for j in comp)
        out.append(sp.factor(total))
    return out


def audit(J: sp.Matrix, d: list[sp.Expr], expect_crossing: bool) -> None:
    n=J.rows
    assert J.det()==0
    for r in range(n-1):
        for I in combinations(range(n),r):
            assert signed_minor(J,I)>0
    order_sum=sp.factor(sum(signed_minor(J,I) for I in combinations(range(n),n-1)))
    assert order_sum>0
    bs=betas(J,d)
    assert all(x>0 for x in bs[1:])
    assert bool(bs[0] < 0) == expect_crossing

    s,lam=sp.symbols('s lam', positive=True)
    p=sp.factor((s*sp.diag(*d)-J).det())
    q=sp.factor(p/s)
    q_from=sum(bs[k]*s**k for k in range(n))
    assert sp.factor(q-q_from)==0
    assert all(c>0 for c in sp.Poly(sp.diff(q,s),s).all_coeffs())

    # Exact derivative decomposition: lower-order terms are individually
    # positive; order-(n-1) terms contribute their positive total.
    derivative=sp.diff((lam*sp.eye(n)+s*sp.diag(*d)-J).det(),lam)
    manual=0
    for r in range(n):
        for I in combinations(range(n),r):
            comp=[j for j in range(n) if j not in I]
            a=signed_minor(J,I)
            manual += a*sum(sp.prod(lam+s*d[j] for j in comp if j!=k) for k in comp)
    assert sp.factor(derivative-manual)==0


# No-crossing singular stable M-matrix example.
for n in (3,4,5):
    J=sp.ones(n)-n*sp.eye(n)  # eigenvalues 0,-n,...,-n
    audit(J,[sp.Rational(j+2,j+1) for j in range(n)],False)

# Crossing examples from the reaction topology.
for m in (3,4,5,6):
    A=Avec(m)
    d=[sp.Rational(i+3,i+2) for i in range(m+1)]
    d[-1]=sp.Integer(100*m)
    audit(A,d,True)

print('PRINCIPAL_MINOR_DIFFUSION_RAY_PASS')
