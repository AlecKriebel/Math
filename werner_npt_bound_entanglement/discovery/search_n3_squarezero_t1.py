"""Discovery search for the sharp square-zero marginal inequality.

This is not a verifier.  It maximizes

    sum_i ||Tr_i C||_2^2 / ||C||_2^2

over C = U X W^*, where [U W] is a four-frame in (C^3)^tensor 3.
The orthogonality W^* U = 0 makes C^2 = 0 and rank(C) <= 2.
"""

from __future__ import annotations

import argparse
import numpy as np


DIMS = (3, 3, 3)
D = 27


def partial_trace_one(c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape(DIMS + DIMS)
    t = np.trace(t, axis1=site, axis2=site + 3)
    return t.reshape(9, 9)


def partial_trace(c: np.ndarray, sites: tuple[int, ...]) -> np.ndarray:
    t = c.reshape(DIMS + DIMS)
    n = 3
    for site in sorted(sites, reverse=True):
        t = np.trace(t, axis1=site, axis2=site + n)
        n -= 1
    return t.reshape(3**n, 3**n)


def trace_adjoint(b: np.ndarray, sites: tuple[int, ...]) -> np.ndarray:
    # Direct index implementation of the adjoint of a simultaneous trace.
    remaining = tuple(i for i in range(3) if i not in sites)
    bt = b.reshape((3,) * (2 * len(remaining)))
    out = np.zeros(DIMS + DIMS, dtype=np.complex128)
    for traced_values in np.ndindex(*(3 for _ in sites)):
        sl: list[int | slice] = [slice(None)] * 6
        for site, value in zip(sites, traced_values):
            sl[site] = value
            sl[site + 3] = value
        out[tuple(sl)] = bt
    return out.reshape(D, D)


def marginal_operator(c: np.ndarray) -> np.ndarray:
    return sum(
        trace_adjoint(partial_trace_one(c, site), (site,))
        for site in range(3)
    )


def endpoint_operator(c: np.ndarray) -> np.ndarray:
    out = c - marginal_operator(c) / 2
    for sites in ((0, 1), (0, 2), (1, 2)):
        out += trace_adjoint(partial_trace(c, sites), sites) / 4
    out -= np.trace(c) * np.eye(D) / 8
    return out


def orthonormalize(z: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1)
    return q * phases.conj()


def fixed_frame_extreme(
    z: np.ndarray, objective: str
) -> tuple[float, np.ndarray]:
    u, w = z[:, :2], z[:, 2:]
    units = [
        np.outer(u[:, a], w[:, b].conj())
        for a in range(2)
        for b in range(2)
    ]
    operator = marginal_operator if objective == "t1" else endpoint_operator
    gram = np.array(
        [
            [np.vdot(e, operator(f)) for f in units]
            for e in units
        ]
    )
    gram = (gram + gram.conj().T) / 2
    vals, vecs = np.linalg.eigh(gram)
    index = -1 if objective == "t1" else 0
    return float(vals[index]), vecs[:, index].reshape(2, 2)


def optimize(
    z: np.ndarray, steps: int, rate: float, objective: str
) -> tuple[float, np.ndarray, np.ndarray]:
    sign = 1 if objective == "t1" else -1
    best = (sign * -np.inf, z.copy(), np.zeros((2, 2), dtype=np.complex128))
    for step in range(steps):
        value, x = fixed_frame_extreme(z, objective)
        if sign * value > sign * best[0]:
            best = (value, z.copy(), x.copy())
        u, w = z[:, :2], z[:, 2:]
        c = u @ x @ w.conj().T
        operator = marginal_operator if objective == "t1" else endpoint_operator
        y = sign * (operator(c) - value * c)
        gu = 2 * y @ w @ x.conj().T
        gw = 2 * y.conj().T @ u @ x
        g = np.column_stack((gu, gw))
        tangent = g - z @ ((z.conj().T @ g + g.conj().T @ z) / 2)
        trial_rate = rate / np.sqrt(1 + step / 100)
        z = orthonormalize(z + trial_rate * tangent)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--rate", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--objective", choices=("t1", "q"), default="q")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    sign = 1 if args.objective == "t1" else -1
    global_best = (sign * -np.inf, None, None)
    for start in range(args.starts):
        z = orthonormalize(
            rng.normal(size=(D, 4)) + 1j * rng.normal(size=(D, 4))
        )
        best = optimize(z, args.steps, args.rate, args.objective)
        if sign * best[0] > sign * global_best[0]:
            global_best = best
        print(start, best[0], "global", global_best[0], flush=True)
    value, z, x = global_best
    np.savez(f"n3_squarezero_{args.objective}_best.npz", value=value, z=z, x=x)


if __name__ == "__main__":
    main()
