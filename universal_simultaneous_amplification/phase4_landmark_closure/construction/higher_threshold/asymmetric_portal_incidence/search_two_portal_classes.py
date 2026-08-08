#!/usr/bin/env python3
"""Numerical search of a two-portal-class, two-blade-type trace.

The labelled portal-subset episode lumps exactly to counts ``(k0,k1)``
because weights and incidences are constant inside each portal class.  This
script is for discovery only; all displayed rates are direct aggregates of
the atomic labelled rates in ``GENERAL_TRACE_AND_RANK_ONE_NO_GO.md``.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
from scipy.linalg import solve
from scipy.optimize import differential_evolution


HERE = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fast = load_module("fast_no_portal", HERE / "search_higher_rank_no_portal.py")


def states(q):
    return [(i, j) for i in range(q + 1) for j in range(q + 1) if i + j]


def episode_transform(rule, r, q, loads, frac, portal_weights, z):
    """Transforms from a singleton in either portal class."""
    # Equal portal-class sizes make a common cross-edge weight symmetric.
    w00, w11, w01 = portal_weights
    edge = np.array([[w00, w01], [w01, w11]])
    degree = np.array([
        loads[0] + (q - 1) * w00 + q * w01,
        loads[1] + (q - 1) * w11 + q * w01,
    ])
    pi0 = np.ones(frac.shape[1]) / frac.shape[1]
    lam = loads[:, None] * frac / (2.0 * pi0[None, :])
    ss = states(q); row = {state: i for i, state in enumerate(ss)}
    mat = np.zeros((len(ss), len(ss))); rhs = np.zeros(len(ss))

    for state in ss:
        idx = row[state]
        k = np.asarray(state, dtype=int)
        transitions = []
        for g in range(2):
            h = 1 - g
            if k[g]:
                if rule == "Bd":
                    per = (
                        loads[g]
                        + (q - k[g]) * edge[g, g] / degree[g]
                        + (q - k[h]) * edge[g, h] / degree[h]
                    )
                else:
                    resident = (
                        loads[g]
                        + (q - k[g]) * edge[g, g]
                        + (q - k[h]) * edge[g, h]
                    )
                    mutant = (k[g] - 1) * edge[g, g] + k[h] * edge[g, h]
                    per = resident / (resident + r * mutant)
                nxt = list(state); nxt[g] -= 1
                transitions.append((tuple(nxt), k[g] * per))
            if k[g] < q:
                if rule == "Bd":
                    per = r * (
                        k[g] * edge[g, g] / degree[g]
                        + k[h] * edge[g, h] / degree[h]
                    )
                else:
                    mutant = k[g] * edge[g, g] + k[h] * edge[g, h]
                    resident = (
                        loads[g]
                        + (q - k[g] - 1) * edge[g, g]
                        + (q - k[h]) * edge[g, h]
                    )
                    per = r * mutant / (resident + r * mutant)
                nxt = list(state); nxt[g] += 1
                transitions.append((tuple(nxt), (q - k[g]) * per))

        if rule == "Bd":
            child = (
                2.0 * pi0 * r**2 / (r + 1.0)
                * sum((k[g] * lam[g] / degree[g] for g in range(2)), start=np.zeros(frac.shape[1]))
            )
        else:
            child = pi0 * r * sum((k[g] * lam[g] for g in range(2)), start=np.zeros(frac.shape[1]))
        killing = float(child @ (1.0 - z))
        mat[idx, idx] = sum(rate for _, rate in transitions) + killing
        for nxt, rate in transitions:
            if nxt == (0, 0):
                rhs[idx] += rate
            else:
                mat[idx, row[nxt]] -= rate
    value = solve(mat, rhs, assume_a="gen")
    return np.array([value[row[(1, 0)]], value[row[(0, 1)]]])


def extinction(rule, r, q, loads, frac, portal_weights):
    t = frac.shape[1]
    pi0 = np.ones(t) / t
    lam = loads[:, None] * frac / (2.0 * pi0[None, :])
    w00, w11, w01 = portal_weights
    degree = np.array([
        loads[0] + (q - 1) * w00 + q * w01,
        loads[1] + (q - 1) * w11 + q * w01,
    ])
    if rule == "Bd":
        death = 2.0 * q / (r + 1.0) * (lam / degree[:, None]).sum(axis=0)
        seed = 2.0 * q * r * lam
    else:
        death = q * lam.sum(axis=0) / r
        seed = 2.0 * q * r * lam / degree[:, None]
    z = np.zeros(t)
    for _ in range(100000):
        f = episode_transform(rule, r, q, loads, frac, portal_weights, z)
        killed = (seed * (1.0 - f[:, None])).sum(axis=0)
        new = death / (death + killed)
        if np.max(np.abs(new - z)) < 2e-12:
            return new
        z = new
    raise RuntimeError("fixed point did not converge")


def decode(v):
    loads = np.exp(np.asarray(v[:2]))
    # One logit per row for two blade types.
    p = 1.0 / (1.0 + np.exp(-np.asarray(v[2:4])))
    frac = np.c_[p, 1.0 - p]
    portal_weights = np.exp(np.asarray(v[4:7]))
    return loads, frac, portal_weights


def objective(v, q, r):
    try:
        loads, frac, pw = decode(v)
        qb = extinction("Bd", r, q, loads, frac, pw)
        qd = extinction("dB", r, q, loads, frac, pw)
        return -fast.best_type_mixture(r, qb, qd)[0]
    except (FloatingPointError, RuntimeError, np.linalg.LinAlgError, ValueError):
        return 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-size", type=int, default=3)
    ap.add_argument("--fitness", type=float, default=1.6)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=200)
    ap.add_argument("--popsize", type=int, default=12)
    args = ap.parse_args()
    result = differential_evolution(
        objective,
        [(-9.0, 9.0)] * 7,
        args=(args.class_size, args.fitness),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        polish=True,
        tol=1e-9,
        workers=1,
        updating="immediate",
    )
    loads, frac, pw = decode(result.x)
    qb = extinction("Bd", args.fitness, args.class_size, loads, frac, pw)
    qd = extinction("dB", args.fitness, args.class_size, loads, frac, pw)
    score, pi, gaps = fast.best_type_mixture(args.fitness, qb, qd)
    print("objective min gap", -result.fun)
    print("loads", loads)
    print("fractions\n", frac)
    print("within0, within1, cross", pw)
    print("optimal type mixture", pi, "gaps", gaps, "score", score)
    print("q_B", qb, "q_D", qd)


if __name__ == "__main__":
    main()
