"""Exact verifier for the JC root path-reversal move Omega.

The move relates two triangle-free, nonisomorphic semi-directed topologies at
the globally suppressed root.  A rational nine-variable correspondence gives
a full-dimensional regular stochastic overlap.  Restoring an incoming cut
edge destroys the ambiguity: a quartet invariant is identically zero on one
lift and strictly positive on the other throughout the open JC cube.
"""

from __future__ import annotations

from collections import defaultdict
from functools import reduce
from itertools import permutations, product
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from enumerate_four_leaf_root_theta import (
    canonical_code,
    enumerate_networks,
    valid_binary_strong,
)
from fourier_models import zero_sum_assignments
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_four_network_class import colored_graph_isomorphisms, semi_directed_graph


SOURCE_LABELS = (1, 2, 3, 4)
TARGET_LABELS = (2, 1, 4, 3)
CANDIDATES = {
    "N16_source": (16, SOURCE_LABELS),
    "N16_target": (16, TARGET_LABELS),
    "N26_source": (26, SOURCE_LABELS),
    "N26_target": (26, TARGET_LABELS),
}
GAUGE_COLUMNS = (0, 1, 2, 3, 4, 7, 8, 9, 10)
RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 9)
N26_RANK_COLUMNS = (0, 1, 2, 3, 5, 7, 8, 9, 10)


def model(network, labels, prefix, assignments=zero_sum_assignments()):
    edges = tuple(tuple(edge) for edge in network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    edge_parameters = sp.symbols(f"{prefix}e0:{len(edges)}")
    inheritance_parameters = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], labels)),
        assignments,
        edge_parameters,
        dict(zip(reticulations, inheritance_parameters)),
    )
    return {
        "network": network,
        "labels": labels,
        "edges": edges,
        "reticulations": reticulations,
        "edge_parameters": edge_parameters,
        "inheritance_parameters": inheritance_parameters,
        "parameters": edge_parameters + inheritance_parameters,
        "coordinates": coordinates,
    }


def root_suppressed_underlying(network, labels):
    leaf_labels = dict(zip(network["leaves"], labels))
    root = next(vertex for vertex, color in network["vertices"].items() if color == "S")
    colors = {
        vertex: (f"L{leaf_labels[vertex]}" if color == "L" else "I")
        for vertex, color in network["vertices"].items()
        if vertex != root
    }
    root_children = []
    edges = []
    for tail, head in (tuple(edge) for edge in network["edges"]):
        if tail == root:
            root_children.append(head)
        else:
            edges.append(tuple(sorted((tail, head))))
    assert len(root_children) == 2
    edges.append(tuple(sorted(root_children)))
    return colors, tuple(sorted(edges))


def colored_underlying_isomorphisms(first, second):
    first_colors, first_edges = first
    second_colors, second_edges = second
    first_groups = defaultdict(list)
    second_groups = defaultdict(list)
    for vertex, color in first_colors.items():
        first_groups[color].append(vertex)
    for vertex, color in second_colors.items():
        second_groups[color].append(vertex)
    if {key: len(value) for key, value in first_groups.items()} != {
        key: len(value) for key, value in second_groups.items()
    }:
        return ()
    keys = sorted(first_groups)
    answers = []
    for choices in product(*(permutations(second_groups[key]) for key in keys)):
        mapping = {
            old: new
            for key, choice in zip(keys, choices)
            for old, new in zip(first_groups[key], choice)
        }
        transported = tuple(
            sorted(tuple(sorted((mapping[left], mapping[right]))) for left, right in first_edges)
        )
        if transported == second_edges:
            answers.append(mapping)
    return tuple(answers)


def verify_root_graphs(networks):
    rooted_codes = []
    semi_directed = {}
    suppressed_cycle_lengths = {}
    for name, (index, labels) in CANDIDATES.items():
        network = networks[index]
        rooted_codes.append(
            canonical_code(
                network["vertices"],
                tuple(tuple(edge) for edge in network["edges"]),
                dict(zip(network["leaves"], labels)),
            )
        )
        semi_directed[name] = semi_directed_graph(network, labels)
        assert network["triangle_count_after_root_suppression"] == 0
        colors, edges = root_suppressed_underlying(network, labels)
        vertex_types = {
            vertex: ("L" if color.startswith("L") else "T")
            for vertex, color in colors.items()
        }
        suppressed_cycle_lengths[name] = internal_cycle_lengths(vertex_types, edges)
        assert suppressed_cycle_lengths[name] == [4, 4, 6]
    assert len(set(rooted_codes)) == 4

    equivalent = set()
    for first in CANDIDATES:
        for second in CANDIDATES:
            if colored_graph_isomorphisms(semi_directed[first], semi_directed[second]):
                equivalent.add((first, second))
    expected = {
        (first, second)
        for block in (("N16_source", "N26_source"), ("N16_target", "N26_target"))
        for first in block
        for second in block
    }
    assert equivalent == expected

    source = networks[16]
    underlying_maps = colored_underlying_isomorphisms(
        root_suppressed_underlying(source, SOURCE_LABELS),
        root_suppressed_underlying(source, TARGET_LABELS),
    )
    assert len(underlying_maps) == 1
    mapping = underlying_maps[0]
    source_reticulations = {
        vertex for vertex, color in source["vertices"].items() if color in {"R", "X"}
    }
    mapped_reticulations = {mapping[vertex] for vertex in source_reticulations}
    target_reticulations = source_reticulations
    assert mapped_reticulations != target_reticulations
    assert not mapped_reticulations & target_reticulations
    return {
        "rooted_isomorphism_classes": 4,
        "semi_directed_classes": [
            ["N16_source", "N26_source"],
            ["N16_target", "N26_target"],
        ],
        "triangle_count_after_root_suppression": 0,
        "root_suppressed_blob_cycle_lengths": [4, 4, 6],
        "underlying_reflection_isomorphism_count": 1,
        "source_reticulations": sorted(source_reticulations),
        "reflected_source_reticulations": sorted(mapped_reticulations),
        "target_reticulations": sorted(target_reticulations),
        "triangle_equivalent": False,
    }


def gauge_fixed(model_data):
    edges = model_data["edge_parameters"]
    inheritances = model_data["inheritance_parameters"]
    return {
        edges[5]: sp.Rational(1, 2),
        edges[6]: sp.Rational(1, 2),
        edges[11]: sp.Rational(1, 2),
        inheritances[0]: sp.Rational(1, 2),
        inheritances[1]: sp.Rational(1, 2),
    }


def omega_substitutions(source, target):
    ae = source["edge_parameters"]
    be = target["edge_parameters"]
    bl = target["inheritance_parameters"]
    A, B, C, D, E, F, P, Q, R = (
        ae[0],
        ae[1],
        ae[2],
        ae[3],
        ae[4],
        ae[7],
        ae[8],
        ae[9],
        ae[10],
    )
    G = E + 2 * F
    H = A * F + 2 * E
    target_substitution = {
        be[0]: 2 * F * (4 - A) / G,
        be[1]: D / (4 - A),
        be[2]: C,
        be[3]: 2 * B * H / G,
        be[4]: 4 * E * R * (4 - A) / H,
        be[5]: sp.Rational(1, 2),
        be[6]: sp.Rational(1, 2),
        be[7]: 2 * A * R * G / H,
        be[8]: Q,
        be[9]: P,
        be[10]: G / 8,
        be[11]: sp.Rational(1, 2),
        bl[0]: sp.Rational(1, 2),
        bl[1]: sp.Rational(1, 2),
    }
    return G, H, gauge_fixed(source), target_substitution


def verify_omega_map(networks):
    source = model(networks[16], SOURCE_LABELS, "mapA_")
    target = model(networks[16], TARGET_LABELS, "mapB_")
    G, H, source_substitution, target_substitution = omega_substitutions(source, target)
    differences = tuple(
        sp.factor(left.subs(source_substitution) - right.subs(target_substitution))
        for left, right in zip(source["coordinates"], target["coordinates"])
    )
    assert all(difference == 0 for difference in differences)
    return {
        "zero_sum_coordinates_checked": len(differences),
        "denominators": [str(G), str(H), str(4 - source["edge_parameters"][0])],
        "source_constraints": {
            "edge_5": "1/2",
            "edge_6": "1/2",
            "edge_11": "1/2",
            "both_inheritance_probabilities": "1/2",
        },
    }


def relocation_substitution(source, target):
    x = source["edge_parameters"]
    inheritance = source["inheritance_parameters"]
    y = target["edge_parameters"]
    target_inheritance = target["inheritance_parameters"]
    return {
        y[0]: x[1],
        y[1]: x[2],
        y[2]: x[3],
        y[3]: (1 + x[0]) / 2,
        y[4]: 2 * x[0] / (1 + x[0]),
        y[5]: x[4] * x[5],
        y[6]: x[6],
        y[7]: x[7],
        y[8]: x[8],
        y[9]: x[9],
        y[10]: x[10],
        y[11]: x[11],
        target_inheritance[0]: 1 - inheritance[0],
        target_inheritance[1]: inheritance[1],
    }


def verify_root_relocation(networks):
    checks = {}
    for side, labels in (("source", SOURCE_LABELS), ("target", TARGET_LABELS)):
        first = model(networks[16], labels, f"rel16{side}_")
        second = model(networks[26], labels, f"rel26{side}_")
        substitution = relocation_substitution(first, second)
        differences = tuple(
            sp.factor(left - right.subs(substitution))
            for left, right in zip(first["coordinates"], second["coordinates"])
        )
        assert all(difference == 0 for difference in differences)
        checks[side] = len(differences)
    return {
        "symbolic_zero_sum_coordinate_checks": checks,
        "root_edge_split": ["(1+x0)/2", "2*x0/(1+x0)"],
        "complete_open_stochastic_images_equal_within_each_semi_directed_class": True,
    }


def exact_points():
    half = sp.Rational(1, 2)
    source_16 = (
        half,
        sp.Rational(1, 4),
        half,
        half,
        half,
        half,
        half,
        sp.Rational(1, 20),
        half,
        half,
        sp.Rational(1, 10),
        half,
        half,
        half,
    )
    target_16 = (
        sp.Rational(7, 12),
        sp.Rational(1, 7),
        half,
        sp.Rational(41, 48),
        sp.Rational(28, 41),
        half,
        half,
        sp.Rational(12, 205),
        half,
        half,
        sp.Rational(3, 40),
        half,
        half,
        half,
    )
    source_26 = (
        sp.Rational(1, 4),
        half,
        half,
        sp.Rational(3, 4),
        sp.Rational(2, 3),
        sp.Rational(1, 4),
        half,
        sp.Rational(1, 20),
        half,
        half,
        sp.Rational(1, 10),
        half,
        half,
        half,
    )
    target_26 = (
        sp.Rational(1, 7),
        half,
        sp.Rational(41, 48),
        sp.Rational(19, 24),
        sp.Rational(14, 19),
        sp.Rational(14, 41),
        half,
        sp.Rational(12, 205),
        half,
        half,
        sp.Rational(3, 40),
        half,
        half,
        half,
    )
    return {
        "N16_source": source_16,
        "N16_target": target_16,
        "N26_source": source_26,
        "N26_target": target_26,
    }


def gauge_determinant(model_data):
    fixed = gauge_fixed(model_data)
    outputs = [model_data["coordinates"][row + 1].subs(fixed) for row in RANK_ROWS]
    parameters = [model_data["parameters"][column] for column in GAUGE_COLUMNS]
    return sp.factor(sp.Matrix(outputs).jacobian(parameters).det(method="domain-ge"))


def verify_dimension_and_ranks(networks):
    source = model(networks[16], SOURCE_LABELS, "dimA_", JC_REPRESENTATIVES)
    target = model(networks[16], TARGET_LABELS, "dimB_", JC_REPRESENTATIVES)

    # Remove the four pendant multipliers.  Exact polynomial-matrix reduction
    # gives core rank six.
    pendant_indices = (8, 9, 10, 11)
    core_parameters = source["edge_parameters"][:8] + source["inheritance_parameters"]
    pendant_one = {source["edge_parameters"][index]: 1 for index in pendant_indices}
    core_coordinates = tuple(coordinate.subs(pendant_one) for coordinate in source["coordinates"][1:])
    core_jacobian = sp.Matrix(core_coordinates).jacobian(core_parameters)
    assert DomainMatrix.from_Matrix(core_jacobian).rank() == 6

    # The leaf-4 pendant scaling direction is already a core tangent:
    # x4*d/dx4 + x7*d/dx7 is the leaf-4 support Euler operator.
    x = source["edge_parameters"]
    for assignment, coordinate in zip(JC_REPRESENTATIVES[1:], core_coordinates):
        identity = sp.factor(
            x[4] * sp.diff(coordinate, x[4])
            + x[7] * sp.diff(coordinate, x[7])
            - int(assignment[3] != 0) * coordinate
        )
        assert identity == 0

    # Core rank <= 6, four pendant torus directions, and the displayed Euler
    # dependence imply complete rank <= 9.  A nonzero gauge minor gives >= 9.
    source_determinant = gauge_determinant(source)
    target_determinant = gauge_determinant(target)

    points = exact_points()
    minors = {}
    common_coordinates = None
    for name, (index, labels) in CANDIDATES.items():
        data = model(networks[index], labels, f"point{name}_", JC_REPRESENTATIVES)
        substitution = dict(zip(data["parameters"], points[name]))
        assert all(0 < value < 1 for value in substitution.values())
        values = tuple(sp.factor(coordinate.subs(substitution)) for coordinate in data["coordinates"])
        if common_coordinates is None:
            common_coordinates = values
        else:
            assert values == common_coordinates
        columns = GAUGE_COLUMNS if index == 16 else N26_RANK_COLUMNS
        jacobian = sp.Matrix(data["coordinates"][1:]).jacobian(data["parameters"])
        determinant = sp.factor(jacobian.subs(substitution).extract(RANK_ROWS, columns).det())
        assert determinant != 0
        minors[name] = str(determinant)

    assert minors == {
        "N16_source": "-171/2305843009213693952000000",
        "N16_target": "-513/9223372036854775808000000",
        "N26_source": "57/576460752303423488000000",
        "N26_target": "189/2305843009213693952000000",
    }
    return {
        "core_symbolic_jacobian_rank": 6,
        "complete_model_dimension": 9,
        "pendant_core_euler_identity_count": len(core_coordinates),
        "source_gauge_determinant": str(source_determinant),
        "target_gauge_determinant": str(target_determinant),
        "common_point_zero_sum_orbit_coordinates_checked": len(common_coordinates),
        "rank_nine_minors": minors,
        "exact_points": {
            name: [str(value) for value in values] for name, values in points.items()
        },
    }


def normalized_cycle(cycle):
    images = []
    for sequence in (cycle, tuple(reversed(cycle))):
        for offset in range(len(sequence)):
            images.append(sequence[offset:] + sequence[:offset])
    return min(images)


def internal_cycle_lengths(vertices, edges):
    adjacency = defaultdict(set)
    for tail, head in edges:
        if vertices[tail] != "L" and vertices[head] != "L":
            adjacency[tail].add(head)
            adjacency[head].add(tail)
    cycles = set()

    def visit(start, path):
        for neighbour in adjacency[path[-1]]:
            if neighbour == start and len(path) >= 3:
                cycles.add(normalized_cycle(tuple(path)))
            elif neighbour not in path and neighbour >= start:
                visit(start, path + [neighbour])

    for start in sorted(adjacency):
        visit(start, [start])
    return sorted(map(len, cycles))


def augmented_model(network, labels, prefix):
    vertices = dict(network["vertices"])
    vertices["S"] = "T"
    vertices["RHO"] = "S"
    vertices["LIN"] = "L"
    edges = tuple(tuple(edge) for edge in network["edges"]) + (
        ("RHO", "S"),
        ("RHO", "LIN"),
    )
    leaves = tuple(network["leaves"]) + ("LIN",)
    data = {
        "vertices": vertices,
        "edges": [list(edge) for edge in edges],
        "leaves": list(leaves),
    }
    # The generic model constructor indexes characters by the numerical leaf
    # labels.  Extend the four-leaf orbit representatives by character zero at
    # the incoming outgroup; the quartet invariant below is evaluated on its
    # own lifted assignments.
    assignments = tuple(representative + (0,) for representative in JC_REPRESENTATIVES)
    return model(data, labels + (5,), prefix, assignments)


def ordered_quartet_invariant(model_data, order=(1, 2, 5, 3)):
    assignments = []
    for representative in JC_REPRESENTATIVES:
        full = [0] * 5
        for label, character in zip(order, representative):
            full[label - 1] = character
        assignments.append(tuple(full))
    coordinates = evaluate_jc_coordinates(
        model_data["network"]["vertices"],
        model_data["edges"],
        dict(zip(model_data["network"]["leaves"], model_data["labels"])),
        assignments,
        model_data["edge_parameters"],
        dict(zip(model_data["reticulations"], model_data["inheritance_parameters"])),
    )
    J, K, M, N = coordinates[9], coordinates[10], coordinates[12], coordinates[13]
    return sp.factor(J - K - M + N)


def verify_nonroot_obstruction(networks):
    source = augmented_model(networks[16], SOURCE_LABELS, "liftA_")
    target = augmented_model(networks[16], TARGET_LABELS, "liftB_")
    for data in (source, target):
        assert valid_binary_strong(data["network"]["vertices"], data["edges"])
        assert internal_cycle_lengths(data["network"]["vertices"], data["edges"]) == [4, 5, 7]

    source_underlying = root_suppressed_underlying(source["network"], source["labels"])
    target_underlying = root_suppressed_underlying(target["network"], target["labels"])
    assert not colored_underlying_isomorphisms(source_underlying, target_underlying)

    source_invariant = ordered_quartet_invariant(source)
    target_invariant = ordered_quartet_invariant(target)
    assert source_invariant == 0
    e = target["edge_parameters"]
    inheritance = target["inheritance_parameters"]
    expected = -2 * e[1] * e[11] * e[12] * e[13] * e[3] * e[4] * e[6] * e[7] * e[8] * e[9] * (
        e[2] - 1
    ) * (inheritance[0] - 1) * (inheritance[1] - 1)
    assert sp.factor(target_invariant - expected) == 0
    # The three parenthesized factors are negative and every other parameter
    # factor is positive, so the target invariant is strictly positive.
    return {
        "binary_strong_tree_child_level_2": True,
        "blob_cycle_lengths": [4, 5, 7],
        "triangle_count": 0,
        "underlying_leaf_labelled_isomorphism_count": 0,
        "ordered_quartet": [1, 2, 5, 3],
        "invariant": "J-K-M+N",
        "source_pullback": "0",
        "target_pullback": str(target_invariant),
        "target_strictly_positive_on_complete_open_cube": True,
        "stochastic_interiors_disjoint": True,
    }


def main():
    _raw, networks = enumerate_networks()
    output = {
        "status": "EXACTLY COMPUTED",
        "move": "Omega: JC root path reversal",
        "root_graph_classification": verify_root_graphs(networks),
        "rational_omega_map": verify_omega_map(networks),
        "root_relocation": verify_root_relocation(networks),
        "dimension_and_rank": verify_dimension_and_ranks(networks),
        "nonroot_obstruction": verify_nonroot_obstruction(networks),
        "conclusion": (
            "Omega gives two non-triangle-equivalent semi-directed root topologies "
            "with a common nine-dimensional regular JC region, but its incoming-port "
            "lifts have disjoint open stochastic images"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
