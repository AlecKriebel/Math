#!/usr/bin/env python3
"""Independent exact replay of the strong-selection obstruction.

This verifier does not call ``src.exact_markov``.  It independently constructs
the single-vertex-flip chain, proves row identities over QQ(r), checks the
complete-graph mutant-count lumping, solves the absorbing equations, extracts
strong-selection coefficients, and emits exact sign certificates for a
nontrivial rational comparison.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


r = sp.symbols("r", positive=True)
x = sp.symbols("x", positive=True)


def matrix(weights: Sequence[Sequence[int]]) -> Tuple[Tuple[sp.Rational, ...], ...]:
    w = tuple(tuple(sp.Rational(value) for value in row) for row in weights)
    n = len(w)
    require(n >= 2 and all(len(row) == n for row in w))
    require(all(w[i][i] == 0 for i in range(n)))
    require(all(w[i][j] == w[j][i] >= 0 for i in range(n) for j in range(n)))
    return w


def is_mutant(mask: int, vertex: int) -> bool:
    return bool(mask & (1 << vertex))


def flip(mask: int, vertex: int) -> int:
    return mask ^ (1 << vertex)


def coefficient_nonnegative_on_r_gt_one(value: sp.Expr) -> bool:
    """Exact coefficient certificate after the substitution r=1+x."""

    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_poly = sp.Poly(sp.expand(numerator.subs(r, 1 + x)), x)
    denominator_poly = sp.Poly(sp.expand(denominator.subs(r, 1 + x)), x)
    if denominator_poly.LC() < 0:
        numerator_poly = -numerator_poly
        denominator_poly = -denominator_poly
    return (
        all(coefficient >= 0 for coefficient in numerator_poly.all_coeffs())
        and all(coefficient >= 0 for coefficient in denominator_poly.all_coeffs())
        and any(coefficient > 0 for coefficient in denominator_poly.all_coeffs())
    )


def transition_rows(
    weights: Sequence[Sequence[int]], rule: str
) -> List[Dict[int, sp.Expr]]:
    """Construct aggregate flip probabilities from the defining rule."""

    w = matrix(weights)
    n = len(w)
    full = (1 << n) - 1
    degree = [sum(row) for row in w]
    rows: List[Dict[int, sp.Expr]] = []
    for mask in range(1 << n):
        if mask in (0, full):
            rows.append({mask: sp.Integer(1)})
            continue
        row: Dict[int, sp.Expr] = {}
        if rule == "Bd":
            count = sum(is_mutant(mask, i) for i in range(n))
            total_fitness = r * count + n - count
            for target in range(n):
                if is_mutant(mask, target):
                    incoming = sum(
                        w[parent][target] / degree[parent]
                        for parent in range(n)
                        if not is_mutant(mask, parent)
                    )
                    probability = incoming / total_fitness
                else:
                    incoming = sum(
                        w[parent][target] / degree[parent]
                        for parent in range(n)
                        if is_mutant(mask, parent)
                    )
                    probability = r * incoming / total_fitness
                if probability:
                    row[flip(mask, target)] = sp.cancel(probability)
        elif rule == "dB":
            for dead in range(n):
                mutant_mass = sum(
                    w[parent][dead]
                    for parent in range(n)
                    if is_mutant(mask, parent)
                )
                resident_mass = degree[dead] - mutant_mass
                denominator = r * mutant_mass + resident_mass
                if is_mutant(mask, dead):
                    probability = sp.Rational(1, n) * resident_mass / denominator
                else:
                    probability = sp.Rational(1, n) * r * mutant_mass / denominator
                if probability:
                    row[flip(mask, dead)] = sp.cancel(probability)
        else:
            raise ValueError(rule)
        row[mask] = sp.cancel(1 - sum(row.values()))
        require(sp.cancel(sum(row.values()) - 1) == 0)
        require(all(coefficient_nonnegative_on_r_gt_one(p) for p in row.values()))
        require(all(
            target == mask or (target ^ mask) & ((target ^ mask) - 1) == 0
            for target in row
        ))
        rows.append(row)
    return rows


@lru_cache(maxsize=None)
def solve_average(
    weights: Tuple[Tuple[int, ...], ...], rule: str
) -> sp.Expr:
    """Solve the state-change Laplacian exactly over rational functions."""

    rows = transition_rows(weights, rule)
    n = len(weights)
    full = (1 << n) - 1
    transient = tuple(range(1, full))
    location = {mask: i for i, mask in enumerate(transient)}
    system = sp.zeros(len(transient), len(transient))
    rhs = sp.zeros(len(transient), 1)
    for state in transient:
        i = location[state]
        outgoing = sum(
            probability for target, probability in rows[state].items() if target != state
        )
        system[i, i] = outgoing
        for target, probability in rows[state].items():
            if target == full:
                rhs[i, 0] += probability
            elif target not in (0, state):
                system[i, location[target]] -= probability
    solution_set = sp.linsolve((system, rhs))
    solution = tuple(next(iter(solution_set)))
    return sp.cancel(sum(solution[location[1 << i]] for i in range(n)) / n)


def complete_weights(n: int) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(0 if i == j else 1 for j in range(n)) for i in range(n))


def baseline(n: int, rule: str) -> sp.Expr:
    if rule == "Bd":
        return sp.cancel((1 - 1 / r) / (1 - r ** (-n)))
    return sp.cancel(sp.Rational(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1))))


def verify_complete_lumping(n: int, rule: str) -> None:
    rows = transition_rows(complete_weights(n), rule)
    cells = [
        tuple(mask for mask in range(1 << n) if bin(mask).count("1") == count)
        for count in range(n + 1)
    ]
    for source in cells:
        aggregates = []
        for state in source:
            aggregates.append(
                tuple(
                    sp.cancel(sum(rows[state].get(target, 0) for target in target_cell))
                    for target_cell in cells
                )
            )
        require(all(aggregate == aggregates[0] for aggregate in aggregates))


def support_limit(weights: Tuple[Tuple[int, ...], ...]) -> sp.Rational:
    n = len(weights)
    support_degrees = [sum(value > 0 for value in row) for row in weights]
    return sum(sp.Rational(k, k + 1) for k in support_degrees) / n


def predicted_complete_coefficient(weights: Tuple[Tuple[int, ...], ...]) -> sp.Expr:
    n = len(weights)
    degree = [sum(row) for row in weights]
    obstruction = sum(
        sp.Rational(
            degree[vertex] - weights[vertex][neighbor],
            weights[vertex][neighbor],
        )
        for vertex in range(n)
        for neighbor in range(n)
        if vertex != neighbor
    )
    return sp.cancel(obstruction / (n**2 * (n - 2)))


def strict_sign_by_shift(polynomial: sp.Expr, wanted: int) -> Dict[str, object]:
    shifted = sp.Poly(sp.expand(polynomial.subs(r, 1 + x)), x)
    multiplicity = 0
    while shifted.eval(0) == 0:
        shifted = sp.Poly(sp.cancel(shifted.as_expr() / x), x)
        multiplicity += 1
    signed = shifted if wanted > 0 else -shifted
    require(all(coefficient >= 0 for coefficient in signed.all_coeffs()))
    require(any(coefficient > 0 for coefficient in signed.all_coeffs()))
    return {
        "sign": wanted,
        "endpoint_multiplicity": multiplicity,
        "shifted_coefficients": signed.all_coeffs(),
    }


def main() -> None:
    # Every subset transition is constructed and checked for these exact cases.
    for n in (2, 3, 4):
        for rule in ("Bd", "dB"):
            verify_complete_lumping(n, rule)
            require(sp.cancel(solve_average(complete_weights(n), rule) - baseline(n, rule)) == 0)

    path4 = ((0, 1, 0, 0), (1, 0, 1, 0), (0, 1, 0, 1), (0, 0, 1, 0))
    star4 = ((0, 1, 1, 1), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0))
    for weights, expected in ((path4, sp.Rational(7, 12)), (star4, sp.Rational(9, 16))):
        rho = solve_average(weights, "dB")
        require(support_limit(weights) == expected)
        require(sp.limit(rho, r, sp.oo) == expected)
        require(expected < sp.Rational(3, 4))

    triangle = ((0, 2, 3), (2, 0, 5), (3, 5, 0))
    weighted_k4 = ((0, 1, 2, 3), (1, 0, 4, 5), (2, 4, 0, 6), (3, 5, 6, 0))
    extracted_coefficients = []
    for weights in (triangle, weighted_k4):
        n = len(weights)
        rho = solve_average(weights, "dB")
        extracted = sp.limit(r * (sp.Rational(n - 1, n) - rho), r, sp.oo)
        predicted = predicted_complete_coefficient(weights)
        require(extracted == predicted)
        require(predicted > sp.Rational(n - 1, n))
        extracted_coefficients.append(extracted)

    # Exact comparison certificate for a nonuniform weighted triangle.
    triangle_difference = sp.cancel(solve_average(triangle, "dB") - baseline(3, "dB"))
    numerator, denominator = sp.fraction(triangle_difference)
    numerator_certificate = strict_sign_by_shift(numerator, -1)
    denominator_certificate = strict_sign_by_shift(denominator, 1)

    print("PASS: exact transition rows, complete-graph lumping, and absorption solves")
    print("PASS: incomplete-support limits path4=7/12 and star4=9/16")
    print("PASS: complete-support 1/r coefficients", extracted_coefficients)
    print("PASS: weighted-triangle numerator certificate", numerator_certificate)
    print("PASS: weighted-triangle denominator certificate", denominator_certificate)


if __name__ == "__main__":
    main()
