#!/usr/bin/env python3
"""Exact order-four certificates for two invalid annealing intermediaries.

The orbital conjecture concerns the *kernel* midpoint.  It cannot be split
through either the arithmetic mean of the endpoint generators or the full
permutation-annealed generator.  This verifier constructs all labelled dB
rates at fitness two over QQ and certifies both strict failures.
"""

from __future__ import annotations

from fractions import Fraction as F

import sympy as sp


def h(x: F) -> F:
    return 2 * x / (1 + x)


def regular_k4(a: F, b: F, c: F) -> list[list[F]]:
    return [
        [F(0), a, b, c],
        [a, F(0), c, b],
        [b, c, F(0), a],
        [c, b, a, F(0)],
    ]


def generator(weights: list[list[F]]):
    size = len(weights)
    full = (1 << size) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    boundary = [F(0) for _ in states]
    for row, state in enumerate(states):
        for target in range(size):
            context = state & ~(1 << target)
            mass = sum(
                (weights[target][source] for source in range(size) if context >> source & 1),
                F(0),
            )
            mutant_probability = h(mass)
            if state >> target & 1:
                next_state = context
                rate = 1 - mutant_probability
            else:
                next_state = state | (1 << target)
                rate = mutant_probability
            if next_state == full:
                boundary[row] += rate
            elif next_state:
                matrix[row][index[next_state]] += rate
            matrix[row][row] -= rate
    return states, matrix, boundary


def solve(matrix: list[list[F]], boundary: list[F]) -> sp.Matrix:
    transient = sp.Matrix(
        [[-sp.Rational(value.numerator, value.denominator) for value in row] for row in matrix]
    )
    rhs = sp.Matrix([sp.Rational(value.numerator, value.denominator) for value in boundary])
    return transient.inv() * rhs


def rational_matrix(matrix: list[list[F]]) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.Rational(value.numerator, value.denominator) for value in row]
            for row in matrix
        ]
    )


def rational_vector(vector: list[F]) -> sp.Matrix:
    return sp.Matrix([sp.Rational(value.numerator, value.denominator) for value in vector])


def mean_singleton(states: list[int], values: sp.Matrix, size: int) -> sp.Rational:
    return sp.factor(sum(values[states.index(1 << vertex)] for vertex in range(size)) / size)


def fixation(weights: list[list[F]]) -> sp.Rational:
    states, matrix, boundary = generator(weights)
    return mean_singleton(states, solve(matrix, boundary), len(weights))


def row_kernel(conductances: list[list[F]]) -> list[list[F]]:
    return [
        [value / sum(conductances[row], F(0)) for value in conductances[row]]
        for row in range(len(conductances))
    ]


def conjugate(weights: list[list[F]], permutation: list[int]) -> list[list[F]]:
    return [
        [weights[permutation[row]][permutation[column]] for column in range(len(weights))]
        for row in range(len(weights))
    ]


def arithmetic_mean(first, second):
    return [
        [(first[row][column] + second[row][column]) / 2 for column in range(len(first))]
        for row in range(len(first))
    ]


def swap_mask(mask: int) -> int:
    return (mask & ~3) | (2 if mask & 1 else 0) | (1 if mask & 2 else 0)


def hit_generator(weights: list[list[F]], occupied: int, target_set: int) -> F:
    """Apply the exact dB-dual generator to 1{A intersects target_set}."""
    intersection = occupied & target_set
    if not intersection:
        return sum(
            (
                h(
                    sum(
                        (
                            weights[vertex][source]
                            for source in range(len(weights))
                            if target_set >> source & 1
                        ),
                        F(0),
                    )
                )
                for vertex in range(len(weights))
                if occupied >> vertex & 1
            ),
            F(0),
        )
    if intersection & (intersection - 1) == 0:
        vertex = intersection.bit_length() - 1
        mass = sum(
            (
                weights[vertex][source]
                for source in range(len(weights))
                if target_set >> source & 1
            ),
            F(0),
        )
        return h(mass) - 1
    return F(0)


def main() -> None:
    a, b, c = F(7, 10), F(1, 5), F(1, 10)
    endpoint = regular_k4(a, b, c)
    endpoint_value = fixation(endpoint)

    permutation = [1, 0, 2, 3]
    conjugate_endpoint = conjugate(endpoint, permutation)
    states, first_generator, first_boundary = generator(endpoint)
    _, second_generator, second_boundary = generator(conjugate_endpoint)
    averaged_generator = arithmetic_mean(first_generator, second_generator)
    averaged_boundary = [
        (first_boundary[row] + second_boundary[row]) / 2 for row in range(len(states))
    ]
    generator_average_value = mean_singleton(
        states,
        solve(averaged_generator, averaged_boundary),
        4,
    )

    a1 = (h(a) + h(b) + h(c)) / 3
    a2 = (h(a + b) + h(a + c) + h(b + c)) / 3
    probabilities = [F(0), a1, a2, F(1)]
    product = F(1)
    denominator = F(1)
    for mutant_count in range(1, 4):
        birth = F(4 - mutant_count) * probabilities[mutant_count]
        death = F(mutant_count) * (1 - probabilities[mutant_count - 1])
        product *= death / birth
        denominator += product
    fully_annealed_value = sp.Rational(denominator.denominator, denominator.numerator)

    kernel_midpoint = arithmetic_mean(endpoint, conjugate_endpoint)
    kernel_midpoint_value = fixation(kernel_midpoint)

    occupied = 0b0011
    target_set = 0b0101
    coverage_residual = (
        hit_generator(kernel_midpoint, occupied, target_set)
        + hit_generator(kernel_midpoint, occupied, swap_mask(target_set))
        - hit_generator(endpoint, occupied, target_set)
        - hit_generator(endpoint, swap_mask(occupied), target_set)
    )

    # The sharp sector functional is linear on the U-even coverage cone.
    # Test its extreme ray g(S)=1{S intersects {0,1}} exactly.
    _, midpoint_generator, midpoint_boundary = generator(kernel_midpoint)
    q_endpoint = rational_matrix(first_generator)
    q_conjugate = rational_matrix(second_generator)
    q_midpoint = rational_matrix(midpoint_generator)
    b_endpoint = rational_vector(first_boundary)
    b_conjugate = rational_vector(second_boundary)
    b_midpoint = rational_vector(midpoint_boundary)
    q_average = (q_endpoint + q_conjugate) / 2
    b_average = (b_endpoint + b_conjugate) / 2
    odd_coupling = (q_endpoint - q_conjugate) / 2
    odd_boundary = (b_endpoint - b_conjugate) / 2
    midpoint_bonus = q_midpoint - q_average
    midpoint_boundary_bonus = b_midpoint - b_average

    coverage_set = 0b0011
    coverage = sp.Matrix(
        [
            sp.Rational(
                int(bool(state & coverage_set))
                + int(bool(state & swap_mask(coverage_set))),
                2,
            )
            for state in states
        ]
    )
    odd_source = odd_coupling * coverage + odd_boundary
    odd_solution = (-q_average).inv() * odd_source
    sector_residual = (
        midpoint_bonus * coverage
        + midpoint_boundary_bonus
        - odd_coupling * odd_solution
    )
    singleton_start = sp.zeros(len(states), 1)
    for vertex in range(4):
        singleton_start[states.index(1 << vertex)] = sp.Rational(1, 4)
    midpoint_occupation = (-q_midpoint).T.inv() * singleton_start
    coverage_sector_value = sp.factor((midpoint_occupation.T * sector_residual)[0])

    directed_endpoint = [
        [F(0), F(999, 1000), F(1, 1000)],
        [F(24, 25), F(0), F(1, 25)],
        [F(2, 5), F(3, 5), F(0)],
    ]
    directed_permutation = [1, 0, 2]
    directed_conjugate = conjugate(directed_endpoint, directed_permutation)
    directed_midpoint = arithmetic_mean(directed_endpoint, directed_conjugate)
    directed_endpoint_value = fixation(directed_endpoint)
    directed_midpoint_value = fixation(directed_midpoint)
    directed_slack = sp.factor(directed_midpoint_value - directed_endpoint_value)

    conductances = [[F(0) for _ in range(5)] for _ in range(5)]
    for first, second, value in (
        (0, 2, F(5)),
        (0, 4, F(1)),
        (1, 3, F(20)),
        (1, 4, F(1, 10)),
    ):
        conductances[first][second] = conductances[second][first] = value
    conductance_permutation = [1, 0, 2, 3, 4]
    conjugate_conductances = conjugate(conductances, conductance_permutation)
    midpoint_conductances = arithmetic_mean(conductances, conjugate_conductances)
    conductance_endpoint_value = fixation(row_kernel(conductances))
    conductance_midpoint_value = fixation(row_kernel(midpoint_conductances))
    conductance_slack = sp.factor(conductance_midpoint_value - conductance_endpoint_value)

    assert endpoint_value == sp.Rational(8941, 21293)
    assert generator_average_value == sp.Rational(387817, 926066)
    assert fully_annealed_value == sp.Rational(959027, 2557096)
    assert generator_average_value - endpoint_value == -sp.Rational(22168725, 19718723338)
    assert fully_annealed_value - endpoint_value == -sp.Rational(2442433425, 54448245128)
    assert kernel_midpoint_value > endpoint_value
    assert coverage_residual == -F(10, 69)
    assert q_average * odd_solution + odd_source == sp.zeros(len(states), 1)
    assert coverage_sector_value == -sp.Rational(268925, 327199119)
    assert directed_endpoint_value == sp.Rational(150104029643, 432850757676)
    assert directed_midpoint_value == sp.Rational(52230380, 150626871)
    assert directed_slack == -sp.Rational(
        580250970313391,
        21732985079571703932,
    )
    assert conductance_endpoint_value == sp.Rational(39794039823911, 114450553349505)
    assert conductance_midpoint_value == sp.Rational(
        65633240271786525885720837847,
        203520905146834717343643922215,
    )
    assert conductance_slack == -sp.Rational(
        39143889145638008146691134610289543891142,
        1552872014149823570194880387852400261916905,
    )

    print("PASS: exact labelled generator-average counterexample")
    print("endpoint", endpoint_value)
    print("generator_average", generator_average_value)
    print("generator_average_minus_endpoint", generator_average_value - endpoint_value)
    print("PASS: exact full-permutation annealing counterexample")
    print("fully_annealed", fully_annealed_value)
    print("fully_annealed_minus_endpoint", fully_annealed_value - endpoint_value)
    print("PASS: the actual transposition kernel midpoint still improves fixation")
    print("kernel_midpoint", kernel_midpoint_value)
    print("kernel_midpoint_minus_endpoint", sp.factor(kernel_midpoint_value - endpoint_value))
    print("PASS: exact coverage-cone one-step comparison counterexample")
    print("coverage_generator_residual", coverage_residual)
    print("PASS: exact coverage-cone sector counterexample")
    print("coverage_sector_value", coverage_sector_value)
    print("PASS: exact directed-kernel orbital counterexample")
    print("directed_endpoint", directed_endpoint_value)
    print("directed_midpoint", directed_midpoint_value)
    print("directed_orbital_slack", directed_slack)
    print("PASS: exact undirected-conductance orbital counterexample")
    print("conductance_endpoint", conductance_endpoint_value)
    print("conductance_midpoint", conductance_midpoint_value)
    print("conductance_orbital_slack", conductance_slack)


if __name__ == "__main__":
    main()
