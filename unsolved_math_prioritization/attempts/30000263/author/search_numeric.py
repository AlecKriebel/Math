#!/usr/bin/env python3
"""Finite exploratory search, never a mathematical certificate of the conjecture."""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import least_squares


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unpack(z, p, dim):
    x = np.zeros((p, dim))
    x[1, 0] = 1.0
    q = (p - 2) * dim
    x[2:] = z[:q].reshape((p - 2, dim))
    u = z[q:]
    norm = np.linalg.norm(u)
    require(math.isfinite(norm) and norm > 1e-14, "zero or invalid charge vector")
    return x, u / norm


def quantities(x, u):
    p = len(u)
    delta = x[:, None, :] - x[None, :, :]
    r = np.linalg.norm(delta, axis=2)
    r[np.diag_indices(p)] = np.inf
    require(np.isfinite(x).all() and np.isfinite(u).all(), "nonfinite inputs")
    require(float(np.min(r)) > 1e-10, "collision")
    A = 1.0 / r
    P = A @ u
    F = np.einsum("ijd,j->id", delta / r[:, :, None] ** 3, u)
    G = -2.0 * u[:, None] * F
    D = float(np.sum(A * A * u[None, :] ** 2))
    require(math.isfinite(D) and D > 0, "invalid denominator")
    return P, G, D, float(np.min(r))


def residual(z, p, dim):
    try:
        x, u = unpack(z, p, dim)
        P, G, D, _ = quantities(x, u)
        return np.r_[P / np.sqrt(D), G.ravel() / D]
    except ValueError:
        return np.full(p * (dim + 1), 1e8)


def run(starts, budget, seed):
    rng = np.random.default_rng(seed)
    rows = []
    for p, dim in [(6, 2), (6, 3), (7, 3), (8, 3)]:
        for k in range(starts):
            x = rng.normal(size=(p - 2, dim))
            u = rng.normal(size=p)
            z = np.r_[x.ravel(), u]
            fit = least_squares(residual, z, args=(p, dim), max_nfev=budget,
                                xtol=1e-10, ftol=1e-10, gtol=1e-10)
            x, u = unpack(fit.x, p, dim)
            P, G, D, sep = quantities(x, u)
            ratio = (float(P @ P) + float(np.max(np.abs(G)))) / D
            row = dict(p=p, dimension=dim, start=k, nfev=int(fit.nfev),
                       optimizer_status=int(fit.status), ratio_coordinate=ratio,
                       smooth_objective=float(fit.fun @ fit.fun),
                       min_separation=sep, positions=x.tolist(), charges=u.tolist())
            require(math.isfinite(ratio) and ratio > 0, "zero or invalid numeric outcome")
            rows.append(row)
            print(f"p={p}, d={dim}, start={k}, ratio={ratio:.9g}, nfev={fit.nfev}", file=sys.stderr)
    return dict(status="FINITE_EXPLORATION_NOT_A_PROOF", seed=seed,
                starts_per_family=starts, evaluation_budget_per_start=budget,
                numpy_version=np.__version__, scipy_version=scipy.__version__,
                objective="norm(P)^2/D + sum(G**2)/D**2; reported ratio is (norm(P)^2+max(abs(G)))/D",
                coordinate_gauge="x0=0, x1=(1,0,...); charges normalized in evaluations",
                limitations=["No interval arithmetic", "No exhaustion of configurations",
                             "No rigorous lower bound", "Optimizer termination is not a theorem"],
                rows=rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=int, default=6)
    ap.add_argument("--budget", type=int, default=500)
    ap.add_argument("--seed", type=int, default=30000263)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    require(args.starts > 0 and args.budget > 0, "positive search bounds required")
    result = run(args.starts, args.budget, args.seed)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
