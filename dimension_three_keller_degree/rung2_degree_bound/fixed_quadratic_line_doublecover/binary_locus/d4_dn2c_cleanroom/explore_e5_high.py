#!/usr/bin/env python3
"""Clean-room search for lower-variable-free E5 coefficients on DN2C charts.

The script restores all binary coefficients of A,B and all nine linear
entries before extracting E5.  It first solves only the constant-rank
r^1 block of E6 (the ar2,br2 variables), then reports E5 coefficients
which are independent of every remaining lower variable.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

import derive_e6_projection as base

p, q, r, weight = base.p, base.q, base.r, base.weight
a, b, c, d, e, f = base.a, base.b, base.c, base.d, base.e, base.f
s = sp.sqrt(-2)

rows1 = [
    index for index, exponent in enumerate(base.EXPONENTS) if exponent[2] == 1
]
columns1 = [base.LOWER.index(base.ar[2]), base.LOWER.index(base.br[2])]
A1 = base.matrix[rows1, columns1].subs({a: 0, b: 0})
b1 = -base.constant[rows1, :].subs({a: 0, b: 0})
assert A1.extract((0, 1), (0, 1)).det() == 36
ar2_solution, br2_solution = tuple(
    A1.extract((0, 1), (0, 1)).inv() * b1.extract((0, 1), (0,))
)
general_r1_solution = {
    base.ar[2]: sp.factor(ar2_solution),
    base.br[2]: sp.factor(br2_solution),
}

plus_plane = {
    a: 0,
    b: 0,
    d: -2 * f,
    c: -sp.Rational(1, 3) * ((4 + 2 * s) * e + (2 - 2 * s) * f),
}
minus_plane = {
    a: 0,
    b: 0,
    d: -2 * f,
    c: -sp.Rational(1, 3) * ((4 - 2 * s) * e + (2 + 2 * s) * f),
}

for plane in (plus_plane, minus_plane):
    candidate = {
        variable: sp.factor(value.subs(plane), extension=s)
        for variable, value in general_r1_solution.items()
    }
    assert all(
        sp.factor(
            value.subs(plane).subs(candidate),
            extension=s,
        )
        == 0
        for value in A1 * sp.Matrix((base.ar[2], base.br[2])) - b1
    )

ab = sp.symbols("ab0:3")
bb = sp.symbols("bb0:3")
binary2 = (p**2, p * q, q**2)
Afull = base.A + sum(value * monomial for value, monomial in zip(ab, binary2))
Bfull = base.B + sum(value * monomial for value, monomial in zip(bb, binary2))

ell = sp.symbols("ell0:9")
linear = sp.Matrix(3, 3, ell)
linear[2, 2] = base.ell33
H2 = sp.Matrix((Afull, Bfull, base.T))
H3 = sp.Matrix((base.U, base.V, base.R))
H4 = sp.Matrix((base.P, base.Q, 0))
determinant = sp.Poly(
    sp.expand(
        (
            linear
            + weight * H2.jacobian(base.coords)
            + weight**2 * H3.jacobian(base.coords)
            + weight**3 * H4.jacobian(base.coords)
        ).det()
    ),
    weight,
)
E5 = sp.Poly(sp.expand(determinant.coeff_monomial(weight**5)), p, q, r)

all_lower = set(base.LOWER) | set(ab) | set(bb) | set(ell)
all_lower.discard(base.ell33)
all_lower.add(base.ell33)


def coefficient(polynomial: sp.Poly, exponent: tuple[int, int, int]) -> sp.Expr:
    i, j, k = exponent
    return polynomial.coeff_monomial(p**i * q**j * r**k)


def scan_chart(name: str, substitution: dict[sp.Symbol, sp.Expr]) -> None:
    r1_solution = {
        variable: value.subs(substitution)
        for variable, value in general_r1_solution.items()
    }
    specialized = sp.Poly(
        sp.expand(E5.as_expr().subs(substitution).subs(r1_solution)),
        p,
        q,
        r,
    )
    remaining_lower = all_lower - set(r1_solution)
    print("CHART", name)
    print(
        "  ar2,br2 =",
        tuple(sp.factor(r1_solution[value], extension=s) for value in (base.ar[2], base.br[2])),
    )
    found = 0
    for exponent in tuple(
        (i, 5 - k - i, k)
        for k in range(6)
        for i in range(5 - k, -1, -1)
    ):
        value = sp.expand(coefficient(specialized, exponent))
        dependencies = value.free_symbols & remaining_lower
        if value != 0 and not dependencies:
            print(
                "  LOWER_FREE",
                exponent,
                sp.factor(value, extension=s),
            )
            found += 1
    print("  lower-free nonzero count:", found)


scan_chart("plus_plane", plus_plane)
scan_chart("minus_plane", minus_plane)
k = sp.symbols("k")
scan_chart(
    "intersection",
    {a: 0, b: 0, c: -2 * k, d: -2 * k, e: k, f: k},
)
scan_chart("origin", {a: 0, b: 0, c: 0, d: 0, e: 0, f: 0})

# The three plus-plane lower-free coefficients span every binary
# quadratic in e,f after division by e-f.  Hence the plus interior is
# impossible; conjugation gives the minus interior.
plus_r1_solution = {
    variable: value.subs(plus_plane)
    for variable, value in general_r1_solution.items()
}
E5plus = sp.Poly(
    sp.expand(E5.as_expr().subs(plus_plane).subs(plus_r1_solution)),
    p,
    q,
    r,
)
selected_exponents = ((3, 0, 2), (2, 1, 2), (1, 2, 2))
selected = [
    sp.factor(coefficient(E5plus, exponent) / (e - f), extension=s)
    for exponent in selected_exponents
]
quadratic_monomials = (e**2, e * f, f**2)
selected_matrix = sp.Matrix(
    [
        [
            sp.Poly(value, e, f, extension=s).coeff_monomial(monomial)
            for monomial in quadratic_monomials
        ]
        for value in selected
    ]
)
selected_determinant = sp.factor(selected_matrix.det(), extension=s)
assert selected_determinant != 0
print("PLUS_INTERIOR_SELECTED_MATRIX_DET =", selected_determinant)

# Punctured intersection.  Solve the complete r^0 block of E6 by an
# explicit 4x4 pivot, retain every free lower variable, and rescan E5.
intersection = {a: 0, b: 0, c: -2 * k, d: -2 * k, e: k, f: k}
rows0 = [
    index for index, exponent in enumerate(base.EXPONENTS) if exponent[2] == 0
]
r0_variables = (
    base.uc
    + base.vc
    + base.tc
    + (base.ar[0], base.ar[1], base.br[0], base.br[1], base.ell33)
)
r0_columns = [base.LOWER.index(value) for value in r0_variables]
A0line = base.matrix[rows0, r0_columns].subs(intersection)
b0line = -base.constant[rows0, :].subs(intersection)
assert A0line.rank() == 4
_, pivot_columns = A0line.rref()
assert len(pivot_columns) == 4
pivot_rows = next(
    rows
    for rows in sp.utilities.iterables.combinations(range(7), 4)
    if A0line.extract(rows, pivot_columns).det() != 0
)
pivot = A0line.extract(pivot_rows, pivot_columns)
pivot_determinant = sp.factor(pivot.det())
print("INTERSECTION_E6_R0_RAW_PIVOT_DET =", pivot_determinant)
assert len(sp.Poly(pivot_determinant, k).terms()) == 1
assert sp.Poly(pivot_determinant, k).degree() > 0
pivot_variables = tuple(r0_variables[index] for index in pivot_columns)
pivot_solution_vector = pivot.inv() * (
    b0line.extract(pivot_rows, (0,))
    - A0line.extract(
        pivot_rows,
        tuple(index for index in range(16) if index not in pivot_columns),
    )
    * sp.Matrix(
        tuple(
            r0_variables[index]
            for index in range(16)
            if index not in pivot_columns
        )
    )
)
pivot_solution = {
    variable: sp.factor(value)
    for variable, value in zip(pivot_variables, pivot_solution_vector)
}
assert all(
    sp.factor(value.subs(pivot_solution)) == 0
    for value in A0line * sp.Matrix(r0_variables) - b0line
)
print(
    "INTERSECTION_E6_R0_PIVOT =",
    pivot_rows,
    pivot_columns,
    pivot_variables,
    pivot_determinant,
)

intersection_all = dict(intersection)
intersection_all.update({base.ar[2]: 2 * k**2, base.br[2]: 2 * k**2})
intersection_all.update(pivot_solution)
E5line = sp.Poly(
    sp.expand(E5.as_expr().subs(intersection_all)),
    p,
    q,
    r,
)
remaining_line_lower = all_lower - set(intersection_all)
line_lower_free: list[tuple[tuple[int, int, int], sp.Expr]] = []
for exponent in tuple(
    (i, 5 - rdegree - i, rdegree)
    for rdegree in range(6)
    for i in range(5 - rdegree, -1, -1)
):
    value = sp.factor(coefficient(E5line, exponent))
    if value != 0 and not (value.free_symbols & remaining_line_lower):
        line_lower_free.append((exponent, value))
        print("INTERSECTION_LOWER_FREE", exponent, value)
print("INTERSECTION_LOWER_FREE_COUNT =", len(line_lower_free))
# The exploratory full-support dump was intentionally removed after the
# sparse r^1/r^0 blocks below were isolated; factoring the dense r^0
# coefficients obscures the exact pivot calculation and is unnecessary.

# Solve the punctured-intersection E5 r^1 equations by an explicit pivot.
e5_r1_exponents = tuple((4 - index, index, 1) for index in range(5))
e5_r1_equations = sp.Matrix(
    [coefficient(E5line, exponent) for exponent in e5_r1_exponents]
)
e5_r1_pivot_candidates = (
    base.ar[0],
    base.ar[1],
    base.br[0],
    base.br[1],
)
M51 = e5_r1_equations.jacobian(e5_r1_pivot_candidates)
c51 = e5_r1_equations.subs(
    {variable: 0 for variable in e5_r1_pivot_candidates}
)
assert e5_r1_equations == M51 * sp.Matrix(e5_r1_pivot_candidates) + c51
rank51 = M51.rank()
print("INTERSECTION_E5_R1_MATRIX_RANK =", rank51)
assert rank51 in (2, 3, 4)
columns51 = M51.rref()[1]
assert len(columns51) == rank51
rows51 = next(
    rows
    for rows in sp.utilities.iterables.combinations(range(5), rank51)
    if M51.extract(rows, columns51).det() != 0
)
pivot51 = M51.extract(rows51, columns51)
det51 = sp.factor(pivot51.det())
free51_columns = tuple(
    index for index in range(4) if index not in columns51
)
solution51_vector = -pivot51.inv() * (
    c51.extract(rows51, (0,))
    + M51.extract(rows51, free51_columns)
    * sp.Matrix(
        tuple(e5_r1_pivot_candidates[index] for index in free51_columns)
    )
)
solution51 = {
    e5_r1_pivot_candidates[index]: sp.factor(value)
    for index, value in zip(columns51, solution51_vector)
}
residual51 = tuple(
    sp.factor(value.subs(solution51)) for value in e5_r1_equations
)
print("INTERSECTION_E5_R1_PIVOT =", rows51, columns51, det51)
for variable in solution51:
    print("  SOLVE", variable, "=", solution51[variable])
for index, value in enumerate(residual51):
    if value != 0:
        print("  RESIDUAL", e5_r1_exponents[index], value)

E5line_after_r1 = sp.Poly(
    sp.expand(E5line.as_expr().subs(solution51)),
    p,
    q,
    r,
)
e5_r0_exponents = tuple((5 - index, index, 0) for index in range(6))
e5_r0_equations = sp.Matrix(
    [coefficient(E5line_after_r1, exponent) for exponent in e5_r0_exponents]
)
e5_new_candidates = ab + bb + (ell[2], ell[5], ell[6], ell[7])
M50 = e5_r0_equations.jacobian(e5_new_candidates)
c50 = e5_r0_equations.subs({variable: 0 for variable in e5_new_candidates})
affine50 = sp.simplify(
    e5_r0_equations - M50 * sp.Matrix(e5_new_candidates) - c50
)
assert affine50 == sp.zeros(6, 1)
rank50 = M50.rank()
augmented_rank50 = M50.row_join(-c50).rank()
print(
    "INTERSECTION_E5_R0_NEW_MATRIX_SHAPE_RANK =",
    M50.shape,
    rank50,
    augmented_rank50,
)
if rank50 > 0:
    columns50 = M50.rref()[1]
    assert len(columns50) == rank50
    rows50 = next(
        rows
        for rows in sp.utilities.iterables.combinations(range(6), rank50)
        if M50.extract(rows, columns50).det() != 0
    )
    pivot50 = M50.extract(rows50, columns50)
    det50 = sp.factor(pivot50.det())
    solution50_vector = -pivot50.inv() * (
        c50.extract(rows50, (0,))
        + M50.extract(
            rows50,
            tuple(index for index in range(len(e5_new_candidates)) if index not in columns50),
        )
        * sp.Matrix(
            tuple(
                e5_new_candidates[index]
                for index in range(len(e5_new_candidates))
                if index not in columns50
            )
        )
    )
    solution50 = {
        e5_new_candidates[index]: sp.factor(value)
        for index, value in zip(columns50, solution50_vector)
    }
    residual50 = tuple(
        sp.factor(value.subs(solution50)) for value in e5_r0_equations
    )
    print(
        "INTERSECTION_E5_R0_PIVOT =",
        rows50,
        columns50,
        tuple(e5_new_candidates[index] for index in columns50),
        det50,
    )
    for index, value in enumerate(residual50):
        if value != 0:
            print(
                "  E5_R0_RESIDUAL",
                e5_r0_exponents[index],
                tuple(sorted(value.free_symbols & remaining_line_lower, key=str)),
                value,
            )
else:
    solution50 = {}

if rank50 == 3:
    Ahat, Bhat, Lhat = sp.symbols("Ahat Bhat Lhat")
    normalized50 = tuple(
        sp.factor(
            value.subs(
                {
                    base.ar[1]: k * Ahat,
                    base.br[0]: k * Bhat,
                    base.ell33: k * Lhat,
                }
            )
            / k
        )
        for value in residual50
        if value != 0
    )
    assert len(normalized50) == 3
    assert all(k not in value.free_symbols for value in normalized50)
    print("INTERSECTION_E5_NORMALIZED_RESIDUALS")
    for value in normalized50:
        print("  ", value)
    factored_last = sp.factor_list(normalized50[2])
    assert len(factored_last[1]) == 2
    branch_factors = tuple(value for value, multiplicity in factored_last[1])
    for branch_index, branch_factor in enumerate(branch_factors):
        print("INTERSECTION_E5_BRANCH", branch_index, branch_factor)
        if Lhat in branch_factor.free_symbols:
            branch_solution = sp.solve(branch_factor, Lhat, dict=True)[0]
        else:
            branch_solution = sp.solve(branch_factor, Ahat, dict=True)[0]
        branch_pair = tuple(
            sp.factor(value.subs(branch_solution))
            for value in normalized50[:2]
        )
        print("  BRANCH_SOLUTION", branch_solution)
        print("  BRANCH_EQ0", branch_pair[0])
        print("  BRANCH_EQ1", branch_pair[1])
        print("  BRANCH_DIFF", sp.factor(branch_pair[0] - branch_pair[1]))

    # Four explicit E5 components: two factors of the final residual and
    # two factors of the common quadratic.
    X0 = base.tc[0] - base.tc[1] + base.tc[2]
    Z0 = 6 * base.vc[1] - 9 * base.vc[2] + 9 * base.vc[3]
    common_quadratic = sp.factor(
        -sp.Rational(3, 2)
        * branch_pair[0]
    )
    expected_quadratic = sp.expand(
        (3 * Bhat - (2 + 2 * sp.I) * X0 - Z0)
        * (3 * Bhat - (2 - 2 * sp.I) * X0 - Z0)
    )
    assert sp.expand(common_quadratic - expected_quadratic) == 0

    E4 = sp.Poly(
        sp.expand(determinant.coeff_monomial(weight**4)),
        p,
        q,
        r,
    )
    base_substitutions = (
        intersection,
        {base.ar[2]: 2 * k**2, base.br[2]: 2 * k**2},
        pivot_solution,
        solution51,
        solution50,
    )
    f_branch_direct = {
        base.ell33: k
        * (
            base.tc[1]
            - 2 * base.tc[2]
            - sp.Rational(3, 2) * base.vc[1]
            + 3 * base.vc[2]
            - sp.Rational(9, 2) * base.vc[3]
        )
    }
    g_branch_direct = {
        base.ar[1]: (
            8 * base.ell33
            + k
            * (
                8 * base.tc[2]
                - 9 * base.uc[3]
                + 12 * base.vc[1]
                - 12 * base.vc[2]
                + 18 * base.vc[3]
            )
        )
        / 6
    }
    e4_exponents = tuple(
        (i, 4 - rdegree - i, rdegree)
        for rdegree in range(4, 0, -1)
        for i in range(4 - rdegree, -1, -1)
    )
    for fg_name, fg_substitution in (
        ("F", f_branch_direct),
        ("G", g_branch_direct),
    ):
        for sign in (1, -1):
            q_substitution = {
                base.br[0]: k
                * ((2 + sign * 2 * sp.I) * X0 + Z0)
                / 3
            }
            solved_variables = (
                set(intersection)
                | {base.ar[2], base.br[2]}
                | set(pivot_solution)
                | set(solution51)
                | set(solution50)
                | set(q_substitution)
                | set(fg_substitution)
            )
            remaining4 = all_lower - solved_variables
            print("INTERSECTION_E4_COMPONENT", fg_name, sign)
            for exponent in e4_exponents:
                value = coefficient(E4, exponent)
                for substitution in base_substitutions:
                    value = value.subs(substitution)
                value = value.subs(q_substitution).subs(fg_substitution)
                value = sp.cancel(value)
                if value == 0:
                    continue
                dependencies = tuple(
                    sorted(value.free_symbols & remaining4, key=str)
                )
                if len(dependencies) <= 4:
                    print(
                        "  E4_SIMPLE",
                        exponent,
                        dependencies,
                        sp.factor_terms(value),
                    )

    xzero = {base.tc[0]: base.tc[1] - base.tc[2]}
    q_common = {base.br[0]: k * Z0 / 3}
    for fg_name, fg_substitution in (
        ("F", f_branch_direct),
        ("G", g_branch_direct),
    ):
        print("INTERSECTION_E4_AFTER_XZERO", fg_name)
        for exponent in tuple((3 - index, index, 1) for index in range(4)):
            value = coefficient(E4, exponent)
            for substitution in base_substitutions:
                value = value.subs(substitution)
            value = (
                value.subs(q_common)
                .subs(fg_substitution)
                .subs(xzero)
            )
            value = sp.cancel(value)
            dependencies = tuple(
                sorted(value.free_symbols & all_lower, key=str)
            )
            print(
                "  E4_R1",
                exponent,
                dependencies,
                sp.factor_terms(value),
            )

    # Exact low-complexity point on the F=G overlap.  Choose all remaining
    # binary cubic freedom zero and T0=p^2+pq; solve only for the upper-left
    # 2x2 block of L.
    v_quadratic = (
        base.vc[1] ** 2
        - 3 * base.vc[1] * base.vc[2]
        + 3 * base.vc[1] * base.vc[3]
        + 2 * base.vc[2] ** 2
        - 3 * base.vc[2] * base.vc[3]
    )
    overlap_substitutions = (
        xzero,
        q_common,
        f_branch_direct,
        g_branch_direct,
        {
            ell[5]: k
            * (
                bb[1]
                - 2 * bb[2]
                - sp.Rational(1, 2) * v_quadratic
            )
        },
    )
    print("INTERSECTION_E4_F_BRANCH_R0")
    f_e4_substitutions = (
        xzero,
        q_common,
        f_branch_direct,
        overlap_substitutions[-1],
    )
    for exponent in ((0, 4, 0), (1, 3, 0), (2, 2, 0)):
        value = coefficient(E4, exponent)
        for substitution in base_substitutions + f_e4_substitutions:
            value = value.subs(substitution)
        value = sp.cancel(value)
        dependencies = tuple(sorted(value.free_symbols & all_lower, key=str))
        print(
            "  E4_F_R0",
            exponent,
            dependencies,
            sp.factor_terms(value),
        )
    print("D4_DN2C_E4_F_R0_SCAN_PASS")
    raise SystemExit(0)
    representative_fixed = {
        k: 1,
        base.tc[1]: 1,
        base.tc[2]: 0,
        base.uc[3]: 0,
        base.vc[1]: 0,
        base.vc[2]: 0,
        base.vc[3]: 0,
        ab[2]: 0,
        bb[1]: 0,
        bb[2]: 0,
        ell[2]: 0,
        ell[6]: 0,
        ell[7]: 0,
    }
    top_linear = (ell[0], ell[1], ell[3], ell[4])
    representative_e4 = []
    for exponent in tuple(
        (i, 4 - rdegree - i, rdegree)
        for rdegree in range(5)
        for i in range(4 - rdegree, -1, -1)
    ):
        value = coefficient(E4, exponent)
        for substitution in base_substitutions + overlap_substitutions:
            value = value.subs(substitution)
        value = sp.cancel(value.subs(representative_fixed))
        representative_e4.append(value)
    representative_e4 = sp.Matrix(representative_e4)
    M4rep = representative_e4.jacobian(top_linear)
    c4rep = representative_e4.subs({value: 0 for value in top_linear})
    assert representative_e4 == M4rep * sp.Matrix(top_linear) + c4rep
    print(
        "REPRESENTATIVE_E4_LINEAR_RANKS =",
        M4rep.rank(),
        M4rep.row_join(-c4rep).rank(),
    )
    representative_linear_solutions = sp.linsolve(
        (M4rep, -c4rep),
        top_linear,
    )
    print("REPRESENTATIVE_E4_LINEAR_SOLUTIONS =", representative_linear_solutions)

print("D4_DN2C_E5_HIGH_SCAN_PASS")
