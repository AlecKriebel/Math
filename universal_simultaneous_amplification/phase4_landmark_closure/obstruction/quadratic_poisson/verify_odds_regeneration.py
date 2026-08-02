#!/usr/bin/env python3
"""Exact verifier for the r=2 odds-regeneration reduction.

The script has three independent purposes.

1.  It checks, on an integer-weight K4, that the stationary one-coordinate
    regeneration identities recover both the vacancy probability and the
    mean raw return count.
2.  It gives an exact counterexample to the tempting *arbitrary outside
    start* inequality ``u(Y) (1 + g(Y)) >= 1``.
3.  It checks the exact first-marginal comparison between the stationary
    unbatched branching--coalescing random walk and one batched dB-dual
    generator step.

Only Fraction arithmetic is used.
"""

from __future__ import annotations

from fractions import Fraction as F


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a square rational system by Gauss--Jordan elimination."""

    n = len(matrix)
    aug = [matrix[i][:] + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if aug[row][column])
        aug[column], aug[pivot] = aug[pivot], aug[column]
        scale = aug[column][column]
        aug[column] = [entry / scale for entry in aug[column]]
        for row in range(n):
            if row == column:
                continue
            scale = aug[row][column]
            if scale:
                aug[row] = [
                    left - scale * right
                    for left, right in zip(aug[row], aug[column])
                ]
    return [aug[row][-1] for row in range(n)]


def transition(weights: list[list[int]]) -> list[list[F]]:
    return [[F(entry, sum(row)) for entry in row] for row in weights]


def h(value: F) -> F:
    return 2 * value / (1 + value)


def geometric_union_law(row: list[F]) -> dict[int, F]:
    """Law of the distinct sites in K geometric(1/2) row samples."""

    n = len(row)
    values = [F(0) for _ in range(1 << n)]
    for mask in range(1 << n):
        mass = sum(
            (row[j] for j in range(n) if (mask >> j) & 1),
            F(0),
        )
        values[mask] = mass / (2 - mass)
    # Boolean-lattice Mobius inversion of Pr(union subseteq mask).
    for j in range(n):
        for mask in range(1 << n):
            if (mask >> j) & 1:
                values[mask] -= values[mask ^ (1 << j)]
    law = {mask: values[mask] for mask in range(1, 1 << n) if values[mask]}
    assert sum(law.values()) == 1
    assert all(probability > 0 for probability in law.values())
    return law


def stationary(generator: list[list[F]]) -> list[F]:
    """Return the stationary row law of an irreducible generator."""

    size = len(generator)
    matrix = [
        [generator[column][row] for column in range(size)]
        for row in range(size)
    ]
    rhs = [F(0) for _ in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs[-1] = F(1)
    answer = solve(matrix, rhs)
    assert sum(answer) == 1
    assert all(value >= 0 for value in answer)
    for column in range(size):
        assert sum(answer[row] * generator[row][column] for row in range(size)) == 0
    return answer


def batched_generator(P: list[list[F]]) -> tuple[list[list[F]], list[dict[int, F]]]:
    n = len(P)
    states = list(range(1, 1 << n))
    laws = [geometric_union_law(row) for row in P]
    generator = [[F(0) for _ in states] for _ in states]
    for state in states:
        row = state - 1
        for v in range(n):
            if not ((state >> v) & 1):
                continue
            for offspring, probability in laws[v].items():
                new_state = (state & ~(1 << v)) | offspring
                if new_state != state:
                    generator[row][new_state - 1] += probability
        generator[row][row] = -sum(generator[row])
    return generator, laws


def unbatched_generator(P: list[list[F]]) -> list[list[F]]:
    """Neutral move rate one plus selective retain/add rate one."""

    n = len(P)
    states = list(range(1, 1 << n))
    generator = [[F(0) for _ in states] for _ in states]
    for state in states:
        row = state - 1
        for v in range(n):
            if not ((state >> v) & 1):
                continue
            for u in range(n):
                rate = P[v][u]
                neutral = (state & ~(1 << v)) | (1 << u)
                selective = state | (1 << u)
                if neutral != state:
                    generator[row][neutral - 1] += rate
                if selective != state:
                    generator[row][selective - 1] += rate
        generator[row][row] = -sum(generator[row])
    return generator


def marginals(pi: list[F], n: int) -> list[F]:
    return [
        sum(pi[state - 1] for state in range(1, 1 << n) if (state >> i) & 1)
        for i in range(n)
    ]


def stopped_systems(
    P: list[list[F]], laws: list[dict[int, F]], target: int
) -> tuple[list[F], list[F], list[int]]:
    """Return u(Y)=Pr(N=0), g(Y)=E N before an Exp(1) kill."""

    n = len(P)
    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    size = 1 << (n - 1)
    generator = [[F(0) for _ in range(size)] for _ in range(size)]
    zero_hit = [[F(int(row == column)) for column in range(size)] for row in range(size)]
    reward = [F(0) for _ in range(size)]

    for state in range(size):
        active = [
            outside[position]
            for position in range(n - 1)
            if (state >> position) & 1
        ]
        zero_hit[state][state] += len(active)
        for v in active:
            reward[state] += 2 * P[v][target]
            marginal: dict[int, F] = {}
            for offspring, probability in laws[v].items():
                outside_offspring = sum(
                    1 << local[j]
                    for j in outside
                    if (offspring >> j) & 1
                )
                new_state = (state & ~(1 << local[v])) | outside_offspring
                marginal[new_state] = marginal.get(new_state, F(0)) + probability
                if not ((offspring >> target) & 1):
                    zero_hit[state][new_state] -= probability
            for new_state, probability in marginal.items():
                if new_state != state:
                    generator[state][new_state] += probability
        generator[state][state] = -sum(generator[state])

    resolvent = [
        [F(int(row == column)) - generator[row][column] for column in range(size)]
        for row in range(size)
    ]
    u = solve(zero_hit, [F(1) for _ in range(size)])
    g = solve(resolvent, reward)
    return u, g, outside


def post_target_law(
    pi: list[F], laws: list[dict[int, F]], target: int, n: int
) -> list[F]:
    """Outside-set law immediately after a rate-one target clock ring."""

    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    eta = [F(0) for _ in range(1 << (n - 1))]
    for state in range(1, 1 << n):
        if not ((state >> target) & 1):
            outputs = {state: F(1)}
        else:
            outputs: dict[int, F] = {}
            for offspring, probability in laws[target].items():
                new_state = (state & ~(1 << target)) | offspring
                outputs[new_state] = outputs.get(new_state, F(0)) + probability
        for output, probability in outputs.items():
            assert not ((output >> target) & 1)
            local_state = sum(
                1 << local[j] for j in outside if (output >> j) & 1
            )
            eta[local_state] += pi[state - 1] * probability
    assert sum(eta) == 1
    return eta


def main() -> None:
    # Edge order (01,02,03,12,13,23) = (89,21,1,34,1,2).
    weights = [
        [0, 89, 21, 1],
        [89, 0, 34, 1],
        [21, 34, 0, 2],
        [1, 1, 2, 0],
    ]
    P = transition(weights)
    n = len(P)
    dual, laws = batched_generator(P)
    pi = stationary(dual)
    p = marginals(pi, n)

    # The exact stationary-regeneration reduction, checked at every target.
    stationary_slacks = []
    for target in range(n):
        u, g, _ = stopped_systems(P, laws, target)
        eta = post_target_law(pi, laws, target, n)
        regenerated_q = sum(weight * value for weight, value in zip(eta, u))
        regenerated_mean = sum(weight * value for weight, value in zip(eta, g))
        q = 1 - p[target]
        raw_mean = 2 * sum(P[v][target] * p[v] for v in range(n))
        assert regenerated_q == q
        assert regenerated_mean == raw_mean
        stationary_slacks.append(q * (1 + raw_mean) - 1)
    assert all(slack >= 0 for slack in stationary_slacks)

    # The arbitrary-start strengthening is false.  Target 2 and the full
    # outside start Y={0,1,3} give a strict exact counterexample.
    target = 2
    u, g, outside = stopped_systems(P, laws, target)
    full_outside = (1 << len(outside)) - 1
    false_slack = u[full_outside] * (1 + g[full_outside]) - 1
    assert false_slack < 0

    # First-marginal BCRW comparison.  Under its exact stationary law,
    # replacing rate 2P by H can only lower every coordinate's generator
    # drift.  This is a one-step fact, not a stationary-domination proof.
    unbatched = unbatched_generator(P)
    nu = stationary(unbatched)
    p_unbatched = marginals(nu, n)
    batched_drifts = []
    for i in range(n):
        cross = [
            sum(
                nu[state - 1]
                for state in range(1, 1 << n)
                if not ((state >> i) & 1) and ((state >> v) & 1)
            )
            for v in range(n)
        ]
        unbatched_fill = 2 * sum(P[v][i] * cross[v] for v in range(n))
        assert unbatched_fill == p_unbatched[i]
        drift = sum(h(P[v][i]) * cross[v] for v in range(n)) - p_unbatched[i]
        assert drift <= 0
        batched_drifts.append(drift)

    print("PASS: exact stationary-regeneration identities at all four targets")
    print("stationary odds slacks:", stationary_slacks)
    print("arbitrary-start counterexample target/outside:", target, outside)
    print("u(Y):", u[full_outside])
    print("g(Y):", g[full_outside])
    print("u(Y)(1+g(Y))-1:", false_slack)
    print("unbatched-to-batched coordinate drifts:", batched_drifts)


if __name__ == "__main__":
    main()
