"""Exact lifting classification for the JC root-collapsed Psi orbit.

The four root-spanning models in ``verify_jc_psi_move`` share a regular
seven-dimensional JC region.  This verifier restores an incoming cut edge
and an outgroup leaf.  It proves that the orbit then splits into two classes:

* A and B_reflected have a full-dimensional ten-dimensional overlap and are
  related by ordinary redirection of the restored triangle;
* A_reflected and B form the second triangle-redirection pair;
* a quartet polynomial is zero on the first pair and strictly positive on
  every open stochastic point of the second pair.

Thus Psi is a genuinely distinct semi-directed move only when the global-root
artifact suppresses its triangle.  Its surviving nonroot lift is exactly the
standard triangle move, not a stackable new semi-directed ambiguity.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import permutations, product
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from enumerate_four_leaf_root_theta import enumerate_networks, valid_binary_strong
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_psi_move import TOPOLOGIES


PAIR_ZERO = ("A", "B_reflected")
PAIR_POSITIVE = ("A_reflected", "B")
SOURCE_FREE_COLUMNS = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10)
TARGET_FREE_COLUMNS = (0, 1, 2, 3, 4, 5, 7, 8, 9, 10)
RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 14, 15)


def canonical_character_orbit(assignment):
    images = []
    for permutation in permutations((1, 2, 3)):
        mapping = {0: 0, 1: permutation[0], 2: permutation[1], 3: permutation[2]}
        images.append(tuple(mapping[value] for value in assignment))
    return min(images)


FIVE_LEAF_REPRESENTATIVES = tuple(
    sorted(
        {
            canonical_character_orbit(assignment)
            for assignment in product(range(4), repeat=5)
            if reduce(int.__xor__, assignment, 0) == 0
        }
    )
)

FIVE_LEAF_ZERO_SUM = tuple(
    (first, second, third, fourth, first ^ second ^ third ^ fourth)
    for first, second, third, fourth in product(range(4), repeat=4)
)


def augmented_network(name):
    """Restore an incoming cut edge and attach labelled outgroup leaf 5."""
    _raw, networks = enumerate_networks()
    network_index, labels = TOPOLOGIES[name]
    base = networks[network_index]
    vertices = dict(base["vertices"])
    vertices["S"] = "T"
    vertices["RHO"] = "S"
    vertices["LIN"] = "L"
    edges = tuple(tuple(edge) for edge in base["edges"]) + (
        ("RHO", "S"),
        ("RHO", "LIN"),
    )
    leaf_labels = dict(zip(base["leaves"], labels))
    leaf_labels["LIN"] = 5
    return {
        "name": name,
        "census_index": network_index,
        "port_labels": labels,
        "vertices": vertices,
        "edges": edges,
        "leaf_labels": leaf_labels,
    }


def model(name, prefix, assignments=FIVE_LEAF_REPRESENTATIVES):
    network = augmented_network(name)
    reticulations = reticulation_vertices(network["vertices"])
    edge_parameters = sp.symbols(f"{prefix}e0:{len(network['edges'])}")
    inheritance_parameters = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        network["edges"],
        network["leaf_labels"],
        assignments,
        edge_parameters,
        dict(zip(reticulations, inheritance_parameters)),
    )
    return {
        **network,
        "reticulations": reticulations,
        "edge_parameters": edge_parameters,
        "inheritance_parameters": inheritance_parameters,
        "parameters": edge_parameters + inheritance_parameters,
        "coordinates": coordinates,
    }


def normalized_cycle(cycle):
    images = []
    for sequence in (cycle, tuple(reversed(cycle))):
        for offset in range(len(sequence)):
            images.append(sequence[offset:] + sequence[:offset])
    return min(images)


def internal_cycles(network):
    vertices = tuple(
        sorted(vertex for vertex, color in network["vertices"].items() if color != "L")
    )
    adjacency = defaultdict(set)
    for tail, head in network["edges"]:
        if network["vertices"][tail] != "L" and network["vertices"][head] != "L":
            adjacency[tail].add(head)
            adjacency[head].add(tail)
    cycles = set()

    def visit(start, path):
        for neighbour in adjacency[path[-1]]:
            if neighbour == start and len(path) >= 3:
                cycles.add(normalized_cycle(tuple(path)))
            elif neighbour not in path and neighbour >= start:
                visit(start, path + [neighbour])

    for start in vertices:
        visit(start, [start])
    return tuple(sorted(cycles))


def connected_after_deletion(network, deleted):
    vertices = {
        vertex
        for vertex, color in network["vertices"].items()
        if color != "L" and vertex not in deleted and vertex != "RHO"
    }
    adjacency = defaultdict(set)
    for tail, head in network["edges"]:
        if tail in vertices and head in vertices:
            adjacency[tail].add(head)
            adjacency[head].add(tail)
    if not vertices:
        return True
    reached = set()
    stack = [next(iter(vertices))]
    while stack:
        vertex = stack.pop()
        if vertex in reached:
            continue
        reached.add(vertex)
        stack.extend(adjacency[vertex] - reached)
    return reached == vertices


def verify_network_class():
    summary = {}
    for name in TOPOLOGIES:
        network = augmented_network(name)
        assert valid_binary_strong(network["vertices"], network["edges"])
        assert len(reticulation_vertices(network["vertices"])) == 2
        cycles = internal_cycles(network)
        # RHO lies outside the blob.  The core itself is biconnected and has
        # precisely the 3-, 6-, and 7-cycles shown by this exact enumeration.
        assert sorted(map(len, cycles)) == [3, 6, 7]
        core_vertices = {
            vertex
            for vertex, color in network["vertices"].items()
            if color != "L" and vertex != "RHO"
        }
        assert all(connected_after_deletion(network, {vertex}) for vertex in core_vertices)
        summary[name] = {
            "cycle_lengths": sorted(map(len, cycles)),
            "reticulations_in_blob": 2,
            "binary_strong_tree_child": True,
        }
    return summary


def root_suppressed_underlying(network):
    root = next(vertex for vertex, color in network["vertices"].items() if color == "S")
    colors = {}
    for vertex, color in network["vertices"].items():
        if vertex == root:
            continue
        colors[vertex] = (
            f"L{network['leaf_labels'][vertex]}" if color == "L" else "I"
        )
    root_children = []
    edges = []
    for tail, head in network["edges"]:
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
    answers = []
    keys = sorted(first_groups)
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


def directed_reticulation_edges(network):
    return {
        (tail, head)
        for tail, head in network["edges"]
        if network["vertices"][head] in {"R", "X"}
    }


def verify_triangle_redirection_pair(first_name, second_name):
    first = augmented_network(first_name)
    second = augmented_network(second_name)
    isomorphisms = colored_underlying_isomorphisms(
        root_suppressed_underlying(first), root_suppressed_underlying(second)
    )
    assert len(isomorphisms) == 1
    mapping = isomorphisms[0]
    first_triangle = {"S", "U", "V"}
    second_triangle = {"S", "U", "V"}
    assert {mapping[vertex] for vertex in first_triangle} == second_triangle

    first_directed = directed_reticulation_edges(first)
    second_directed = directed_reticulation_edges(second)
    transported_outside = {
        (mapping[tail], mapping[head])
        for tail, head in first_directed
        if {tail, head} - first_triangle
    }
    second_outside = {
        edge for edge in second_directed if set(edge) - second_triangle
    }
    assert transported_outside == second_outside

    first_triangle_reticulation = next(
        vertex for vertex in first_triangle if first["vertices"][vertex] in {"R", "X"}
    )
    second_triangle_reticulation = next(
        vertex for vertex in second_triangle if second["vertices"][vertex] in {"R", "X"}
    )
    assert mapping[first_triangle_reticulation] != second_triangle_reticulation
    return {
        "underlying_isomorphism_count": len(isomorphisms),
        "source_triangle_reticulation": first_triangle_reticulation,
        "mapped_source_triangle_reticulation": mapping[first_triangle_reticulation],
        "target_triangle_reticulation": second_triangle_reticulation,
        "outside_reticulation_directions_preserved": True,
    }


def ordered_quartet_coordinates(model_data, order=(5, 1, 2, 3)):
    assignments = []
    for representative in JC_REPRESENTATIVES:
        full = [0] * 5
        for label, character in zip(order, representative):
            full[label - 1] = character
        assignments.append(tuple(full))
    return evaluate_jc_coordinates(
        model_data["vertices"],
        model_data["edges"],
        model_data["leaf_labels"],
        assignments,
        model_data["edge_parameters"],
        dict(zip(model_data["reticulations"], model_data["inheritance_parameters"])),
    )


def quartet_invariant(model_data):
    coordinates = ordered_quartet_coordinates(model_data)
    _A, _B, _C, _D, _E, _F, _G, _H, J, K, _L, M, N, _O = coordinates[1:]
    return sp.factor(J - K - M + N)


def verify_strict_separation(models):
    values = {name: quartet_invariant(data) for name, data in models.items()}
    assert values["A"] == 0
    assert values["B_reflected"] == 0

    data = models["A_reflected"]
    e = data["edge_parameters"]
    inheritance = data["inheritance_parameters"][0]
    expected = -2 * e[1] * e[10] * e[12] * e[13] * e[3] * e[6] * e[8] * e[9] * (
        e[5] * (inheritance * e[0] + (1 - inheritance) * e[2]) - 1
    )
    assert sp.factor(values["A_reflected"] - expected) == 0

    data = models["B"]
    e = data["edge_parameters"]
    inheritance = data["inheritance_parameters"][0]
    u = inheritance * e[0] + (1 - inheritance) * e[2]
    v = inheritance * e[0] * e[1] + (1 - inheritance) * e[2]
    expected = -2 * e[10] * e[12] * e[13] * e[4] * e[6] * e[8] * e[9] * (
        e[1] * e[3] * u - v
    )
    assert sp.factor(values["B"] - expected) == 0

    # On the complete open JC cube, the outside factors are positive.
    # For A_reflected, e5*u < 1.  For B, e1*e3*u < e1*u < v.
    # Therefore both displayed pullbacks are strictly positive.
    return {
        "ordered_quartet": [5, 1, 2, 3],
        "invariant": "J-K-M+N",
        "zero_pair": list(PAIR_ZERO),
        "strictly_positive_pair": list(PAIR_POSITIVE),
        "strict_on_complete_open_parameter_cube": True,
        "A_reflected_factorization": str(sp.factor(values["A_reflected"])),
        "B_factorization": str(sp.factor(values["B"])),
    }


def lifting_substitutions(source, target):
    ae = source["edge_parameters"]
    al = source["inheritance_parameters"]
    be = target["edge_parameters"]
    bl = target["inheritance_parameters"]
    denominator = ae[0] * ae[1] + ae[2]
    source_substitution = {
        ae[5]: sp.Rational(1, 2),
        al[0]: sp.Rational(1, 2),
        al[1]: sp.Rational(1, 2),
    }
    target_substitution = {
        be[0]: 4 * ae[0] * ae[1] * ae[3] / denominator,
        be[1]: ae[1],
        be[2]: 4 * ae[1] * ae[2] * ae[3] / denominator,
        be[3]: denominator / (4 * ae[1]),
        be[4]: ae[6],
        be[5]: ae[7],
        be[6]: sp.Rational(1, 2),
        be[7]: ae[4],
        be[8]: ae[9],
        be[9]: ae[10],
        be[10]: ae[8],
        be[11]: ae[11],
        be[12]: ae[12],
        be[13]: ae[13],
        bl[0]: sp.Rational(1, 2),
        bl[1]: sp.Rational(1, 2),
    }
    return denominator, source_substitution, target_substitution


def verify_full_tensor_map():
    coordinate_checks = {}
    denominator = None
    for source_name, target_name in (PAIR_ZERO, PAIR_POSITIVE):
        source = model(source_name, f"map{source_name}_", FIVE_LEAF_ZERO_SUM)
        target = model(target_name, f"map{target_name}_", FIVE_LEAF_ZERO_SUM)
        pair_denominator, source_substitution, target_substitution = lifting_substitutions(
            source, target
        )
        differences = tuple(
            sp.factor(
                source_coordinate.subs(source_substitution)
                - target_coordinate.subs(target_substitution)
            )
            for source_coordinate, target_coordinate in zip(
                source["coordinates"], target["coordinates"]
            )
        )
        assert all(difference == 0 for difference in differences)
        coordinate_checks[f"{source_name}--{target_name}"] = len(differences)
        if denominator is None:
            denominator = pair_denominator

    # Explicit rational source box.  The crude endpoint bounds imply all four
    # rational target parameters b0,b1,b2,b3 lie strictly in (0,1).
    a0_low, a0_high = sp.Rational(89, 100), sp.Rational(91, 100)
    middle_low, middle_high = sp.Rational(99, 200), sp.Rational(101, 200)
    denominator_low = a0_low * middle_low + middle_low
    denominator_high = a0_high * middle_high + middle_high
    assert 4 * a0_high * middle_high**2 < denominator_low
    assert 4 * middle_high**3 < denominator_low
    assert denominator_high < 4 * middle_low
    return {
        "zero_sum_coordinates_checked": coordinate_checks,
        "rational_denominator": str(denominator),
        "source_box": {
            "a0": [str(a0_low), str(a0_high)],
            "a1,a2,a3": [str(middle_low), str(middle_high)],
            "all_other_free_source_multipliers": ["0", "1"],
        },
        "target_open_cube_certified_by_endpoint_bounds": True,
    }


def exact_point_and_ranks():
    source = model("A", "rankA_")
    target = model("B_reflected", "rankB_")
    denominator, source_fixed, target_map = lifting_substitutions(source, target)
    ae = source["edge_parameters"]
    al = source["inheritance_parameters"]
    source_fixed.update(
        {
            ae[11]: sp.Rational(1, 2),
            ae[12]: sp.Rational(1, 2),
            ae[13]: sp.Rational(1, 2),
        }
    )
    source_values = (
        sp.Rational(9, 10),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(2, 5),
        sp.Rational(1, 10),
        sp.Rational(1, 3),
        sp.Rational(3, 5),
        sp.Rational(2, 3),
        sp.Rational(3, 4),
    )
    source_point = dict(source_fixed)
    source_point.update(
        {
            source["parameters"][index]: value
            for index, value in zip(SOURCE_FREE_COLUMNS, source_values)
        }
    )
    assert set(source_point) == set(source["parameters"])
    target_point = {
        parameter: sp.factor(value.subs(source_point))
        for parameter, value in target_map.items()
    }
    assert set(target_point) == set(target["parameters"])
    assert all(0 < value < 1 for value in source_point.values())
    assert all(0 < value < 1 for value in target_point.values())

    source_jacobian = sp.Matrix(source["coordinates"][1:]).jacobian(source["parameters"])
    target_jacobian = sp.Matrix(target["coordinates"][1:]).jacobian(target["parameters"])
    assert DomainMatrix.from_Matrix(source_jacobian).rank() == 10
    assert DomainMatrix.from_Matrix(target_jacobian).rank() == 10

    source_minor = sp.factor(
        source_jacobian.subs(source_point).extract(RANK_ROWS, SOURCE_FREE_COLUMNS).det()
    )
    target_minor = sp.factor(
        target_jacobian.subs(target_point).extract(RANK_ROWS, TARGET_FREE_COLUMNS).det()
    )
    assert source_minor == -sp.Rational(263169, 13743895347200000000000)
    assert target_minor == sp.Rational(5000211, 274877906944000000000000)

    gauge_parameters = [source["parameters"][index] for index in SOURCE_FREE_COLUMNS]
    gauge_outputs = [
        source["coordinates"][row + 1].subs(source_fixed) for row in RANK_ROWS
    ]
    gauge_determinant = sp.factor(sp.Matrix(gauge_outputs).jacobian(gauge_parameters).det())
    expected = -(
        ae[0]
        * ae[1] ** 2
        * ae[10] ** 3
        * ae[3] ** 3
        * ae[4] ** 3
        * ae[6] ** 2
        * ae[7]
        * ae[8]
        * ae[9] ** 3
        * (ae[1] - 1) ** 2
        * (ae[6] - 1) ** 2
        * denominator**2
        / 2**32
    )
    assert sp.factor(gauge_determinant - expected) == 0
    return {
        "generic_model_dimensions": {"A": 10, "B_reflected": 10},
        "rank_rows": list(RANK_ROWS),
        "source_rank_columns": list(SOURCE_FREE_COLUMNS),
        "target_rank_columns": list(TARGET_FREE_COLUMNS),
        "source_rank_minor": str(source_minor),
        "target_rank_minor": str(target_minor),
        "common_gauge_determinant": str(gauge_determinant),
        "source_point": {str(parameter): str(value) for parameter, value in source_point.items()},
        "target_point": {str(parameter): str(value) for parameter, value in target_point.items()},
    }


def main():
    models = {name: model(name, f"sep{name}_") for name in TOPOLOGIES}
    output = {
        "status": "EXACTLY COMPUTED",
        "network_class": verify_network_class(),
        "triangle_redirection_pairs": {
            "A--B_reflected": verify_triangle_redirection_pair("A", "B_reflected"),
            "A_reflected--B": verify_triangle_redirection_pair("A_reflected", "B"),
        },
        "strict_quartet_separation": verify_strict_separation(models),
        "full_tensor_map": verify_full_tensor_map(),
        "rank_certificate": exact_point_and_ranks(),
        "conclusion": (
            "the fourfold root Psi orbit splits after restoring an incoming cut edge "
            "into two strictly separated ordinary triangle-redirection pairs"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
