#!/usr/bin/env python3
"""Exact JC atlas after exposing the incoming state port.

Every root-spanning four-leaf census network is placed below a new root and
given an outgroup leaf 5.  This turns the old root into the incoming
attachment vertex of a five-port level-2 blob.  Exact quartet-marginal
invariants prove that ordinary triangle redirection is the only surviving
full-dimensional ambiguity in this finite nonroot atlas.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from flint import fmpq_mpoly_ctx

from enumerate_four_leaf_root_theta import (
    canonical_code,
    enumerate_networks,
    valid_binary_strong,
)
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from jc_root_spanning_atlas_data import INVARIANT_TEMPLATES
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_root_spanning_atlas import (
    DisjointSet,
    canonical_colored_graph,
    fraction_free_rank,
    invariant_orbit,
    is_triangle_redirection,
    move_components,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_incoming_port_atlas.json"

# The modular probe found four minimum two-template certificates.  Templates
# 2 and 4 minimize the total number of relabelled pullbacks (60) and avoid
# degree five.
SELECTED_TEMPLATE_INDICES = (2, 4)
EXPECTED_DIMENSIONS = (
    11, 11, 11, 11, 10, 11, 10, 11, 10, 11, 11, 11, 11, 10,
    10, 10, 11, 11, 10, 10, 11, 11, 11, 11, 11, 11, 11,
)


def canonical_character_orbit(assignment):
    return min(
        tuple(
            {0: 0, 1: permutation[0], 2: permutation[1], 3: permutation[2]}[
                value
            ]
            for value in assignment
        )
        for permutation in permutations((1, 2, 3))
    )


JC5_REPRESENTATIVES = tuple(
    sorted(
        {
            canonical_character_orbit(
                first + (first[0] ^ first[1] ^ first[2] ^ first[3],)
            )
            for first in product(range(4), repeat=4)
        }
    )
)
JC5_INDEX = {
    assignment: JC5_REPRESENTATIVES.index(canonical_character_orbit(assignment))
    for assignment in (
        first + (first[0] ^ first[1] ^ first[2] ^ first[3],)
        for first in product(range(4), repeat=4)
    )
}
assert len(JC5_REPRESENTATIVES) == 51


def lift_network(network):
    """Expose the old root as a nonroot incoming attachment vertex."""
    rename = lambda vertex: "IN" if vertex == "S" else vertex
    vertices = {
        rename(vertex): ("T" if vertex == "S" else color)
        for vertex, color in network["vertices"].items()
    }
    vertices.update({"S": "S", "LIN": "L"})
    edges = [
        (rename(tail), rename(head)) for tail, head in network["edges"]
    ] + [("S", "IN"), ("S", "LIN")]
    leaves = tuple(rename(vertex) for vertex in network["leaves"]) + ("LIN",)
    lifted = {"vertices": vertices, "edges": tuple(edges), "leaves": leaves}
    assert valid_binary_strong(vertices, tuple(edges))
    return lifted


def coordinate_permutation5(position_to_label):
    answer = []
    for assignment in JC5_REPRESENTATIVES:
        by_position = [0] * 5
        for position, label in enumerate(position_to_label):
            by_position[position] = assignment[label - 1]
        answer.append(JC5_INDEX[tuple(by_position)])
    assert sorted(answer) == list(range(51))
    return tuple(answer)


def quartet_coordinate_indices(omitted):
    retained = tuple(label for label in range(1, 6) if label != omitted)
    answer = []
    for assignment in JC_REPRESENTATIVES:
        full = [0] * 5
        for label, character in zip(retained, assignment):
            full[label - 1] = character
        answer.append(JC5_INDEX[tuple(full)])
    return tuple(answer)


class LiftedExactModels:
    def __init__(self, networks):
        self.networks = networks
        self.base = {}

    def coordinates(self, item):
        network_index, labels = item
        if network_index not in self.base:
            network = lift_network(self.networks[network_index])
            reticulations = reticulation_vertices(network["vertices"])
            context = fmpq_mpoly_ctx.get(
                [f"incoming_n{network_index}_p{index}" for index in range(15)]
            )
            parameters = context.gens()
            # The two new root edges occur only through their product under a
            # uniform reversible root distribution.  Fix S->IN to one and use
            # parameter 12 for the effective incoming/outgroup multiplier.
            edge_parameters = parameters[:12] + (
                context.constant(1),
                parameters[12],
            )
            coordinates = evaluate_jc_coordinates(
                network["vertices"],
                network["edges"],
                dict(zip(network["leaves"], range(1, 6))),
                JC5_REPRESENTATIVES,
                edge_parameters,
                dict(zip(reticulations, parameters[13:])),
            )
            self.base[network_index] = (context, coordinates)
        context, base = self.base[network_index]
        permutation = coordinate_permutation5(labels + (5,))
        return context, tuple(base[index] for index in permutation)


def lifted_topology_components(networks, root_topology):
    items = root_topology["items"]
    graphs = []
    rooted_codes = []
    for network_index, labels in items:
        network = lift_network(networks[network_index])
        complete_labels = labels + (5,)
        graphs.append(semi_directed_graph(network, complete_labels))
        rooted_codes.append(
            canonical_code(
                network["vertices"],
                network["edges"],
                dict(zip(network["leaves"], complete_labels)),
            )
        )
    assert len(set(rooted_codes)) == 612
    assert len({canonical_colored_graph(graph) for graph in graphs}) == 612

    disjoint = DisjointSet(len(items))
    underlying_groups = defaultdict(list)
    for index, graph in enumerate(graphs):
        underlying_groups[
            canonical_colored_graph(
                graph, ignore_internal=True, ignore_edge_type=True
            )
        ].append(index)
    triangle_edges = []
    for group in underlying_groups.values():
        for first, second in combinations(group, 2):
            if is_triangle_redirection(graphs[first], graphs[second]):
                disjoint.union(first, second)
                triangle_edges.append((first, second))
    assert len(triangle_edges) == 96

    components = defaultdict(list)
    for index in range(len(items)):
        components[disjoint.find(index)].append(index)
    components = tuple(
        sorted(
            (tuple(sorted(component)) for component in components.values()),
            key=lambda component: items[component[0]],
        )
    )
    assert len(components) == 516
    assert Counter(map(len, components)) == {1: 420, 2: 96}

    root_item_to_component = {
        item: component_index
        for component_index, component in enumerate(root_topology["components"])
        for item in component
    }
    for component in components:
        assert len({root_item_to_component[items[index]] for index in component}) == 1
    return {
        "graphs": graphs,
        "components": components,
        "triangle_edges": tuple(triangle_edges),
        "root_item_to_component": root_item_to_component,
    }


def symbolic_lifted_rank(network_index, network):
    network = lift_network(network)
    reticulations = reticulation_vertices(network["vertices"])
    context = fmpq_mpoly_ctx.get(
        [f"incoming_rank_n{network_index}_p{index}" for index in range(10)]
    )
    parameters = context.gens()
    one = context.constant(1)
    # Eight internal edges, four normalized outgoing pendant edges, and two
    # normalized new-root edges.
    edge_parameters = parameters[:8] + (one,) * 6
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        network["edges"],
        dict(zip(network["leaves"], range(1, 6))),
        JC5_REPRESENTATIVES,
        edge_parameters,
        dict(zip(reticulations, parameters[8:])),
    )
    tangent = []
    for assignment, coordinate in zip(JC5_REPRESENTATIVES[1:], coordinates[1:]):
        row = [coordinate.derivative(index) for index in range(10)]
        row.extend(
            int(assignment[leaf] != 0) * coordinate for leaf in range(5)
        )
        tangent.append(row)
    rank, pivots = fraction_free_rank(tangent)
    return {
        "rank": rank,
        "last_pivot_sha256": sha256(str(pivots[-1]).encode()).hexdigest(),
    }


def bit_string(values):
    return "".join("1" if value else "0" for value in values)


def generate_certificate():
    _raw, networks = enumerate_networks()
    root_topology = move_components(networks)
    items = root_topology["items"]
    topology = lifted_topology_components(networks, root_topology)
    components = topology["components"]

    ranks = []
    for network_index, network in enumerate(networks):
        rank = symbolic_lifted_rank(network_index, network)
        assert rank["rank"] == EXPECTED_DIMENSIONS[network_index]
        ranks.append(rank)

    selected_orbits = tuple(
        invariant_orbit(INVARIANT_TEMPLATES[index])
        for index in SELECTED_TEMPLATE_INDICES
    )
    assert tuple(map(len, selected_orbits)) == (3, 12)
    selected_invariants = tuple(
        invariant for orbit in selected_orbits for invariant in orbit
    )
    quartet_indices = {
        omitted: quartet_coordinate_indices(omitted) for omitted in range(1, 5)
    }
    models = LiftedExactModels(networks)

    item_signatures = {}
    for item in items:
        context, coordinates = models.coordinates(item)
        signature = []
        for omitted in range(1, 5):
            quartet = tuple(coordinates[index] for index in quartet_indices[omitted])
            for invariant in selected_invariants:
                # Reuse the root-atlas exact substitution engine with a small
                # adapter exposing these quartet coordinates.
                answer = context.constant(0)
                for monomial, coefficient in invariant:
                    term = context.constant(coefficient)
                    for coordinate in monomial:
                        term *= quartet[coordinate]
                    answer += term
                signature.append(bool(answer))
        item_signatures[item] = tuple(signature)
    assert {len(signature) for signature in item_signatures.values()} == {60}

    component_signatures = []
    component_dimensions = []
    component_root_ids = []
    for component in components:
        signatures = {item_signatures[items[index]] for index in component}
        assert len(signatures) == 1
        component_signatures.append(next(iter(signatures)))
        dimensions = {EXPECTED_DIMENSIONS[items[index][0]] for index in component}
        assert len(dimensions) == 1
        component_dimensions.append(next(iter(dimensions)))
        root_ids = {
            topology["root_item_to_component"][items[index]] for index in component
        }
        assert len(root_ids) == 1
        component_root_ids.append(next(iter(root_ids)))
    assert len(set(component_signatures)) == 516

    same_dimension_pairs = 0
    for first, second in combinations(range(len(components)), 2):
        if component_dimensions[first] == component_dimensions[second]:
            same_dimension_pairs += 1
            assert component_signatures[first] != component_signatures[second]

    directed_total = 0
    directed_rejected = 0
    directed_unresolved = []
    for lower in range(len(components)):
        for higher in range(len(components)):
            if component_dimensions[lower] >= component_dimensions[higher]:
                continue
            directed_total += 1
            rejected = any(
                low and not high
                for low, high in zip(
                    component_signatures[lower], component_signatures[higher]
                )
            )
            if rejected:
                directed_rejected += 1
            else:
                directed_unresolved.append((lower, higher))
    assert (directed_total, directed_rejected, len(directed_unresolved)) == (
        40320,
        39168,
        1152,
    )

    records = []
    for component_id, component in enumerate(components):
        records.append(
            {
                "id": component_id,
                "dimension": component_dimensions[component_id],
                "root_marginal_component": component_root_ids[component_id],
                "signature": bit_string(component_signatures[component_id]),
                "members": [
                    {
                        "network_index": items[index][0],
                        "outgoing_port_labels": list(items[index][1]),
                        "incoming_leaf_label": 5,
                    }
                    for index in component
                ],
            }
        )

    network_records = []
    for network_index, network in enumerate(networks):
        lifted = lift_network(network)
        network_records.append(
            {
                "index": network_index,
                "vertices": dict(sorted(lifted["vertices"].items())),
                "edges": [list(edge) for edge in lifted["edges"]],
                "leaves": list(lifted["leaves"]),
                "generic_jc_dimension": EXPECTED_DIMENSIONS[network_index],
                "rank_last_pivot_sha256": ranks[network_index][
                    "last_pivot_sha256"
                ],
            }
        )

    signature_serialization = "\n".join(
        bit_string(signature) for signature in component_signatures
    )
    t_index_pairs = Counter(
        tuple(sorted((items[first][0], items[second][0])))
        for first, second in topology["triangle_edges"]
    )
    assert t_index_pairs == {
        (4, 13): 24,
        (6, 14): 24,
        (8, 15): 24,
        (18, 19): 24,
    }
    return {
        "status": {
            "finite_incoming_port_bowtie_classification": "PROVED",
            "complete_move_system": ["T"],
            "one_sided_containment_classification": "UNRESOLVED",
        },
        "scope": (
            "incoming-port lifts of all 612 root-spanning simple four-leaf "
            "census networks, with incoming block represented by leaf 5"
        ),
        "five_leaf_jc_character_orbits": len(JC5_REPRESENTATIVES),
        "lifted_rooted_topologies": 612,
        "lifted_semi_directed_topologies": 612,
        "triangle_redirection_edges": len(topology["triangle_edges"]),
        "triangle_redirection_index_pairs": {
            f"{first}-{second}": count
            for (first, second), count in sorted(t_index_pairs.items())
        },
        "observational_components": len(components),
        "component_size_distribution": dict(
            sorted(Counter(map(len, components)).items())
        ),
        "component_dimension_distribution": dict(
            sorted(Counter(component_dimensions).items())
        ),
        "unlabelled_network_dimensions": list(EXPECTED_DIMENSIONS),
        "unlabelled_dimension_distribution": dict(
            sorted(Counter(EXPECTED_DIMENSIONS).items())
        ),
        "selected_root_invariant_templates": list(SELECTED_TEMPLATE_INDICES),
        "selected_template_degrees": [3, 4],
        "selected_template_supports": [18, 19],
        "selected_template_orbit_sizes": [3, 12],
        "incoming_quartets": [
            [label for label in range(1, 6) if label != omitted]
            for omitted in range(1, 5)
        ],
        "exact_quartet_pullbacks_per_model": 60,
        "component_signature_sha256": sha256(
            signature_serialization.encode()
        ).hexdigest(),
        "same_dimension_component_pairs_separated": same_dimension_pairs,
        "lower_to_higher_component_pairs": directed_total,
        "directed_containments_rejected_by_quartet_templates": directed_rejected,
        "directed_containments_unresolved": len(directed_unresolved),
        "unresolved_directed_component_pairs": [
            list(pair) for pair in directed_unresolved
        ],
        "networks": network_records,
        "components": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = generate_certificate()
    certificate = json.loads(json.dumps(certificate, sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n"
        )
    else:
        assert CERTIFICATE.exists(), f"missing certificate: {CERTIFICATE}"
        assert certificate == json.loads(CERTIFICATE.read_text())
    summary_keys = (
        "lifted_rooted_topologies",
        "lifted_semi_directed_topologies",
        "triangle_redirection_edges",
        "observational_components",
        "component_size_distribution",
        "unlabelled_network_dimensions",
        "selected_root_invariant_templates",
        "exact_quartet_pullbacks_per_model",
        "same_dimension_component_pairs_separated",
        "directed_containments_rejected_by_quartet_templates",
        "directed_containments_unresolved",
    )
    print(
        json.dumps(
            {key: certificate[key] for key in summary_keys},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
