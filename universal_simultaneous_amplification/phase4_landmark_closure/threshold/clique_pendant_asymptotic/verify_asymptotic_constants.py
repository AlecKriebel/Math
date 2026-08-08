#!/usr/bin/env python3
"""Independent exact verifier for the growing clique--pendant calculation."""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations

import sympy as sp


def add(row, target, value):
    if value:
        row[target] = row.get(target, Q(0)) + value


def quotient_changes(c, m, r, rule, state):
    h, i, j = state
    n, d = c + m + 1, c + m
    row = {}
    if rule == "Bd":
        F = Q(n) + (r - 1) * (h + i + j)
        if i < c:
            add(row, (h, i + 1, j), r * (c - i) * (Q(h, d) + Q(i, c)) / F)
        if i:
            add(row, (h, i - 1, j), i * (Q(1 - h, d) + Q(c - i, c)) / F)
        if h == 0:
            add(row, (1, i, j), r * (Q(i, c) + j) / F)
        else:
            add(row, (0, i, j), (Q(c - i, c) + m - j) / F)
        if h and j < m:
            add(row, (h, i, j + 1), r * Q(m - j, d) / F)
        if not h and j:
            add(row, (h, i, j - 1), Q(j, d) / F)
    elif rule == "dB":
        if i < c:
            add(row, (h, i + 1, j), Q(c - i, n) * r * (h + i) /
                (c + (r - 1) * (h + i)))
        if i:
            add(row, (h, i - 1, j), Q(i, n) * (c - i + 1 - h) /
                (c + (r - 1) * (i - 1 + h)))
        den = d + (r - 1) * (i + j)
        if h == 0:
            add(row, (1, i, j), Q(1, n) * r * (i + j) / den)
        else:
            add(row, (0, i, j), Q(1, n) * (d - i - j) / den)
        if h and j < m:
            add(row, (h, i, j + 1), Q(m - j, n))
        if not h and j:
            add(row, (h, i, j - 1), Q(j, n))
    else:
        raise ValueError(rule)
    return row


def labelled_changes(c, m, r, rule, mask):
    n = c + m + 1
    graph = [set() for _ in range(n)]
    for u, v in combinations(range(c + 1), 2):
        graph[u].add(v)
        graph[v].add(u)
    for v in range(c + 1, n):
        graph[0].add(v)
        graph[v].add(0)
    mutant = [(mask >> v) & 1 for v in range(n)]
    fitness = [r if mutant[v] else Q(1) for v in range(n)]
    row = {}
    if rule == "Bd":
        total = sum(fitness, Q(0))
        for u in range(n):
            for v in graph[u]:
                p = fitness[u] / total / len(graph[u])
                if mutant[u] != mutant[v]:
                    add(row, mask ^ (1 << v), p)
    else:
        for v in range(n):
            den = sum((fitness[u] for u in graph[v]), Q(0))
            for u in graph[v]:
                p = Q(1, n) * fitness[u] / den
                if mutant[u] != mutant[v]:
                    add(row, mask ^ (1 << v), p)
    return row


def label(c, m, mask):
    h = mask & 1
    i = sum((mask >> v) & 1 for v in range(1, c + 1))
    j = sum((mask >> v) & 1 for v in range(c + 1, c + m + 1))
    return h, i, j


def check_lumping(c=3, m=2):
    n, r = c + m + 1, Q(3, 2)
    for rule in ("Bd", "dB"):
        for mask in range(1 << n):
            aggregated = {}
            for target, p in labelled_changes(c, m, r, rule, mask).items():
                add(aggregated, label(c, m, target), p)
            assert aggregated == quotient_changes(c, m, r, rule, label(c, m, mask))


def check_constants():
    r = Q(3, 2)
    p = 1 - 1 / r
    lam = r * r / 9
    mu = Q(1, 9)
    kappa = 8 * r * r * p / 9
    assert (p, lam, mu, kappa) == (Q(1, 3), Q(1, 4), Q(1, 9), Q(2, 3))
    q = Q(1, 9)
    assert lam * q * q - (lam + mu + kappa) * q + mu == 0
    assert Q(4) != q and lam * 4 * 4 - (lam + mu + kappa) * 4 + mu == 0
    ell = 1 - q
    rho_bd = Q(8, 9) * p + Q(1, 9) * ell
    rho_db = Q(8, 9) * p
    x, y = rho_bd / p, rho_db / p
    assert (ell, rho_bd, rho_db, x, y, x * y) == (
        Q(8, 9), Q(32, 81), Q(8, 27), Q(32, 27), Q(8, 9), Q(256, 243)
    )
    assert x * y > 1 and y < 1
    return p, ell, rho_bd, rho_db, x, y, x * y


def check_averaged_algebra():
    """Verify the three Bd scale limits used after core establishment."""
    y, r, a = sp.symbols("y r a", positive=True)
    pi = r * y / (1 + (r - 1) * y)
    drift = sp.factor((r * pi * (1 - y) - (1 - pi) * y) / (a + 1))
    target = y * (1 - y) * (r**2 - 1) / ((a + 1) * (1 + (r - 1) * y))
    assert sp.simplify(drift - target) == 0

    m, k, ell = sp.symbols("m k ell", positive=True)
    # With a full core and k=O(1) leaves, average over the two hub states.
    activation = r * (1 + k)
    deactivation = m - k
    hub_on = activation / (activation + deactivation)
    leaf_up = hub_on * r * (m - k) / ((a + 1) * m)
    leaf_down = (1 - hub_on) * k / ((a + 1) * m)
    assert sp.simplify(sp.limit(m * leaf_up, m, sp.oo) - r**2 * (1 + k) / (a + 1)) == 0
    assert sp.simplify(sp.limit(m * leaf_down, m, sp.oo) - k / (a + 1)) == 0

    # With ell=O(1) resident leaves, use slow time and reverse the signs.
    activation = r * (1 + m - ell)
    deactivation = ell
    hub_on = activation / (activation + deactivation)
    deficit_down = hub_on * r * ell / ((a + 1) * m)
    deficit_up = (1 - hub_on) * (m - ell) / ((a + 1) * m)
    assert sp.simplify(sp.limit(m * deficit_down, m, sp.oo) - r * ell / (a + 1)) == 0
    assert sp.simplify(sp.limit(m * deficit_up, m, sp.oo) - ell / (r * (a + 1))) == 0


def main():
    check_lumping()
    check_averaged_algebra()
    values = check_constants()
    names = ("core", "Bd_leaf", "rho_Bd", "rho_dB", "Bd_ratio", "dB_ratio", "product")
    print("labelled_lumping=PASS")
    print("averaged_rate_algebra=PASS")
    for name, value in zip(names, values):
        print(f"{name}={value}")
    print("asymptotic_product_counterexample=PASS")


if __name__ == "__main__":
    main()
