#!/usr/bin/env python3
"""Exact JC atlas for every relative labelling of bounded support tensors.

Milestone 4A reduces every ordered strong theta expansion to restrictions
formed from a minimal core-preserving support and at most two additional
ports.  The earlier 496-case replay fixes the support/probe label roles.  This
verifier applies every permutation of the outgoing labels and therefore
closes that relative-labelling gap.

The symbolic calculation is compressed without approximation.  On a quartet
marginal, an edge is represented by its descendant mask in each of the four
displayed trees.  Edges with the same four masks occur together in every JC
Fourier monomial, so their parameters may be replaced by their product.  The
7,360 quartet restrictions reduce to 90 exact tensor types.  Exact pullbacks
of all sixty root-atlas invariants on those types separate all 19,500
structural classes modulo ordinary triangle redirection.
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
from generic_fourier_network import precompute_displayed_trees
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES, coordinate_permutation
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_incoming_port_atlas import lift_network
from verify_jc_root_spanning_atlas import normalized_candidate, triangles
from verify_jc_support_augmented_atlas import (
    SELECTED_FEATURES as ROLE_SELECTED_FEATURES,
    build_labelled,
    enumerate_candidates,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_fully_labelled_support_atlas.json"
ROLE_CERTIFICATE = HERE / "certificates" / "jc_support_augmented_atlas.json"

# Global feature indices are quartet_index * 60 + invariant_index, where the
# quartets are lexicographically ordered three-subsets of the outgoing labels
# followed by the distinguished incoming label.  A deterministic greedy
# search found these lists; the verifier uses them only after exact replay.
SELECTED_FEATURES = {
    5: (
        38, 520, 100, 76, 397, 500, 247, 186, 128, 577, 339, 426,
        21, 252, 126, 558, 216, 452, 332, 378, 84, 441, 264, 138,
        497, 189, 549, 131, 371, 32, 310, 250, 69, 432, 498, 36,
        380, 436, 193, 248, 129, 68, 547, 488, 11, 550, 309, 403,
        256, 493, 67, 367, 188, 246, 66, 308, 187, 127, 427, 487,
        428, 486, 9, 7, 8, 133, 306, 548, 404, 307, 366, 546, 6,
        17, 18,
    ),
    6: (
        26, 96, 154, 687, 968, 907, 426, 726, 275, 1086, 852, 376,
        617, 1153, 201, 321, 796, 1040, 560, 257, 492, 136, 1100,
        21, 680, 432, 921, 976, 732, 620, 316, 496, 81, 861, 196,
        792, 730, 969, 551, 71, 1091, 11, 430, 250, 671, 1149, 129,
        911, 1031, 369, 610, 489, 801, 189, 312, 851, 672, 436, 370,
        977, 1145, 122, 182, 242, 902,
    ),
}


def enumerate_plus_one_candidates():
    """Enumerate the support-size-four core with one additional probe."""

    _raw, cores = enumerate_cores()
    candidates = {}
    raw = 0
    for core_index, core in enumerate(cores):
        repairs = minimal_strong_repairs(
            core["vertex_types"], core["directed_segments"]
        )
        sink_count = sum(
            color == "X" for color in core["vertex_types"].values()
        )
        if sink_count != 2 or not repairs or len(repairs[0]) != 2:
            continue
        assert core_index == 1
        for repair in repairs:
            for extra_segments in product(
                range(len(core["directed_segments"])), repeat=1
            ):
                for base, labels, repair_labels, extra_labels, words in build_labelled(
                    core, repair, extra_segments
                ):
                    raw += 1
                    assert valid_binary_strong(base["vertices"], base["edges"])
                    lifted = lift_network(base)
                    complete_labels = labels + (len(labels) + 1,)
                    code = canonical_code(
                        lifted["vertices"],
                        lifted["edges"],
                        dict(zip(lifted["leaves"], complete_labels)),
                    )
                    candidates.setdefault(
                        code,
                        {
                            "rooted_code_sha256": sha256(
                                repr(code).encode()
                            ).hexdigest(),
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
    assert raw == 32 and len(candidates) == 24
    return raw, tuple(candidates[code] for code in sorted(candidates))


def enumerate_atlas_candidates():
    old_raw, old_candidates = enumerate_candidates()
    plus_one_raw, plus_one = enumerate_plus_one_candidates()
    return old_raw + plus_one_raw, old_candidates + plus_one, len(old_candidates)


def outgoing_quartets(outgoing_count):
    incoming = outgoing_count + 1
    return tuple(
        tuple(outgoing) + (incoming,)
        for outgoing in combinations(range(1, incoming), 3)
    )


def invariant_actions():
    lookup = {invariant: index for index, invariant in enumerate(ALL_INVARIANTS)}
    actions = {}
    for permutation in permutations((1, 2, 3, 4)):
        coordinate_map = coordinate_permutation(permutation)
        image = []
        for invariant in ALL_INVARIANTS:
            transported = normalized_candidate(
                tuple(
                    (
                        tuple(sorted(coordinate_map[index] for index in monomial)),
                        coefficient,
                    )
                    for monomial, coefficient in invariant
                )
            )
            image.append(lookup[transported])
        actions[permutation] = tuple(image)
    assert len(set(actions.values())) == 24
    return actions


def feature_transport(outgoing_count, relabelling, actions):
    """Map every global feature to its canonical-role feature."""

    quartets = outgoing_quartets(outgoing_count)
    quartet_lookup = {quartet: index for index, quartet in enumerate(quartets)}
    inverse = {new: old for old, new in enumerate(relabelling, 1)}
    answer = []
    for new_quartet in quartets:
        new_outgoing = new_quartet[:-1]
        old_outgoing = tuple(sorted(inverse[label] for label in new_outgoing))
        old_quartet = old_outgoing + (outgoing_count + 1,)
        old_quartet_index = quartet_lookup[old_quartet]
        position_to_label = tuple(
            new_outgoing.index(relabelling[old_label - 1]) + 1
            for old_label in old_outgoing
        ) + (4,)
        invariant_action = actions[position_to_label]
        answer.extend(
            old_quartet_index * len(ALL_INVARIANTS) + invariant_action[index]
            for index in range(len(ALL_INVARIANTS))
        )
    return tuple(answer)


def observational_graph(candidate, relabelling):
    """Semi-directed graph in the quotient generated by ordinary move T."""

    outgoing_count = len(candidate["labels"]) - 1
    mapped_labels = tuple(
        relabelling[label - 1] if label <= outgoing_count else label
        for label in candidate["labels"]
    )
    colors, edges = semi_directed_graph(candidate["network"], mapped_labels)
    local_triangles = triangles((colors, edges))
    if not local_triangles:
        return colors, edges
    assert len(local_triangles) == 1
    triangle = local_triangles[0]
    normalized_colors = {
        vertex: (
            color
            if color.startswith("L")
            else "IT"
            if vertex in triangle
            else "I"
        )
        for vertex, color in colors.items()
    }
    normalized_edges = []
    for kind, left, right in edges:
        if left in triangle and right in triangle:
            kind = "U"
            left, right = sorted((left, right))
        elif kind == "U":
            left, right = sorted((left, right))
        normalized_edges.append((kind, left, right))
    return normalized_colors, tuple(sorted(normalized_edges))


def relation_neighborhood(colors, edges):
    answer = {vertex: [] for vertex in colors}
    for kind, left, right in edges:
        if kind == "U":
            answer[left].append(("U", right))
            answer[right].append(("U", left))
        else:
            answer[left].append(("D+", right))
            answer[right].append(("D-", left))
    return answer


def canonical_mixed_graph(graph):
    """Exact individualization-refinement code for a coloured mixed graph."""

    colors, edges = graph
    neighborhood = relation_neighborhood(colors, edges)
    initial_groups = defaultdict(list)
    for vertex, color in colors.items():
        initial_groups[color].append(vertex)
    initial = tuple(
        tuple(sorted(initial_groups[color])) for color in sorted(initial_groups)
    )

    def refine(partition):
        while True:
            cell_index = {
                vertex: index
                for index, cell in enumerate(partition)
                for vertex in cell
            }
            changed = False
            answer = []
            for cell in partition:
                blocks = defaultdict(list)
                for vertex in cell:
                    counts = Counter(
                        (relation, cell_index[neighbor])
                        for relation, neighbor in neighborhood[vertex]
                    )
                    signature = tuple(
                        counts[(relation, index)]
                        for index in range(len(partition))
                        for relation in ("U", "D+", "D-")
                    )
                    blocks[signature].append(vertex)
                if len(blocks) > 1:
                    changed = True
                answer.extend(tuple(sorted(blocks[key])) for key in sorted(blocks))
            partition = tuple(answer)
            if not changed:
                return partition

    def leaf_code(partition):
        order = tuple(cell[0] for cell in partition)
        position = {vertex: index for index, vertex in enumerate(order)}
        transported = []
        for kind, left, right in edges:
            left, right = position[left], position[right]
            if kind == "U":
                left, right = sorted((left, right))
            transported.append((kind, left, right))
        return tuple(colors[vertex] for vertex in order), tuple(sorted(transported))

    def search(partition):
        partition = refine(partition)
        if all(len(cell) == 1 for cell in partition):
            return leaf_code(partition)
        split_index = next(index for index, cell in enumerate(partition) if len(cell) > 1)
        cell = partition[split_index]
        best = None
        for vertex in cell:
            remainder = tuple(item for item in cell if item != vertex)
            individualized = (
                partition[:split_index]
                + ((vertex,), remainder)
                + partition[split_index + 1 :]
            )
            candidate = search(individualized)
            if best is None or candidate < best:
                best = candidate
        return best

    return search(initial)


def cube_actions():
    choices = tuple(product((0, 1), repeat=2))
    lookup = {choice: index for index, choice in enumerate(choices)}
    actions = []
    for coordinate_order in permutations((0, 1)):
        for flips in product((0, 1), repeat=2):
            actions.append(
                tuple(
                    lookup[
                        tuple(
                            choice[coordinate_order[index]] ^ flips[index]
                            for index in range(2)
                        )
                    ]
                    for choice in choices
                )
            )
    assert len(set(actions)) == 8
    return tuple(sorted(set(actions)))


CUBE_ACTIONS = cube_actions()


def reduced_tensor_type(candidate, quartet):
    """Canonical displayed-tree descendant-mask type of one quartet."""

    network = candidate["network"]
    edges = tuple(network["edges"])
    label_to_leaf = dict(zip(candidate["labels"], network["leaves"]))
    selected_leaf_labels = {
        label_to_leaf[global_label]: local_label
        for local_label, global_label in enumerate(quartet, 1)
    }
    reticulations, trees = precompute_displayed_trees(
        network["vertices"], edges, selected_leaf_labels
    )
    assert len(reticulations) == 2 and len(trees) == 4
    signatures = []
    for edge_index in range(len(edges)):
        signature = []
        for _choices, selected, descendants in trees:
            if edge_index not in selected:
                signature.append(0)
                continue
            mask = 0
            for local_label in descendants[edge_index]:
                mask |= 1 << (local_label - 1)
            signature.append(mask)
        if any(signature):
            signatures.append(tuple(signature))
    # Repeated signatures always occur together and are replaced by the
    # product of their independent edge multipliers.
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


def reduced_coordinates(tensor_type, context, parameters):
    edge_parameters = parameters[: len(tensor_type)]
    inheritance = parameters[len(tensor_type) :]
    assert len(inheritance) == 2
    choices = tuple(product((0, 1), repeat=2))
    outputs = []
    for assignment in JC_REPRESENTATIVES:
        total = context.constant(0)
        for choice_index, choice in enumerate(choices):
            term = context.constant(1)
            for index, bit in enumerate(choice):
                term *= inheritance[index] if bit == 0 else 1 - inheritance[index]
            for edge_parameter, signature in zip(edge_parameters, tensor_type):
                mask = signature[choice_index]
                character = 0
                for position in range(4):
                    if mask & (1 << position):
                        character ^= assignment[position]
                if character:
                    term *= edge_parameter
            total += term
        outputs.append(total)
    return tuple(outputs)


def exact_type_signature(tensor_type, contexts):
    variable_count = len(tensor_type) + 2
    if variable_count not in contexts:
        context = fmpq_mpoly_ctx.get(
            [f"reduced_v{variable_count}_p{index}" for index in range(variable_count)]
        )
        contexts[variable_count] = (context, context.gens())
    context, parameters = contexts[variable_count]
    coordinates = reduced_coordinates(tensor_type, context, parameters)
    signature = []
    for invariant in ALL_INVARIANTS:
        answer = context.constant(0)
        for monomial, coefficient in invariant:
            term = context.constant(coefficient)
            for coordinate in monomial:
                term *= coordinates[coordinate]
            answer += term
        signature.append(bool(answer))
    return tuple(signature)


def bit_string(signature):
    return "".join("1" if value else "0" for value in signature)


def feature_records(outgoing_count):
    quartets = outgoing_quartets(outgoing_count)
    return [
        {
            "global_feature_index": feature,
            "quartet": list(quartets[feature // len(ALL_INVARIANTS)]),
            "root_invariant_feature": feature % len(ALL_INVARIANTS),
        }
        for feature in SELECTED_FEATURES[outgoing_count]
    ]


def generate_certificate():
    raw, candidates, old_candidate_count = enumerate_atlas_candidates()
    assert raw == 656 and len(candidates) == 520 and old_candidate_count == 496
    permutations_by_count = {
        count: tuple(permutations(range(1, count + 1))) for count in (5, 6)
    }

    structural = defaultdict(list)
    virtual_count = 0
    for candidate_index, candidate in enumerate(candidates):
        outgoing_count = len(candidate["labels"]) - 1
        for permutation_index, relabelling in enumerate(
            permutations_by_count[outgoing_count]
        ):
            virtual_count += 1
            code = canonical_mixed_graph(observational_graph(candidate, relabelling))
            structural[(outgoing_count, code)].append(
                (candidate_index, permutation_index)
            )
    assert virtual_count == 192000
    assert len(structural) == 19500

    structural_items = tuple(
        sorted(
            (
                outgoing_count,
                code,
                tuple(sorted(members)),
            )
            for (outgoing_count, code), members in structural.items()
        )
    )
    assert Counter(item[0] for item in structural_items) == {5: 8520, 6: 10980}

    tensor_by_restriction = {}
    tensor_occurrences = Counter()
    for candidate_index, candidate in enumerate(candidates):
        outgoing_count = len(candidate["labels"]) - 1
        for quartet_index, quartet in enumerate(outgoing_quartets(outgoing_count)):
            tensor_type = reduced_tensor_type(candidate, quartet)
            tensor_by_restriction[(candidate_index, quartet_index)] = tensor_type
            tensor_occurrences[tensor_type] += 1
    assert len(tensor_by_restriction) == 7360
    assert len(tensor_occurrences) == 90

    contexts = {}
    type_signatures = {}
    for type_index, tensor_type in enumerate(sorted(tensor_occurrences)):
        type_signatures[tensor_type] = exact_type_signature(tensor_type, contexts)
        if (type_index + 1) % 10 == 0:
            print("exact reduced tensor types", type_index + 1, "/ 90", flush=True)

    # Independent normalization audit: the earlier 496-case verifier pulled
    # its selected invariants directly through every full network.  Recompute
    # those same bits from the reduced tensor types and require byte-for-byte
    # agreement with that direct symbolic certificate.
    role_certificate = json.loads(ROLE_CERTIFICATE.read_text())
    assert len(role_certificate["networks"]) == old_candidate_count
    for candidate_index, candidate in enumerate(candidates[:old_candidate_count]):
        outgoing_count = len(candidate["labels"]) - 1
        quartet_lookup = {
            quartet: index
            for index, quartet in enumerate(outgoing_quartets(outgoing_count))
        }
        signature = []
        for quartet, invariant_index in ROLE_SELECTED_FEATURES[outgoing_count]:
            tensor_type = tensor_by_restriction[
                (candidate_index, quartet_lookup[quartet])
            ]
            signature.append(type_signatures[tensor_type][invariant_index])
        assert bit_string(signature) == role_certificate["networks"][
            candidate_index
        ]["selected_signature"]

    actions = invariant_actions()
    transports = {
        (outgoing_count, permutation_index): feature_transport(
            outgoing_count, relabelling, actions
        )
        for outgoing_count in (5, 6)
        for permutation_index, relabelling in enumerate(
            permutations_by_count[outgoing_count]
        )
    }

    class_records = []
    exact_signatures = set()
    for class_index, (outgoing_count, code, members) in enumerate(structural_items):
        candidate_index, permutation_index = members[0]
        transport = transports[(outgoing_count, permutation_index)]
        signature = []
        for global_feature in SELECTED_FEATURES[outgoing_count]:
            base_feature = transport[global_feature]
            quartet_index, invariant_index = divmod(base_feature, len(ALL_INVARIANTS))
            tensor_type = tensor_by_restriction[(candidate_index, quartet_index)]
            signature.append(type_signatures[tensor_type][invariant_index])
        signature = tuple(signature)
        key = (outgoing_count, signature)
        assert key not in exact_signatures
        exact_signatures.add(key)
        relabelling = permutations_by_count[outgoing_count][permutation_index]
        class_records.append(
            {
                "id": class_index,
                "outgoing_port_count": outgoing_count,
                "presentation_count": len(members),
                "representative_candidate_index": candidate_index,
                "representative_outgoing_relabelling": list(relabelling),
                "canonical_T_quotient_sha256": sha256(repr(code).encode()).hexdigest(),
                "exact_selected_signature": bit_string(signature),
            }
        )
    assert len(exact_signatures) == 19500

    type_records = []
    for type_index, tensor_type in enumerate(sorted(tensor_occurrences)):
        type_records.append(
            {
                "id": type_index,
                "edge_descendant_signatures": [list(item) for item in tensor_type],
                "occurrences_among_7360_restrictions": tensor_occurrences[tensor_type],
                "exact_sixty_invariant_signature": bit_string(
                    type_signatures[tensor_type]
                ),
            }
        )

    return {
        "status": {
            "fully_labelled_bounded_support_bowtie_classification": "PROVED",
            "complete_move_system_in_this_atlas": ["T"],
            "one_sided_containment_classification": "UNRESOLVED",
            "arbitrary_blob_completeness": "UNRESOLVED",
        },
        "scope": (
            "all relative outgoing-port labellings of every strong nonroot "
            "theta restriction consisting of a support of size three plus "
            "two probes, or a support of size four plus one or two probes; "
            "the incoming state port is fixed"
        ),
        "raw_role_presentations": raw,
        "canonical_role_labelled_candidates": len(candidates),
        "virtual_relative_label_presentations": virtual_count,
        "virtual_presentations_by_outgoing_count": {
            "5": 304 * 120,
            "6": 216 * 720,
        },
        "structural_classes_modulo_isomorphism_and_T": len(structural_items),
        "structural_classes_by_outgoing_count": {"5": 8520, "6": 10980},
        "presentation_class_size_distribution": dict(
            sorted(Counter(map(len, structural.values())).items())
        ),
        "selected_features": {
            str(count): feature_records(count) for count in (5, 6)
        },
        "selected_feature_counts": {
            str(count): len(SELECTED_FEATURES[count]) for count in (5, 6)
        },
        "quartet_restrictions": len(tensor_by_restriction),
        "reduced_quartet_tensor_types": len(tensor_occurrences),
        "exact_symbolic_invariant_pullbacks": len(tensor_occurrences)
        * len(ALL_INVARIANTS),
        "direct_full_network_signature_crosschecks": sum(
            len(ROLE_SELECTED_FEATURES[len(candidate["labels"]) - 1])
            for candidate in candidates[:old_candidate_count]
        ),
        "exact_selected_signature_classes": len(exact_signatures),
        "non_T_exact_signature_collisions": 0,
        "tensor_types": type_records,
        "structural_classes": class_records,
        "conclusion": (
            "full-dimensional regular JC overlap in the fully relatively "
            "labelled bounded strong-support atlas occurs exactly under "
            "labelled isomorphism or ordinary triangle redirection"
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
                "virtual_relative_label_presentations": certificate[
                    "virtual_relative_label_presentations"
                ],
                "structural_classes_modulo_isomorphism_and_T": certificate[
                    "structural_classes_modulo_isomorphism_and_T"
                ],
                "reduced_quartet_tensor_types": certificate[
                    "reduced_quartet_tensor_types"
                ],
                "exact_symbolic_invariant_pullbacks": certificate[
                    "exact_symbolic_invariant_pullbacks"
                ],
                "non_T_exact_signature_collisions": certificate[
                    "non_T_exact_signature_collisions"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
