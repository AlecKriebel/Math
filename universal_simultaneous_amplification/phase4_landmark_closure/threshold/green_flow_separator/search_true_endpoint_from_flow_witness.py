#!/usr/bin/env python3
"""Hostile true-chain endpoint search seeded by the flow-LP witness.

This is discovery code only.  Unlike the projected LP, every objective value
here is obtained by solving both full 126-state absorbing chains.  The modes
are the bare three-blade support, a common weak completion edge weight, and
all 21 complete-support weights independently.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
from scipy.optimize import differential_evolution, minimize


HERE = pathlib.Path(__file__).resolve().parent
ENDPOINT = HERE.parent / "endpoint_hostile_exact"
sys.path.insert(0, str(ENDPOINT))

from search_endpoint import score


N = 7
BLADE_EDGES = (
    (0, 1), (0, 2), (1, 2),
    (0, 3), (0, 4), (3, 4),
    (0, 5), (0, 6), (5, 6),
)
ALL_EDGES = tuple((i, j) for i in range(N) for j in range(i + 1, N))
MISSING_EDGES = tuple(edge for edge in ALL_EDGES if edge not in BLADE_EDGES)

# Exact-flow-relaxation witness and the best bare-support true-chain point
# found in the hostile cycle.
FLOW_SEED = (1, 100000, 20, 3000, 20, 1e-6, 50, 30, 1e-4)
BARE_TRUE_SEED = (
    0.3341945037023992,
    1.8285784590639669,
    12.011113617850214,
    0.02176671548635371,
    0.003505389857419266,
    14.105382524615576,
    4.0091894467758,
    4.00583525427861,
    7.882065960403788,
)


def parameter_edges(mode: str):
    if mode == "bare":
        return BLADE_EDGES
    if mode == "common-completion":
        return BLADE_EDGES + ((-1, -1),)
    if mode == "full-completion":
        return ALL_EDGES
    raise ValueError(mode)


def weights_from_logs(logs, mode: str):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(np.clip(logs, -40.0, 40.0))
    weights = np.zeros((N, N))
    if mode == "bare":
        for edge, value in zip(BLADE_EDGES, values):
            weights[edge] = weights[edge[::-1]] = value
    elif mode == "common-completion":
        for edge, value in zip(BLADE_EDGES, values[:9]):
            weights[edge] = weights[edge[::-1]] = value
        for edge in MISSING_EDGES:
            weights[edge] = weights[edge[::-1]] = values[9]
    elif mode == "full-completion":
        for edge, value in zip(ALL_EDGES, values):
            weights[edge] = weights[edge[::-1]] = value
    else:
        raise ValueError(mode)
    return weights


def seed_logs(mode: str):
    if mode == "bare":
        return np.log(BARE_TRUE_SEED)
    if mode == "common-completion":
        return np.r_[np.log(BARE_TRUE_SEED), -20.0]
    seed = {edge: value for edge, value in zip(BLADE_EDGES, BARE_TRUE_SEED)}
    return np.asarray([np.log(seed.get(edge, 1e-7)) for edge in ALL_EDGES])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("bare", "common-completion", "full-completion"),
        default="bare",
    )
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--popsize", type=int, default=6)
    parser.add_argument("--span", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=813)
    args = parser.parse_args()

    dimension = len(parameter_edges(args.mode))
    start = seed_logs(args.mode)
    if len(start) != dimension:
        raise AssertionError((len(start), dimension))
    # Complete support contains K_7.  Recording 1 as the incumbent makes any
    # printed improvement an apparent endpoint simultaneous amplifier.
    incumbent = [1.0 if args.mode != "bare" else -np.inf, None, None]

    def objective(logs):
        try:
            candidate_weights = weights_from_logs(logs, args.mode)
            candidate = score(candidate_weights)
            value = candidate.minimum
        except (FloatingPointError, np.linalg.LinAlgError, ValueError):
            return 1e4
        if value > incumbent[0] + 2e-9:
            incumbent[:] = [value, logs.copy(), candidate]
            print(
                json.dumps(
                    {
                        "M": value,
                        "x": candidate.x,
                        "y": candidate.y,
                        "span": float(np.ptp(logs)),
                        "weights": candidate_weights.tolist(),
                    }
                ),
                flush=True,
            )
        return -value

    result = differential_evolution(
        objective,
        [(-args.span, args.span)] * dimension,
        x0=np.clip(start, -args.span, args.span),
        seed=args.seed,
        popsize=args.popsize,
        maxiter=args.iterations,
        polish=False,
        updating="immediate",
        tol=1e-9,
    )
    starts = [start, result.x]
    if args.mode != "bare":
        starts.insert(0, np.zeros(dimension))
    for initial in starts:
        polished = minimize(
            objective,
            np.clip(initial, -args.span, args.span),
            method="Powell",
            bounds=[(-args.span - 4, args.span + 4)] * dimension,
            options={"maxiter": 3000, "xtol": 1e-9, "ftol": 1e-13},
        )
        candidate = score(weights_from_logs(polished.x, args.mode))
        print(
            "POLISH",
            json.dumps({"M": candidate.minimum, "x": candidate.x, "y": candidate.y}),
            flush=True,
        )
    print(
        "BEST",
        json.dumps(
            {
                "M": incumbent[0],
                "x": None if incumbent[2] is None else incumbent[2].x,
                "y": None if incumbent[2] is None else incumbent[2].y,
            }
        ),
    )


if __name__ == "__main__":
    main()
