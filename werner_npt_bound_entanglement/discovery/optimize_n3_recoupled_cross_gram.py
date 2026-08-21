#!/usr/local/bin/python
"""Discovery search for the stronger four-column cross-Gram lemma.

The singular values are presently fixed equal.  Four two-column
isometries X,Y,U,V determine

    E_ij = conjugate(X_i) tensor U_j,
    F_ij = conjugate(Y_i) tensor V_j.

The objective is

    Tr((E*ZE)(F*ZF)) - ||E*Z conjugate(F)||_F^2,

where Z=2I-3Pi_2.  Floating-point output is not evidence.
"""

from __future__ import annotations

import argparse

import numpy as np

from optimize_n3_recoupled_rank2 import N, apply_y_left, basis_index


def isometry(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    return np.linalg.qr(matrix)[0][:, :2]


def retract(matrix: np.ndarray) -> np.ndarray:
    return np.linalg.qr(matrix)[0][:, :2]


def tangent(frame: np.ndarray, gradient: np.ndarray) -> np.ndarray:
    compression = frame.conjugate().T @ gradient
    hermitian = (compression + compression.conjugate().T) / 2
    return gradient - frame @ hermitian


def columns(
    first: np.ndarray, second: np.ndarray
) -> np.ndarray:
    return np.einsum(
        "pi,qj->pqij", first.conjugate(), second
    ).reshape(N * N, 4)


def value_and_gradient(
    x: np.ndarray,
    y: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    true_objective: bool = False,
) -> tuple[float, tuple[np.ndarray, ...]]:
    e = columns(x, u)
    f = columns(y, v)
    ze = apply_y_left(e)
    zf = apply_y_left(f)
    zbarf = apply_y_left(f.conjugate())
    ge = e.conjugate().T @ ze
    gf = f.conjugate().T @ zf
    h = e.conjugate().T @ zbarf
    if true_objective:
        value = (np.trace(ge @ gf) - np.trace(h @ h.conjugate())).real
        gradient_e = apply_y_left(
            e @ gf - f.conjugate() @ h.conjugate()
        )
        gradient_f = apply_y_left(
            f @ ge - e.conjugate() @ h.conjugate().T
        )
    else:
        value = (np.trace(ge @ gf) - np.vdot(h, h)).real
        gradient_e = apply_y_left(
            e @ gf - f.conjugate() @ h.conjugate().T
        )
        gradient_f = apply_y_left(
            f @ ge - e.conjugate() @ h.conjugate()
        )
    gradient_e = gradient_e.reshape(N, N, 2, 2)
    gradient_f = gradient_f.reshape(N, N, 2, 2)

    gradient_x = np.einsum(
        "qj,pqij->pi", u, gradient_e.conjugate(), optimize=True
    )
    gradient_u = np.einsum(
        "pi,pqij->qj", x, gradient_e, optimize=True
    )
    gradient_y = np.einsum(
        "qj,pqij->pi", v, gradient_f.conjugate(), optimize=True
    )
    gradient_v = np.einsum(
        "pi,pqij->qj", y, gradient_f, optimize=True
    )
    gradients = tuple(
        tangent(frame, gradient)
        for frame, gradient in (
            (x, gradient_x),
            (y, gradient_y),
            (u, gradient_u),
            (v, gradient_v),
        )
    )
    return float(value), gradients


def boundary_frames() -> tuple[np.ndarray, ...]:
    eye = np.eye(N, dtype=complex)
    x = np.stack(
        [eye[:, basis_index(0, 0, k)] for k in range(2)], axis=1
    )
    y = np.stack(
        [eye[:, basis_index(1, 0, k)] for k in range(2)], axis=1
    )
    u = np.stack(
        [eye[:, basis_index(0, 1, k)] for k in range(2)], axis=1
    )
    v = np.stack(
        [eye[:, basis_index(1, 1, k)] for k in range(2)], axis=1
    )
    return x, y, u, v


def gradient_check(
    rng: np.random.Generator,
    frames: tuple[np.ndarray, ...],
    true_objective: bool,
) -> None:
    value, gradients = value_and_gradient(
        *frames, true_objective=true_objective
    )
    directions = []
    for frame in frames:
        raw = rng.normal(size=frame.shape) + 1j * rng.normal(
            size=frame.shape
        )
        directions.append(tangent(frame, raw))
    epsilon = 1e-6
    plus = [
        retract(frame + epsilon * direction)
        for frame, direction in zip(frames, directions)
    ]
    minus = [
        retract(frame - epsilon * direction)
        for frame, direction in zip(frames, directions)
    ]
    numeric = (
        value_and_gradient(
            *plus, true_objective=true_objective
        )[0]
        - value_and_gradient(
            *minus, true_objective=true_objective
        )[0]
    ) / (2 * epsilon)
    analytic = 2 * sum(
        np.vdot(direction, gradient).real
        for direction, gradient in zip(directions, gradients)
    )
    print("gradient check", value, numeric, analytic, numeric - analytic)


def optimize(
    frames: tuple[np.ndarray, ...],
    steps: int,
    true_objective: bool,
) -> tuple[float, tuple[np.ndarray, ...]]:
    value = value_and_gradient(
        *frames, true_objective=true_objective
    )[0]
    step_size = 0.1
    for step in range(steps):
        current, gradients = value_and_gradient(
            *frames, true_objective=true_objective
        )
        accepted = False
        trial_step = step_size
        for _ in range(15):
            trial = tuple(
                retract(frame - trial_step * gradient)
                for frame, gradient in zip(frames, gradients)
            )
            trial_value = value_and_gradient(
                *trial, true_objective=true_objective
            )[0]
            if trial_value < current - 1e-13:
                frames = trial
                value = trial_value
                step_size = min(1.0, trial_step * 1.25)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
        if step % 20 == 0:
            print("  step", step, "value", repr(value), flush=True)
    return value, frames


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--true", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    gradient_check(
        rng,
        tuple(isometry(rng) for _ in range(4)),
        args.true,
    )
    seeds = [boundary_frames()]
    seeds.extend(
        tuple(isometry(rng) for _ in range(4))
        for _ in range(args.starts)
    )
    best = np.inf
    for start, frames in enumerate(seeds):
        value, _ = optimize(frames, args.steps, args.true)
        best = min(best, value)
        print("start", start, "value", repr(value), "best", repr(best))


if __name__ == "__main__":
    main()
