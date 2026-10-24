#!/usr/bin/env python3
"""Finite certificates only; no claim that their data are QI invariants."""

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        row = next((r for r in range(pivot, len(a)) if a[r][col]), None)
        if row is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        scale = a[pivot][col]
        a[pivot] = [x / scale for x in a[pivot]]
        for r in range(len(a)):
            if r != pivot and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[pivot])]
        pivot += 1
    return pivot


edges = list(combinations(range(1, 5), 2))
units = {edge: [int(edge == other) for other in edges] for edge in edges}
v = [1] * 6
e02 = [int(edge in {(1, 3), (1, 4), (3, 4)}) for edge in edges]
e03 = [int(edge in {(1, 2), (1, 4), (2, 4)}) for edge in edges]
u_prime = [e02, e03, units[(2, 3)]]
assert rank([v] + u_prime) - rank([v]) == 3
for edge in [(1, 4), (2, 3)]:
    assert rank([v] + u_prime + [units[edge]]) == rank([v] + u_prime)

homology_checks = []
for triple in combinations(range(1, 5), 3):
    u_t = [units[edge] for edge in combinations(triple, 2)]
    joint_dimension = rank([v] + u_prime + u_t) - 1
    assert joint_dimension > 3
    homology_checks.append({"finite_triple": triple, "U_prime_dimension": 3,
                            "U_T_dimension": rank([v] + u_t) - 1,
                            "joint_dimension": joint_dimension,
                            "same_subspace": False})


def arm_tree(arms):
    """Vertex 0 is the unique trivalent vertex."""
    adjacency = {0: []}
    next_vertex = 1
    for length in arms:
        previous = 0
        for _ in range(length):
            node = next_vertex
            next_vertex += 1
            adjacency[node] = [previous]
            adjacency[previous].append(node)
            previous = node
    return adjacency


def deletion_components(adjacency, deleted):
    remaining = set(adjacency) - {deleted}
    components = []
    while remaining:
        start = min(remaining)
        seen, frontier = set(), [start]
        while frontier:
            node = frontier.pop()
            if node in seen or node == deleted:
                continue
            seen.add(node)
            frontier.extend(x for x in adjacency[node] if x != deleted)
        remaining -= seen
        components.append(sorted(seen))
    return sorted(components, key=lambda component: (-len(component), component))


deletion_checks = []
for n in [6, 7, 8]:
    d_graph = arm_tree([1, 1, n - 3])
    e_graph = arm_tree([1, 2, n - 4])
    spectra = {}
    for family, graph in [("D", d_graph), ("E", e_graph)]:
        entries = []
        for deleted in graph:
            components = deletion_components(graph, deleted)
            sizes = sorted((len(c) for c in components), reverse=True)
            entries.append({"deleted_vertex": deleted,
                            "component_sizes": sizes,
                            "central_Euclidean_dimension": len(components),
                            "non_Euclidean_factor_count": sum(s > 1 for s in sizes)})
        branch_entry = next(entry for entry in entries if entry["deleted_vertex"] == 0)
        assert branch_entry["central_Euclidean_dimension"] == 3
        assert branch_entry["non_Euclidean_factor_count"] == (1 if family == "D" else 2)
        assert all(entry["central_Euclidean_dimension"] <= 2
                   for entry in entries if entry["deleted_vertex"] != 0)
        spectra[family] = entries
    deletion_checks.append({"rank": n, "spectra": spectra,
                            "warning": "raw parabolic deletion data, NOT QI invariants"})

result = {
    "scope": "finite linear algebra and diagram-deletion certificates",
    "homology_edges_in_order": edges,
    "full_twist_relation": v,
    "U_prime_generators": u_prime,
    "homology_subspace_separations": homology_checks,
    "D_E_deletion_checks": deletion_checks,
    "F4_deletions": ["B3", "A2 x A1", "A2 x A1", "B3"],
    "H4_deletions": ["A3", "A2 x A1", "I2(5) x A1", "H3"],
    "not_a_resolution": True,
}

nested_pairing_checks = []
for n in range(2, 10):
    # The i-th difference is lambda_Hi - lambda_H(i+1), with 1-based i.
    matrix = [[int(i <= j) - int(i + 1 <= j)
               for j in range(1, n)] for i in range(1, n)]
    identity = [[int(i == j) for j in range(n - 1)] for i in range(n - 1)]
    assert matrix == identity
    nested_pairing_checks.append({"rank": n, "pairing_matrix": matrix,
                                  "is_identity": True})
result["nested_central_retract_pairing_checks"] = nested_pairing_checks

output = Path(__file__).with_name("CERTIFICATES.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(f"Validated all homology and D/E deletion assertions; wrote {output}.")
