#!/usr/bin/env python3
"""Fresh exact boundary audit; no package checker imports or receipts used."""
from fractions import Fraction as F
from itertools import combinations
import json


def require(value, message):
    if not value:
        raise RuntimeError(message)


def is_forest(n, edges):
    parent = list(range(n))
    def representative(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for u, v in edges:
        a, b = representative(u), representative(v)
        if a == b:
            return False
        parent[a] = b
    return True


def force_rows(n, edges, points):
    d = len(points[0])
    rows = []
    for v in range(n):
        for coordinate in range(d):
            row = []
            for a, b in edges:
                other = b if a == v else a if b == v else None
                row.append(F(0) if other is None else
                           points[other][coordinate] - points[v][coordinate])
            rows.append(row)
    return rows


def exact_rank(rows, width):
    # Forward elimination only; no package kernel routine or reference output.
    a = [list(map(F, row)) for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((r for r in range(pivot_row, len(a)) if a[r][column]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        for row in range(pivot_row + 1, len(a)):
            if a[row][column]:
                ratio = a[row][column] / a[pivot_row][column]
                a[row] = [x-ratio*y for x, y in zip(a[row], a[pivot_row])]
        pivot_row += 1
    return pivot_row


def prescribed_forest_points(n, edges, d, mask):
    adjacency = [[] for _ in range(n)]
    for c, (u, v) in enumerate(edges):
        vector = tuple(F(0) if mask & (1 << c) else
                       F((c+1)**(q+1)) * (-1 if (c+q) % 2 else 1)
                       for q in range(d))
        adjacency[u].append((v, vector))
        adjacency[v].append((u, tuple(-x for x in vector)))
    points = [None] * n
    for root in range(n):
        if points[root] is not None:
            continue
        points[root] = tuple(F(13*root+q) for q in range(d))
        todo = [root]
        while todo:
            u = todo.pop()
            for v, vector in adjacency[u]:
                if points[v] is not None:
                    continue
                points[v] = tuple(x+y for x, y in zip(points[u], vector))
                todo.append(v)
    return points


def ambient_change(points):
    a, b, c, e = points
    return [a, b, tuple(x+z-y for x, y, z in zip(a, b, c)),
            tuple(x+w-z for x, z, w in zip(a, c, e))]


def ambient_inverse(points):
    a, b, c, e = points
    return [a, b, tuple(y+z-x for x, y, z in zip(a, b, c)),
            tuple(y+z+w-2*x for x, y, z, w in zip(a, b, c, e))]


def main():
    forests = 0
    checks = 0
    graph_counts = {}
    for n in range(1, 6):
        pairs = tuple(combinations(range(n), 2))
        count = 0
        for graph_mask in range(1 << len(pairs)):
            edges = tuple(e for c, e in enumerate(pairs) if graph_mask & (1 << c))
            if not is_forest(n, edges):
                continue
            count += 1
            forests += 1
            for d in (1, 2, 4):
                for collision_mask in range(1 << len(edges)):
                    p = prescribed_forest_points(n, edges, d, collision_mask)
                    rows = force_rows(n, edges, p)
                    collapsed = [c for c, (u, v) in enumerate(edges) if p[u] == p[v]]
                    require(len(collapsed) == collision_mask.bit_count(),
                            'prescribed collapsed-edge subset differs')
                    require(all(row[c] == 0 for row in rows for c in collapsed),
                            'collapsed singleton exerts a force')
                    require(exact_rank(rows, len(edges)) == len(edges)-len(collapsed),
                            'forest has a noncollapsed stress degree of freedom')
                    checks += 1
        graph_counts[str(n)] = count

    path = ((0, 1), (1, 2), (2, 3))
    star = ((0, 1), (0, 2), (0, 3))
    ambient_checks = 0
    for d in (1, 2, 4, 7):
        for mask in range(8):
            p = prescribed_forest_points(4, path, d, mask)
            q = ambient_change(p)
            require(ambient_inverse(q) == p, 'path/star inverse failed')
            for (u, v), (a, b) in zip(path, star):
                require(tuple(y-x for x, y in zip(p[u], p[v])) ==
                        tuple(y-x for x, y in zip(q[a], q[b])),
                        'path/star corresponding edge differences differ')
            require(exact_rank(force_rows(4, path, p), 3) ==
                    exact_rank(force_rows(4, star, q), 3) == 3-mask.bit_count(),
                    'path/star forest freedom differs')
            ambient_checks += 1

    # Source's K3 pair-collision nullity is directly challenged in d=1 and d=3.
    triangle = ((0, 1), (0, 2), (1, 2))
    triangle_checks = 0
    for d in (1, 3):
        p = [tuple(F(0) for _ in range(d)), tuple(F(0) for _ in range(d)),
             tuple(F(q+1) for q in range(d))]
        rows = force_rows(3, triangle, p)
        require(exact_rank(rows, 3) == 2, 'K3 pair-collision rank differs')
        require(all(row[0] == 0 for row in rows), 'K3 singleton missing')
        triangle_checks += 1

    print(json.dumps({'status': 'PASS', 'forests_through_n5': forests,
                      'forest_counts_by_n': graph_counts,
                      'all_collapsed_edge_subset_checks': checks,
                      'dimensions_for_forest_checks': [1, 2, 4],
                      'path_star_inverse_and_difference_checks': ambient_checks,
                      'K3_pair_collision_nullity_one_checks': triangle_checks,
                      'limits': 'finite exact boundary diagnostics; universal topology is independently proved in INDEPENDENT_DERIVATION.md'}, indent=2))


if __name__ == '__main__':
    main()
