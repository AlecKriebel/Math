#!/usr/bin/env python3
"""Exact K2P/K3P displayed-tree containment and exponential-family certificate.

For any chosen displayed tree, make every unchosen reticulation arc the
uniform group-based kernel.  The parent mixture then becomes an ordinary
Markov edge with Fourier multipliers p*a(g).  A positive convolution
factorization assigns all remaining network edges and inheritance factors.

The verifier checks the universal local identity, the two three-port cycle
presentations, exact tree and critical-cycle ranks, and the all-m combinatorial
family for m=1,...,4.  The mathematical induction proving the arbitrary-m and
arbitrary-network statements is recorded in Milestone 6F.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import (
    canonical_code,
    valid_binary_strong,
)
from verify_group_based_root_two_port_collapse import (
    factorization_chambers,
    fourier,
)
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import canonical_mixed_graph
from verify_jc_root_spanning_atlas import triangles
from verify_jc_root_three_port_saturation import enumerate_unlabelled
from verify_k2p_root_three_port_saturation import (
    ORBIT_REPRESENTATIVES,
    k2p_parameterization,
)
from verify_k3p_root_three_port_atlas import (
    ASSIGNMENTS,
    NONCONSTANT_ASSIGNMENTS,
    k3p_parameterization,
    k3p_transition_probabilities,
    quartic_expression,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "group_based_displayed_tree_containment.json"
DEPENDENCIES = (
    "group_based_root_two_port_collapse.json",
    "jc_root_three_port_tree_separation.json",
    "k2p_root_three_port_saturation.json",
    "k3p_root_three_port_atlas.json",
    "group_based_triangle_redirection.json",
)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def universal_uniformization_identity():
    p, r0, r1, r2 = sp.symbols("p r0 r1 r2")
    source = (r0, r1, r2, 1 - r0 - r1 - r2)
    uniform = (sp.Rational(1, 4),) * 4
    effective = tuple(
        sp.factor(p * value + (1 - p) * uniform[index])
        for index, value in enumerate(source)
    )
    source_fourier = fourier(source)
    effective_fourier = fourier(effective)
    assert effective_fourier[0] == 1
    for character in range(1, 4):
        assert sp.factor(
            effective_fourier[character] - p * source_fourier[character]
        ) == 0
    assert fourier(uniform) == (1, 0, 0, 0)

    # Subtracting the same uniform mass and rescaling preserves every K2P
    # probability-coordinate equality, independently of the chosen character
    # naming convention.
    for first, second in combinations(range(4), 2):
        assert sp.factor(
            effective[first]
            - effective[second]
            - p * (source[first] - source[second])
        ) == 0
    return {
        "source_probabilities": [str(value) for value in source],
        "effective_probabilities": [str(value) for value in effective],
        "effective_nonzero_Fourier_multipliers": [
            str(sp.factor(p * source_fourier[character]))
            for character in range(1, 4)
        ],
        "uniform_kernel_Fourier_multipliers": [1, 0, 0, 0],
        "exact_Fourier_identities": 4,
        "strict_positivity": (
            "if 0<p<1 and every r_h>0, then every "
            "p*r_h+(1-p)/4 is strictly positive"
        ),
    }


def edge_multiplier(parameters, edge, character, model):
    if character == 0:
        return sp.Integer(1)
    if model == "K2P":
        return parameters[2 * edge + (0 if character == 1 else 1)]
    assert model == "K3P"
    return parameters[3 * edge + character - 1]


def effective_cycle_arms(parameters, inheritance, record_id, model):
    multiplier = lambda edge, character: edge_multiplier(
        parameters, edge, character, model
    )
    if record_id == 1:
        first_path = (0, 2, 4)
    elif record_id == 2:
        first_path = (2, 4)
    else:
        raise ValueError(record_id)
    arms = []
    for port in range(3):
        values = []
        for character in range(4):
            if port == 0:
                value = sp.prod(multiplier(edge, character) for edge in first_path)
            elif port == 1:
                value = multiplier(5, character)
            elif character == 0:
                value = sp.Integer(1)
            else:
                value = (1 - inheritance) * multiplier(3, character) * multiplier(6, character)
            values.append(sp.factor(value))
        arms.append(tuple(values))
    return tuple(arms)


def star_coordinate(assignment, arms):
    return sp.factor(
        sp.prod(arms[leaf][character] for leaf, character in enumerate(assignment))
    )


def cycle_tensor_identities(records):
    results = []
    for record_id, uniform_edge in ((1, 1), (2, 0)):
        network = records[record_id]["network"]

        k2_outputs, k2_parameters = k2p_parameterization(network, f"c{record_id}_")
        k2_inheritance = k2_parameters[-1]
        k2_zero = {
            k2_parameters[2 * uniform_edge]: 0,
            k2_parameters[2 * uniform_edge + 1]: 0,
        }
        k2_arms = effective_cycle_arms(
            k2_parameters, k2_inheritance, record_id, "K2P"
        )
        for assignment in ORBIT_REPRESENTATIVES:
            assert sp.factor(
                k2_outputs[assignment].subs(k2_zero)
                - star_coordinate(assignment, k2_arms)
            ) == 0

        k3_outputs, k3_parameters = k3p_parameterization(network, f"d{record_id}_")
        k3_inheritance = k3_parameters[-1]
        k3_zero = {
            k3_parameters[3 * uniform_edge + offset]: 0 for offset in range(3)
        }
        k3_arms = effective_cycle_arms(
            k3_parameters, k3_inheritance, record_id, "K3P"
        )
        for assignment in ASSIGNMENTS:
            assert sp.factor(
                k3_outputs[assignment].subs(k3_zero)
                - star_coordinate(assignment, k3_arms)
            ) == 0

        results.append(
            {
                "record_id": record_id,
                "uniform_incoming_edge_index": uniform_edge,
                "K2P_exact_coordinate_identities": len(ORBIT_REPRESENTATIVES),
                "K3P_exact_coordinate_identities": len(ASSIGNMENTS),
                "effective_arm_edge_paths": {
                    "port_0": [0, 2, 4] if record_id == 1 else [2, 4],
                    "port_1": [5],
                    "port_2": [
                        "JC inheritance multiplier 1-lambda",
                        3,
                        6,
                    ],
                },
            }
        )
    return results


def first_nonzero_minor(matrix, rank):
    _rref, row_pivots = matrix.T.rref()
    rows = tuple(row_pivots[:rank])
    assert len(rows) == rank
    row_matrix = matrix.extract(rows, range(matrix.cols))
    _rref, column_pivots = row_matrix.rref()
    columns = tuple(column_pivots[:rank])
    assert len(columns) == rank
    determinant = sp.factor(matrix.extract(rows, columns).det())
    assert determinant != 0
    return rows, columns, determinant


def star_parameterization(assignments, model):
    width = 2 if model == "K2P" else 3
    parameters = sp.symbols(f"{model.lower()}a0:{3 * width}")

    def multiplier(leaf, character):
        if character == 0:
            return sp.Integer(1)
        if model == "K2P":
            return parameters[2 * leaf + (0 if character == 1 else 1)]
        return parameters[3 * leaf + character - 1]

    outputs = tuple(
        sp.prod(multiplier(leaf, character) for leaf, character in enumerate(assignment))
        for assignment in assignments
    )
    return parameters, outputs


def rank_certificates(records):
    result = {}
    target_by_assignment = {
        assignment: sp.Rational(1, 8) ** sum(character != 0 for character in assignment)
        for assignment in ASSIGNMENTS
    }
    for model, assignments, expected_tree_rank, expected_cycle_rank in (
        ("K2P", ORBIT_REPRESENTATIVES, 6, 8),
        ("K3P", NONCONSTANT_ASSIGNMENTS, 9, 12),
    ):
        tree_parameters, tree_outputs = star_parameterization(assignments, model)
        tree_substitution = {
            parameter: sp.Rational(1, 8) for parameter in tree_parameters
        }
        tree_jacobian = sp.Matrix(tree_outputs).jacobian(tree_parameters).subs(
            tree_substitution
        )
        assert tree_jacobian.rank() == expected_tree_rank
        tree_rows, tree_columns, tree_minor = first_nonzero_minor(
            tree_jacobian, expected_tree_rank
        )
        assert all(
            output.subs(tree_substitution) == target_by_assignment[assignment]
            for assignment, output in zip(assignments, tree_outputs)
        )

        cycle_records = []
        for record_id, uniform_edge in ((1, 1), (2, 0)):
            network = records[record_id]["network"]
            if model == "K2P":
                outputs, parameters = k2p_parameterization(network, f"w{record_id}_")
                values = {
                    1: (sp.Rational(1, 2), 0, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 8), sp.Rational(1, 2)),
                    2: (0, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 2)),
                }[record_id]
                substitution = {}
                for edge, value in enumerate(values):
                    substitution[parameters[2 * edge]] = value
                    substitution[parameters[2 * edge + 1]] = value
                substitution[parameters[-1]] = sp.Rational(1, 2)
                selected_outputs = [outputs[assignment] for assignment in assignments]
                transition_probabilities = []
                for edge, value in enumerate(values):
                    singleton = substitution[parameters[2 * edge]]
                    doubleton = substitution[parameters[2 * edge + 1]]
                    transition_probabilities.extend(
                        (
                            (1 + singleton + 2 * doubleton) / 4,
                            (1 + singleton - 2 * doubleton) / 4,
                            (1 - singleton) / 4,
                            (1 - singleton) / 4,
                        )
                    )
            else:
                outputs, parameters = k3p_parameterization(network, f"z{record_id}_")
                values = {
                    1: (sp.Rational(1, 2), 0, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 8), sp.Rational(1, 2)),
                    2: (0, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 2)),
                }[record_id]
                substitution = {}
                transition_probabilities = []
                for edge, value in enumerate(values):
                    for offset in range(3):
                        substitution[parameters[3 * edge + offset]] = value
                    transition_probabilities.extend(
                        k3p_transition_probabilities(value, value, value)
                    )
                substitution[parameters[-1]] = sp.Rational(1, 2)
                selected_outputs = [outputs[assignment] for assignment in assignments]

            assert values[uniform_edge] == 0
            assert min(transition_probabilities) == sp.Rational(1, 8)
            assert all(
                output.subs(substitution) == target_by_assignment[assignment]
                for assignment, output in zip(assignments, selected_outputs)
            )
            jacobian = sp.Matrix(selected_outputs).jacobian(parameters).subs(substitution)
            assert jacobian.rank() == expected_cycle_rank
            rows, columns, determinant = first_nonzero_minor(
                jacobian, expected_cycle_rank
            )
            cycle_records.append(
                {
                    "record_id": record_id,
                    "uniform_edge_index": uniform_edge,
                    "edge_diagonal_multiplier_values": [str(value) for value in values],
                    "inheritance_probability": "1/2",
                    "minimum_transition_probability": "1/8",
                    "parameterization_rank_at_containment_witness": expected_cycle_rank,
                    "rank_minor_rows": list(rows),
                    "rank_minor_columns": list(columns),
                    "rank_minor": str(determinant),
                }
            )

        result[model] = {
            "common_tree_target": {
                "three_effective_arm_multiplier_vectors": [
                    ["1/8"] * (2 if model == "K2P" else 3)
                ]
                * 3,
                "pair_coordinates": "1/64",
                "all_distinct_triple_coordinates": "1/512",
            },
            "tree_dimension_and_regular_rank": expected_tree_rank,
            "tree_rank_minor_rows": list(tree_rows),
            "tree_rank_minor_columns": list(tree_columns),
            "tree_rank_minor": str(tree_minor),
            "cycle_critical_witnesses": cycle_records,
        }

    # The K3P tree is contained in the H14 cycle class, so its quartic must
    # vanish.  Replay this directly on the full symbolic star tensor.
    tree_parameters, tree_outputs = star_parameterization(ASSIGNMENTS, "K3P")
    tree_coordinates = dict(zip(ASSIGNMENTS, tree_outputs))
    assert sp.factor(quartic_expression(tree_coordinates)) == 0
    result["K3P"]["quartic_tree_pullback"] = "0"
    return result


def caterpillar_family(bits):
    m = len(bits)
    vertices = {"S": "S"}
    edges = []
    leaves = [f"L{index}" for index in range(m + 2)]
    for leaf in leaves:
        vertices[leaf] = "L"
    edges.append(("S", "L0"))

    entries = [f"A{index}" if bit else f"V{index}" for index, bit in enumerate(bits, 1)]
    edges.append(("S", entries[0]))
    for index, bit in enumerate(bits, 1):
        continuation = entries[index] if index < m else f"L{m + 1}"
        if bit:
            top, side, reticulation = f"A{index}", f"B{index}", f"C{index}"
            vertices.update({top: "T", side: "T", reticulation: "X"})
            edges.extend(
                (
                    (top, side),
                    (top, reticulation),
                    (side, reticulation),
                    (side, f"L{index}"),
                    (reticulation, continuation),
                )
            )
        else:
            vertex = f"V{index}"
            vertices[vertex] = "T"
            edges.extend(((vertex, f"L{index}"), (vertex, continuation)))
    network = {"vertices": vertices, "edges": tuple(edges), "leaves": tuple(leaves)}
    assert valid_binary_strong(vertices, tuple(edges))
    return network


def undirected_adjacency(network, omitted_edge=None):
    adjacency = defaultdict(set)
    for edge in network["edges"]:
        if omitted_edge is not None and frozenset(edge) == frozenset(omitted_edge):
            continue
        left, right = edge
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def connected_component(adjacency, start):
    seen = {start}
    queue = deque((start,))
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen


def family_graph_checks(network, bits):
    triangle_edges = set()
    for index, bit in enumerate(bits, 1):
        if bit:
            triple = (f"A{index}", f"B{index}", f"C{index}")
            triangle_edges.update(frozenset(edge) for edge in combinations(triple, 2))
    graph = semi_directed_graph(network, tuple(range(len(network["leaves"]))))
    assert len(triangles(graph)) == sum(bits)

    vertices = set(network["vertices"])
    leaf_set = set(network["leaves"])
    bridges = 0
    for edge in network["edges"]:
        if frozenset(edge) in triangle_edges:
            continue
        adjacency = undirected_adjacency(network, edge)
        component = connected_component(adjacency, edge[0])
        assert edge[1] not in component
        other = vertices - component
        assert component & leaf_set and other & leaf_set
        bridges += 1
    return graph, bridges


def suppress_displayed_tree(network, bits):
    vertices = dict(network["vertices"])
    edges = set(network["edges"])
    for index, bit in enumerate(bits, 1):
        if bit:
            edges.remove((f"B{index}", f"C{index}"))

    changed = True
    while changed:
        changed = False
        for vertex, kind in list(vertices.items()):
            if kind in {"S", "L"}:
                continue
            incoming = [edge for edge in edges if edge[1] == vertex]
            outgoing = [edge for edge in edges if edge[0] == vertex]
            if len(incoming) == len(outgoing) == 1:
                parent = incoming[0][0]
                child = outgoing[0][1]
                edges.remove(incoming[0])
                edges.remove(outgoing[0])
                edges.add((parent, child))
                del vertices[vertex]
                changed = True
                break
    return vertices, tuple(sorted(edges))


def rooted_tree_shape(vertices, edges, leaf_labels):
    children = defaultdict(list)
    for parent, child in edges:
        children[parent].append(child)

    def visit(vertex):
        if vertices[vertex] == "L":
            return ("L", leaf_labels[vertex])
        return ("I", tuple(sorted((visit(child) for child in children[vertex]), key=repr)))

    return visit("S")


def exponential_family_certificate(max_checked_m=4):
    checked = []
    for m in range(1, max_checked_m + 1):
        base = caterpillar_family((0,) * m)
        labels = {leaf: index for index, leaf in enumerate(base["leaves"])}
        base_shape = rooted_tree_shape(base["vertices"], base["edges"], labels)
        rooted_codes = set()
        semi_codes = set()
        bit_signatures = set()
        records = []
        for bits in product((0, 1), repeat=m):
            network = caterpillar_family(bits)
            graph, bridge_count = family_graph_checks(network, bits)
            displayed_vertices, displayed_edges = suppress_displayed_tree(network, bits)
            assert rooted_tree_shape(displayed_vertices, displayed_edges, labels) == base_shape
            rooted = canonical_code(network["vertices"], network["edges"], labels)
            semi = canonical_mixed_graph(graph)
            rooted_codes.add(rooted)
            semi_codes.add(semi)
            signature = tuple(index for index, bit in enumerate(bits, 1) if bit)
            bit_signatures.add(signature)
            records.append(
                {
                    "bits": list(bits),
                    "triangle_sites": list(signature),
                    "reticulation_count": sum(bits),
                    "bridge_count": bridge_count,
                    "vertices": dict(sorted(network["vertices"].items())),
                    "edges": [list(edge) for edge in network["edges"]],
                    "leaves": list(network["leaves"]),
                    "rooted_code_sha256": sha256(repr(rooted).encode()).hexdigest(),
                    "semi_directed_code_sha256": sha256(repr(semi).encode()).hexdigest(),
                }
            )
        assert len(rooted_codes) == len(semi_codes) == len(bit_signatures) == 2**m
        checked.append(
            {
                "m": m,
                "leaf_count": m + 2,
                "family_size": 2**m,
                "distinct_rooted_topologies": len(rooted_codes),
                "distinct_semi_directed_topologies": len(semi_codes),
                "members": records,
            }
        )
    return {
        "schema": (
            "start with the rooted labelled caterpillar on L0,...,L_(m+1); "
            "at site i independently retain its ordinary binary vertex or "
            "replace it by A_i->B_i, A_i->C_i, B_i->C_i with C_i reticulate"
        ),
        "all_m_formulas": {
            "leaf_count": "m+2",
            "topology_count": "2^m",
            "triangle_count_of_member_bits": "sum(bits)",
            "K2P_common_tree_model_dimension": "2*(2*(m+2)-3)=4*m+2",
            "K3P_common_tree_model_dimension": "3*(2*(m+2)-3)=6*m+3",
        },
        "checked_examples": checked,
    }


def generate_certificate():
    dependency_hashes = {
        name: file_sha256(HERE / "certificates" / name) for name in DEPENDENCIES
    }
    factorization = factorization_chambers()
    assert len(factorization) == 4
    records = enumerate_unlabelled()
    identities = cycle_tensor_identities(records)
    ranks = rank_certificates(records)
    family = exponential_family_certificate()

    certificate = {
        "status": {
            "K2P_every_displayed_tree_complete_stochastic_containment": "PROVED",
            "K3P_every_displayed_tree_complete_stochastic_containment": "PROVED",
            "JC_open_displayed_tree_containment_by_uniformization": (
                "PROVED ABSENT; uniform multiplier x=0 is excluded"
            ),
            "K2P_K3P_exponential_one_sided_topology_fibers": "PROVED",
            "full_dimensional_bowtie_of_exponential_family": "UNRESOLVED",
        },
        "theorem": {
            "statement": (
                "For M in {K2P,K3P}, every binary rooted network N and every "
                "displayed tree T satisfy M_T^M subseteq M_N^M on the complete "
                "open stochastic tree image."
            ),
            "local_uniformization": universal_uniformization_identity(),
            "positive_factorization_chambers": factorization,
            "construction": [
                "choose the parent retained in the displayed tree at each reticulation",
                "put the uniform kernel on every unchosen incoming arc",
                "replace each local parent mixture by p*T+(1-p)*U",
                "factor every target tree-edge kernel into the required JC inheritance factors and strict network-edge kernels",
            ],
            "models": {
                "K2P": "closed under convolution and contains every JC and uniform kernel",
                "K3P": "all strict group-based kernels; closed under convolution",
            },
        },
        "three_port_cycle_corollary": {
            "complete_tree_image_contained_in_each_labelled_cycle_orientation": True,
            "distinct_rooted_cycle_topologies": 9,
            "distinct_semi_directed_cycle_topologies": 3,
            "tensor_identities": identities,
            "rank_certificates": ranks,
            "relations": {
                "K2P": "tree preceq cycle; dimensions 6<9; not bowtie",
                "K3P": "tree preceq cycle; dimensions 9<14; not bowtie",
                "JC": "open stochastic interiors disjoint by the prior strict invariant",
            },
        },
        "exponential_family": family,
        "dependency_file_sha256": dependency_hashes,
        "conclusion": (
            "Under K2P and K3P, generic exact data from a displayed tree are "
            "compatible with every network displaying that tree.  In the "
            "explicit strong level-1 family on m+2 leaves, every open tree "
            "distribution has at least 2^m pairwise non-triangle-equivalent "
            "compatible topologies."
        ),
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate["deterministic_sha256"] = sha256(payload.encode()).hexdigest()
    return certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(
        json.dumps(
            {
                "deterministic_sha256": certificate["deterministic_sha256"],
                "status": certificate["status"],
                "three_port_relations": certificate["three_port_cycle_corollary"]["relations"],
                "checked_family_sizes": [
                    record["family_size"]
                    for record in certificate["exponential_family"]["checked_examples"]
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
