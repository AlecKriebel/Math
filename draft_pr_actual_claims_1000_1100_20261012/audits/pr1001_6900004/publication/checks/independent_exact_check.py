#!/usr/bin/env python3
"""Independent finite stress-kernel regression checks for PR #1001.

This file derives equilibrium matrices from the definition. It imports no PR
checker and trusts no PR receipt. Finite checks do not prove the universal claim.
"""
from fractions import Fraction as F
from itertools import combinations
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(matrix, width):
    a = [list(map(F, row)) for row in matrix]
    pivot_columns = []
    r = 0
    for c in range(width):
        pivot = next((s for s in range(r, len(a)) if a[s][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [value / scale for value in a[r]]
        for s in range(len(a)):
            if s != r and a[s][c]:
                scale = a[s][c]
                a[s] = [x - scale*y for x, y in zip(a[s], a[r])]
        pivot_columns.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivot_columns


def kernel(matrix, width):
    reduced, pivots = rref(matrix, width)
    basis = []
    for c in range(width):
        if c in pivots:
            continue
        v = [F(0)] * width
        v[c] = F(1)
        for r, p in enumerate(pivots):
            v[p] = -reduced[r][c]
        basis.append(v)
    return basis


def equilibrium(n, edges, points):
    d = len(points[0])
    rows = [[F(0)] * len(edges) for _ in range(n*d)]
    for c, (u, v) in enumerate(edges):
        for q in range(d):
            delta = points[v][q] - points[u][q]
            rows[u*d + q][c] = delta
            rows[v*d + q][c] = -delta
    return rows


def product(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector)), F(0)) for row in matrix]


def point_path(n, missing, t, direction):
    u, v = missing
    x = [F(k+2) for k in range(n)]
    x[u], x[v] = F(t), F(0)
    return x, [tuple(s*F(a) for a in direction) for s in x]


def edge_transport(edges, x0, xt):
    factors = []
    for u, v in edges:
        delta0 = x0[v] - x0[u]
        deltat = xt[v] - xt[u]
        require(delta0 != 0 and deltat != 0, "collapsed edge in transport")
        factor = delta0 / deltat
        require(factor > 0, "transport loses coordinate sign")
        factors.append(factor)
    return factors


def check_one(n, edges, missing, directions):
    count = 0
    all_steps = (F(-1, 2), F(-1, 4), F(0), F(1, 4), F(1, 2))
    for direction in directions:
        x0, p0 = point_path(n, missing, F(0), direction)
        a0 = equilibrium(n, edges, p0)
        basis0 = kernel(a0, len(edges))
        for t in all_steps:
            xt, pt = point_path(n, missing, t, direction)
            at = equilibrium(n, edges, pt)
            factors = edge_transport(edges, x0, xt)
            scaled_at = [[value * factors[c] for c, value in enumerate(row)]
                         for row in at]
            require(scaled_at == a0, "A(t) T(t) != A(0)")
            transported = [[factor * value for factor, value in zip(factors, v)]
                           for v in basis0]
            for v in transported:
                require(all(value == 0 for value in product(at, v)),
                        "transported kernel vector violates equilibrium")
            require(len(kernel(at, len(edges))) == len(basis0),
                    "kernel dimension changes at nonedge collision")
            require(len(rref(transported, len(edges))[1]) == len(basis0),
                    "transported basis is not independent")
            inverse_scaled_a0 = [[value / factors[c] for c, value in enumerate(row)]
                                 for row in a0]
            require(inverse_scaled_a0 == at, "inverse transport fails")
            count += 1

        g_edges = edges + [missing]
        g0 = equilibrium(n, g_edges, p0)
        _, p1 = point_path(n, missing, F(1, 4), direction)
        g1 = equilibrium(n, g_edges, p1)
        singleton = [F(0)] * len(g_edges)
        singleton[-1] = F(1)
        require(all(value == 0 for value in product(g0, singleton)),
                "collapsed singleton does not satisfy equilibrium")
        require(any(value != 0 for value in product(g1, singleton)),
                "noncollapsed singleton satisfies equilibrium")
        count += 1
    return count


def main():
    graph_count = 0
    missing_edge_witnesses = 0
    exact_placement_checks = 0
    n_counts = {}
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        this_count = 0
        for mask in range(1 << len(pairs)):
            edges = [pair for c, pair in enumerate(pairs) if mask & (1 << c)]
            graph_count += 1
            for missing in pairs:
                if missing in edges:
                    continue
                # Both edge orientations are independently assembled. Reverse
                # the witness orientation too: its two labels have no hierarchy.
                for orientation in (0, 1):
                    h = edges if not orientation else [(v, u) for u, v in edges]
                    witness = missing if not orientation else missing[::-1]
                    directions = [(1,)]
                    if n <= 4:
                        directions += [(1, -2), (0, 0, 1), (2, 0, -3)]
                    exact_placement_checks += check_one(n, h, witness, directions)
                missing_edge_witnesses += 1
                this_count += 1
        n_counts[str(n)] = this_count

    # Equal dimension is not enough to distinguish the cyclic-edge witness.
    triangle = [(0, 1), (0, 2), (1, 2)]
    _, p0 = point_path(3, (0, 1), F(0), (1,))
    _, p1 = point_path(3, (0, 1), F(1, 4), (1,))
    k0 = kernel(equilibrium(3, triangle, p0), 3)
    k1 = kernel(equilibrium(3, triangle, p1), 3)
    require(len(k0) == len(k1) == 1, "triangle dimension boundary wrong")
    require(k0 == [[F(1), F(0), F(0)]], "triangle singleton kernel wrong")
    require(all(value != 0 for value in k1[0]), "triangle support failed")

    # Formula mutation: reversing the transport ratio must actually be rejected.
    h = [(0, 2), (1, 2)]
    x0, p0 = point_path(3, (0, 1), F(0), (1,))
    x1, p1 = point_path(3, (0, 1), F(1, 4), (1,))
    factors = edge_transport(h, x0, x1)
    a0, a1 = equilibrium(3, h, p0), equilibrium(3, h, p1)
    bad_matrix = [[value / factors[c] for c, value in enumerate(row)]
                  for row in a1]
    require(bad_matrix != a0, "checker did not detect inverse-ratio mutation")

    # The graph edge itself cannot be transported through its collision.
    rejected_collapse = False
    try:
        edge_transport([(0, 1)], x0, x1)
    except RuntimeError:
        rejected_collapse = True
    require(rejected_collapse, "checker failed to reject collapsed graph edge")

    # Merely removing zero preservation changes the decisive support test.
    require(len(k0) == len(k1), "dimension-only negative control invalid")
    require([value != 0 for value in k0[0]] !=
            [value != 0 for value in k1[0]],
            "coordinate-zero sensitivity control invalid")

    # K3 exactly-two-coincident vertices: direct rank/kernel arithmetic.
    require(len(k0) == 1, "K3 pair-collision stress dimension is not one")

    # Boundary control: nonisomorphic trees are ambient-linearly equivalent as
    # stratified spaces. Literal equality of subsets cannot be replaced by this.
    path_edges = [(0, 1), (1, 2), (2, 3)]
    star_edges = [(0, 1), (0, 2), (0, 3)]
    def tree_change(points):
        return [points[0], points[1],
                tuple(x+z-y for x, y, z in zip(points[0], points[1], points[2])),
                tuple(x+w-z for x, z, w in zip(points[0], points[2], points[3]))]
    forest_checks = 0
    for d in (1, 2, 3):
        # Each subset of the three edge differences is zero; others are nonzero.
        root = tuple(F(2*q-1) for q in range(d))
        for mask in range(8):
            differences = [tuple(F(0) if mask & (1 << c) else F((c+1)*(q+1))
                                 for q in range(d)) for c in range(3)]
            points = [root]
            for difference in differences:
                points.append(tuple(x+y for x, y in zip(points[-1], difference)))
            changed = tree_change(points)
            path_matrix = equilibrium(4, path_edges, points)
            star_matrix = equilibrium(4, star_edges, changed)
            kp = kernel(path_matrix, 3)
            ks = kernel(star_matrix, 3)
            require(kp == ks, "path/star ambient equivalence kernel test failed")
            require(len(kp) == mask.bit_count(), "forest collapsed-edge freedom wrong")
            forest_checks += 1

    print(json.dumps({
        "verdict": "PASS",
        "graph_counts_by_n": {str(n): 1 << (n*(n-1)//2) for n in range(1, 6)},
        "total_graphs": graph_count,
        "missing_edge_witnesses_by_n": n_counts,
        "total_missing_edge_witnesses": missing_edge_witnesses,
        "exact_transport_or_singleton_case_checks": exact_placement_checks,
        "higher_dimensions": "all graphs through n=4, d=2/3, zero and negative direction coordinates",
        "orientations": "both edge orientations and both missing-pair label orders",
        "kernel_reproduction": "independent exact RREF at every sampled endpoint/path point",
        "mutation_controls": {
            "reversed_transport_ratio": "rejected by exact matrix identity",
            "collapsed_graph_edge": "rejected",
            "dimension_only_equivalence": "shown insufficient by K3 equal-dimensional different supports",
        },
        "source_arithmetic": {"K3_exactly_two_coincident_stress_dimension": 1},
        "scope_boundary": {"nonisomorphic_path_star_ambient_equivalence_checks": forest_checks},
        "limits": "finite exact formula/kernel tests; continuous connected-component and universal claims need the written proof",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
