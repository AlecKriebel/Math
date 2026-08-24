#!/usr/bin/env python3
"""Independent finite separated-trace calculation for Paper II.

This uses only the transition-rate tables printed in the manuscript.  The
isolated center committor is solved as a block-tridiagonal linear system in the
ordinary-clique count i.  It is intentionally independent of delivered
certificate code, which does not compute the large finite center chains.
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np


R_HYB = 1.5028569127905696
SIGMA = 0.130677282287048377
LAMBDA = 0.750806483031880492


def rates(C: int, m: int, r: float, rule: str, h: int, i: int, ell: int):
    """Return (i_up, i_down, hub_flip, ell_up, ell_down)."""
    c = C - 1
    d = c + m
    if rule == "Bd":
        i_up = r * (c - i) * (h / d + i / c)
        i_down = i * ((1 - h) / d + (c - i) / c)
        if h == 0:
            hub = r * (i / c + ell)
        else:
            hub = (c - i) / c + m - ell
        ell_up = r * h * (m - ell) / d
        ell_down = (1 - h) * ell / d
    elif rule == "dB":
        i_up = (c - i) * r * (h + i) / (c + (r - 1) * (h + i))
        if i:
            i_down = i * (c - i + 1 - h) / (
                c + (r - 1) * (i - 1 + h)
            )
        else:
            i_down = 0.0
        if h == 0:
            hub = r * (i + ell) / (d + (r - 1) * (i + ell))
        else:
            hub = (d - i - ell) / (d + (r - 1) * (i + ell))
        ell_up = h * (m - ell)
        ell_down = (1 - h) * ell
    else:
        raise ValueError(rule)
    return i_up, i_down, hub, ell_up, ell_down


def center_block(C: int, m: int, r: float, rule: str, i: int):
    """Positive harmonic-system blocks A_i, B_i, C_i, d_i."""
    c = C - 1
    b = 2 * (m + 1)
    a_diag = np.zeros(b)
    c_diag = np.zeros(b)
    B = np.zeros((b, b))
    rhs = np.zeros(b)

    def idx(h: int, ell: int) -> int:
        return h * (m + 1) + ell

    for h in (0, 1):
        for ell in range(m + 1):
            j = idx(h, ell)
            if i == 0 and h == 0 and ell == 0:
                B[j, j] = 1.0
                continue
            if i == c and h == 1 and ell == m:
                B[j, j] = 1.0
                rhs[j] = 1.0
                continue
            i_up, i_down, hub, ell_up, ell_down = rates(
                C, m, r, rule, h, i, ell
            )
            total = i_up + i_down + hub + ell_up + ell_down
            B[j, j] = total
            a_diag[j] = -i_down
            c_diag[j] = -i_up
            if hub:
                B[j, idx(1 - h, ell)] -= hub
            if ell_up:
                B[j, idx(h, ell + 1)] -= ell_up
            if ell_down:
                B[j, idx(h, ell - 1)] -= ell_down
    return a_diag, B, c_diag, rhs


def solve_center(C: int, m: int, r: float, rule: str):
    """Return ordinary, hub, leaf starts and the two center averages."""
    c = C - 1
    b = 2 * (m + 1)
    transformed_C: list[np.ndarray] = []
    transformed_d: list[np.ndarray] = []
    previous_C = None
    previous_d = None

    for i in range(c + 1):
        a_diag, B, c_diag, rhs = center_block(C, m, r, rule, i)
        if i:
            B -= a_diag[:, None] * previous_C
            rhs -= a_diag * previous_d
        Cmat = np.zeros((b, b))
        np.fill_diagonal(Cmat, c_diag)
        joined = np.column_stack((Cmat, rhs))
        solved = np.linalg.solve(B, joined)
        current_C = solved[:, :b]
        current_d = solved[:, b]
        transformed_C.append(current_C)
        transformed_d.append(current_d)
        previous_C = current_C
        previous_d = current_d

    x_next = transformed_d[c]
    wanted = {}
    if c in (0, 1):
        wanted[c] = x_next.copy()
    for i in range(c - 1, -1, -1):
        x = transformed_d[i] - transformed_C[i] @ x_next
        if i in (0, 1):
            wanted[i] = x.copy()
        x_next = x

    def idx(h: int, ell: int) -> int:
        return h * (m + 1) + ell

    ordinary = float(wanted[1][idx(0, 0)])
    hub = float(wanted[0][idx(1, 0)])
    leaf = float(wanted[0][idx(0, 1)]) if m else float("nan")
    u_core = (c * ordinary + hub) / C
    a_center = (c * ordinary + hub + m * leaf) / (C + m)
    J = ordinary + hub / (c + m)
    extrema = (min(map(float, x_next)), max(map(float, x_next)))
    return {
        "ordinary": ordinary,
        "hub": hub,
        "leaf": leaf,
        "u_core": u_core,
        "a_center": a_center,
        "J": J,
        "last_block_extrema": extrema,
    }


def macro_probabilities(q: int, A: float, D: float, B: float, Cp: float):
    """Exact finite macro-chain committors from a center and one pair."""
    size = 2 * (q + 1)
    M = np.zeros((size, size))
    d = np.zeros(size)

    def ix(h: int, k: int) -> int:
        return h * (q + 1) + k

    # x_0 = 0 and y_q = 1.
    M[ix(0, 0), ix(0, 0)] = 1.0
    M[ix(1, q), ix(1, q)] = 1.0
    d[ix(1, q)] = 1.0
    a = A / (A + D)
    dd = D / (A + D)
    bb = B / (B + Cp)
    cc = Cp / (B + Cp)
    for k in range(1, q + 1):
        row = ix(0, k)
        M[row, row] = 1.0
        M[row, ix(1, k)] = -a
        M[row, ix(0, k - 1)] = -dd
    for k in range(q):
        row = ix(1, k)
        M[row, row] = 1.0
        M[row, ix(1, k + 1)] = -bb
        M[row, ix(0, k)] = -cc
    sol = np.linalg.solve(M, d)
    return float(sol[ix(1, 0)]), float(sol[ix(0, 1)])


def complete_baseline(N: int, r: float, rule: str) -> float:
    p = 1.0 - 1.0 / r
    if rule == "Bd":
        return p / (1.0 - r ** (-N))
    return ((N - 1.0) / N) * p / (1.0 - r ** (-(N - 1)))


def finite_trace(t: int, r: float, rule: str):
    C = t**4
    q = t
    m = math.floor(LAMBDA * t)
    N = C + m + 2 * q
    center_r = solve_center(C, m, r, rule)
    center_s = solve_center(C, m, 1.0 / r, rule)
    c = C - 1
    I_H = 1.0 + 1.0 / (c + m)
    I_P = 2.0 * SIGMA / C
    J_P = SIGMA / C
    if rule == "Bd":
        a_pair = r / (r + 1.0)
        A = C * r * I_P * center_r["u_core"]
        D = 2.0 * I_H / (r + 1.0)
        B = 2.0 * r * I_H * a_pair
        Cp = C * I_P * center_s["u_core"]
    else:
        a_pair = 0.5
        A = 2.0 * r * center_r["J"]
        D = (C / r) * J_P
        B = C * r * J_P
        Cp = (2.0 / r) * center_s["J"]
    P_H, P_P = macro_probabilities(q, A, D, B, Cp)
    rho0 = ((C + m) / N) * center_r["a_center"] * P_H
    rho0 += (2.0 * q / N) * a_pair * P_P
    baseline = complete_baseline(N, r, rule)
    scaled = (N / q) * (rho0 / baseline - 1.0)
    if rule == "Bd":
        response = 2.0 * (SIGMA - 1.0) / (1 + SIGMA * (r * r - 1))
        response += LAMBDA / (r - 1.0)
    else:
        response = 2.0 * (r * (2 - r) - SIGMA) / (
            SIGMA + 2 * r * (r - 1)
        ) - LAMBDA
    return {
        "t": t,
        "C": C,
        "m": m,
        "q": q,
        "N": N,
        "r": r,
        "rule": rule,
        "rho0": rho0,
        "baseline": baseline,
        "scaled_gain": scaled,
        "response": response,
        "deficit": scaled - response,
        "P_H": P_H,
        "P_P": P_P,
        "center_r": center_r,
        "center_reciprocal": center_s,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", type=int, nargs="+", required=True)
    parser.add_argument("--r", type=float, default=1.4)
    parser.add_argument("--rule", choices=("Bd", "dB"), default="Bd")
    args = parser.parse_args()
    for t in args.t:
        started = time.time()
        result = finite_trace(t, args.r, args.rule)
        print(result)
        print(f"elapsed_seconds={time.time() - started:.3f}", flush=True)


if __name__ == "__main__":
    main()
