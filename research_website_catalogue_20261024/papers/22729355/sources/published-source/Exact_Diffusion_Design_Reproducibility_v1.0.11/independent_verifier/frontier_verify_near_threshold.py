#!/usr/bin/env python3
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import sympy as sp
from pareto_core import A, Hessian, cvec, rhovec


def verify_affine_ansatz(m: int) -> None:
    """Reconstruct every printed affine-vector diffusion identity exactly."""
    u0, v0, p0, q0 = sp.symbols("u v p q", nonzero=True)
    r_aff = sp.Matrix(
        [1]
        + [
            -(u0 + v0 * sp.Rational(m - 1 - i, m - 2))
            for i in range(2, m)
        ]
        + [-p0, q0]
    )
    d = [
        -2 + u0 + p0 + 2 * q0,
        sp.factor(
            (
                1
                + 2 * p0
                - u0
                - v0 * sp.Rational(m - 3, m - 2)
            )
            / (u0 + v0 * sp.Rational(m - 3, m - 2))
        ),
    ]
    d += [
        sp.factor(v0 / ((m - 2) * u0 + v0 * (m - 1 - i)))
        for i in range(3, m)
    ]
    d += [
        sp.factor((2 * u0 - 5 * p0 - 2 * q0 - 1) / p0),
        sp.factor((2 - 2 * p0 - 4 * q0) / q0),
    ]
    residual = (A(m) - sp.diag(*d)) * r_aff
    assert all(sp.factor(entry) == 0 for entry in residual)


for dimension in (3, 4, 5, 6, 8, 10):
    verify_affine_ansatz(dimension)

e,omega,M,theta,nu,k=sp.symbols('epsilon omega M theta nu k',positive=True)
p=e;u=1+(2-omega)*e+theta*e**2;v=omega*e-theta*e**2
q=sp.Rational(1,2)-(sp.Rational(1,2)+omega)*e+(theta-M/sp.Integer(2))*e**2
d1=sp.factor(-2+u+p+2*q);dm=sp.factor((2*u-5*p-2*q-1)/p);dz=sp.factor((2-2*p-4*q)/q)
di=sp.factor(v/(nu*u+v*k))
assert sp.expand(d1-(e*(2-3*omega)+(3*theta-M)*e**2))==0
assert sp.expand(dm-M*e)==0
sum2=sp.factor(sp.summation(sp.series(di,e,0,3).removeO(),(k,0,nu-1)))
delta=sp.factor(sp.series(dz-8*sum2,e,0,3).removeO())
assert sp.factor(delta-4*e**2*(M*nu+3*nu*omega**2+6*nu*omega-omega**2)/nu)==0

def positive_rational_certificate(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    substitutions: dict[sp.Symbol, sp.Expr],
    expected_terms: tuple[int, int],
) -> None:
    """Prove positivity on a nonnegative orthant by exact coefficients."""

    numerator, denominator = sp.fraction(sp.factor(expression.subs(substitutions)))
    numerator_poly = sp.Poly(numerator, *variables)
    denominator_poly = sp.Poly(denominator, *variables)
    if all(coefficient < 0 for coefficient in denominator_poly.coeffs()):
        numerator_poly = sp.Poly(-numerator, *variables)
        denominator_poly = sp.Poly(-denominator, *variables)
    assert len(numerator_poly.terms()) == expected_terms[0]
    assert len(denominator_poly.terms()) == expected_terms[1]
    assert all(coefficient > 0 for coefficient in numerator_poly.coeffs())
    assert all(coefficient > 0 for coefficient in denominator_poly.coeffs())
    assert numerator_poly.coeff_monomial(1) > 0
    assert denominator_poly.coeff_monomial(1) > 0


def is_zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.factor(entry) == 0 for entry in matrix)


# Exact m=3 prescribed-path control, reconstructed from the reaction list.
A3=A(3)
r3=sp.Matrix([1,-(1+sp.Rational(16,9)*e+e**2/2),-e,sp.Rational(1,2)-sp.Rational(13,18)*e])
d3=[sp.factor(entry/r3[index]) for index,entry in enumerate(A3*r3)]
expected_d3=[
    e*(3*e+8)/6,
    e*(4-9*e)/(9*e**2+32*e+18),
    e,
    16*e/(9-13*e),
]
assert all(sp.factor(actual-expected)==0 for actual,expected in zip(d3,expected_d3))
D3=sp.diag(*d3)
M3=A3-D3
assert is_zero_matrix(M3*r3)
ell3=M3.T.nullspace()[0]
ell3=sp.simplify(ell3/ell3[-1])
assert is_zero_matrix(ell3.T*M3)

forcing=-Hessian(3,r3,r3)/4
bordered=A3.row_join(rhovec(3)).col_join(cvec(3).T.row_join(sp.zeros(1)))
w0=bordered.inv()*forcing.col_join(sp.zeros(1,1))
w0=sp.Matrix(w0[:-1,0])
w2=(A3-4*D3).inv()*forcing
assert is_zero_matrix(A3*w0-forcing)
assert sp.factor((cvec(3).T*w0)[0])==0
assert is_zero_matrix((A3-4*D3)*w2-forcing)

cubic=sp.factor(
    (ell3.T*(Hessian(3,r3,w0)+Hessian(3,r3,w2)/2))[0]
    /(ell3.T*r3)[0]
)
N=(18718533*e**12+746773020*e**11+6223086873*e**10+19157763816*e**9+12668661720*e**8-49876101168*e**7-103878539968*e**6-37609207926*e**5+68189826636*e**4+62316267192*e**3+9680484312*e**2-3464522928*e-238085568)
D1=81*e**4+531*e**3+708*e**2-1102*e-1182
D2=243*e**6+2133*e**5+7431*e**4+5047*e**3-10329*e**2-17415*e-3402
assert sp.factor(cubic+N/(13608*D1*D2))==0
assert sp.limit(cubic,e,0,dir='+')==sp.Rational(6,1379)
assert sp.limit((cubic-sp.Rational(6,1379))/e,e,0,dir='+')==sp.Rational(421985,11409846)
assert sp.factor(d3[3]-8*d3[1]-8*e**2*(197-99*e)/((9-13*e)*(9*e**2+32*e+18)))==0

# The substitution e=1/[1000(1+w)] maps the full interval
# 0<e<=1/1000 to w>=0.  It proves diffusion, cubic, pairing, and
# transversality signs without sampling.
s,w=sp.symbols('s w',nonnegative=True)
interval_substitution={e:1/(1000*(1+w))}
for expression,counts in zip(d3,((2,3),(2,3),(1,2),(1,2))):
    positive_rational_certificate(expression,(w,),interval_substitution,counts)
positive_rational_certificate(cubic,(w,),interval_substitution,(13,13))
positive_rational_certificate(-(ell3.T*r3)[0],(w,),interval_substitution,(7,7))

lam,t=sp.symbols('lambda t')
characteristic=sp.Poly((lam*sp.eye(4)-A3+t*D3).det(method='domain-ge'),lam)
assert characteristic.LC()==1
a1,a2,a3,a4=map(sp.factor,characteristic.all_coeffs()[1:])
H2=sp.factor(a1*a2-a3)
H3=sp.factor(a3*H2-a1**2*a4)
spatial_substitution={t:1+s,e:1/(1000*(1+w))}
for expression,counts in (
    (a1,(11,6)),
    (a2,(18,7)),
    (a3,(22,7)),
    (sp.cancel(a4/(t-1)),(17,7)),
    (H2,(42,12)),
    (H3,(105,18)),
):
    positive_rational_certificate(expression,(s,w),spatial_substitution,counts)

assert sp.factor(a4.subs(t,1))==0
eta=sp.factor((ell3.T*D3*r3)[0]/(ell3.T*r3)[0])
assert sp.factor(eta-sp.diff(a4,t).subs(t,1)/a3.subs(t,1))==0
positive_rational_certificate(eta,(w,),interval_substitution,(5,7))
homogeneous_quotient=sp.factor((lam*sp.eye(4)-A3).det()/lam)
assert sp.factor(homogeneous_quotient-(lam+7)*(lam**2+5*lam+2))==0
print('VERIFY_NEAR_THRESHOLD_PASS')
