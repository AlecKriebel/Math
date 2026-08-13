#!/usr/bin/env python3
"""Exact audit of the common marked cross-rule current at fitness two.

This verifies identities and the weighted-P3 pointwise Poisson obstruction.
It does not assert the open all-graph stationary sign.
"""

from __future__ import annotations

from fractions import Fraction as F

from verify_cross_rule_tree_reduction import (
    dot,
    marked_kernel_r2,
    marked_psi,
    shared_l_two_step_forcing,
    transition_matrix,
    tree_cofactors,
    tree_data,
    unbatched_generators,
)


def solve_with_gauge(matrix, source, gauge_index):
    """Solve matrix*x=source over QQ after fixing one additive gauge."""

    size = len(matrix)
    work = [row[:] + [value] for row, value in zip(matrix, source)]
    work[gauge_index] = [F(0) for _ in range(size + 1)]
    work[gauge_index][gauge_index] = F(1)
    rank = 0
    pivots = []
    for column in range(size):
        pivot = next(
            (row for row in range(rank, size) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(size):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
    assert rank == size
    answer = [F(0) for _ in range(size)]
    for row, column in enumerate(pivots):
        answer[column] = work[row][-1]
    return answer


def product_generator(generator):
    """Kronecker-sum generator Q tensor I + I tensor Q."""

    side = len(generator)
    size = side * side
    answer = [[F(0) for _ in range(size)] for _ in range(size)]
    for left in range(side):
        for right in range(side):
            row = left * side + right
            for output in range(side):
                answer[row][output * side + right] += generator[left][output]
                answer[row][left * side + output] += generator[right][output]
    return answer


def forcing_data(weights):
    """Return L, pi_L, m_L, and the exact marked two-step forcing F_P."""

    n = len(weights)
    full = (1 << n) - 1
    left, _ = unbatched_generators(weights)
    tau, partition, first_moment, mean = tree_data(
        left, list(range(1, full + 1))
    )
    pi = [weight / partition for weight in tau]
    marked_states, marked_kernel = marked_kernel_r2(weights)
    psi = [marked_psi(n, cache.bit_count()) for cache, _ in marked_states]
    one_step = [dot(row, psi) for row in marked_kernel]
    two_step = [dot(row, one_step) for row in marked_kernel]
    forcing = shared_l_two_step_forcing(weights, marked_states, two_step)

    index = {state: row for row, state in enumerate(marked_states)}
    q_l = []
    for cache, _ in marked_states:
        occupied = full ^ cache
        q_l.append(pi[occupied - 1] / mean)
    assert sum(q_l, F(0)) == 1
    forcing_mean = dot(pi, forcing)
    assert forcing_mean == mean * dot(q_l, two_step)
    assert first_moment / partition == mean
    assert len(index) == len(marked_states)
    return left, pi, mean, forcing


def transported_complement_palm(weights, pi, marked_states):
    """Closed formula for (lambda_L M_P)(D,w) in equation (5a)."""

    p = transition_matrix(weights)
    n = len(weights)
    full = (1 << n) - 1

    def stationary_mass(state):
        return F(0) if state == 0 else pi[state - 1]

    answer = []
    for cache, output_target in marked_states:
        occupied = full ^ cache
        active_cache = cache | (1 << output_target)
        active_size = active_cache.bit_count()
        continue_mass = (
            sum(
                (p[output_target][source] for source in range(n)
                 if (cache >> source) & 1),
                F(0),
            )
            * stationary_mass(occupied)
            + sum(
                (
                    p[output_target][source]
                    * stationary_mass(occupied | (1 << source))
                    for source in range(n)
                    if (cache >> source) & 1
                ),
                F(0),
            )
        )
        occupied_without_output = occupied & ~(1 << output_target)
        stop_mass = stationary_mass(occupied_without_output) * sum(
            (
                p[old_target][sample]
                for old_target in range(n)
                if (occupied_without_output >> old_target) & 1
                for sample in range(n)
                if (active_cache >> sample) & 1
            ),
            F(0),
        )
        for sample in range(n):
            if not ((active_cache >> sample) & 1):
                continue
            predecessor_occupied = occupied_without_output | (1 << sample)
            stop_mass += stationary_mass(predecessor_occupied) * sum(
                (
                    p[old_target][sample]
                    for old_target in range(n)
                    if (predecessor_occupied >> old_target) & 1
                ),
                F(0),
            )
        answer.append(continue_mass / 2 + stop_mass / (2 * active_size))
    return answer


def main():
    weighted_path = (
        (0, 1, 2),
        (1, 0, 0),
        (2, 0, 0),
    )
    complete = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    n = 3
    full = (1 << n) - 1
    side = full
    b = F(12, 7)
    d = F(4, 3)

    left, pi, mean, forcing = forcing_data(weighted_path)
    complete_left, complete_pi, complete_mean, complete_forcing = forcing_data(
        complete
    )
    assert all(mass == F(1, full) for mass in complete_pi)
    assert complete_mean == b

    # Literal complemented-Palm transport (5a).
    marked_states, marked_kernel = marked_kernel_r2(weighted_path)
    marked_index = {state: row for row, state in enumerate(marked_states)}
    lambda_l = []
    for cache, _ in marked_states:
        occupied = full ^ cache
        lambda_l.append(pi[occupied - 1])
    direct_transport = [
        sum(
            (
                lambda_l[source] * marked_kernel[source][target]
                for source in range(len(marked_states))
            ),
            F(0),
        )
        for target in range(len(marked_states))
    ]
    assert direct_transport == transported_complement_palm(
        weighted_path, pi, marked_states
    )
    assert sum(lambda_l, F(0)) == mean
    assert len(marked_index) == len(marked_states)

    # One actual marked Green current plus the radial covariance, (5c).
    marked_generator = [
        [
            marked_kernel[row][column] - F(row == column)
            for column in range(len(marked_states))
        ]
        for row in range(len(marked_states))
    ]
    marked_trees = tree_cofactors(marked_generator)
    marked_partition = sum(marked_trees, F(0))
    mu_d = [weight / marked_partition for weight in marked_trees]
    marked_psi_values = [
        marked_psi(n, cache.bit_count()) for cache, _ in marked_states
    ]
    inverse_mean_d = dot(mu_d, marked_psi_values)
    assert inverse_mean_d == F(5, 6)
    centered_psi = [value - inverse_mean_d for value in marked_psi_values]
    green = solve_with_gauge(
        [
            [F(row == column) - marked_kernel[row][column]
             for column in range(len(marked_states))]
            for row in range(len(marked_states))
        ],
        centered_psi,
        len(marked_states) - 1,
    )
    marked_current = dot(
        lambda_l,
        [dot(row, green) for row in marked_generator],
    )
    lambda_psi = dot(lambda_l, marked_psi_values)
    radial_covariance = lambda_psi - mean * mean / (b * d)
    assert marked_current == F(739, 5115)
    assert radial_covariance == F(-293, 581405)
    assert marked_current + radial_covariance == mean * (
        inverse_mean_d - mean / (b * d)
    )
    assert marked_current + radial_covariance == F(50224, 348843)

    complete_product = product_generator(complete_left)
    product_size = side * side
    complete_target = []
    for first in range(1, full + 1):
        for second in range(1, full + 1):
            complete_target.append(
                (complete_forcing[first - 1] + complete_forcing[second - 1]) / 2
                - F(first.bit_count() * second.bit_count(), 1) / (b * d)
            )
    assert sum(complete_target, F(0)) == 0

    poisson_matrix = [[-entry for entry in row] for row in complete_product]
    gauge = product_size - 1
    potential = solve_with_gauge(poisson_matrix, complete_target, gauge)
    radial_table = {
        (1, 1): F(17, 24),
        (1, 2): F(59, 96),
        (1, 3): F(19, 32),
        (2, 1): F(59, 96),
        (2, 2): F(17, 48),
        (2, 3): F(7, 32),
        (3, 1): F(19, 32),
        (3, 2): F(7, 32),
        (3, 3): F(0),
    }
    for first in range(1, full + 1):
        for second in range(1, full + 1):
            index = (first - 1) * side + second - 1
            assert potential[index] == radial_table[
                first.bit_count(), second.bit_count()
            ]

    actual_product = product_generator(left)
    residuals = []
    integrated_target = F(0)
    integrated_residual = F(0)
    for first in range(1, full + 1):
        for second in range(1, full + 1):
            index = (first - 1) * side + second - 1
            target = (
                (forcing[first - 1] + forcing[second - 1]) / 2
                - F(first.bit_count() * second.bit_count(), 1) / (b * d)
            )
            current = dot(actual_product[index], potential)
            residual = target + current
            direct_difference = (
                forcing[first - 1]
                - complete_forcing[first - 1]
                + forcing[second - 1]
                - complete_forcing[second - 1]
            ) / 2
            generator_difference = dot(
                [
                    actual - baseline
                    for actual, baseline in zip(
                        actual_product[index], complete_product[index]
                    )
                ],
                potential,
            )
            assert residual == direct_difference + generator_difference
            mass = pi[first - 1] * pi[second - 1]
            integrated_target += mass * target
            integrated_residual += mass * residual
            residuals.append(
                (
                    residual,
                    first,
                    second,
                    direct_difference,
                    generator_difference,
                )
            )

    assert integrated_residual == integrated_target
    assert integrated_target == dot(pi, forcing) - mean * mean / (b * d)
    assert integrated_target == F(18560, 116281)
    assert b * d * dot(pi, forcing) - mean * mean == F(296960, 813967)

    minimum = min(residuals)
    assert minimum == (F(-107, 288), 1, 5, F(-25, 144), F(-19, 96))
    assert sum(residual < 0 for residual, *_ in residuals) == 14

    # No graph-dependent scalar multiple of the bare overlap drift can
    # repair the pointwise residual: its drift vanishes at (001,111), where
    # the residual is already negative.
    overlap = [
        F((first & second).bit_count())
        for first in range(1, full + 1)
        for second in range(1, full + 1)
    ]
    overlap_index = full - 1
    assert dot(actual_product[overlap_index], overlap) == 0
    assert residuals[overlap_index][0] == F(-11, 36)

    print("PASS: common marked L/dB probability-space normalization")
    print("PASS: literal lambda_L transport and current/covariance identity")
    print("PASS: exact two-L forcing and complete product Poisson identity")
    print("REFUTED: pointwise radial product-Poisson residual")
    print("minimum = -107/288 at (A,B)=(001,101); 14/49 pairs negative")
    print("REFUTED: any scalar bare-overlap correction at (001,111)")
    print("OPEN: integrated two-step floor; exact surplus = 18560/116281")


if __name__ == "__main__":
    main()
