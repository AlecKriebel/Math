#!/usr/bin/env python3
"""Probe the odd-parity inequality exposed by phase superposition.

For matched purifications A,B with the same qubit marginal, the exact
phase-average identity gives

    D_even >= -(delta(A)+delta(B))/4.

Consequently D>=0 would follow from the strictly smaller candidate

    D_odd >= (delta(A)+delta(B))/4.

This script searches unrestricted complex orthonormal singular frames for
violations.  It is floating-point discovery code only.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np


def random_frame(rng: np.random.Generator, dimension: int) -> np.ndarray:
    matrix = rng.normal(size=(dimension, 2)) + 1j * rng.normal(
        size=(dimension, 2)
    )
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1)
    return q * phases.conj()


def reduced_pure(
    vector: np.ndarray,
    dims: tuple[int, ...],
    keep: tuple[int, ...],
) -> np.ndarray:
    tensor = vector.reshape(dims)
    complement = tuple(i for i in range(len(dims)) if i not in keep)
    matrix = np.transpose(tensor, keep + complement).reshape(
        np.prod([dims[i] for i in keep], dtype=int), -1
    )
    return matrix @ matrix.conj().T


def swap_moments(
    first: np.ndarray,
    second: np.ndarray,
    dims: tuple[int, ...],
) -> np.ndarray:
    moments = np.empty(1 << len(dims), dtype=float)
    parties = tuple(range(len(dims)))
    for mask in range(1 << len(dims)):
        keep = tuple(i for i in parties if (mask >> i) & 1)
        rho_first = reduced_pure(first, dims, keep)
        rho_second = reduced_pure(second, dims, keep)
        moments[mask] = np.vdot(rho_first, rho_second).real
    return moments


def sector_weights(moments: np.ndarray) -> np.ndarray:
    count = int(np.log2(len(moments)))
    out = np.empty_like(moments)
    for sector in range(1 << count):
        value = 0.0
        for mask, moment in enumerate(moments):
            value += (-1) ** ((sector & mask).bit_count()) * moment
        out[sector] = value / (1 << count)
    return out


def diagonal_defect(vector: np.ndarray, dims: tuple[int, ...]) -> float:
    moments = swap_moments(vector, vector, dims)
    # q_K and the complementary-purity form of delta.
    value = 3 * moments[1]
    for site in (1, 2, 3):
        value -= 2 * moments[1 | (1 << site)]
        value += moments[1 << site]
    return float(value)


def odd_even(weights: np.ndarray) -> tuple[float, float]:
    odd = 0.0
    even = 0.0
    for sector, weight in enumerate(weights):
        k = sector & 1
        r = (sector >> 1).bit_count()
        coefficient = (-1 if k else 1) * (3**r - 2) + 1
        target = coefficient / 2
        if (k + r) & 1:
            odd += target * weight
        else:
            even += target * weight
    return float(odd), float(even)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=int, default=3)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    physical_dimension = args.local**3
    dims = (2, args.local, args.local, args.local)
    best = None
    best_conditional = None
    minimum_odd = None

    for sample in range(args.samples):
        left = random_frame(rng, physical_dimension)
        right = random_frame(rng, physical_dimension)
        probability = rng.random()
        singular = np.sqrt([probability, 1 - probability])
        first = np.zeros(dims, dtype=complex)
        second = np.zeros(dims, dtype=complex)
        for logical in range(2):
            first[logical] = singular[logical] * left[:, logical].reshape(
                dims[1:]
            )
            second[logical] = singular[logical] * right[:, logical].reshape(
                dims[1:]
            )
        first = first.reshape(-1)
        second = second.reshape(-1)

        delta_first = diagonal_defect(first, dims)
        delta_second = diagonal_defect(second, dims)
        weights = sector_weights(swap_moments(first, second, dims))
        odd, even = odd_even(weights)
        gap = odd - (delta_first + delta_second) / 4
        record = (
            gap,
            odd + even,
            odd,
            even,
            delta_first,
            delta_second,
            probability,
        )
        if best is None or record[0] < best[0]:
            best = record
        if minimum_odd is None or odd < minimum_odd[0]:
            minimum_odd = (odd, record)
        if even < 0 and (
            best_conditional is None or gap < best_conditional[0]
        ):
            best_conditional = record

    print("best", best)
    print("minimum odd", minimum_odd)
    print("best with D_even < 0", best_conditional)


if __name__ == "__main__":
    main()
