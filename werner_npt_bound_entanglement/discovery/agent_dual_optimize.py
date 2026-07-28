"""Floating-point search for violations of a strengthened endpoint conjecture.

Conjectured discovery inequality:
    Q_n(C) >= 2**(-n) * (s_1(C)-s_2(C))**2
for rank(C) <= 2.  This script is not a verifier.
"""

import argparse
import numpy as np
from scipy.optimize import minimize


def orthonormalize(raw: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(raw)
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1
    return q * signs


def traces(c: np.ndarray, d: int, n: int, subset: int) -> np.ndarray:
    tensor = c.reshape((d,) * (2 * n))
    remaining = n
    # Trace in descending order so original axis labels stay valid.
    for i in reversed(range(n)):
        if subset & (1 << i):
            tensor = np.trace(tensor, axis1=i, axis2=remaining + i)
            remaining -= 1
    return tensor.reshape(d**remaining, d**remaining)


def q_value(c: np.ndarray, d: int, n: int) -> float:
    total = 0.0
    for subset in range(1 << n):
        contracted = traces(c, d, n, subset)
        total += (-0.5) ** bin(subset).count("1") * np.vdot(
            contracted, contracted
        ).real
    return total


def unpack(x: np.ndarray, dim: int, fixed_theta=None):
    block = 2 * dim
    u = orthonormalize(x[:block].reshape(dim, 2))
    v = orthonormalize(x[block : 2 * block].reshape(dim, 2))
    theta = (
        fixed_theta
        if fixed_theta is not None
        else np.pi / (2 * (1 + np.exp(-x[-1])))
    )
    singular = np.array([np.cos(theta), np.sin(theta)])
    return u, v, singular


def objective(x: np.ndarray, d: int, n: int, fixed_theta=None) -> float:
    dim = d**n
    u, v, singular = unpack(x, dim, fixed_theta)
    c = (u * singular) @ v.T
    return q_value(c, d, n) - 2.0 ** (-n) * (singular[0] - singular[1]) ** 2


def run(d: int, n: int, starts: int, seed: int, maxiter: int, fixed_theta=None):
    rng = np.random.default_rng(seed)
    dim = d**n
    best = None
    for start in range(starts):
        x0 = rng.normal(size=4 * dim + 1)
        result = minimize(
            objective,
            x0,
            args=(d, n, fixed_theta),
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": 1e-13, "gtol": 1e-9},
        )
        if best is None or result.fun < best.fun:
            best = result
        print(start, result.fun, result.nit, result.success)
    u, v, singular = unpack(best.x, dim, fixed_theta)
    print("best", best.fun)
    print("singular", singular)
    print("U", np.array2string(u, precision=6, suppress_small=True))
    print("V", np.array2string(v, precision=6, suppress_small=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=int, default=3)
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--starts", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument(
        "--theta", type=float, default=None, help="Fix theta with singular=(cos,sin)"
    )
    args = parser.parse_args()
    run(args.d, args.n, args.starts, args.seed, args.maxiter, args.theta)
