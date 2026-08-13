#!/usr/bin/env python3
"""Exact subsolution certificate at r=1001/1000 for the theta graph.

Floating sparse solves are used only to propose rational vectors.  Every
Bellman inequality and both final comparison signs are then checked exactly
over QQ.  Hence floating error cannot create a false positive.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction as F

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import bicgstab

import audit_theta_full_fitness as theta


FITNESS = F(1001, 1000)
ENDPOINT_WEIGHT = F(103, 500)
SCALE = 10**16
MIXING = F(1, 10**6)


def neutral_value(state, rule: str) -> F:
    if state == theta.EXTINCTION:
        return F(0)
    if state == theta.FIXATION:
        return F(1)
    left_hub, right_hub, counts = state
    hub_degree = 7 * ENDPOINT_WEIGHT
    endpoint_degree = 1 + ENDPOINT_WEIGHT
    middle_degree = F(2)
    total_degree = 2 * hub_degree + 14 * endpoint_degree + 7 * middle_degree
    C = 1 / (
        F(2) / hub_degree
        + F(14) / endpoint_degree
        + F(7) / middle_degree
    )
    mutant_hubs = left_hub + right_hub
    mutant_endpoints = sum(
        count * (pattern[0] + pattern[2])
        for count, pattern in zip(counts, theta.PATTERNS)
    )
    mutant_middles = sum(
        count * pattern[1]
        for count, pattern in zip(counts, theta.PATTERNS)
    )
    if rule == "Bd":
        return C * (
            F(mutant_hubs) / hub_degree
            + F(mutant_endpoints) / endpoint_degree
            + F(mutant_middles) / middle_degree
        )
    return (
        mutant_hubs * hub_degree
        + mutant_endpoints * endpoint_degree
        + mutant_middles * middle_degree
    ) / total_degree


def boundary_value(target, vector) -> F:
    if target == theta.FIXATION:
        return F(1)
    if target == theta.EXTINCTION:
        return F(0)
    return vector[theta.INDEX[target]]


def exact_embedded_apply(rows, vector):
    result = []
    for row, exit_probability in rows:
        result.append(
            sum(
                (
                    probability * boundary_value(target, vector)
                    for target, probability in row.items()
                ),
                F(0),
            )
            / exit_probability
        )
    return result


def float_solution(rule: str):
    rows = []
    columns = []
    data = []
    rhs = np.zeros(len(theta.TRANSIENT))
    for state, row_index in theta.INDEX.items():
        row = theta.changes(state, float(FITNESS), float(ENDPOINT_WEIGHT), rule)
        exit_probability = sum(row.values())
        rows.append(row_index)
        columns.append(row_index)
        data.append(exit_probability)
        for target, probability in row.items():
            if target == theta.FIXATION:
                rhs[row_index] += probability
            elif target != theta.EXTINCTION:
                rows.append(row_index)
                columns.append(theta.INDEX[target])
                data.append(-probability)
    matrix = csr_matrix(
        (data, (rows, columns)),
        shape=(len(theta.TRANSIENT), len(theta.TRANSIENT)),
    )
    diagonal = matrix.diagonal()
    scaled = matrix.multiply((1 / diagonal)[:, None]).tocsr()
    solution, info = bicgstab(
        scaled,
        rhs / diagonal,
        rtol=2e-13,
        atol=1e-14,
        maxiter=200_000,
    )
    assert info == 0
    assert np.max(np.abs(matrix @ solution - rhs)) < 2e-13
    return solution


def uniform_average(vector):
    total = vector[theta.INDEX[(1, 0, (theta.ARMS,) + (0,) * 7)]]
    total += vector[theta.INDEX[(0, 1, (theta.ARMS,) + (0,) * 7)]]
    zero = (0, 0, 0)
    for position in range(3):
        pattern = list(zero)
        pattern[position] = 1
        counts = [0] * 8
        counts[theta.PATTERN_INDEX[zero]] = theta.ARMS - 1
        counts[theta.PATTERN_INDEX[tuple(pattern)]] = 1
        total += theta.ARMS * vector[theta.INDEX[(0, 0, tuple(counts))]]
    return total / theta.ORDER


def complete_baseline(rule: str) -> F:
    numerator = 1 - 1 / FITNESS
    if rule == "Bd":
        return numerator / (1 - FITNESS ** (-theta.ORDER))
    return F(theta.ORDER - 1, theta.ORDER) * numerator / (
        1 - FITNESS ** (1 - theta.ORDER)
    )


def certify(rule: str):
    exact_rows = []
    for state in theta.TRANSIENT:
        row = theta.changes(state, FITNESS, ENDPOINT_WEIGHT, rule)
        exact_rows.append((row, sum(row.values(), F(0))))

    neutral = [neutral_value(state, rule) for state in theta.TRANSIENT]
    if rule == "Bd":
        strict_subsolution = neutral
    else:
        first_iterate = exact_embedded_apply(exact_rows, neutral)
        strict_subsolution = [
            (left + right) / 2 for left, right in zip(neutral, first_iterate)
        ]
    next_strict = exact_embedded_apply(exact_rows, strict_subsolution)
    strict_slacks = [
        right - left for left, right in zip(strict_subsolution, next_strict)
    ]
    assert min(strict_slacks) > 0

    proposal = float_solution(rule)
    candidate_numerators = [
        int(
            SCALE
            * (
                (1 - float(MIXING)) * proposal[index]
                + float(MIXING) * float(strict_subsolution[index])
            )
        )
        for index in range(len(proposal))
    ]
    candidate = [F(value, SCALE) for value in candidate_numerators]
    assert all(0 <= value <= 1 for value in candidate)

    minimum_slack = None
    for index, (row, exit_probability) in enumerate(exact_rows):
        slack = sum(
            (
                probability * boundary_value(target, candidate)
                for target, probability in row.items()
            ),
            F(0),
        ) - exit_probability * candidate[index]
        assert slack >= 0
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack

    gap = uniform_average(candidate) - complete_baseline(rule)
    assert gap > 0
    digest = hashlib.sha256(
        ",".join(str(value) for value in candidate_numerators).encode()
    ).hexdigest()
    return gap, minimum_slack, min(strict_slacks), digest


def main() -> None:
    for rule in ("Bd", "dB"):
        gap, minimum_slack, strict_slack, digest = certify(rule)
        print(f"{rule}: exact subsolution mean gap={gap} (~{float(gap):.15g})")
        print(f"{rule}: strict analytic drift floor ~{float(strict_slack):.15g}")
        print(f"{rule}: minimum exact Bellman slack ~{float(minimum_slack):.15g}")
        print(f"{rule}: candidate SHA-256={digest}")
    print("PASS exact finite-fitness simultaneous amplification at r=1001/1000")


if __name__ == "__main__":
    main()
