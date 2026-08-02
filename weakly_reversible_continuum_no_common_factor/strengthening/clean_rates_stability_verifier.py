#!/usr/bin/env python3
"""Exact verifier for a smaller rate vector and stability of the v1 ellipse.

This file is independent of the project-level verifier.  It reconstructs the
fixed-support rate family, certifies the cleaner integer point (including its
steady ideal), and derives the two transverse eigenvalue invariants for the
original rate vector.  All assertions use exact arithmetic.
"""

from functools import reduce

import sympy as sp

x, y, z, t, lam = sp.symbols("x y z t lam")
xyz = (x, y, z)

complexes = (
    (0, 0, 0), (0, 0, 1), (0, 0, 3), (0, 1, 1), (0, 3, 0),
    (1, 0, 1), (1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 0, 0),
)
pairs = ((0, 1), (0, 4), (0, 6), (1, 7), (2, 4),
         (2, 7), (2, 9), (3, 4), (5, 9), (8, 9))
directed = tuple(edge for i, j in pairs for edge in ((i, j), (j, i)))

original_rates = (
    845740, 7732494, 702464, 3920, 437290, 4380128, 1405575, 5600,
    706384, 900816, 1518755, 6873328, 3920, 896896, 3863552, 3920,
    3863552, 15680, 4346496, 658560,
)

# The free rates (k12,k15,k17,k19) are (653,1,70,915).
clean_rates = (
    1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
    1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915,
)

L = z - x - y + 1
Q = 7*x**2 - 2*x*y - 16*x + 7*y**2 - 16*y + 16
D = y**2 - y*z - y + sp.Rational(7, 16)*z**2 - z/8 + sp.Rational(7, 16)


def monomial(c):
    return sp.prod(v**a for v, a in zip(xyz, c))


def field(rates):
    result = [0, 0, 0]
    for rate, (i, j) in zip(rates, directed):
        delta = tuple(complexes[j][a] - complexes[i][a] for a in range(3))
        for a in range(3):
            result[a] += rate*monomial(complexes[i])*delta[a]
    return tuple(sp.expand(f) for f in result)


def constraint_matrix():
    """Return the exact linear conic-preservation matrix."""
    conic_basis = sp.groebner((L, Q), z, y, x, order="lex", domain=sp.QQ)
    column_remainders = []
    for j in range(20):
        unit = [0]*20
        unit[j] = 1
        column_remainders.append(
            tuple(sp.expand(conic_basis.reduce(f)[1]) for f in field(unit))
        )
    monomials = sorted(set().union(*(
        set(sp.Poly(column_remainders[j][a], x, y, z).monoms())
        for j in range(20) for a in range(3)
    )))
    rows = []
    for a in range(3):
        for mon in monomials:
            row = [
                sp.Poly(column_remainders[j][a], x, y, z).coeff_monomial(mon)
                for j in range(20)
            ]
            if any(row):
                rows.append(row)
    return sp.Matrix(rows)


def family_vector(a, b, c, d):
    """All conic-preserving rates in free coordinates k12,k15,k17,k19."""
    return (
        -5*c/16 + 31*d/24,
        -297*c/32 + 957*d/80,
        16*d/15,
        -b/3 + c/3,
        -221*c/224 + 11*d/16,
        -221*c/98 + 704*d/105,
        -9945*c/3136 + 495*d/224,
        5*c/14,
        a + 16*d/15,
        -b/3 - c/3 + 62*d/45,
        -3*a - 221*c/64 + 77*d/32,
        -33*c/4 + 319*d/30,
        a,
        -2*c/3 + 62*d/45,
        88*d/15,
        b,
        88*d/15,
        c,
        33*d/5,
        d,
    )


def rational_family_vector(a, b, c, d):
    return tuple(sp.sympify(value) for value in family_vector(
        sp.Rational(a), sp.Rational(b), sp.Rational(c), sp.Rational(d)
    ))


def verify_rate_family_and_clean_point():
    matrix = constraint_matrix()
    assert matrix.shape == (21, 20)
    assert matrix.rank() == 16
    assert len(matrix.nullspace()) == 4

    a, b, c, d = sp.symbols("a b c d")
    symbolic_family = sp.Matrix(family_vector(a, b, c, d))
    assert matrix*symbolic_family == sp.zeros(matrix.rows, 1)
    assert tuple(symbolic_family[i] for i in (12, 15, 17, 19)) == (a, b, c, d)
    # These four free entries show that the displayed four kernel vectors are
    # linearly independent; nullity four makes the parametrization exhaustive.

    assert rational_family_vector(653, 1, 70, 915) == clean_rates
    assert all(isinstance(rate, int) and rate > 0 for rate in clean_rates)
    assert reduce(sp.igcd, clean_rates) == 1
    assert max(clean_rates) == 10296
    assert sum(clean_rates) == 52464
    assert max(original_rates) == 7732494
    assert sum(original_rates) == 39165070

    clean_field = field(clean_rates)
    expected = (
        -4697*x**3 + 6039*x**2*y - 9177*x*y*z - 5977*x*y
        + 10736*x*z + 1960*z**3 + 1800*z + 560,
        915*x**3 - 6039*x**2*y - 9177*x*y*z - 5977*x*y
        - 3782*y**3 + 10736*y*z + 4888*z**3 + 1800*z + 3488,
        3712*x**3 + 18304*x*y*z - 5368*x*z + 3712*y**3
        - 5368*y*z - 6848*z**3 - 10296*z + 1160,
    )
    assert all(sp.expand(f-g) == 0 for f, g in zip(clean_field, expected))
    conic_basis = sp.groebner((L, Q), z, y, x, order="lex", domain=sp.QQ)
    assert all(sp.expand(conic_basis.reduce(f)[1]) == 0 for f in clean_field)

    primitive = [sp.Poly(f, xyz, domain=sp.QQ).primitive()[1] for f in clean_field]
    assert reduce(sp.gcd, primitive).total_degree() == 0
    point = {x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}
    assert sp.Matrix(clean_field).jacobian(xyz).subs(point).rank() == 2

    # Full radical decomposition: K=(L,D) intersection q, with q a degree-15
    # maximal ideal over Q whose scalar extension is 15 reduced points.
    steady_basis = sp.groebner(clean_field, x, y, z, order="lex", domain=sp.QQ)
    basis = tuple(g.as_expr() for g in steady_basis.polys)
    assert len(basis) == 3
    common = sp.gcd(sp.Poly(basis[1], xyz), sp.Poly(basis[2], xyz)).monic()
    assert sp.expand(common.as_expr() - D) == 0
    H = sp.Poly(basis[1], xyz).exquo(common).as_expr()
    R = sp.Poly(basis[2], xyz).exquo(common).as_expr()
    assert H.free_symbols <= {y, z} and sp.degree(H, y) == 1
    assert sp.Poly(H, y).LC().free_symbols == set()
    assert R.free_symbols <= {z} and sp.degree(R, z) == 15
    factors = sp.factor_list(R, z)[1]
    assert len(factors) == 1 and sp.degree(factors[0][0], z) == 15
    assert factors[0][1] == 1
    isolated_basis = sp.groebner((basis[0], H, R), x, y, z,
                                 order="lex", domain=sp.QQ)
    isolated = tuple(g.as_expr() for g in isolated_basis.polys)
    assert len(isolated) == 3
    assert isolated[0].free_symbols <= {x, z}
    assert sp.degree(isolated[0], x) == 1 and sp.Poly(isolated[0], x).LC() == 1
    assert isolated[1].free_symbols <= {y, z}
    assert sp.degree(isolated[1], y) == 1 and sp.Poly(isolated[1], y).LC() == 1
    assert isolated[2].free_symbols <= {z} and sp.degree(isolated[2], z) == 15
    # Thus q is isomorphic to Q[z]/(R), a field.  In characteristic zero its
    # scalar extension consists of 15 reduced points.
    assert all(sp.expand(isolated_basis.reduce(g)[1]) == 0 for g in basis)
    assert sp.expand(isolated_basis.reduce(D)[1]) != 0
    assert sp.rem(Q - 16*D, L, x) == 0
    conic_factors = sp.factor_list(D, y, z)[1]
    assert len(conic_factors) == 1 and conic_factors[0][1] == 1
    assert sp.Poly(conic_factors[0][0], y, z).total_degree() == 2
    assert all(
        sp.expand(steady_basis.reduce(p*q)[1]) == 0
        for p in (L, D) for q in isolated
    )


def integer_height_minima_up_to(maximum_d):
    """Return exact minimum max-rate and rate-sum up to a bound on d."""
    best_max = None
    best_sum = None
    # Integrality of k2=16d/15 and k7=5c/14 forces 15|d and 14|c.
    for d in range(15, maximum_d + 1, 15):
        for c in range(14, d + 1, 14):
            independent = rational_family_vector(0, 0, c, d)
            # Entries depending on a or b are checked below.
            fixed_indices = (0, 1, 2, 4, 5, 6, 7, 11, 13, 14, 16, 17, 18, 19)
            if not all(independent[i].is_Integer and independent[i] > 0
                       for i in fixed_indices):
                continue
            b_groups = []
            for b in range(1, c + 1):
                rates = rational_family_vector(0, b, c, d)
                if all(rates[i].is_Integer and rates[i] > 0 for i in (3, 9, 15)):
                    b_groups.append(tuple(int(rates[i]) for i in (3, 9, 15)))
            a_groups = []
            # Positivity of k10 gives a < (154d-221c)/192, so d is a safe
            # finite upper bound throughout the positive cone.
            for a in range(1, d + 1):
                rates = rational_family_vector(a, 0, c, d)
                if all(rates[i].is_Integer and rates[i] > 0 for i in (8, 10, 12)):
                    a_groups.append(tuple(int(rates[i]) for i in (8, 10, 12)))
            if not a_groups or not b_groups:
                continue
            fixed = tuple(int(independent[i]) for i in fixed_indices)
            local_max = max(
                max(fixed),
                min(max(group) for group in a_groups),
                min(max(group) for group in b_groups),
            )
            local_sum = (
                sum(fixed)
                + min(sum(group) for group in a_groups)
                + min(sum(group) for group in b_groups)
            )
            best_max = local_max if best_max is None else min(best_max, local_max)
            best_sum = local_sum if best_sum is None else min(best_sum, local_sum)
    return best_max, best_sum


def verify_integer_height_minimality():
    """Certify the clean ray has minimum max-rate and minimum rate-sum.

    This is only a statement inside the fixed support and among primitive
    positive integral rate vectors.  It is not network-support minimality.
    """
    # If max(k)<10296, then k14=88d/15 implies d<1755.
    best_max, _ = integer_height_minima_up_to(1754)
    assert best_max == 10296

    # If sum(k)<52464, then k14+k16+k18+k19=(58/3)d implies d<2714.
    _, best_sum = integer_height_minima_up_to(2713)
    assert best_sum == 52464


def verify_original_transverse_stability():
    original_field = field(original_rates)
    denominator = t**2 - t + 1
    parametrization = (
        (t**2 + 3)/(2*denominator),
        (3*t**2 + 1)/(2*denominator),
        (t**2 + t + 1)/denominator,
    )
    jacobian = sp.Matrix(original_field).jacobian(xyz).subs(dict(zip(xyz, parametrization)))
    characteristic = sp.Poly(jacobian.charpoly(lam).as_expr(), lam)

    trace_numerator = (
        5399367*t**4 + 1602005*t**3 + 11579010*t**2
        + 1602005*t + 6979911
    )
    trace = -8*trace_numerator/denominator**2
    product_numerator = (
        5730530769*t**8 + 20026244073*t**7 + 29613209084*t**6
        + 118245415239*t**5 - 38238695578*t**4 + 127692520263*t**3
        - 127590858244*t**2 + 10579139049*t - 79465564719
    )
    product = -6272*product_numerator/denominator**4
    discriminant_numerator = (
        31399532062137*t**8 + 25149913538286*t**7
        + 139213446954293*t**6 + 100751092465458*t**5
        + 199590946186248*t**4 + 109518436416306*t**3
        + 114191722124597*t**2 + 26510727150318*t + 17568656198073
    )
    discriminant = 64*discriminant_numerator/denominator**4

    asserted_characteristic = lam*(lam**2 - trace*lam + product)
    assert sp.cancel(characteristic.as_expr() - asserted_characteristic) == 0
    assert sp.cancel(trace**2 - 4*product - discriminant) == 0
    assert sp.Poly(trace_numerator, t).count_roots(-sp.oo, sp.oo) == 0
    assert trace_numerator.subs(t, 0) > 0
    assert sp.Poly(discriminant_numerator, t).count_roots(-sp.oo, sp.oo) == 0
    assert discriminant_numerator.subs(t, 0) > 0

    product_poly = sp.Poly(product_numerator, t)
    assert product_poly.count_roots(-sp.oo, sp.oo) == 2
    assert product_poly.count_roots(-4, -3) == 1
    assert product_poly.count_roots(sp.Rational(9, 10), 1) == 1
    assert product_poly.count_roots(-sp.oo, -4) == 0
    assert product_poly.count_roots(-3, sp.Rational(9, 10)) == 0
    assert product_poly.count_roots(1, sp.oo) == 0
    assert product_numerator.subs(t, -4) > 0
    assert product_numerator.subs(t, -3) < 0
    assert product_numerator.subs(t, sp.Rational(9, 10)) < 0
    assert product_numerator.subs(t, 1) > 0


def main():
    verify_rate_family_and_clean_point()
    verify_integer_height_minimality()
    verify_original_transverse_stability()
    print("PASS: exact clean-rate and transverse-stability checks succeeded")
    print("  fixed-support conic-preserving rate-space dimension: 4")
    print("  clean primitive integer rates: max=10296, sum=52464")
    print("  clean steady ideal: same conic plus 15 reduced isolated points")
    print("  original ellipse: two exact transverse stability-transition points")


if __name__ == "__main__":
    main()
