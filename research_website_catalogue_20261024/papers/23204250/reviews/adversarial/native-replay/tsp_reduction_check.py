#!/usr/bin/env python3
"""Finite checks of the PM-to-TSP projections; no PSD lower bound checked."""
from collections import Counter
from datetime import datetime, timezone
from itertools import permutations
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json
import platform


def edge(i, j):
    assert i != j
    return tuple(sorted((i, j)))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i+1:]
        for matching in matchings(rest):
            yield tuple(sorted((edge(vertices[0], vertices[i]),) + matching))


def degrees(n, edges):
    result = [0] * n
    for i, j in edges:
        result[i] += 1
        result[j] += 1
    return result


def connected(n, edges):
    neighbors = [set() for _ in range(n)]
    for i, j in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)
    seen, todo = {0}, [0]
    while todo:
        i = todo.pop()
        for j in neighbors[i] - seen:
            seen.add(j)
            todo.append(j)
    return len(seen) == n


def is_tour(n, edges):
    return (len(set(edges)) == n and degrees(n, edges) == [2] * n
            and connected(n, edges))


def all_tours(n):
    """Fix city 0 first and suppress reversals of undirected cycles."""
    for order in permutations(range(1, n)):
        if order[0] > order[-1]:
            continue
        order = (0,) + order
        yield frozenset(edge(order[i], order[(i+1) % n]) for i in range(n))


def gadget(n, left, right, layers):
    result = set(left)
    result.update(edge((layers-1)*n+i, (layers-1)*n+j) for i, j in right)
    result.update(edge(i, n+i) for i in range(n))
    if layers == 3:
        result.update(edge(n+i, 2*n+i) for i in range(n))
    return frozenset(result)


def project_left(n, edges):
    return tuple(sorted((i, j) for i, j in edges if j < n))


def allowed_original(n):
    result = {edge(i, j) for i in range(n) for j in range(i+1, n)}
    result.update(edge(2*n+i, 2*n+j) for i in range(n) for j in range(i+1, n))
    result.update(edge(i, n+i) for i in range(n))
    result.update(edge(n+i, 2*n+i) for i in range(n))
    return result


def compressed_face(n, tour):
    forced = {edge(i, n+i) for i in range(n)}
    forbidden = {edge(i, n+j) for i in range(n) for j in range(n) if i != j}
    return forced <= tour and not (forbidden & tour)


def check_pairs():
    rows, generated = [], {}
    for n in (2, 4, 6, 8):
        ms = list(matchings(tuple(range(n))))
        preimages = Counter({matching: 0 for matching in ms})
        tours = {2: set(), 3: set()}
        for left in ms:
            for right in ms:
                assert degrees(n, left+right) == [2]*n  # multigraph copies
                good = connected(n, left+right)
                for layers in (2, 3):
                    actual = gadget(n, left, right, layers)
                    assert len(actual) == layers*n
                    assert degrees(layers*n, actual) == [2]*(layers*n)
                    assert is_tour(layers*n, actual) == good
                    assert project_left(n, actual) == left
                    assert (actual <= allowed_original(n) if layers == 3
                            else compressed_face(n, actual))
                    if good:
                        tours[layers].add(actual)
                if good:
                    preimages[left] += 1
        expected = 2**(n//2-1) * factorial(n//2-1)
        assert all(preimages.values())
        assert set(preimages.values()) == {expected}
        assert len(tours[2]) == len(tours[3]) == factorial(n-1)
        generated[n, 2], generated[n, 3] = tours[2], tours[3]
        rows.append({'matching_vertices': n, 'perfect_matchings': len(ms),
                     'matching_pairs_checked': len(ms)**2,
                     'original_cities': 3*n, 'compressed_cities': 2*n,
                     'tours_in_each_face': len(tours[2]),
                     'preimages_of_each_matching': expected,
                     'rejected_disconnected_pairs': len(ms)**2-sum(preimages.values())})
    ambient_rows = []
    for n, layers in ((2, 3), (2, 2), (4, 2)):
        accepted, count = set(), 0
        for tour in all_tours(n*layers):
            count += 1
            if (tour <= allowed_original(n) if layers == 3
                    else compressed_face(n, tour)):
                accepted.add(tour)
        assert count == factorial(n*layers-1)//2
        assert accepted == generated[n, layers]
        ambient_rows.append({'ambient_cities': n*layers, 'layers': layers,
                             'ambient_tours_checked': count,
                             'face_tours_found': len(accepted)})
    return rows, ambient_rows


def check_padding():
    rows = []
    for m, n in ((3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7)):
        path = (0,) + tuple(range(m, n))
        forced = {edge(path[i], path[i+1]) for i in range(len(path)-1)}
        old_tours, projected, count = set(all_tours(m)), set(), 0
        for tour in all_tours(n):
            if not forced <= tour:
                continue
            count += 1
            image = Counter({edge(i, j): 1 for i, j in tour if 0 < i < j < m})
            for j in range(1, m):
                value = int(edge(0, j) in tour) + int(edge(n-1, j) in tour)
                if value:
                    image[edge(0, j)] = value
            assert set(image.values()) == {1}
            support = frozenset(image)
            assert is_tour(m, support) and support in old_tours
            projected.add(support)
        assert projected == old_tours and count == 2*len(old_tours)
        rows.append({'old_cities': m, 'new_cities': n, 'forced_path_edges': len(forced),
                     'padding_face_tours': count, 'all_old_tours_recovered': len(old_tours)})
    return rows


def check_negative_controls():
    order = (0, 1, 2, 3, 7, 6, 5, 4)
    bad = frozenset(edge(order[i], order[(i+1) % len(order)]) for i in range(len(order)))
    forbidden = {edge(i, 4+j) for i in range(4) for j in range(4) if i != j}
    assert is_tour(8, bad) and not compressed_face(4, bad)
    assert not forbidden & bad
    assert degrees(4, project_left(4, bad)) == [1, 2, 2, 1]
    left = ((0, 1), (2, 3))
    for layers in (2, 3):
        subtour = gadget(4, left, left, layers)
        assert degrees(4*layers, subtour) == [2]*(4*layers)
        assert not is_tour(4*layers, subtour)
    return {'missing_forced_diagonal_detected': True,
            'matching_union_subtours_detected': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    pair_rows, ambient_rows = check_pairs()
    result = {'status': 'all assertions passed',
              'checked_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'finite construction checks; no exponential matching theorem checked',
              'matching_pair_checks': pair_rows,
              'ambient_complete_graph_checks': ambient_rows,
              'padding_checks': check_padding(),
              'negative_controls': check_negative_controls()}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
