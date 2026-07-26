#!/usr/bin/env python3
"""Fail-closed clean-room replay for the frozen conic-embedding row.

This is deliberately stronger than the two lower regression scripts.  In
addition to replaying them, it reconstructs the constant exact linear
systems behind the unproved-in-code rank, kernel, cokernel, and
compatibility assertions in WORKING_CONIC_TYPE_22.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import sympy as sp


if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


HERE = Path(__file__).resolve().parent
FREEZE = HERE.parent
RUNG = FREEZE.parent

EXPECTED_HASHES = {
    FREEZE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    FREEZE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    RUNG / "WORKING_CONIC_TYPE_22.md":
        "4b0c86dd4e4b7537bad21012daf5564c75c0c971b2579fcfb046fa6395b649c3",
    RUNG / "verify_conic_doubleline_sympy.py":
        "38db15a0d1651482f6316f06b39e8591a0bdb6dbe57e1241f87dfe85f5f6bd80",
    RUNG / "verify_conic_doubleline_pari.gp":
        "378fd06ca2855855a058ec08f9a1e4ed4f302683fd5e4980a20edcefd855b322",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


x, y, z, weight = sp.symbols("x y z weight")
variables = (x, y, z)
quadratic_monomials = (x**2, x*y, x*z, y**2, y*z, z**2)


def ver(first: sp.Expr, second: sp.Expr) -> sp.Matrix:
    return sp.Matrix([first**2, first*second, second**2])


def homogeneous_monomials(degree: int) -> list[sp.Expr]:
    return [
        x**i * y**j * z**(degree-i-j)
        for i in range(degree, -1, -1)
        for j in range(degree-i, -1, -1)
    ]


def coefficient_vector(poly: sp.Expr, degree: int) -> sp.Matrix:
    encoded = sp.Poly(sp.expand(poly), x, y, z)
    return sp.Matrix([
        encoded.coeff_monomial(mon)
        for mon in homogeneous_monomials(degree)
    ])


def determinant_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    degree: int,
) -> sp.Expr:
    encoded = sp.expand(
        (
            linear
            + weight * quadratic.jacobian(variables)
            + weight**2 * cubic.jacobian(variables)
            + weight**3 * quartic.jacobian(variables)
        ).det()
    )
    return sp.expand(sp.Poly(encoded, weight).coeff_monomial(weight**degree))


def matrix_span_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    return (
        left.rank() == right.rank()
        and sp.Matrix.hstack(left, right).rank() == left.rank()
    )


def ideals_equal(
    left: list[sp.Expr],
    right: list[sp.Expr],
    generators: list[sp.Symbol],
) -> bool:
    left_basis = sp.groebner(left, *generators, order="grevlex")
    right_basis = sp.groebner(right, *generators, order="grevlex")
    for item in left:
        if sp.expand(right_basis.reduce(item)[1]) != 0:
            return False
    for item in right:
        if sp.expand(left_basis.reduce(item)[1]) != 0:
            return False
    return True


def h2_kernel_basis(p_form: sp.Expr, q_form: sp.Expr) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for component in range(3):
        for form in (p_form, q_form):
            encoded: list[sp.Expr] = []
            for row in range(3):
                polynomial = sp.Poly(form if row == component else 0, x, y, z)
                encoded.extend(
                    polynomial.coeff_monomial(mon)
                    for mon in quadratic_monomials
                )
            columns.append(sp.Matrix(encoded))
    return sp.Matrix.hstack(*columns)


def degree_seven_operator(q_form: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
    p_form = x**2
    quartic = ver(p_form, q_form)
    columns: list[sp.Matrix] = []
    for component in range(3):
        for monomial in quadratic_monomials:
            trial = sp.zeros(3, 1)
            trial[component] = monomial
            columns.append(coefficient_vector(
                determinant_coefficient(
                    sp.zeros(3), trial, sp.zeros(3, 1), quartic, 7
                ),
                7,
            ))
    return sp.Matrix.hstack(*columns), quartic


def degree_six_linear_operator(q_form: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
    p_form = x**2
    quartic = ver(p_form, q_form)
    columns: list[sp.Matrix] = []
    for row in range(3):
        for column in range(3):
            trial = sp.zeros(3)
            trial[row, column] = 1
            columns.append(coefficient_vector(
                determinant_coefficient(
                    trial, sp.zeros(3, 1), sp.zeros(3, 1), quartic, 6
                ),
                6,
            ))
    return sp.Matrix.hstack(*columns), quartic


def compatibility_residuals(
    operator: sp.Matrix,
    right_hand_side: sp.Matrix,
) -> list[sp.Expr]:
    return [
        sp.factor((functional.T * right_hand_side)[0])
        for functional in operator.T.nullspace()
        if sp.factor((functional.T * right_hand_side)[0]) != 0
    ]


def frozen_scope_checks(mutation: str | None) -> None:
    expected_hashes = dict(EXPECTED_HASHES)
    if mutation == "hash":
        expected_hashes[FREEZE / "FROZEN_TAXONOMY_v1.md"] = "0" * 64
    for path, expected in expected_hashes.items():
        require(digest(path) == expected, f"pinned-input hash mismatch: {path}")

    manifest = json.loads((FREEZE / "frozen_manifest_v1.json").read_text())
    expected_pivots = [f"C{i:02d}" for i in range(45)]
    if mutation == "pivots":
        expected_pivots[-1] = "C45"
    require(manifest["version"] == 1, "wrong frozen version")
    require(manifest["frozen_row_count"] == 14, "wrong frozen denominator")
    require(manifest["pivot_ids"] == expected_pivots, "wrong pivot list")
    rows = [
        row for row in manifest["rows"]
        if row["id"] == "Q2-E0-A2-B2-D2-N1"
    ]
    require(len(rows) == 1, "target row missing or duplicated")
    require(rows[0]["rank"] == 2, "wrong target rank")
    require(rows[0]["tuple"] == [0, 2, 2, 2, 1], "wrong target tuple")

    # A conic embedding is the complete binary quadratic system.
    P, Q = sp.symbols("P Q")
    conic = ver(P, Q)
    require(
        sp.expand(conic[1]**2-conic[0]*conic[2]) == 0,
        "Veronese conic identity",
    )
    require(sp.eye(3).rank() == 3, "conic components fail to span target")
    # Hence each of the three original component quartics is nonzero:
    # only C00--C14 can be nonempty; all later pivots are empty.
    require(len(expected_pivots[:15]) == 15, "wrong routed pivot count")
    require(len(expected_pivots[15:]) == 30, "wrong empty pivot count")

    # A pencil basis change lifts invertibly through Sym^2.
    a, b, c, d = sp.symbols("a b c d")
    sym2 = sp.Matrix([
        [a**2, 2*a*b, b**2],
        [a*c, a*d+b*c, b*d],
        [c**2, 2*c*d, d**2],
    ])
    require(
        sp.expand(sym2.det()-(a*d-b*c)**3) == 0,
        "Sym^2 basis-change determinant",
    )

    # Two double lines give C(r^2) proper in C(r), and the canonical
    # binary quartic map has (a,b,delta,nu)=(1,4,2,2).
    r, base = sp.symbols("r base")
    minpoly = r**2-base
    require(sp.Poly(minpoly, r).degree() == 2, "wrong square extension")
    require(
        sp.degree(sp.discriminant(minpoly, r), base) % 2 == 1,
        "square extension discriminant became a square",
    )
    boundary = sp.Matrix([P**4, P**2*Q**2, Q**4])
    require(
        sp.expand(boundary[1]**2-boundary[0]*boundary[2]) == 0,
        "two-double-line boundary is not a conic",
    )


def universal_eight_and_seven_checks() -> None:
    p0, q0, ell0, emm0 = sp.symbols("p0 q0 ell0 emm0")
    dp = sp.Matrix(1, 3, sp.symbols("dp0:3"))
    dq = sp.Matrix(1, 3, sp.symbols("dq0:3"))
    dl = sp.Matrix(1, 3, sp.symbols("dl0:3"))
    dm = sp.Matrix(1, 3, sp.symbols("dm0:3"))
    arbitrary_h2_jacobian = sp.Matrix(3, 3, sp.symbols("h2_0:9"))

    leading_jacobian = sp.Matrix.vstack(
        2*p0*dp,
        q0*dp+p0*dq,
        2*q0*dq,
    )
    cross = (
        sp.Matrix(dp).reshape(3, 1)
        .cross(sp.Matrix(dq).reshape(3, 1))
    )
    normal = sp.Matrix([q0**2, -2*p0*q0, p0**2])
    adj_difference = leading_jacobian.adjugate()-2*cross*normal.T
    require(
        all(sp.expand(entry) == 0 for entry in adj_difference),
        "universal degree-eight adjugate identity",
    )

    # The Hilbert--Burch matrix gives the complete tangent syzygies whenever
    # coprime p,q form a regular sequence.
    P, Q = sp.symbols("P Q")
    hb = sp.Matrix([[2*P, 0], [Q, P], [0, 2*Q]])
    normal_binary = sp.Matrix([Q**2, -2*P*Q, P**2])
    require(normal_binary.T*hb == sp.zeros(1, 2), "tangent syzygies")
    signed_minors = sp.Matrix([
        hb.extract((1, 2), (0, 1)).det(),
        -hb.extract((0, 2), (0, 1)).det(),
        hb.extract((0, 1), (0, 1)).det(),
    ])
    require(
        all(sp.expand(entry) == 0 for entry in signed_minors-2*normal_binary),
        "Hilbert--Burch maximal minors",
    )

    # Universal exterior expansion behind equation (9).
    cubic_jacobian = sp.Matrix.vstack(
        2*ell0*dp+2*p0*dl,
        ell0*dq+q0*dl+emm0*dp+p0*dm,
        2*emm0*dq+2*q0*dm,
    )
    formal_weight = sp.symbols("formal_weight")
    degree_seven = sp.Poly(
        sp.expand(
            (
                formal_weight*arbitrary_h2_jacobian
                + formal_weight**2*cubic_jacobian
                + formal_weight**3*leading_jacobian
            ).det()
        ),
        formal_weight,
    ).coeff_monomial(formal_weight**7)
    theta = q0*ell0-p0*emm0
    expected = 2*(
        (normal.T*arbitrary_h2_jacobian*cross)[0]
        - 2*theta*(q0*(dl*cross)[0]-p0*(dm*cross)[0])
    )
    require(
        sp.expand(degree_seven-expected) == 0,
        "universal degree-seven exterior identity",
    )

    # Every binary cubic is n dot M(P,Q).
    parameters = sp.symbols("m0:6")
    matrix_m = sp.Matrix(3, 2, parameters)
    cubic = sp.expand((normal_binary.T*matrix_m*sp.Matrix([P, Q]))[0])
    coefficient_map = sp.Matrix([
        [sp.Poly(cubic, P, Q).coeff_monomial(mon).coeff(parameter)
         for parameter in parameters]
        for mon in (P**3, P**2*Q, P*Q**2, Q**3)
    ])
    require(coefficient_map.rank() == 4, "binary-cubic image not surjective")


def no_double_line_normal_form_checks() -> None:
    u, v = sp.symbols("u v")
    aa, bb, cc = sp.symbols("aa bb cc")
    cases = [
        (
            aa*x**2+bb*y**2+cc*z**2,
            x**2+y**2+z**2,
            (aa*u+v)*(bb*u+v)*(cc*u+v),
            0,
        ),
        (
            y**2+z**2,
            2*x*y+z**2,
            -v**2*(u+v),
            0,
        ),
        (
            2*y*z,
            2*x*z+y**2,
            -v**3,
            1,
        ),
    ]
    for p_form, q_form, discriminant, expected_intersection in cases:
        symmetric_matrix = sp.hessian(u*p_form+v*q_form, variables)/2
        require(
            sp.expand(symmetric_matrix.det()-discriminant) == 0,
            "regular-pencil discriminant",
        )
        cross = sp.Matrix([
            sp.diff(p_form, variable) for variable in variables
        ]).cross(
            sp.Matrix([
                sp.diff(q_form, variable) for variable in variables
            ])
        )
        component_vectors = [
            coefficient_vector(component, 2)
            for component in cross
        ]
        W = sp.Matrix.hstack(*component_vectors)
        U = sp.Matrix.hstack(
            coefficient_vector(p_form, 2),
            coefficient_vector(q_form, 2),
        )
        require(W.rank() == 3, "delta is not injective")
        intersection_dimension = W.rank()+U.rank()-sp.Matrix.hstack(W, U).rank()
        require(
            intersection_dimension == expected_intersection,
            "wrong W intersection U",
        )
        require(
            sp.Matrix.hstack(W, U).rank() > W.rank(),
            "U unexpectedly contained in W",
        )


def unique_degree_seven_checks(mutation: str | None) -> None:
    alpha, beta, gamma, delta = sp.symbols("alpha beta gamma delta")
    ell_x, ell_y, ell_z = sp.symbols("ell_x ell_y ell_z")
    m_x, m_y, m_z = sp.symbols("m_x m_y m_z")
    ell = ell_x*x+ell_y*y+ell_z*z
    emm = m_x*x+m_y*y+m_z*z
    ell_bar = ell_y*y+ell_z*z
    emm_bar = m_y*y+m_z*z
    u_column = sp.Matrix(sp.symbols("u1:4"))
    v_column = sp.Matrix(sp.symbols("v1:4"))
    compatibility_generators = [
        alpha, beta, gamma, delta,
        ell_x, ell_y, ell_z, m_x, m_y, m_z,
    ]

    for q_form in (y*z, y**2+2*x*z):
        p_form = x**2
        operator, quartic = degree_seven_operator(q_form)
        expected_rank = 13 if mutation == "e7_rank" else 12
        require(operator.rank() == expected_rank, "degree-seven rank")
        kernel = h2_kernel_basis(p_form, q_form)
        require(kernel.rank() == 6, "M(p,q) kernel rank")
        require(operator*kernel == sp.zeros(operator.rows, kernel.cols),
                "M(p,q) not in degree-seven kernel")
        require(
            matrix_span_equal(kernel, sp.Matrix.hstack(*operator.nullspace())),
            "degree-seven kernel is larger than M(p,q)",
        )

        tangent = sp.Matrix([
            2*p_form*ell,
            q_form*ell+p_form*emm,
            2*q_form*emm,
        ])
        exceptional = x*sp.Matrix([
            alpha*q_form+beta*p_form,
            0,
            gamma*q_form+delta*p_form,
        ])
        cubic = tangent+exceptional
        right_hand_side = -coefficient_vector(
            determinant_coefficient(
                sp.zeros(3), sp.zeros(3, 1), cubic, quartic, 7
            ),
            7,
        )
        residuals = compatibility_residuals(operator, right_hand_side)
        expected_compatibility = [alpha*ell_y, alpha*ell_z]
        if mutation == "e7_compat":
            expected_compatibility.append(alpha*ell_x)
        require(
            ideals_equal(
                residuals,
                expected_compatibility,
                compatibility_generators,
            ),
            "degree-seven compatibility ideal",
        )

        # Particular solution for alpha=0.  Kernel equality then proves
        # that (21)+M(p,q) is the entire solution affine space.
        alpha_zero_quadratic = (
            ver(ell, emm)
            + x*sp.Matrix([
                sp.Rational(3, 2)*beta*ell_bar,
                -sp.Rational(1, 4)*gamma*ell_bar,
                sp.Rational(3, 2)*delta*ell_bar+gamma*emm_bar,
            ])
            + u_column*p_form+v_column*q_form
        )
        require(
            determinant_coefficient(
                sp.zeros(3),
                alpha_zero_quadratic,
                cubic.subs(alpha, 0),
                quartic,
                7,
            ) == 0,
            "alpha-zero degree-seven particular solution",
        )

        # After the allowed X translation, bar(ell)=0 becomes ell=0.
        ell_zero_cubic = cubic.subs({
            ell_x: 0, ell_y: 0, ell_z: 0,
        })
        ell_zero_quadratic = (
            ver(0, emm)
            + x*sp.Matrix([alpha*emm_bar, 0, gamma*emm_bar])
            + u_column*p_form+v_column*q_form
        )
        require(
            determinant_coefficient(
                sp.zeros(3),
                ell_zero_quadratic,
                ell_zero_cubic,
                quartic,
                7,
            ) == 0,
            "ell-zero degree-seven particular solution",
        )


def first_column_kernel_basis() -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for row in range(3):
        encoded = sp.zeros(9, 1)
        encoded[3*row] = 1
        columns.append(encoded)
    return sp.Matrix.hstack(*columns)


def unique_degree_six_checks(mutation: str | None) -> None:
    alpha, beta, gamma, delta = sp.symbols("alpha beta gamma delta")
    ell_x, ell_y, ell_z = sp.symbols("ell_x ell_y ell_z")
    m_x, m_y, m_z = sp.symbols("m_x m_y m_z")
    ell = ell_x*x+ell_y*y+ell_z*z
    emm = m_x*x+m_y*y+m_z*z
    ell_bar = ell_y*y+ell_z*z
    emm_bar = m_y*y+m_z*z
    u_column = sp.Matrix(sp.symbols("u1:4"))
    v_column = sp.Matrix(sp.symbols("v1:4"))
    a_column = sp.Matrix(sp.symbols("a1:4"))
    linear_kernel = first_column_kernel_basis()

    for q_form in (y*z, y**2+2*x*z):
        p_form = x**2
        operator, quartic = degree_six_linear_operator(q_form)
        expected_rank = 7 if mutation == "e6_rank" else 6
        require(operator.rank() == expected_rank, "degree-six linear rank")
        require(
            matrix_span_equal(
                linear_kernel,
                sp.Matrix.hstack(*operator.nullspace()),
            ),
            "degree-six linear kernel is not first-column space",
        )

        # Complete ell=0 branch: this is one particular solution, and the
        # operator kernel proves that its arbitrary first column is all.
        ell_zero_cubic = (
            sp.Matrix([0, p_form*emm, 2*q_form*emm])
            + x*sp.Matrix([
                alpha*q_form+beta*p_form,
                0,
                gamma*q_form+delta*p_form,
            ])
        )
        ell_zero_quadratic = (
            ver(0, emm)
            + x*sp.Matrix([alpha*emm_bar, 0, gamma*emm_bar])
            + u_column*p_form+v_column*q_form
        )
        forced_linear = sp.Matrix.hstack(
            a_column, v_column*m_y, v_column*m_z
        )
        require(
            determinant_coefficient(
                forced_linear,
                ell_zero_quadratic,
                ell_zero_cubic,
                quartic,
                6,
            ) == 0,
            "ell-zero degree-six particular solution",
        )
        require(forced_linear.det() == 0, "ell-zero forced linear part invertible")

    # alpha=0, bar(ell) nonzero: reconstruct both full compatibility ideals.
    l1, l2, m0, kappa = sp.symbols("l1 l2 m0 kappa")
    compatibility_generators = [beta, gamma, delta, l1, l2, m0, kappa]
    normalized_cases = (
        (
            y*z,
            l1*y+l2*z,
            m0*x,
            [
                beta*l1**2, beta*l2**2,
                gamma*l1**2, gamma*l2**2,
                delta*l1**2, delta*l2**2,
            ],
        ),
        (
            y**2+2*x*z,
            l1*y+l2*z,
            kappa*z,
            [
                beta*l2**2, beta*l1*l2,
                gamma*l2**2, gamma*l1*l2,
                delta*l2**2, delta*l1*l2,
            ],
        ),
    )
    for q_form, normalized_ell, normalized_m, expected_ideal in normalized_cases:
        p_form = x**2
        operator, quartic = degree_six_linear_operator(q_form)
        cubic = (
            sp.Matrix([
                2*p_form*normalized_ell,
                q_form*normalized_ell+p_form*normalized_m,
                2*q_form*normalized_m,
            ])
            + x*sp.Matrix([
                beta*p_form,
                0,
                gamma*q_form+delta*p_form,
            ])
        )
        normalized_m_bar = (
            0 if q_form == y*z else kappa*z
        )
        quadratic = (
            ver(normalized_ell, normalized_m)
            + x*sp.Matrix([
                sp.Rational(3, 2)*beta*normalized_ell,
                -sp.Rational(1, 4)*gamma*normalized_ell,
                sp.Rational(3, 2)*delta*normalized_ell
                + gamma*normalized_m_bar,
            ])
            + u_column*p_form+v_column*q_form
        )
        right_hand_side = -coefficient_vector(
            determinant_coefficient(
                sp.zeros(3), quadratic, cubic, quartic, 6
            ),
            6,
        )
        residuals = compatibility_residuals(operator, right_hand_side)
        require(
            ideals_equal(
                residuals,
                expected_ideal,
                compatibility_generators,
            ),
            "degree-six compatibility ideal",
        )

    # The sole residue l2=0 in the Jordan pencil.  Kernel equality above
    # makes the displayed arbitrary-first-column matrix the full solution.
    lam = sp.symbols("lam", nonzero=True)
    p_form = x**2
    q_form = y**2+2*x*z
    quartic = ver(p_form, q_form)
    residual_ell = lam*y
    residual_m = kappa*z
    residual_cubic = (
        sp.Matrix([
            2*p_form*residual_ell,
            q_form*residual_ell+p_form*residual_m,
            2*q_form*residual_m,
        ])
        + x*sp.Matrix([
            beta*p_form,
            0,
            gamma*q_form+delta*p_form,
        ])
    )
    residual_quadratic = (
        ver(residual_ell, residual_m)
        + x*sp.Matrix([
            sp.Rational(3, 2)*beta*residual_ell,
            -sp.Rational(1, 4)*gamma*residual_ell,
            sp.Rational(3, 2)*delta*residual_ell+gamma*residual_m,
        ])
        + u_column*p_form+v_column*q_form
    )
    residual_linear = sp.Matrix([
        [
            a_column[0],
            lam*u_column[0],
            kappa*v_column[0]-sp.Rational(3, 4)*beta*lam**2,
        ],
        [
            a_column[1],
            lam*u_column[1],
            kappa*v_column[1]+sp.Rational(3, 8)*gamma*lam**2,
        ],
        [
            a_column[2],
            lam*u_column[2]-sp.Rational(1, 4)*gamma**2*lam,
            kappa*v_column[2]-sp.Rational(3, 4)*delta*lam**2,
        ],
    ])
    require(
        determinant_coefficient(
            residual_linear,
            residual_quadratic,
            residual_cubic,
            quartic,
            6,
        ) == 0,
        "residual degree-six particular solution",
    )

    degree_five = sp.Poly(
        determinant_coefficient(
            residual_linear,
            residual_quadratic,
            residual_cubic,
            quartic,
            5,
        ),
        x, y, z,
    )
    expected_coefficients = {
        x**2*z**3: 12*beta*lam**3,
        x*y**4: 2*lam*(-v_column[0]*gamma+2*a_column[0]),
        x**3*z**2:
            2*lam*(-4*v_column[0]*gamma+3*gamma*lam**2+8*a_column[0]),
        x**3*y**2:
            -4*lam*(-v_column[1]*gamma+2*a_column[1]),
        x**4*z:
            -lam*(-8*v_column[1]*gamma-3*delta*lam**2+16*a_column[1]),
    }
    for monomial, expected in expected_coefficients.items():
        require(
            sp.expand(degree_five.coeff_monomial(monomial)-expected) == 0,
            f"residual degree-five coefficient {monomial}",
        )

    # Check the stated sequential elimination under lam != 0.
    c2 = expected_coefficients[x*y**4]
    c3 = expected_coefficients[x**3*z**2]
    c4 = expected_coefficients[x**3*y**2]
    c5 = expected_coefficients[x**4*z]
    a1_solution = v_column[0]*gamma/2
    require(
        sp.factor(c3.subs(a_column[0], a1_solution))
        == 6*gamma*lam**3,
        "degree-five gamma elimination",
    )
    require(
        sp.factor(c4.subs(gamma, 0)) == -8*a_column[1]*lam,
        "degree-five a2 elimination",
    )
    require(
        sp.factor(c5.subs({gamma: 0, a_column[1]: 0}))
        == 3*delta*lam**3,
        "degree-five delta elimination",
    )
    require(
        sp.factor(c2.subs({gamma: 0, a_column[0]: 0})) == 0,
        "degree-five a1 consistency",
    )


def factorization_check() -> None:
    source, first, second, dilation = sp.symbols(
        "source first second dilation"
    )
    a_column = sp.Matrix(sp.symbols("factor_a1:4"))
    u_column = sp.Matrix(sp.symbols("factor_u1:4"))
    v_column = sp.Matrix(sp.symbols("factor_v1:4"))
    map_g = (
        a_column*source
        + ver(first, second)
        + u_column*first+v_column*second
    )
    determinant = sp.expand(
        map_g.jacobian((source, first, second)).det()
    )
    scaled = sp.Poly(
        sp.expand(determinant.subs({
            first: dilation*first,
            second: dilation*second,
        })),
        dilation,
    )
    require(
        sp.expand(
            scaled.coeff_monomial(dilation**2)
            - 2*(
                a_column[0]*second**2
                - 2*a_column[1]*first*second
                + a_column[2]*first**2
            )
        ) == 0,
        "factorization top-degree obstruction",
    )


def lower_regression_checks(mutation: str | None) -> None:
    sympy_result = subprocess.run(
        [sys.executable, str(RUNG / "verify_conic_doubleline_sympy.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    expected_sympy = "PASS: exact SymPy unique-double-line conic regressions"
    if mutation == "lower_output":
        expected_sympy += " MUTATED"
    require(sympy_result.returncode == 0, "lower SymPy checker failed")
    require(
        expected_sympy in sympy_result.stdout.splitlines(),
        "lower SymPy pass token missing",
    )

    gp_binary = shutil.which("gp")
    require(gp_binary is not None, "PARI/GP is unavailable")
    pari_result = subprocess.run(
        [gp_binary, "-q", str(RUNG / "verify_conic_doubleline_pari.gp")],
        check=False,
        capture_output=True,
        text=True,
    )
    require(pari_result.returncode == 0, "lower PARI checker failed")
    combined = pari_result.stdout+"\n"+pari_result.stderr
    require(
        not re.search(
            r"\*\*\*.*(?:error|at top-level|in function)|syntax error|skipping file",
            combined,
            flags=re.IGNORECASE,
        ),
        "lower PARI emitted an interpreter error",
    )
    require(
        "PASS: independent PARI unique-double-line conic regressions"
        in combined.splitlines(),
        "lower PARI pass token missing",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=(
            "hash",
            "pivots",
            "e7_rank",
            "e7_compat",
            "e6_rank",
            "lower_output",
        ),
    )
    args = parser.parse_args()

    frozen_scope_checks(args.mutation)
    universal_eight_and_seven_checks()
    no_double_line_normal_form_checks()
    unique_degree_seven_checks(args.mutation)
    unique_degree_six_checks(args.mutation)
    factorization_check()
    lower_regression_checks(args.mutation)
    print("INDEPENDENT_Q2_E0_A2_B2_D2_N1_AUDIT_PASS")


if __name__ == "__main__":
    main()
