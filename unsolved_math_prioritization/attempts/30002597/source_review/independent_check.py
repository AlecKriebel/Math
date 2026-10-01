#!/usr/bin/env python3
"""Independent finite check, starting with Carter's signed word.

Does not import the author's verifier. Ribbon boundaries are counted by gluing
disk corners with union-find, rather than tracing its dart permutation.
Topology and source applicability are reviewed in REVIEW.md, not proved here.
"""
from collections import Counter
from itertools import permutations
from pathlib import Path
import hashlib
import json


COUNT = 0


def check(ok):
    global COUNT
    if not ok:
        raise AssertionError("independent control failed")
    COUNT += 1


def word_indices(word):
    labels = sorted({label for label, _ in word})
    assert len(word) == 2 * len(labels)
    for label in labels:
        assert sorted(sign for name, sign in word if name == label) == [-1, 1]
    out = []
    for label in labels:
        start = word.index((label, -1))
        stop = word.index((label, 1))
        i, total = (start + 1) % len(word), 0
        while i != stop:
            total -= word[i][1]
            i = (i + 1) % len(word)
        out.append(total)
    return out


def poly(indices):
    c = Counter()
    for x in indices:
        if x:
            c[abs(x)] += 1 if x > 0 else -1
    return {k: c[k] for k in sorted(c) if c[k]}


def boundary_count(word):
    labels = sorted({label for label, _ in word})
    parent = {(label, k): (label, k) for label in labels for k in range(4)}

    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def join(x, y):
        parent[root(x)] = root(y)

    ray_corner = {}
    for label in labels:
        t, h = word.index((label, -1)), word.index((label, 1))
        for k, ray in enumerate(((t, 1), (h, 1), (t, -1), (h, -1))):
            ray_corner[ray] = (label, k)
    for i in range(len(word)):
        left, a = ray_corner[(i, 1)]
        right, b = ray_corner[((i + 1) % len(word), -1)]
        # An untwisted edge pairs opposite sides at its two ends.
        join((left, (a - 1) % 4), (right, b))
        join((left, a), (right, (b - 1) % 4))
    return len({root(x) for x in parent})


def determinant(a):
    n = len(a)
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        value = (-1) ** inversions
        for i in range(n):
            value *= a[i][p[i]]
        total += value
    return total


def main():
    word = [('a', 1), ('b', 1), ('c', 1), ('b', -1), ('a', -1), ('c', -1)]
    indices = word_indices(word)
    check(indices == [1, 1, -2])
    check(poly(indices) == {1: 2, 2: -1})
    check(boundary_count(word) == 1)
    check(3 - 6 + boundary_count(word) == -2)
    variants = 0
    for reverse in (False, True):
        for invert in (False, True):
            w = list(reversed(word)) if reverse else list(word)
            if invert:
                w = [(label, -sign) for label, sign in w]
            for shift in range(6):
                v = w[shift:] + w[:shift]
                p = poly(word_indices(v))
                check(p == ({1: -2, 2: 1} if reverse else {1: 2, 2: -1}))
                check(boundary_count(v) == 1)
                check(sum(word_indices(v)) == 0)
                variants += 1
    # Complete list of involutions on three labels, represented by images.
    tested = 0
    for p in permutations(range(3)):
        if all(p[p[i]] == i for i in range(3)):
            orbits = {tuple(sorted({i, p[i]})) for i in range(3)}
            check(any(sum(indices[i] for i in orbit) for orbit in orbits))
            tested += 1
    check(tested == 4)
    matrix = [[0, -1, -1, 2], [1, 0, 0, 1], [1, 0, 0, 2], [-2, -1, -2, 0]]
    check(determinant(matrix) == 1)
    check(all(matrix[i][j] == -matrix[j][i] for i in range(4) for j in range(4)))
    # Controls for an embedded circle's one-crossing curl and a nested pair.
    check(boundary_count([('a', -1), ('a', 1)]) == 3)
    check(poly(word_indices([('a', -1), ('a', 1)])) == {})
    check(poly(word_indices([('a', -1), ('a', 1), ('b', -1), ('b', 1)])) == {})
    bad = [('a', -1), ('a', -1)]
    try:
        word_indices(bad)
    except AssertionError:
        check(True)
    else:
        raise AssertionError('Malformed word was accepted')
    print(json.dumps({'status': 'PASS', 'assertions': COUNT,
                      'indices': indices, 'polynomial': poly(indices),
                      'boundary_components': boundary_count(word),
                      'genus': 2, 'orientation_basepoint_variants': variants,
                      'involutions_checked': tested,
                      'based_matrix_determinant': determinant(matrix),
                      'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'limitation': 'Finite combinatorics only; no classification or topology certification'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
