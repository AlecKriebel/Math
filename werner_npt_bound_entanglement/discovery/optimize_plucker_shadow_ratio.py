#!/usr/bin/env python3
"""Maximize the pair/singleton complement-defect ratio.

For a rank-two four-qutrit projection put

    delta_T = A_T - A_complement(T).

This discovery script searches for the largest value of

    sum_{|T|=2, T representative} delta_T^2
    --------------------------------------------------
                sum_{|T|=1} delta_T^2.

If this ratio has a finite universal bound, the four singleton balance
conditions force all pair balances.  Floating-point output is not a
certificate.
"""

from __future__ import annotations

import argparse

import numpy as np

from optimize_hodge_frames import load_frame
from search_balanced_weight3 import (
    real_inner,
    retract,
    tangent_projection,
    trace_maps,
)


SINGLES = (1, 2, 4, 8)
PAIR_REPRESENTATIVES = (3, 5, 6)


def defect_data(
    frame: np.ndarray,
) -> tuple[np.ndarray, list[np.ndarray]]:
    projection = frame @ frame.conj().T
    maps = trace_maps(projection)
    moments = np.array(
        [
            np.vdot(projection, maps[15 ^ subset]).real
            for subset in range(16)
        ]
    )
    subsets = SINGLES + PAIR_REPRESENTATIVES
    defects = np.array(
        [moments[subset] - moments[15 ^ subset] for subset in subsets]
    )
    gradients: list[np.ndarray] = []
    for subset in subsets:
        operator = maps[15 ^ subset] - maps[subset]
        gradients.append(
            tangent_projection(frame, 4 * operator @ frame)
        )
    return defects, gradients


def evaluate(
    frame: np.ndarray,
    need_gradient: bool,
    regularizer: float,
) -> tuple[float, np.ndarray | None, np.ndarray]:
    defects, gradients = defect_data(frame)
    singles = defects[:4]
    pairs = defects[4:]
    denominator = float(singles @ singles) + regularizer
    numerator = float(pairs @ pairs)
    ratio = numerator / denominator
    if not need_gradient:
        return ratio, None, defects
    numerator_gradient = 2 * sum(
        pairs[index] * gradients[4 + index] for index in range(3)
    )
    denominator_gradient = 2 * sum(
        singles[index] * gradients[index] for index in range(4)
    )
    gradient = (
        denominator * numerator_gradient
        - numerator * denominator_gradient
    ) / denominator**2
    return ratio, gradient, defects


def maximize(
    frame: np.ndarray,
    iterations: int,
    initial_step: float,
    regularizer: float,
) -> tuple[np.ndarray, float]:
    step = initial_step
    best = frame.copy()
    best_value = evaluate(frame, False, regularizer)[0]
    for iteration in range(iterations):
        value, gradient, defects = evaluate(
            frame, True, regularizer
        )
        assert gradient is not None
        norm_squared = real_inner(gradient, gradient)
        if value > best_value:
            best_value = value
            best = frame.copy()
        if iteration % 25 == 0:
            print(
                f"iter={iteration} ratio={value:.12g} "
                f"single2={defects[:4] @ defects[:4]:.3e} "
                f"pair2={defects[4:] @ defects[4:]:.3e} "
                f"grad2={norm_squared:.3e}"
            )
        if norm_squared < 1e-20:
            break
        accepted = False
        trial_step = step
        for _ in range(30):
            candidate = retract(frame + trial_step * gradient)
            candidate_value = evaluate(
                candidate, False, regularizer
            )[0]
            if candidate_value >= (
                value + 1e-6 * trial_step * norm_squared
            ):
                frame = candidate
                step = min(initial_step, 1.25 * trial_step)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
    return best, best_value


def random_frame(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = rng.normal(size=(81, 2)) + 1j * rng.normal(size=(81, 2))
    return retract(matrix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--regularizer", type=float, default=1e-16)
    parser.add_argument("--output")
    args = parser.parse_args()

    overall = (-1.0, None, None)
    for restart in range(args.restarts):
        if restart == 0 and args.frame:
            u, v = load_frame(args.frame)
            frame = np.stack((u, v), axis=1)
        else:
            frame = random_frame(args.seed + restart)
        best, value = maximize(
            frame,
            args.iterations,
            args.step,
            args.regularizer,
        )
        defects = evaluate(best, False, args.regularizer)[2]
        print(
            f"restart={restart} best_ratio={value:.15g} "
            f"singles={defects[:4]} pairs={defects[4:]}"
        )
        if value > overall[0]:
            overall = (value, args.seed + restart, defects)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as target:
                    for index, row in enumerate(best):
                        target.write(
                            f"{index} {row[0].real:.17g} "
                            f"{row[0].imag:.17g} {row[1].real:.17g} "
                            f"{row[1].imag:.17g}\n"
                        )
    print("overall", overall)


if __name__ == "__main__":
    main()
