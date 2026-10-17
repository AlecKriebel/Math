#!/usr/bin/env python3
"""Deterministic, exact finite controls for Sections 4--6 and 8.

Uses only Python's standard library. No sampling or floating point arithmetic.
The weighted hypercube transform minimizes over every simple repair graph,
including repairs adding edges, deleting apex edges, and isolating vertices.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent


def pair_list(n):
    return list(combinations(range(n), 2))


def adjacency(n, mask):
    a = [set() for _ in range(n)]
    for i, (u, v) in enumerate(pair_list(n)):
        if (mask >> i) & 1:
            a[u].add(v)
            a[v].add(u)
    return a


def colorable(a, removed=frozenset(), colors=3):
    vertices = set(range(len(a))) - set(removed)
    assignment = {}

    def visit():
        if len(assignment) == len(vertices):
            return True
        v = max(vertices - assignment.keys(),
                key=lambda x: (len({assignment[u] for u in a[x] if u in assignment}),
                               len(a[x] & vertices), -x))
        forbidden = {assignment[u] for u in a[v] if u in assignment}
        # Color symmetry: use no color beyond one past the largest used color.
        for c in range(min(colors, max(assignment.values(), default=-1) + 2)):
            if c not in forbidden:
                assignment[v] = c
                if visit():
                    return True
                del assignment[v]
        return False

    return visit()


def triangle_free(a):
    return not any(a[u] & a[v] for u in range(len(a)) for v in a[u] if u < v)


def has_k4(a):
    return any(all(v in a[u] for u, v in combinations(q, 2))
               for q in combinations(range(len(a)), 4))


def in_property(a):
    return not has_k4(a) and any(colorable(a, {v}) for v in range(len(a)))


def distance_transform(good, weights):
    """Exact minimum sum of coordinate weights to a good Boolean vector.

    After processing coordinate i, all possible flips of coordinates 0..i
    have been minimized; independent coordinates yield the full cube minimum.
    """
    infinity = sum(weights) + 1
    dist = [0 if yes else infinity for yes in good]
    for i, weight in enumerate(weights):
        bit = 1 << i
        for low in range(len(dist)):
            if not low & bit:
                high = low | bit
                x, y = dist[low], dist[high]
                dist[low] = min(x, y + weight)
                dist[high] = min(y, x + weight)
    return dist


def all_small_distances():
    rows = []
    for n in range(1, 6):
        ps = pair_list(n)
        graphs = [adjacency(n, m) for m in range(1 << len(ps))]
        triangle_distance = distance_transform([triangle_free(a) for a in graphs],
                                               [1] * len(ps))
        joined_pairs = pair_list(n + 1)
        property_members = [in_property(adjacency(n + 1, m))
                            for m in range(1 << len(joined_pairs))]
        # Integer unit = 1/(4*n*n); apex coordinate has cost n units.
        joined_distance = distance_transform(property_members,
                                              [n if v == n else 1
                                               for u, v in joined_pairs])
        checked, positive = 0, 0
        for mask, a in enumerate(graphs):
            if not colorable(a):
                continue
            joined = sum(1 << i for i, (u, v) in enumerate(joined_pairs)
                         if v == n or v in a[u])
            assert joined_distance[joined] == triangle_distance[mask]
            checked += 1
            positive += triangle_distance[mask] > 0
        rows.append(dict(tail_vertices=n, tail_graphs_checked=checked,
                         positive_distance_tails=positive,
                         repair_graphs_per_tail=1 << len(joined_pairs),
                         mismatches=0))
    return rows


def encode(v, B):
    return 1 + sum(x * (2 * B) ** i for i, x in enumerate(v))


def sphere(B, d):
    buckets = defaultdict(list)
    for v in product(range(B), repeat=d):
        buckets[sum(x * x for x in v)].append(v)
    # Deterministic tie breaking: smallest norm, then tuple enumeration order.
    norm = min(buckets, key=lambda r: (-len(buckets[r]), r))
    return norm, buckets[norm]


def is_ap_free(A):
    aset = set(A)
    return all((a + b) % 2 or (a + b) // 2 not in aset or a == b
               for a in A for b in A)


def host(m, A, xs=None):
    xs = range(1, m + 1) if xs is None else xs
    designated = set()
    edges = set()
    counts = Counter()
    for x in xs:
        for t in A:
            triangle = ((0, x), (1, x + t), (2, x + 2 * t))
            designated.add(triangle)
            for e in combinations(triangle, 2):
                edges.add(e)
                counts[e] += 1
    a = defaultdict(set)
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    triangles = set()
    for u in sorted(v for v in a if v[0] == 0):
        for v in sorted(w for w in a[u] if w[0] == 1):
            for w in a[u] & a[v]:
                if w[0] == 2:
                    triangles.add((u, v, w))
    return designated, triangles, edges, max(counts.values(), default=0)


def construction_controls():
    d, B = 4, 16
    m = (2 * B) ** d
    K = (2 ** (d * d - 2 * d)) // d
    norm, vectors = sphere(B, d)
    A = [encode(v, B) for v in vectors[:K]]
    assert len(A) == K and is_ap_free(A)
    assert len(vectors) * d * B * B >= B ** d
    assert min(A) >= 1 and max(A) <= m
    A_text = "\n".join(map(str, A)) + "\n"
    (OUT / "actual_d4_A.txt").write_text(A_text)
    D, T, E, multiplicity = host(m, A, range(1, 24))
    assert D == T and multiplicity == 1 and len(E) == 3 * len(D)
    small_B, small_d = 2, 3
    small_m = (2 * small_B) ** small_d
    small_norm, small_vectors = sphere(small_B, small_d)
    small_A = [encode(v, small_B) for v in small_vectors]
    assert is_ap_free(small_A)
    Ds, Ts, Es, mults = host(small_m, small_A)
    assert Ds == Ts and mults == 1 and len(Es) == 3 * len(Ds)
    # Deliberately violate the AP-free assumption. The attack must succeed.
    Da, Ta, Ea, multa = host(8, [1, 2, 3])
    assert Ta - Da
    return dict(actual_d4=dict(B=B, d=d, m=m, K=K, sphere_norm=norm,
                             sphere_size=len(vectors),
                             A_sha256=hashlib.sha256(A_text.encode()).hexdigest(),
                             sparse_x_count=23, triangles_checked=len(T),
                             extra_triangles=0, edge_multiplicity=multiplicity),
                complete_small_host=dict(B=small_B, d=small_d, m=small_m,
                                        A=small_A, sphere_norm=small_norm,
                                        designated=len(Ds), triangles=len(Ts),
                                        edges=len(Es), edge_multiplicity=mults),
                non_ap_free_attack=dict(A=[1, 2, 3], m=8,
                                        designated=len(Da), triangles=len(Ta),
                                        extra_example=min(Ta - Da)))


def distribution_controls():
    good = [0, 3, 5, 6]
    bad = [7, 4, 2, 1]
    projection_checks = 0
    for count in range(3):
        for coordinates in combinations(range(3), count):
            def projection(patterns):
                return Counter(tuple((p >> i) & 1 for i in coordinates)
                               for p in patterns)
            assert projection(good) == projection(bad)
            projection_checks += 1
    assert Counter(good) != Counter(bad)
    # Exhaust all 4^2 choices for two disjoint triangles: full-pattern counts.
    for patterns in product(bad, repeat=2):
        complete = sum(p == 7 for p in patterns)
        # Each isolated triangle costs one edge to destroy; no sharing.
        tail = [set() for _ in range(6)]
        for j, p in enumerate(patterns):
            for i, (u, v) in enumerate(combinations(range(3 * j, 3 * j + 3), 2)):
                if p >> i & 1:
                    tail[u].add(v)
                    tail[v].add(u)
        assert sum(all(v in tail[u] for u, v in combinations(q, 2))
                   for q in combinations(range(6), 3)) == complete
    # Exact binomial probability for all small T; compare with rational
    # bound (32/33)^T >= exp(-T/32) is only a control, not the proof.
    probabilities = []
    for T in range(1, 65):
        numerator = sum(comb(T, z) * 3 ** (T - z)
                        for z in range(T + 1) if 8 * z < T)
        p = Fraction(numerator, 4 ** T)
        assert p <= Fraction(32, 33) ** T
        if T in (1, 2, 8, 16, 32, 64):
            probabilities.append(dict(T=T, exact_failure=str(p)))
    return dict(projection_checks=projection_checks,
                full_three_coordinate_distributions_differ=True,
                bad_two_triangle_patterns_checked=16,
                exact_small_T_failure_probabilities=probabilities)


def doubled_wheel_controls():
    W = [set() for _ in range(6)]
    for i in range(1, 6):
        W[0].add(i)
        W[i].add(0)
        j = 1 + i % 5
        W[i].add(j)
        W[j].add(i)
    assert in_property(W) and not colorable(W) and not has_k4(W)
    results = Counter()
    for internal in range(64):
        a = [set() for _ in range(12)]
        for u, v in combinations(range(12), 2):
            c, d = u // 2, v // 2
            if (c != d and d in W[c]) or (c == d and internal >> c & 1):
                a[u].add(v)
                a[v].add(u)
        assert not in_property(a)
        if internal:
            assert has_k4(a)
            results["internal_edge_has_K4"] += 1
        else:
            assert not has_k4(a)
            assert all(not colorable(a, {v}) for v in range(12))
            results["independent_classes_not_A3"] += 1
    return dict(W_vertices=6, W_in_P=True, W_not_3colorable=True,
                all_64_internal_assignments_outside_P=True,
                classifications=dict(results))


def assumptions_attacks():
    # Triangle-free 4-chromatic Grötzsch graph = Mycielski(C5).
    a = [set() for _ in range(11)]
    def edge(u, v):
        a[u].add(v)
        a[v].add(u)
    for i in range(5):
        j = (i + 1) % 5
        edge(i, j)
        edge(i + 5, j)
        edge(j + 5, i)
        edge(i + 5, 10)
    assert triangle_free(a) and not colorable(a)
    joined = [set(neighbors) | {11} for neighbors in a] + [set(range(11))]
    assert not has_k4(joined) and not in_property(joined)
    # If the apex is too light, deleting one apex edge is cheaper than
    # every tail triangle repair. Full 4-vertex repair-space minimum.
    weights = [9 if v < 3 else 3 for u, v in pair_list(4)]
    dist = distance_transform([in_property(adjacency(4, mask)) for mask in range(64)],
                              weights)
    assert dist[63] == 3
    return dict(non_3colorable_tail=dict(vertices=11, triangle_free=True,
                                       apex_join_in_P=False,
                                       disproves_identity_without_tail_assumption=True),
                light_apex=dict(root_mass="1/10", tail_each="3/10",
                                exact_join_distance="3/100",
                                tail_only_distance="9/100"))


def parameter_controls():
    rows = []
    for d in range(4, 65):
        m = 2 ** (d * (d + 1))
        K = (2 ** (d * d - 2 * d)) // d
        eps = Fraction(K, 1152 * m)
        low = Fraction(1, 2304 * d * 2 ** (3 * d))
        high = Fraction(1, 1152 * d * 2 ** (3 * d))
        assert 0 < low <= eps <= high
        T = m * K
        n = 6 * m
        assert eps == Fraction(T, 32 * n * n)
        assert Fraction(n ** 3, 96 * T) >= m
        assert T >= 128  # implies T >= 32*log(4), since log(4)<4.
        if d in (4, 5, 6, 8, 16, 32, 64):
            rows.append(dict(d=d, m=str(m), K=str(K), epsilon=str(eps)))
    # All d>=4 analytically: log(1/eps)<=12*d*log(2), so the lower
    # exponent can use c=1/(432*log(2)). The report proves this inequality.
    return dict(integer_d_checked="4..64", selected=rows)


def main():
    results = dict(distance_identities=all_small_distances(),
                   constructions=construction_controls(),
                   distributions=distribution_controls(),
                   doubled_wheel=doubled_wheel_controls(),
                   assumptions_attacks=assumptions_attacks(),
                   parameter_controls=parameter_controls())
    results["all_assertions_passed"] = True
    (OUT / "RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
