#!/usr/bin/env python3
"""Exact interface checks for the network-specific one-bad-minor corollary on the flagship family."""
from itertools import combinations
import sympy as sp
from core import Avec

for m in (3,4,5,6):
    n=m+1
    A=Avec(m)
    # A generic positive rational diffusion vector satisfying the criterion.
    d=[sp.Rational(i+3,i+2) for i in range(n)]
    d[-1]=sp.Integer(100*m)
    betas=[]
    for k in range(1,n+1):
        total=0
        for I in combinations(range(n),n-k):
            Ic=[j for j in range(n) if j not in I]
            det=sp.Integer(1) if not I else A.extract(I,I).det()
            total += (-1)**len(I)*det*sp.prod(d[j] for j in Ic)
        betas.append(sp.factor(total))
    assert betas[0] < 0
    assert all(x>0 for x in betas[1:])
    s=sp.symbols('s', nonnegative=True)
    q=sum(betas[k]*s**k for k in range(n))
    assert sp.Poly(sp.diff(q,s),s).all_coeffs() and all(c>0 for c in sp.Poly(sp.diff(q,s),s).all_coeffs())
    # The lambda derivative's order-(n-1) contribution equals the positive
    # coefficient of lambda in det(lambda I-A).
    lam=sp.symbols('lam', nonnegative=True)
    coeff=sp.Poly((lam*sp.eye(n)-A).det(),lam).coeff_monomial(lam)
    signed_sum=sum((-1)**(n-1)*A.extract(I,I).det() for I in combinations(range(n),n-1))
    assert sp.factor(coeff-signed_sum)==0 and coeff>0
print("NETWORK_ONE_BAD_MINOR_COROLLARY_PASS")
