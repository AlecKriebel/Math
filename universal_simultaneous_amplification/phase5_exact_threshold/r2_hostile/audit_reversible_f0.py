#!/usr/bin/env python3
"""Bounded exact hostile search for the true reversible r=2 sign F0.

For an undirected weighted graph let ``m=n*rho_dB(G,2)`` and let ``m_K`` be
the corresponding complete dual mean.  The true collision target is

    F0 = 1/m - 1/m_K >= 0.

This script evaluates F0 itself—not the stronger two-step promotion margin—
on a fixed seeded corpus of complete, sparse, nearly disconnected,
core--periphery and multiple-hub rational graphs of orders five through
seven.  Every solve and sign is exact over QQ.  Passing is finite evidence.
"""

from __future__ import annotations

from itertools import combinations
from random import Random

from exact_fixation import Q, as_float, baseline, connected, fixation


SCALES = (1, 2, 10, 1000, 10**6, 10**12)


def empty(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def set_edge(weights, u, v, value):
    weights[u][v] = weights[v][u] = Q(value)


def random_complete(n: int, rng: Random):
    weights = empty(n)
    for u, v in combinations(range(n), 2):
        set_edge(weights, u, v, rng.choice(SCALES))
    return weights


def random_sparse(n: int, rng: Random):
    weights = empty(n)
    order = list(range(n))
    rng.shuffle(order)
    # A random spanning tree guarantees connectivity.  The remaining edges
    # include independent weak/strong choices and exact zeros.
    for position in range(1, n):
        parent = rng.randrange(position)
        set_edge(weights, order[position], order[parent], rng.choice(SCALES))
    for u, v in combinations(range(n), 2):
        if not weights[u][v] and rng.random() < rng.uniform(0.08, 0.55):
            set_edge(weights, u, v, rng.choice(SCALES))
    assert connected(weights)
    return weights


def random_core_periphery(n: int, rng: Random):
    weights = empty(n)
    core = rng.randint(2, n - 2)
    core_scale = rng.choice(SCALES)
    portal_scale = rng.choice(SCALES)
    completion_scale = rng.choice((0, 0, 1, 10, 1000))
    for u, v in combinations(range(core), 2):
        set_edge(weights, u, v, core_scale)
    for vertex in range(core, n):
        hub = rng.randrange(core)
        set_edge(weights, hub, vertex, portal_scale * rng.choice((1, 2, 10)))
        if completion_scale:
            for u in range(core):
                if not weights[u][vertex]:
                    set_edge(weights, u, vertex, completion_scale)
    for u, v in combinations(range(core, n), 2):
        if rng.random() < 0.35:
            set_edge(weights, u, v, rng.choice(SCALES))
    assert connected(weights)
    return weights


def corpus(n: int, count: int, seed: int):
    rng = Random(seed)
    builders = (random_complete, random_sparse, random_core_periphery)
    for index in range(count):
        builder = builders[index % len(builders)]
        yield builder.__name__, index, builder(n, rng)


def f0(weights, db=None):
    n = len(weights)
    if db is None:
        db = fixation(weights, "dB")
    complete_mean = n * baseline(n, "dB")
    return 1 / (n * db) - 1 / complete_mean


def main() -> None:
    counts = {5: 1200, 6: 800, 7: 300}
    tested = 0
    violations = []
    smallest = None
    for n, count in counts.items():
        local_smallest = None
        for label, index, weights in corpus(n, count, 26080811 + 1009 * n):
            db = fixation(weights, "dB")
            margin = f0(weights, db)
            ratio = db / baseline(n, "dB")
            record = (margin, ratio, n, label, index, weights)
            if local_smallest is None or margin < local_smallest[0]:
                local_smallest = record
            if smallest is None or margin < smallest[0]:
                smallest = record
            if margin < 0:
                violations.append(record)
            tested += 1
        assert local_smallest is not None
        print(
            f"n={n}: {count} exact reversible rational graphs; "
            f"min F0={local_smallest[0]} (~{as_float(local_smallest[0]):.17g}); "
            f"max dB ratio~{as_float(local_smallest[1]):.17g}",
            flush=True,
        )

    assert smallest is not None
    margin, ratio, n, label, index, weights = smallest
    print(f"EXACT REVERSIBLE F0 CORPUS: {tested} graphs")
    print(f"true F0 violations={len(violations)}")
    print(
        "smallest F0:", f"n={n}", label, index, margin,
        f"(~{as_float(margin):.17g}); dB ratio={ratio} (~{as_float(ratio):.17g})",
    )
    print("weights=", [[str(value) for value in row] for row in weights])
    if violations:
        raise AssertionError("exact reversible F0 counterexample found")
    print("PASS: no F0<0 witness in the bounded exact reversible corpus")
    print("Finite evidence only; the universal r=2 inequality remains OPEN.")


if __name__ == "__main__":
    main()
