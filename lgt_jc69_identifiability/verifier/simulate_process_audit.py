#!/usr/bin/env python3
"""Monte Carlo audit of the stated species-lineage Poisson process.

This is not part of the proof.  It simulates all transfers, including events
that hit an empty recipient branch and events that move a sampled ancestral
lineage into the currently ancestrally unoccupied branch.  The output converges to the
CTMC-corrected map in the manuscript and not to the auxiliary fourteen-history map.
"""
from __future__ import annotations

import argparse
import math
import random
from statistics import fmean

MU = 4.0 / 3.0


def corrected_map(q: float, x: float, y: float):
    r = q + (1.0 - q) * y * y
    X = x ** (2.0 - q)
    Z = x ** 3
    D = (1.0 - r) * x ** (2.0 + q / 2.0)
    M = q * (1.0 - X) / (2.0 - q) + (1.0 + 2.0 * r) * X / 3.0
    C = (
        q * q * ((q - 2.0) * Z + 3.0 * X - (q + 1.0)) / ((q - 2.0) * (q + 1.0))
        + r * Z
        + q * (1.0 + 2.0 * r) * (X - Z) / (1.0 + q)
    )
    return M + 2.0 * D / 3.0, M - D / 3.0, C


def table_map(q: float, x: float, y: float):
    K = q * (2.0 * q + 1.0) / (q + 2.0)
    xq = x ** q
    A = K + (1.0 - q) * x * x * (1.0 + (1.0 - xq) * y * y) + q * (1.0 - q) * x ** (q + 2.0) / (q + 2.0)
    B = K + (1.0 - q) * x * x * (1.0 + (3.0 - xq) * y * y) / 2.0 - (1.0 - q) * (2.0 - q) * x ** (q + 2.0) / (2.0 * (q + 2.0))
    C = q * q + q * (1.0 - q) * x * x + 2.0 * q * (1.0 - q) * x * x * y * y + (1.0 - q) * (1.0 - 2.0 * q) * x ** 3 * y * y
    return A, B, C


def merge(branches, donor, recipient, time, events):
    """Backward response to donor->recipient transfer."""
    rec = branches[recipient]
    if rec is None:
        return
    don = branches[donor]
    if don is None:
        branches[donor] = rec
        branches[recipient] = None
        return
    events.append((time, frozenset(don), frozenset(rec)))
    branches[donor] = frozenset(don | rec)
    branches[recipient] = None


def species_merge(branches, a, b, out, time, events):
    A, B = branches[a], branches[b]
    if A is not None and B is not None:
        events.append((time, frozenset(A), frozenset(B)))
        branches[out] = frozenset(A | B)
    else:
        branches[out] = A if A is not None else B


def one_history(t1: float, t2: float, lam: float, rng: random.Random):
    branches = {1: frozenset({1}), 2: frozenset({2}), 3: frozenset({3})}
    events = []

    # Three species lineages, total event rate 3 lambda.
    t = 0.0
    ordered3 = [(d, r) for d in (1, 2, 3) for r in (1, 2, 3) if d != r]
    while True:
        t += rng.expovariate(3.0 * lam)
        if t >= t1:
            break
        donor, recipient = ordered3[rng.randrange(6)]
        merge(branches, donor, recipient, t, events)
        if len(events) >= 2:
            break

    # Species lineages 1 and 2 merge at t1.
    species_merge(branches, 1, 2, 12, t1, events)
    b2 = {12: branches[12], 3: branches[3]}

    # Two species lineages, total event rate 2 lambda.
    if len(events) < 2:
        t = t1
        ordered2 = [(12, 3), (3, 12)]
        while True:
            t += rng.expovariate(2.0 * lam)
            if t >= t2:
                break
            donor, recipient = ordered2[rng.randrange(2)]
            merge(b2, donor, recipient, t, events)
            if len(events) >= 2:
                break

    if len(events) < 2:
        species_merge(b2, 12, 3, 123, t2, events)

    events.sort(key=lambda z: z[0])
    if len(events) != 2:
        raise RuntimeError(f"expected two coalescences, got {events!r}")
    g1, left, right = events[0]
    g2 = events[1][0]
    cherry = frozenset(left | right)
    if len(cherry) != 2:
        raise RuntimeError("first coalescence was not a cherry")

    e1 = math.exp(-2.0 * MU * g1)
    e2 = math.exp(-2.0 * MU * g2)
    A = e1 if cherry == frozenset({1, 2}) else e2
    B = e1 if cherry == frozenset({1, 3}) else e2
    C = math.exp(-MU * (g1 + 2.0 * g2))
    return A, B, C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20260803)
    args = ap.parse_args()

    q, x, y = 0.5, 0.1, 0.6
    lam = MU * q / (1.0 - q)
    t1 = -(1.0 - q) * math.log(x) / MU
    t2 = t1 - (1.0 - q) * math.log(y) / MU
    rng = random.Random(args.seed)
    sums = [0.0, 0.0, 0.0]
    sums2 = [0.0, 0.0, 0.0]
    for _ in range(args.samples):
        row = one_history(t1, t2, lam, rng)
        for j, z in enumerate(row):
            sums[j] += z
            sums2[j] += z * z
    means = [z / args.samples for z in sums]
    ses = [math.sqrt(max(0.0, sums2[j] / args.samples - means[j] ** 2) / args.samples) for j in range(3)]
    corr = corrected_map(q, x, y)
    lit = table_map(q, x, y)

    print(f"samples={args.samples} seed={args.seed}")
    print("coordinate       Monte Carlo (SE)       corrected map       auxiliary table map")
    for name, m, se, c, l in zip(("A", "B", "C"), means, ses, corr, lit):
        print(f"{name:>3s}       {m:.9f} ({se:.2e})   {c:.9f}       {l:.9f}")
    ok = all(abs(means[j] - corr[j]) <= 6.0 * ses[j] + 2e-4 for j in range(3))
    far = all(abs(means[j] - lit[j]) >= 20.0 * ses[j] for j in range(3))
    print("PASS" if ok and far else "FAIL")
    if ok and far:
        print("SIMULATION AUDIT PASSED")
    return 0 if ok and far else 1


if __name__ == "__main__":
    raise SystemExit(main())
