#!/usr/bin/env python3
"""Independent exact verifier for the Bd and dB additive duals.

Only the Python standard library is used.  All transition probabilities,
absorbing solves, stationary solves, and comparisons use Fraction arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Gauss--Jordan solve of a square rational system."""
    n = len(rhs)
    aug = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [a - scale * b for a, b in zip(aug[row], aug[col], strict=True)]
    return [aug[row][-1] for row in range(n)]


def kernel(weights: list[list[F]]) -> list[list[F]]:
    degree = [sum(row, F(0)) for row in weights]
    assert all(degree)
    return [[weights[u][v] / degree[u] for v in range(len(weights))] for u in range(len(weights))]


def add_rate(rates: dict[int, F], state: int, target: int, rate: F) -> None:
    if target != state and rate:
        rates[target] = rates.get(target, F(0)) + rate


def original_rates(weights: list[list[F]], r: F, rule: str, state: int) -> dict[int, F]:
    n = len(weights)
    p = kernel(weights)
    degrees = [sum(row, F(0)) for row in weights]
    rates: dict[int, F] = {}
    if rule == "Bd":
        # State-dependent time-changed rates; fixation is unchanged.
        for u in range(n):
            mutant_u = bool(state & (1 << u))
            fitness = r if mutant_u else F(1)
            for v in range(n):
                if mutant_u == bool(state & (1 << v)):
                    continue
                target = state | (1 << v) if mutant_u else state & ~(1 << v)
                add_rate(rates, state, target, fitness * p[u][v])
    elif rule == "dB":
        for v in range(n):
            mutant_mass = sum(
                (weights[u][v] for u in range(n) if state & (1 << u)), F(0)
            )
            resident_mass = degrees[v] - mutant_mass
            denominator = r * mutant_mass + resident_mass
            if state & (1 << v):
                add_rate(rates, state, state & ~(1 << v), resident_mass / denominator)
            else:
                add_rate(rates, state, state | (1 << v), r * mutant_mass / denominator)
    else:
        raise ValueError(rule)
    return rates


def fixation(weights: list[list[F]], r: F, rule: str) -> F:
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: i for i, state in enumerate(states)}
    matrix = [[F(int(i == j)) for j in range(len(states))] for i in range(len(states))]
    rhs = [F(0) for _ in states]
    for state in states:
        row = index[state]
        rates = original_rates(weights, r, rule, state)
        total = sum(rates.values(), F(0))
        assert total
        for target, rate in rates.items():
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target:
                matrix[row][index[target]] -= probability
    values = solve(matrix, rhs)
    return sum((values[index[1 << v]] for v in range(n)), F(0)) / n


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def geometric_union_law(row: list[F], r: F) -> dict[int, F]:
    """Law of the set of distinct values in K geometric iid samples."""
    support = sum((1 << u for u, probability in enumerate(row) if probability), 0)

    def contained(mask: int) -> F:
        mass = sum((row[u] for u in range(len(row)) if mask & (1 << u)), F(0))
        if not mass:
            return F(0)
        # E[mass^K] for P(K=k)=r^-1(1-r^-1)^(k-1).
        return mass / (r - (r - 1) * mass)

    law: dict[int, F] = {}
    for target in subsets(support):
        if not target:
            continue
        value = F(0)
        for inside in subsets(target):
            sign = -1 if (target.bit_count() - inside.bit_count()) % 2 else 1
            value += sign * contained(inside)
        if value:
            law[target] = value
    assert sum(law.values(), F(0)) == 1
    return law


def dual_generator(weights: list[list[F]], r: F, rule: str) -> list[list[F]]:
    n = len(weights)
    p = kernel(weights)
    states = list(range(1, 1 << n))
    index = {state: i for i, state in enumerate(states)}
    q = [[F(0) for _ in states] for _ in states]
    union_laws = [geometric_union_law(row, r) for row in p]
    for state in states:
        rates: dict[int, F] = {}
        if rule == "Bd":
            for u in range(n):
                for v in range(n):
                    if not p[u][v] or not state & (1 << v):
                        continue
                    neutral = (state & ~(1 << v)) | (1 << u)
                    selective = state | (1 << u)
                    add_rate(rates, state, neutral, p[u][v])
                    add_rate(rates, state, selective, (r - 1) * p[u][v])
        elif rule == "dB":
            for v in range(n):
                if not state & (1 << v):
                    continue
                base = state & ~(1 << v)
                for sampled, probability in union_laws[v].items():
                    add_rate(rates, state, base | sampled, probability)
        else:
            raise ValueError(rule)
        row = index[state]
        for target, rate in rates.items():
            q[row][index[target]] += rate
            q[row][row] -= rate
    return q


def stationary_from_full(q: list[list[F]], n: int) -> list[F]:
    """Stationary law; test cases have one nonempty recurrent class."""
    size = len(q)
    matrix = [[q[col][row] for col in range(size)] for row in range(size)]
    rhs = [F(0) for _ in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs[-1] = F(1)
    pi = solve(matrix, rhs)
    assert all(value >= 0 for value in pi)
    for col in range(size):
        assert sum((pi[row] * q[row][col] for row in range(size)), F(0)) == 0
    return pi


def h(r: F, probability: F) -> F:
    return r * probability / (1 + (r - 1) * probability)


def verify_boolean_maps(weights: list[list[F]], r: F) -> int:
    """Check the elementary map dualities and the dB OR probability."""
    n = len(weights)
    p = kernel(weights)
    checks = 0
    for x in range(1 << n):
        for a in range(1, 1 << n):
            for u in range(n):
                for v in range(n):
                    if not p[u][v]:
                        continue
                    # Neutral map x_v <- x_u.
                    phi_x = (x | (1 << v)) if x & (1 << u) else (x & ~(1 << v))
                    phi_a = ((a & ~(1 << v)) | (1 << u)) if a & (1 << v) else a
                    assert bool(phi_x & a) == bool(x & phi_a)
                    # Selective map x_v <- x_v OR x_u.
                    psi_x = x | (1 << v) if x & (1 << u) else x
                    psi_a = a | (1 << u) if a & (1 << v) else a
                    assert bool(psi_x & a) == bool(x & psi_a)
                    checks += 2
            for v in range(n):
                mutant_mass = sum((p[v][u] for u in range(n) if x & (1 << u)), F(0))
                law = geometric_union_law(p[v], r)
                or_probability = sum(
                    (probability for sampled, probability in law.items() if sampled & x),
                    F(0),
                )
                assert or_probability == h(r, mutant_mass)
                checks += 1
    return checks


def verify_case(weights: list[list[F]], r: F) -> int:
    n = len(weights)
    p = kernel(weights)
    checks = verify_boolean_maps(weights, r)
    states = list(range(1, 1 << n))
    for rule in ("Bd", "dB"):
        q = dual_generator(weights, r, rule)
        pi = stationary_from_full(q, n)
        density = sum(
            (pi[row] * state.bit_count() for row, state in enumerate(states)), F(0)
        ) / n
        original = fixation(weights, r, rule)
        assert density == original, (rule, density, original)
        checks += 1

        # Generator first-moment balance, averaged under pi.
        balance = F(0)
        for row, state in enumerate(states):
            if rule == "Bd":
                temperatures = [sum((p[u][v] for u in range(n)), F(0)) for v in range(n)]
                incoming = sum(
                    (
                        p[u][v]
                        for u in range(n)
                        for v in range(n)
                        if not state & (1 << u) and state & (1 << v)
                    ),
                    F(0),
                )
                drift = r * incoming - sum(
                    (temperatures[v] for v in range(n) if state & (1 << v)), F(0)
                )
            else:
                drift = -state.bit_count() + sum(
                    (
                        h(r, p[v][u])
                        for v in range(n)
                        for u in range(n)
                        if state & (1 << v) and not state & (1 << u)
                    ),
                    F(0),
                )
            direct = sum(
                (q[row][col] * (states[col].bit_count() - state.bit_count()) for col in range(len(states))),
                F(0),
            )
            assert drift == direct
            balance += pi[row] * drift
            checks += 1
        assert balance == 0
        checks += 1
    return checks


def symmetric_weights(size: int, edges: dict[tuple[int, int], int]) -> list[list[F]]:
    weights = [[F(0) for _ in range(size)] for _ in range(size)]
    for (u, v), value in edges.items():
        weights[u][v] = weights[v][u] = F(value)
    return weights


def main() -> None:
    cases = [
        (symmetric_weights(3, {(0, 1): 2, (1, 2): 5}), F(3, 2)),
        (symmetric_weights(3, {(0, 1): 1, (0, 2): 3, (1, 2): 7}), F(2)),
        (
            symmetric_weights(
                4,
                {(0, 1): 1, (0, 2): 2, (0, 3): 5, (1, 2): 3, (1, 3): 4, (2, 3): 6},
            ),
            F(7, 3),
        ),
    ]
    checks = sum(verify_case(weights, r) for weights, r in cases)
    print(f"PASS exact Bd/dB additive-duality certificates checks={checks}")


if __name__ == "__main__":
    main()
