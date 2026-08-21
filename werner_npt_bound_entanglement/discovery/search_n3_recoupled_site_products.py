#!/usr/bin/env python3
"""Low-memory falsifier for a stronger recoupled block-positivity claim.

The physical pair-sector wedge uses four global vectors.  This search
allows a larger class: the left-replica and right-replica vectors may
be entangled with each other locally, but are products across the three
qutrit sites.  Alternating exact local eigensolves minimize the
recoupled witness.  Floating-point output is discovery evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np


COEFFICIENT = (2.0, -1.0, 2.0 / 3.0, -1.0 / 3.0)
MASKS = tuple(range(8))


def permutation_matrix(order: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((81, 81), dtype=complex)
    for word in np.ndindex(3, 3, 3, 3):
        source = np.ravel_multi_index(word, (3, 3, 3, 3))
        target_word = tuple(word[index] for index in order)
        target = np.ravel_multi_index(target_word, (3, 3, 3, 3))
        matrix[target, source] = 1
    return matrix


def compose(*orders: tuple[int, ...]) -> tuple[int, ...]:
    result = tuple(range(4))
    for order in reversed(orders):
        result = tuple(result[index] for index in order)
    return result


IDENTITY = (0, 1, 2, 3)
F1 = (2, 1, 0, 3)
F2 = (0, 3, 2, 1)
LEFT_SWAP = (1, 0, 2, 3)
RIGHT_SWAP = (0, 1, 3, 2)


def mask_order(first: bool, second: bool) -> tuple[int, ...]:
    return compose(F1 if first else IDENTITY, F2 if second else IDENTITY)


LOCAL_DIRECT: dict[tuple[int, int], np.ndarray] = {}
LOCAL_CROSSED: dict[tuple[int, int], np.ndarray] = {}
for first in (0, 1):
    for second in (0, 1):
        vertical = mask_order(bool(first), bool(second))
        LOCAL_DIRECT[first, second] = permutation_matrix(vertical)
        LOCAL_CROSSED[first, second] = permutation_matrix(
            compose(LEFT_SWAP, vertical, RIGHT_SWAP)
        )


def local_expectations(
    left: np.ndarray, right: np.ndarray
) -> tuple[dict[tuple[int, int], complex], dict[tuple[int, int], complex]]:
    product = np.kron(left, right)
    direct = {
        key: np.vdot(product, operator @ product)
        for key, operator in LOCAL_DIRECT.items()
    }
    crossed = {
        key: np.vdot(product, operator @ product)
        for key, operator in LOCAL_CROSSED.items()
    }
    return direct, crossed


def coefficient(mask: int) -> float:
    return COEFFICIENT[bin(mask).count("1")]


def objective(left: list[np.ndarray], right: list[np.ndarray]) -> float:
    data = [local_expectations(left[i], right[i]) for i in range(3)]
    value = 0j
    for first_mask in MASKS:
        for second_mask in MASKS:
            direct = 1.0 + 0j
            crossed = 1.0 + 0j
            for site in range(3):
                key = (
                    (first_mask >> site) & 1,
                    (second_mask >> site) & 1,
                )
                direct *= data[site][0][key]
                crossed *= data[site][1][key]
            value += (
                coefficient(first_mask)
                * coefficient(second_mask)
                * (direct - crossed)
            )
    return float(value.real)


def local_effective(
    left: list[np.ndarray],
    right: list[np.ndarray],
    site: int,
    vary_left: bool,
) -> np.ndarray:
    data = [local_expectations(left[i], right[i]) for i in range(3)]
    effective = np.zeros((9, 9), dtype=complex)
    fixed = right[site] if vary_left else left[site]
    for first_mask in MASKS:
        for second_mask in MASKS:
            key = (
                (first_mask >> site) & 1,
                (second_mask >> site) & 1,
            )
            direct_weight = 1.0 + 0j
            crossed_weight = 1.0 + 0j
            for other in range(3):
                if other == site:
                    continue
                other_key = (
                    (first_mask >> other) & 1,
                    (second_mask >> other) & 1,
                )
                direct_weight *= data[other][0][other_key]
                crossed_weight *= data[other][1][other_key]
            scalar = coefficient(first_mask) * coefficient(second_mask)
            for operator, weight, sign in (
                (LOCAL_DIRECT[key], direct_weight, 1),
                (LOCAL_CROSSED[key], crossed_weight, -1),
            ):
                tensor = operator.reshape(9, 9, 9, 9)
                if vary_left:
                    block = np.einsum(
                        "j,ijkl,l->ik",
                        np.conjugate(fixed),
                        tensor,
                        fixed,
                    )
                else:
                    block = np.einsum(
                        "i,ijkl,k->jl",
                        np.conjugate(fixed),
                        tensor,
                        fixed,
                    )
                effective += scalar * sign * weight * block
    return (effective + effective.conjugate().T) / 2


def random_unit(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=9) + 1j * rng.normal(size=9)
    return vector / np.linalg.norm(vector)


def truncate_local_rank(vector: np.ndarray, rank: int) -> np.ndarray:
    matrix = vector.reshape(3, 3)
    left, singular, right = np.linalg.svd(matrix, full_matrices=False)
    singular[rank:] = 0
    truncated = (left * singular) @ right
    return truncated.reshape(-1) / np.linalg.norm(truncated)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=100)
    parser.add_argument("--sweeps", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--output")
    parser.add_argument(
        "--local-ranks",
        default="3,3,3",
        help="comma-separated rank caps for each site on both sides",
    )
    args = parser.parse_args()
    local_ranks = tuple(int(value) for value in args.local_ranks.split(","))
    if len(local_ranks) != 3 or any(
        rank not in (1, 2, 3) for rank in local_ranks
    ):
        raise ValueError("--local-ranks must contain three values in 1,2,3")
    rng = np.random.default_rng(args.seed)
    best = float("inf")
    for start in range(args.starts):
        left = [
            truncate_local_rank(random_unit(rng), local_ranks[site])
            for site in range(3)
        ]
        right = [
            truncate_local_rank(random_unit(rng), local_ranks[site])
            for site in range(3)
        ]
        for _ in range(args.sweeps):
            for site in range(3):
                _, frame = np.linalg.eigh(
                    local_effective(left, right, site, True)
                )
                left[site] = truncate_local_rank(
                    frame[:, 0], local_ranks[site]
                )
                _, frame = np.linalg.eigh(
                    local_effective(left, right, site, False)
                )
                right[site] = truncate_local_rank(
                    frame[:, 0], local_ranks[site]
                )
        value = objective(left, right)
        if value < best:
            best = value
            print("best", start, repr(best), flush=True)
            if args.output:
                np.savez(
                    args.output,
                    value=np.array([value]),
                    left=np.stack(left),
                    right=np.stack(right),
                )


if __name__ == "__main__":
    main()
