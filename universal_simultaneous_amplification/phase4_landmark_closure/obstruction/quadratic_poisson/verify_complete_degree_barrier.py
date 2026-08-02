#!/usr/bin/env python3
"""Exact finite verifier for the complete-graph degree-barrier identities.

The theorem itself is symbolic and is proved in COMPLETE_DEGREE_BARRIER.md.
This standard-library script checks its burst factorial moments, leading
coefficient identity, complete stationary level law, and sharp Poisson
degree for 3 <= n <= 12 using Fraction arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb, factorial


def exact_union_subset_probability(categories: int, size: int) -> F:
    """Probability that the geometric burst union is one specified set."""
    return sum(
        F((-1) ** (size - used) * comb(size, used) * used, 2 * categories - used)
        for used in range(1, size + 1)
    )


def named_appearance_probability(categories: int, size: int) -> F:
    return sum(
        F((-1) ** (used + 1) * comb(size, used) * 2 * used, categories + used)
        for used in range(1, size + 1)
    )


def level_generator(order: int) -> list[list[F]]:
    categories = order - 1
    exact = {
        size: exact_union_subset_probability(categories, size)
        for size in range(1, categories + 1)
    }
    generator = [[F(0) for _ in range(categories)] for _ in range(categories)]
    for level in range(1, order):
        active_neighbors = level - 1
        outside_neighbors = order - level
        for active_sampled in range(active_neighbors + 1):
            for outside_sampled in range(outside_neighbors + 1):
                union_size = active_sampled + outside_sampled
                if union_size == 0:
                    continue
                probability = (
                    comb(active_neighbors, active_sampled)
                    * comb(outside_neighbors, outside_sampled)
                    * exact[union_size]
                )
                new_level = level - 1 + outside_sampled
                if new_level != level:
                    generator[level - 1][new_level - 1] += level * probability
        generator[level - 1][level - 1] = -sum(
            generator[level - 1][column]
            for column in range(categories)
            if column != level - 1
        )
    assert all(sum(row) == 0 for row in generator)
    return generator


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    order = len(rhs)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(order)]
    for column in range(order):
        pivot = next(row for row in range(column, order) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(order):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(order)]


def finite_differences(values: list[F]) -> list[list[F]]:
    rows = [values]
    while len(rows[-1]) > 1:
        rows.append(
            [rows[-1][index + 1] - rows[-1][index] for index in range(len(rows[-1]) - 1)]
        )
    return rows


def main() -> None:
    for order in range(3, 13):
        categories = order - 1
        for size in range(1, categories + 1):
            assert named_appearance_probability(categories, size) == F(
                2, comb(categories + size, size)
            )

        for degree in range(1, order - 1):
            leading_sum = F(2, factorial(degree)) * sum(
                F((-1) ** size * comb(degree, size), comb(categories + size, size))
                for size in range(1, degree + 1)
            )
            assert leading_sum == -F(
                2, factorial(degree - 1) * (categories + degree)
            )

        generator = level_generator(order)
        normalization = 2**categories - 1
        invariant = [F(comb(categories, level), normalization) for level in range(1, order)]
        assert sum(invariant) == 1
        assert all(
            sum(
                invariant[row] * generator[row][column]
                for row in range(categories)
            )
            == 0
            for column in range(categories)
        )
        complete_mean = sum(
            F(level) * invariant[level - 1] for level in range(1, order)
        )
        assert complete_mean == F(
            categories * 2 ** (categories - 1), normalization
        )

        # Fix h(1)=0 and replace one redundant Poisson equation by that gauge.
        system = [row[:] for row in generator]
        rhs = [F(level) - complete_mean for level in range(1, order)]
        system[0] = [F(0) for _ in range(categories)]
        system[0][0] = F(1)
        rhs[0] = F(0)
        solution = solve_linear(system, rhs)
        assert all(
            sum(generator[row][column] * solution[column] for column in range(categories))
            == F(row + 1) - complete_mean
            for row in range(categories)
        )
        differences = finite_differences(solution)
        assert differences[-1][0] != 0

        print(
            f"PASS K_{order}: mean={complete_mean}, "
            f"minimal Poisson degree={order - 2}"
        )


if __name__ == "__main__":
    main()

