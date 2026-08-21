#!/usr/bin/env python3
"""Unrestricted complex rank-two search for the Haar block-Gram system.

This is discovery code only.  It minimizes the exact residual

    beta_i = gamma |I>><<I|,   rho_i^L = rho_i^R = I/3

at all three sites with C=A B^*.  Analytic first derivatives avoid a
large finite-difference search.
"""

from __future__ import annotations

import argparse
import numpy as np
from scipy.optimize import minimize

from probe_n3_haar_equality_kernel import local_L


def block_matrix(c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3, 3, 3, 3, 3, 3))
    axes = [site, 3 + site] + [
        j for j in range(6) if j not in (site, 3 + site)
    ]
    # Columns are vectorized 9 by 9 environment blocks.
    return np.transpose(t, axes).reshape((9, 81)).T


def unblock_matrix(k: np.ndarray, site: int) -> np.ndarray:
    axes = [site, 3 + site] + [
        j for j in range(6) if j not in (site, 3 + site)
    ]
    inv = np.argsort(axes)
    return np.transpose(k.T.reshape((3,) * 6), inv).reshape((27, 27))


def rest_L(c: np.ndarray, site: int) -> np.ndarray:
    out = c
    for other in range(3):
        if other != site:
            out = local_L(out, other)
    return out


def one_body_left(c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3, 3, 3, 3, 3, 3))
    # (CC*) local reduction, evaluated by direct contraction.
    axes = [site] + [j for j in range(6) if j != site]
    m = np.transpose(t, axes).reshape((3, -1))
    return m @ m.conj().T


def one_body_right(c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3, 3, 3, 3, 3, 3))
    col = 3 + site
    axes = [col] + [j for j in range(6) if j != col]
    m = np.transpose(t, axes).reshape((3, -1))
    return m.conj() @ m.T


def lift_left(r: np.ndarray, c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3,) * 6)
    out = np.tensordot(r, t, axes=(1, site))
    return np.moveaxis(out, 0, site).reshape((27, 27))


def lift_right(c: np.ndarray, r: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3,) * 6)
    col = 3 + site
    # Right multiplication: contract the old column with row index of r.
    out = np.tensordot(t, r, axes=(col, 0))
    return np.moveaxis(out, -1, col).reshape((27, 27))


def pack(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    z = np.concatenate((a.reshape(-1), b.reshape(-1)))
    return np.concatenate((z.real, z.imag))


def unpack(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = 27 * 2
    z = x[: 2 * n] + 1j * x[2 * n :]
    return z[:n].reshape((27, 2)), z[n:].reshape((27, 2))


def objective(
    x: np.ndarray,
    marginal_weight: float,
    sites: tuple[int, ...],
    marginal_sites: tuple[int, ...],
    fixed_gamma: float | None,
) -> tuple[float, np.ndarray]:
    a, b = unpack(x)
    c = a @ b.conj().T
    target_vec = np.eye(3).reshape(-1)
    target = np.outer(target_vec, target_vec)
    betas: list[np.ndarray] = []
    ks: list[np.ndarray] = []
    tks: list[np.ndarray] = []
    for site in sites:
        k = block_matrix(c, site)
        tk = block_matrix(rest_L(c, site), site)
        ks.append(k)
        tks.append(tk)
        betas.append(k.conj().T @ tk)
    gamma = (
        fixed_gamma
        if fixed_gamma is not None
        else sum(np.vdot(target, z).real for z in betas)
        / (9.0 * len(sites))
    )
    residuals = [z - gamma * target for z in betas]
    value = sum(np.vdot(z, z).real for z in residuals)

    # With df=2 Re Tr(G* dc), each beta residual contributes
    # G_K=2 T K R.  Convert the block gradient back to C.
    gc = np.zeros_like(c)
    for site, (r, tk) in enumerate(zip(residuals, tks)):
        gk = 2.0 * tk @ r
        gc += unblock_matrix(gk, site)

    eye = np.eye(3) / 3
    marginal_residual = 0.0
    for site in marginal_sites:
        rl = one_body_left(c, site) - eye
        rr = one_body_right(c, site) - eye
        marginal_residual += np.vdot(rl, rl).real + np.vdot(rr, rr).real
        gc += marginal_weight * (
            2.0 * lift_left(rl, c, site)
            + 2.0 * lift_right(c, rr, site)
        )
    value += marginal_weight * marginal_residual

    ga = gc @ b
    gb = gc.conj().T @ a
    gz = np.concatenate((ga.reshape(-1), gb.reshape(-1)))
    grad = np.concatenate((2 * gz.real, 2 * gz.imag))
    return float(value), grad


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--weight", type=float, default=10.0)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--sites", default="012")
    parser.add_argument("--marginal-sites", default="012")
    parser.add_argument("--gamma", type=float)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    a = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    b = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    x0 = pack(a, b)
    sites = tuple(int(s) for s in args.sites)
    marginal_sites = tuple(int(s) for s in args.marginal_sites)
    result = minimize(
        lambda x: objective(
            x, args.weight, sites, marginal_sites, args.gamma
        ),
        x0,
        jac=True,
        method="L-BFGS-B",
        options={"maxiter": args.maxiter, "ftol": 1e-14, "gtol": 1e-10},
    )
    print(result.message)
    print("iterations", result.nit)
    print("objective", result.fun)
    a, b = unpack(result.x)
    c = a @ b.conj().T
    print("rank singular values", np.linalg.svd(c, compute_uv=False)[:4])
    for site in range(3):
        k = block_matrix(c, site)
        tk = block_matrix(rest_L(c, site), site)
        beta = k.conj().T @ tk
        d = np.eye(3).reshape(-1)
        gamma = np.vdot(np.outer(d, d), beta).real / 9
        print(
            "site", site,
            "gamma", gamma,
            "beta residual", np.linalg.norm(beta - gamma * np.outer(d, d)),
            "rhoL", np.linalg.eigvalsh(one_body_left(c, site)),
            "rhoR", np.linalg.eigvalsh(one_body_right(c, site)),
        )


if __name__ == "__main__":
    main()
