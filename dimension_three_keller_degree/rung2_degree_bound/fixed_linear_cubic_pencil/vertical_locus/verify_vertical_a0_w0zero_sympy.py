#!/usr/bin/env python3
"""Exact raw-determinant check of the a=0, W0=0 vertical exclusion."""

from __future__ import annotations

import os

import sympy as sp


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


mutation = os.environ.get("A0_W0_ZERO_MUTATION", "strict")


def expect(actual: sp.Expr, expected: sp.Expr, tag: str) -> None:
    if mutation == tag:
        expected += 1
    check(sp.expand(actual - expected) == 0, tag)


x, y, z = sp.symbols("x y z")
u, v, w, alpha = sp.symbols("u v w alpha")
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
t = sp.symbols("t0:9")
l = sp.symbols("l0:9")

quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
cubics = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratics))
V = sum(coefficient * monomial for coefficient, monomial in zip(t, cubics))
L = sp.Matrix(3, 3, l)
W = z * (u * x + v * y + w * z)

charts = {
    "squarefree": (
        x * y * (x - y)
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    ),
    "double": (
        x**2 * y
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    ),
    "triple_C": x**3 + y**2 * z + alpha * x * z**2,
    "triple_B": x**3 + x * y * z,
    "triple_E": x**3 + y * z**2,
}

e6_rows = {
    "squarefree": ((3, 0, 3), (2, 1, 3), (0, 3, 3), (2, 0, 4), (0, 2, 4)),
    "double": ((3, 0, 3), (2, 1, 3), (1, 2, 3), (2, 0, 4), (1, 1, 4)),
    "triple_C": ((1, 1, 4), (3, 0, 3), (2, 1, 3), (0, 1, 5), (2, 0, 4)),
    "triple_B": ((3, 0, 3), (2, 1, 3), (0, 1, 5), (1, 0, 5), (2, 0, 4)),
    "triple_E": ((1, 0, 5), (3, 0, 3), (2, 1, 3), (0, 0, 6), (2, 0, 4)),
}
e6_determinants = {
    "squarefree": -1728,
    "double": -6912,
    "triple_C": -186624,
    "triple_B": 15552,
    "triple_E": -46656,
}

universal_e6 = {
    a[0]: sp.Rational(2, 9) * u**2,
    a[1]: sp.Rational(4, 9) * u * v,
    a[2]: sp.Rational(2, 9) * v**2,
    l[6]: (9 * a[3] - 4 * u * w) / 12,
    l[7]: (9 * a[4] - 4 * v * w) / 12,
}


def coefficient_map(poly: sp.Poly, degree: int) -> dict[tuple[int, int, int], sp.Expr]:
    return {
        monomial: sp.expand(coefficient)
        for monomial, coefficient in poly.terms()
        if sum(monomial) == degree
    }


determinants: dict[str, sp.Poly] = {}
maps: dict[str, dict[int, dict[tuple[int, int, int], sp.Expr]]] = {}

for label, q in charts.items():
    h2 = sp.Matrix((A, B, W))
    h3 = sp.Matrix((sp.Rational(4, 3) * z * W, V, z**3))
    h4 = sp.Matrix((z**4, z * q, 0))
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + h2.jacobian((x, y, z))
                + h3.jacobian((x, y, z))
                + h4.jacobian((x, y, z))
            ).det()
        ),
        x,
        y,
        z,
    )
    determinants[label] = determinant
    maps[label] = {
        degree: coefficient_map(determinant, degree)
        for degree in (6, 5, 4)
    }

    e6 = maps[label][6]
    selected = [e6.get(row, sp.Integer(0)) for row in e6_rows[label]]
    matrix, rhs = sp.linear_eq_to_matrix(selected, a[:3] + (l[6], l[7]))
    expected_det = sp.Integer(e6_determinants[label])
    if mutation == "e6_minor" and label == "squarefree":
        expected_det += 1
    check(sp.expand(matrix.det() - expected_det) == 0, f"{label}: E6 minor")

    solution = sp.solve(
        selected,
        a[:3] + (l[6], l[7]),
        dict=True,
        simplify=False,
    )
    check(len(solution) == 1, f"{label}: unique E6 solution")
    for variable, expected in universal_e6.items():
        check(
            sp.expand(solution[0][variable] - expected) == 0,
            f"{label}: E6 solution {variable}",
        )
    for monomial, coefficient in e6.items():
        check(
            sp.expand(coefficient.subs(universal_e6)) == 0,
            f"{label}: full E6 residual {monomial}",
        )


def coeff(label: str, degree: int, monomial: tuple[int, int, int]) -> sp.Expr:
    return maps[label][degree].get(monomial, sp.Integer(0))


sf5 = {m: sp.expand(c.subs(universal_e6)) for m, c in maps["squarefree"][5].items()}
dbl5 = {m: sp.expand(c.subs(universal_e6)) for m, c in maps["double"][5].items()}
c5 = {m: sp.expand(c.subs(universal_e6)) for m, c in maps["triple_C"][5].items()}
b5 = {m: sp.expand(c.subs(universal_e6)) for m, c in maps["triple_B"][5].items()}
e5 = {m: sp.expand(c.subs(universal_e6)) for m, c in maps["triple_E"][5].items()}

expect(sf5[(4, 0, 1)], sp.Rational(4, 9) * u**3, "squarefree_e5_u")
expect(sf5[(0, 4, 1)], sp.Rational(4, 9) * v**3, "squarefree_e5_v")
expect(dbl5[(4, 0, 1)], sp.Rational(4, 9) * u**3, "double_e5_u")
expect(dbl5[(1, 3, 1)], -sp.Rational(8, 9) * v**3, "double_e5_v")
expect(c5[(2, 2, 1)], -sp.Rational(4, 3) * v**3, "triple_c_e5_v")
expect(
    c5[(2, 1, 2)].subs(v, 0),
    sp.Rational(8, 9) * u**3,
    "triple_c_e5_u",
)

expect(b5[(2, 2, 1)], -sp.Rational(4, 3) * v**3, "triple_b_e5_v")
expect(
    b5[(3, 0, 2)].subs(v, 0),
    u * (27 * a[4] + 4 * u**2) / 9,
    "triple_b_e5_a01",
)
expect(
    (-sp.Rational(1, 3) * b5[(2, 0, 3)] + b5[(0, 1, 4)]).subs(v, 0),
    -sp.Rational(2, 27) * u * (-9 * a[3] + 8 * u * w),
    "triple_b_e5_a10",
)

expect(e5[(2, 2, 1)], -sp.Rational(4, 3) * v**3, "triple_e_e5_v")
expect(
    e5[(1, 0, 4)].subs(v, 0),
    sp.Rational(2, 9) * u * (-9 * a[3] + 8 * u * w),
    "triple_e_e5_a10",
)
expect(e5[(0, 1, 4)].subs(v, 0), -u * a[4], "triple_e_e5_a01")

zero_ell_e5_rows = {
    "squarefree": ((2, 0, 3), (0, 2, 3)),
    "double": ((2, 0, 3), (1, 1, 3)),
    "triple_C": ((0, 1, 4), (2, 0, 3)),
    "triple_B": ((1, 0, 4), (2, 0, 3)),
    "triple_E": ((0, 0, 5), (2, 0, 3)),
}
zero_ell_solution = {
    l[0]: a[3] * w / 3,
    l[1]: a[4] * w / 3,
}

for label in charts:
    reduced5 = {
        monomial: sp.expand(
            coefficient.subs(universal_e6).subs({u: 0, v: 0})
        )
        for monomial, coefficient in maps[label][5].items()
    }
    selected = [reduced5.get(row, sp.Integer(0)) for row in zero_ell_e5_rows[label]]
    matrix, _ = sp.linear_eq_to_matrix(selected, (l[0], l[1]))
    check(matrix.det() != 0, f"{label}: zero-ell E5 minor")
    solution = sp.solve(selected, (l[0], l[1]), dict=True, simplify=False)
    check(len(solution) == 1, f"{label}: zero-ell E5 solution")
    for variable, expected in zero_ell_solution.items():
        check(
            sp.expand(solution[0][variable] - expected) == 0,
            f"{label}: zero-ell {variable}",
        )
    for monomial, coefficient in reduced5.items():
        check(
            sp.expand(coefficient.subs(zero_ell_solution)) == 0,
            f"{label}: full zero-ell E5 residual {monomial}",
        )

zero_substitution = {
    **universal_e6,
    u: 0,
    v: 0,
    **zero_ell_solution,
}
reduced4 = {
    label: {
        monomial: sp.factor(coefficient.subs(zero_substitution))
        for monomial, coefficient in maps[label][4].items()
    }
    for label in charts
}

expect(reduced4["squarefree"][(3, 0, 1)], -sp.Rational(3, 4) * a[3] ** 2, "zero_e4_sf_a10")
expect(reduced4["squarefree"][(0, 3, 1)], -sp.Rational(3, 4) * a[4] ** 2, "zero_e4_sf_a01")
expect(reduced4["double"][(3, 0, 1)], -sp.Rational(3, 4) * a[3] ** 2, "zero_e4_dbl_a10")
expect(reduced4["double"][(1, 2, 1)], sp.Rational(3, 2) * a[4] ** 2, "zero_e4_dbl_a01")
expect(reduced4["triple_C"][(2, 1, 1)], sp.Rational(9, 4) * a[4] ** 2, "zero_e4_c_a01")
expect(reduced4["triple_C"][(1, 1, 2)], -sp.Rational(3, 2) * a[3] ** 2, "zero_e4_c_a10")
expect(reduced4["triple_B"][(2, 1, 1)], sp.Rational(9, 4) * a[4] ** 2, "zero_e4_b_a01")
expect(
    reduced4["triple_B"][(2, 0, 2)].subs(a[4], 0),
    -sp.Rational(3, 4) * a[3] ** 2,
    "zero_e4_b_a10",
)
expect(reduced4["triple_E"][(2, 1, 1)], sp.Rational(9, 4) * a[4] ** 2, "zero_e4_e_a01")
expect(reduced4["triple_E"][(1, 0, 3)], -sp.Rational(3, 4) * a[3] ** 2, "zero_e4_e_a10")

for entry in (l[0], l[1]):
    check(
        sp.expand(
            entry.subs(zero_ell_solution).subs({a[3]: 0, a[4]: 0})
        )
        == 0,
        f"singular L entry {entry}",
    )
for entry in (l[6], l[7]):
    check(
        sp.expand(
            entry.subs(universal_e6).subs(
                {u: 0, v: 0, a[3]: 0, a[4]: 0}
            )
        )
        == 0,
        f"singular L entry {entry}",
    )

exceptional_b = {
    v: 0,
    a[3]: sp.Rational(8, 9) * u * w,
    a[4]: -sp.Rational(4, 27) * u**2,
}
exceptional_b_l = {
    l[0]: sp.Rational(2, 3) * a[5] * u
    - sp.Rational(4, 9) * l[8] * u
    - sp.Rational(4, 27) * u * w**2,
    l[1]: -sp.Rational(4, 81) * u**2 * w,
}
for monomial, coefficient in maps["triple_B"][5].items():
    check(
        sp.expand(
            coefficient
            .subs(universal_e6)
            .subs(exceptional_b)
            .subs(exceptional_b_l)
        )
        == 0,
        f"triple_B exceptional E5 residual {monomial}",
    )
b4 = {
    monomial: sp.factor(
        coefficient
        .subs(universal_e6)
        .subs(exceptional_b)
        .subs(exceptional_b_l)
    )
    for monomial, coefficient in maps["triple_B"][4].items()
}
expect(
    b4[(4, 0, 0)],
    sp.Rational(4, 81) * u**3 * (9 * t[1] + u),
    "triple_b_e4_first",
)
expect(
    b4[(0, 2, 2)],
    sp.Rational(4, 243) * u**3 * (18 * t[6] + u),
    "triple_b_e4_second",
)
expect(
    b4[(2, 1, 1)],
    -sp.Rational(4, 27) * u**3 * (t[1] - 6 * t[6] - u),
    "triple_b_e4_third",
)

exceptional_e = {
    v: 0,
    a[3]: sp.Rational(8, 9) * u * w,
    a[4]: 0,
}
exceptional_e_l = {
    l[0]: sp.Rational(2, 3) * a[5] * u
    - sp.Rational(4, 9) * l[8] * u
    - sp.Rational(4, 27) * u * w**2,
    l[1]: sp.Rational(4, 81) * u**3,
}
for monomial, coefficient in maps["triple_E"][5].items():
    check(
        sp.expand(
            coefficient
            .subs(universal_e6)
            .subs(exceptional_e)
            .subs(exceptional_e_l)
        )
        == 0,
        f"triple_E exceptional E5 residual {monomial}",
    )
e4 = {
    monomial: sp.factor(
        coefficient
        .subs(universal_e6)
        .subs(exceptional_e)
        .subs(exceptional_e_l)
    )
    for monomial, coefficient in maps["triple_E"][4].items()
}
expect(
    e4[(3, 0, 1)],
    sp.Rational(4, 81) * u**3 * (9 * t[5] - 2 * u),
    "triple_e_e4_first",
)
expect(
    e4[(0, 1, 3)],
    -sp.Rational(4, 27) * u**3 * (t[5] - u),
    "triple_e_e4_second",
)

if mutation != "strict":
    raise SystemExit(f"FAIL: unknown or escaped mutation {mutation}")

print("VERTICAL_A0_W0_ZERO_SYMPY_PASS_3C79E1")
