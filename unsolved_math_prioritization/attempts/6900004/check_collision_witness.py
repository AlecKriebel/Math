#!/usr/bin/env python3
"""Exact, read-only regression checks for the collinear collision argument.

Only the Python standard library is used. All guards survive -O and -OO.
Finite checks support the explicit formulas; they do not decide source intent.
The program reads no external mathematical data and writes only to stdout.
"""

from fractions import Fraction
from itertools import combinations
import json
import os
import sys


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def validate_graph(n, edges):
    require(type(n) is int and n >= 1, "n must be a positive integer")
    require(type(edges) is tuple, "edges must be a tuple")
    require(len(set(edges)) == len(edges), "duplicate edge")
    for edge in edges:
        require(type(edge) is tuple and len(edge) == 2, "invalid edge")
        u, v = edge
        require(type(u) is int and type(v) is int, "invalid vertex")
        require(0 <= u < v < n, "edges must be distinct ordered vertex pairs")


def scalar_positions(n, edge, t):
    require(type(t) is Fraction, "use exact Fraction parameters")
    require(Fraction(-1, 2) <= t <= Fraction(1, 2), "parameter out of range")
    u, v = edge
    return tuple(t if k == u else Fraction(0) if k == v else Fraction(k + 2)
                 for k in range(n))


def configuration(n, d, edge, t):
    require(type(d) is int and d >= 1, "d must be positive")
    scalars = scalar_positions(n, edge, t)
    # Use a non-axis direction as an additional exact check of dimension handling.
    direction = tuple(Fraction((-1 if r % 2 else 1) * (r + 1)) for r in range(d))
    return tuple(tuple(x * a for a in direction) for x in scalars)


def equilibrium_matrix(n, d, edges, points):
    validate_graph(n, edges)
    require(len(points) == n and all(len(p) == d for p in points), "point shape")
    matrix = [[Fraction(0) for _ in edges] for _ in range(n * d)]
    for c, (u, v) in enumerate(edges):
        for r in range(d):
            delta = points[v][r] - points[u][r]
            matrix[u * d + r][c] = delta
            matrix[v * d + r][c] = -delta
    return matrix


def validate_rescaling(base, moved, factors):
    require(len(base) == len(moved), "row count differs")
    require(all(len(row) == len(factors) for row in base + moved), "column count differs")
    require(all(f > 0 for f in factors), "factor must be strictly positive")
    for row0, rowt in zip(base, moved):
        for a0, at, factor in zip(row0, rowt, factors):
            require(at * factor == a0, "equilibrium matrix identity fails")


def rank(matrix):
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    ncols = len(rows[0])
    result = 0
    for column in range(ncols):
        pivot = next((i for i in range(result, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        factor = rows[result][column]
        rows[result] = [x / factor for x in rows[result]]
        for i in range(len(rows)):
            if i != result and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[result])]
        result += 1
    return result


def check_witness(n, d, containing, omitting, edge, t):
    validate_graph(n, containing)
    validate_graph(n, omitting)
    require(edge in containing and edge not in omitting, "edge must distinguish the graphs")
    require(t != 0, "comparison parameter must be nonzero")
    p0 = configuration(n, d, edge, Fraction(0))
    pt = configuration(n, d, edge, t)
    x0 = scalar_positions(n, edge, Fraction(0))
    xt = scalar_positions(n, edge, t)
    factors = []
    for u, v in omitting:
        require(xt[v] != xt[u] and x0[v] != x0[u], "omitting graph edge collapsed")
        factors.append((x0[v] - x0[u]) / (xt[v] - xt[u]))
    base = equilibrium_matrix(n, d, omitting, p0)
    moved = equilibrium_matrix(n, d, omitting, pt)
    validate_rescaling(base, moved, factors)
    # Explicit inverse map, so the check is not only kernel containment.
    validate_rescaling(moved, base, [1 / f for f in factors])
    g0 = equilibrium_matrix(n, d, containing, p0)
    gt = equilibrium_matrix(n, d, containing, pt)
    ecolumn = containing.index(edge)
    require(all(row[ecolumn] == 0 for row in g0), "singleton stress missing at collision")
    require(any(row[ecolumn] != 0 for row in gt), "singleton stress survives separation")
    return 1


def graphs(n):
    universe = tuple(combinations(range(n), 2))
    return tuple(tuple(e for k, e in enumerate(universe) if mask & (1 << k))
                 for mask in range(1 << len(universe)))


def distinguishing_orientation(g, h):
    difference = set(g) - set(h)
    if difference:
        return g, h, min(difference)
    difference = set(h) - set(g)
    require(bool(difference), "graphs are identical")
    return h, g, min(difference)


def expect_failure(operation, label):
    try:
        operation()
    except CheckFailure:
        return label
    raise CheckFailure("negative control was accepted: " + label)


def run():
    require(len(sys.argv) == 1, "no command-line arguments supported")
    parameters = (Fraction(-1, 2), Fraction(-1, 4), Fraction(1, 4), Fraction(1, 2))
    checks = 0
    pair_counts = {}
    for n in range(1, 5):
        count = 0
        for g, h in combinations(graphs(n), 2):
            containing, omitting, edge = distinguishing_orientation(g, h)
            count += 1
            for d in (1, 2, 3):
                for t in parameters:
                    checks += check_witness(n, d, containing, omitting, edge, t)
        pair_counts[str(n)] = count
    # Test all possible nonedges, not just the first symmetric-difference edge.
    nonedge_checks = 0
    for n in range(2, 5):
        complete = tuple(combinations(range(n), 2))
        for h in graphs(n):
            for edge in complete:
                if edge not in h:
                    g = tuple(sorted(h + (edge,)))
                    nonedge_checks += check_witness(n, 2, g, h, edge, Fraction(1, 4))
    large = []
    for n in (5, 8, 12):
        complete = tuple(combinations(range(n), 2))
        for edge in ((0, 1), (0, n - 1), (n - 2, n - 1)):
            dense = tuple(e for e in complete if e != edge)
            forest = tuple(e for e in ((k, k + 1) for k in range(n - 1)) if e != edge)
            disconnected = tuple(e for e in dense if e[0] // 3 == e[1] // 3)
            for name, h in (("dense", dense), ("forest", forest), ("disconnected", disconnected), ("empty", ())):
                g = tuple(sorted(set(h) | {edge}))
                for d in (1, 2, 3, 5):
                    for t in parameters:
                        checks += check_witness(n, d, g, h, edge, t)
                large.append({"n": n, "edge": list(edge), "family": name})
    triangle = ((0, 1), (0, 2), (1, 2))
    nullities = []
    for t in (Fraction(0), Fraction(1, 4)):
        matrix = equilibrium_matrix(3, 2, triangle, configuration(3, 2, (0, 1), t))
        nullities.append(len(triangle) - rank(matrix))
    require(nullities == [1, 1], "expected equal-dimension sign-change example")
    negative = [
        expect_failure(lambda: configuration(2, 0, (0, 1), Fraction(0)), "zero ambient dimension"),
        expect_failure(lambda: scalar_positions(2, (0, 1), Fraction(3, 4)), "out-of-range path"),
        expect_failure(lambda: check_witness(2, 1, ((0, 1),), ((0, 1),), (0, 1), Fraction(1, 4)), "non-distinguishing edge"),
        expect_failure(lambda: check_witness(2, 1, ((0, 1),), (), (0, 1), Fraction(0)), "zero comparison parameter"),
        expect_failure(lambda: validate_rescaling([[Fraction(2)]], [[Fraction(1)]], [Fraction(-2)]), "negative factor"),
        expect_failure(lambda: validate_rescaling([[Fraction(2)]], [[Fraction(1)]], [Fraction(3)]), "wrong factor"),
        expect_failure(lambda: validate_rescaling([[Fraction(2)]], [[Fraction(1)]], [Fraction(0)]), "singular factor"),
        expect_failure(lambda: validate_graph(2, ((0, 1), (0, 1))), "duplicate edge"),
        expect_failure(lambda: validate_graph(2, ((0, 0),)), "loop edge"),
        expect_failure(lambda: distinguishing_orientation((), ()), "identical graph pair"),
    ]
    return {
        "status": "PASS",
        "arithmetic": "fractions.Fraction; exact, no tolerance",
        "all_unordered_distinct_graph_pairs": pair_counts,
        "pair_witness_and_selected_family_checks": checks,
        "additional_each_nonedge_checks": nonedge_checks,
        "selected_larger_families": large,
        "equal_dimension_triangle_stress_nullities": nullities,
        "negative_controls_rejected": negative,
        "uid": os.getuid() if hasattr(os, "getuid") else None,
        "optimization": sys.flags.optimize,
        "scope": "Formula regression only; proof and source intent require separate review",
    }


if __name__ == "__main__":
    try:
        print(json.dumps(run(), indent=2, sort_keys=True))
    except CheckFailure as error:
        print(json.dumps({"status": "FAIL", "reason": str(error)}, sort_keys=True))
        sys.exit(1)
