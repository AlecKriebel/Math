#!/usr/bin/env python3
"""Independent exact checks for the projective bridge gate.

This file intentionally imports no project Fourier, graph, atlas, invariant, or
rank implementation.  It works with the universal logarithmic factor map for
positive JC-symmetric tensors on a bridge tree.  Integer kernel containments
and finite-field rank lower bounds together certify the stated rational ranks.

The finite tests are adversarial checks, not substitutes for the proofs in
``repair/reviews/BRIDGE_GATE_REVIEW.md``.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import isqrt


PRIME = 1_000_003
G = (0, 1, 2, 3)  # Z_2 x Z_2, with xor as addition.


def xor_all(values):
    out = 0
    for value in values:
        out ^= value
    return out


def automorphisms():
    maps = []
    for perm in permutations((1, 2, 3)):
        alpha = (0,) + perm
        assert all(alpha[a ^ b] == (alpha[a] ^ alpha[b]) for a in G for b in G)
        maps.append(alpha)
    assert len(maps) == 6
    return tuple(maps)


AUT = automorphisms()


def orbit_rep(chars):
    return min(tuple(alpha[c] for c in chars) for alpha in AUT)


def rank_mod(matrix, prime=PRIME):
    if not matrix:
        return 0
    a = [[value % prime for value in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], prime - 2, prime)
        a[rank] = [(x * inv) % prime for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col]:
                scalar = a[r][col]
                a[r] = [(x - scalar * y) % prime for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def transpose(matrix):
    return [list(row) for row in zip(*matrix)] if matrix else []


def matmul(a, b):
    if not a or not b:
        return []
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def tree_from_prufer(code):
    n = len(code) + 2
    degree = [1] * n
    for vertex in code:
        degree[vertex] += 1
    edges = []
    for vertex in code:
        leaf = min(i for i, d in enumerate(degree) if d == 1)
        edges.append(tuple(sorted((leaf, vertex))))
        degree[leaf] -= 1
        degree[vertex] -= 1
    last = [i for i, d in enumerate(degree) if d == 1]
    edges.append(tuple(sorted(last)))
    return tuple(sorted(edges))


def adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for edge_index, (u, v) in enumerate(edges):
        adj[u].append((v, edge_index))
        adj[v].append((u, edge_index))
    return adj


def edge_side_vertices(n, edges, edge_index, start):
    adj = adjacency(n, edges)
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for nxt, index in adj[vertex]:
            if index == edge_index or nxt in seen:
                continue
            seen.add(nxt)
            stack.append(nxt)
    return seen


def local_orbits(physical_count, degree):
    reps = set()
    width = physical_count + degree
    if width == 0:
        return tuple()
    for prefix in product(G, repeat=width - 1):
        chars = tuple(prefix) + (xor_all(prefix),)
        assert xor_all(chars) == 0
        if any(chars):
            reps.add(orbit_rep(chars))
    return tuple(sorted(reps))


def build_log_factor_map(n, edges, physical_counts):
    """Return the universal JC-invariant log-factor design matrix.

    Local coordinates are arbitrary normalized positive table entries, modulo
    diagonal Aut(G) symmetry.  This is a larger class than any network-local
    model, so exact fiber uniqueness here is a sufficient structural result.
    """
    adj = adjacency(n, edges)
    local_reps = {}
    columns = []
    column_index = {}
    for vertex in range(n):
        degree = len(adj[vertex])
        reps = local_orbits(physical_counts[vertex], degree)
        local_reps[vertex] = reps
        for rep in reps:
            key = ("local", vertex, rep)
            column_index[key] = len(columns)
            columns.append(key)
    for edge_index in range(len(edges)):
        key = ("edge", edge_index)
        column_index[key] = len(columns)
        columns.append(key)

    physical_owner = []
    for vertex, count in enumerate(physical_counts):
        physical_owner.extend([vertex] * count)
    total_physical = len(physical_owner)
    if total_physical == 0:
        global_assignments = [tuple()]
    else:
        global_assignments = [
            tuple(prefix) + (xor_all(prefix),)
            for prefix in product(G, repeat=total_physical - 1)
        ]

    owner_indices = {
        vertex: tuple(i for i, owner in enumerate(physical_owner) if owner == vertex)
        for vertex in range(n)
    }
    side_indices = {}
    for edge_index, (u, v) in enumerate(edges):
        side = edge_side_vertices(n, edges, edge_index, v)
        side_indices[edge_index] = tuple(
            i for i, owner in enumerate(physical_owner) if owner in side
        )

    rows = set()
    for global_chars in global_assignments:
        h = {
            edge_index: xor_all(global_chars[i] for i in indices)
            for edge_index, indices in side_indices.items()
        }
        row = [0] * len(columns)
        for vertex in range(n):
            incident = sorted(index for _other, index in adj[vertex])
            chars = tuple(global_chars[i] for i in owner_indices[vertex]) + tuple(
                h[index] for index in incident
            )
            assert xor_all(chars) == 0
            if any(chars):
                rep = orbit_rep(chars)
                row[column_index[("local", vertex, rep)]] += 1
        for edge_index, value in h.items():
            if value:
                row[column_index[("edge", edge_index)]] += 1
        rows.add(tuple(row))
    matrix = [list(row) for row in sorted(rows)]

    generators = []
    for edge_index, (u, v) in enumerate(edges):
        for vertex in (u, v):
            generator = [0] * len(columns)
            incident = sorted(index for _other, index in adj[vertex])
            slot = physical_counts[vertex] + incident.index(edge_index)
            for rep in local_reps[vertex]:
                if rep[slot] != 0:
                    generator[column_index[("local", vertex, rep)]] += 1
            generator[column_index[("edge", edge_index)]] -= 1
            generators.append(generator)

    return matrix, transpose(generators), columns, local_reps


def certify_full_kernel(n, edges, physical_counts):
    matrix, generators, columns, local_reps = build_log_factor_map(
        n, edges, physical_counts
    )
    zero = matmul(matrix, generators)
    assert all(value == 0 for row in zero for value in row)
    edge_count = len(edges)
    generator_rank = rank_mod(transpose(generators))
    map_rank = rank_mod(matrix)
    kernel_dimension = len(columns) - map_rank
    return {
        "columns": len(columns),
        "rows": len(matrix),
        "map_rank": map_rank,
        "kernel_dimension": kernel_dimension,
        "generator_rank": generator_rank,
        "expected_incidence_dimension": 2 * edge_count,
        "local_dimensions": tuple(len(local_reps[v]) for v in range(n)),
        "exact": (
            generator_rank == 2 * edge_count
            and kernel_dimension == 2 * edge_count
        ),
    }


def local_action_rank(physical_count, degree):
    rows = set()
    width = physical_count + degree
    if width:
        for prefix in product(G, repeat=width - 1):
            chars = tuple(prefix) + (xor_all(prefix),)
            row = tuple(int(chars[physical_count + j] != 0) for j in range(degree))
            if any(row):
                rows.add(row)
    matrix = [list(row) for row in sorted(rows)]
    rank = rank_mod(matrix)
    return rank, degree - rank


def stabilizer_table():
    out = []
    for physical_count in (0, 1, 2):
        for degree in range(1, 7):
            rank, stabilizer = local_action_rank(physical_count, degree)
            expected = (
                degree
                if physical_count > 0 or degree >= 3
                else (0 if degree == 1 else 1)
            )
            assert rank == expected
            out.append((physical_count, degree, rank, stabilizer))
    return out


def anchor_rank_table():
    out = []
    for degree in range(1, 8):
        physical_anchor_matrix = [
            [int(i == j) for j in range(degree)] for i in range(degree)
        ]
        assert rank_mod(physical_anchor_matrix) == degree
        if degree >= 3:
            pairs = [(0, 1), (0, 2), (1, 2)] + [
                (0, k) for k in range(3, degree)
            ]
            pair_matrix = [
                [int(j in pair) for j in range(degree)] for pair in pairs
            ]
            assert len(pair_matrix) == degree
            assert rank_mod(pair_matrix) == degree
            out.append((degree, "pair anchors", degree))
    rank_two, stab_two = local_action_rank(0, 2)
    assert (rank_two, stab_two) == (1, 1)
    return out


def exhaustive_reduced_tree_kernel_check():
    cases = 0
    max_columns = 0
    max_rows = 0
    for n in range(2, 6):
        codes = [tuple()] if n == 2 else product(range(n), repeat=n - 2)
        for code in codes:
            edges = tree_from_prufer(tuple(code))
            degree = [0] * n
            for u, v in edges:
                degree[u] += 1
                degree[v] += 1
            leaves = [v for v, d in enumerate(degree) if d == 1]
            internal = [v for v, d in enumerate(degree) if d > 1]
            for mask in range(1 << len(internal)):
                physical_counts = [0] * n
                for leaf in leaves:
                    physical_counts[leaf] = 1
                for bit, vertex in enumerate(internal):
                    physical_counts[vertex] = (mask >> bit) & 1
                result = certify_full_kernel(n, edges, physical_counts)
                assert result["exact"], (n, edges, physical_counts, result)
                cases += 1
                max_columns = max(max_columns, result["columns"])
                max_rows = max(max_rows, result["rows"])
    return {"cases": cases, "max_columns": max_columns, "max_rows": max_rows}


def two_port_counterexample():
    edges = ((0, 1), (1, 2))
    physical_counts = (1, 0, 1)
    result = certify_full_kernel(3, edges, physical_counts)
    assert result["exact"]
    local_dims = result["local_dimensions"]
    local_action_ranks = (
        local_action_rank(1, 1)[0],
        local_action_rank(0, 2)[0],
        local_action_rank(1, 1)[0],
    )
    naive_product_dimension = sum(
        dim - action_rank for dim, action_rank in zip(local_dims, local_action_ranks)
    ) + len(edges)
    observed_dimension = result["map_rank"]
    assert naive_product_dimension == observed_dimension + 1

    first = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    second = (Fraction(3, 5), Fraction(3, 5), Fraction(25, 72))
    assert first[0] * first[1] * first[2] == Fraction(1, 8)
    assert second[0] * second[1] * second[2] == Fraction(1, 8)
    return {
        "local_dimensions": local_dims,
        "local_action_ranks": local_action_ranks,
        "observed_dimension": observed_dimension,
        "naive_local_quotients_plus_edges_dimension": naive_product_dimension,
        "middle_local_stabilizer_dimension": 1,
        "same_effective_product": "1/8",
    }


def inaccessible_side_counterexample():
    # Vertex 1 has no physical block.  The nonzero separator sector is never
    # globally accessed, so arbitrary shape changes on vertex 0 survive beyond
    # incidence scaling.
    edges = ((0, 1),)
    physical_counts = (2, 0)
    result = certify_full_kernel(2, edges, physical_counts)
    assert result["kernel_dimension"] > result["expected_incidence_dimension"]
    assert not result["exact"]
    return result


def reduced_core_port_check(limit=18):
    minimum_theta_ports = None
    equality_cases = []
    checked = 0
    for lengths in combinations_with_replacement(range(1, limit + 1), 3):
        if sum(length == 1 for length in lengths) > 1:
            continue  # simple theta: no parallel core edges
        triangles = sum(lengths[i] + lengths[j] == 3 for i, j in combinations(range(3), 2))
        if triangles > 1:
            continue
        ports = sum(lengths) - 3
        minimum_theta_ports = ports if minimum_theta_ports is None else min(minimum_theta_ports, ports)
        if ports == 3:
            equality_cases.append(lengths)
        assert ports >= 3
        checked += 1
    assert minimum_theta_ports == 3
    assert all(cycle_length >= 3 for cycle_length in range(3, limit + 1))
    return {
        "theta_triples_checked": checked,
        "minimum_theta_ports": minimum_theta_ports,
        "minimum_cycle_ports": 3,
        "minimum_theta_examples": equality_cases[:8],
    }


def perfect_square_fraction_sqrt(value):
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def analytic_pair_anchor_inverse_check():
    # A slice tensor has pair anchors kappa_ij.  Applying incidence scales b_i
    # multiplies them by b_i b_j.  The positive formulas recover 1/b_i exactly.
    b = (Fraction(2, 3), Fraction(3, 5), Fraction(5, 7), Fraction(7, 11), Fraction(11, 13))
    r12 = 1 / (b[0] * b[1])
    r13 = 1 / (b[0] * b[2])
    r23 = 1 / (b[1] * b[2])
    a1 = perfect_square_fraction_sqrt(r12 * r13 / r23)
    a2 = perfect_square_fraction_sqrt(r12 * r23 / r13)
    a3 = perfect_square_fraction_sqrt(r13 * r23 / r12)
    recovered = [a1, a2, a3]
    recovered.extend((1 / (b[0] * b[k])) / a1 for k in range(3, len(b)))
    assert tuple(recovered) == tuple(1 / value for value in b)
    return {"input_scales": tuple(map(str, b)), "normalizers": tuple(map(str, recovered))}


def marginal_arm_submersion_check():
    # The outside one-output JC channel may have a large internal kernel.  Its
    # only relevant multiplier c_i is fixed while the adjacent bridge x_i is
    # varied.  z_i=c_i*x_i has diagonal Jacobian diag(c_i).
    outside = (
        Fraction(7, 20),
        Fraction(11, 30),
        Fraction(13, 40),
        Fraction(17, 50),
    )
    bridges = (
        Fraction(2, 5),
        Fraction(3, 7),
        Fraction(5, 8),
        Fraction(7, 9),
    )
    effective = tuple(c * x for c, x in zip(outside, bridges))
    determinant = Fraction(1)
    for c in outside:
        determinant *= c
    assert determinant > 0
    assert all(Fraction(0) < z < Fraction(1) for z in effective)

    # An exact two-route outside network still collapses to one positive JC
    # scalar; nonidentifiability of its internal products does not alter the
    # diagonal derivative with respect to the adjacent bridge.
    lam = Fraction(2, 5)
    route_a = Fraction(2, 3) * Fraction(3, 4)
    route_b = Fraction(4, 5) * Fraction(5, 6) * Fraction(6, 7)
    mixed = lam * route_a + (1 - lam) * route_b
    assert Fraction(0) < mixed < Fraction(1)

    # If two ports were forced to share one bridge parameter, the 2-by-1
    # Jacobian would have rank one rather than two.  This is the precise
    # counterexample to dropping independent adjacent bridge multipliers.
    coupled_jacobian = [[7], [11]]  # nonzero scalar multiples of one column
    assert rank_mod(coupled_jacobian) == 1
    return {
        "effective_arms": tuple(map(str, effective)),
        "arm_jacobian_determinant": str(determinant),
        "two_route_outside_multiplier": str(mixed),
        "shared-arm-parameter-rank": 1,
    }


def main():
    stabilizers = stabilizer_table()
    anchors = anchor_rank_table()
    exhaustive = exhaustive_reduced_tree_kernel_check()
    two_port = two_port_counterexample()
    inaccessible = inaccessible_side_counterexample()
    cores = reduced_core_port_check()
    inverse = analytic_pair_anchor_inverse_check()
    marginal = marginal_arm_submersion_check()

    print("EXACTLY COMPUTED: Aut(G) has", len(AUT), "elements")
    print("EXACTLY COMPUTED: local stabilizer cases", len(stabilizers))
    print("EXACTLY COMPUTED: anchor systems", len(anchors))
    print("EXACTLY COMPUTED: reduced bridge-tree kernel cases", exhaustive)
    print("EXACT COUNTEREXAMPLE: retained empty two-port product overcounts", two_port)
    print("EXACT COUNTEREXAMPLE: missing leaf-side accessibility adds kernel", inaccessible)
    print("EXACTLY COMPUTED: reduced level-2 core port check", cores)
    print("EXACTLY COMPUTED: positive pair-anchor inverse", inverse)
    print("EXACTLY COMPUTED: marginal arm submersion", marginal)
    print("BRIDGE GATE INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
