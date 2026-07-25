#!/usr/bin/env python3
"""Exact exploration of the rank-one e=2 triple-companion lower identities."""

from __future__ import annotations

import sys
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions are required")

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import explore_rankone_triple as base


x, y, z, scale = base.x, base.y, base.z, base.scale
variables = base.variables
P, Q, R = base.P, base.Q, base.R
mon2 = base.mon2


def exact_zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def compose(
    substitutions: dict[sp.Symbol, sp.Expr],
    later: dict[sp.Symbol, sp.Expr],
) -> dict[sp.Symbol, sp.Expr]:
    """Compose simultaneous-style substitutions: first substitutions, then later."""
    result = {
        variable: sp.cancel(sp.sympify(value).subs(later, simultaneous=True))
        for variable, value in substitutions.items()
    }
    result.update(later)
    return result


def coeffs(value: sp.Expr, degree: int) -> list[sp.Expr]:
    return base.homogeneous_coefficients(value, degree)


def identity_data(
    weighted: sp.Poly,
    unknowns: tuple[sp.Symbol, ...],
    degree: int,
    substitutions: dict[sp.Symbol, sp.Expr],
):
    identity = sp.expand(
        weighted.coeff_monomial(scale**degree).subs(substitutions)
    )
    remaining = tuple(
        variable for variable in unknowns if variable in identity.free_symbols
    )
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(identity, degree), remaining)
    pairs = base.nonzero_pairs(matrix, rhs)
    return identity, remaining, matrix, rhs, pairs


def solve_linear_identity(
    weighted: sp.Poly,
    unknowns: tuple[sp.Symbol, ...],
    degree: int,
    substitutions: dict[sp.Symbol, sp.Expr],
):
    identity, remaining, matrix, rhs, pairs = identity_data(
        weighted, unknowns, degree, substitutions
    )
    print(
        f"E{degree}: remaining={remaining}, rank={matrix.rank()}, "
        f"compat={[value for _, value in pairs]}"
    )
    if pairs:
        return None
    solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
    update = dict(zip(remaining, solution))
    assert exact_zero(identity.subs(update))
    substitutions.update(update)
    print(
        " changed=",
        [
            (variable, sp.factor(value))
            for variable, value in update.items()
            if not exact_zero(variable - value)
        ],
    )
    return matrix, rhs, update


def show_identity(
    weighted: sp.Poly,
    degree: int,
    substitutions: dict[sp.Symbol, sp.Expr],
):
    identity = sp.expand(
        weighted.coeff_monomial(scale**degree).subs(substitutions)
    )
    print(f"E{degree} coefficients:")
    for exponent, value in zip(base.homogeneous_exponents(degree), coeffs(identity, degree)):
        if not exact_zero(value):
            print(" ", exponent, sp.factor(value))
    return identity


def branch_data(label: str, U: sp.Expr, V: sp.Expr, W: sp.Expr):
    weighted, a, b, ell, L = base.weighted_data(U, V, W, label)
    return weighted, a + b + ell, a, b, ell, L


def a0_w3_open_reduced():
    """A=0, s=w3!=0 after E5 has killed C2,...,C7."""
    s, C0, C1 = sp.symbols("s C0 C1", nonzero=True)
    U = sp.Rational(4, 3) * s * x * (y**2 + x * z)
    V = C0 * x**2 * z + C1 * x * y**2
    W = s * (y**2 + x * z)
    weighted, unknowns, a, b, ell, L = branch_data("s", U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    solve_linear_identity(weighted, unknowns, 5, substitutions)
    print("L=", L.subs(substitutions))
    print("detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 4, substitutions)


def a0_w3_open_general():
    """A=0, s=w3!=0 before the E5 compatibility reduction."""
    s = sp.symbols("s", nonzero=True)
    C = sp.symbols("C0:8")
    U = sp.Rational(4, 3) * s * x * (y**2 + x * z)
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    W = s * (y**2 + x * z)
    weighted, unknowns, _, _, _, _ = branch_data("g", U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    _, remaining, matrix, rhs, pairs = identity_data(
        weighted, unknowns, 5, substitutions
    )
    print("E5 remaining/rank=", remaining, matrix.rank())
    print("E5 compatibility:")
    for vector, value in pairs:
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        polynomial_vector = vector.applyfunc(
            lambda entry: sp.cancel(denominator * entry)
        )
        polynomial_value = sp.factor((polynomial_vector.T * rhs)[0])
        print(" ", polynomial_value, "cleared by", denominator)


def a0_w3_open_d_nonzero():
    """Polynomial parametrization of the C0-C1 != 0 chart through E4."""
    s, D = sp.symbols("s D", nonzero=True)
    C1, r = sp.symbols("C1 r")
    U = sp.Rational(4, 3) * s * x * (y**2 + x * z)
    V = (C1 + D) * x**2 * z + C1 * x * y**2
    W = s * (y**2 + x * z)
    weighted, unknowns, a, b, ell, L = branch_data("d", U, V, W)
    substitutions = {
        a[1]: 0,
        a[2]: r + sp.Rational(4, 3) * s * D,
        a[3]: r,
        a[4]: 0,
        a[5]: 0,
        b[1]: 0,
        b[3]: b[2] - C1 * D,
        b[4]: 0,
        b[5]: 0,
        ell[1]: 0,
        ell[2]: D * r,
        ell[7]: 0,
        ell[8]: s * D,
    }
    for degree in (6, 5, 4):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    print("D-open through E4; detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 3, substitutions)
    for degree in (3, 2, 1):
        result = solve_linear_identity(
            weighted, unknowns, degree, substitutions
        )
        if result is None:
            return
        print(" detL=", sp.factor(L.det().subs(substitutions)))
    print("E0=", sp.factor(weighted.coeff_monomial(scale**0).subs(substitutions)))


def a0_w3_open_d_zero():
    """The C0=C1 rank-drop chart, recomputed without localization."""
    s, C = sp.symbols("s C", nonzero=True)
    U = sp.Rational(4, 3) * s * x * (y**2 + x * z)
    V = C * x * (y**2 + x * z)
    W = s * (y**2 + x * z)
    weighted, unknowns, a, b, ell, L = branch_data("e", U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    for degree in (6, 5, 4, 3, 2, 1):
        result = solve_linear_identity(
            weighted, unknowns, degree, substitutions
        )
        if result is None:
            return
        print(" detL=", sp.factor(L.det().subs(substitutions)))
    print("E0=", sp.factor(weighted.coeff_monomial(scale**0).subs(substitutions)))


def a_w3_zero_origin():
    """A=w3=0 with arbitrary w1,w2 and the full V tail."""
    w1, w2 = sp.symbols("w1 w2")
    C = sp.symbols("C0:8")
    W = w1 * x * y + w2 * x * z
    U = sp.Rational(4, 3) * x * W
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    weighted, unknowns, a, b, ell, L = branch_data("o", U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    identity, remaining, matrix, rhs, pairs = identity_data(
        weighted, unknowns, 5, substitutions
    )
    print(
        "E5:",
        "remaining=", remaining,
        "rank=", matrix.rank(),
        "compat=", [sp.factor(value) for _, value in pairs],
    )
    for exponent, value in zip(base.homogeneous_exponents(5), coeffs(identity, 5)):
        if not exact_zero(value):
            print(" ", exponent, sp.factor(value))


def a_w3_zero_axis(which: str):
    """The two nonzero residual-symmetry representatives W=s*x*y or s*x*z."""
    s = sp.symbols("s", nonzero=True)
    C = sp.symbols("C0:8")
    if which == "xy":
        W = s * x * y
    elif which == "xz":
        W = s * x * z
    else:
        raise ValueError(which)
    U = sp.Rational(4, 3) * x * W
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    weighted, unknowns, _, _, _, L = branch_data(which, U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    _, remaining, matrix, rhs, pairs = identity_data(
        weighted, unknowns, 5, substitutions
    )
    print("E5 remaining/rank=", remaining, matrix.rank())
    print("E5 compatibility:")
    for vector, value in pairs:
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        polynomial_vector = vector.applyfunc(
            lambda entry: sp.cancel(denominator * entry)
        )
        print(
            " ",
            sp.factor((polynomial_vector.T * rhs)[0]),
            "cleared by",
            denominator,
        )
    print("E5 literal coefficients:")
    identity = sp.expand(weighted.coeff_monomial(scale**5).subs(substitutions))
    for exponent, value in zip(base.homogeneous_exponents(5), coeffs(identity, 5)):
        if not exact_zero(value):
            print(" ", exponent, sp.factor(value))
    print("detL before E5=", sp.factor(L.det().subs(substitutions)))


def axis_xy_reduced():
    """The s*x*y chart after all E5 equations, with h=2s-3C4 != 0."""
    s, h = sp.symbols("s h", nonzero=True)
    C0, C1, C2 = sp.symbols("C0 C1 C2")
    C4 = (2 * s - h) / 3
    W = s * x * y
    U = sp.Rational(4, 3) * s * x**2 * y
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C4 * y**3
    )
    weighted, unknowns, a, b, ell, L = branch_data("r", U, V, W)
    k = 4 * s**3 / (3 * h)
    substitutions = {
        a[1]: sp.Rational(4, 3) * ell[7],
        a[3]: 2 * s**2 * (3 * h - 2 * s) / (27 * h),
        a[2]: -k / 9 + sp.Rational(4, 3) * ell[8],
        a[4]: 0,
        a[5]: 0,
        ell[1]: 2 * s * (3 * a[0] - 2 * ell[6]) / 9,
        ell[2]: -4 * s * (3 * h * ell[7] + (C0 - C1) * s**2)
        / (27 * h),
        ell[8]: -(2 * s - 3 * C2) * s**2 / (9 * h),
    }
    for degree in (6, 5):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    print("axis xy through E5; detL=", sp.factor(L.det().subs(substitutions)))
    identity = show_identity(weighted, 4, substitutions)
    selected = (ell[0], b[3], b[4], b[5])
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(identity, 4), selected)
    print("E4 selected rank=", matrix.rank())
    print("E4 compatibility:")
    for vector, value in base.nonzero_pairs(matrix, rhs):
        print(" ", sp.factor(value))
    pivot_rows = matrix.T.rref()[1]
    solution = next(
        iter(
            sp.linsolve(
                (
                    matrix.extract(pivot_rows, range(len(selected))),
                    rhs.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    print("E4 pivot rows=", pivot_rows)
    print(
        "E4 selected solve=",
        [(variable, sp.factor(value)) for variable, value in zip(selected, solution)],
    )


def axis_xy_after_e4_state():
    s, h = sp.symbols("s h", nonzero=True)
    C0, C1, C2 = sp.symbols("C0 C1 C2")
    C4 = (2 * s - h) / 3
    W = s * x * y
    U = sp.Rational(4, 3) * s * x**2 * y
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C4 * y**3
    )
    weighted, unknowns, a, b, ell, L = branch_data("u", U, V, W)
    k = 4 * s**3 / (3 * h)
    substitutions = {
        a[1]: sp.Rational(4, 3) * ell[7],
        a[3]: 2 * s**2 * (3 * h - 2 * s) / (27 * h),
        a[2]: -k / 9 + sp.Rational(4, 3) * ell[8],
        a[4]: 0,
        a[5]: 0,
        ell[1]: 2 * s * (3 * a[0] - 2 * ell[6]) / 9,
        ell[2]: -4 * s * (3 * h * ell[7] + (C0 - C1) * s**2)
        / (27 * h),
        ell[8]: -(2 * s - 3 * C2) * s**2 / (9 * h),
    }
    E4 = sp.expand(weighted.coeff_monomial(scale**4).subs(substitutions))
    selected = (ell[0], b[3], b[4], b[5])
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(E4, 4), selected)
    pivot_rows = matrix.T.rref()[1]
    solution = next(
        iter(
            sp.linsolve(
                (
                    matrix.extract(pivot_rows, range(len(selected))),
                    rhs.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    substitutions.update(dict(zip(selected, solution)))
    return (
        s,
        h,
        C0,
        C1,
        C2,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
        substitutions,
    )


def axis_xy_e4_factor_one():
    """E4 branch 3h+2s=0; the other E4 factor is unrestricted."""
    (
        s,
        h,
        C0,
        C1,
        C2,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
        substitutions,
    ) = axis_xy_after_e4_state()
    substitutions = compose(
        substitutions, {h: -2 * s / 3, ell[7]: -C1 * s / 2}
    )
    for degree in (6, 5, 4):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    print("xy factor-one detL=", sp.factor(L.det().subs(substitutions)))
    identity = show_identity(weighted, 3, substitutions)
    substitutions = compose(substitutions, {C2: s})
    identity = sp.expand(weighted.coeff_monomial(scale**3).subs(substitutions))
    selected = (b[0], b[2], ell[4], ell[5])
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(identity, 3), selected)
    print("after square C2=s, rank=", matrix.rank())
    print(
        "compat=",
        [sp.factor(value) for _, value in base.nonzero_pairs(matrix, rhs)],
    )
    pivot_rows = matrix.T.rref()[1]
    solution = next(
        iter(
            sp.linsolve(
                (
                    matrix.extract(pivot_rows, range(len(selected))),
                    rhs.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    print(
        "solve=",
        [(variable, sp.factor(value)) for variable, value in zip(selected, solution)],
    )


def axis_xy_e4_factor_one_lower(which: str):
    (
        s,
        h,
        C0,
        C1,
        C2,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
        substitutions,
    ) = axis_xy_after_e4_state()
    substitutions = compose(
        substitutions,
        {h: -2 * s / 3, ell[7]: -C1 * s / 2, C2: s},
    )
    E3 = sp.expand(weighted.coeff_monomial(scale**3).subs(substitutions))
    selected = (b[0], b[2], ell[4], ell[5])
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(E3, 3), selected)
    pivot_rows = matrix.T.rref()[1]
    solution = next(
        iter(
            sp.linsolve(
                (
                    matrix.extract(pivot_rows, range(len(selected))),
                    rhs.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    substitutions = compose(substitutions, dict(zip(selected, solution)))
    if which == "c1zero":
        substitutions = compose(substitutions, {C1: 0})
    elif which == "ratio":
        substitutions = compose(substitutions, {C0: 3 * C1 / 2})
    else:
        raise ValueError(which)
    for degree in (6, 5, 4, 3):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    print(which, "detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 2, substitutions)


def axis_xy_e4_factor_one_final(which: str):
    (
        s,
        h,
        C0,
        C1,
        C2,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
        substitutions,
    ) = axis_xy_after_e4_state()
    substitutions = compose(
        substitutions,
        {h: -2 * s / 3, ell[7]: -C1 * s / 2, C2: s},
    )
    E3 = sp.expand(weighted.coeff_monomial(scale**3).subs(substitutions))
    selected = (b[0], b[2], ell[4], ell[5])
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(E3, 3), selected)
    pivot_rows = matrix.T.rref()[1]
    solution = next(
        iter(
            sp.linsolve(
                (
                    matrix.extract(pivot_rows, range(len(selected))),
                    rhs.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    substitutions = compose(substitutions, dict(zip(selected, solution)))
    if which == "zero":
        substitutions = compose(
            substitutions,
            {
                C0: 0,
                C1: 0,
                ell[6]: 0,
                ell[3]: 3 * a[0] * b[1] / (2 * s),
            },
        )
    elif which == "ratio":
        substitutions = compose(
            substitutions,
            {
                C0: 3 * C1 / 2,
                ell[6]: -3 * C1**2 / 4,
                b[1]: 0,
            },
        )
        E2 = sp.expand(weighted.coeff_monomial(scale**2).subs(substitutions))
        equation = coeffs(E2, 2)[0]
        solution_l3 = sp.solve(equation, ell[3], dict=False)[0]
        substitutions = compose(substitutions, {ell[3]: solution_l3})
    else:
        raise ValueError(which)
    for degree in (6, 5, 4, 3, 2):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    print(which, "detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 1, substitutions)


def axis_xy_e4_factor_two(generic_g: bool):
    """E4 branch C2=(4s-3h)/6, split by G=3h^2+2s^2."""
    (
        s,
        h,
        C0,
        C1,
        C2,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
        substitutions,
    ) = axis_xy_after_e4_state()
    G = 3 * h**2 + 2 * s**2
    later = {C2: (4 * s - 3 * h) / 6}
    if generic_g:
        g = sp.symbols("g", nonzero=True)
        # Use g=G as a denominator marker; the equality is checked separately.
        later[ell[7]] = -C1 * s**2 * (s - h) / G
        label = "G-open"
    else:
        # On G=0, s-h is nonzero, so compatibility forces C1=0.
        later[C1] = 0
        label = "G-zero"
    substitutions = compose(substitutions, later)
    for degree in (6, 5):
        assert exact_zero(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
    E4 = sp.factor(weighted.coeff_monomial(scale**4).subs(substitutions))
    if generic_g:
        assert exact_zero(E4)
    else:
        # Reduce coefficients modulo the single relation G=0.
        for value in coeffs(E4, 4):
            remainder = sp.rem(
                sp.Poly(sp.together(value).as_numer_denom()[0], h),
                sp.Poly(G, h),
            ).as_expr()
            assert exact_zero(remainder)
    print(label, "detL=", sp.factor(L.det().subs(substitutions)))
    E3 = sp.expand(weighted.coeff_monomial(scale**3).subs(substitutions))
    print(label, "E3 coefficients:")
    for exponent, value in zip(base.homogeneous_exponents(3), coeffs(E3, 3)):
        if not exact_zero(value):
            if generic_g:
                print(" ", exponent, sp.factor(value))
            else:
                numerator = sp.together(value).as_numer_denom()[0]
                remainder = sp.rem(
                    sp.Poly(numerator, h), sp.Poly(G, h)
                ).as_expr()
                print(" ", exponent, sp.factor(remainder))


def axis_xz_reduced():
    """The s*x*z chart after C4=0, before solving E5."""
    s = sp.symbols("s", nonzero=True)
    C0, C1, C2, C3, C5, C6, C7 = sp.symbols(
        "C0 C1 C2 C3 C5 C6 C7"
    )
    W = s * x * z
    U = sp.Rational(4, 3) * s * x**2 * z
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + C5 * y**2 * z
        + C6 * y * z**2
        + C7 * z**3
    )
    weighted, unknowns, _, _, _, L = branch_data("z", U, V, W)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    solve_linear_identity(weighted, unknowns, 5, substitutions)
    print("axis xz through E5; detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 4, substitutions)


def a_open_state(prefix: str = "a"):
    A = sp.symbols("A", nonzero=True)
    w1, w2, w3 = sp.symbols("w1 w2 w3")
    C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3")
    W = w1 * x * y + w2 * x * z + w3 * y**2
    U = A * x * (y**2 + x * z) + sp.Rational(4, 3) * x * W
    C4 = w1 * (3 * A - 4 * w3) / (9 * A)
    C5 = (w2 - w3) * (3 * A - 4 * w3) / (9 * A)
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + C4 * y**3
        + C5 * y**2 * z
    )
    weighted, unknowns, a, b, ell, L = branch_data(prefix, U, V, W)
    return (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    )


def a_open_general():
    (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    ) = a_open_state()
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    _, remaining, matrix, rhs, pairs = identity_data(
        weighted, unknowns, 5, substitutions
    )
    print("A-open E5 remaining/rank=", remaining, matrix.rank())
    print("compatibility:")
    for vector, value in pairs:
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        polynomial_vector = vector.applyfunc(
            lambda entry: sp.cancel(denominator * entry)
        )
        print(
            " ",
            sp.factor((polynomial_vector.T * rhs)[0]),
            "cleared by",
            denominator,
        )


def a_open_factor(which: str):
    state = a_open_state(which)
    (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    ) = state
    if which == "w3zero":
        top = {w3: 0}
    elif which == "plus":
        top = {w3: 3 * A / 4}
    elif which == "minus":
        top = {w3: -3 * A / 4}
    elif which == "equal":
        top = {w2: w3}
    else:
        raise ValueError(which)
    substitutions = compose({}, top)
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    result = solve_linear_identity(weighted, unknowns, 5, substitutions)
    print(which, "detL through E5=", sp.factor(L.det().subs(substitutions)))
    if result is not None:
        show_identity(weighted, 4, substitutions)


def a_top_compat(which: str):
    (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    ) = a_open_state("t")
    _, remaining6, matrix6, rhs6, pairs6 = identity_data(
        weighted, unknowns, 6, {}
    )
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), remaining6)))
    substitutions6 = dict(zip(remaining6, solution6))
    _, _, matrix5, rhs5, pairs5 = identity_data(
        weighted, unknowns, 5, substitutions6
    )
    if which == "w3zero":
        top = {w3: 0}
    elif which == "plus":
        top = {w3: 3 * A / 4}
    elif which == "minus":
        top = {w3: -3 * A / 4}
    elif which == "equal":
        top = {w2: w3}
    else:
        raise ValueError(which)
    equations = []
    print(which, "top E5 compatibility:")
    for _, value in pairs5:
        numerator = sp.factor(sp.together(value.subs(top)).as_numer_denom()[0])
        if not exact_zero(numerator):
            equations.append(numerator)
            print(" ", numerator)
    print("groebner C3,C2,w2,w1:")
    basis = sp.groebner(equations, C3, C2, w2, w1, order="lex")
    for polynomial in basis.polys:
        print(" ", sp.factor(polynomial.as_expr()))


def a_compatible_branch(which: str):
    (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    ) = a_open_state("v")
    if which == "z_w1":
        top = {w3: 0, w2: 0, w1: 0}
    elif which == "z_c3":
        top = {w3: 0, w2: 0, C3: 0}
    elif which == "p_w1":
        top = {w3: 3 * A / 4, w2: 3 * A / 4, w1: 0}
    elif which == "p_c3":
        top = {w3: 3 * A / 4, w2: 3 * A / 4, C3: 0}
    elif which == "minus_exact":
        top = {
            w3: -3 * A / 4,
            w2: -3 * A / 4,
            C3: 0,
            C2: 2 * w1 / 3,
        }
    elif which == "equal_generic":
        top = {w2: w3, w1: 0, C2: 0, C3: 0}
    else:
        raise ValueError(which)
    substitutions = compose({}, top)
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    result = solve_linear_identity(weighted, unknowns, 5, substitutions)
    print(which, "detL=", sp.factor(L.det().subs(substitutions)))
    if result is not None:
        show_identity(weighted, 4, substitutions)


def a_special_branch(which: str):
    (
        A,
        w1,
        w2,
        w3,
        C0,
        C1,
        C2,
        C3,
        weighted,
        unknowns,
        a,
        b,
        ell,
        L,
    ) = a_open_state("k")
    if which == "z_origin":
        top = {w3: 0, w2: 0, w1: 0, C3: 0}
    elif which == "plus_origin":
        top = {
            w3: 3 * A / 4,
            w2: 3 * A / 4,
            w1: 0,
            C3: 0,
        }
    elif which == "plus_nonzero":
        top = {
            w3: 3 * A / 4,
            w2: 3 * A / 4,
            C3: 0,
            C2: -w1 / 3,
        }
    elif which == "minus_wzero":
        top = {
            w3: -3 * A / 4,
            w2: -3 * A / 4,
            w1: 0,
            C2: 0,
            C3: 0,
        }
    elif which == "minus_dzero":
        top = {
            w3: -3 * A / 4,
            w2: -3 * A / 4,
            C2: 2 * w1 / 3,
            C3: 0,
            C0: C1,
        }
    elif which == "equal_dzero":
        top = {
            w2: w3,
            w1: 0,
            C2: 0,
            C3: 0,
            C0: C1,
        }
    else:
        raise ValueError(which)
    substitutions = compose({}, top)
    solve_linear_identity(weighted, unknowns, 6, substitutions)
    result = solve_linear_identity(weighted, unknowns, 5, substitutions)
    print(which, "detL=", sp.factor(L.det().subs(substitutions)))
    if result is not None:
        show_identity(weighted, 4, substitutions)


def plus_aligned_d_open():
    """The final plus resonance: C0-C1=D != 0 and C2=C3=w1=0."""
    A, D = sp.symbols("A D", nonzero=True)
    C1, r = sp.symbols("C1 r")
    U = 2 * A * x * (y**2 + x * z)
    V = (C1 + D) * x**2 * z + C1 * x * y**2
    W = sp.Rational(3, 4) * A * (y**2 + x * z)
    weighted, unknowns, a, b, ell, L = branch_data("p", U, V, W)
    substitutions = {
        a[1]: 0,
        a[2]: r + 2 * A * D,
        a[3]: r,
        a[4]: 0,
        a[5]: 0,
        b[1]: ell[1] / A,
        b[3]: b[2] + D * (r - A * C1) / A - ell[2] / A,
        b[4]: 0,
        b[5]: 0,
        ell[7]: 0,
        ell[8]: sp.Rational(3, 4) * A * D,
        ell[4]: -(r - A * C1) * ell[1] / A**2,
        ell[5]: -(r - A * C1) * ell[2] / A**2,
    }
    for degree in (6, 5, 4):
        residual = sp.factor(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
        print("plus aligned residual", degree, residual)
        assert exact_zero(residual)
    print("plus aligned detL=", sp.factor(L.det().subs(substitutions)))
    show_identity(weighted, 3, substitutions)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: explore_branches.py {s|origin}")
    if sys.argv[1] == "s":
        a0_w3_open_reduced()
    elif sys.argv[1] == "s_general":
        a0_w3_open_general()
    elif sys.argv[1] == "s_d":
        a0_w3_open_d_nonzero()
    elif sys.argv[1] == "s_equal":
        a0_w3_open_d_zero()
    elif sys.argv[1] == "origin":
        a_w3_zero_origin()
    elif sys.argv[1] == "axis_xy":
        a_w3_zero_axis("xy")
    elif sys.argv[1] == "axis_xz":
        a_w3_zero_axis("xz")
    elif sys.argv[1] == "axis_xy_reduced":
        axis_xy_reduced()
    elif sys.argv[1] == "axis_xy_f1":
        axis_xy_e4_factor_one()
    elif sys.argv[1] == "axis_xy_f1_c1zero":
        axis_xy_e4_factor_one_lower("c1zero")
    elif sys.argv[1] == "axis_xy_f1_ratio":
        axis_xy_e4_factor_one_lower("ratio")
    elif sys.argv[1] == "axis_xy_f1_zero_final":
        axis_xy_e4_factor_one_final("zero")
    elif sys.argv[1] == "axis_xy_f1_ratio_final":
        axis_xy_e4_factor_one_final("ratio")
    elif sys.argv[1] == "axis_xy_f2":
        axis_xy_e4_factor_two(True)
    elif sys.argv[1] == "axis_xy_f2_g0":
        axis_xy_e4_factor_two(False)
    elif sys.argv[1] == "axis_xz_reduced":
        axis_xz_reduced()
    elif sys.argv[1] == "a_general":
        a_open_general()
    elif sys.argv[1] in {"w3zero", "plus", "minus", "equal"}:
        a_open_factor(sys.argv[1])
    elif sys.argv[1].startswith("top_"):
        a_top_compat(sys.argv[1][4:])
    elif sys.argv[1].startswith("compat_"):
        a_compatible_branch(sys.argv[1][7:])
    elif sys.argv[1].startswith("special_"):
        a_special_branch(sys.argv[1][8:])
    elif sys.argv[1] == "plus_aligned":
        plus_aligned_d_open()
    else:
        raise SystemExit(f"unknown branch {sys.argv[1]}")
