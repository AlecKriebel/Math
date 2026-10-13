#!/usr/bin/env python3
"""Exact-rational adversarial checks of the upstream dyadic finite mechanism.

This is independent code, not a copy of the upstream Lean implementation.
It tests finite instances; it does not certify the infinite-dimensional map
or nonamenability theorem. All intervals are represented by rational endpoints.
"""

from fractions import Fraction as Q
from functools import lru_cache
import json
import random


def depth(I):
    length = I[1] - I[0]
    assert length > 0 and length.numerator == 1
    d = length.denominator
    assert d & (d - 1) == 0
    assert (I[0] / length).denominator == 1
    return d.bit_length() - 1


def copy(I, J):
    return tuple(I[0] + (I[1] - I[0]) * x for x in J)


def family(D):
    r = (2 * D).bit_length()
    parents = tuple((Q(2 * i + 1, 2**r), Q(2 * i + 2, 2**r)) for i in range(D))
    children = tuple(tuple(copy(I, J) for J in parents) for I in parents)
    return r, parents, children, parents + tuple(J for row in children for J in row)


def grid_gap(a, b):
    assert a < b
    d = max(a.denominator.bit_length(), b.denominator.bit_length()) - 1
    cells = [(Q(k, 2**d), Q(k + 1, 2**d))
             for k in range(int(a * 2**d), int(b * 2**d))]
    # Merge sibling cells to keep the construction compact.
    changed = True
    while changed:
        changed = False
        merged = []
        i = 0
        while i < len(cells):
            if i + 1 < len(cells):
                I, J = cells[i:i+2]
                ell = I[1] - I[0]
                if ell == J[1] - J[0] and I[1] == J[0] and (I[0] / (2 * ell)).denominator == 1:
                    merged.append((I[0], J[1])); i += 2; changed = True
                    continue
            merged.append(cells[i]); i += 1
        cells = merged
    return cells


def increase_count(cells):
    i = max(range(len(cells)), key=lambda k: cells[k][1] - cells[k][0])
    a, b = cells[i]; m = (a + b) / 2
    cells[i:i+1] = [(a, m), (m, b)]


class PL:
    def __init__(self, source, target):
        self.source, self.target = tuple(source), tuple(target)
        assert len(source) == len(target) and len(source) > 0
        for cells in (source, target):
            assert cells[0][0] == 0 and cells[-1][1] == 1
            assert all(I[1] == J[0] for I, J in zip(cells, cells[1:]))
            for I in cells: depth(I)
        self.exponents = tuple(depth(I) - depth(J) for I, J in zip(source, target))

    def __call__(self, x):
        for I, J in zip(self.source, self.target):
            if I[0] <= x <= I[1]:
                return J[0] + (J[1] - J[0]) * (x - I[0]) / (I[1] - I[0])
        raise AssertionError(x)

    def inverse(self):
        return PL(self.target, self.source)

    def threshold(self, family_depth):
        return max(max(map(depth, self.source)), family_depth + max(self.exponents) + 1)


def transport(I, J, Ip, Jp):
    assert 0 < I[0] < I[1] < J[0] < J[1] < 1
    assert 0 < Ip[0] < Ip[1] < Jp[0] < Jp[1] < 1
    source_gaps = [grid_gap(0, I[0]), grid_gap(I[1], J[0]), grid_gap(J[1], 1)]
    target_gaps = [grid_gap(0, Ip[0]), grid_gap(Ip[1], Jp[0]), grid_gap(Jp[1], 1)]
    for a, b in zip(source_gaps, target_gaps):
        while len(a) < len(b): increase_count(a)
        while len(b) < len(a): increase_count(b)
    source = source_gaps[0] + [I] + source_gaps[1] + [J] + source_gaps[2]
    target = target_gaps[0] + [Ip] + target_gaps[1] + [Jp] + target_gaps[2]
    h = PL(source, target)
    assert tuple(map(h, I)) == Ip and tuple(map(h, J)) == Jp
    return h


def restrict(T, I):
    cells = tuple(J for J in T if I[0] <= J[0] and J[1] <= I[1])
    assert cells and cells[0][0] == I[0] and cells[-1][1] == I[1]
    assert all(J[1] == K[0] for J, K in zip(cells, cells[1:]))
    out = tuple(tuple((x - I[0]) / (I[1] - I[0]) for x in J) for J in cells)
    for J in out: depth(J)
    return out


def uniform(n):
    return tuple((Q(k, 2**n), Q(k + 1, 2**n)) for k in range(2**n))


def exact_checks():
    pair_count = 0
    covariance_count = 0
    recursion_count = 0
    for D in (2, 3, 5, 7):
        r, parents, children, intervals = family(D)
        for I in intervals: depth(I)
        for I in intervals:
            for J in intervals:
                if I[1] >= J[0]: continue
                h = transport(I, J, parents[0], parents[1])
                n = h.threshold(2 * r)
                # Uniform source cells resolve every source piece. Their images
                # are basic cells and mesh is smaller than every family member.
                assert n >= max(map(depth, h.source))
                assert all(n - q > 2 * r for q in h.exponents)
                for selected, target in ((I, parents[0]), (J, parents[1])):
                    for K in uniform(3):
                        C = copy(selected, K)
                        image = tuple(map(h, C))
                        assert image == copy(target, K)
                        depth(image)
                        covariance_count += 1
                pair_count += 1
        # Test normalized restriction associativity on both uniform and
        # nonuniform refinements, including cells at all family endpoints.
        T = list(uniform(2 * r))
        rng = random.Random(D)
        for _ in range(13):
            index = rng.randrange(len(T)); a, b = T[index]; mid = (a + b) / 2
            T[index:index+1] = [(a, mid), (mid, b)]
        T = tuple(T)
        for i, I in enumerate(parents):
            for j, J in enumerate(parents):
                assert restrict(restrict(T, I), J) == restrict(T, children[i][j])
        # Use a bounded nonconstant Lipschitz scalar color. This map has a fixed
        # point and is deliberately not offered as a displacement witness.
        @lru_cache(None)
        def color(partition):
            try: sub = tuple(restrict(partition, I) for I in parents)
            except AssertionError: return Q(0)
            assert all(len(U) < len(partition) for U in sub)
            out = Q(1, 4) - sum(map(color, sub), Q(0)) / (2 * D)
            assert -1 <= out <= 1
            return out
        for i, I in enumerate(parents):
            x = color(restrict(T, I))
            z = sum((color(restrict(T, children[i][j])) for j in range(D)), Q(0)) / D
            assert x == Q(1, 4) - z / 2
            recursion_count += 1
    # Fully enumerate actual image partitions for a nontrivial transport.
    r, p, c, all_intervals = family(3)
    I, J = c[0][1], c[2][2]
    h = transport(I, J, p[0], p[1])
    n = h.threshold(2 * r)
    T = uniform(n)
    hT = tuple(tuple(map(h, K)) for K in T)
    for K in hT: depth(K)
    for K in all_intervals: restrict(hT, K)
    assert restrict(T, I) == restrict(hT, p[0])
    assert restrict(T, J) == restrict(hT, p[1])
    return {"status": "pass", "transport_pairs": pair_count,
            "local_covariance_cells": covariance_count,
            "recursive_identities": recursion_count,
            "fully_enumerated_image_level": n,
            "fully_enumerated_image_cells": len(hT),
            "scope": "Exact finite dyadic checks, not a theorem/formal build certificate"}


if __name__ == "__main__":
    print(json.dumps(exact_checks(), indent=2))
