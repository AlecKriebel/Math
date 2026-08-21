#!/usr/local/bin/python
"""Discovery search for a negative eigenvalue of the 4x4 exterior Gram W."""

from __future__ import annotations

import argparse

import numpy as np

from optimize_n3_recoupled_cross_gram import (
    boundary_frames,
    columns,
    isometry,
    retract,
    tangent,
)
from optimize_n3_recoupled_rank2 import N, apply_y_left


def data(frames: tuple[np.ndarray, ...]):
    x, y, u, v = frames
    e = columns(x, u)
    f = columns(y, v)
    ze = apply_y_left(e)
    zf = apply_y_left(f)
    a = e.conjugate().T @ ze
    b = f.conjugate().T @ zf
    h = e.conjugate().T @ apply_y_left(f.conjugate())
    w = a * b.conjugate() - h * h.T.conjugate()
    w = (w + w.conjugate().T) / 2
    values, vectors = np.linalg.eigh(w)
    return float(values[0]), vectors[:, 0], e, f


def value_and_gradient(
    frames: tuple[np.ndarray, ...],
) -> tuple[float, tuple[np.ndarray, ...]]:
    value, coefficient, e, f = data(frames)
    coefficient_matrix = np.diag(coefficient)
    ep = e @ coefficient_matrix
    zep = apply_y_left(ep)
    zf = apply_y_left(f)
    zbarf = apply_y_left(f.conjugate())
    ge = ep.conjugate().T @ zep
    gf = f.conjugate().T @ zf
    h = ep.conjugate().T @ zbarf
    gradient_ep = apply_y_left(
        ep @ gf - f.conjugate() @ h.conjugate()
    )
    gradient_f = apply_y_left(
        f @ ge - ep.conjugate() @ h.conjugate().T
    )
    gradient_e = gradient_ep @ coefficient_matrix.conjugate().T
    gradient_e = gradient_e.reshape(N, N, 2, 2)
    gradient_f = gradient_f.reshape(N, N, 2, 2)

    x, y, u, v = frames
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
    return value, gradients


def gradient_check(
    rng: np.random.Generator, frames: tuple[np.ndarray, ...]
) -> None:
    value, gradients = value_and_gradient(frames)
    directions = []
    for frame in frames:
        raw = rng.normal(size=frame.shape) + 1j * rng.normal(
            size=frame.shape
        )
        directions.append(tangent(frame, raw))
    epsilon = 1e-6
    plus = tuple(
        retract(frame + epsilon * direction)
        for frame, direction in zip(frames, directions)
    )
    minus = tuple(
        retract(frame - epsilon * direction)
        for frame, direction in zip(frames, directions)
    )
    numeric = (data(plus)[0] - data(minus)[0]) / (2 * epsilon)
    analytic = 2 * sum(
        np.vdot(direction, gradient).real
        for direction, gradient in zip(directions, gradients)
    )
    print("gradient check", value, numeric, analytic, numeric - analytic)


def optimize(frames: tuple[np.ndarray, ...], steps: int):
    value = data(frames)[0]
    step_size = 0.1
    for step in range(steps):
        current, gradients = value_and_gradient(frames)
        trial_step = step_size
        accepted = False
        for _ in range(15):
            trial = tuple(
                retract(frame - trial_step * gradient)
                for frame, gradient in zip(frames, gradients)
            )
            trial_value = data(trial)[0]
            if trial_value < current - 1e-13:
                value = trial_value
                frames = trial
                step_size = min(1.0, trial_step * 1.25)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
        if step % 20 == 0:
            print("  step", step, "value", repr(value), flush=True)
    return value, frames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=150)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--output")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    gradient_check(rng, tuple(isometry(rng) for _ in range(4)))
    seeds = [boundary_frames()]
    seeds.extend(
        tuple(isometry(rng) for _ in range(4))
        for _ in range(args.starts)
    )
    best = np.inf
    best_frames = None
    for start, frames in enumerate(seeds):
        value, frames = optimize(frames, args.steps)
        if value < best:
            best = value
            best_frames = frames
            if args.output:
                coefficient = data(frames)[1]
                np.savez(
                    args.output,
                    value=value,
                    coefficient=coefficient,
                    x=frames[0],
                    y=frames[1],
                    u=frames[2],
                    v=frames[3],
                )
        print("start", start, "value", repr(value), "best", repr(best))


if __name__ == "__main__":
    main()
