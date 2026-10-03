#!/usr/bin/env python3
"""Independent finite regression controls; not an asphericity decision procedure."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


EDGES = [(0, 1, 2), (1, 2, 4), (2, 3, 0), (3, 4, 2)]
N = 5
FROZEN_MANIFEST = "be95213c69677878ce0aa59d3e029fbbe046e11408d206be4ef400057158581e"


def trimmed(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def plus(a, b):
    return trimmed([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                    for i in range(max(len(a), len(b)))])


def times(a, b):
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trimmed(out)


def determinant(matrix):
    if not matrix:
        return (1,)
    result = ()
    for j, entry in enumerate(matrix[0]):
        minor = [[x for k, x in enumerate(row) if k != j] for row in matrix[1:]]
        term = times(entry, determinant(minor))
        result = plus(result, tuple((-1)**j * x for x in term))
    return result


def integer_det(a):
    a = [list(map(Fraction, row)) for row in a]
    value = Fraction(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            value = -value
        d = a[col][col]
        value *= d
        for i in range(col + 1, len(a)):
            q = a[i][col] / d
            for j in range(col, len(a)):
                a[i][j] -= q * a[col][j]
    assert value.denominator == 1
    return value.numerator


def word(edge):
    s, t, label = edge
    return (s + 1, label + 1, -(t + 1), -(label + 1))


def corners(words):
    # Each cyclic corner joins the incoming endpoint of a letter to the
    # outgoing endpoint of the next letter. Signed vertex names encode ends.
    return Counter(tuple(sorted((-w[i], w[(i + 1) % len(w)])))
                   for w in words for i in range(len(w)))


def monochrome(graph, sign):
    return [(abs(u) - 1, abs(v) - 1)
            for (u, v), multiplicity in graph.items()
            if u * sign > 0 and v * sign > 0 for _ in range(multiplicity)]


def cycle_rank(edges, n):
    adjacent = [set() for _ in range(n)]
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    unseen = set(range(n))
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for v in adjacent[stack.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
    return len(edges) - n + components


def ranks(words):
    graph = corners(words)
    return [cycle_rank(monochrome(graph, sign), N) for sign in (1, -1)]


def permutation_product(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    return tuple(a.index(i) for i in range(len(a)))


def ring_sum(*terms):
    out = Counter()
    for term in terms:
        out.update(term)
    return {g: n for g, n in out.items() if n}


def ring_neg(a):
    return {g: -n for g, n in a.items()}


def ring_product(a, b):
    out = Counter()
    for x, m in a.items():
        for y, n in b.items():
            out[permutation_product(x, y)] += m * n
    return {g: n for g, n in out.items() if n}


def main():
    root = Path(__file__).resolve().parent.parent
    manifest_bytes = (root / "MANIFEST.json").read_bytes()
    assert sha256(manifest_bytes).hexdigest() == FROZEN_MANIFEST
    manifest = json.loads(manifest_bytes)
    for filename, expected in manifest["files"].items():
        assert sha256((root / "artifacts" / filename).read_bytes()).hexdigest() == expected

    # Recursive Laplace determinant, independent of the supplied permutation
    # expansion. Coefficients here are dense tuples in increasing degree.
    matrix = []
    for s, t, label in EDGES:
        row = [()] * N
        row[s] = plus(row[s], (1,))
        row[t] = plus(row[t], (0, -1))
        row[label] = plus(row[label], (-1, 1))
        matrix.append(row)
    minors = []
    for root_vertex in range(N):
        minor = [[x for j, x in enumerate(row) if j != root_vertex] for row in matrix]
        d = determinant(minor)
        assert d == tuple((-1)**root_vertex * x for x in (0, 1, -1, 1))
        assert sum(d) in (-1, 1)
        assert len([x for x in d if x]) > 1  # A Laurent-ring nonunit control.
        minors.append(list(d))
    assert determinant([]) == (1,)

    # Unimodularity of every root-deleted incidence minor on all labeled
    # four-vertex trees and all orientations, using rational elimination.
    tree_controls = 0
    vertices = range(4)
    for edge_set in combinations(list(combinations(vertices, 2)), 3):
        if cycle_rank(edge_set, 4) != 0:
            continue
        for orientation in product((0, 1), repeat=3):
            incidence = []
            for (u, v), reverse in zip(edge_set, orientation):
                row = [0] * 4
                row[u], row[v] = ((-1, 1) if reverse else (1, -1))
                incidence.append(row)
            for omitted in vertices:
                minor = [[x for j, x in enumerate(row) if j != omitted] for row in incidence]
                assert abs(integer_det(minor)) == 1
                tree_controls += 1
    assert tree_controls == 512

    inversion_ranks = []
    for flags in product((0, 1), repeat=N):
        words = [tuple(-letter if flags[abs(letter)-1] else letter for letter in word(e))
                 for e in EDGES]
        reoriented = [(t, s, label) if flags[label] else (s, t, label)
                      for s, t, label in EDGES]
        assert corners(words) == corners([word(e) for e in reoriented])
        result = ranks(words)
        assert result != [0, 0]
        inversion_ranks.append({"flags_abcde": list(flags), "cycle_ranks_positive_negative": result})
    witnesses = [
        (1, [(0, 2), (0, 2)]),
        (1, [(1, 2), (2, 4), (1, 4)]),
        (1, [(0, 2), (0, 2)]),
        (1, [(2, 4), (2, 4)]),
        (-1, [(2, 4), (2, 4)]),
        (-1, [(0, 2), (0, 2)]),
        (1, [(0, 2), (2, 3), (0, 3)]),
        (1, [(2, 4), (2, 4)]),
    ]
    for (a, e, c), (sign, edges) in zip(product((0, 1), repeat=3), witnesses):
        flags = (a, 0, c, 0, e)
        words = [tuple(-letter if flags[abs(letter)-1] else letter for letter in word(edge))
                 for edge in EDGES]
        available = Counter(tuple(sorted(pair)) for pair in monochrome(corners(words), sign))
        required = Counter(tuple(sorted(pair)) for pair in edges)
        assert all(available[pair] >= count for pair, count in required.items())
        assert cycle_rank(edges, N) == 1
    successes = []
    for flags in product((0, 1), repeat=4):
        oriented = [(t, s, label) if flip else (s, t, label)
                    for (s, t, label), flip in zip(EDGES, flags)]
        if ranks([word(e) for e in oriented]) == [0, 0]:
            successes.append(list(flags))
    assert successes == [[0, 0, 1, 1], [1, 1, 0, 0]]

    # Endpoint coincidences in the abelianized Fox derivative: calculate by
    # prefix walks rather than from the predicted three-term expression.
    fox_controls = 0
    for s, t, label in product(range(N), repeat=3):
        if s == t:
            continue
        observed = [Counter() for _ in range(N)]
        exponent = 0
        for letter in word((s, t, label)):
            if letter < 0:
                exponent -= 1
            observed[abs(letter)-1][exponent] += 1 if letter > 0 else -1
            if letter > 0:
                exponent += 1
        expected = [Counter() for _ in range(N)]
        expected[s][0] += 1
        expected[t][1] -= 1
        expected[label][1] += 1
        expected[label][0] -= 1
        assert all({k: c for k, c in x.items() if c} == {k: c for k, c in y.items() if c}
                   for x, y in zip(observed, expected))
        fox_controls += 1

    # A noncommutative representation into A4 (written as permutations of
    # four points). Unlike involutive images, it detects a reversed product
    # in the left-module chain identity.
    images = [(0, 2, 3, 1), (2, 0, 1, 3), (1, 3, 2, 0),
              (3, 1, 0, 2), (0, 2, 3, 1)]
    identity = (0, 1, 2, 3)
    units = [{g: 1} for g in images]
    differences = [ring_sum(x, {identity: -1}) for x in units]
    wrong_order_detected = 0
    for s, t, label in EDGES:
        assert permutation_product(images[s], images[label]) == permutation_product(images[label], images[t])
        coefficients = [{} for _ in range(N)]
        coefficients[s] = ring_sum(coefficients[s], {identity: 1})
        coefficients[label] = ring_sum(coefficients[label], differences[s])
        coefficients[t] = ring_sum(coefficients[t], ring_neg(units[label]))
        prefix = identity
        fox = [{} for _ in range(N)]
        for letter in word((s, t, label)):
            j = abs(letter)-1
            if letter > 0:
                fox[j] = ring_sum(fox[j], {prefix: 1})
                prefix = permutation_product(prefix, images[j])
            else:
                prefix = permutation_product(prefix, inverse(images[j]))
                fox[j] = ring_sum(fox[j], {prefix: -1})
        assert prefix == identity and fox == coefficients
        assert ring_sum(*(ring_product(c, d) for c, d in zip(coefficients, differences))) == {}
        if ring_sum(*(ring_product(d, c) for c, d in zip(coefficients, differences))):
            wrong_order_detected += 1
    assert wrong_order_detected > 0
    assert permutation_product(images[0], images[2]) != permutation_product(images[2], images[0])

    # The displayed commutator identities are exact in a noncommutative
    # group ring. General augmentation-ideal membership is proved in prose.
    u, v = images[0], images[2]
    commutator = permutation_product(permutation_product(permutation_product(u, v), inverse(u)), inverse(v))
    uv_vu = ring_sum({permutation_product(u, v): 1}, {permutation_product(v, u): -1})
    assert ring_product(uv_vu, {permutation_product(inverse(u), inverse(v)): 1}) == {commutator: 1, identity: -1}
    assert ring_sum(ring_product(differences[0], differences[2]),
                    ring_neg(ring_product(differences[2], differences[0]))) == uv_vu

    intervals = [(left, right) for left in range(N) for right in range(left+1, N)
                 if (left, right) != (0, N-1)]
    assert len(intervals) == 9
    assert all(any(not left <= label <= right for _, _, label in EDGES[left:right])
               for left, right in intervals)
    assert all(label not in (s, t) for s, t, label in EDGES)
    assert all(EDGES[i][2] != EDGES[i+1][2] for i in range(3))
    assert {0, 4} <= {label for _, _, label in EDGES}

    print(json.dumps({
        "result": "PASS",
        "scope": "Independent finite controls only; no general asphericity decision.",
        "frozen_manifest_sha256": FROZEN_MANIFEST,
        "frozen_artifacts_checked": len(manifest["files"]),
        "root_minor_coefficients_in_increasing_degree": minors,
        "oriented_tree_incidence_minor_controls": tree_controls,
        "abelian_fox_triples": fox_controls,
        "generator_inversion_cases": inversion_ranks,
        "full_whitehead_graph_inversion_equalities": 32,
        "eight_case_cycle_witnesses": 8,
        "independent_orientation_successes": successes,
        "noncommutative_fox_rows": 4,
        "reversed_product_negative_controls_detected": wrong_order_detected,
        "nonabelian_representation_images_zero_based": images,
        "commutator_ring_identities": 2,
        "proper_intervals": len(intervals),
        "general_problem_status": "unresolved"
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
