#!/usr/bin/env python3
"""Clean-room sparse exploration below E6 for D4-DN-3.

This script contains the frozen top form and audited contact atlas explicitly.
It imports no project module and reads no project data.
"""

from __future__ import annotations

import argparse
import itertools
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


p, q, r, w = sp.symbols("p q r w")
s, k = sp.symbols("s k")
sqrt2 = sp.sqrt(2)


def homogeneous_monomials(degree: int) -> tuple[sp.Expr, ...]:
    values: list[sp.Expr] = []
    for ip in range(degree, -1, -1):
        remainder = degree - ip
        for iq in range(remainder, -1, -1):
            ir = remainder - iq
            values.append(p**ip * q**iq * r**ir)
    return tuple(values)


def coefficients(expression: sp.Expr, degree: int) -> tuple[sp.Expr, ...]:
    polynomial = sp.Poly(expression, p, q, r)
    return tuple(
        polynomial.coeff_monomial(monomial)
        for monomial in homogeneous_monomials(degree)
    )


def build(contact_root: sp.Expr):
    h = (p + q) ** 2
    P = sp.expand(h * p**2)
    Q = sp.expand(h * q**2)
    R = sp.expand((p + q) ** 3)

    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    t = sp.symbols("t0:3")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")

    U0 = u[0] * p**3 + u[1] * p**2 * q + u[2] * p * q**2 + u[3] * q**3
    V0 = v[0] * p**3 + v[1] * p**2 * q + v[2] * p * q**2 + v[3] * q**3
    T0 = t[0] * p**2 + t[1] * p * q + t[2] * q**2
    A = (
        a[0] * p**2
        + a[1] * p * q
        + a[2] * p * r
        + a[3] * q**2
        + a[4] * q * r
        + a[5] * r**2
    )
    B = (
        b[0] * p**2
        + b[1] * p * q
        + b[2] * p * r
        + b[3] * q**2
        + b[4] * q * r
        + b[5] * r**2
    )
    L = sp.Matrix(3, 3, ell)

    U1 = sp.expand(
        (4 * k - 3 * (s + contact_root * k)) * p**2 / 3
        + (4 * k - 3 * s) * p * q / 3
    )
    V1 = sp.expand((s + contact_root * k) * p * q + s * q**2)
    T1 = k * (p + q)

    H4 = sp.Matrix((P, Q, 0))
    H3 = sp.Matrix((U0 + r * U1, V0 + r * V1, R))
    H2 = sp.Matrix((A, B, T0 + r * T1))
    jacobian = (
        L
        + w * H2.jacobian((p, q, r))
        + w**2 * H3.jacobian((p, q, r))
        + w**3 * H4.jacobian((p, q, r))
    )
    determinant = sp.Poly(sp.expand(jacobian.det()), w)
    lower18 = (
        a[2],
        a[4],
        a[5],
        b[2],
        b[4],
        b[5],
        ell[8],
    ) + u + v + t
    return {
        "contact_root": contact_root,
        "determinant": determinant,
        "a": a,
        "b": b,
        "ell": ell,
        "u": u,
        "v": v,
        "t": t,
        "lower18": lower18,
    }


def solve_chart(data, chart: str):
    determinant = data["determinant"]
    lower18 = data["lower18"]
    e6_equations = coefficients(determinant.coeff_monomial(w**6), 6)
    matrix6, rhs6 = sp.linear_eq_to_matrix(e6_equations, lower18)
    assert matrix6.shape == (28, 18)

    if chart == "interior":
        rows = (0, 1, 2, 3, 4, 6, 10)
        columns = (0, 1, 2, 3, 5, 7, 8)
        expected_rank = 7
    elif chart == "intersection":
        matrix6 = matrix6.subs(k, 0)
        rhs6 = rhs6.subs(k, 0)
        e6_equations = tuple(value.subs(k, 0) for value in e6_equations)
        rows = (0, 1, 2, 3, 4, 6)
        columns = (0, 1, 2, 3, 5, 7)
        expected_rank = 6
    elif chart == "origin":
        matrix6 = matrix6.subs({k: 0, s: 0})
        rhs6 = rhs6.subs({k: 0, s: 0})
        e6_equations = tuple(
            value.subs({k: 0, s: 0}) for value in e6_equations
        )
        rows = (0, 1, 2, 3, 4)
        columns = (0, 1, 2, 3, 5)
        expected_rank = 5
    else:
        raise ValueError(chart)

    pivot_matrix = matrix6.extract(rows, columns)
    pivot = sp.factor(pivot_matrix.det(), extension=sqrt2)
    assert matrix6.rank() == expected_rank
    assert matrix6.row_join(rhs6).rank() == expected_rank

    pivot_variables = tuple(lower18[index] for index in columns)
    free_columns = tuple(index for index in range(18) if index not in columns)
    free_variables = sp.Matrix([lower18[index] for index in free_columns])
    selected_rhs = rhs6.extract(rows, (0,))
    selected_free = matrix6.extract(rows, free_columns)
    solution_vector = pivot_matrix.inv() * (
        selected_rhs - selected_free * free_variables
    )
    solution = dict(zip(pivot_variables, map(sp.cancel, solution_vector)))
    assert all(
        sp.cancel(equation.subs(solution)) == 0
        for equation in e6_equations
    )

    return {
        "equations": e6_equations,
        "matrix": matrix6,
        "rhs": rhs6,
        "pivot": pivot,
        "rank": expected_rank,
        "solution": solution,
        "pivot_variables": pivot_variables,
        "free_variables": tuple(free_variables),
    }


def summarize_lower(data, solved, chart: str):
    determinant = data["determinant"]
    substitutions = dict(solved["solution"])
    if chart == "intersection":
        substitutions[k] = 0
    elif chart == "origin":
        substitutions[k] = 0
        substitutions[s] = 0

    print("CHART", chart)
    print("PIVOT", solved["pivot"])
    print("RANK", solved["rank"])
    print("PIVOT_VARIABLES", solved["pivot_variables"])
    print("FREE_VARIABLE_COUNT", len(solved["free_variables"]))

    all_unknowns = (
        set(data["a"])
        | set(data["b"])
        | set(data["ell"])
        | set(data["u"])
        | set(data["v"])
        | set(data["t"])
    )

    saved_residuals = None
    for weight_degree in (5,):
        homogeneous_degree = weight_degree
        raw = coefficients(
            determinant.coeff_monomial(w**weight_degree),
            homogeneous_degree,
        )
        residuals = [sp.cancel(value.subs(substitutions)) for value in raw]
        saved_residuals = residuals
        nonzero = [
            (homogeneous_monomials(homogeneous_degree)[index], value)
            for index, value in enumerate(residuals)
            if value != 0
        ]
        constants = [
            (monomial, value)
            for monomial, value in nonzero
            if not (value.free_symbols & all_unknowns)
        ]
        print(
            "WEIGHT",
            weight_degree,
            "NONZERO",
            len(nonzero),
            "UNKNOWN_FREE",
            len(constants),
        )
        for monomial, value in nonzero:
            unknown_count = len(value.free_symbols & all_unknowns)
            print(
                "PROFILE",
                monomial,
                "OPS",
                sp.count_ops(value),
                "UNKNOWNS",
                unknown_count,
            )
            if sp.count_ops(value) <= 80:
                print(
                    "SMALL",
                    monomial,
                    sp.factor(value, extension=sqrt2),
                )
            if unknown_count == 0:
                print(
                    "OBSTRUCTION",
                    monomial,
                    sp.factor(value, extension=sqrt2),
                )

    if chart == "interior":
        assert saved_residuals is not None
        root = data["contact_root"]
        if sp.simplify(root - (-4 + 2 * sqrt2) / 3) == 0:
            scalar = 3 * (sqrt2 - 2)
            marker = "D4_DN3_CLEANROOM_PLUS_INTERIOR_E5_PASS"
        else:
            assert sp.simplify(root - (-4 - 2 * sqrt2) / 3) == 0
            scalar = 3 * (-sqrt2 - 2)
            marker = "D4_DN3_CLEANROOM_MINUS_INTERIOR_E5_PASS"
        residual_by_monomial = dict(
            zip(homogeneous_monomials(5), saved_residuals)
        )
        assert sp.expand(
            residual_by_monomial[p**3 * r**2]
            - scalar * k * (s + root * k) ** 2
        ) == 0
        assert sp.expand(
            residual_by_monomial[q**3 * r**2]
            - scalar * k * (s - sp.Rational(4, 3) * k) ** 2
        ) == 0
        assert scalar != 0
        assert sp.simplify(root + sp.Rational(4, 3)) != 0
        print(marker)
        return

    if chart == "intersection":
        assert saved_residuals is not None
        monomials5 = homogeneous_monomials(5)
        r_rows = tuple(
            index
            for index, monomial in enumerate(monomials5)
            if sp.degree(monomial, r) == 1 and saved_residuals[index] != 0
        )
        r_equations = tuple(saved_residuals[index] for index in r_rows)
        b = data["b"]
        ell = data["ell"]
        u = data["u"]
        v = data["v"]
        t = data["t"]
        candidates = (b[4], ell[8]) + t + u[1:] + v[1:]
        r_matrix, r_rhs = sp.linear_eq_to_matrix(r_equations, candidates)
        assert r_matrix.rows == 5
        r_rank = r_matrix.rank()
        print("INTERSECTION_E5_R_RANK", r_rank)
        print(
            "INTERSECTION_E5_R_AUGMENTED_RANK",
            r_matrix.row_join(r_rhs).rank(),
        )
        for left in r_matrix.T.nullspace():
            compatibility = sp.factor((left.T * r_rhs)[0])
            print("INTERSECTION_E5_R_COMPATIBILITY", compatibility)
        pivots: list[tuple[int, tuple[int, ...], sp.Expr]] = []
        for selected_rows in itertools.combinations(range(r_matrix.rows), r_rank):
            for columns in itertools.combinations(range(len(candidates)), r_rank):
                determinant5 = sp.factor(
                    r_matrix.extract(selected_rows, columns).det()
                )
                if determinant5 != 0:
                    pivots.append(
                        (
                            sp.count_ops(determinant5),
                            selected_rows,
                            columns,
                            determinant5,
                        )
                    )
        pivots.sort(key=lambda item: (item[0], item[1]))
        print("INTERSECTION_E5_R_ROWS", r_rows)
        print("INTERSECTION_E5_R_CANDIDATES", candidates)
        print("INTERSECTION_E5_R_PIVOTS", len(pivots))
        for pivot_data in pivots[:10]:
            print("R_PIVOT", pivot_data)

        # Freeze a pivot with determinant 192*s^4: the first three nonzero
        # r-equations, solving b4,l8,t1.  It is valid on the entire s != 0
        # intersection chart.
        stage1_rows = (0, 1, 2)
        stage1_columns = (0, 1, 3)
        stage1_matrix = r_matrix.extract(stage1_rows, stage1_columns)
        assert stage1_matrix.det() == 192 * s**4
        stage1_variables = tuple(candidates[index] for index in stage1_columns)
        stage1_free_columns = tuple(
            index for index in range(len(candidates)) if index not in stage1_columns
        )
        stage1_solution_vector = stage1_matrix.inv() * (
            r_rhs.extract(stage1_rows, (0,))
            - r_matrix.extract(stage1_rows, stage1_free_columns)
            * sp.Matrix([candidates[index] for index in stage1_free_columns])
        )
        stage1_solution = dict(
            zip(stage1_variables, map(sp.cancel, stage1_solution_vector))
        )
        assert all(
            sp.cancel(equation.subs(stage1_solution)) == 0
            for equation in r_equations
        )
        print("INTERSECTION_E5_STAGE1_VARIABLES", stage1_variables)
        for variable in stage1_variables:
            print("INTERSECTION_E5_STAGE1", variable, stage1_solution[variable])

        stage1_residuals = [
            sp.cancel(value.subs(stage1_solution)) for value in saved_residuals
        ]
        non_r_rows = tuple(
            index
            for index, monomial in enumerate(monomials5)
            if sp.degree(monomial, r) == 0 and stage1_residuals[index] != 0
        )
        non_r_equations = tuple(stage1_residuals[index] for index in non_r_rows)
        a = data["a"]
        stage2_candidates = (
            a[0],
            a[1],
            a[3],
            b[0],
            b[1],
            b[3],
        ) + tuple(ell[:8])
        stage2_matrix, stage2_rhs = sp.linear_eq_to_matrix(
            non_r_equations, stage2_candidates
        )
        assert stage2_matrix.rows == 6

        # Choose pivot columns from a deterministic exact sample, then certify
        # the resulting symbolic determinant.
        remaining_symbols = sorted(
            (
                set().union(*(equation.free_symbols for equation in non_r_equations))
                - set(stage2_candidates)
                - {s}
            ),
            key=str,
        )
        stage2_columns = None
        sampled_ranks = []
        sample_patterns = (
            lambda index: 0,
            lambda index: index + 1,
            lambda index: (2 * index + 1) % 7 - 3,
            lambda index: (3 * index + 2) % 11 - 5,
        )
        for sample_pattern in sample_patterns:
            sample_substitution = {
                symbol: sample_pattern(index)
                for index, symbol in enumerate(remaining_symbols)
            }
            sample_substitution[s] = 1
            sampled = stage2_matrix.subs(sample_substitution)
            sampled_ranks.append(sampled.rank())
            if sampled.rank() == 6:
                stage2_columns = tuple(sampled.rref()[1])
                break
        print("INTERSECTION_E5_STAGE2_SAMPLE_RANKS", sampled_ranks)
        if stage2_columns is None:
            stage2_rank = stage2_matrix.rank()
            print("INTERSECTION_E5_STAGE2_SYMBOLIC_RANK", stage2_rank)
            print(
                "INTERSECTION_E5_STAGE2_AUGMENTED_RANK",
                stage2_matrix.row_join(stage2_rhs).rank(),
            )
            compatibilities = [
                sp.factor((left.T * stage2_rhs)[0])
                for left in stage2_matrix.T.nullspace()
            ]
            for compatibility in compatibilities:
                print("INTERSECTION_E5_STAGE2_COMPATIBILITY", compatibility)

            stage2_pivots = []
            for selected_rows in itertools.combinations(
                range(stage2_matrix.rows), stage2_rank
            ):
                for columns in itertools.combinations(
                    range(len(stage2_candidates)), stage2_rank
                ):
                    determinant3 = sp.factor(
                        stage2_matrix.extract(selected_rows, columns).det()
                    )
                    if determinant3 != 0:
                        stage2_pivots.append(
                            (
                                sp.count_ops(determinant3),
                                selected_rows,
                                columns,
                                determinant3,
                            )
                        )
            stage2_pivots.sort(key=lambda item: (item[0], item[1], item[2]))
            print("INTERSECTION_E5_STAGE2_PIVOTS", len(stage2_pivots))
            for item in stage2_pivots[:10]:
                print("STAGE2_PIVOT", item)

            _, stage2_rows, stage2_columns, stage2_pivot = stage2_pivots[0]
            stage2_variables = tuple(
                stage2_candidates[index] for index in stage2_columns
            )
            stage2_free_columns = tuple(
                index
                for index in range(len(stage2_candidates))
                if index not in stage2_columns
            )
            stage2_selected_matrix = stage2_matrix.extract(
                stage2_rows, stage2_columns
            )
            stage2_solution_vector = stage2_selected_matrix.inv() * (
                stage2_rhs.extract(stage2_rows, (0,))
                - stage2_matrix.extract(stage2_rows, stage2_free_columns)
                * sp.Matrix(
                    [
                        stage2_candidates[index]
                        for index in stage2_free_columns
                    ]
                )
            )
            stage2_solution = dict(
                zip(stage2_variables, map(sp.cancel, stage2_solution_vector))
            )
            print("INTERSECTION_E5_STAGE2_VARIABLES", stage2_variables)
            print("INTERSECTION_E5_STAGE2_SAFE_PIVOT", stage2_pivot)

            combined_solution = dict(stage1_solution)
            combined_solution.update(stage2_solution)
            e5_after = [
                sp.factor(sp.cancel(value.subs(stage2_solution)))
                for value in stage1_residuals
            ]
            nonzero_after = [value for value in e5_after if value != 0]
            assert nonzero_after
            common_compatibility = sp.factor(
                compatibilities[0] / (3 * s / 4)
            )
            for value in nonzero_after:
                print(
                    "INTERSECTION_E5_REMAINING_RATIO",
                    sp.factor(sp.cancel(value / common_compatibility)),
                )
            print(
                "INTERSECTION_E5_SINGLE_CONDITION",
                common_compatibility,
            )

            # Proceed to E4 without solving the quadratic compatibility.
            e4_raw = coefficients(
                determinant.coeff_monomial(w**4).subs(k, 0), 4
            )
            e4_residuals = [
                sp.cancel(
                    value.subs(solved["solution"])
                    .subs(stage1_solution)
                    .subs(stage2_solution)
                )
                for value in e4_raw
            ]
            monomials4 = homogeneous_monomials(4)
            print(
                "INTERSECTION_E4_NONZERO",
                sum(value != 0 for value in e4_residuals),
            )
            for monomial, value in zip(monomials4, e4_residuals):
                if value == 0:
                    continue
                print(
                    "E4_PROFILE",
                    monomial,
                    "OPS",
                    sp.count_ops(value),
                    "UNKNOWNS",
                    len(value.free_symbols & all_unknowns),
                )
                if sp.count_ops(value) <= 100:
                    print(
                        "E4_SMALL",
                        monomial,
                        sp.factor(value),
                    )

            v_difference = v[0] - v[1] + v[2] - v[3]
            assert sp.factor(
                e4_residuals[5] / v_difference
            ) == -9 * s**3 / 4
            v0_solution = {v[0]: v[1] - v[2] + v[3]}
            compatibility_after_v = sp.factor(
                common_compatibility.subs(v0_solution)
            )
            print(
                "INTERSECTION_E5_CONDITION_AFTER_E4",
                compatibility_after_v,
            )
            e4_after_v = [
                sp.cancel(value.subs(v0_solution)) for value in e4_residuals
            ]
            print(
                "INTERSECTION_E4_AFTER_V_NONZERO",
                sum(value != 0 for value in e4_after_v),
            )
            for monomial, value in zip(monomials4, e4_after_v):
                if value == 0:
                    continue
                if sp.count_ops(value) <= 250:
                    print(
                        "E4_AFTER_V",
                        monomial,
                        sp.factor(value),
                    )

            w_linear = (
                u[1]
                - 2 * u[2]
                + 3 * u[3]
                - v[1]
                + 2 * v[2]
                - 3 * v[3]
            )
            assert compatibility_after_v == w_linear**2
            u1_solution = {
                u[1]: 2 * u[2] - 3 * u[3] + v[1] - 2 * v[2] + 3 * v[3]
            }
            e4_after_vw = [
                sp.cancel(value.subs(u1_solution)) for value in e4_after_v
            ]
            assert all(
                sp.cancel(value.subs(v0_solution).subs(u1_solution)) == 0
                for value in e5_after
            )
            e4_r_rows = tuple(
                index
                for index, monomial in enumerate(monomials4)
                if sp.degree(monomial, r) == 1 and e4_after_vw[index] != 0
            )
            e4_r_equations = tuple(
                e4_after_vw[index] for index in e4_r_rows
            )
            e4_r_candidates = (b[0], ell[6])
            e4_r_matrix, e4_r_rhs = sp.linear_eq_to_matrix(
                e4_r_equations, e4_r_candidates
            )
            print("INTERSECTION_E4_R_ROWS", e4_r_rows)
            print("INTERSECTION_E4_R_RANK", e4_r_matrix.rank())
            print(
                "INTERSECTION_E4_R_AUGMENTED_RANK",
                e4_r_matrix.row_join(e4_r_rhs).rank(),
            )
            for left in e4_r_matrix.T.nullspace():
                print(
                    "INTERSECTION_E4_R_COMPATIBILITY",
                    sp.factor((left.T * e4_r_rhs)[0]),
                )
            e4_r_rows_pivot = tuple(e4_r_matrix.T.rref()[1])
            e4_r_columns_pivot = tuple(e4_r_matrix.rref()[1])
            e4_r_pivot = sp.factor(
                e4_r_matrix.extract(
                    e4_r_rows_pivot, e4_r_columns_pivot
                ).det()
            )
            print("INTERSECTION_E4_R_PIVOT_ROWS", e4_r_rows_pivot)
            print("INTERSECTION_E4_R_PIVOT_COLUMNS", e4_r_columns_pivot)
            print("INTERSECTION_E4_R_PIVOT", e4_r_pivot)

            e4_r_pivot_variables = tuple(
                e4_r_candidates[index] for index in e4_r_columns_pivot
            )
            e4_r_solution_vector = e4_r_matrix.extract(
                e4_r_rows_pivot, e4_r_columns_pivot
            ).inv() * e4_r_rhs.extract(e4_r_rows_pivot, (0,))
            e4_r_solution = dict(
                zip(e4_r_pivot_variables, map(sp.cancel, e4_r_solution_vector))
            )
            assert all(
                sp.cancel(equation.subs(e4_r_solution)) == 0
                for equation in e4_r_equations
            )
            print("INTERSECTION_E4_R_VARIABLES", e4_r_pivot_variables)
            for variable in e4_r_pivot_variables:
                print(
                    "INTERSECTION_E4_R_SOLUTION",
                    variable,
                    e4_r_solution[variable],
                )

            e4_after_r = [
                sp.cancel(value.subs(e4_r_solution)) for value in e4_after_vw
            ]
            e4_non_r_rows = tuple(
                index
                for index, monomial in enumerate(monomials4)
                if sp.degree(monomial, r) == 0 and e4_after_r[index] != 0
            )
            e4_non_r_equations = tuple(
                e4_after_r[index] for index in e4_non_r_rows
            )
            e4_non_r_candidates = (
                a[0],
                a[3],
                b[1],
                b[3],
                ell[0],
                ell[1],
                ell[3],
                ell[4],
                ell[7],
            )
            e4_non_r_matrix, e4_non_r_rhs = sp.linear_eq_to_matrix(
                e4_non_r_equations, e4_non_r_candidates
            )
            print("INTERSECTION_E4_NONR_ROWS", e4_non_r_rows)
            print(
                "INTERSECTION_E4_NONR_RANK",
                e4_non_r_matrix.rank(),
            )
            print(
                "INTERSECTION_E4_NONR_AUGMENTED_RANK",
                e4_non_r_matrix.row_join(e4_non_r_rhs).rank(),
            )
            for left in e4_non_r_matrix.T.nullspace():
                print(
                    "INTERSECTION_E4_NONR_COMPATIBILITY",
                    sp.factor((left.T * e4_non_r_rhs)[0]),
                )

            e4_non_r_rows_pivot = tuple(e4_non_r_matrix.T.rref()[1])
            e4_non_r_columns_pivot = tuple(e4_non_r_matrix.rref()[1])
            e4_non_r_pivot = sp.factor(
                e4_non_r_matrix.extract(
                    e4_non_r_rows_pivot, e4_non_r_columns_pivot
                ).det()
            )
            print(
                "INTERSECTION_E4_NONR_PIVOT_ROWS",
                e4_non_r_rows_pivot,
            )
            print(
                "INTERSECTION_E4_NONR_PIVOT_COLUMNS",
                e4_non_r_columns_pivot,
            )
            print("INTERSECTION_E4_NONR_PIVOT", e4_non_r_pivot)
            e4_non_r_variables = tuple(
                e4_non_r_candidates[index]
                for index in e4_non_r_columns_pivot
            )
            e4_non_r_free_columns = tuple(
                index
                for index in range(len(e4_non_r_candidates))
                if index not in e4_non_r_columns_pivot
            )
            e4_non_r_solution_vector = e4_non_r_matrix.extract(
                e4_non_r_rows_pivot, e4_non_r_columns_pivot
            ).inv() * (
                e4_non_r_rhs.extract(e4_non_r_rows_pivot, (0,))
                - e4_non_r_matrix.extract(
                    e4_non_r_rows_pivot, e4_non_r_free_columns
                )
                * sp.Matrix(
                    [
                        e4_non_r_candidates[index]
                        for index in e4_non_r_free_columns
                    ]
                )
            )
            e4_non_r_solution = dict(
                zip(
                    e4_non_r_variables,
                    map(sp.cancel, e4_non_r_solution_vector),
                )
            )
            assert all(
                sp.cancel(equation.subs(e4_non_r_solution)) == 0
                for equation in e4_non_r_equations
            )
            print("INTERSECTION_E4_NONR_VARIABLES", e4_non_r_variables)

            # The preceding pivot divides by
            # V=v1-2*v2+3*v3.  Recompute its V=0 boundary from the unsolved
            # E4 system.
            v_linear = v[1] - 2 * v[2] + 3 * v[3]
            v1_boundary = {v[1]: 2 * v[2] - 3 * v[3]}
            e4_boundary_equations = tuple(
                sp.cancel(equation.subs(v1_boundary))
                for equation in e4_non_r_equations
            )
            boundary_matrix, boundary_rhs = sp.linear_eq_to_matrix(
                e4_boundary_equations, e4_non_r_candidates
            )
            boundary_rank = boundary_matrix.rank()
            print("INTERSECTION_E4_V0_RANK", boundary_rank)
            print(
                "INTERSECTION_E4_V0_AUGMENTED_RANK",
                boundary_matrix.row_join(boundary_rhs).rank(),
            )
            for left in boundary_matrix.T.nullspace():
                print(
                    "INTERSECTION_E4_V0_COMPATIBILITY",
                    sp.factor((left.T * boundary_rhs)[0]),
                )

            boundary_solution = {}
            if boundary_rank:
                boundary_rows = tuple(boundary_matrix.T.rref()[1])
                boundary_columns = tuple(boundary_matrix.rref()[1])
                boundary_pivot = sp.factor(
                    boundary_matrix.extract(
                        boundary_rows, boundary_columns
                    ).det()
                )
                boundary_variables = tuple(
                    e4_non_r_candidates[index]
                    for index in boundary_columns
                )
                boundary_free_columns = tuple(
                    index
                    for index in range(len(e4_non_r_candidates))
                    if index not in boundary_columns
                )
                boundary_solution_vector = boundary_matrix.extract(
                    boundary_rows, boundary_columns
                ).inv() * (
                    boundary_rhs.extract(boundary_rows, (0,))
                    - boundary_matrix.extract(
                        boundary_rows, boundary_free_columns
                    )
                    * sp.Matrix(
                        [
                            e4_non_r_candidates[index]
                            for index in boundary_free_columns
                        ]
                    )
                )
                boundary_solution = dict(
                    zip(
                        boundary_variables,
                        map(sp.cancel, boundary_solution_vector),
                    )
                )
                assert all(
                    sp.cancel(equation.subs(boundary_solution)) == 0
                    for equation in e4_boundary_equations
                )
                print("INTERSECTION_E4_V0_PIVOT", boundary_pivot)
                print("INTERSECTION_E4_V0_VARIABLES", boundary_variables)

            boundary_substitutions = (
                solved["solution"],
                stage1_solution,
                stage2_solution,
                v0_solution,
                u1_solution,
                e4_r_solution,
                v1_boundary,
                boundary_solution,
            )

            def descend_boundary(expression):
                value = expression
                for substitution in boundary_substitutions:
                    value = value.subs(substitution)
                return sp.cancel(value)

            print(
                "INTERSECTION_DET_L_V0_AFTER_E4",
                sp.factor(descend_boundary(sp.Matrix(3, 3, data["ell"]).det())),
            )
            assert all(descend_boundary(value) == 0 for value in e4_raw)
            assert descend_boundary(sp.Matrix(3, 3, data["ell"]).det()) == 0

            all_descent_substitutions = (
                solved["solution"],
                stage1_solution,
                stage2_solution,
                v0_solution,
                u1_solution,
                e4_r_solution,
                e4_non_r_solution,
            )

            def descend(expression):
                value = expression
                for substitution in all_descent_substitutions:
                    value = value.subs(substitution)
                return sp.cancel(value)

            e3_raw = coefficients(
                determinant.coeff_monomial(w**3).subs(k, 0), 3
            )
            e3_residuals = [descend(value) for value in e3_raw]
            assert all(descend(value) == 0 for value in e4_raw)
            assert descend(sp.Matrix(3, 3, data["ell"]).det()) == 0
            monomials3 = homogeneous_monomials(3)
            print(
                "INTERSECTION_E3_NONZERO",
                sum(value != 0 for value in e3_residuals),
            )
            for monomial, value in zip(monomials3, e3_residuals):
                if value == 0:
                    continue
                print(
                    "E3_PROFILE",
                    monomial,
                    "OPS",
                    sp.count_ops(value),
                    "UNKNOWNS",
                    len(value.free_symbols & all_unknowns),
                )
                if sp.count_ops(value) <= 200:
                    print("E3_SMALL", monomial, sp.factor(value))

            for lower_weight in (2, 1):
                lower_raw = coefficients(
                    determinant.coeff_monomial(w**lower_weight).subs(k, 0),
                    lower_weight,
                )
                lower_residuals = [descend(value) for value in lower_raw]
                print(
                    f"INTERSECTION_E{lower_weight}_NONZERO",
                    sum(value != 0 for value in lower_residuals),
                )
                for monomial, value in zip(
                    homogeneous_monomials(lower_weight), lower_residuals
                ):
                    if value != 0:
                        print(
                            f"E{lower_weight}_FORMULA",
                            monomial,
                            sp.factor(value),
                        )
            print(
                "INTERSECTION_DET_L_AFTER_GENERIC_DESCENT",
                sp.factor(descend(sp.Matrix(3, 3, data["ell"]).det())),
            )
            print("D4_DN3_CLEANROOM_INTERSECTION_DETL_PASS")
            return

    if chart == "origin":
        e4_raw = coefficients(
            determinant.coeff_monomial(w**4).subs({k: 0, s: 0}), 4
        )
        e4_after_e6 = [
            sp.cancel(value.subs(solved["solution"])) for value in e4_raw
        ]
        b4 = data["b"][4]
        l8 = data["ell"][8]
        selected_origin = []
        for monomial, value in zip(
            homogeneous_monomials(4), e4_after_e6
        ):
            if value == 0:
                continue
            unknown_symbols = value.free_symbols & all_unknowns
            if unknown_symbols <= {b4, l8}:
                selected_origin.append((monomial, sp.factor(value)))
        print("ORIGIN_E4_SELECTED_COUNT", len(selected_origin))
        for monomial, value in selected_origin:
            print("ORIGIN_E4_SELECTED", monomial, value)
        assert dict(selected_origin)[p**3 * r] == 3 * b4**2
        assert dict(selected_origin)[q**3 * r] == (3 * b4 - 4 * l8) ** 2 / 3
        forced_origin = {b4: 0, l8: 0}
        assert all(
            sp.factor(value.subs(forced_origin)) == 0
            for value in solved["solution"].values()
        )
        print("ORIGIN_ALL_SIX_NONBINARY_QUADRATICS_ZERO")
        print("D4_DN3_CLEANROOM_ORIGIN_MOH_EXIT_PASS")
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sign", choices=("plus", "minus"), default="plus")
    parser.add_argument(
        "--chart",
        choices=("interior", "intersection", "origin"),
        default="interior",
    )
    args = parser.parse_args()

    root = (-4 + (2 if args.sign == "plus" else -2) * sqrt2) / 3
    data = build(root)
    solved = solve_chart(data, args.chart)
    summarize_lower(data, solved, args.chart)


if __name__ == "__main__":
    main()
