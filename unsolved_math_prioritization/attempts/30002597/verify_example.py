#!/usr/bin/env python3
"""Exact audit of the published three-crossing obstruction; no proof search.

Standard library only. Run this file from any directory. It prints JSON and
asserts the hand-computable values in APPLICATION_CHECK.md. It does not prove
Turaev's topological obstruction theorem or classify arbitrary curves.
"""

import json
from collections import Counter
from fractions import Fraction


def validate(arrows):
    endpoints = [x for arrow in arrows for x in arrow]
    if sorted(endpoints) != list(range(2 * len(arrows))):
        raise ValueError("Endpoints must partition range(2 * number of arrows)")


def arc(a, b, size):
    """Interior of the positively oriented circular arc a -> b."""
    return {x for x in range(size) if 0 < (x - a) % size < (b - a) % size}


def linking_matrix(arrows):
    validate(arrows)
    size = 2 * len(arrows)
    matrix = []
    for i, (a, b) in enumerate(arrows):
        inside = arc(a, b, size)
        row = []
        for j, (c, d) in enumerate(arrows):
            row.append(0 if i == j else int(c in inside) - int(d in inside))
        matrix.append(row)
    assert all(matrix[i][j] == -matrix[j][i]
               for i in range(len(arrows)) for j in range(len(arrows)))
    return matrix


def polynomial(arrows):
    indices = list(map(sum, linking_matrix(arrows)))
    coefficients = Counter()
    for index in indices:
        if index:
            coefficients[abs(index)] += 1 if index > 0 else -1
    return indices, {k: v for k, v in sorted(coefficients.items()) if v}


def boundary_cycles(arrows):
    """Cycles of rotation composed with edge reversal in the oriented ribbon graph.

    Darts (i,+1), (i,-1) are outgoing/incoming at circle position i. At a
    crossing (tail a, head b), cyclic order is a+, b+, a-, b-.
    """
    validate(arrows)
    size = 2 * len(arrows)
    if not size:
        return [[], []]  # regular neighborhood of a simple circle is an annulus
    rotation, reverse = {}, {}
    for a, b in arrows:
        darts = [(a, 1), (b, 1), (a, -1), (b, -1)]
        rotation.update({darts[i]: darts[(i + 1) % 4] for i in range(4)})
    for i in range(size):
        x, y = (i, 1), ((i + 1) % size, -1)
        reverse[x], reverse[y] = y, x
    boundary = {d: rotation[reverse[d]] for d in rotation}
    seen, cycles = set(), []
    for start in sorted(boundary):
        if start in seen:
            continue
        d, cycle = start, []
        while d not in seen:
            cycle.append(d)
            seen.add(d)
            d = boundary[d]
        assert d == start
        cycles.append(cycle)
    assert len(seen) == 4 * len(arrows)
    return cycles


def genus(arrows):
    twice = 2 + len(arrows) - len(boundary_cycles(arrows))
    assert twice >= 0 and twice % 2 == 0
    return twice // 2


def based_matrix(arrows):
    """Second genus check, using Turaev 4.2.1; core s is first."""
    indices, _ = polynomial(arrows)
    size = 2 * len(arrows)
    matrix = [[0] * (len(arrows) + 1) for _ in range(len(arrows) + 1)]
    linking = linking_matrix(arrows)
    for i, index in enumerate(indices, 1):
        matrix[i][0], matrix[0][i] = index, -index
    for i, (a, b) in enumerate(arrows, 1):
        first = arc(a, b, size)
        for j, (c, d) in enumerate(arrows, 1):
            second = arc(c, d, size)
            dot = sum(int(t in first and h in second) -
                      int(t in second and h in first) for t, h in arrows)
            matrix[i][j] = dot + linking[i - 1][j - 1]
    assert all(matrix[i][j] == -matrix[j][i]
               for i in range(len(matrix)) for j in range(len(matrix)))
    return matrix


def rational_rank(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def partitions_singletons_pairs(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in partitions_singletons_pairs(rest):
        yield [[first]] + part
    for i, second in enumerate(rest):
        for part in partitions_singletons_pairs(rest[:i] + rest[i + 1:]):
            yield [[first, second]] + part


def audit():
    # Carter word a b c b^-1 a^-1 c^-1: negative -> positive exponents.
    arrows = [(4, 0), (3, 1), (5, 2)]
    indices, coefficients = polynomial(arrows)
    matrix = based_matrix(arrows)
    cycles = boundary_cycles(arrows)
    assert indices == [1, 1, -2]
    assert coefficients == {1: 2, 2: -1}
    assert sum(indices) == sum(k * v for k, v in coefficients.items()) == 0
    assert len(cycles) == 1 and len(cycles[0]) == 12
    assert genus(arrows) == 2
    assert matrix == [[0, -1, -1, 2], [1, 0, 0, 1],
                      [1, 0, 0, 2], [-2, -1, -2, 0]]
    assert rational_rank(matrix) == 4
    pfaffian = matrix[0][1] * matrix[2][3] - matrix[0][2] * matrix[1][3] + matrix[0][3] * matrix[1][2]
    assert pfaffian == -1
    orbit_checks = []
    for partition in partitions_singletons_pairs([0, 1, 2]):
        sums = [sum(indices[i] for i in block) for block in partition]
        assert any(sums)
        orbit_checks.append({"partition": partition, "index_sums": sums})
    assert len(orbit_checks) == 4
    # Independent reindexing checks: six basepoints, reversed surface orientation,
    # and reversed circle orientation. Nonvanishing must survive every choice.
    reindexings = 0
    for shift in range(6):
        rotated = [((a + shift) % 6, (b + shift) % 6) for a, b in arrows]
        for candidate in [rotated, [(b, a) for a, b in rotated]]:
            assert polynomial(candidate)[1] == coefficients
            assert genus(candidate) == 2
            assert rational_rank(based_matrix(candidate)) == 4
            reversed_circle = [((-a) % 6, (-b) % 6) for a, b in candidate]
            assert polynomial(reversed_circle)[1] == {k: -v for k, v in coefficients.items()}
            assert genus(reversed_circle) == 2
            reindexings += 2
    # Degenerate-size sanity checks, plus rejection of malformed encodings.
    for candidate, expected_genus in [([], 0), ([(0, 1)], 0),
                                      ([(0, 2), (1, 3)], 1),
                                      ([(0, 1), (2, 3)], 0)]:
        assert polynomial(candidate)[1] == {}
        assert genus(candidate) == expected_genus
    try:
        polynomial([(0, 1), (1, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("Malformed arrow diagram accepted")
    return {"status": "passed", "indexing": "zero-based",
            "arrows": arrows, "linking_matrix": linking_matrix(arrows),
            "indices": indices, "u_coefficients_by_degree": coefficients,
            "ribbon_boundary_cycles": cycles, "ribbon_genus": genus(arrows),
            "based_matrix_order": ["s", "a", "b", "c"], "based_matrix": matrix,
            "based_matrix_rank": rational_rank(matrix), "pfaffian": pfaffian,
            "involution_orbit_checks": orbit_checks,
            "orientation_and_basepoint_variants_checked": reindexings,
            "limitation": "Verifies the published example's combinatorics, not the topological theorem or a general classification"}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
