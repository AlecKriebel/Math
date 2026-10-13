#!/usr/bin/env python3
"""Fresh finite LC reconstruction. No submitted imports, certificates, or assertions.

The mathematical bridge is LM 1411.6310v3, sections 2.1, 2.3, 5.3 and A.5.
This program verifies only finite hypotheses of that bridge, not the source theorems.
"""
import itertools
import json
from fractions import Fraction

SEG = {"A": (0, 2), "B": (1, 4), "C": (3, 3), "D": (2, 5), "E": (4, 6)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def precedes(u, v):
    a, b = u
    c, d = v
    return a < c <= b + 1 and b < d


def set_precedes(u, v):
    U = frozenset(range(u[0], u[1] + 1))
    V = frozenset(range(v[0], v[1] + 1))
    union = U | V
    contiguous = len(union) == max(union) - min(union) + 1
    return contiguous and not U <= V and not V <= U and min(U) < min(V)


def ladder(labels, segments=SEG):
    entries = [segments[x] for x in labels]
    return all(not (a <= c and d <= b) and not (c <= a and b <= d)
               for (a, b), (c, d) in itertools.combinations(entries, 2))


def graph(m, n, segments=SEG, relation=precedes):
    # Vertices are occurrence positions, so duplicates remain distinct.
    X = [(i, j) for i, u in enumerate(m) for j, v in enumerate(n)
         if relation(segments[u], segments[v])]
    Y = [(i, j) for i, u in enumerate(m) for j, v in enumerate(n)
         if relation(tuple(x - 1 for x in segments[u]), segments[v])]
    edges = {}
    for i1, j1 in X:
        edges[(i1, j1)] = [y for y in Y
            if (i1 == y[0] and relation(segments[n[y[1]]], segments[n[j1]]))
            or (j1 == y[1] and relation(segments[m[i1]], segments[m[y[0]]]))]
    return X, Y, edges


def hall(X, edges):
    deficiencies = []
    for size in range(1, len(X) + 1):
        for subset in itertools.combinations(X, size):
            neighbors = sorted({y for x in subset for y in edges[x]})
            if len(neighbors) < size:
                deficiencies.append((subset, neighbors))
    return deficiencies


def exhaustive_match(X, edges):
    # Exhaustive injection search, a different decision mechanism from Hall enumeration.
    def search(k, used, assigned):
        if k == len(X):
            return assigned
        for y in edges[X[k]]:
            if y not in used:
                answer = search(k + 1, used | {y}, assigned + [(X[k], y)])
                if answer is not None:
                    return answer
        return None
    return search(0, set(), [])


def encode_vertex(v, m, n):
    return {"positions": list(v), "segments": [m[v[0]], n[v[1]]]}


def direction(m, n, segments=SEG):
    X, Y, edges = graph(m, n, segments)
    require((X, Y, edges) == graph(m, n, segments, set_precedes),
            "Endpoint and discrete-set graph disagreement")
    deficits = hall(X, edges)
    matching = exhaustive_match(X, edges)
    require((matching is None) == bool(deficits), "Hall and injection disagreement")
    witnesses = [{"X_subset": [encode_vertex(x, m, n) for x in subset],
                  "Y_neighbors": [encode_vertex(y, m, n) for y in neighbors],
                  "deficiency": len(subset) - len(neighbors)}
                 for subset, neighbors in deficits]
    return {"m": list(m), "n": list(n), "LC": matching is not None,
            "X": [encode_vertex(x, m, n) for x in X],
            "Y": [encode_vertex(y, m, n) for y in Y],
            "neighbors": [{"x": encode_vertex(x, m, n),
                           "ys": [encode_vertex(y, m, n) for y in edges[x]]} for x in X],
            "matching": None if matching is None else [
                {"x": encode_vertex(x, m, n), "y": encode_vertex(y, m, n)}
                for x, y in matching],
            "minimum_Hall_obstruction": witnesses[0] if witnesses else None,
            "all_Hall_obstruction_count": len(witnesses)}


def controls():
    expected = [
        ((0, 1), (2, 3), True, "juxtaposed"),
        ((0, 1), (3, 4), False, "one-integer gap"),
        ((0, 2), (2, 4), True, "single-endpoint overlap"),
        ((0, 2), (0, 4), False, "same left endpoint containment"),
        ((0, 4), (2, 4), False, "same right endpoint containment"),
        ((0, 2), (0, 2), False, "equal"),
        ((0, 4), (1, 2), False, "strict containment"),
        ((0, 1), (1, 2), True, "overlap"),
        ((1, 2), (0, 1), False, "reverse orientation"),
    ]
    records = []
    for u, v, wanted, name in expected:
        actual = precedes(u, v)
        require(actual == wanted and set_precedes(u, v) == wanted, name)
        records.append({"control": name, "u": u, "v": v, "precedes": actual})
    intervals = [(a, b) for a in range(-3, 5) for b in range(a, 6)]
    for u in intervals:
        for v in intervals:
            require(precedes(u, v) == set_precedes(u, v), "boundary grid disagreement")
            require(precedes(u, v) == precedes((-v[1], -v[0]), (-u[1], -u[0])),
                    "contragredient precedence disagreement")
    # Positive matching controls use a larger m segment to absorb the obstruction.
    good = {"u": (0, 1), "v": (1, 2), "w": (2, 2)}
    forward = direction(("u", "v"), ("w",), good)
    reverse = direction(("w",), ("u", "v"), good)
    require(forward["LC"] and reverse["LC"], "positive nonempty matching control")
    # A segment pair is reducible exactly when linked (under the ladder interface).
    segment_controls = 0
    for u, v in itertools.product(intervals, repeat=2):
        data = {"u": u, "v": v}
        a = direction(("u",), ("v",), data)["LC"]
        b = direction(("v",), ("u",), data)["LC"]
        require((a and b) == (not (precedes(u, v) or precedes(v, u))),
                "two-singleton irreducibility control")
        segment_controls += 1
    duplicate = graph(("u", "u"), ("v",), good)
    require(len(duplicate[0]) == 2 and len(set(duplicate[0])) == 2,
            "duplicate segment occurrence collapse")
    return {"explicit_boundary_cases": records, "interval_grid_size": len(intervals),
            "ordered_pair_controls": segment_controls,
            "positive_matching": [forward, reverse],
            "duplicate_occurrence_vertices": duplicate[0]}


def run():
    control_output = controls()
    labels = tuple(SEG)
    partitions = []
    # Exactly once: every side with fewer than three entries, no complements duplicated.
    for size in (1, 2):
        for m in itertools.combinations(labels, size):
            n = tuple(x for x in labels if x not in m)
            dm, dn = direction(m, n), direction(n, m)
            ladders = [list(x) for x in (m, n) if ladder(x)]
            require(bool(ladders), "partition without ladder side")
            require(not (dm["LC"] and dn["LC"]), "induced candidate partition survived")
            require(any(d["minimum_Hall_obstruction"] is not None
                        and len(d["minimum_Hall_obstruction"]["X_subset"]) == 1
                        and len(d["minimum_Hall_obstruction"]["Y_neighbors"]) == 0
                        for d in (dm, dn)), "missing empty-neighborhood singleton")
            # All internal segment permutations preserve the named directed graph.
            for p in itertools.permutations(m):
                for q in itertools.permutations(n):
                    require(direction(p, q)["LC"] == dm["LC"], "m/n indexing dependence")
                    require(direction(q, p)["LC"] == dn["LC"], "n/m indexing dependence")
            translated = {x: (a + 11, b + 11) for x, (a, b) in SEG.items()}
            require(direction(m, n, translated)["LC"] == dm["LC"], "translation dependence")
            require(direction(n, m, translated)["LC"] == dn["LC"], "reverse translation dependence")
            dual = {x: (-b, -a) for x, (a, b) in SEG.items()}
            require(direction(n, m, dual)["LC"] == dm["LC"], "dual LC orientation")
            require(direction(m, n, dual)["LC"] == dn["LC"], "reverse dual LC orientation")
            partitions.append({"partition": [list(m), list(n)], "ladder_sides": ladders,
                               "directions": [dm, dn], "product_irreducible": False})
    require(len(partitions) == 15, "incorrect partition enumeration")
    orders = (("E", "D", "C", "B", "A"),
              ("E", "C", "D", "B", "A"),
              ("E", "D", "B", "C", "A"))
    order_checks = []
    for order in orders:
        bad = [(u, v) for i, u in enumerate(order) for v in order[i+1:]
               if precedes(SEG[u], SEG[v])]
        flo_bad = [(u, v) for i, u in enumerate(order) for v in order[i+1:]
                   if SEG[u][0] <= SEG[v][0] <= SEG[u][1] <= SEG[v][1]]
        require(not bad and not flo_bad, "bad ordered form or FLO condition")
        order_checks.append({"order": order, "LM_precedence_violations": bad,
                             "FLO_preorder_violations": flo_bad})
    exponents = [Fraction(sum(SEG[x]), 2) for x in orders[0]]
    require(all(a > b for a, b in zip(exponents, exponents[1:])), "standard exponent order")
    degree = sum(b - a + 1 for a, b in SEG.values())
    require(degree == 15, "degree")
    return {"finite_verdict": "PASS_ALL_15_PARTITIONS_HAVE_SINGLETON_HALL_OBSTRUCTION",
            "claim_scope": "finite LM combinatorics only; no analytic multiplicity claim",
            "segments": SEG, "degree": degree, "standard_real_exponents": list(map(str, exponents)),
            "order_checks": order_checks, "partitions": partitions, "hostile_controls": control_output}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
