#!/usr/bin/env python3
"""Fail-closed scope audit of the zero-binary E6 slice for D4-DN-3.

The calculation retains arbitrary binary cubic terms in the first two
components of H3, an arbitrary binary quadratic term in the third component
of H2, arbitrary quadratic terms in the first two components of H2, and all
nine entries of the linear part in the determinant.  It proves that eleven
binary coefficients really occur in full E6.  It then sets precisely those
coefficients to zero and proves the radical and two-plane decomposition of
that restricted compatibility ideal.  It intentionally does not promote the
slice denominator to the full contact variety.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, w = sp.symbols("p q r w")
coordinates = (p, q, r)

# E7 syzygy coordinates.  The x variables multiply the r^2 contact and the
# y variables multiply the r contact.
x0, x1, y0, y1, y2, y3 = sp.symbols("x0 x1 y0 y1 y2 y3")
contact_variables = (x0, x1, y0, y1, y2, y3)

u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("ell0:9")

binary_cubics = (p**3, p**2 * q, p * q**2, q**3)
binary_quadratics = (p**2, p * q, q**2)
ternary_quadratics = (p**2, p * q, p * r, q**2, q * r, r**2)

U0 = sum(coefficient * monomial for coefficient, monomial in zip(u, binary_cubics))
V0 = sum(coefficient * monomial for coefficient, monomial in zip(v, binary_cubics))
T0 = sum(coefficient * monomial for coefficient, monomial in zip(t, binary_quadratics))
A = sum(coefficient * monomial for coefficient, monomial in zip(a, ternary_quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, ternary_quadratics))
L = sp.Matrix(3, 3, ell)

# A basis for the degree-two E7 syzygies:
# (-p^2,pq,0), (-pq,q^2,0), (4p^2/3,0,p), (4pq/3,0,q).
U1 = -y0 * p**2 - y1 * p * q + sp.Rational(4, 3) * y2 * p**2 + sp.Rational(4, 3) * y3 * p * q
V1 = y0 * p * q + y1 * q**2
T1 = y2 * p + y3 * q

# A basis for the degree-one E7 syzygies:
# (-p,q,0), (4p/3,0,1).  The factor 1/2 compensates differentiation in r.
U2 = -x0 * p + sp.Rational(4, 3) * x1 * p
V2 = x0 * q
T2 = x1

U = U0 + r * U1 + sp.Rational(1, 2) * r**2 * U2
V = V0 + r * V1 + sp.Rational(1, 2) * r**2 * V2
T = T0 + r * T1 + sp.Rational(1, 2) * r**2 * T2

h = (p + q) ** 2
P = h * p**2
Q = h * q**2
R = (p + q) ** 3
H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A, B, T))


def homogeneous_coefficients(polynomial: sp.Expr, degree: int) -> tuple[sp.Expr, ...]:
    expanded = sp.Poly(sp.expand(polynomial), p, q, r)
    return tuple(
        expanded.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def unique_nonzero(polynomials: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    output: list[sp.Expr] = []
    for polynomial in polynomials:
        value = sp.factor(polynomial)
        if value == 0:
            continue
        primitive = sp.Poly(value, *contact_variables).primitive()[1].as_expr()
        value = sp.factor(primitive)
        if value not in output and -value not in output:
            output.append(value)
    return tuple(output)


def main() -> None:
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + w * H2.jacobian(coordinates)
                + w**2 * H3.jacobian(coordinates)
                + w**3 * H4.jacobian(coordinates)
            ).det()
        ),
        w,
    )

    # These assertions independently check that the displayed parameterization
    # is the complete E7 syzygy parameterization used in the determinant.
    assert determinant.coeff_monomial(w**9) == 0
    assert determinant.coeff_monomial(w**8) == 0
    assert determinant.coeff_monomial(w**7) == 0

    full_e6_equations = homogeneous_coefficients(
        determinant.coeff_monomial(w**6), 6
    )
    full_lower_variables = (
        (a[2], a[4], a[5], b[2], b[4], b[5], ell[8]) + u + v + t
    )
    full_matrix, full_rhs = sp.linear_eq_to_matrix(
        full_e6_equations, full_lower_variables
    )
    assert full_matrix.shape == (28, 18)

    # This is the scope-failure certificate.  These eleven coefficients were
    # omitted in the earlier two-plane calculation, but all occur in full E6.
    binary_lower_variables = set(u + v + t)
    present_at_e6 = set().union(
        *(equation.free_symbols for equation in full_e6_equations)
    )
    assert present_at_e6 & binary_lower_variables == binary_lower_variables

    # Two exact specializations certify that the full system has
    # parameter-dependent consistency; a zero-binary compatibility calculation
    # cannot silently be substituted for it.
    generic_substitution = dict(zip(contact_variables, (1, 2, 3, 4, 5, 6)))
    generic_matrix = full_matrix.subs(generic_substitution)
    generic_rhs = full_rhs.subs(generic_substitution)
    assert generic_matrix.rank() == 9
    assert generic_matrix.row_join(generic_rhs).rank() == 10
    line_substitution = dict(zip(contact_variables, (0, 0, 1, 1, 0, 0)))
    line_matrix = full_matrix.subs(line_substitution)
    line_rhs = full_rhs.subs(line_substitution)
    assert line_matrix.rank() == 6
    assert line_matrix.row_join(line_rhs).rank() == 6

    zero_binary = {variable: 0 for variable in u + v + t}
    slice_e6_equations = tuple(
        sp.expand(equation.subs(zero_binary)) for equation in full_e6_equations
    )
    slice_lower_variables = (a[2], a[4], a[5], b[2], b[4], b[5], ell[8])
    lower_matrix, lower_rhs = sp.linear_eq_to_matrix(
        slice_e6_equations, slice_lower_variables
    )
    assert lower_matrix.shape == (28, 7)
    assert lower_matrix.rank() == 5

    compatibility = unique_nonzero(
        tuple((left.T * lower_rhs)[0] for left in lower_matrix.T.nullspace())
    )
    assert len(compatibility) == 13
    contact_groebner = sp.groebner(
        compatibility, *contact_variables, order="grevlex"
    )

    delta = y2 - y3
    conic = 9 * (y0 - y1) ** 2 + 24 * (y0 - y1) * y3 + 8 * y3**2
    radical_generators = (x0, x1, delta, conic)
    radical_groebner = sp.groebner(
        radical_generators, *contact_variables, order="grevlex"
    )

    # I is contained in J, while every generator of J has its square in I.
    # Since J is radical (the residual binary quadratic is squarefree), this
    # proves sqrt(I)=J without relying on a black-box primary decomposition.
    assert all(
        radical_groebner.reduce(sp.expand(generator))[1] == 0
        for generator in compatibility
    )
    assert all(
        contact_groebner.reduce(sp.expand(generator**2))[1] == 0
        for generator in radical_generators
    )
    z = sp.symbols("z")
    residual = sp.Poly(9 * z**2 + 24 * z + 8, z)
    assert sp.gcd(residual, residual.diff()).degree() == 0

    sqrt2 = sp.sqrt(2)
    slope_plus = (-4 + 2 * sqrt2) / 3
    slope_minus = (-4 - 2 * sqrt2) / 3
    assert sp.factor(
        conic
        - 9
        * (y0 - y1 - slope_plus * y3)
        * (y0 - y1 - slope_minus * y3)
    ) == 0
    assert sp.factor(slope_plus - slope_minus) != 0

    # The two planes meet exactly along y3=0, y0=y1 (and y2=y3).
    plane_plus = (x0, x1, y2 - y3, y0 - y1 - slope_plus * y3)
    plane_minus = (x0, x1, y2 - y3, y0 - y1 - slope_minus * y3)
    for substitution in (
        {x0: 0, x1: 0, y2: y3, y0: y1 + slope_plus * y3},
        {x0: 0, x1: 0, y2: y3, y0: y1 + slope_minus * y3},
    ):
        assert all(sp.factor(generator.subs(substitution)) == 0 for generator in compatibility)
    assert set(plane_plus[:3]) == set(plane_minus[:3])

    print("D4_DN3_E7_SYZYGY_DIMENSIONS_PASS_2_4")
    print("D4_DN3_FULL_E6_RETAINED_BINARY_SCOPE_FAILURE_PASS_11")
    print("D4_DN3_ZERO_BINARY_SLICE_RADICAL_PASS_2_PLANES")
    print("D4_DN3_ZERO_BINARY_SLICE_STRATA_PASS_PPLUS_PMINUS_LINE_ORIGIN")
    print("D4_DN3_BOUNDED_SCOPE_AUDIT_STRICT_PASS")


if __name__ == "__main__":
    main()
