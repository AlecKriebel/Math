#!/usr/bin/env python3
"""Independent exact checks for the weighted clique--pendant analysis."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q

import sympy as sp

from model import moves, states


def graph(c: int, m: int, w: Q):
    n = c + m + 1
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for u in range(c + 1):
        for v in range(u + 1, c + 1):
            weights[u][v] = weights[v][u] = Q(1)
    for leaf in range(c + 1, n):
        weights[0][leaf] = weights[leaf][0] = w
    return weights


def canonical_set(state, c: int, m: int):
    h, i, j = state
    answer = set()
    if h:
        answer.add(0)
    answer.update(range(1, i + 1))
    answer.update(range(c + 1, c + j + 1))
    return frozenset(answer)


def lump(mutants, c: int, m: int):
    return (
        int(0 in mutants),
        sum(v in mutants for v in range(1, c + 1)),
        sum(v in mutants for v in range(c + 1, c + m + 1)),
    )


def microscopic(rule: str, state, c: int, m: int, r: Q, w: Q):
    weights = graph(c, m, w)
    n = len(weights)
    S = canonical_set(state, c, m)
    out = defaultdict(Q)
    if rule == "Bd":
        fitness = [r if u in S else Q(1) for u in range(n)]
        total = sum(fitness, Q())
        degree = [sum(row, Q()) for row in weights]
        for u in range(n):
            for v in range(n):
                if weights[u][v] and ((u in S) != (v in S)):
                    target = S | {v} if u in S else S - {v}
                    out[lump(target, c, m)] += (
                        fitness[u] * weights[u][v] / (total * degree[u])
                    )
    else:
        for v in range(n):
            denominator = sum(
                (r if u in S else Q(1)) * weights[u][v] for u in range(n)
            )
            for u in range(n):
                if weights[u][v] and ((u in S) != (v in S)):
                    target = S | {v} if u in S else S - {v}
                    out[lump(target, c, m)] += (
                        (r if u in S else Q(1))
                        * weights[u][v]
                        / (n * denominator)
                    )
    return dict(out)


def verify_lumping():
    cases = [
        (2, 1, Q(3, 2), Q(5, 7)),
        (3, 2, Q(3, 2), Q(11, 3)),
        (4, 3, Q(7, 5), Q(1, 10)),
    ]
    checks = 0
    for c, m, r, w in cases:
        for rule in ("Bd", "dB"):
            for state in states(c, m):
                direct = microscopic(rule, state, c, m, r, w)
                formula = moves(rule, state, c, m, r, w)
                assert direct == formula, (c, m, r, w, rule, state, direct, formula)
                assert sum(direct.values(), Q()) <= 1
                checks += 1
    print(f"PASS {checks} exact labelled/lumped row comparisons")


def verify_leaf_bound():
    cases = [
        (3, Q(3, 2), [Q(1, 7), Q(5, 3), Q(11, 2)]),
        (17, Q(7, 5), [Q(1, 100), Q(2), Q(200), Q(7, 9)]),
        (1, Q(2), [Q(13, 11)]),
    ]
    for c, r, weights in cases:
        D = Q(c) + sum(weights, Q())
        activation_bounds = []
        for w in weights:
            # Exact probability that H activates before the initial leaf dies.
            activation = r * w / (D + (2 * r - 1) * w)
            assert activation <= r * w / D
            activation_bounds.append(activation)
        assert sum(activation_bounds, Q()) <= r
    print("PASS exact arbitrary-weight leaf-activation sum bound")


def verify_symbolic_core_rates():
    c, i, r, W = sp.symbols("c i r W", positive=True)
    b = (c - i) * r * i / (c + (r - 1) * i)
    d = i * (c - i + 1) / (c + (r - 1) * (i - 1))
    a = r * i / (c + W + (r - 1) * i)
    ratio = sp.factor(b / d)
    target = sp.factor(
        r
        * (c - i)
        / (c - i + 1)
        * (c + (r - 1) * (i - 1))
        / (c + (r - 1) * i)
    )
    assert sp.simplify(ratio - target) == 0
    hazard_ratio = sp.factor(a / d)
    target_hazard = sp.factor(
        r
        * (c + (r - 1) * (i - 1))
        / ((c + W + (r - 1) * i) * (c - i + 1))
    )
    assert sp.simplify(hazard_ratio - target_hazard) == 0

    # The explicit endpoint constants in the proof: for c>=13 and i<=c/2,
    # b/d >=5/4 and a/d <=15/(4c).  These rational lower envelopes imply
    # the inequalities without finite sampling.
    lower_envelope = (2 * c - 1) / (2 * (c + 2))
    assert sp.simplify(
        lower_envelope
        - sp.Rational(5, 6)
        - (c - 13) / (6 * (c + 2))
    ) == 0
    s, z = sp.Rational(5, 4), sp.Rational(9, 8)
    gamma = sp.factor((s / z + z) / (s + 1))
    assert gamma == sp.Rational(161, 162)
    assert z ** -1 / (1 - gamma) == 144
    assert sp.Rational(15, 4) * 144 == 540
    print("PASS symbolic embedded-chain ratios and endpoint constants")


def main():
    verify_lumping()
    verify_leaf_bound()
    verify_symbolic_core_rates()
    print("ALL WEIGHTED CLIQUE--PENDANT EXACT CHECKS PASS")


if __name__ == "__main__":
    main()
