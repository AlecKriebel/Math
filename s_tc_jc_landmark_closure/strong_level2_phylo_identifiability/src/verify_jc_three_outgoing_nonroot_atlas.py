#!/usr/bin/env python3
"""Exact JC atlas for strong nonroot theta blobs with three outgoing ports.

These are the smallest strong nonroot theta tensors: three outgoing state
ports plus one distinguished incoming port.  Reversible root relocation maps
every candidate to the certified root-spanning four-leaf atlas.  Exact graph
enumeration and strict invariant factors then classify both full-dimensional
overlap and all dimension-8-to-9 stochastic containments.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, permutations
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import (
    build_network,
    canonical_code,
    enumerate_networks,
    valid_binary_strong,
)
from enumerate_theta_orientation_cores import enumerate_cores, weak_compositions
from verify_jc_cross_root_separation import ALL_INVARIANTS, model, pullback
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_incoming_port_atlas import lift_network
from verify_jc_root_spanning_atlas import (
    canonical_colored_graph,
    is_triangle_redirection,
    item_action,
    move_components,
    triangles,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_three_outgoing_nonroot_atlas.json"
ROOT_CERTIFICATE = HERE / "certificates" / "jc_root_spanning_atlas.json"

# Representatives under the outgoing S3 action fixing incoming label 4.
# Entries are (dimension-8 root component, dimension-9 root component,
# selected strict-invariant feature).
DIRECTED_ORBITS = (
    (13, 40, 9),
    (13, 41, 8),
    (13, 46, 9),
    (13, 88, 8),
    (13, 89, 8),
    (13, 94, 9),
    (16, 40, 9),
    (16, 41, 9),
    (16, 44, 6),
    (16, 45, 10),
    (16, 46, 6),
    (16, 47, 10),
    (16, 88, 3),
    (16, 89, 3),
    (16, 92, 6),
    (16, 93, 6),
    (16, 94, 6),
    (16, 95, 6),
)


def enumerate_candidates():
    """Generate every labelled three-outgoing-port candidate exactly once."""
    _raw, cores = enumerate_cores()
    candidates = {}
    raw_expansions = 0
    for core_index, core in enumerate(cores):
        sink_count = sum(color == "X" for color in core["vertex_types"].values())
        ordinary_count = 3 - sink_count
        if ordinary_count < 0:
            continue
        segment_count = len(core["directed_segments"])
        for counts in weak_compositions(ordinary_count, segment_count):
            raw_expansions += 1
            vertices, edges, leaves = build_network(core, counts)
            if not valid_binary_strong(vertices, edges):
                continue
            base = {
                "vertices": vertices,
                "edges": tuple(edges),
                "leaves": tuple(leaves),
            }
            lifted = lift_network(base)
            assert valid_binary_strong(lifted["vertices"], lifted["edges"])
            for outgoing_labels in permutations((1, 2, 3)):
                labels = outgoing_labels + (4,)
                code = canonical_code(
                    lifted["vertices"],
                    lifted["edges"],
                    dict(zip(lifted["leaves"], labels)),
                )
                candidates.setdefault(
                    code,
                    {
                        "core_index": core_index,
                        "subdivision_counts": tuple(counts),
                        "network": lifted,
                        "labels": labels,
                    },
                )
    return raw_expansions, tuple(candidates[code] for code in sorted(candidates))


def root_item(root_certificate, component_index):
    member = root_certificate["components"][component_index]["members"][0]
    return member["network_index"], tuple(member["port_labels"])


def expected_strict_factor(parameters, orbit_index):
    b = parameters
    common_long = (
        b[0]*b[1]*b[10]**2*b[11]**2*b[12]*b[13]*b[2]*b[3]*b[4]
        *b[5]*b[6]*b[7]*b[8]**2*b[9]**2
        *(b[12]-1)*(b[13]-1)*(b[3]-1)*(b[5]-1)
        *(b[0]*b[3]-1)*(b[0]*b[5]-1)
    )
    if orbit_index in {0, 6}:
        return 2 * common_long
    if orbit_index in {2, 7, 9, 11}:
        return -2 * common_long

    pattern_b = (
        2*b[1]*b[10]*b[11]*b[12]*b[2]*b[3]*b[5]*b[7]*b[8]*b[9]
        *(b[0]-1)*(b[0]+1)*(b[13]-1)
    )
    if orbit_index in {1, 8, 10}:
        return pattern_b

    pattern_c = (
        -2*b[1]*b[10]*b[11]*b[12]*b[13]*b[2]*b[4]*b[5]*b[6]
        *b[8]*b[9]*(b[0]-1)*(b[0]+1)
    )
    if orbit_index in {3, 15, 17}:
        return pattern_c

    pattern_d = (
        2*b[0]*b[10]*b[11]*b[13]*b[3]*b[4]*b[5]*b[6]*b[8]*b[9]
        *(b[12]-1)*(b[2]-1)*(b[2]+1)
    )
    if orbit_index in {4, 14, 16}:
        return pattern_d

    if orbit_index == 5:
        convex_minus_one = b[6]*(b[12]*b[1] + (1-b[12])*b[3]) - 1
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]*b[13]*b[2]*b[3]
            *b[4]*b[5]*b[6]**2*b[7]*b[8]**2*b[9]**2
            *(b[0]-1)*(b[12]-1)*(b[13]-1)*(b[2]-1)
            *(b[0]*b[2]-1)*convex_minus_one
        )

    assert orbit_index in {12, 13}
    return (
        -2*b[0]*b[1]*b[10]*b[11]*b[12]*b[2]*b[3]*b[6]**2*b[7]
        *b[8]**2*b[9]**2*(b[12]-1)*(b[13]-1)*(b[0]*b[2]-1)**2
    )


def strict_reason(orbit_index):
    if orbit_index == 5:
        return (
            "x6*(lambda*x1+(1-lambda)*x3)-1 is strictly negative on the "
            "open cube; every other factor is nonzero there"
        )
    return (
        "all monomial factors are positive; x-1 and product-minus-one "
        "factors are strictly negative, while x+1 factors are positive"
    )


def component_action(networks, root_topology, candidate_components):
    item_to_component = {
        item: component_index
        for component_index, component in enumerate(root_topology["components"])
        for item in component
    }

    def image(component_index, permutation):
        representative = root_topology["components"][component_index][0]
        transformed = item_action(
            networks,
            root_topology["rooted_code_to_item"],
            representative,
            permutation,
        )
        result = item_to_component[transformed]
        assert result in candidate_components
        return result

    return image


def generate_certificate():
    root_certificate = json.loads(ROOT_CERTIFICATE.read_text())
    root_components = root_certificate["components"]
    raw_expansions, candidates = enumerate_candidates()
    assert raw_expansions == 42
    assert len(candidates) == 30

    _raw, root_networks = enumerate_networks()
    root_topology = move_components(root_networks)
    root_items = root_topology["items"]
    root_item_to_component = {
        item: component_index
        for component_index, component in enumerate(root_topology["components"])
        for item in component
    }
    root_graph_to_items = defaultdict(list)
    for item in root_items:
        network_index, labels = item
        graph = semi_directed_graph(root_networks[network_index], labels)
        root_graph_to_items[canonical_colored_graph(graph)].append(item)
    assert len(root_graph_to_items) == 216

    graphs = []
    graph_codes = []
    assignments = []
    triangle_counts = []
    for candidate in candidates:
        graph = semi_directed_graph(candidate["network"], candidate["labels"])
        graph_code = canonical_colored_graph(graph)
        graphs.append(graph)
        graph_codes.append(graph_code)
        triangle_counts.append(len(triangles(graph)))
        matching_root_items = root_graph_to_items[graph_code]
        assert matching_root_items
        matching_components = {
            root_item_to_component[item] for item in matching_root_items
        }
        assert len(matching_components) == 1
        assignments.append(next(iter(matching_components)))
    assert len(set(graph_codes)) == 30
    assert Counter(triangle_counts) == {1: 18, 0: 12}

    observational_groups = defaultdict(list)
    for candidate_index, component_index in enumerate(assignments):
        observational_groups[component_index].append(candidate_index)
    observational_groups = dict(sorted(observational_groups.items()))
    assert len(observational_groups) == 21
    assert Counter(map(len, observational_groups.values())) == {2: 9, 1: 12}

    triangle_edges = set()
    for first, second in combinations(range(len(candidates)), 2):
        if is_triangle_redirection(graphs[first], graphs[second]):
            triangle_edges.add((first, second))
    assert len(triangle_edges) == 9
    for group in observational_groups.values():
        if len(group) == 2:
            assert tuple(sorted(group)) in triangle_edges
        else:
            assert len(group) == 1

    candidate_components = frozenset(observational_groups)
    component_dimensions = {
        component: root_components[component]["dimension"]
        for component in candidate_components
    }
    assert Counter(component_dimensions.values()) == {8: 9, 9: 12}
    for component, group in observational_groups.items():
        expected_size = 2 if component_dimensions[component] == 8 else 1
        assert len(group) == expected_size

    image = component_action(root_networks, root_topology, candidate_components)
    outgoing_s3 = tuple(
        permutation + (4,) for permutation in permutations((1, 2, 3))
    )
    directed_pair_to_orbit = {}
    directed_orbit_sizes = []
    strict_certificates = []
    for orbit_index, (lower, higher, feature_index) in enumerate(DIRECTED_ORBITS):
        orbit = {
            (image(lower, permutation), image(higher, permutation))
            for permutation in outgoing_s3
        }
        assert len(orbit) == 6
        directed_orbit_sizes.append(len(orbit))
        for pair in orbit:
            assert pair not in directed_pair_to_orbit
            directed_pair_to_orbit[pair] = orbit_index

        low_item = root_item(root_certificate, lower)
        high_item = root_item(root_certificate, higher)
        _low_parameters, low_coordinates = model(
            root_networks, low_item, f"three{orbit_index}a"
        )
        high_parameters, high_coordinates = model(
            root_networks, high_item, f"three{orbit_index}b"
        )
        invariant = ALL_INVARIANTS[feature_index]
        low_pullback = pullback(low_coordinates, invariant)
        high_pullback = pullback(high_coordinates, invariant)
        assert low_pullback == 0
        expected = sp.factor(expected_strict_factor(high_parameters, orbit_index))
        assert sp.factor(high_pullback - expected) == 0
        strict_certificates.append(
            {
                "orbit_index": orbit_index,
                "lower_root_component": lower,
                "higher_root_component": higher,
                "feature_index": feature_index,
                "invariant_degree": len(invariant[0][0]),
                "invariant_support": len(invariant),
                "lower_representative": [low_item[0], list(low_item[1])],
                "higher_representative": [high_item[0], list(high_item[1])],
                "lower_pullback": "0",
                "higher_pullback": str(high_pullback),
                "strict_nonzero_reason": strict_reason(orbit_index),
            }
        )

    all_directed_pairs = {
        (lower, higher)
        for lower in candidate_components
        for higher in candidate_components
        if component_dimensions[lower] == 8 and component_dimensions[higher] == 9
    }
    assert len(all_directed_pairs) == 108
    assert set(directed_pair_to_orbit) == all_directed_pairs
    assert tuple(directed_orbit_sizes) == (6,) * 18

    network_records = []
    for index, (candidate, component, triangle_count) in enumerate(
        zip(candidates, assignments, triangle_counts)
    ):
        network = candidate["network"]
        network_records.append(
            {
                "index": index,
                "core_index": candidate["core_index"],
                "subdivision_counts": list(candidate["subdivision_counts"]),
                "outgoing_port_labels": list(candidate["labels"][:3]),
                "incoming_port_label": 4,
                "vertices": dict(sorted(network["vertices"].items())),
                "edges": [list(edge) for edge in network["edges"]],
                "leaves": list(network["leaves"]),
                "triangle_count": triangle_count,
                "root_atlas_component": component,
                "generic_jc_dimension": component_dimensions[component],
            }
        )

    group_records = []
    for component, group in observational_groups.items():
        group_records.append(
            {
                "root_atlas_component": component,
                "dimension": component_dimensions[component],
                "candidate_indices": list(group),
                "relation": "T" if len(group) == 2 else "singleton",
            }
        )

    return {
        "status": {
            "three_outgoing_nonroot_bowtie_classification": "PROVED",
            "three_outgoing_nonroot_one_sided_containment_classification": "PROVED",
            "complete_move_system": ["T"],
        },
        "scope": (
            "binary strongly tree-child nonroot level-2 theta blobs with "
            "exactly three outgoing ports and one distinguished incoming port"
        ),
        "raw_core_subdivision_expansions": raw_expansions,
        "labelled_rooted_candidates": len(candidates),
        "labelled_semi_directed_candidates": len(set(graph_codes)),
        "candidate_core_distribution": dict(
            sorted(Counter(candidate["core_index"] for candidate in candidates).items())
        ),
        "candidate_triangle_distribution": dict(sorted(Counter(triangle_counts).items())),
        "observational_components": len(observational_groups),
        "observational_component_size_distribution": dict(
            sorted(Counter(map(len, observational_groups.values())).items())
        ),
        "component_dimension_distribution": dict(
            sorted(Counter(component_dimensions.values()).items())
        ),
        "triangle_redirection_pairs": len(triangle_edges),
        "directed_dimension_8_to_9_pairs": len(all_directed_pairs),
        "directed_pair_orbits_under_outgoing_S3": len(DIRECTED_ORBITS),
        "directed_pair_orbit_sizes": directed_orbit_sizes,
        "strict_directed_certificates": strict_certificates,
        "one_sided_stochastic_containments": 0,
        "networks": network_records,
        "components": group_records,
        "conclusion": (
            "full-dimensional regular overlap occurs exactly for labelled "
            "isomorphism or triangle redirection; all unequal-dimensional "
            "complete open stochastic images are disjoint"
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
                "labelled_rooted_candidates": certificate["labelled_rooted_candidates"],
                "observational_components": certificate["observational_components"],
                "triangle_redirection_pairs": certificate["triangle_redirection_pairs"],
                "directed_dimension_8_to_9_pairs": certificate[
                    "directed_dimension_8_to_9_pairs"
                ],
                "one_sided_stochastic_containments": certificate[
                    "one_sided_stochastic_containments"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
