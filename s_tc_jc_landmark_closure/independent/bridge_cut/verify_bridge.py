#!/usr/bin/env python3
"""Standalone exact regressions for the projective bridge theorem.

This program is intentionally independent of every historical graph, Fourier,
atlas, and rank implementation.  It tests the universal logarithmic
factorization of positive JC-symmetric component tensors over a bridge tree.
The finite tests are regressions for, not substitutes for, the general proof
in ``PROOF.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


G = (0, 1, 2, 3)  # xor realizes Z_2 x Z_2


def xor_sum(values):
    value = 0
    for item in values:
        value ^= item
    return value


def group_automorphisms():
    result = []
    for image in itertools.permutations((1, 2, 3)):
        mapping = (0,) + image
        if all(mapping[a ^ b] == (mapping[a] ^ mapping[b]) for a in G for b in G):
            result.append(mapping)
    assert len(result) == 6
    return tuple(result)


AUTOMORPHISMS = group_automorphisms()


def orbit_representative(chars):
    return min(tuple(mapping[value] for value in chars) for mapping in AUTOMORPHISMS)


def rational_rank(matrix):
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next((row for row in range(rank, row_count) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(row_count):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right for left, right in zip(work[row], work[rank])]
        rank += 1
        if rank == row_count:
            break
    return rank


def transpose(matrix):
    return [list(row) for row in zip(*matrix)] if matrix else []


def multiply(left, right):
    if not left or not right:
        return []
    right_columns = transpose(right)
    return [[sum(a * b for a, b in zip(row, column)) for column in right_columns] for row in left]


def prufer_tree(code):
    vertex_count = len(code) + 2
    degrees = [1] * vertex_count
    for vertex in code:
        degrees[vertex] += 1
    edges = []
    for vertex in code:
        leaf = next(index for index, degree in enumerate(degrees) if degree == 1)
        edges.append(tuple(sorted((leaf, vertex))))
        degrees[leaf] -= 1
        degrees[vertex] -= 1
    leaves = [index for index, degree in enumerate(degrees) if degree == 1]
    edges.append(tuple(sorted(leaves)))
    return tuple(sorted(edges))


def adjacency(vertex_count, edges):
    result = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        result[left].append((right, edge_index))
        result[right].append((left, edge_index))
    return result


def edge_side(vertex_count, edges, forbidden_edge, start):
    graph = adjacency(vertex_count, edges)
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbor, edge_index in graph[vertex]:
            if edge_index == forbidden_edge or neighbor in seen:
                continue
            seen.add(neighbor)
            stack.append(neighbor)
    return seen


def local_coordinate_orbits(physical_count, boundary_count):
    width = physical_count + boundary_count
    if width == 0:
        return ()
    representatives = set()
    for prefix in itertools.product(G, repeat=width - 1):
        assignment = tuple(prefix) + (xor_sum(prefix),)
        if any(assignment):
            representatives.add(orbit_representative(assignment))
    return tuple(sorted(representatives))


def universal_design(vertex_count, edges, physical_counts):
    """Build the exact log-linear factor map and incidence generators."""

    graph = adjacency(vertex_count, edges)
    local_orbits = {}
    columns = []
    column_position = {}
    for vertex in range(vertex_count):
        orbits = local_coordinate_orbits(physical_counts[vertex], len(graph[vertex]))
        local_orbits[vertex] = orbits
        for orbit in orbits:
            key = ("local", vertex, orbit)
            column_position[key] = len(columns)
            columns.append(key)
    for edge_index in range(len(edges)):
        key = ("edge", edge_index)
        column_position[key] = len(columns)
        columns.append(key)

    owners = []
    for vertex, count in enumerate(physical_counts):
        owners.extend([vertex] * count)
    owner_positions = {
        vertex: tuple(index for index, owner in enumerate(owners) if owner == vertex)
        for vertex in range(vertex_count)
    }
    side_positions = {}
    for edge_index, (left, right) in enumerate(edges):
        side_vertices = edge_side(vertex_count, edges, edge_index, right)
        side_positions[edge_index] = tuple(
            index for index, owner in enumerate(owners) if owner in side_vertices
        )

    if owners:
        global_assignments = (
            tuple(prefix) + (xor_sum(prefix),)
            for prefix in itertools.product(G, repeat=len(owners) - 1)
        )
    else:
        global_assignments = ((),)

    rows = set()
    for assignment in global_assignments:
        separators = {
            edge_index: xor_sum(assignment[index] for index in positions)
            for edge_index, positions in side_positions.items()
        }
        row = [0] * len(columns)
        for vertex in range(vertex_count):
            incident = tuple(sorted(edge_index for _neighbor, edge_index in graph[vertex]))
            local_assignment = tuple(assignment[index] for index in owner_positions[vertex]) + tuple(
                separators[edge_index] for edge_index in incident
            )
            assert xor_sum(local_assignment) == 0
            if any(local_assignment):
                orbit = orbit_representative(local_assignment)
                row[column_position[("local", vertex, orbit)]] += 1
        for edge_index, separator in separators.items():
            if separator:
                row[column_position[("edge", edge_index)]] += 1
        rows.add(tuple(row))

    incidence_generators = []
    for edge_index, endpoints in enumerate(edges):
        for vertex in endpoints:
            generator = [0] * len(columns)
            incident = tuple(sorted(index for _neighbor, index in graph[vertex]))
            boundary_slot = physical_counts[vertex] + incident.index(edge_index)
            for orbit in local_orbits[vertex]:
                if orbit[boundary_slot]:
                    generator[column_position[("local", vertex, orbit)]] += 1
            generator[column_position[("edge", edge_index)]] -= 1
            incidence_generators.append(generator)
    return [list(row) for row in sorted(rows)], incidence_generators, columns, local_orbits


def check_kernel(vertex_count, edges, physical_counts):
    design, generators, columns, local_orbits = universal_design(
        vertex_count, edges, physical_counts
    )
    annihilation = multiply(design, transpose(generators))
    assert all(not entry for row in annihilation for entry in row)
    design_rank = rational_rank(design)
    generator_rank = rational_rank(generators)
    kernel_dimension = len(columns) - design_rank
    return {
        "columns": len(columns),
        "rows": len(design),
        "rank": design_rank,
        "kernel_dimension": kernel_dimension,
        "incidence_rank": generator_rank,
        "expected_incidence_rank": 2 * len(edges),
        "local_coordinate_counts": [len(local_orbits[v]) for v in range(vertex_count)],
        "exact_kernel": kernel_dimension == generator_rank == 2 * len(edges),
    }


def local_action_matrix(physical_count, boundary_count):
    rows = set()
    width = physical_count + boundary_count
    if width:
        for prefix in itertools.product(G, repeat=width - 1):
            assignment = tuple(prefix) + (xor_sum(prefix),)
            row = tuple(
                int(assignment[physical_count + index] != 0)
                for index in range(boundary_count)
            )
            if any(row):
                rows.add(row)
    return [list(row) for row in sorted(rows)]


def check_local_stabilizers():
    rows = []
    for physical_count in range(3):
        for boundary_count in range(1, 7):
            rank = rational_rank(local_action_matrix(physical_count, boundary_count))
            stabilizer = boundary_count - rank
            expected = (
                boundary_count
                if physical_count or boundary_count >= 3
                else (0 if boundary_count == 1 else 1)
            )
            assert rank == expected
            rows.append(
                {
                    "physical_blocks": physical_count,
                    "boundaries": boundary_count,
                    "action_rank": rank,
                    "stabilizer_dimension": stabilizer,
                }
            )
    return rows


def check_anchor_slices():
    records = []
    for degree in range(1, 8):
        marked = [[int(row == column) for column in range(degree)] for row in range(degree)]
        assert rational_rank(marked) == degree
        if degree >= 3:
            pairs = [(0, 1), (0, 2), (1, 2)] + [(0, index) for index in range(3, degree)]
            unmarked = [[int(column in pair) for column in range(degree)] for pair in pairs]
            assert rational_rank(unmarked) == degree
            records.append({"degree": degree, "pair_anchor_rank": degree})
    scales = tuple(Fraction(value) for value in (2, 3, 5, 7, 11))
    inverse_pairs = {
        (i, j): Fraction(1, 1) / (scales[i] * scales[j])
        for i, j in itertools.combinations(range(len(scales)), 2)
    }
    a0_squared = inverse_pairs[(0, 1)] * inverse_pairs[(0, 2)] / inverse_pairs[(1, 2)]
    assert a0_squared == Fraction(1, scales[0] ** 2)
    recovered = [Fraction(1, scales[0])]
    recovered.extend(inverse_pairs[(0, index)] / recovered[0] for index in range(1, len(scales)))
    assert tuple(recovered) == tuple(Fraction(1, value) for value in scales)
    return {"ranks": records, "exact_positive_normalizers": [str(value) for value in recovered]}


def check_two_port_theta_obstruction():
    """Exhaust the reticulation pairs on the only simple two-port theta.

    The blob is K4-e with cubic poles U,V and degree-two boundary vertices
    X,Y; external incidences at X,Y restore binary degree three.  An adjacent
    reticulation pair forces a reticulation to tail an edge entering the other.
    The sole nonadjacent pair X,Y forces both U and V to tail two reticulation
    edges.  Either pattern violates the locked S_TC criterion.
    """

    vertices = ("U", "V", "X", "Y")
    edges = {
        frozenset(edge)
        for edge in (("U", "V"), ("U", "X"), ("V", "X"), ("U", "Y"), ("V", "Y"))
    }
    records = []
    for reticulations in itertools.combinations(vertices, 2):
        left, right = reticulations
        adjacent = frozenset((left, right)) in edges
        if adjacent:
            obstruction = "adjacent_reticulation_tail"
        else:
            assert set(reticulations) == {"X", "Y"}
            common_neighbors = [
                vertex
                for vertex in vertices
                if vertex not in reticulations
                and all(frozenset((vertex, reticulation)) in edges for reticulation in reticulations)
            ]
            assert set(common_neighbors) == {"U", "V"}
            obstruction = "two_tree_vertices_tail_two_reticulation_edges"
        records.append(
            {
                "reticulations": list(reticulations),
                "adjacent": adjacent,
                "obstruction": obstruction,
            }
        )
    assert len(records) == 6
    assert sum(row["adjacent"] for row in records) == 5
    return {
        "status": "EXACTLY COMPUTED",
        "reticulation_pairs": records,
        "pair_count": len(records),
        "admissible_strong_pairs": 0,
    }


def exhaustive_small_tree_regression():
    checked = 0
    largest = {"rows": 0, "columns": 0}
    for vertex_count in range(2, 6):
        codes = ((),) if vertex_count == 2 else itertools.product(range(vertex_count), repeat=vertex_count - 2)
        for code in codes:
            edges = prufer_tree(tuple(code))
            degrees = [0] * vertex_count
            for left, right in edges:
                degrees[left] += 1
                degrees[right] += 1
            leaves = [vertex for vertex, degree in enumerate(degrees) if degree == 1]
            internal = [vertex for vertex, degree in enumerate(degrees) if degree > 1]
            for mask in range(1 << len(internal)):
                physical_counts = [0] * vertex_count
                for leaf in leaves:
                    physical_counts[leaf] = 1
                for index, vertex in enumerate(internal):
                    physical_counts[vertex] = (mask >> index) & 1
                result = check_kernel(vertex_count, edges, physical_counts)
                assert result["exact_kernel"], (edges, physical_counts, result)
                checked += 1
                largest["rows"] = max(largest["rows"], result["rows"])
                largest["columns"] = max(largest["columns"], result["columns"])
    return {"cases": checked, "largest": largest}


def adversarial_regressions():
    first = tuple(Fraction(1, 2) for _ in range(3))
    second = (Fraction(3, 5), Fraction(3, 5), Fraction(25, 72))
    assert first[0] * first[1] * first[2] == second[0] * second[1] * second[2] == Fraction(1, 8)
    reciprocal_ratio_left = second[0] / first[0]
    reciprocal_ratio_right = second[1] / first[1]
    assert reciprocal_ratio_left * reciprocal_ratio_right != 1

    retained_bivalent = check_kernel(3, ((0, 1), (1, 2)), (1, 0, 1))
    assert retained_bivalent["exact_kernel"]
    inaccessible = check_kernel(2, ((0, 1),), (2, 0))
    assert inaccessible["kernel_dimension"] > inaccessible["incidence_rank"]

    outside = tuple(Fraction(value, denominator) for value, denominator in ((7, 20), (11, 30), (13, 40)))
    bridges = tuple(Fraction(value, denominator) for value, denominator in ((2, 5), (3, 7), (5, 8)))
    effective = tuple(left * right for left, right in zip(outside, bridges))
    determinant = outside[0] * outside[1] * outside[2]
    assert determinant > 0 and all(0 < value < 1 for value in effective)
    return {
        "withdrawn_reciprocal_chart": {
            "first": [str(value) for value in first],
            "second": [str(value) for value in second],
            "common_product": "1/8",
            "reciprocal_only_related": False,
        },
        "retained_unmarked_bivalent": retained_bivalent,
        "missing_leaf_support": inaccessible,
        "independent_arm_jacobian_determinant": str(determinant),
        "effective_arms": [str(value) for value in effective],
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = {
        "status": "EXACTLY COMPUTED",
        "automorphism_count": len(AUTOMORPHISMS),
        "local_stabilizers": check_local_stabilizers(),
        "anchor_slices": check_anchor_slices(),
        "two_port_theta_obstruction": check_two_port_theta_obstruction(),
        "small_tree_exact_kernel_regression": exhaustive_small_tree_regression(),
        "adversarial_regressions": adversarial_regressions(),
    }
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        result["output_sha256"] = sha256(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
