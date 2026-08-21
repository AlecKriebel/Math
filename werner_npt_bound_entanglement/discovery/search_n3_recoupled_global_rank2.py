#!/usr/bin/env python3
"""Discovery search for the replica-rank-two recoupled inequality.

This is floating-point discovery code.  It evaluates the recoupled
operator without constructing its 531441-square ambient matrix.
"""

from __future__ import annotations

import argparse

import numpy as np


DIM = 27
SHAPE = (3,) * 12
ROW_PAIRS = ((0, 3), (1, 4), (2, 5))
COL_PAIRS = ((6, 9), (7, 10), (8, 11))
SWAP_HALVES = (6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5)


def scalar_projection(tensor: np.ndarray, first: int, second: int) -> np.ndarray:
    """Project two qutrit axes onto normalized sum_j |jj>."""
    diagonal_sum = None
    for value in range(3):
        selector = [slice(None)] * tensor.ndim
        selector[first] = value
        selector[second] = value
        section = tensor[tuple(selector)]
        diagonal_sum = section.copy() if diagonal_sum is None else diagonal_sum + section
    output = np.zeros_like(tensor)
    diagonal_sum /= 3.0
    for value in range(3):
        selector = [slice(None)] * tensor.ndim
        selector[first] = value
        selector[second] = value
        output[tuple(selector)] = diagonal_sum
    return output


def pattern_projection(
    tensor: np.ndarray,
    pairs: tuple[tuple[int, int], ...],
    traceless_pattern: tuple[bool, bool, bool],
) -> np.ndarray:
    output = tensor
    for pair, traceless in zip(pairs, traceless_pattern):
        scalar = scalar_projection(output, *pair)
        output = output - scalar if traceless else scalar
    return output


def pair_sector_projection(
    tensor: np.ndarray,
    pairs: tuple[tuple[int, int], ...],
) -> np.ndarray:
    output = np.zeros_like(tensor)
    for scalar_site in range(3):
        pattern = tuple(site != scalar_site for site in range(3))
        output += pattern_projection(tensor, pairs, pattern)
    return output


def coefficient_tensor(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """A tensor conjugate(B), regrouped as (L1,R1):(L2,R2)."""
    matrix = (
        left[:, None, :, None]
        * np.conjugate(right)[None, :, None, :]
    )
    return matrix.reshape(SHAPE)


def objective_and_image(
    left: np.ndarray, right: np.ndarray
) -> tuple[float, np.ndarray]:
    matrix = coefficient_tensor(left, right)
    skew = (matrix - matrix.transpose(SWAP_HALVES)) / 2.0

    row_pair = pair_sector_projection(skew, ROW_PAIRS)
    col_pair = pair_sector_projection(skew, COL_PAIRS)
    both_pair = pair_sector_projection(row_pair, COL_PAIRS)

    pair_out = row_pair - both_pair
    out_pair = col_pair - both_pair
    both_out = skew - row_pair - col_pair + both_pair

    norm = lambda value: float(np.vdot(value, value).real)
    # 2 <P_-M, (2Q-P) tensor (2Q-P) P_-M>.
    value = (
        8.0 * norm(both_out)
        - 4.0 * norm(pair_out)
        - 4.0 * norm(out_pair)
        + 2.0 * norm(both_pair)
    )
    # O M for O=(I-F)(2Q-P) tensor (2Q-P).
    image = 2.0 * (
        4.0 * both_out
        - 2.0 * pair_out
        - 2.0 * out_pair
        + both_pair
    )
    return value, image


def objective(left: np.ndarray, right: np.ndarray) -> float:
    return objective_and_image(left, right)[0]


def objective_gradient(
    left: np.ndarray, right: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    value, image = objective_and_image(left, right)
    image = image.reshape(DIM, DIM, DIM, DIM)
    left_gradient = np.einsum("iajb,ab->ij", image, right)
    right_gradient = np.einsum("iajb,ij->ab", np.conjugate(image), left)
    return value, left_gradient, right_gradient


def quotient_gradient(
    left: np.ndarray, right: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    value, image = objective_and_image(left, right)
    matrix = coefficient_tensor(left, right)
    skew = (matrix - matrix.transpose(SWAP_HALVES)) / 2.0
    denominator = float(np.vdot(skew, skew).real)
    if denominator < 1e-14:
        return np.inf, np.zeros_like(left), np.zeros_like(right)
    quotient = value / denominator
    image = (image - quotient * skew) / denominator
    image = image.reshape(DIM, DIM, DIM, DIM)
    left_gradient = np.einsum("iajb,ab->ij", image, right)
    right_gradient = np.einsum("iajb,ij->ab", np.conjugate(image), left)
    return quotient, left_gradient, right_gradient


def normalized_low_rank(
    rng: np.random.Generator, rank: int
) -> np.ndarray:
    left = rng.normal(size=(DIM, rank)) + 1j * rng.normal(size=(DIM, rank))
    right = rng.normal(size=(DIM, rank)) + 1j * rng.normal(size=(DIM, rank))
    matrix = left @ right.conjugate().T
    return matrix / np.linalg.norm(matrix)


def truncate_rank(matrix: np.ndarray, rank: int) -> np.ndarray:
    left, singular, right = np.linalg.svd(matrix, full_matrices=False)
    singular[rank:] = 0
    matrix = (left * singular) @ right
    return matrix / np.linalg.norm(matrix)


def projected_descent(
    left: np.ndarray,
    right: np.ndarray,
    rank: int,
    steps: int,
    quotient: bool,
) -> tuple[float, np.ndarray, np.ndarray]:
    function = (
        (lambda a, b: quotient_gradient(a, b)[0])
        if quotient
        else objective
    )
    gradient_function = quotient_gradient if quotient else objective_gradient
    value = function(left, right)
    step_size = 0.1
    for _ in range(steps):
        _, left_gradient, right_gradient = gradient_function(left, right)
        # Remove radial components before the projected step.
        left_gradient -= np.vdot(left, left_gradient).real * left
        right_gradient -= np.vdot(right, right_gradient).real * right
        accepted = False
        trial_step = step_size
        for _ in range(12):
            left_trial = truncate_rank(left - trial_step * left_gradient, rank)
            right_trial = truncate_rank(right - trial_step * right_gradient, rank)
            trial_value = function(left_trial, right_trial)
            if trial_value < value - 1e-12:
                left, right, value = left_trial, right_trial, trial_value
                step_size = min(0.5, trial_step * 1.2)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
    return value, left, right


def check_gradient(rng: np.random.Generator) -> None:
    left = normalized_low_rank(rng, 2)
    right = normalized_low_rank(rng, 2)
    _, left_gradient, right_gradient = objective_gradient(left, right)
    for variable, gradient, other, vary_left in (
        (left, left_gradient, right, True),
        (right, right_gradient, left, False),
    ):
        direction = rng.normal(size=variable.shape) + 1j * rng.normal(
            size=variable.shape
        )
        epsilon = 1e-6
        if vary_left:
            plus = objective(variable + epsilon * direction, other)
            minus = objective(variable - epsilon * direction, other)
        else:
            plus = objective(other, variable + epsilon * direction)
            minus = objective(other, variable - epsilon * direction)
        finite_difference = (plus - minus) / (2 * epsilon)
        predicted = 2 * np.vdot(gradient, direction).real
        if not np.isclose(finite_difference, predicted, rtol=2e-5, atol=2e-6):
            raise RuntimeError((finite_difference, predicted))


def root_family(rank: int) -> tuple[np.ndarray, np.ndarray]:
    e01 = np.zeros((3, 3), dtype=complex)
    e00 = np.zeros((3, 3), dtype=complex)
    e11 = np.zeros((3, 3), dtype=complex)
    e01[0, 1] = 1
    e00[0, 0] = 1
    e11[1, 1] = 1
    diagonal = np.zeros((3, 3), dtype=complex)
    diagonal[range(rank), range(rank)] = 1 / np.sqrt(rank)
    return (
        np.kron(np.kron(e01, e00), diagonal),
        np.kron(np.kron(e01, e11), diagonal),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--rank", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--steps", type=int, default=0)
    parser.add_argument("--quotient", action="store_true")
    args = parser.parse_args()

    for rank in (1, 2, 3):
        left, right = root_family(rank)
        expected = (2.0 / rank - 1.0) / 3.0
        value = objective(left, right)
        print("root family", rank, value, "expected", expected)
        if not np.isclose(value, expected, atol=2e-12):
            raise RuntimeError("objective implementation failed its exact family")

    rng = np.random.default_rng(args.seed)
    check_gradient(rng)
    best = np.inf
    for sample in range(args.samples):
        left = normalized_low_rank(rng, args.rank)
        right = normalized_low_rank(rng, args.rank)
        if args.steps:
            value, left, right = projected_descent(
                left, right, args.rank, args.steps, args.quotient
            )
        else:
            value = objective(left, right)
        if value < best:
            best = value
            print("best", sample, repr(best), flush=True)


if __name__ == "__main__":
    main()
