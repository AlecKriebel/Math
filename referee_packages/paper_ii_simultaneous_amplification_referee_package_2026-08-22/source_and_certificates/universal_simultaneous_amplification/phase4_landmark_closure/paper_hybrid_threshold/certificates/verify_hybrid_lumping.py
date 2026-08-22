#!/usr/bin/env python3
"""Exact labelled audit of the five-coordinate hybrid lumping.

This implementation does not import the discovery solver.  It constructs a
small labelled graph, enumerates every Bd source--target and dB death--parent
event over ``Fraction``, aggregates by the orbit label, and compares with an
independently written formula for ``(h,i,u,v,l)`` transitions.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


R = F(3, 2)
CORE, PAIRS, PENDANTS = 3, 2, 2
SIGMA, EPSILON = F(19, 137), F(1, 100)
PAIR_WEIGHT = F(CORE, 1) / SIGMA


def graph():
    n = CORE + 2 * PAIRS + PENDANTS
    weights = [[F(0) for _ in range(n)] for _ in range(n)]
    for a, b in combinations(range(CORE), 2):
        weights[a][b] = weights[b][a] = F(1)
    offset = CORE
    for pair in range(PAIRS):
        left, right = offset + 2 * pair, offset + 2 * pair + 1
        weights[left][right] = weights[right][left] = PAIR_WEIGHT
        for vertex in (left, right):
            for core in range(CORE):
                weights[vertex][core] = weights[core][vertex] = EPSILON
    offset += 2 * PAIRS
    for pendant in range(PENDANTS):
        vertex = offset + pendant
        weights[0][vertex] = weights[vertex][0] = F(1)
    return weights


def label(mask: int):
    h = (mask >> 0) & 1
    i = sum((mask >> vertex) & 1 for vertex in range(1, CORE))
    u = v = 0
    offset = CORE
    for pair in range(PAIRS):
        count = ((mask >> (offset + 2 * pair)) & 1) + ((mask >> (offset + 2 * pair + 1)) & 1)
        u += count == 1
        v += count == 2
    offset += 2 * PAIRS
    l = sum((mask >> (offset + pendant)) & 1 for pendant in range(PENDANTS))
    return h, i, u, v, l


def add(row, target, value):
    if value:
        row[target] = row.get(target, F(0)) + value


def labelled(mask: int, rule: str):
    weights = graph()
    n = len(weights)
    mutant = [bool(mask & (1 << vertex)) for vertex in range(n)]
    fitness = [R if kind else F(1) for kind in mutant]
    row = {}
    if rule == "Bd":
        total = sum(fitness, F(0))
        degree = [sum(values, F(0)) for values in weights]
        for parent in range(n):
            for target in range(n):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    probability = fitness[parent] / total * weights[parent][target] / degree[parent]
                    add(row, label(mask ^ (1 << target)), probability)
    elif rule == "dB":
        for target in range(n):
            denominator = sum(
                (fitness[parent] * weights[parent][target] for parent in range(n)), F(0)
            )
            for parent in range(n):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    probability = F(1, n) * fitness[parent] * weights[parent][target] / denominator
                    add(row, label(mask ^ (1 << target)), probability)
    else:
        raise ValueError(rule)
    return row


def declared(state, rule: str):
    h, i, u, v, l = state
    c, q, k = CORE - 1, PAIRS, PENDANTS
    n0 = q - u - v
    mp = u + 2 * v
    rp = 2 * q - mp
    W, e = PAIR_WEIGHT, EPSILON
    dh, do, dp = F(c) + 2 * q * e + k, F(c) + 2 * q * e, W + CORE * e
    row = {}
    if rule == "Bd":
        scale = 1 / (F(CORE + 2 * q + k) + (R - 1) * (h + i + mp + l))
        if h == 0:
            add(row, (1, i, u, v, l), scale * R * (F(i, 1) / do + mp * e / dp + l))
        else:
            add(row, (0, i, u, v, l), scale * (F(c - i, 1) / do + rp * e / dp + k - l))
        if i < c:
            add(row, (h, i + 1, u, v, l), scale * R * (c - i) * (F(h, 1) / dh + F(i, 1) / do + mp * e / dp))
        if i:
            add(row, (h, i - 1, u, v, l), scale * i * (F(1 - h, 1) / dh + F(c - i, 1) / do + rp * e / dp))
        mb = e * (F(h, 1) / dh + F(i, 1) / do)
        rb = e * (F(1 - h, 1) / dh + F(c - i, 1) / do)
        if n0:
            add(row, (h, i, u + 1, v, l), scale * R * 2 * n0 * mb)
        if u:
            add(row, (h, i, u - 1, v + 1, l), scale * R * u * (mb + W / dp))
            add(row, (h, i, u - 1, v, l), scale * u * (rb + W / dp))
        if v:
            add(row, (h, i, u + 1, v - 1, l), scale * 2 * v * rb)
        if h and l < k:
            add(row, (h, i, u, v, l + 1), scale * R * (k - l) / dh)
        if not h and l:
            add(row, (h, i, u, v, l - 1), scale * l / dh)
    elif rule == "dB":
        scale = F(1, CORE + 2 * q + k)
        mm, rm = i + mp * e + l, c - i + rp * e + k - l
        if h == 0 and mm:
            add(row, (1, i, u, v, l), scale * R * mm / (R * mm + rm))
        if h == 1 and rm:
            add(row, (0, i, u, v, l), scale * rm / (R * mm + rm))
        if i < c:
            mm = h + i + mp * e; rm = do - mm
            add(row, (h, i + 1, u, v, l), scale * (c - i) * R * mm / (R * mm + rm))
        if i:
            mm = h + i - 1 + mp * e; rm = do - mm
            add(row, (h, i - 1, u, v, l), scale * i * rm / (R * mm + rm))
        mb, rb = e * (h + i), e * (CORE - h - i)
        if n0 and mb:
            add(row, (h, i, u + 1, v, l), scale * 2 * n0 * R * mb / (R * mb + W + rb))
        if u:
            add(row, (h, i, u - 1, v + 1, l), scale * u * R * (W + mb) / (R * (W + mb) + rb))
            add(row, (h, i, u - 1, v, l), scale * u * (W + rb) / (R * mb + W + rb))
        if v and rb:
            add(row, (h, i, u + 1, v - 1, l), scale * 2 * v * rb / (R * (W + mb) + rb))
        if h and l < k:
            add(row, (h, i, u, v, l + 1), scale * (k - l))
        if not h and l:
            add(row, (h, i, u, v, l - 1), scale * l)
    else:
        raise ValueError(rule)
    return row


def main():
    n = CORE + 2 * PAIRS + PENDANTS
    fibres = {}
    for mask in range(1 << n):
        fibres.setdefault(label(mask), []).append(mask)
    for rule in ("Bd", "dB"):
        for state, masks in fibres.items():
            expected = declared(state, rule)
            for mask in masks:
                assert labelled(mask, rule) == expected, (rule, state, mask)
    print(f"PASS exact labelled hybrid lumping: n={n}, masks={1<<n}, fibres={len(fibres)}")


if __name__ == "__main__":
    main()
