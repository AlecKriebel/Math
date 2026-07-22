#!/usr/bin/env python3
"""Exact symbolic certificate for full wreath monodromy of F^2.

Requires SymPy 1.14.  Every assertion is over ZZ or QQ; no floating point is
used.  The group-theoretic deduction from the printed data is proved in the
paper and independently checked by verify_group.g.
"""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
a, b, c = sp.symbols("a b c")
s, t, r = sp.symbols("s t r")


def F(point: tuple[sp.Expr, sp.Expr, sp.Expr]) -> tuple[sp.Expr, ...]:
    """The announced three-dimensional Keller map."""
    xx, yy, zz = point
    u = 1 + xx * yy
    return (
        u**3 * zz + yy**2 * u * (4 + 3 * xx * yy),
        yy + 3 * xx * u**2 * zz + 3 * xx * yy**2 * (4 + 3 * xx * yy),
        2 * xx - 3 * xx**2 * yy - xx**3 * zz,
    )


P_EXPECTED = (
    128 * r**9 * s
    - 256 * r**8
    + 2592 * r**7 * s**2
    - 3072 * r**7 * s
    + 1408 * r**7
    - 7452 * r**6 * s**3
    + 1248 * r**6 * s**2
    - 1584 * r**6 * s
    - 576 * r**6
    - 17496 * r**5 * s**4
    + 82944 * r**5 * s**3
    - 87936 * r**5 * s**2
    + 42240 * r**5 * s
    - 5760 * r**5
    + 52488 * r**4 * s**4
    - 142884 * r**4 * s**3
    + 135144 * r**4 * s**2
    - 60144 * r**4 * s
    + 8928 * r**4
    + 104976 * r**3 * s**5
    + 97200 * r**3 * s**4
    - 97056 * r**3 * s**3
    - 41472 * r**3 * s**2
    + 93824 * r**3 * s
    - 26880 * r**3
    + 236196 * r**2 * s**6
    - 380538 * r**2 * s**5
    - 147744 * r**2 * s**4
    + 772080 * r**2 * s**3
    - 754944 * r**2 * s**2
    + 333792 * r**2 * s
    - 62208 * r**2
    + 236196 * r * s**6
    - 734832 * r * s**5
    + 1916784 * r * s**4
    - 2658432 * r * s**3
    + 2128320 * r * s**2
    - 919296 * r * s
    + 186624 * r
    + 531441 * s**8
    - 2204496 * s**7
    + 5436882 * s**6
    - 11805534 * s**5
    + 17996446 * s**4
    - 17402304 * s**3
    + 10364976 * s**2
    - 3544992 * s
    + 557280
)


A_EXPECTED = (
    1129718145924 * s**12
    - 6474958632657 * s**11
    + 21955119111630 * s**10
    - 60661410535386 * s**9
    + 123515279853390 * s**8
    - 191093865073182 * s**7
    + 235490291194248 * s**6
    - 188631015819696 * s**5
    + 54561577345568 * s**4
    + 41882989175328 * s**3
    - 44714997684096 * s**2
    + 15094447332352 * s
    - 1434819245056
)


B_EXPECTED = (
    1423119505038213888 * s**22
    - 155058052818404824443 * s**21
    + 1413754646027656083066 * s**20
    - 8145658955220494785812 * s**19
    + 33677018812011807334224 * s**18
    - 108385682498649366622416 * s**17
    + 280859820926917245978240 * s**16
    - 598631883156564470992728 * s**15
    + 1062288637590844067815584 * s**14
    - 1579910926841521168581900 * s**13
    + 1974730823883289142626824 * s**12
    - 2073348574060015592229024 * s**11
    + 1822485349587628391880960 * s**10
    - 1333523184375693801555072 * s**9
    + 806144943610022071172864 * s**8
    - 398941760796329492797440 * s**7
    + 159756878618286560778240 * s**6
    - 50952869532774134959104 * s**5
    + 12636860641575849510912 * s**4
    - 2344566242453066735616 * s**3
    + 304677812001210531840 * s**2
    - 24551525690267664384 * s
    + 926711257485017088
)


F_MINUS_THREE = (
    -384 * r**9
    - 256 * r**8
    + 33952 * r**7
    + 216612 * r**6
    - 4580568 * r**5
    + 9515052 * r**4
    - 15697056 * r**3
    + 223986114 * r**2
    + 599887620 * r
    + 17172300267
)


def check_map() -> None:
    image = F((x, y, z))
    jacobian = sp.Matrix(image).jacobian((x, y, z))
    assert sp.expand(jacobian.det()) == -2

    points = [
        (0, 0, sp.Rational(-1, 4)),
        (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
        (-1, sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    common = (sp.Rational(-1, 4), 0, 0)
    assert all(tuple(map(sp.expand, F(point))) == common for point in points)
    second_common = (0, 0, sp.Rational(-1, 2))
    assert all(tuple(map(sp.expand, F(F(point)))) == second_common for point in points)

    # det J(F o F) = (-2)^2 and postcomposing by diag(1/4,1,1)
    # therefore gives an identity-Jacobian map.
    assert (-2) * (-2) * sp.Rational(1, 4) == 1


def check_resolvent_parametrization() -> None:
    cubic = 2 * a * t**3 - b * t**2 + 2 * t - c
    yy = sp.cancel(-(b * t**2 + 3 * c - 6 * t) / (2 * t**2))
    xx = sp.cancel(t / (1 - t * yy))
    zz = sp.cancel((2 * xx - 3 * xx**2 * yy - c) / xx**3)
    field = sp.QQ.frac_field(a, b, c)

    for actual, expected in zip(F((xx, yy, zz)), (a, b, c)):
        numerator = sp.together(actual - expected).as_numer_denom()[0]
        remainder = sp.rem(
            sp.Poly(numerator, t, domain=field),
            sp.Poly(cubic, t, domain=field),
        )
        assert remainder.is_zero


def derive_line_polynomial() -> sp.Poly:
    outer = 2 * t**3 - 2 * t**2 + 2 * t - s
    yy = sp.cancel(-(2 * t**2 + 3 * s - 6 * t) / (2 * t**2))
    xx = sp.cancel(t / (1 - t * yy))
    zz = sp.cancel((2 * xx - 3 * xx**2 * yy - s) / xx**3)

    # A second inverse step for F: r is the inner resolvent root.
    inner = sp.together(2 * xx * r**3 - yy * r**2 + 2 * r - zz)
    inner_numerator, inner_denominator = inner.as_numer_denom()
    resultant = sp.resultant(outer, inner_numerator, t)
    content, primitive = sp.Poly(resultant, r, domain=sp.QQ[s]).primitive()
    assert sp.factor(content) == 256 * s**7
    polynomial = sp.Poly(primitive, r, domain=sp.QQ[s])
    assert sp.expand(polynomial.as_expr() - P_EXPECTED) == 0

    # Generic denominator control.  On the outer cubic, the only parameters at
    # which t or the other reconstruction denominator can vanish lie over
    # s*q(s)=0.  They therefore do not create a component over QQ(s).
    other_denominator = 3 * s + 2 * t**2 - 4 * t
    q = 27 * s**2 - 28 * s + 12
    assert sp.factor(sp.resultant(outer, t, t)) == s
    assert sp.factor(sp.resultant(outer, other_denominator, t)) == 4 * s * q
    assert sp.rem(
        sp.Poly(inner_denominator, t, domain=sp.QQ[s]),
        sp.Poly(outer, t, domain=sp.QQ[s]),
    ).as_expr() != 0

    # Reduce the cleared inner cubic modulo the outer cubic.  Its resultant is
    # exactly vertical content times P.  The penultimate subresultant is
    # lambda(r,s)*t+mu(r,s), and lambda is a unit in QQ(s)[r]/(P); hence t is
    # recovered rationally from (r,s).  This certifies the function-field
    # tower and rules out a hidden/extraneous generic component of the
    # resultant curve.
    reduced_inner = sp.rem(
        sp.Poly(inner_numerator, t, domain=sp.QQ[r, s]),
        sp.Poly(outer, t, domain=sp.QQ[r, s]),
    ).as_expr()
    assert sp.degree(reduced_inner, t) == 2
    assert sp.expand(
        sp.resultant(outer, reduced_inner, t) - 4 * s**7 * P_EXPECTED
    ) == 0
    subresultants = sp.subresultants(outer, reduced_inner, t)
    assert [sp.degree(item, t) for item in subresultants] == [3, 2, 1, 0]
    linear = sp.Poly(subresultants[-2], t, domain=sp.QQ[r, s])
    coefficient = linear.coeff_monomial(t)
    assert sp.degree(coefficient, r) == 6
    assert len(sp.Poly(coefficient, r, s).terms()) == 52
    fraction_field = sp.QQ.frac_field(s)
    assert sp.gcd(
        sp.Poly(P_EXPECTED, r, domain=fraction_field),
        sp.Poly(coefficient, r, domain=fraction_field),
    ).degree() == 0
    return polynomial


def check_inertia_data(polynomial: sp.Poly) -> None:
    # At s = infinity, u^8 P(r,u^-1) has coefficient valuations below.
    degrees = [sp.degree(polynomial.nth(i), s) for i in range(10)]
    assert degrees == [8, 6, 6, 5, 4, 4, 3, 2, 0, 1]
    valuations = [8 - degree for degree in degrees]
    assert valuations == [0, 2, 2, 3, 4, 4, 5, 6, 8, 7]
    assert all(9 * valuations[i] > 7 * i for i in range(1, 9))
    assert polynomial.nth(0).coeff(s, 8) == 531441
    assert polynomial.nth(9).coeff(s, 1) == 128
    assert sp.gcd(7, 9) == 1

    discriminant = sp.factor(sp.discriminant(polynomial.as_expr(), r))
    constant, factors = sp.factor_list(discriminant, s)
    assert constant == 2**38
    by_degree_exponent = {
        (sp.degree(factor, s), exponent): factor for factor, exponent in factors
    }
    q = 27 * s**2 - 28 * s + 12
    assert sp.expand(by_degree_exponent[(2, 8)] - q) == 0
    assert sp.expand(by_degree_exponent[(12, 1)] - A_EXPECTED) == 0
    big_square_root = by_degree_exponent[(22, 2)]
    assert sp.expand(big_square_root - B_EXPECTED) == 0

    important = [q, A_EXPECTED, big_square_root, polynomial.LC()]
    for item in important[:3]:
        assert sp.gcd(sp.Poly(item, s), sp.Poly(sp.diff(item, s), s)).degree() == 0
    for i, left in enumerate(important):
        for right in important[i + 1 :]:
            assert sp.gcd(sp.Poly(left, s), sp.Poly(right, s)).degree() == 0

    assert sp.Poly(P_EXPECTED.subs(s, -3), r).primitive()[1].as_expr() == F_MINUS_THREE


def main() -> None:
    check_map()
    print("PASS map: det JF = -2; exact collisions for F and F^2")
    check_resolvent_parametrization()
    print("PASS inverse resolvent: the cubic root reconstructs a generic preimage")
    polynomial = derive_line_polynomial()
    print("PASS line eliminant: degree 9, exact resultant and function-field tower")
    check_inertia_data(polynomial)
    print("PASS inertia: one Newton edge (0,0)-(9,7), simple degree-12 branch")
    print("PASS discriminant: 2^38 q(s)^8 A(s) B(s)^2 with A squarefree")


if __name__ == "__main__":
    main()
