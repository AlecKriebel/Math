#!/usr/bin/env python3
"""Exact JC cycle atlas and cycle--theta cross-generator separation."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

from flint import fmpq_mpoly_ctx
import numpy as np

from enumerate_four_leaf_root_theta import canonical_code, valid_binary_strong
from generic_fourier_network import precompute_displayed_trees
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_cross_support_weak_atlas import (
    bit_tuple,
    enumerate_weak_presentations as theta_weak_presentations,
)
from verify_jc_fully_labelled_support_atlas import (
    canonical_mixed_graph,
    enumerate_atlas_candidates,
    feature_transport,
    invariant_actions,
    observational_graph,
    outgoing_quartets,
    reduced_tensor_type as theta_reduced_type,
)
from verify_jc_incoming_port_atlas import lift_network


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_cycle_cross_generator_atlas.json"
THETA_CERTIFICATE = HERE / "certificates" / "jc_cross_support_weak_atlas.json"


def build_cycle_strong(counts):
    vertices = {"S": "S", "X": "X"}
    edges = []
    parents = []
    for side, count in enumerate(counts):
        chain = ["S"]
        for index in range(count):
            vertex = f"P{side}_{index}"
            vertices[vertex] = "T"
            parents.append(vertex)
            chain.append(vertex)
        chain.append("X")
        edges.extend(zip(chain, chain[1:]))
    parents.append("X")
    leaves = []
    for index, parent in enumerate(parents):
        leaf = f"L{index}"
        vertices[leaf] = "L"
        edges.append((parent, leaf))
        leaves.append(leaf)
    assert valid_binary_strong(vertices, tuple(edges))
    return lift_network(
        {"vertices": vertices, "edges": tuple(edges), "leaves": tuple(leaves)}
    )


def cycle_role_candidates(outgoing_count):
    candidates = {}
    ordinary_count = outgoing_count - 1
    for left_count in range(ordinary_count + 1):
        counts = (left_count, ordinary_count - left_count)
        network = build_cycle_strong(counts)
        labels = tuple(range(1, outgoing_count + 2))
        code = canonical_code(
            network["vertices"],
            network["edges"],
            dict(zip(network["leaves"], labels)),
        )
        candidates.setdefault(
            code,
            {"counts": counts, "network": network, "labels": labels},
        )
    return tuple(candidates[code] for code in sorted(candidates))


def build_cycle_weak(outgoing_count, sink_selected, counts):
    vertices = {"S": "S", "X": "X"}
    edges = []
    selected_parents = []
    for side, count in enumerate(counts):
        chain = ["S"]
        for index in range(count):
            vertex = f"P{side}_{index}"
            vertices[vertex] = "T"
            selected_parents.append(vertex)
            chain.append(vertex)
        chain.append("X")
        edges.extend(zip(chain, chain[1:]))
    dummy_parents = []
    if sink_selected:
        selected_parents.append("X")
    else:
        dummy_parents.append("X")
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
    assert len(selected_leaves) == outgoing_count
    assert valid_binary_strong(vertices, tuple(edges))
    network = lift_network(
        {"vertices": vertices, "edges": tuple(edges), "leaves": tuple(all_leaves)}
    )
    selected_map = {
        leaf: label for label, leaf in enumerate(selected_leaves, 1)
    }
    selected_map["LIN"] = outgoing_count + 1
    return network, selected_map


def cycle_weak_presentations(outgoing_count):
    presentations = []
    for sink_selected in (False, True):
        ordinary_count = outgoing_count - int(sink_selected)
        for left_count in range(ordinary_count + 1):
            counts = (left_count, ordinary_count - left_count)
            network, selected_map = build_cycle_weak(
                outgoing_count, sink_selected, counts
            )
            presentations.append(
                {
                    "sink_selected": sink_selected,
                    "counts": counts,
                    "network": network,
                    "selected_map": selected_map,
                }
            )
    return tuple(presentations)


def cycle_reduced_type(network, selected_map, quartet):
    edges = tuple(network["edges"])
    global_to_leaf = {label: leaf for leaf, label in selected_map.items()}
    leaf_labels = {
        global_to_leaf[global_label]: local_label
        for local_label, global_label in enumerate(quartet, 1)
    }
    reticulations, trees = precompute_displayed_trees(
        network["vertices"], edges, leaf_labels
    )
    assert len(reticulations) == 1 and len(trees) == 2
    signatures = []
    for edge_index in range(len(edges)):
        values = []
        for _choice, selected, descendants in trees:
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
    flipped = tuple(sorted((right, left) for left, right in signatures))
    return min(signatures, flipped)


def cycle_deck_from_strong(candidate, outgoing_count):
    selected_map = dict(zip(candidate["network"]["leaves"], candidate["labels"]))
    return tuple(
        cycle_reduced_type(candidate["network"], selected_map, quartet)
        for quartet in outgoing_quartets(outgoing_count)
    )


def cycle_deck_from_weak(presentation, outgoing_count):
    return tuple(
        cycle_reduced_type(
            presentation["network"], presentation["selected_map"], quartet
        )
        for quartet in outgoing_quartets(outgoing_count)
    )


def exact_cycle_type_signature(tensor_type, contexts):
    variable_count = len(tensor_type) + 1
    if variable_count not in contexts:
        context = fmpq_mpoly_ctx.get(
            [
                f"cycle_reduced_v{variable_count}_p{index}"
                for index in range(variable_count)
            ]
        )
        contexts[variable_count] = context, context.gens()
    context, parameters = contexts[variable_count]
    edge_parameters = parameters[:-1]
    inheritance = parameters[-1]
    coordinates = []
    for assignment in JC_REPRESENTATIVES:
        total = context.constant(0)
        for choice in (0, 1):
            term = inheritance if choice == 0 else 1 - inheritance
            for edge_parameter, signature in zip(edge_parameters, tensor_type):
                mask = signature[choice]
                character = 0
                for position in range(4):
                    if mask & (1 << position):
                        character ^= assignment[position]
                if character:
                    term *= edge_parameter
            total += term
        coordinates.append(total)
    signature = []
    for invariant in ALL_INVARIANTS:
        polynomial = context.constant(0)
        for monomial, coefficient in invariant:
            term = context.constant(coefficient)
            for coordinate in monomial:
                term *= coordinates[coordinate]
            polynomial += term
        signature.append(bool(polynomial))
    return tuple(signature)


def deck_matrix(decks, type_signatures):
    return np.asarray(
        [
            [bit for tensor_type in deck for bit in type_signatures[tensor_type]]
            for deck in decks
        ],
        dtype=np.uint8,
    )


def orbit_signature_set(matrix, outgoing_count, transports):
    signatures = set()
    for permutation_index in range(len(transports[outgoing_count])):
        transported = matrix[:, transports[outgoing_count][permutation_index]]
        signatures.update(row.tobytes() for row in np.packbits(transported, axis=1))
    return signatures


def generate_certificate():
    theta_certificate = json.loads(THETA_CERTIFICATE.read_text())
    theta_type_signatures = {
        tuple(tuple(value) for value in record["edge_descendant_signatures"]):
        bit_tuple(record["exact_sixty_invariant_signature"])
        for record in theta_certificate["tensor_types"]
    }
    assert len(theta_type_signatures) == 130

    actions = invariant_actions()
    permutations_by_count = {
        count: tuple(permutations(range(1, count + 1)))
        for count in (2, 3, 4, 5, 6)
    }
    transports = {
        count: tuple(
            np.asarray(feature_transport(count, item, actions), dtype=np.int32)
            for item in permutations_by_count[count]
        )
        for count in (3, 4, 5, 6)
    }

    strong_cycle_candidates = {
        count: cycle_role_candidates(count) for count in (2, 3, 4)
    }
    assert {count: len(items) for count, items in strong_cycle_candidates.items()} == {
        2: 1,
        3: 2,
        4: 3,
    }
    weak_cycle = {
        count: cycle_weak_presentations(count) for count in (3, 4, 5, 6)
    }
    assert {count: len(items) for count, items in weak_cycle.items()} == {
        3: 7,
        4: 9,
        5: 11,
        6: 13,
    }

    cycle_types = set()
    strong_cycle_decks = {}
    for count in (3, 4):
        strong_cycle_decks[count] = tuple(
            cycle_deck_from_strong(candidate, count)
            for candidate in strong_cycle_candidates[count]
        )
        cycle_types.update(
            item for deck in strong_cycle_decks[count] for item in deck
        )
    weak_cycle_decks = {}
    for count in (3, 4, 5, 6):
        weak_cycle_decks[count] = tuple(
            cycle_deck_from_weak(presentation, count)
            for presentation in weak_cycle[count]
        )
        cycle_types.update(item for deck in weak_cycle_decks[count] for item in deck)
    assert len(cycle_types) == 4
    contexts = {}
    cycle_type_signatures = {
        tensor_type: exact_cycle_type_signature(tensor_type, contexts)
        for tensor_type in sorted(cycle_types)
    }

    # The two-outgoing strong cycle is a triangle.  Its two leaf placements
    # are one exact T class, covered by the inherited T correspondence.
    cycle_two = strong_cycle_candidates[2][0]
    two_codes = {
        canonical_mixed_graph(observational_graph(cycle_two, relabelling))
        for relabelling in permutations_by_count[2]
    }
    assert len(two_codes) == 1

    cycle_strong_sets = {}
    cycle_strong_maps = {}
    cycle_strong_summaries = {
        "2": {
            "role_candidates": 1,
            "relative_label_presentations": 2,
            "structural_T_classes": 1,
            "exact_signature_classes": "not needed; one T class",
        }
    }
    for count, expected in ((3, (12, 9)), (4, (72, 48))):
        candidates = strong_cycle_candidates[count]
        base = deck_matrix(strong_cycle_decks[count], cycle_type_signatures)
        signature_groups = defaultdict(list)
        structural_groups = defaultdict(list)
        for permutation_index, relabelling in enumerate(permutations_by_count[count]):
            transported = base[:, transports[count][permutation_index]]
            packed = np.packbits(transported, axis=1)
            for candidate_index, candidate in enumerate(candidates):
                item = (candidate_index, permutation_index)
                signature_groups[packed[candidate_index].tobytes()].append(item)
                structural_groups[
                    canonical_mixed_graph(observational_graph(candidate, relabelling))
                ].append(item)
        assert sum(map(len, signature_groups.values())) == expected[0]
        assert len(signature_groups) == len(structural_groups) == expected[1]
        item_signature = {
            item: signature
            for signature, members in signature_groups.items()
            for item in members
        }
        assert {
            frozenset(item_signature[item] for item in members)
            for members in structural_groups.values()
        } == {frozenset((signature,)) for signature in signature_groups}
        signature_codes = defaultdict(set)
        for code, members in structural_groups.items():
            for item in members:
                signature_codes[item_signature[item]].add(code)
        assert all(len(codes) == 1 for codes in signature_codes.values())
        cycle_strong_sets[count] = set(signature_groups)
        cycle_strong_maps[count] = {
            signature: members[0] for signature, members in signature_groups.items()
        }
        cycle_strong_summaries[str(count)] = {
            "role_candidates": len(candidates),
            "relative_label_presentations": expected[0],
            "structural_T_classes": len(structural_groups),
            "exact_signature_classes": len(signature_groups),
            "non_T_signature_collisions": 0,
        }

    cycle_weak_sets = {}
    cycle_weak_statuses = {}
    cycle_weak_summaries = {}
    for count in (3, 4, 5, 6):
        deck_members = defaultdict(list)
        for index, deck in enumerate(weak_cycle_decks[count]):
            deck_members[deck].append(index)
        decks = tuple(sorted(deck_members))
        status = {}
        for deck, members in deck_members.items():
            statuses = {weak_cycle[count][index]["sink_selected"] for index in members}
            assert len(statuses) == 1
            status[deck] = next(iter(statuses))
        base = deck_matrix(decks, cycle_type_signatures)
        signature_statuses = defaultdict(set)
        for permutation_index in range(len(permutations_by_count[count])):
            transported = base[:, transports[count][permutation_index]]
            packed = np.packbits(transported, axis=1)
            for row, deck in enumerate(decks):
                signature_statuses[packed[row].tobytes()].add(status[deck])
        assert all(len(values) == 1 for values in signature_statuses.values())
        cycle_weak_sets[count] = set(signature_statuses)
        cycle_weak_statuses[count] = signature_statuses
        cycle_weak_summaries[str(count)] = {
            "role_presentations": len(weak_cycle[count]),
            "base_tensor_decks": len(decks),
            "all_label_exact_signatures": len(signature_statuses),
            "signature_status_distribution": {
                str(key[0]).lower(): value
                for key, value in sorted(
                    Counter(tuple(values) for values in signature_statuses.values()).items()
                )
            },
        }
    assert {
        count: len(cycle_weak_sets[count]) for count in (3, 4, 5, 6)
    } == {3: 12, 4: 63, 5: 390, 6: 2790}

    # Cross-support cycle reconstruction uses the four-outgoing case.
    cycle_intersection = cycle_strong_sets[4] & cycle_weak_sets[4]
    assert len(cycle_intersection) == 48
    assert {
        tuple(cycle_weak_statuses[4][signature]) for signature in cycle_intersection
    } == {(True,)}
    source_code_cache = {}
    cycle_target_checks = 0
    non_T_cycle_targets = []
    for presentation_index, presentation in enumerate(weak_cycle[4]):
        if not presentation["sink_selected"]:
            continue
        candidate = {
            "network": presentation["network"],
            "labels": tuple(
                presentation["selected_map"][leaf]
                for leaf in presentation["network"]["leaves"]
            ),
        }
        deck = weak_cycle_decks[4][presentation_index]
        base = deck_matrix((deck,), cycle_type_signatures)[0]
        for permutation_index, relabelling in enumerate(permutations_by_count[4]):
            signature = np.packbits(base[transports[4][permutation_index]]).tobytes()
            if signature not in cycle_strong_maps[4]:
                continue
            cycle_target_checks += 1
            source_item = cycle_strong_maps[4][signature]
            if source_item not in source_code_cache:
                source_index, source_permutation = source_item
                source_code_cache[source_item] = canonical_mixed_graph(
                    observational_graph(
                        strong_cycle_candidates[4][source_index],
                        permutations_by_count[4][source_permutation],
                    )
                )
            target_code = canonical_mixed_graph(
                observational_graph(candidate, relabelling)
            )
            if target_code != source_code_cache[source_item]:
                non_T_cycle_targets.append(
                    (presentation_index, permutation_index, source_item)
                )
    assert cycle_target_checks == 96 and not non_T_cycle_targets

    # Theta source signatures: use all selected-strong weak presentations for
    # three/four ports, and the bounded support atlas for five/six.
    theta_strong_sets = {}
    theta_weak_all_sets = {}
    theta_small_summaries = {}
    for count in (3, 4):
        presentations = theta_weak_presentations(count)
        all_decks = tuple(sorted({item["deck"] for item in presentations}))
        strong_decks = tuple(
            sorted(
                {
                    item["deck"]
                    for item in presentations
                    if item["selected_pattern_is_strong"]
                }
            )
        )
        assert {
            tensor_type
            for deck in all_decks
            for tensor_type in deck
        } <= set(theta_type_signatures)
        theta_weak_all_sets[count] = orbit_signature_set(
            deck_matrix(all_decks, theta_type_signatures), count, transports
        )
        theta_strong_sets[count] = orbit_signature_set(
            deck_matrix(strong_decks, theta_type_signatures), count, transports
        )
        theta_small_summaries[str(count)] = {
            "weak_role_presentations": len(presentations),
            "weak_base_tensor_decks": len(all_decks),
            "weak_all_label_signatures": len(theta_weak_all_sets[count]),
            "selected_strong_role_presentations": sum(
                item["selected_pattern_is_strong"] for item in presentations
            ),
            "selected_strong_base_decks": len(strong_decks),
            "selected_strong_all_label_signatures": len(theta_strong_sets[count]),
        }
    assert {count: len(theta_weak_all_sets[count]) for count in (3, 4)} == {
        3: 78,
        4: 1236,
    }
    assert {count: len(theta_strong_sets[count]) for count in (3, 4)} == {
        3: 21,
        4: 516,
    }

    _raw, theta_candidates, _old_count = enumerate_atlas_candidates()
    for count in (5, 6):
        candidates = tuple(
            item for item in theta_candidates if len(item["labels"]) - 1 == count
        )
        decks = tuple(
            tuple(
                theta_reduced_type(candidate, quartet)
                for quartet in outgoing_quartets(count)
            )
            for candidate in candidates
        )
        theta_strong_sets[count] = orbit_signature_set(
            deck_matrix(decks, theta_type_signatures), count, transports
        )
    assert {count: len(theta_strong_sets[count]) for count in (5, 6)} == {
        5: 8520,
        6: 10980,
    }

    cross_intersections = {}
    for count in (3, 4, 5, 6):
        intersection = theta_strong_sets[count] & cycle_weak_sets[count]
        assert not intersection
        cross_intersections[str(count)] = {
            "theta_strong_signatures": len(theta_strong_sets[count]),
            "cycle_weak_signatures": len(cycle_weak_sets[count]),
            "intersection": 0,
        }

    reverse_small = {}
    for count in (3, 4):
        all_intersection = cycle_strong_sets[count] & theta_weak_all_sets[count]
        strong_intersection = cycle_strong_sets[count] & theta_strong_sets[count]
        assert len(all_intersection) == len(cycle_strong_sets[count])
        assert not strong_intersection
        reverse_small[str(count)] = {
            "cycle_strong_signatures": len(cycle_strong_sets[count]),
            "theta_weak_signature_intersection": len(all_intersection),
            "theta_selected_strong_signature_intersection": 0,
            "interpretation": "only an invisible-reticulation weak theta marginal mimics cycle",
        }

    type_records = [
        {
            "id": index,
            "edge_descendant_signatures": [list(item) for item in tensor_type],
            "exact_sixty_invariant_signature": "".join(
                "1" if value else "0" for value in cycle_type_signatures[tensor_type]
            ),
        }
        for index, tensor_type in enumerate(sorted(cycle_types))
    ]
    return {
        "status": {
            "arbitrary_nonroot_cycle_bowtie_classification": "PROVED",
            "cycle_theta_cross_generator_separation": "PROVED",
            "all_nonroot_cycle_theta_local_classification": "PROVED",
            "complete_local_move_system": ["T"],
            "one_sided_containment_classification": "UNRESOLVED",
            "global_blob_tree_reconstruction": "UNRESOLVED",
        },
        "cycle_support_sizes": {
            "minimum_strong_support": 2,
            "maximum_support_plus_two_outgoing_ports": 4,
        },
        "cycle_strong_atlas": cycle_strong_summaries,
        "cycle_weak_atlas": cycle_weak_summaries,
        "cycle_cross_support_four_outgoing": {
            "strong_signature_classes": 48,
            "weak_signature_classes": 63,
            "intersection": 48,
            "intersection_status": "selected sink is retained; restriction is strong",
            "intersecting_presentations_checked": cycle_target_checks,
            "non_T_targets": 0,
        },
        "theta_small_weak_atlas": theta_small_summaries,
        "theta_source_vs_cycle_weak": cross_intersections,
        "cycle_source_vs_theta_weak_small": reverse_small,
        "cycle_quartet_tensor_types": len(cycle_types),
        "cycle_exact_symbolic_invariant_pullbacks": len(cycle_types)
        * len(ALL_INVARIANTS),
        "cycle_tensor_types": type_records,
        "conclusion": (
            "arbitrary finite strongly tree-child nonroot cycle or theta "
            "blobs have full-dimensional regular JC overlap exactly under "
            "labelled isomorphism and ordinary triangle redirection T; "
            "cycle and theta generators are mutually separated"
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
                "cycle_strong_atlas": certificate["cycle_strong_atlas"],
                "cycle_cross_support_four_outgoing": certificate[
                    "cycle_cross_support_four_outgoing"
                ],
                "theta_source_vs_cycle_weak": certificate[
                    "theta_source_vs_cycle_weak"
                ],
                "cycle_quartet_tensor_types": certificate[
                    "cycle_quartet_tensor_types"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
