#!/usr/bin/env python3
"""Independent exact rational checks; no infinite-dimensional theorem is inferred."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import json


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(c, a):
    return [[c*x for x in r] for r in a]


def mul(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def star(a):
    return [list(r) for r in zip(*a)]  # all test coefficients are real


def total(items, n):
    a = zero(n)
    for b in items:
        a = add(a, b)
    return a


def matrix_unit(n, i, j):
    a = zero(n)
    a[i][j] = F(1)
    return a


def diagonal(values):
    a = zero(len(values))
    for i, value in enumerate(values):
        a[i][i] = F(value)
    return a


def character(label, group_element):
    return (-1) ** ((label & group_element).bit_count() % 2)


def ad(u, a):
    return mul(mul(u, a), star(u))


def main():
    n = 4
    unit = eye(n)
    group = range(4)  # Z_2 x Z_2 with xor as group operation
    reps = [diagonal([character(k, g) for k in range(4)]) for g in group]
    v = [F(1), F(2), F(2), F(4)]
    q = [[F(i == j) - F(2, 25)*v[i]*v[j] for j in range(n)] for i in range(n)]
    assert mul(q, star(q)) == unit
    p = matrix_unit(n, 0, 0)
    basis = [matrix_unit(n, i, j) for i in range(n) for j in range(n)]
    ys = []
    for j in range(n):
        y = zero(n)
        for i in range(n):
            y[i][0] = q[i][j]
        ys.append(y)
    assert total([mul(y, star(y)) for y in ys], n) == unit
    assert any(ad(reps[g], y) not in (y, scale(-1, y)) for y in ys for g in group)
    xs = []
    for y in ys:
        for label in group:
            x = scale(F(1, 4), total([scale(character(label, h), ad(reps[h], y)) for h in group], n))
            assert all(ad(reps[h], x) == scale(character(label, h), x) for h in group)
            xs.append(x)
    assert total([mul(x, star(x)) for x in xs], n) == unit
    frame_implementation_checks = 0
    for g in group:
        lift = total([mul(mul(ad(reps[g], x), p), star(x)) for x in xs], n)
        assert lift == reps[g]
        assert mul(lift, star(lift)) == mul(star(lift), lift) == unit
        assert all(ad(reps[h], lift) == lift for h in group)
        for a in basis:
            assert ad(lift, a) == ad(reps[g], a)
            frame_implementation_checks += 1

    # Noncommutative honest cocycle obtained by conjugating the representation.
    new_reps = [mul(mul(q, r), star(q)) for r in reps]
    ds = [mul(new_reps[g], star(reps[g])) for g in group]
    assert any(ad(reps[h], ds[g]) != ds[g] for g in group for h in group)
    assert any(mul(ds[g], ds[h]) != mul(ds[h], ds[g]) for g in group for h in group)
    for g, h in product(group, repeat=2):
        assert mul(ds[g], ad(reps[g], ds[h])) == ds[g ^ h]
        assert mul(ds[h], ad(reps[h], ds[g])) == mul(ds[g], ad(reps[g], ds[h]))
        e_g, e_h = star(ds[g]), star(ds[h])
        assert mul(e_g, ad(new_reps[g], e_h)) == star(ds[g ^ h])
        t = mul(ds[g], reps[g])
        assert t == new_reps[g]
        assert ad(new_reps[h], t) == t
        avg = scale(F(1, 4), total([ad(new_reps[k], t) for k in group], n))
        assert avg == t
        for a in basis:
            assert ad(t, a) == ad(ds[g], ad(reps[g], a))

    # Projective obstruction: every matrix commuting with X and Z is scalar.
    x = [[F(0), F(1)], [F(1), F(0)]]
    z = diagonal([1, -1])
    assert mul(x, z) == scale(-1, mul(z, x))
    pauli = [eye(2), x, z, mul(x, z)]
    assert mul(mul(mul(x, z), star(x)), star(z)) == scale(-1, eye(2))
    fixed_basis_averages = []
    for i, j in product(range(2), repeat=2):
        a = matrix_unit(2, i, j)
        avg = scale(F(1, 4), total([ad(u, a) for u in pauli], 2))
        fixed_basis_averages.append(avg)
        assert avg == scale(F(i == j, 2), eye(2))

    # Bidirected K_2,2, exact CK source-character subclass.
    vertices = range(4)
    edges = [(i, j) for i in vertices for j in vertices if (i < 2) != (j < 2)]
    paths = {0: [], 1: [(0, 2), (2, 1)], 2: [(0, 2)], 3: [(0, 3)]}
    cycles = []
    def visit(start, current, visited, path):
        for e in edges:
            if e[0] != current:
                continue
            if e[1] == start:
                cycles.append(path + [e])
            elif e[1] not in visited:
                visit(start, e[1], visited | {e[1]}, path + [e])
    for start in vertices:
        visit(start, start, {start}, [])

    histogram = Counter()
    for labels in product(group, repeat=4):
        def path_label(path):
            result = 0
            for i, _ in path:
                result ^= labels[i]
            return result
        potentials = [path_label(paths[i]) for i in vertices]
        kernel = {g for g in group if all(character(path_label(c), g) == 1 for c in cycles)}
        residual = [potentials[i] ^ labels[i] ^ potentials[j] for i, j in edges]
        twisted_kernel = {g for g in group if all(character(r, g) == 1 for r in residual)}
        assert twisted_kernel == kernel
        for g in kernel:
            for i, j in edges:
                assert character(labels[i], g) == character(potentials[i], g)*character(potentials[j], g)
        histogram[len(kernel)] += 1

    # The mixed source labeling is faithful and has a nontrivial inner kernel.
    mixed = [1, 1, 2, 2]
    ordinary = {g for g in group if all(character(l, g) == 1 for l in mixed)}
    inner = {g for g in group if character(mixed[0] ^ mixed[2], g) == 1}
    assert ordinary == {0} and inner == {0, 3}
    # Return graph on the first cyclic class: two distinct length-two paths per pair.
    return_adjacency = [[sum(1 for k in [2, 3] if (i, k) in edges and (k, j) in edges)
                         for j in [0, 1]] for i in [0, 1]]
    assert return_adjacency == [[2, 2], [2, 2]]
    result = {
        'arithmetic': 'exact rational, real matrices; no floating point',
        'group': 'Z2 x Z2',
        'fourier_frame_elements': len(xs),
        'nonhomogeneous_initial_frame': True,
        'frame_matrix_unit_implementation_checks': frame_implementation_checks,
        'ambient_full_corner_not_fixed_full': 'rank-one p in M4, fixed algebra diagonal',
        'honest_noncommutative_cocycle_and_inverse': 'all 16 group pairs passed',
        'cocycle_not_beta_fixed': True,
        'pauli_fixed_expectation': 'matrix-unit averages equal trace(a)/2 times identity',
        'source_label_assignments_checked': 4**4,
        'inner_kernel_size_histogram': dict(sorted(histogram.items())),
        'mixed_ordinary_kernel': sorted(ordinary),
        'mixed_inner_kernel': sorted(inner),
        'period_two_return_adjacency': return_adjacency,
        'scope': 'finite algebraic consistency checks; general proofs are in REPORT.md',
        'all_assertions_passed': True,
    }
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
