#!/usr/bin/env python3
"""Full lower identities on the two-contact leaf w^2=-1, a=0.

This is the unique exact-open point on the singular generic E7 chart
whose lifted E6 contact kernel meets the Veronese cone.  The top-only
E5 obstruction vanishes, so all lower coefficients are retained here.
"""

from __future__ import annotations

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
w = sp.I
variables = (p, q, r)

uc = sp.symbols("u0:4")
vc = sp.symbols("v0:4")
tc = sp.symbols("t0:3")
xc = sp.symbols("x0:5")
yc = sp.symbols("y0:5")
ell = sp.symbols("l0:9")


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        sp.expand(poly.coeff_monomial(p ** (degree - index) * q**index))
        for index in range(degree + 1)
    ]


h = w * (p**2 + q**2)
H4 = sp.Matrix([h * p**2, h * q**2, 0])
H3 = sp.Matrix(
    [
        binary(uc, 3) + r * (2 * p**2 + q**2),
        binary(vc, 3) + r * q**2,
        4 * w * q**3,
    ]
)
H2 = sp.Matrix(
    [
        binary(xc[:3], 2)
        + r * (xc[3] * p + xc[4] * q)
        - w * r**2,
        binary(yc[:3], 2) + r * (yc[3] * p + yc[4] * q),
        binary(tc, 2),
    ]
)
L = sp.Matrix(3, 3, ell)

weighted = sp.Poly(
    sp.expand(
        (
            L
            + z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E = {
    degree: sp.expand(weighted.coeff_monomial(z**degree))
    for degree in range(9)
}
assert E[8] == 0
assert E[7] == 0

E6 = sp.Poly(E[6], r)
print("E6 r-degree", E6.degree())
for power in range(E6.degree(), -1, -1):
    value = sp.expand(E6.coeff_monomial(r**power))
    if value != 0:
        print("E6 r^", power, "=", sp.factor(value, extension=sp.I))

eq6 = coefficients(E[6], 6)
unknown6 = (
    xc[3],
    xc[4],
    yc[3],
    yc[4],
    ell[8],
    *tc,
    *uc,
    *vc,
)
M6, rhs6 = sp.linear_eq_to_matrix(eq6, unknown6)
print("E6 matrix", M6.shape, "rank", M6.rank(), "pivots", M6.rref()[1])
print("E6 free symbols", sorted(
    {str(symbol) for equation in eq6 for symbol in equation.free_symbols}
))
print("E6 solution", sp.linsolve((M6, rhs6), unknown6))

e6_solution = {
    xc[3]: -sp.Rational(3, 2) * w * uc[0]
    + sp.Rational(3, 4) * w * uc[2]
    + sp.Rational(1, 4) * w * vc[2],
    xc[4]: -w * uc[1],
    yc[3]: -sp.Rational(1, 4) * w * uc[2]
    - sp.Rational(3, 2) * w * vc[0]
    + sp.Rational(1, 4) * w * vc[2],
    yc[4]: -w * vc[1],
    ell[8]: -w * tc[0],
    tc[1]: -3 * uc[2] + 3 * vc[2],
}
assert sp.expand(E[6].subs(e6_solution)) == 0

E5 = sp.Poly(sp.expand(E[5].subs(e6_solution)), r)
print("E5 r-degree", E5.degree())
print(
    "E5 r^1 =",
    sp.factor(E5.coeff_monomial(r), extension=sp.I),
)

e5_high = {
    uc[0]: 2 * uc[2] + vc[0],
    vc[2]: uc[2] + 2 * vc[0],
}
assert sp.expand(E5.coeff_monomial(r).subs(e5_high)) == 0
E5constant = sp.expand(E5.coeff_monomial(1).subs(e5_high))
eq5 = coefficients(E5constant, 5)
print("E5 constant free symbols", sorted(
    {str(symbol) for equation in eq5 for symbol in equation.free_symbols}
))
M5ell, rhs5ell = sp.linear_eq_to_matrix(eq5, ell[:8])
print(
    "E5 constant L matrix",
    M5ell.shape,
    "rank",
    M5ell.rank(),
    "pivots",
    M5ell.rref()[1],
)
print("E5 L compatibility count", len(M5ell.T.nullspace()))
for index, vector in enumerate(M5ell.T.nullspace()):
    print(
        "E5 L compatibility",
        index,
        sp.factor((vector.T * rhs5ell)[0], extension=sp.I),
    )

e5_compatibility = {
    vc[0]: 0,
    xc[1]: -w * uc[1] * uc[2],
    yc[1]: -w * uc[2] * vc[1],
}
eq5_compatible = [
    sp.expand(equation.subs(e5_compatibility)) for equation in eq5
]
unknown5 = (ell[2], ell[5], ell[6])
M5, rhs5 = sp.linear_eq_to_matrix(eq5_compatible, unknown5)
print(
    "E5 compatible matrix",
    M5.shape,
    "rank",
    M5.rank(),
    "pivots",
    M5.rref()[1],
)
print("E5 compatible solution", sp.linsolve((M5, rhs5), unknown5))

e5_solution = {
    uc[0]: 2 * uc[2],
    vc[0]: 0,
    vc[2]: uc[2],
    xc[1]: -w * uc[1] * uc[2],
    yc[1]: -w * uc[2] * vc[1],
    ell[2]: uc[2] ** 2 - w * xc[0],
    ell[5]: -w * yc[0],
    ell[6]: -w * tc[0] * uc[2],
}
assert sp.expand(E[5].subs(e6_solution).subs(e5_solution)) == 0

E4 = sp.Poly(
    sp.expand(E[4].subs(e6_solution).subs(e5_solution)),
    r,
)
print("E4 r-degree", E4.degree())
for power in range(E4.degree(), -1, -1):
    value = sp.factor(E4.coeff_monomial(r**power), extension=sp.I)
    if value != 0:
        print("E4 r^", power, "=", value)

e4_solution = {
    ell[3]: -w * uc[2] * yc[0],
    ell[0]: uc[2] ** 3 - w * uc[2] * xc[0],
}
assert (
    sp.expand(
        E[4].subs(e6_solution).subs(e5_solution).subs(e4_solution)
    )
    == 0
)

E3 = sp.Poly(
    sp.expand(
        E[3].subs(e6_solution).subs(e5_solution).subs(e4_solution)
    ),
    r,
)
print("E3 r-degree", E3.degree())
assert E3.is_zero
print("E3 identically zero")

def reduced(value):
    return sp.expand(
        value.subs(e6_solution).subs(e5_solution).subs(e4_solution)
    )


for degree in (2, 1):
    current = sp.Poly(reduced(E[degree]), r)
    print(f"E{degree} r-degree", current.degree())
    assert current.is_zero
    if not current.is_zero:
        for power in range(int(current.degree()), -1, -1):
            value = sp.factor(
                current.coeff_monomial(r**power), extension=sp.I
            )
            if value != 0:
                print(f"E{degree} r^", power, "=", value)

Ldone = L.applyfunc(reduced)
assert sp.simplify(Ldone[:, 0] - uc[2] * Ldone[:, 2]) == sp.zeros(3, 1)
assert sp.expand(Ldone.det()) == 0
print("det L =", sp.factor(Ldone.det(), extension=sp.I))
print("PASS full u=-1,a=0 lower chain forces col_1(L)=u2 col_3(L)")
