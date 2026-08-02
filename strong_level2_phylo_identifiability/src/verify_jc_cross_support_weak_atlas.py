#!/usr/bin/env python3
"""Exact separation of nonstrong restrictions from strong theta supports.

For a support chosen in one strong theta blob, the same labelled restriction
of a competing strong blob need not itself be strong.  This verifier
enumerates every such weak restriction with five or six outgoing labels by
supplying all omitted sink children and tree-child repairs with unobserved
dummy leaves.  Exact quartet-tensor signatures prove that no genuinely weak
restriction shares a model closure with a strong support restriction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

import numpy as np

from enumerate_four_leaf_root_theta import valid_binary_strong
from enumerate_theta_orientation_cores import (
    enumerate_cores,
    minimal_strong_repairs,
    weak_compositions,
)
from generic_fourier_network import precompute_displayed_trees
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_fully_labelled_support_atlas import (
    CUBE_ACTIONS,
    SELECTED_FEATURES,
    canonical_mixed_graph,
    enumerate_atlas_candidates,
    exact_type_signature,
    feature_transport,
    invariant_actions,
    observational_graph,
    outgoing_quartets,
    reduced_tensor_type,
)
from verify_jc_incoming_port_atlas import lift_network


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_cross_support_weak_atlas.json"
STRONG_CERTIFICATE = HERE / "certificates" / "jc_fully_labelled_support_atlas.json"


def build_extension(core, repair, selected_sink_subset, ordinary_counts):
    """Build one full strong extension of a possibly weak selected pattern."""

    vertices = dict(core["vertex_types"])
    edges = []
    selected_parents = []
    dummy_parents = []
    occupied = {index for index, count in enumerate(ordinary_counts) if count}
    for segment_index, (segment, count) in enumerate(
        zip(core["directed_segments"], ordinary_counts)
    ):
        chain = [segment["tail"]]
        for port_index in range(count):
            vertex = f"P{segment_index}_{port_index}"
            vertices[vertex] = "T"
            selected_parents.append(vertex)
            chain.append(vertex)
        if segment_index in repair and segment_index not in occupied:
            vertex = f"D{segment_index}"
            vertices[vertex] = "T"
            dummy_parents.append(vertex)
            chain.append(vertex)
        chain.append(segment["head"])
        edges.extend(zip(chain, chain[1:]))

    sinks = tuple(
        sorted(vertex for vertex, color in vertices.items() if color == "X")
    )
    for sink_index, sink in enumerate(sinks):
        if sink_index in selected_sink_subset:
            selected_parents.append(sink)
        else:
            dummy_parents.append(sink)

    selected_leaves = []
    all_leaves = []
    for index, parent in enumerate(selected_parents):
        leaf = f"L{index}"
        vertices[leaf] = "L"
        edges.append((parent, leaf))
        selected_leaves.append(leaf)
        all_leaves.append(leaf)
    for index, parent in enumerate(dummy_parents):
        leaf = f"Z{index}"
        vertices[leaf] = "L"
        edges.append((parent, leaf))
        all_leaves.append(leaf)

    assert valid_binary_strong(vertices, tuple(edges))
    lifted = lift_network(
        {
            "vertices": vertices,
            "edges": tuple(edges),
            "leaves": tuple(all_leaves),
        }
    )
    selected_map = {
        leaf: label for label, leaf in enumerate(selected_leaves, 1)
    }
    selected_map["LIN"] = len(selected_leaves) + 1
    return lifted, selected_map


def weak_reduced_tensor_type(network, selected_map, quartet):
    edges = tuple(network["edges"])
    global_to_leaf = {label: leaf for leaf, label in selected_map.items()}
    leaf_labels = {
        global_to_leaf[global_label]: local_label
        for local_label, global_label in enumerate(quartet, 1)
    }
    reticulations, trees = precompute_displayed_trees(
        network["vertices"], edges, leaf_labels
    )
    assert len(reticulations) == 2 and len(trees) == 4
    signatures = []
    for edge_index in range(len(edges)):
        values = []
        for _choices, selected, descendants in trees:
            if edge_index not in selected:
                values.append(0)
                continue
            mask = 0
            for local_label in descendants[edge_index]:
                mask |= 1 << (local_label - 1)
            values.append(mask)
        if any(values):
            signatures.append(tuple(values))
    signatures = tuple(sorted(set(signatures)))
    return min(
        tuple(
            sorted(
                tuple(signature[index] for index in action)
                for signature in signatures
            )
        )
        for action in CUBE_ACTIONS
    )


def selected_pattern_is_strong(core, selected_sinks, ordinary_counts):
    sink_count = sum(color == "X" for color in core["vertex_types"].values())
    occupied = {
        index for index, count in enumerate(ordinary_counts) if count
    }
    repairs = minimal_strong_repairs(
        core["vertex_types"], core["directed_segments"]
    )
    return (
        len(selected_sinks) == sink_count
        and any(set(repair) <= occupied for repair in repairs)
    )


def enumerate_weak_presentations(outgoing_count):
    """Every selected occupancy that has a full strong extension."""

    _raw, cores = enumerate_cores()
    presentations = []
    for core_index, core in enumerate(cores):
        sinks = tuple(
            sorted(
                vertex
                for vertex, color in core["vertex_types"].items()
                if color == "X"
            )
        )
        repairs = minimal_strong_repairs(
            core["vertex_types"], core["directed_segments"]
        )
        for sink_count in range(len(sinks) + 1):
            for selected_sinks in combinations(range(len(sinks)), sink_count):
                ordinary_count = outgoing_count - sink_count
                for counts in weak_compositions(
                    ordinary_count, len(core["directed_segments"])
                ):
                    decks = []
                    extensions = []
                    for repair in repairs:
                        network, selected_map = build_extension(
                            core, repair, selected_sinks, counts
                        )
                        deck = tuple(
                            weak_reduced_tensor_type(network, selected_map, quartet)
                            for quartet in outgoing_quartets(outgoing_count)
                        )
                        decks.append(deck)
                        extensions.append((repair, network, selected_map))
                    # Dummy subdivisions on omitted repair segments enter only
                    # through the same edge-product parameters.
                    assert len(set(decks)) == 1
                    repair, network, selected_map = extensions[0]
                    presentations.append(
                        {
                            "core_index": core_index,
                            "selected_sink_indices": tuple(selected_sinks),
                            "ordinary_counts": tuple(counts),
                            "chosen_dummy_repair": tuple(repair),
                            "network": network,
                            "selected_map": selected_map,
                            "deck": decks[0],
                            "selected_pattern_is_strong": selected_pattern_is_strong(
                                core, selected_sinks, counts
                            ),
                        }
                    )
    return tuple(presentations)


def bit_tuple(text):
    return tuple(character == "1" for character in text)


def generate_certificate():
    strong_certificate = json.loads(STRONG_CERTIFICATE.read_text())
    assert strong_certificate["exact_selected_signature_classes"] == 19500
    inherited_types = {
        tuple(tuple(value) for value in record["edge_descendant_signatures"]):
        bit_tuple(record["exact_sixty_invariant_signature"])
        for record in strong_certificate["tensor_types"]
    }
    assert len(inherited_types) == 90

    _raw_cores, cores = enumerate_cores()
    weak_presentations = {
        count: enumerate_weak_presentations(count) for count in (5, 6)
    }
    assert {count: len(items) for count, items in weak_presentations.items()} == {
        5: 1512,
        6: 2856,
    }
    weak_types = {
        tensor_type
        for presentations in weak_presentations.values()
        for presentation in presentations
        for tensor_type in presentation["deck"]
    }
    new_types = tuple(sorted(weak_types - set(inherited_types)))
    assert len(weak_types) == 50 and len(new_types) == 40
    contexts = {}
    type_signatures = dict(inherited_types)
    for type_index, tensor_type in enumerate(new_types):
        type_signatures[tensor_type] = exact_type_signature(tensor_type, contexts)
        if (type_index + 1) % 10 == 0:
            print("exact new weak tensor types", type_index + 1, "/ 40", flush=True)
    assert len(type_signatures) == 130

    _raw, strong_candidates, _old_count = enumerate_atlas_candidates()
    actions = invariant_actions()
    permutations_by_count = {
        count: tuple(permutations(range(1, count + 1))) for count in (5, 6)
    }
    transports = {
        (count, index): np.asarray(
            feature_transport(count, relabelling, actions), dtype=np.int32
        )
        for count in (5, 6)
        for index, relabelling in enumerate(permutations_by_count[count])
    }

    strong_signatures = {}
    strong_selected_signatures = set()
    for outgoing_count in (5, 6):
        indices = [
            index
            for index, candidate in enumerate(strong_candidates)
            if len(candidate["labels"]) - 1 == outgoing_count
        ]
        base = []
        for candidate_index in indices:
            candidate = strong_candidates[candidate_index]
            bits = []
            for quartet in outgoing_quartets(outgoing_count):
                bits.extend(
                    type_signatures[reduced_tensor_type(candidate, quartet)]
                )
            base.append(bits)
        base = np.asarray(base, dtype=np.uint8)
        for permutation_index in range(len(permutations_by_count[outgoing_count])):
            transport = transports[(outgoing_count, permutation_index)]
            transported = base[:, transport]
            packed = np.packbits(transported, axis=1)
            selected = np.packbits(
                transported[:, SELECTED_FEATURES[outgoing_count]], axis=1
            )
            for row, candidate_index in enumerate(indices):
                strong_signatures.setdefault(
                    (outgoing_count, packed[row].tobytes()),
                    (candidate_index, permutation_index),
                )
                strong_selected_signatures.add(
                    (outgoing_count, selected[row].tobytes())
                )
    assert len(strong_signatures) == len(strong_selected_signatures) == 19500

    sorted_types = tuple(sorted(type_signatures))
    type_index = {
        tensor_type: index for index, tensor_type in enumerate(sorted_types)
    }
    summaries = {}
    deck_records = []
    for outgoing_count in (5, 6):
        presentations = weak_presentations[outgoing_count]
        deck_members = defaultdict(list)
        for presentation_index, presentation in enumerate(presentations):
            deck_members[presentation["deck"]].append(presentation_index)
        expected_decks = 427 if outgoing_count == 5 else 1027
        assert len(deck_members) == expected_decks
        deck_status = {}
        for deck, members in deck_members.items():
            statuses = {
                presentations[index]["selected_pattern_is_strong"]
                for index in members
            }
            assert len(statuses) == 1
            deck_status[deck] = next(iter(statuses))

        decks = tuple(sorted(deck_members))
        base = np.asarray(
            [
                [
                    bit
                    for tensor_type in deck
                    for bit in type_signatures[tensor_type]
                ]
                for deck in decks
            ],
            dtype=np.uint8,
        )
        weak_signature_statuses = defaultdict(set)
        intersections = set()
        for permutation_index in range(len(permutations_by_count[outgoing_count])):
            transport = transports[(outgoing_count, permutation_index)]
            packed = np.packbits(base[:, transport], axis=1)
            for row, deck in enumerate(decks):
                signature = packed[row].tobytes()
                weak_signature_statuses[signature].add(deck_status[deck])
                if (outgoing_count, signature) in strong_signatures:
                    intersections.add(signature)

        expected = {
            5: {
                "weak_signatures": 16470,
                "strong_only_signatures": 8520,
                "weak_only_signatures": 7950,
                "intersections": 8520,
                "intersecting_presentations": 12720,
            },
            6: {
                "weak_signatures": 218205,
                "strong_only_signatures": 127260,
                "weak_only_signatures": 90945,
                "intersections": 10980,
                "intersecting_presentations": 43920,
            },
        }[outgoing_count]
        assert len(weak_signature_statuses) == expected["weak_signatures"]
        status_counter = Counter(
            tuple(sorted(statuses)) for statuses in weak_signature_statuses.values()
        )
        assert status_counter == {
            (True,): expected["strong_only_signatures"],
            (False,): expected["weak_only_signatures"],
        }
        assert len(intersections) == expected["intersections"]
        assert {
            tuple(sorted(weak_signature_statuses[signature]))
            for signature in intersections
        } == {(True,)}

        source_code_cache = {}
        target_checks = 0
        non_T_targets = []
        for presentation_index, presentation in enumerate(presentations):
            if not presentation["selected_pattern_is_strong"]:
                continue
            core = cores[presentation["core_index"]]
            occupied = {
                index
                for index, count in enumerate(presentation["ordinary_counts"])
                if count
            }
            repairs = minimal_strong_repairs(
                core["vertex_types"], core["directed_segments"]
            )
            contained = [repair for repair in repairs if set(repair) <= occupied]
            assert contained
            network, selected_map = build_extension(
                core,
                contained[0],
                presentation["selected_sink_indices"],
                presentation["ordinary_counts"],
            )
            assert len(network["leaves"]) == outgoing_count + 1
            target_candidate = {
                "network": network,
                "labels": tuple(selected_map[leaf] for leaf in network["leaves"]),
            }
            base_bits = np.asarray(
                [
                    bit
                    for tensor_type in presentation["deck"]
                    for bit in type_signatures[tensor_type]
                ],
                dtype=np.uint8,
            )
            for permutation_index, relabelling in enumerate(
                permutations_by_count[outgoing_count]
            ):
                signature = np.packbits(
                    base_bits[transports[(outgoing_count, permutation_index)]]
                ).tobytes()
                source_key = (outgoing_count, signature)
                if source_key not in strong_signatures:
                    continue
                target_checks += 1
                source_item = strong_signatures[source_key]
                if source_item not in source_code_cache:
                    source_index, source_permutation = source_item
                    source_code_cache[source_item] = canonical_mixed_graph(
                        observational_graph(
                            strong_candidates[source_index],
                            permutations_by_count[outgoing_count][source_permutation],
                        )
                    )
                target_code = canonical_mixed_graph(
                    observational_graph(target_candidate, relabelling)
                )
                if target_code != source_code_cache[source_item]:
                    non_T_targets.append(
                        (presentation_index, permutation_index, source_item)
                    )
        assert target_checks == expected["intersecting_presentations"]
        assert not non_T_targets

        status_counts = Counter(deck_status.values())
        expected_status = {5: {False: 335, True: 92}, 6: {False: 794, True: 233}}
        assert status_counts == expected_status[outgoing_count]
        summaries[str(outgoing_count)] = {
            "role_presentations": len(presentations),
            "distinct_base_tensor_decks": len(decks),
            "base_decks_by_selected_strong_status": {
                str(status).lower(): count
                for status, count in sorted(status_counts.items())
            },
            "all_label_exact_signatures": len(weak_signature_statuses),
            "signatures_from_selected_strong_patterns": expected[
                "strong_only_signatures"
            ],
            "signatures_from_genuinely_weak_patterns": expected[
                "weak_only_signatures"
            ],
            "strong_atlas_signature_intersections": len(intersections),
            "intersection_status": "selected restriction is strong",
            "intersecting_selected_strong_presentations_checked": target_checks,
            "non_T_intersecting_presentations": 0,
        }

        for deck_index, deck in enumerate(decks):
            deck_records.append(
                {
                    "outgoing_port_count": outgoing_count,
                    "deck_index": deck_index,
                    "presentation_count": len(deck_members[deck]),
                    "selected_pattern_is_strong": deck_status[deck],
                    "quartet_tensor_type_ids": [type_index[item] for item in deck],
                    "deck_sha256": sha256(repr(deck).encode()).hexdigest(),
                }
            )

    type_records = []
    for index, tensor_type in enumerate(sorted_types):
        type_records.append(
            {
                "id": index,
                "origin": "new_weak" if tensor_type in new_types else "inherited_strong",
                "edge_descendant_signatures": [list(item) for item in tensor_type],
                "exact_sixty_invariant_signature": "".join(
                    "1" if value else "0" for value in type_signatures[tensor_type]
                ),
            }
        )

    return {
        "status": {
            "cross_support_nonstrong_separation": "PROVED",
            "arbitrary_nonroot_theta_bowtie_classification": "PROVED",
            "complete_local_move_system": ["T"],
            "one_sided_containment_classification": "UNRESOLVED",
            "global_blob_tree_reconstruction": "UNRESOLVED",
        },
        "scope": (
            "all five- and six-outgoing selected restrictions induced from "
            "an arbitrary full strongly tree-child nonroot theta blob"
        ),
        "weak_role_presentations": sum(
            len(items) for items in weak_presentations.values()
        ),
        "weak_quartet_tensor_types": len(weak_types),
        "new_tensor_types_beyond_strong_support_atlas": len(new_types),
        "new_exact_symbolic_invariant_pullbacks": len(new_types)
        * len(ALL_INVARIANTS),
        "inherited_exact_symbolic_invariant_pullbacks": 90
        * len(ALL_INVARIANTS),
        "strong_exact_signature_classes_replayed": len(strong_signatures),
        "by_outgoing_port_count": summaries,
        "tensor_types": type_records,
        "new_tensor_type_ids": [type_index[item] for item in new_types],
        "base_tensor_decks": deck_records,
        "conclusion": (
            "a selected weak restriction can share a model closure with a "
            "strong support restriction only when the selected restriction "
            "is itself strong and isomorphic or T-equivalent to the source"
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
                "weak_role_presentations": certificate["weak_role_presentations"],
                "weak_quartet_tensor_types": certificate[
                    "weak_quartet_tensor_types"
                ],
                "new_exact_symbolic_invariant_pullbacks": certificate[
                    "new_exact_symbolic_invariant_pullbacks"
                ],
                "by_outgoing_port_count": certificate[
                    "by_outgoing_port_count"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
