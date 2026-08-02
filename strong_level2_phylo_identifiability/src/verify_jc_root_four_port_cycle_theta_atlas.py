#!/usr/bin/env python3
"""Exact JC root four-port cycle--theta atlas and contextual C_root replay."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

from flint import fmpq_mpoly_ctx

from enumerate_four_leaf_root_theta import (
    canonical_code,
    enumerate_networks,
    labelled_canonical_codes,
    valid_binary_strong,
)
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES, coordinate_permutation
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import canonical_mixed_graph
from verify_jc_root_spanning_atlas import (
    fraction_free_rank,
    move_components,
)
from verify_jc_root_three_port_saturation import build_cycle_root


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_root_four_port_cycle_theta_atlas.json"
THETA_CERTIFICATE = HERE / "certificates" / "jc_root_spanning_atlas.json"
COLLAPSE_CERTIFICATE = (
    HERE / "certificates" / "group_based_root_two_port_collapse.json"
)


def enumerate_cycles():
    cycles = {}
    for counts in ((0, 3), (1, 2), (2, 1), (3, 0)):
        network = build_cycle_root(counts)
        code = canonical_code(network["vertices"], network["edges"])
        cycles.setdefault(code, {"counts": counts, "network": network})
    return tuple(cycles[code] for code in sorted(cycles))


def cycle_items(cycles):
    items = []
    for network_index, record in enumerate(cycles):
        network = record["network"]
        assignments = labelled_canonical_codes(
            network["vertices"], network["edges"], network["leaves"]
        )
        assert len(assignments) == 24
        for assignment in assignments.values():
            items.append(
                (
                    network_index,
                    tuple(assignment[leaf] for leaf in network["leaves"]),
                )
            )
    return tuple(sorted(items))


def cycle_symbolic_data(network_index, network):
    edges = tuple(network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    assert len(reticulations) == 1
    leaf_set = set(network["leaves"])
    pendant = tuple(
        index for index, (_tail, head) in enumerate(edges) if head in leaf_set
    )
    internal = tuple(index for index in range(len(edges)) if index not in pendant)
    assert len(pendant) == 4 and len(internal) == 5
    context = fmpq_mpoly_ctx.get(
        [f"root_cycle_n{network_index}_p{index}" for index in range(6)]
    )
    parameters = context.gens()
    edge_parameters = [context.constant(1)] * len(edges)
    for local_index, edge_index in enumerate(internal):
        edge_parameters[edge_index] = parameters[local_index]
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], (1, 2, 3, 4))),
        JC_REPRESENTATIVES,
        tuple(edge_parameters),
        {reticulations[0]: parameters[-1]},
    )
    tangent = []
    for assignment, coordinate in zip(JC_REPRESENTATIVES[1:], coordinates[1:]):
        row = [coordinate.derivative(index) for index in range(6)]
        row.extend(
            int(assignment[leaf] != 0) * coordinate for leaf in range(4)
        )
        tangent.append(row)
    rank, pivots = fraction_free_rank(tangent)
    assert rank == 7
    return context, coordinates, {
        "rank": rank,
        "pivot_count": len(pivots),
        "last_pivot_sha256": sha256(str(pivots[-1]).encode()).hexdigest(),
    }


def item_signature(item, symbolic):
    network_index, labels = item
    context, base, _rank = symbolic[network_index]
    coordinate_map = coordinate_permutation(labels)
    coordinates = tuple(base[index] for index in coordinate_map)
    bits = []
    for invariant in ALL_INVARIANTS:
        polynomial = context.constant(0)
        for monomial, coefficient in invariant:
            term = context.constant(coefficient)
            for coordinate in monomial:
                term *= coordinates[coordinate]
            polynomial += term
        bits.append(bool(polynomial))
    return "".join("1" if bit else "0" for bit in bits)


def insert_root_cycle(network, tree_port_side):
    """Insert C_root above the two children of an ordinary root."""

    vertices = dict(network["vertices"])
    edges = list(network["edges"])
    children = sorted(head for tail, head in edges if tail == "S")
    assert len(children) == 2
    tree_child = children[tree_port_side]
    reticulation_child = children[1 - tree_port_side]
    edges = [edge for edge in edges if edge[0] != "S"]
    vertices.update({"CU": "T", "CV": "R"})
    edges.extend(
        (
            ("S", "CU"),
            ("S", "CV"),
            ("CU", "CV"),
            ("CU", tree_child),
            ("CV", reticulation_child),
        )
    )
    answer = {
        "vertices": vertices,
        "edges": tuple(edges),
        "leaves": network["leaves"],
    }
    assert valid_binary_strong(answer["vertices"], answer["edges"])
    return answer


def generate_certificate():
    theta_certificate = json.loads(THETA_CERTIFICATE.read_text())
    collapse_certificate = json.loads(COLLAPSE_CERTIFICATE.read_text())
    assert collapse_certificate["status"] == {
        "JC_complete_image_equality": "PROVED",
        "K2P_complete_image_equality": "PROVED",
        "K3P_complete_image_equality": "PROVED",
        "arbitrary_component_substitution_all_models": "PROVED",
        "move": "C_root",
    }

    cycles = enumerate_cycles()
    assert len(cycles) == 2
    assert {tuple(record["counts"]) for record in cycles} == {(0, 3), (1, 2)}
    items = cycle_items(cycles)
    assert len(items) == 48

    semi_groups = defaultdict(list)
    for item in items:
        network_index, labels = item
        graph = semi_directed_graph(cycles[network_index]["network"], labels)
        semi_groups[canonical_mixed_graph(graph)].append(item)
    assert len(semi_groups) == 12
    assert Counter(map(len, semi_groups.values())) == {4: 12}

    symbolic = {
        index: cycle_symbolic_data(index, record["network"])
        for index, record in enumerate(cycles)
    }
    signatures = {item: item_signature(item, symbolic) for item in items}
    signature_groups = defaultdict(list)
    for item, signature in signatures.items():
        signature_groups[signature].append(item)
    assert len(signature_groups) == 12
    assert Counter(map(len, signature_groups.values())) == {4: 12}
    assert {
        frozenset(group) for group in signature_groups.values()
    } == {frozenset(group) for group in semi_groups.values()}

    theta_components = theta_certificate["components"]
    assert all(
        component["id"] == index
        for index, component in enumerate(theta_components)
    )
    dimension_seven = {
        component["id"] for component in theta_components if component["dimension"] == 7
    }
    assert dimension_seven == set(range(96, 108))
    theta_signature_to_component = {
        component["signature"]: component["id"] for component in theta_components
    }
    assert set(signature_groups) == {
        theta_components[index]["signature"] for index in dimension_seven
    }

    _raw, theta_networks = enumerate_networks()
    theta_topology = move_components(theta_networks)
    theta_items = theta_topology["items"]
    theta_code_to_item = {}
    for item in theta_items:
        network_index, labels = item
        network = theta_networks[network_index]
        code = canonical_code(
            network["vertices"],
            tuple(tuple(edge) for edge in network["edges"]),
            dict(zip(network["leaves"], labels)),
        )
        theta_code_to_item[code] = item
    assert len(theta_code_to_item) == 612
    theta_item_to_component = {
        item: component_index
        for component_index, component in enumerate(theta_topology["components"])
        for item in component
    }

    balanced_index = next(
        index for index, record in enumerate(cycles) if tuple(record["counts"]) == (1, 2)
    )
    balanced = cycles[balanced_index]["network"]
    balanced_items = [item for item in items if item[0] == balanced_index]
    inserted_theta_items = set()
    insertion_records = []
    for item in balanced_items:
        _network_index, labels = item
        component_ids = set()
        for side in (0, 1):
            inserted = insert_root_cycle(balanced, side)
            code = canonical_code(
                inserted["vertices"],
                inserted["edges"],
                dict(zip(inserted["leaves"], labels)),
            )
            assert code in theta_code_to_item
            theta_item = theta_code_to_item[code]
            inserted_theta_items.add(theta_item)
            component_ids.add(theta_item_to_component[theta_item])
        assert len(component_ids) == 1
        signature_component = theta_signature_to_component[signatures[item]]
        assert component_ids == {signature_component}
        insertion_records.append(
            {
                "cycle_labels": list(labels),
                "theta_component": signature_component,
            }
        )
    expected_psi_items = {
        item
        for component_index in dimension_seven
        for item in theta_topology["components"][component_index]
    }
    assert inserted_theta_items == expected_psi_items
    assert len(inserted_theta_items) == 48

    combined_components = []
    for signature, group in sorted(
        signature_groups.items(), key=lambda entry: theta_signature_to_component[entry[0]]
    ):
        component_id = theta_signature_to_component[signature]
        theta_component = theta_components[component_id]
        assert theta_component["rooted_topology_count"] == 4
        assert theta_component["semi_directed_topology_count"] == 4
        combined_components.append(
            {
                "theta_component": component_id,
                "cycle_rooted_topology_count": len(group),
                "theta_rooted_topology_count": 4,
                "combined_rooted_topology_count": len(group) + 4,
                "cycle_semi_directed_topology_count": 1,
                "theta_semi_directed_topology_count": 4,
                "combined_semi_directed_topology_count": 5,
                "signature": signature,
                "cycle_members": [
                    {"network_index": item[0], "port_labels": list(item[1])}
                    for item in sorted(group)
                ],
            }
        )
    assert all(record["combined_rooted_topology_count"] == 8 for record in combined_components)

    cycle_records = []
    for index, record in enumerate(cycles):
        network = record["network"]
        cycle_records.append(
            {
                "id": index,
                "subdivision_counts": list(record["counts"]),
                "generic_jc_dimension": symbolic[index][2]["rank"],
                "rank_last_pivot_sha256": symbolic[index][2][
                    "last_pivot_sha256"
                ],
                "vertices": dict(sorted(network["vertices"].items())),
                "edges": [list(edge) for edge in network["edges"]],
                "leaves": list(network["leaves"]),
            }
        )

    return {
        "status": {
            "complete_nontrivial_root_four_port_bowtie_classification": "PROVED",
            "cycle_theta_cross_generator_overlap": "PROVED COMPLETE-IMAGE EQUALITY",
            "Psi_primitive_move": "PROVED REDUNDANT",
            "contextual_C_root_JC_K2P_K3P": "PROVED",
            "one_sided_containment_classification": "UNRESOLVED",
        },
        "scope": (
            "all binary strongly tree-child root-containing level-1 cycle "
            "and level-2 theta blobs with exactly four labelled outgoing ports"
        ),
        "cycle_counts": {
            "unlabelled_rooted": len(cycles),
            "leaf_labelled_rooted": len(items),
            "leaf_labelled_semi_directed": len(semi_groups),
            "rooted_presentations_per_semi_directed_topology": 4,
            "generic_jc_dimension": 7,
        },
        "theta_dimension_seven_components": sorted(dimension_seven),
        "exact_cycle_signature_classes": len(signature_groups),
        "exact_cycle_signature_classes_matching_Psi": len(signature_groups),
        "cycle_signature_classes_matching_any_other_theta_component": 0,
        "direct_C_root_insertions_checked": len(insertion_records) * 2,
        "inserted_theta_items": len(inserted_theta_items),
        "contextual_C_root_argument": (
            "equality of the complete two-state port tensor is preserved by "
            "contraction with an arbitrary common downstream two-port tensor, "
            "even when the two continuations reconnect inside one blob"
        ),
        "combined_Psi_components": combined_components,
        "cycle_networks": cycle_records,
        "insertion_records": insertion_records,
        "conclusion": (
            "the 12 former Psi components are exactly C_root expansions of "
            "the 12 labelled semi-directed root cycles; each combined JC "
            "class has eight rooted and five semi-directed topologies, and "
            "no other cycle--theta bowtie collision occurs"
        ),
    }


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
                "status": certificate["status"],
                "cycle_counts": certificate["cycle_counts"],
                "theta_dimension_seven_components": certificate[
                    "theta_dimension_seven_components"
                ],
                "direct_C_root_insertions_checked": certificate[
                    "direct_C_root_insertions_checked"
                ],
                "combined_component_count": len(
                    certificate["combined_Psi_components"]
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
