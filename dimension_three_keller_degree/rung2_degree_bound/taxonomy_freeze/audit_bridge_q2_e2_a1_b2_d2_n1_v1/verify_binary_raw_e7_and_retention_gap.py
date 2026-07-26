#!/usr/bin/env python3
"""Retain the last certified binary step and locate the first exact gap.

The raw E7 calculation below starts with all 12 coefficients of V, all 18
coefficients of H2, and all six tangent parameters in the degree-eight
normal form from the working note.  It verifies the forcing in equation
(6).  A syntax-tree audit then confirms that the upstream E6 regressions
evaluate only a specialized particular solution, not the universal E6
compatibility needed to prove equations (7)--(9) exhaustive.

Exit zero means that this audit result was reproduced.  It does *not* mean
that the proposed global bridge passed.
"""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RUNG2 = HERE.parent.parent
SYMPY_CHECKER = RUNG2 / "verify_fixed_conic_row_sympy.py"
PARI_CHECKER = RUNG2 / "verify_fixed_conic_row_pari.gp"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def jacobian(vector: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    return vector.jacobian(variables)


def coefficient_equations(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
) -> list[sp.Expr]:
    return [
        coefficient
        for _, coefficient in sp.Poly(
            sp.expand(expression), *variables
        ).terms()
    ]


def contains_constant_multiple(
    expressions: list[sp.Expr],
    target: sp.Expr,
) -> bool:
    for expression in expressions:
        quotient = sp.cancel(expression / target)
        if quotient.is_number and quotient != 0:
            return True
    return False


def raw_e7_compatibility(
    h: sp.Expr,
    H3: sp.Matrix,
    H2: sp.Matrix,
    h2_symbols: tuple[sp.Symbol, ...],
    variables: tuple[sp.Symbol, ...],
    A: sp.Matrix,
) -> tuple[int, list[sp.Expr]]:
    C = jacobian(h * A, variables)
    E7 = sp.expand(
        sp.trace(C.adjugate() * jacobian(H2, variables))
        + sp.trace(jacobian(H3, variables).adjugate() * C)
    )
    equations = coefficient_equations(E7, variables)
    matrix, rhs = sp.linear_eq_to_matrix(equations, h2_symbols)
    compatibility = [
        sp.factor((left.T * rhs)[0])
        for left in matrix.T.nullspace()
        if sp.factor((left.T * rhs)[0]) != 0
    ]
    return matrix.rank(), compatibility


def assigned_expression(tree: ast.AST, target_name: str) -> str:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == target_name
            for target in node.targets
        ):
            return ast.unparse(node.value)
    raise AssertionError(f"assignment {target_name} not found")


def load_count(tree: ast.AST, name: str) -> int:
    return sum(
        isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id == name
        for node in ast.walk(tree)
    )


def main() -> None:
    p, q, r = sp.symbols("p q r")
    variables = (p, q, r)
    A = sp.Matrix([p**2, p*q, q**2])
    Ap = A.diff(p)
    Aq = A.diff(q)

    # Full degree-eight binary normal: 12+18 lower coefficients and six
    # tangent parameters, with no computational pivot suppressed.
    v = sp.symbols("v0:12")
    w = sp.symbols("w0:18")
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    cubic_binary = (p**3, p**2*q, p*q**2, q**3)
    quadratic_ternary = (p**2, p*q, q**2, p*r, q*r, r**2)
    V = sp.Matrix([
        sum(v[4*i+j] * cubic_binary[j] for j in range(4))
        for i in range(3)
    ])
    H2 = sp.Matrix([
        sum(w[6*i+j] * quadratic_ternary[j] for j in range(6))
        for i in range(3)
    ])
    H3 = (
        V
        + r*((a*p+b*q)*Ap + (c*p+d*q)*Aq)
        + sp.Rational(1, 2)*r**2*(e*Ap+f*Aq)
    )
    require(len(v) == 12 and len(w) == 18,
            "arbitrary lower-term coefficient counts changed")

    split_rank, split_compatibility = raw_e7_compatibility(
        p*q, H3, H2, w, variables, A
    )
    require(split_rank == 7, "unexpected split E7 H2 rank")
    require(contains_constant_multiple(split_compatibility, e**2),
            "split E7 does not force e=0")
    require(contains_constant_multiple(split_compatibility, f**2),
            "split E7 does not force f=0")
    split_after_ef = [
        sp.factor(item.subs({e: 0, f: 0}))
        for item in split_compatibility
    ]
    require(contains_constant_multiple(split_after_ef, b**2),
            "split E7 does not force b=0")
    require(contains_constant_multiple(split_after_ef, c**2),
            "split E7 does not force c=0")

    double_rank, double_compatibility = raw_e7_compatibility(
        p**2, H3, H2, w, variables, A
    )
    require(double_rank == 7, "unexpected double-root E7 H2 rank")
    require(contains_constant_multiple(double_compatibility, e**2),
            "double-root E7 does not force e=0")
    require(contains_constant_multiple(double_compatibility, f**2),
            "double-root E7 does not force f=0")
    double_after_ef = [
        sp.factor(item.subs({e: 0, f: 0}))
        for item in double_compatibility
    ]
    require(contains_constant_multiple(double_after_ef, b**2),
            "double-root E7 does not force b=0")

    # Inspect what the proposed exact E6 regression actually evaluates.
    source = SYMPY_CHECKER.read_text()
    tree = ast.parse(source)
    split_expression = assigned_expression(tree, "split_weighted")
    double_expression = assigned_expression(tree, "double_weighted")
    for label, expression in (
        ("split", split_expression),
        ("double", double_expression),
    ):
        require("V_general" not in expression,
                f"{label} E6 unexpectedly uses arbitrary V")
        require("H2_general" not in expression,
                f"{label} E6 unexpectedly uses arbitrary H2")
        require("sp.zeros(3)" in expression,
                f"{label} E6 regression shape changed")
    require(load_count(tree, "H2_general") == 0,
            "upstream H2_general is now used; redo this audit")

    pari = PARI_CHECKER.read_text()
    require(
        "splitBranch = matdet(s*jacmap(r^2*splitZ)"
        "+s^2*jacmap(r*splitW)+s^3*jacmap(splitH4));" in pari,
        "PARI split specialization changed",
    )
    require(
        "doubleBranch = matdet(s*jacmap(r^2*doubleZ)"
        "+s^2*jacmap(r*doubleW)+s^3*jacmap(doubleH4));" in pari,
        "PARI double specialization changed",
    )

    print("PASS independent raw binary E7: equation (6) is forced")
    print("PASS exact source audit: both E6 regressions use only a particular")
    print("FAIL-CLOSED global bridge: no retained universal E6 compatibility")
    print("GAP equations (7)--(9) are not certified for arbitrary V and H2")


if __name__ == "__main__":
    main()
