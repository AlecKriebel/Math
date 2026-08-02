#!/usr/bin/env python3
"""Exact JC classification of every theta support plus two probe ports.

Milestone 4A reduces arbitrary ordered port chains to a support augmented by
at most two labelled probes.  This verifier enumerates all 496 such strong
nonroot topologies.  Sixteen or eighteen selected four-leaf invariant
pullbacks give 476 exact signatures; the only collisions are twenty ordinary
triangle-redirection pairs.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from flint import fmpq_mpoly_ctx

from enumerate_four_leaf_root_theta import canonical_code, valid_binary_strong
from enumerate_theta_orientation_cores import enumerate_cores, minimal_strong_repairs
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_incoming_port_atlas import lift_network
from verify_jc_root_spanning_atlas import is_triangle_redirection


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_support_augmented_atlas.json"

# (ordered quartet of global labels, root-atlas invariant feature index)
SELECTED_FEATURES = {
    5: (
        ((1, 3, 4, 6), 16),
        ((2, 4, 5, 6), 50),
        ((2, 4, 5, 6), 59),
        ((1, 2, 3, 6), 11),
        ((1, 2, 5, 6), 27),
        ((1, 4, 5, 6), 36),
        ((1, 3, 5, 6), 18),
        ((2, 3, 4, 6), 37),
        ((1, 2, 4, 6), 38),
        ((2, 3, 5, 6), 8),
        ((1, 3, 4, 6), 14),
        ((1, 2, 4, 6), 14),
        ((1, 3, 4, 6), 36),
        ((1, 2, 5, 6), 7),
        ((1, 3, 5, 6), 6),
        ((1, 2, 4, 6), 1),
    ),
    6: (
        ((1, 3, 5, 7), 6),
        ((1, 3, 6, 7), 6),
        ((1, 2, 5, 7), 9),
        ((1, 2, 6, 7), 10),
        ((1, 2, 3, 7), 9),
        ((1, 2, 4, 7), 9),
        ((1, 2, 5, 7), 10),
        ((1, 2, 6, 7), 9),
        ((1, 5, 6, 7), 7),
        ((2, 4, 5, 7), 7),
        ((1, 3, 5, 7), 7),
        ((2, 4, 6, 7), 7),
        ((1, 3, 6, 7), 7),
        ((2, 5, 6, 7), 7),
        ((1, 4, 5, 7), 7),
        ((2, 3, 5, 7), 7),
        ((1, 4, 6, 7), 7),
        ((2, 3, 6, 7), 7),
    ),
}


def build_labelled(core, repair, extra_segments):
    vertices = dict(core["vertex_types"])
    sink_vertices = sorted(vertex for vertex, color in vertices.items() if color == "X")
    next_label = len(sink_vertices) + 1
    repair_labels = {}
    for segment in repair:
        repair_labels[segment] = next_label
        next_label += 1
    extra_labels = tuple(range(next_label, next_label + len(extra_segments)))
    labels_by_segment = defaultdict(list)
    for segment, label in repair_labels.items():
        labels_by_segment[segment].append(label)
    for segment, label in zip(extra_segments, extra_labels):
        labels_by_segment[segment].append(label)

    segment_orders = tuple(
        tuple(permutations(labels_by_segment[segment]))
        for segment in range(len(core["directed_segments"]))
    )
    for orders in product(*segment_orders):
        local_vertices = dict(vertices)
        local_edges = []
        leaf_parents = {}
        words = []
        for segment_index, (segment, word) in enumerate(
            zip(core["directed_segments"], orders)
        ):
            words.append(tuple(word))
            chain = [segment["tail"]]
            for label in word:
                vertex = f"P{label}"
                local_vertices[vertex] = "T"
                leaf_parents[label] = vertex
                chain.append(vertex)
            chain.append(segment["head"])
            local_edges.extend(zip(chain, chain[1:]))
        for label, sink in enumerate(sink_vertices, 1):
            leaf_parents[label] = sink
        leaves = []
        for label in sorted(leaf_parents):
            leaf = f"L{label}"
            local_vertices[leaf] = "L"
            local_edges.append((leaf_parents[label], leaf))
            leaves.append(leaf)
        yield (
            {
                "vertices": local_vertices,
                "edges": tuple(local_edges),
                "leaves": tuple(leaves),
            },
            tuple(range(1, len(leaves) + 1)),
            repair_labels,
            extra_labels,
            tuple(words),
        )


def enumerate_candidates():
    _raw, cores = enumerate_cores()
    candidates = {}
    raw = 0
    for core_index, core in enumerate(cores):
        repairs = minimal_strong_repairs(core["vertex_types"], core["directed_segments"])
        for repair in repairs:
            segment_count = len(core["directed_segments"])
            for extra_segments in product(range(segment_count), repeat=2):
                for base, labels, repair_labels, extra_labels, words in build_labelled(
                    core, repair, extra_segments
                ):
                    raw += 1
                    assert valid_binary_strong(base["vertices"], base["edges"])
                    lifted = lift_network(base)
                    assert valid_binary_strong(lifted["vertices"], lifted["edges"])
                    complete_labels = labels + (len(labels) + 1,)
                    code = canonical_code(
                        lifted["vertices"],
                        lifted["edges"],
                        dict(zip(lifted["leaves"], complete_labels)),
                    )
                    candidates.setdefault(
                        code,
                        {
                            "rooted_code_sha256": sha256(repr(code).encode()).hexdigest(),
                            "core_index": core_index,
                            "repair": tuple(repair),
                            "repair_labels": dict(repair_labels),
                            "extra_labels": extra_labels,
                            "extra_segments": extra_segments,
                            "segment_words": words,
                            "network": lifted,
                            "labels": complete_labels,
                        },
                    )
    return raw, tuple(candidates[code] for code in sorted(candidates))


def selected_assignments(total_leaves, features):
    assignment_index = {}
    assignments = []
    feature_coordinate_indices = []
    for quartet, _feature_index in features:
        indices = []
        for assignment in JC_REPRESENTATIVES:
            full = [0] * total_leaves
            for label, character in zip(quartet, assignment):
                full[label - 1] = character
            full = tuple(full)
            if full not in assignment_index:
                assignment_index[full] = len(assignments)
                assignments.append(full)
            indices.append(assignment_index[full])
        feature_coordinate_indices.append(tuple(indices))
    return tuple(assignments), tuple(feature_coordinate_indices)


def exact_signature(candidate, context, parameters, assignments, coordinate_indices):
    network = candidate["network"]
    edges = tuple(network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    assert len(parameters) == len(edges) + len(reticulations)
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], candidate["labels"])),
        assignments,
        parameters[: len(edges)],
        dict(zip(reticulations, parameters[len(edges) :])),
    )
    signature = []
    outgoing_count = len(candidate["labels"]) - 1
    for (_quartet, feature_index), indices in zip(
        SELECTED_FEATURES[outgoing_count], coordinate_indices
    ):
        quartet_coordinates = tuple(coordinates[index] for index in indices)
        invariant = ALL_INVARIANTS[feature_index]
        answer = context.constant(0)
        for monomial, coefficient in invariant:
            term = context.constant(coefficient)
            for coordinate in monomial:
                term *= quartet_coordinates[coordinate]
            answer += term
        signature.append(bool(answer))
    return tuple(signature)


def bit_string(signature):
    return "".join("1" if value else "0" for value in signature)


def generate_certificate():
    raw, candidates = enumerate_candidates()
    assert raw == 624
    assert len(candidates) == 496
    assert Counter(candidate["core_index"] for candidate in candidates) == {
        0: 112,
        1: 216,
        2: 56,
        3: 112,
    }
    assert Counter(len(candidate["labels"]) - 1 for candidate in candidates) == {
        5: 280,
        6: 216,
    }

    contexts = {}
    assignment_data = {}
    for outgoing_count in (5, 6):
        total_leaves = outgoing_count + 1
        assignments, indices = selected_assignments(
            total_leaves, SELECTED_FEATURES[outgoing_count]
        )
        parameter_count = 2 * total_leaves + 6
        context = fmpq_mpoly_ctx.get(
            [f"support_n{total_leaves}_p{index}" for index in range(parameter_count)]
        )
        contexts[outgoing_count] = (context, context.gens())
        assignment_data[outgoing_count] = (assignments, indices)

    signatures = []
    for candidate in candidates:
        outgoing_count = len(candidate["labels"]) - 1
        context, parameters = contexts[outgoing_count]
        assignments, indices = assignment_data[outgoing_count]
        signatures.append(
            exact_signature(candidate, context, parameters, assignments, indices)
        )

    groups = defaultdict(list)
    for index, (candidate, signature) in enumerate(zip(candidates, signatures)):
        groups[(len(candidate["labels"]) - 1, signature)].append(index)
    groups = tuple(
        tuple(group)
        for _key, group in sorted(groups.items(), key=lambda record: record[1][0])
    )
    assert len(groups) == 476
    assert Counter(map(len, groups)) == {1: 456, 2: 20}

    t_pairs = []
    for group in groups:
        if len(group) == 1:
            continue
        first, second = group
        first_graph = semi_directed_graph(
            candidates[first]["network"], candidates[first]["labels"]
        )
        second_graph = semi_directed_graph(
            candidates[second]["network"], candidates[second]["labels"]
        )
        assert is_triangle_redirection(first_graph, second_graph)
        t_pairs.append((first, second))
    assert len(t_pairs) == 20

    network_records = []
    for index, (candidate, signature) in enumerate(zip(candidates, signatures)):
        network = candidate["network"]
        network_records.append(
            {
                "index": index,
                "rooted_code_sha256": candidate["rooted_code_sha256"],
                "core_index": candidate["core_index"],
                "minimal_repair_segments": list(candidate["repair"]),
                "repair_labels_by_segment": {
                    str(segment): label
                    for segment, label in sorted(candidate["repair_labels"].items())
                },
                "extra_probe_labels": list(candidate["extra_labels"]),
                "extra_probe_segments": list(candidate["extra_segments"]),
                "segment_words": [list(word) for word in candidate["segment_words"]],
                "outgoing_port_count": len(candidate["labels"]) - 1,
                "incoming_port_label": candidate["labels"][-1],
                "selected_signature": bit_string(signature),
                "vertices": dict(sorted(network["vertices"].items())),
                "edges": [list(edge) for edge in network["edges"]],
                "leaves": list(network["leaves"]),
            }
        )

    component_records = []
    for component_index, group in enumerate(groups):
        component_records.append(
            {
                "id": component_index,
                "candidate_indices": list(group),
                "outgoing_port_count": len(candidates[group[0]]["labels"]) - 1,
                "signature": bit_string(signatures[group[0]]),
                "relation": "T" if len(group) == 2 else "singleton",
            }
        )

    return {
        "status": {
            "support_augmented_bowtie_classification": "PROVED",
            "complete_move_system": ["T"],
            "one_sided_containment_classification": "UNRESOLVED",
        },
        "scope": (
            "all strong nonroot theta restrictions consisting of a minimal "
            "core-preserving labelled support plus two labelled probe ports"
        ),
        "raw_support_probe_presentations": raw,
        "labelled_rooted_topologies": len(candidates),
        "candidate_core_distribution": dict(
            sorted(Counter(candidate["core_index"] for candidate in candidates).items())
        ),
        "candidate_outgoing_port_distribution": dict(
            sorted(Counter(len(candidate["labels"])-1 for candidate in candidates).items())
        ),
        "selected_features": {
            str(count): [
                {"quartet": list(quartet), "root_invariant_feature": feature}
                for quartet, feature in features
            ]
            for count, features in SELECTED_FEATURES.items()
        },
        "selected_feature_counts": {
            str(count): len(features) for count, features in SELECTED_FEATURES.items()
        },
        "exact_signature_components": len(groups),
        "component_size_distribution": dict(sorted(Counter(map(len, groups)).items())),
        "triangle_redirection_components": len(t_pairs),
        "non_triangle_signature_collisions": 0,
        "networks": network_records,
        "components": component_records,
        "conclusion": (
            "full-dimensional regular JC overlap in the complete bounded "
            "support-plus-two atlas occurs exactly under labelled isomorphism "
            "or ordinary triangle redirection"
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
                "labelled_rooted_topologies": certificate["labelled_rooted_topologies"],
                "exact_signature_components": certificate["exact_signature_components"],
                "triangle_redirection_components": certificate[
                    "triangle_redirection_components"
                ],
                "non_triangle_signature_collisions": certificate[
                    "non_triangle_signature_collisions"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
