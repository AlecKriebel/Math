#!/usr/bin/env python3
"""Finite-difference and d=4 calibration checks for the full-U(6) search."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import color_face_d6_search as base
from d6_threecolor_full_relative_search import FullRelativeModel


def main() -> None:
    seed = 26072965
    rng = np.random.default_rng(seed)
    d = 6
    mixing = base.random_unitary(d, rng, "complex")
    model = FullRelativeModel(3, 2, mixing)
    blocks = [
        base.random_reflection(4, rng, "complex")
        for _ in model.block_labels
    ]
    h = model.assemble(blocks)
    value, gradient, _ = base.objective_gradient(h, d)
    directions, generator = model.block_gradients(gradient, blocks)
    original_mixing = model.mixing.copy()

    print(f"seed={seed}")
    print(
        "direction=combined nine Grassmann block directions "
        "plus arbitrary U(6) direction"
    )
    for epsilon in (1e-4, 1e-5, 3e-6, 1e-6):
        model.mixing = original_mixing
        plus_blocks, plus_mixing = model.trial_full(
            blocks, directions, generator, epsilon
        )
        model.mixing = plus_mixing
        plus = base.objective_gradient(model.assemble(plus_blocks), d)[0]

        model.mixing = original_mixing
        minus_blocks, minus_mixing = model.trial_full(
            blocks, directions, generator, -epsilon
        )
        model.mixing = minus_mixing
        minus = base.objective_gradient(model.assemble(minus_blocks), d)[0]

        central = (plus - minus) / (2 * epsilon)
        forward = (plus - value) / epsilon
        backward = (value - minus) / epsilon
        print(
            f"epsilon={epsilon:g} central_derivative={central} "
            f"forward={forward} backward={backward}"
        )
    model.mixing = original_mixing

    candidate = Path(
        "exceptional_ybe_spectrum/results/color_face_candidates/"
        "color_face_mixed_d4_2x2_complex_random_mixopt1_seed26073114.npz"
    )
    saved = np.load(candidate)
    d4_model = FullRelativeModel(
        2, 2, np.kron(saved["mixing"], np.eye(2))
    )
    reassembled = d4_model.assemble(list(saved["blocks"]))
    residual = base.objective_gradient(reassembled, 4)[2]
    difference = np.linalg.norm(reassembled - saved["h"])
    print(f"d4_calibration_candidate={candidate}")
    print(f"d4_calibration_residual_frobenius={residual}")
    print(f"d4_reassembly_difference_frobenius={difference}")

    assert central < 0
    assert abs(forward - backward) < 1
    assert residual < 1e-9
    assert difference == 0
    print("PASS")


if __name__ == "__main__":
    main()
