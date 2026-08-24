#!/usr/bin/env python3
"""Finite/exact regeneration checks for the unit-profile mode certificates."""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import json,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
cert=json.loads((HERE/'improved_modulus_certificate.json').read_text())
assert cert['homogeneous']['term_count']==35
assert cert['improved_mode']['term_count']==77
for sec in cert.values():
 for term in sec['terms']: assert sp.Rational(term['coefficient'])>0
# Reconstruct the homogeneous polynomial as well.
xh,yh,zh=sp.symbols('xh yh zh',real=True);lh=xh+sp.I*yh
Ph=lh**4+12*lh**3+42*lh**2+47*lh+16
Rh=5*lh**2+33*lh+16
def yh2z(expr):
 out=0
 for (k,),c in sp.Poly(sp.expand(expr),yh).terms(): assert k%2==0;out+=c*zh**(k//2)
 return sp.expand(out)
Eh=sp.Poly(yh2z((1+lh)*(1+sp.conjugate(lh))*Ph*sp.conjugate(Ph)-Rh*sp.conjugate(Rh)),xh,zh)
hterms={(tuple(t['powers']),sp.Rational(t['coefficient'])) for t in cert['homogeneous']['terms']}
assert hterms=={(mon,sp.factor(c)) for mon,c in Eh.terms()}

# Reconstruct the improved polynomial rather than trusting the JSON.
x,y,z,s=sp.symbols('x y z s',real=True);lam=x+sp.I*y;t=1+s
q=sp.Rational(91,90);d1=sp.Rational(23,63);dm=sp.Rational(1,7);dz=sp.Rational(16,45)
g1=lam+2+t*d1;gm=lam+5+t*dm;gz=lam+4+t*dz
F=sp.expand(g1*gm*gz-4*g1-4*gm+gz);G=sp.expand(gz*(4*g1+gm)-36)
def y2z(expr):
 out=0
 for (k,),c in sp.Poly(sp.expand(expr),y).terms(): assert k%2==0;out+=c*z**(k//2)
 return sp.expand(out)
E=sp.Poly(sp.expand((q*q+z)*y2z(F*sp.conjugate(F))-y2z(G*sp.conjugate(G))),x,z,s)
terms={(tuple(t['powers']),sp.Rational(t['coefficient'])) for t in cert['improved_mode']['terms']}
assert terms=={(mon,sp.factor(c)) for mon,c in E.terms()}

def verify_selected_zero_derivative():
    """Prove the all-dimensional algebraic-simplicity identity at onset."""

    m,hfrak,index=sp.symbols('m hfrak index',integer=True,positive=True)
    lam0=sp.symbols('lam0')

    # At t=1, the chain factors telescope and their logarithmic derivative
    # is (m-2)-hfrak, where hfrak=sum_{j=1}^{m-2} 1/K_j.
    K=lambda j: 91*m-181-j
    assert sp.factor(1+1/K(index)-K(index-1)/K(index))==0
    assert sp.factor(1/(1+1/K(index))-(1-1/K(index-1)))==0
    assert sp.factor(K(1)/K(m-1)-sp.Rational(91,90))==0
    Q0=sp.Rational(91,90)
    Qprime0=Q0*(m-2-hfrak)

    g1=lam0+2+sp.Rational(23,63)
    gm=lam0+5+sp.Rational(1,7)
    gz=lam0+4+sp.Rational(16,45)
    F0=sp.expand(g1*gm*gz-4*g1-4*gm+gz)
    G0=sp.expand(gz*(4*g1+gm)-36)
    determinant_derivative=sp.factor(
        Qprime0*F0.subs(lam0,0)
        +Q0*sp.diff(F0,lam0).subs(lam0,0)
        -sp.diff(G0,lam0).subs(lam0,0)
    )
    expected=(7043400*m-13600927-7043400*hfrak)/sp.Integer(255150)
    assert sp.factor(determinant_derivative-expected)==0

    from common import ellr_formula
    assert sp.factor(
        determinant_derivative+sp.Rational(163,45)*ellr_formula(m,hfrak)
    )==0

    # The existing harmonic upper bound makes the numerator positive.  Its
    # cleared lower bound is the printed shifted-positive polynomial.
    harmonic_upper=(m-2)/(90*m-179)
    cleared=sp.together(
        (7043400*m-13600927-7043400*harmonic_upper)
    ).as_numer_denom()[0]
    u=sp.symbols('u',nonnegative=True)
    shifted=sp.Poly(sp.expand(cleared.subs(m,u+3)),u).all_coeffs()
    assert shifted==[633906000,1311540570,678120443]
    assert all(coefficient>0 for coefficient in shifted)


verify_selected_zero_derivative()

# Exact finite reconstruction of the sparse determinant formula.
from common import Avec,selected
for mm in [3,4,5]:
    lamv,tv=sp.symbols(f'lam{mm} t{mm}')
    A=Avec(mm);_,ds,_=selected(mm)
    g1=lamv+2+tv*ds[0];gm=lamv+5+tv*ds[mm-1];gz=lamv+4+tv*ds[mm]
    Q=sp.prod(lamv+1+tv*ds[i-1] for i in range(2,mm))
    F=g1*gm*gz-4*g1-4*gm+gz
    G=gz*(4*g1+gm)-36
    assert sp.factor((lamv*sp.eye(mm+1)-A+tv*sp.diag(*ds)).det()-(Q*F-G))==0

print('MODE_ISOLATION_PASS')
