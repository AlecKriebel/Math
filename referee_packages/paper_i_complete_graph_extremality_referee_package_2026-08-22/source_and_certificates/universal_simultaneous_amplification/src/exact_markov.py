"""Exact fixation calculations for weighted evolutionary graphs.

The implementation follows the update definitions literally.  States are
bitmasks, edge weights and fitness are SymPy expressions, and no floating-point
arithmetic is used.  The routines are intentionally small enough to serve as a
readable reference implementation for independent verification.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import sympy as sp


R = sp.symbols("r", positive=True)


def _as_exact_matrix(weights: Sequence[Sequence[object]]) -> Tuple[Tuple[sp.Expr, ...], ...]:
    return tuple(tuple(sp.sympify(x) for x in row) for row in weights)


def validate_weights(weights: Sequence[Sequence[object]]) -> Tuple[Tuple[sp.Expr, ...], ...]:
    """Return an exact matrix after checking the graph hypotheses."""

    w = _as_exact_matrix(weights)
    n = len(w)
    if n < 2 or any(len(row) != n for row in w):
        raise ValueError("the weight matrix must be square of order at least two")
    for i in range(n):
        if sp.simplify(w[i][i]) != 0:
            raise ValueError("self-loop weights must vanish")
        for j in range(n):
            if sp.simplify(w[i][j] - w[j][i]) != 0:
                raise ValueError("the weight matrix must be symmetric")
            if w[i][j].is_negative is True:
                raise ValueError("edge weights must be nonnegative")
    adjacency = [[j for j in range(n) if j != i and w[i][j] != 0] for i in range(n)]
    if any(not row for row in adjacency):
        raise ValueError("every vertex must have positive weighted degree")
    seen = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in adjacency[i]:
            if j not in seen:
                seen.add(j)
                queue.append(j)
    if len(seen) != n:
        raise ValueError("the positive-weight support must be connected")
    return w


def _mutant(mask: int, vertex: int) -> bool:
    return bool(mask & (1 << vertex))


def _replace(mask: int, vertex: int, mutant: bool) -> int:
    if mutant:
        return mask | (1 << vertex)
    return mask & ~(1 << vertex)


def transition_row(
    weights: Sequence[Sequence[object]],
    mask: int,
    rule: str,
    fitness: sp.Expr = R,
) -> Dict[int, sp.Expr]:
    """Build one exact transition row directly from the update definition."""

    w = validate_weights(weights)
    n = len(w)
    full = (1 << n) - 1
    if not 0 <= mask <= full:
        raise ValueError("state mask is out of range")
    if mask in (0, full):
        return {mask: sp.Integer(1)}

    rule_key = rule.lower()
    row: Dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
    degree = [sum(w[i]) for i in range(n)]

    if rule_key == "bd":
        vertex_fitness = [fitness if _mutant(mask, i) else sp.Integer(1) for i in range(n)]
        total_fitness = sum(vertex_fitness)
        for parent in range(n):
            for target in range(n):
                if w[parent][target] == 0:
                    continue
                probability = (
                    vertex_fitness[parent]
                    * w[parent][target]
                    / (total_fitness * degree[parent])
                )
                next_mask = _replace(mask, target, _mutant(mask, parent))
                row[next_mask] += probability
    elif rule_key == "db":
        for dead in range(n):
            competitor_mass = sum(
                (fitness if _mutant(mask, parent) else 1) * w[parent][dead]
                for parent in range(n)
            )
            for parent in range(n):
                if w[parent][dead] == 0:
                    continue
                probability = (
                    (fitness if _mutant(mask, parent) else 1)
                    * w[parent][dead]
                    / (n * competitor_mass)
                )
                next_mask = _replace(mask, dead, _mutant(mask, parent))
                row[next_mask] += probability
    else:
        raise ValueError("rule must be 'Bd' or 'dB'")

    row = {target: sp.cancel(value) for target, value in row.items() if value != 0}
    if sp.simplify(sum(row.values()) - 1) != 0:
        raise AssertionError(f"transition row {mask} does not sum to one")
    return row


def transition_matrix(
    weights: Sequence[Sequence[object]], rule: str, fitness: sp.Expr = R
) -> List[Dict[int, sp.Expr]]:
    """Return the entire exact subset-state transition matrix as sparse rows."""

    w = validate_weights(weights)
    return [transition_row(w, mask, rule, fitness) for mask in range(1 << len(w))]


def fixation_vector(
    weights: Sequence[Sequence[object]], rule: str, fitness: sp.Expr = R
) -> Dict[int, sp.Expr]:
    """Solve all transient absorbing equations exactly."""

    w = validate_weights(weights)
    n = len(w)
    full = (1 << n) - 1
    transient = list(range(1, full))
    index = {mask: i for i, mask in enumerate(transient)}
    rows = transition_matrix(w, rule, fitness)
    matrix = sp.zeros(len(transient), len(transient))
    rhs = sp.zeros(len(transient), 1)
    for mask in transient:
        i = index[mask]
        matrix[i, i] = 1
        for target, probability in rows[mask].items():
            if target == full:
                rhs[i, 0] += probability
            elif target != 0:
                matrix[i, index[target]] -= probability
    solution = sp.linsolve((matrix, rhs))
    values = tuple(next(iter(solution)))
    answer = {0: sp.Integer(0), full: sp.Integer(1)}
    answer.update({mask: sp.cancel(values[index[mask]]) for mask in transient})
    return answer


def average_single_mutant_fixation(
    weights: Sequence[Sequence[object]], rule: str, fitness: sp.Expr = R
) -> sp.Expr:
    """Return the exact uniformly averaged single-mutant fixation probability."""

    w = validate_weights(weights)
    values = fixation_vector(w, rule, fitness)
    n = len(w)
    return sp.cancel(sum(values[1 << i] for i in range(n)) / n)


def complete_graph_weights(n: int) -> Tuple[Tuple[int, ...], ...]:
    if n < 2:
        raise ValueError("n must be at least two")
    return tuple(tuple(0 if i == j else 1 for j in range(n)) for i in range(n))


def complete_baseline(n: int, rule: str, fitness: sp.Expr = R) -> sp.Expr:
    """Closed forms derived from the one-dimensional mutant-count chain."""

    if n < 2:
        raise ValueError("n must be at least two")
    rule_key = rule.lower()
    if rule_key == "bd":
        return sp.cancel((1 - 1 / fitness) / (1 - fitness ** (-n)))
    if rule_key == "db":
        return sp.cancel(
            sp.Rational(n - 1, n)
            * (1 - 1 / fitness)
            / (1 - fitness ** (-(n - 1)))
        )
    raise ValueError("rule must be 'Bd' or 'dB'")


def rational_comparison(
    weights: Sequence[Sequence[object]], rule: str, fitness: sp.Expr = R
) -> Tuple[sp.Poly, sp.Poly]:
    """Return coprime numerator and denominator versus the complete baseline."""

    difference = sp.cancel(
        average_single_mutant_fixation(weights, rule, fitness)
        - complete_baseline(len(weights), rule, fitness)
    )
    numerator, denominator = sp.fraction(difference)
    return sp.Poly(numerator, fitness), sp.Poly(denominator, fitness)


def check_lumping(
    rows: Sequence[Mapping[int, sp.Expr]], cells: Sequence[Iterable[int]]
) -> List[List[sp.Expr]]:
    """Verify strong lumpability and return the exact quotient matrix.

    For each source cell, every constituent state must have the same total
    transition probability into every target cell.
    """

    normalized = [tuple(cell) for cell in cells]
    all_states = [state for cell in normalized for state in cell]
    if sorted(all_states) != list(range(len(rows))) or len(set(all_states)) != len(rows):
        raise ValueError("cells must partition all states exactly once")
    quotient: List[List[sp.Expr]] = []
    for source_cell in normalized:
        reference = None
        for state in source_cell:
            aggregate = tuple(
                sp.cancel(sum(rows[state].get(target, 0) for target in target_cell))
                for target_cell in normalized
            )
            if reference is None:
                reference = aggregate
            elif any(sp.simplify(a - b) != 0 for a, b in zip(reference, aggregate)):
                raise ValueError(f"partition is not lumpable at state {state}")
        quotient.append(list(reference or ()))
    return quotient


def sign_certificate_on_r_gt_one(poly: sp.Poly) -> Mapping[str, object]:
    """Certify a rational polynomial's strict sign on r>1 using Sturm roots."""

    if not poly.is_univariate:
        raise ValueError("a univariate polynomial is required")
    variable = poly.gens[0]
    shifted = sp.Poly(poly.as_expr().subs(variable, variable + 1), variable)
    multiplicity = 0
    while shifted.eval(0) == 0 and not shifted.is_zero:
        shifted = sp.Poly(sp.cancel(shifted.as_expr() / variable), variable)
        multiplicity += 1
    if shifted.is_zero:
        return {"sign": 0, "root_count": sp.oo, "endpoint_multiplicity": multiplicity}
    roots = int(sp.Poly(shifted, variable).count_roots(0, sp.oo))
    sample_sign = sp.sign(shifted.eval(1))
    if roots == 0 and sample_sign in (-1, 1):
        return {
            "sign": int(sample_sign),
            "root_count": 0,
            "endpoint_multiplicity": multiplicity,
            "shifted_polynomial": shifted,
        }
    return {
        "sign": None,
        "root_count": roots,
        "endpoint_multiplicity": multiplicity,
        "shifted_polynomial": shifted,
    }

