#!/usr/bin/env python3
"""Finite-difference guard for the nonuniform cell-rank search."""

from __future__ import annotations

import numpy as np

import color_face_d6_search as base
import d6_threecolor_full_relative_search as uniform
import d6_threecolor_rankpattern_search as search


def main() -> None:
    seed = 26073699
    pattern_index = 1
    pattern = search.CELL_RANK_PATTERNS[pattern_index]
    rng = np.random.default_rng(seed)
    mixing = base.random_unitary(6, rng, "complex")
    model = uniform.FullRelativeModel(3, 2, mixing)
    blocks = [
        search.random_reflection_with_negative_rank(
            4, pattern[a][b], rng
        )
        for a, b in model.block_labels
    ]

    for block, rank in zip(
        blocks, (pattern[a][b] for a, b in model.block_labels)
    ):
        assert np.linalg.norm(block @ block - np.eye(4)) < 1e-12
        assert np.linalg.norm(block - block.conj().T) < 1e-12
        assert np.count_nonzero(np.linalg.eigvalsh(block) < 0) == rank

    h = model.assemble(blocks)
    assert abs(np.trace(h)) < 1e-12
    value, gradient, residual = base.objective_gradient(h, 6)
    directions, generator = model.block_gradients(gradient, blocks)
    original_mixing = model.mixing.copy()
    reference_derivative = np.zeros_like(h)
    for label, direction in zip(model.block_labels, directions):
        indices = model.block_indices(label)
        reference_derivative[np.ix_(indices, indices)] = direction
    pair_unitary = model.pair_unitary()
    pair_generator = np.kron(np.eye(6), generator)
    h_derivative = (
        pair_unitary
        @ reference_derivative
        @ pair_unitary.conj().T
        + pair_generator @ h
        - h @ pair_generator
    )
    predicted_derivative = float(np.vdot(gradient, h_derivative).real)

    print(f"seed={seed}")
    print(f"rank_pattern_index={pattern_index}")
    print(f"rank_pattern={pattern}")
    print(f"initial_residual_frobenius={residual}")
    print(f"predicted_directional_derivative={predicted_derivative}")
    derivatives = []
    for epsilon in (1e-4, 1e-5, 3e-6, 1e-6):
        model.mixing = original_mixing
        plus_blocks, plus_mixing = model.trial_full(
            blocks, directions, generator, epsilon
        )
        model.mixing = plus_mixing
        plus = base.objective_gradient(model.assemble(plus_blocks), 6)[0]

        model.mixing = original_mixing
        minus_blocks, minus_mixing = model.trial_full(
            blocks, directions, generator, -epsilon
        )
        model.mixing = minus_mixing
        minus = base.objective_gradient(model.assemble(minus_blocks), 6)[0]

        central = (plus - minus) / (2 * epsilon)
        forward = (plus - value) / epsilon
        backward = (value - minus) / epsilon
        derivatives.append((epsilon, central, forward, backward))
        print(
            f"epsilon={epsilon:g} central_derivative={central} "
            f"forward={forward} backward={backward}"
        )
    model.mixing = original_mixing

    assert predicted_derivative < 0
    relative_error = abs(
        derivatives[-1][1] - predicted_derivative
    ) / abs(predicted_derivative)
    print(f"central_difference_relative_error={relative_error}")
    assert relative_error < 1e-7
    print("PASS")


if __name__ == "__main__":
    main()
