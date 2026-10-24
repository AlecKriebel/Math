#!/usr/bin/env python3
"""Exact rational homology diagnostics for Kourovka 21.139.

No third-party packages; python3 exact_cover_diagnostics.py reproduces results.
This computes selected covers. The universal statements are proved separately
in ../approach_counterexamples.md; no finite computation proves bounded vb_2.
"""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def subtract_identity(a):
    return [[a[i][j] - int(i == j) for j in range(len(a))]
            for i in range(len(a))]


def rank(a):
    """Exact Gaussian elimination over Q, returning rank and pivot columns."""
    a = [list(map(Fraction, row)) for row in a]
    k = 0
    pivots = []
    for c in range(len(a[0])):
        p = next((i for i in range(k, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[k], a[p] = a[p], a[k]
        scale = a[k][c]
        a[k] = [x / scale for x in a[k]]
        for i in range(k + 1, len(a)):
            scale = a[i][c]
            if scale:
                a[i] = [x - scale * y for x, y in zip(a[i], a[k])]
        pivots.append(c)
        k += 1
        if k == len(a):
            break
    return k, pivots


def power(a, n):
    out = identity(len(a))
    while n:
        if n & 1:
            out = matmul(out, a)
        a = matmul(a, a)
        n //= 2
    return out


def mod_order(a, p):
    out = identity(len(a))
    for n in range(1, 10000):
        out = [[x % p for x in row] for row in matmul(out, a)]
        if out == identity(len(a)):
            return n
    raise AssertionError('order search bound exhausted')


def phi_iterates(n):
    phi = {'a': 'b', 'b': 'c', 'c': 'ab'}
    words = {x: x for x in phi}
    for _ in range(n):
        words = {x: ''.join(phi[y] for y in word)
                 for x, word in words.items()}
    return words


def graph_cover_matrices(p, monodromy_power):
    """Cell maps of the (Z/p)^3 cover of the 3-rose under phi^power.

    Column (v,i) represents the positively oriented i-edge based at v.
    The vertex map is v -> M^power v. A positive word's cellular
    image is found by traversing the word from M^power v, counting edges.
    """
    vertices = list(product(range(p), repeat=3))
    positions = {v: i for i, v in enumerate(vertices)}
    n = 3 * len(vertices)
    boundary = [[0] * n for _ in vertices]
    chain_map = [[0] * n for _ in range(n)]
    words = phi_iterates(monodromy_power)
    m = power([[0, 0, 1], [1, 0, 1], [0, 1, 0]], monodromy_power)
    def image_vertex(v):
        return tuple(sum(m[i][j] * v[j] for j in range(3)) % p for i in range(3))
    vertex_map = [[0] * len(vertices) for _ in vertices]
    for v in vertices:
        vertex_map[positions[image_vertex(v)]][positions[v]] = 1
    for v in vertices:
        for i, letter in enumerate('abc'):
            col = 3 * positions[v] + i
            endpoint = list(v)
            endpoint[i] = (endpoint[i] + 1) % p
            boundary[positions[v]][col] -= 1
            boundary[positions[tuple(endpoint)]][col] += 1
            cursor = list(image_vertex(v))
            for y in words[letter]:
                j = 'abc'.index(y)
                row = 3 * positions[tuple(cursor)] + j
                chain_map[row][col] += 1
                cursor[j] = (cursor[j] + 1) % p
            assert tuple(cursor) == image_vertex(endpoint)
    # This is essential: the chain map must commute with the boundary.
    assert matmul(boundary, chain_map) == matmul(vertex_map, boundary)
    return boundary, chain_map, words, vertex_map


def icosahedron():
    vertices = ['N', 'S'] + [f'a{i}' for i in range(5)] + [f'b{i}' for i in range(5)]
    edges = set()
    def add(x, y):
        edges.add(tuple(sorted((x, y))))
    for i in range(5):
        add('N', f'a{i}')
        add('S', f'b{i}')
        add(f'a{i}', f'a{(i + 1) % 5}')
        add(f'b{i}', f'b{(i + 1) % 5}')
        add(f'a{i}', f'b{i}')
        add(f'a{i}', f'b{(i - 1) % 5}')
    def adjacent(x, y):
        return tuple(sorted((x, y))) in edges
    triangles = [t for t in combinations(vertices, 3)
                 if all(adjacent(x, y) for x, y in combinations(t, 2))]
    squares = [s for s in combinations(vertices, 4)
               if sum(adjacent(x, y) for x, y in combinations(s, 2)) == 4
               and all(sum(adjacent(x, y) for y in s if x != y) == 2 for x in s)]
    four_cliques = [s for s in combinations(vertices, 4)
                    if all(adjacent(x, y) for x, y in combinations(s, 2))]
    assert len(vertices) == 12 and len(edges) == 30 and len(triangles) == 20
    assert not squares and not four_cliques
    cycle = [f'a{i}' for i in range(5)]
    assert sum(adjacent(x, y) for x, y in combinations(cycle, 2)) == 5
    assert not adjacent('S', 'a0')
    return {'vertices': vertices, 'edges': sorted(edges), 'triangles': triangles,
            'induced_squares': squares, 'four_cliques': four_cliques,
            'induced_pentagon': cycle, 'outside_vertex_missing_cycle': ['S', 'a0'],
            'flag_complex_euler_characteristic': 12 - 30 + 20}


def main():
    # Columns are the exponent vectors of phi(a), phi(b), phi(c).
    m = [[0, 0, 1], [1, 0, 1], [0, 1, 0]]
    assert matmul(matmul(m, m), m) == [[m[i][j] + int(i == j) for j in range(3)] for i in range(3)]
    cyclic = []
    for n in range(1, 41):
        r, pivots = rank(subtract_identity(power(m, n)))
        assert r == 3
        cyclic.append({'degree': n, 'b2': 3 - r, 'rank_Mn_minus_I': r})
    order = mod_order(m, 2)
    assert order == 7
    d, t, words, fixed_vertices = graph_cover_matrices(2, order)
    assert fixed_vertices == identity(8)
    d2, t2, words2, vertex_map2 = graph_cover_matrices(2, 2)
    r2, pivots2 = rank(d2 + subtract_identity(t2))
    assert r2 == 23
    index16 = {'monodromy_power': 2, 'total_index': 16,
               'stacked_rational_rank': r2, 'b2': 24 - r2,
               'pivot_columns': pivots2, 'phi2_words': words2,
               'phi2_vertex_matrix': vertex_map2, 'phi2_chain_matrix': t2}
    rd, _ = rank(d)
    assert rd == 7
    special_covers = []
    for n in range(1, 13):
        stacked = d + subtract_identity(power(t, n))
        r, pivots = rank(stacked)
        b2 = len(t) - r
        special_covers.append({'monodromy_power': order * n,
                               'total_index': 8 * order * n,
                               'stacked_rational_rank': r,
                               'pivot_columns': pivots, 'b2': b2})
    assert special_covers[0]['b2'] == 0
    assert special_covers[1]['b2'] == 7
    # This is selected-cover evidence, not an all-cover upper bound.
    output = {'phi': {'a': 'b', 'b': 'c', 'c': 'ab'},
              'characteristic_polynomial': 'x^3-x-1',
              'cyclic_mapping_torus_covers': cyclic,
              'mod2_matrix_order': order, 'phi7_words': words,
              'graph_cover_boundary_rank': rd,
              'graph_cover_C0_dimension': len(d),
              'graph_cover_C1_dimension': len(t),
              'phi7_chain_matrix_T': t, 'graph_boundary_matrix': d,
              'characteristic_fiber_covers': special_covers,
              'index16_cover': index16,
              'icosahedral_graph': icosahedron()}
    path = Path(__file__).with_name('exact_results.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print('Exact checks passed.')
    print('Original cyclic tower: b2=0 for degrees 1..40 (all n proved in note).')
    print('Characteristic fiber cover: index=16, b2=1, rational stacked rank=23.')
    print('Characteristic fiber cover: index=112, b2=7, rational stacked rank=17.')
    print('Icosahedral graph: 12 vertices, 30 edges, 20 triangles, no induced C4.')
    print(f'Wrote {path.name}')


if __name__ == '__main__':
    main()
