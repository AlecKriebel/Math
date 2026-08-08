#!/usr/bin/env python3
"""Exact hostile screen of independently weighted trees at small orders.

For each nonisomorphic unweighted tree, the first listed edge is normalized
to one and every other edge ranges independently over five rational scales
from 10^-6 to 10^6.  Thus the corpus includes paths, stars, double stars and
irregular multiple-hub trees with nearly disconnected cuts.  It is finite
evidence only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product

import networkx as nx

from audit_structured_grid import integrated_two_step
from exact_fixation import Q, as_float, baseline, fixation


ALPHABET = (
    Fraction(1, 10**6),
    Fraction(1, 100),
    Fraction(1),
    Fraction(100),
    Fraction(10**6),
)


def weight_matrix(n, edges, values):
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for (u, v), value in zip(edges, values):
        value = Q(value.numerator, value.denominator)
        weights[u][v] = weights[v][u] = value
    return weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    if not 3 <= args.max_n <= 7:
        raise ValueError("max-n must lie in [3,7]")

    total = 0
    db_violations = 0
    simultaneous = 0
    promotion_violations = 0
    best_db = None
    best_sim = None
    best_promotion = None

    for n in range(3, args.max_n + 1):
        local = 0
        trees = list(nx.generators.nonisomorphic_trees(n))
        for tree_index, tree in enumerate(trees):
            edges = tuple(sorted(tuple(sorted(edge)) for edge in tree.edges()))
            for tail in product(ALPHABET, repeat=len(edges) - 1):
                values = (Fraction(1),) + tail
                weights = weight_matrix(n, edges, values)
                db = fixation(weights, "dB")
                bd = fixation(weights, "Bd")
                db_ratio = db / baseline(n, "dB")
                bd_ratio = bd / baseline(n, "Bd")
                minimum = min(db_ratio, bd_ratio)
                promotion = 1 / (n * db) - integrated_two_step(weights)
                record = (db_ratio, bd_ratio, promotion, n, tree_index, edges, values)
                db_violations += db_ratio > 1
                simultaneous += db_ratio > 1 and bd_ratio > 1
                promotion_violations += promotion < 0
                if best_db is None or db_ratio > best_db[0]:
                    best_db = record
                sim_record = (minimum,) + record
                if best_sim is None or minimum > best_sim[0]:
                    best_sim = sim_record
                promotion_record = (promotion,) + record
                if best_promotion is None or promotion < best_promotion[0]:
                    best_promotion = promotion_record
                local += 1
        total += local
        print(
            f"n={n}: {len(trees)} nonisomorphic trees, {local} exact weightings PASS",
            flush=True,
        )

    assert best_db is not None and best_sim is not None and best_promotion is not None
    print(f"EXACT WEIGHTED-TREE CORPUS: {total} graphs")
    print(
        f"dB violations={db_violations}; simultaneous violations={simultaneous}; "
        f"promotion violations={promotion_violations}"
    )
    db_ratio, bd_ratio, promotion, n, tree_index, edges, values = best_db
    print(
        "best dB:", f"n={n}", f"tree={tree_index}", f"edges={edges}",
        f"weights={tuple(map(str, values))}",
        f"dB={db_ratio} (~{as_float(db_ratio):.17g})",
        f"Bd~{as_float(bd_ratio):.17g}",
        f"promotion~{as_float(promotion):.17g}",
    )
    minimum, db_ratio, bd_ratio, promotion, n, tree_index, edges, values = best_sim
    print(
        "best M:", f"n={n}", f"tree={tree_index}", f"edges={edges}",
        f"weights={tuple(map(str, values))}",
        f"M={minimum} (~{as_float(minimum):.17g})",
        f"dB~{as_float(db_ratio):.17g}", f"Bd~{as_float(bd_ratio):.17g}",
    )
    promotion, db_ratio, bd_ratio, _, n, tree_index, edges, values = best_promotion
    print(
        "smallest promotion:", f"n={n}", f"tree={tree_index}",
        f"edges={edges}", f"weights={tuple(map(str, values))}",
        f"margin={promotion} (~{as_float(promotion):.17g})",
        f"dB~{as_float(db_ratio):.17g}",
    )
    if db_violations or simultaneous or promotion_violations:
        raise AssertionError("exact tree-corpus violation found")
    print("PASS: no exact dB, simultaneous, or promotion violation on weighted trees")
    print("This is finite evidence only; the universal r=2 sign remains open.")


if __name__ == "__main__":
    main()
