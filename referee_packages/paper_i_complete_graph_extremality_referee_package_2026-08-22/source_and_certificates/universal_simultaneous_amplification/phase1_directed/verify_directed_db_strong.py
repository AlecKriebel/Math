"""Exact checks for the directed complete-support dB strong-selection term.

Convention: W[u][v] is the weight from reproducing source u to dead target v.
All calculations use SymPy expressions over QQ(r); no floating point is used.
"""

from __future__ import annotations

from itertools import combinations
from typing import Sequence

import sympy as sp


R = sp.symbols("r", positive=True)


def _exact_matrix(weights: Sequence[Sequence[object]]) -> tuple[tuple[sp.Expr, ...], ...]:
    matrix = tuple(tuple(sp.sympify(value) for value in row) for row in weights)
    n = len(matrix)
    if n < 2 or any(len(row) != n for row in matrix):
        raise ValueError("weights must be a square matrix of order at least two")
    for u in range(n):
        if matrix[u][u] != 0:
            raise ValueError("diagonal weights must vanish")
        for v in range(n):
            if u != v and matrix[u][v].is_positive is not True:
                raise ValueError("this verifier requires complete positive support")
    return matrix


def directed_db_fixation(weights: Sequence[Sequence[object]]) -> sp.Expr:
    """Uniform-singleton dB fixation from the literal source-target rule."""

    w = _exact_matrix(weights)
    n = len(w)
    full = (1 << n) - 1
    transient = list(range(1, full))
    index = {mask: row for row, mask in enumerate(transient)}
    matrix = sp.zeros(len(transient))
    rhs = sp.zeros(len(transient), 1)

    for mask in transient:
        row = index[mask]
        matrix[row, row] = 1
        for target in range(n):
            denominator = sum(
                (R if mask & (1 << source) else 1) * w[source][target]
                for source in range(n)
            )
            for source in range(n):
                if w[source][target] == 0:
                    continue
                probability = (
                    sp.Rational(1, n)
                    * (R if mask & (1 << source) else 1)
                    * w[source][target]
                    / denominator
                )
                if mask & (1 << source):
                    next_mask = mask | (1 << target)
                else:
                    next_mask = mask & ~(1 << target)
                if next_mask == full:
                    rhs[row, 0] += probability
                elif next_mask != 0:
                    matrix[row, index[next_mask]] -= probability

    values = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    return sp.cancel(sum(values[index[1 << i]] for i in range(n)) / n)


def complete_baseline(n: int) -> sp.Expr:
    if n == 2:
        return sp.Rational(1, 2)
    return sp.cancel(
        sp.Rational(n - 1, n)
        * (1 - 1 / R)
        / (1 - R ** (-(n - 1)))
    )


def directed_defect(weights: Sequence[Sequence[object]]) -> sp.Expr:
    w = _exact_matrix(weights)
    n = len(w)
    defect = sp.Integer(0)
    for target in range(n):
        sources = [source for source in range(n) if source != target]
        for source, other_source in combinations(sources, 2):
            a = w[source][target]
            b = w[other_source][target]
            defect += (a - b) ** 2 / (a * b)
    return sp.factor(defect)


def differentiated_coefficient(weights: Sequence[Sequence[object]]) -> sp.Expr:
    """Coefficient A_dir/[n^2(n-2)] predicted for extinction."""

    w = _exact_matrix(weights)
    n = len(w)
    if n < 3:
        raise ValueError("the first-order formula has a separate n=2 case")
    incoming = [sum(w[source][target] for source in range(n)) for target in range(n)]
    a_total = sum(
        (incoming[target] - w[source][target]) / w[source][target]
        for target in range(n)
        for source in range(n)
        if source != target
    )
    defect = directed_defect(w)
    assert sp.simplify(a_total - n * (n - 1) * (n - 2) - defect) == 0
    return sp.factor(a_total / (n**2 * (n - 2)))


def row_defect(weights: Sequence[Sequence[object]]) -> sp.Expr:
    """Deliberately wrong orientation, used as a negative control."""

    w = _exact_matrix(weights)
    n = len(w)
    defect = sp.Integer(0)
    for source in range(n):
        targets = [target for target in range(n) if target != source]
        for target, other_target in combinations(targets, 2):
            a = w[source][target]
            b = w[source][other_target]
            defect += (a - b) ** 2 / (a * b)
    return sp.factor(defect)


def check_example(weights: Sequence[Sequence[object]]) -> tuple[sp.Expr, sp.Expr]:
    w = _exact_matrix(weights)
    n = len(w)
    rho = directed_db_fixation(w)
    predicted_graph = differentiated_coefficient(w)
    extracted_graph = sp.factor(
        sp.limit(R * (sp.Rational(n - 1, n) - rho), R, sp.oo)
    )
    defect = directed_defect(w)
    predicted_difference = sp.factor(defect / (n**2 * (n - 2)))
    extracted_difference = sp.factor(
        sp.limit(R * (complete_baseline(n) - rho), R, sp.oo)
    )
    assert sp.simplify(extracted_graph - predicted_graph) == 0
    assert sp.simplify(extracted_difference - predicted_difference) == 0
    return extracted_graph, extracted_difference


def main() -> None:
    examples = (
        (
            (0, 1, 2),
            (3, 0, 4),
            (5, 6, 0),
        ),
        (
            (0, 2, 6),
            (3, 0, 9),
            (5, 7, 0),
        ),
        (
            (0, 1, 2, 3),
            (4, 0, 5, 6),
            (7, 8, 0, 9),
            (10, 11, 12, 0),
        ),
    )
    for weights in examples:
        graph_coefficient, comparison_coefficient = check_example(weights)
        print(
            f"n={len(weights)} E_dir={directed_defect(weights)} "
            f"graph_coefficient={graph_coefficient} "
            f"comparison_coefficient={comparison_coefficient}"
        )

    column_uniform = (
        (0, 5, 7, 11),
        (2, 0, 7, 11),
        (2, 5, 0, 11),
        (2, 5, 7, 0),
    )
    rho = directed_db_fixation(column_uniform)
    assert directed_defect(column_uniform) == 0
    assert sp.simplify(rho - complete_baseline(4)) == 0
    assert row_defect(column_uniform) == sp.Rational(1131, 77)
    print(
        "column-uniform negative control: exact baseline identity; "
        f"wrong row defect={row_defect(column_uniform)}"
    )

    original = (
        (0, 1, 2),
        (3, 0, 4),
        (5, 6, 0),
    )
    scales = (2, 3, 5)
    scaled = tuple(
        tuple(scales[target] * original[source][target] for target in range(3))
        for source in range(3)
    )
    assert sp.simplify(
        directed_db_fixation(original) - directed_db_fixation(scaled)
    ) == 0
    print("independent incoming-column scaling: exact fixation identity")


if __name__ == "__main__":
    main()
