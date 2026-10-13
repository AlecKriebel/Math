"""Independent finite checks for exact matching/TSP geometry and subset-flow lift.

Run with Python 3; uses only the standard library. Finite checks supplement,
and do not replace, the general proofs in agent_notes/independent_geometry.md.
"""
from itertools import combinations, permutations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield frozenset()
        return
    u = vertices[0]
    for v in vertices[1:]:
        remaining = tuple(w for w in vertices if w not in (u, v))
        for rest in matchings(remaining):
            yield rest | {edge(u, v)}


def tours(n):
    """Enumerate undirected Hamiltonian cycles exactly once, with root 0."""
    for order in permutations(range(1, n)):
        if order[0] > order[-1]:
            continue
        seq = (0,) + order
        yield frozenset(edge(seq[k], seq[(k + 1) % n]) for k in range(n))


def connected_cycle(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if any(len(neighbors) != 2 for neighbors in adj):
        return False
    reached = {0}
    pending = [0]
    while pending:
        u = pending.pop()
        for v in adj[u]:
            if v not in reached:
                reached.add(v)
                pending.append(v)
    return len(reached) == n


def canonical_bottom(top, n):
    pairs = sorted(top)
    k = len(pairs)
    return frozenset(edge(n + pairs[j][1], n + pairs[(j + 1) % k][0])
                     for j in range(k))


def check_two_layer(n):
    vertical = frozenset(edge(i, n + i) for i in range(n))
    all_matchings = list(matchings(range(n)))
    extension_counts = Counter()
    constructed = []
    for top in all_matchings:
        chosen_bottom = canonical_bottom(top, n)
        assert connected_cycle(top | vertical | chosen_bottom, 2 * n)
        constructed.append(sorted(top | vertical | chosen_bottom))
        for bottom_unshifted in all_matchings:
            bottom = frozenset(edge(n + u, n + v) for u, v in bottom_unshifted)
            if connected_cycle(top | vertical | bottom, 2 * n):
                extension_counts[top] += 1
    assert set(extension_counts) == set(all_matchings)
    # Direct all-tour enumeration is independent of matching-pair enumeration.
    brute_count = None
    if n <= 4:
        admissible = []
        for tour in tours(2 * n):
            if vertical <= tour and all((u < n) == (v < n) or v == u + n
                                        for u, v in tour):
                top = frozenset((u, v) for u, v in tour if v < n)
                assert top in all_matchings
                admissible.append(tour)
        brute_count = len(admissible)
        assert brute_count == sum(extension_counts.values())
    # The 3n subdivision checks the graph-theoretic path-gadget version too.
    # New c_i=2n+i subdivides vertical a_i b_i.
    for tour_edges in constructed:
        expanded = set(tuple(e) for e in tour_edges) - set(vertical)
        expanded |= {edge(i, 2 * n + i) for i in range(n)}
        expanded |= {edge(n + i, 2 * n + i) for i in range(n)}
        assert connected_cycle(expanded, 3 * n)
    return {"matching_n": n, "cities": 2 * n,
            "matching_count": len(all_matchings),
            "tour_count_in_face": sum(extension_counts.values()),
            "extension_counts": sorted(set(extension_counts.values())),
            "direct_all_tour_count": brute_count}


def check_padding(m):
    actual = set()
    face_count = 0
    for tour in tours(m + 1):
        if edge(0, m) not in tour:
            continue
        face_count += 1
        contracted = []
        for u, v in tour - {edge(0, m)}:
            contracted.append(edge(0 if u == m else u, 0 if v == m else v))
        assert len(set(contracted)) == m
        actual.add(frozenset(contracted))
    expected = set(tours(m))
    assert actual == expected
    return {"smaller_cities": m, "larger_cities": m + 1,
            "face_tour_count": face_count, "image_tour_count": len(actual)}


def check_path_padding(m, t):
    n = m + t
    path = [0] + list(range(m, n))
    forced = frozenset(edge(path[j], path[j + 1]) for j in range(t))
    image = set()
    face_count = 0
    for tour in tours(n):
        if not forced <= tour:
            continue
        face_count += 1
        projected = []
        for u, v in tour - forced:
            if u in (0, n - 1):
                assert 1 <= v < m
                projected.append(edge(0, v))
            elif v in (0, n - 1):
                assert 1 <= u < m
                projected.append(edge(0, u))
            else:
                assert 1 <= u < m and 1 <= v < m
                projected.append(edge(u, v))
        assert len(set(projected)) == m
        image.add(frozenset(projected))
    assert image == set(tours(m))
    return {"old_cities": m, "new_cities": t, "face_tour_count": face_count,
            "image_tour_count": len(image)}


def check_negative_controls_and_original_boundary():
    n = 4
    top = frozenset({edge(0, 1), edge(2, 3)})
    bottom = frozenset(edge(n + u, n + v) for u, v in top)
    vertical = frozenset(edge(i, n + i) for i in range(n))
    assert not connected_cycle(top | bottom | vertical, 2 * n)
    sequence = (0, 1, 2, 3, 7, 6, 5, 4)
    bad_tour = frozenset(edge(sequence[j], sequence[(j + 1) % 8]) for j in range(8))
    assert connected_cycle(bad_tour, 8)
    assert all((u < n) == (v < n) or v == u + n for u, v in bad_tour)
    assert frozenset((u, v) for u, v in bad_tour if v < n) not in set(matchings(range(n)))
    # Original 3n graph for matching n=2, by full ambient K_6 tour enumeration.
    original_allowed = frozenset({edge(0, 1), edge(2, 3), edge(0, 4),
                                  edge(2, 4), edge(1, 5), edge(3, 5)})
    original_face = [tour for tour in tours(6) if tour <= original_allowed]
    assert len(original_face) == 1
    assert frozenset((u, v) for u, v in original_face[0] if v < 2) == frozenset({(0, 1)})
    return {"disconnected_matching_pair_rejected": True,
            "missing_vertical_equalities_counterexample_confirmed": True,
            "original_six_city_boundary_face_tours": 1}


def subset_graph(n):
    q = n - 1
    states = [(mask, i) for mask in range(1, 1 << q)
              for i in range(1, n) if mask & (1 << (i - 1))]
    arcs = []
    for i in range(1, n):
        arcs.append(("s", (1 << (i - 1), i), edge(0, i)))
    for mask, i in states:
        for j in range(1, n):
            bit = 1 << (j - 1)
            if not mask & bit:
                arcs.append(((mask, i), (mask | bit, j), edge(i, j)))
    full = (1 << q) - 1
    for i in range(1, n):
        arcs.append(((full, i), "t", edge(i, 0)))
    return states, arcs


def check_flow(n):
    q = n - 1
    states, arcs = subset_graph(n)
    assert len(states) + 2 == 2 + q * (1 << (q - 1))
    assert len(arcs) == 2 * q + q * (q - 1) * (1 << (q - 2))
    arc_index = {(u, v): k for k, (u, v, label) in enumerate(arcs)}
    projected = Counter()
    samples = []
    for index, order in enumerate(permutations(range(1, n))):
        nodes = ["s"]
        mask = 0
        for i in order:
            mask |= 1 << (i - 1)
            nodes.append((mask, i))
        nodes.append("t")
        path = [arc_index[(nodes[j], nodes[j + 1])] for j in range(n)]
        labels = frozenset(arcs[k][2] for k in path)
        assert len(labels) == n
        assert connected_cycle(labels, n)
        projected[labels] += 1
        if index < 5:
            samples.append(path)
    assert set(projected) == set(tours(n))
    assert set(projected.values()) == {2}
    # Deterministic rational positive flow independently verifies equality signs.
    z = [Fraction(0) for _ in arcs]
    denominator = len(samples) * (len(samples) + 1) // 2
    for j, path in enumerate(samples, 1):
        for k in path:
            z[k] += Fraction(j, denominator)
    divergence = Counter()
    for k, (u, v, label) in enumerate(arcs):
        divergence[u] += z[k]
        divergence[v] -= z[k]
    assert divergence["s"] == 1 and divergence["t"] == -1
    assert all(divergence[state] == 0 for state in states)
    return {"cities": n, "vertices": len(states) + 2, "arcs": len(arcs),
            "oriented_path_count": sum(projected.values()),
            "tour_count": len(projected), "orientations_per_tour": 2}


def main():
    results = {"two_layer": [check_two_layer(n) for n in (2, 4, 6, 8)],
               "padding": [check_padding(m) for m in range(3, 8)],
               "path_padding": [check_path_padding(m, t) for m in range(3, 6)
                                for t in range(1, 4)],
               "negative_controls": check_negative_controls_and_original_boundary(),
               "subset_flow": [check_flow(n) for n in range(3, 9)],
               "limits": "Finite checks support the proved geometric claims only; no exponential lower bound or upstream theorem is computationally certified."}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
