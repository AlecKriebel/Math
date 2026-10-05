"""New bounded exact controls, authored without importing package code.

The finite primitive continuum check uses all vertices of the line arrangement
where x, x-h, or x+h is a grid point. This is not a limiting-measure proof.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import hashlib
import json

counts = Counter()


def ck(name, value):
    if not value:
        raise AssertionError(name)
    counts[name] += 1


def split(a, b, c):
    if b == 0:
        return (0,) * 4
    left = 2 * (a >= b) - 1
    right = 2 * (c > b) - 1
    middle = {2: (-1, -1), 0: (-1, 1), -2: (1, 1)}[left + right]
    return (b + left, b + middle[0], b + middle[1], b + right)


def step(values):
    n = len(values)
    return [v for j, b in enumerate(values)
            for v in split(values[(j - 1) % n], b, values[(j + 1) % n])]


cycles = 0
for length in range(1, 7):
    for values in product(range(5), repeat=length):
        if any(abs(values[j] - values[(j + 1) % length]) > 2
               for j in range(length)):
            continue
        for offset in (0, 1000001):
            original = [a + offset for a in values]
            refined = step(original)
            ck("cyclic_output_size", len(refined) == 4 * length)
            ck("cyclic_total_mass", sum(refined) == 4 * sum(original))
            ck("cyclic_nonnegativity", min(refined) >= 0)
            ck("every_refined_cyclic_edge",
               all(abs(a - refined[(j + 1) % len(refined)]) <= 2
                   for j, a in enumerate(refined)))
            for j, a in enumerate(original):
                block = refined[4 * j:4 * j + 4]
                ck("parent_mass", sum(block) == 4 * a)
                ck("parent_absorption_or_fairness",
                   block == [0] * 4 if a == 0 else
                   sorted(b - a for b in block) == [-1, -1, 1, 1])
            cycles += 1


def primitive(values):
    n = len(values)
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v - 1)

    def H(x):
        x %= 1
        y = x * n
        j = y.numerator // y.denominator
        return Q(prefix[j], n) + (y - j) * Q(values[j] - 1, n)
    return H


stage_rows = []
for kind in ("submitted", "Kahane_fixed"):
    values = [1]
    for generation in range(5):
        n = len(values)
        ck("stage_mass", sum(values) == n)
        ck("stage_neighbors", all(abs(a - values[(j + 1) % n]) <= 2
                                  for j, a in enumerate(values)))
        H = primitive(values)
        max_norm = max(abs(H(Q(j, n))) for j in range(n))
        ck("large_h_primitive_control", 4 * max_norm <= 6)
        max_ratio = Q(0)
        vertices = 0
        if generation:
            # Every arrangement vertex in 0<=x<=1, 0<h<=1/4 lies on this
            # lattice. At h=0 the limiting ratio is a grid slope jump, <=2.
            for k in range(1, n // 2 + 1):
                h = Q(k, 2 * n)
                for j in range(2 * n + 1):
                    x = Q(j, 2 * n)
                    ratio = abs(H(x + h) + H(x - h) - 2 * H(x)) / h
                    ck("exact_arrangement_lattice_ratio", ratio <= 24)
                    max_ratio = max(max_ratio, ratio)
                    vertices += 1
        stage_rows.append({"rule": kind, "generation": generation,
                           "cells": n, "lattice_evaluations": vertices,
                           "maximum_ratio": str(max_ratio),
                           "primitive_norm": str(max_norm)})
        if kind == "submitted":
            values = step(values)
        else:
            values = [x for a in values for x in
                      ((a - 1, a + 1, a + 1, a - 1) if a else (0,) * 4)]

result = {"status": "PASS", "cycles_including_high_translates": cycles,
          "exact_checks": sum(counts.values()),
          "checks_by_category": dict(counts), "primitive_stages": stage_rows,
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "scope": "New independent bounded cyclic transitions and exact finite-stage primitive controls. No universal limiting, purity, priority, or human-review claim."}
Path(__file__).with_name("INDEPENDENT_ADVERSARY_RESULTS.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
