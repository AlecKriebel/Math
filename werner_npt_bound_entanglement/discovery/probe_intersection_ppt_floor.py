#!/usr/bin/env python3
"""Numerically test whether a quantitative PPT floor closes diagonal-to-product.

Discovery only.  We generate separable two-qubit Gram operators K with
K >= (1/8) I, set G=K^Gamma, and compare

    max_x |x^* T x|^2 / <P_x,G P_x>

with

    max_{u,v} |v^* T u|^2 / <|u><v|,G |u><v|>.

If the second exceeds the first, then the PPT floor plus all diagonal
Hermitian rank-one tests is not sufficient by itself.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import differential_evolution, minimize


M = 1.0 / 8.0


def unit_from_angles(x: np.ndarray) -> np.ndarray:
    """Normalized qubit with its global phase fixed."""
    th, ph = x
    return np.array(
        [np.cos(th / 2.0), np.exp(1j * ph) * np.sin(th / 2.0)],
        dtype=complex,
    )


def vec(a: np.ndarray) -> np.ndarray:
    return a.reshape(-1, order="C")


def partial_transpose(a: np.ndarray) -> np.ndarray:
    return a.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def gram_value(g: np.ndarray, u: np.ndarray, v: np.ndarray) -> float:
    z = vec(np.outer(u, np.conjugate(v)))
    return float(np.real(np.vdot(z, g @ z)))


def diag_ratio(args: np.ndarray, g: np.ndarray, t: np.ndarray) -> float:
    x = unit_from_angles(args)
    num = abs(np.vdot(x, t @ x)) ** 2
    return float(num / gram_value(g, x, x))


def product_ratio(args: np.ndarray, g: np.ndarray, t: np.ndarray) -> float:
    u = unit_from_angles(args[:2])
    v = unit_from_angles(args[2:])
    num = abs(np.vdot(v, t @ u)) ** 2
    return float(num / gram_value(g, u, v))


def random_unit(rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(size=2) + 1j * rng.normal(size=2)
    return x / np.linalg.norm(x)


def random_model(rng: np.random.Generator, terms: int = 8) -> tuple[np.ndarray, np.ndarray]:
    k = M * np.eye(4, dtype=complex)
    for _ in range(terms):
        x, y = random_unit(rng), random_unit(rng)
        p = np.kron(x, y)
        k += rng.exponential() * np.outer(p, np.conjugate(p))
    g = partial_transpose(k)
    # Random Hermitian cross functional.
    r = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    t = (r + r.conj().T) / 2.0
    return g, t


def maximize(
    fun,
    bounds: list[tuple[float, float]],
    args: tuple[np.ndarray, np.ndarray],
    rng: np.random.Generator,
) -> tuple[float, np.ndarray]:
    # A cheap random multistart followed by local refinement is much faster
    # than a full global solve and is enough to locate formal obstructions.
    pts = np.column_stack(
        [
            rng.uniform(lo, hi, size=4000)
            for lo, hi in bounds
        ]
    )
    vals = np.array([fun(p, *args) for p in pts])
    best = int(np.argmax(vals))
    out = minimize(
        lambda z: -fun(z, *args),
        pts[best],
        method="Nelder-Mead",
        options={"maxiter": 3000, "xatol": 1e-12, "fatol": 1e-12},
    )
    return -float(out.fun), out.x


def main() -> None:
    rng = np.random.default_rng(20260729)
    b2 = [(0.0, np.pi), (-np.pi, np.pi)]
    b4 = b2 + b2
    best = (1.0, None)
    for it in range(200):
        g, t = random_model(rng)
        rd, xd = maximize(diag_ratio, b2, (g, t), rng)
        rp, xp = maximize(product_ratio, b4, (g, t), rng)
        quotient = rp / rd
        if quotient > best[0]:
            best = (quotient, (g, t, rd, rp, xd, xp))
            print(f"{it=:03d} product/diagonal={quotient:.12f}")
        if quotient > 1.0001:
            np.savez(
                "discovery/intersection_ppt_floor_obstruction.npz",
                g=g,
                t=t,
                rd=rd,
                rp=rp,
                xd=xd,
                xp=xp,
            )
            break
    else:
        print("no formal obstruction found", best[0])


if __name__ == "__main__":
    main()
