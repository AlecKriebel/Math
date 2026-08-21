#!/usr/local/bin/python
"""Discovery optimizer for grouped replica-Schmidt rank at most two.

This is floating-point discovery code.  It evaluates

    <vec(A) vec(B), B_rec vec(A) vec(B)>

through the realigned wedge formula and uses an analytic Euclidean
gradient followed by best-rank-two projection.
"""

from __future__ import annotations

import argparse

import numpy as np


D = 3
N = D**3
OP = N * N


def digit(index: int, site: int) -> int:
    return (index // (D**site)) % D


def scalar_groups(site: int) -> np.ndarray:
    """The 81 triples averaged by the one-site scalar projection."""
    place = D**site
    groups = []
    for row in range(N):
        if digit(row, site) != 0:
            continue
        for column in range(N):
            if digit(column, site) != 0:
                continue
            groups.append(
                [
                    (row + value * place) * N
                    + column
                    + value * place
                    for value in range(D)
                ]
            )
    return np.array(groups)


GROUPS = [scalar_groups(site) for site in range(3)]


def scalar_part_batch(batch: np.ndarray, site: int) -> np.ndarray:
    out = np.zeros_like(batch)
    groups = GROUPS[site]
    means = batch[groups, :].mean(axis=1)
    out[groups, :] = means[:, None, :]
    return out


def exact_sector_batch(batch: np.ndarray, traceless_mask: int) -> np.ndarray:
    out = batch
    for site in range(3):
        scalar = scalar_part_batch(out, site)
        out = out - scalar if (traceless_mask >> site) & 1 else scalar
    return out


def apply_y_left(batch: np.ndarray) -> np.ndarray:
    out = 2 * batch
    for mask in (3, 5, 6):
        out = out - 3 * exact_sector_batch(batch, mask)
    return out


def apply_y_both(matrix: np.ndarray) -> np.ndarray:
    return apply_y_left(apply_y_left(matrix.T).T)


def wedge(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    raw = np.einsum("pr,qs->pqrs", a.conjugate(), b)
    return (raw - raw.transpose(2, 3, 0, 1)).reshape(OP, OP)


def value_and_gradient(
    a: np.ndarray, b: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    w = wedge(a, b)
    z = apply_y_both(w).reshape(N, N, N, N)
    value = 0.5 * np.vdot(w, z.reshape(OP, OP)).real

    ga_coefficient = np.einsum(
        "qs,pqrs->pr", b.conjugate(), z, optimize=True
    ) - np.einsum(
        "sq,rqps->pr", b.conjugate(), z, optimize=True
    )
    grad_a = ga_coefficient.conjugate()
    grad_b = np.einsum(
        "pr,pqrs->qs", a, z, optimize=True
    ) - np.einsum(
        "rp,psrq->qs", a, z, optimize=True
    )
    return float(value), grad_a, grad_b


def normalize(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.linalg.norm(matrix)


def truncate_rank_two(matrix: np.ndarray) -> np.ndarray:
    left, singular, right = np.linalg.svd(matrix, full_matrices=False)
    return normalize((left[:, :2] * singular[:2]) @ right[:2, :])


def random_rank_two(rng: np.random.Generator) -> np.ndarray:
    left = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    right = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    return normalize(left @ right.conjugate().T)


def basis_index(a: int, b: int, c: int) -> int:
    return a + D * b + D * D * c


def boundary(side: str, rank: int) -> np.ndarray:
    out = np.zeros((N, N), dtype=complex)
    middle = 0 if side == "left" else 1
    for value in range(rank):
        row = basis_index(0, middle, value)
        column = basis_index(1, middle, value)
        out[row, column] = 1 / np.sqrt(rank)
    return out


def finite_difference_check(
    rng: np.random.Generator, a: np.ndarray, b: np.ndarray
) -> None:
    value, grad_a, grad_b = value_and_gradient(a, b)
    da = rng.normal(size=a.shape) + 1j * rng.normal(size=a.shape)
    db = rng.normal(size=b.shape) + 1j * rng.normal(size=b.shape)
    da /= np.linalg.norm(da)
    db /= np.linalg.norm(db)
    epsilon = 1e-6
    plus = value_and_gradient(a + epsilon * da, b + epsilon * db)[0]
    minus = value_and_gradient(a - epsilon * da, b - epsilon * db)[0]
    numeric = (plus - minus) / (2 * epsilon)
    analytic = (
        np.vdot(da, grad_a).real + np.vdot(db, grad_b).real
    )
    print("gradient check", value, numeric, analytic, numeric - analytic)


def optimize(
    a: np.ndarray,
    b: np.ndarray,
    sweeps: int,
    initial_step: float,
) -> tuple[float, np.ndarray, np.ndarray]:
    value = value_and_gradient(a, b)[0]
    step = initial_step
    for sweep in range(sweeps):
        current, grad_a, grad_b = value_and_gradient(a, b)
        accepted = False
        trial_step = step
        for _ in range(15):
            trial_a = truncate_rank_two(a - trial_step * grad_a)
            trial_b = truncate_rank_two(b - trial_step * grad_b)
            trial = value_and_gradient(trial_a, trial_b)[0]
            if trial < current - 1e-13:
                a, b, value = trial_a, trial_b, trial
                step = min(2.0, trial_step * 1.25)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            break
        if sweep % 20 == 0:
            print("  sweep", sweep, "value", repr(value), "step", step)
    return value, a, b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=10)
    parser.add_argument("--sweeps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--output")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    rank3_value = value_and_gradient(
        boundary("left", 3), boundary("right", 3)
    )[0]
    rank2_value = value_and_gradient(
        boundary("left", 2), boundary("right", 2)
    )[0]
    print("known rank3", rank3_value)
    print("rank2 boundary", rank2_value)
    finite_difference_check(
        rng, boundary("left", 2), boundary("right", 2)
    )

    best = (float("inf"), None, None)
    seeds = [
        (boundary("left", 2), boundary("right", 2)),
    ]
    seeds.extend(
        (random_rank_two(rng), random_rank_two(rng))
        for _ in range(args.starts)
    )
    for start, (a, b) in enumerate(seeds):
        value, a, b = optimize(a, b, args.sweeps, 0.1)
        print("start", start, "final", repr(value))
        if value < best[0]:
            best = (value, a, b)
            if args.output:
                np.savez(args.output, value=value, a=a, b=b)
    print("best", repr(best[0]))


if __name__ == "__main__":
    main()
