#!/usr/bin/env python3
"""Exact bounded-deck atlas for arbitrary JC root-blob subdivisions.

The previously certified support reduction produces 520 canonical theta
supports.  After removing the distinguished incoming leaf, this verifier
applies every relative outgoing labelling, computes every four-port marginal
exactly, and classifies the only signature collisions as Omega_chain or
contextual C_root.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

import numpy as np

from enumerate_four_leaf_root_theta import valid_binary_strong
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import (
    canonical_mixed_graph,
    enumerate_atlas_candidates,
    exact_type_signature,
    invariant_actions,
    reduced_tensor_type,
)
from verify_jc_cross_root_separation import ALL_INVARIANTS
from verify_jc_root_spanning_atlas import triangles


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "jc_root_support_deck.json"


def unlift(candidate):
    network = candidate["network"]
    rename = lambda vertex: "S" if vertex == "IN" else vertex
    vertices = {
        rename(vertex): ("S" if vertex == "IN" else color)
        for vertex, color in network["vertices"].items()
        if vertex not in {"S", "LIN"}
    }
    edges = tuple(
        (rename(tail), rename(head))
        for tail, head in network["edges"]
        if tail != "S" and head != "LIN"
    )
    leaves = tuple(leaf for leaf in network["leaves"] if leaf != "LIN")
    assert valid_binary_strong(vertices, edges)
    return {
        **candidate,
        "network": {"vertices": vertices, "edges": edges, "leaves": leaves},
        "labels": candidate["labels"][:-1],
    }


def quartets(count):
    return tuple(combinations(range(1, count + 1), 4))


def transport(count, relabelling, actions):
    local_quartets = quartets(count)
    lookup = {quartet: index for index, quartet in enumerate(local_quartets)}
    inverse = {new: old for old, new in enumerate(relabelling, 1)}
    answer = []
    for new_quartet in local_quartets:
        old_quartet = tuple(sorted(inverse[label] for label in new_quartet))
        old_index = lookup[old_quartet]
        position_to_label = tuple(
            new_quartet.index(relabelling[old_label - 1]) + 1
            for old_label in old_quartet
        )
        action = actions[position_to_label]
        answer.extend(
            old_index * len(ALL_INVARIANTS) + action[index]
            for index in range(len(ALL_INVARIANTS))
        )
    return np.asarray(answer, dtype=np.int32)


def observational_graph(candidate, relabelling):
    labels = tuple(relabelling[label - 1] for label in candidate["labels"])
    colors, edges = semi_directed_graph(candidate["network"], labels)
    local_triangles = triangles((colors, edges))
    if local_triangles:
        assert len(local_triangles) == 1
        triangle = local_triangles[0]
        colors = {
            vertex: (
                color
                if color.startswith("L")
                else "IT"
                if vertex in triangle
                else "I"
            )
            for vertex, color in colors.items()
        }
        normalized = []
        for kind, left, right in edges:
            if left in triangle and right in triangle:
                kind = "U"
                left, right = sorted((left, right))
            elif kind == "U":
                left, right = sorted((left, right))
            normalized.append((kind, left, right))
        edges = tuple(sorted(normalized))
    return canonical_mixed_graph((colors, edges))


def collapse_croot(candidate):
    """Remove a root C_root triangle, if it occurs in this presentation."""
    network = candidate["network"]
    vertices = network["vertices"]
    edges = tuple(network["edges"])
    children = sorted(head for tail, head in edges if tail == "S")
    if len(children) != 2:
        return None
    for tree_vertex, reticulation in (children, tuple(reversed(children))):
        if vertices[tree_vertex] != "T" or vertices[reticulation] not in {"R", "X"}:
            continue
        if (tree_vertex, reticulation) not in edges:
            continue
        tree_other = [
            head for tail, head in edges
            if tail == tree_vertex and head != reticulation
        ]
        reticulation_children = [
            head for tail, head in edges if tail == reticulation
        ]
        if len(tree_other) != 1 or len(reticulation_children) != 1:
            continue
        removed = {tree_vertex, reticulation}
        local_vertices = {
            vertex: color for vertex, color in vertices.items() if vertex not in removed
        }
        local_edges = [
            edge for edge in edges if not (set(edge) & removed)
        ] + [("S", tree_other[0]), ("S", reticulation_children[0])]
        if valid_binary_strong(local_vertices, tuple(local_edges)):
            return {
                "vertices": local_vertices,
                "edges": tuple(local_edges),
                "leaves": network["leaves"],
            }
    return None


def collapsed_graph(candidate, relabelling):
    collapsed = collapse_croot(candidate)
    if collapsed is None:
        return None
    labels = tuple(relabelling[label - 1] for label in candidate["labels"])
    return canonical_mixed_graph(semi_directed_graph(collapsed, labels))


def omega_partner(candidate, relabelling):
    """Reverse the three selected long ports and exchange the opposed pair."""
    words = tuple(word for word in candidate["segment_words"] if word)
    long_words = tuple(word for word in words if len(word) == 3)
    singletons = tuple(word for word in words if len(word) == 1)
    assert len(long_words) == 1 and len(singletons) == 1
    long_word = long_words[0]
    q_label = singletons[0][0]
    sink_labels = tuple(
        label for label in candidate["labels"]
        if all(label not in word for word in words)
    )
    assert len(sink_labels) == 1
    x_label = sink_labels[0]
    partner = [None] * len(relabelling)
    for old, reflected_old in zip(long_word, reversed(long_word)):
        partner[old - 1] = relabelling[reflected_old - 1]
    partner[q_label - 1] = relabelling[x_label - 1]
    partner[x_label - 1] = relabelling[q_label - 1]
    assert all(value is not None for value in partner)
    assert sorted(partner) == list(range(1, len(partner) + 1))
    return tuple(partner)


def code_digest(code):
    return sha256(repr(code).encode()).hexdigest()


def classify_count(count, candidates, candidate_indices, type_signatures, tensor_by_restriction):
    relabellings = tuple(permutations(range(1, count + 1)))
    actions = invariant_actions()
    transports = tuple(transport(count, item, actions) for item in relabellings)
    width = len(quartets(count)) * len(ALL_INVARIANTS)
    base = np.zeros((len(candidates), width), dtype=np.uint8)
    for candidate_index in candidate_indices:
        bits = []
        for quartet_index, _quartet in enumerate(quartets(count)):
            tensor_type = tensor_by_restriction[(candidate_index, quartet_index)]
            bits.extend(type_signatures[tensor_type])
        base[candidate_index] = bits

    signature_to_codes = defaultdict(set)
    signature_to_candidates = defaultdict(set)
    signature_to_code_representatives = defaultdict(dict)
    signature_to_collapsed = defaultdict(set)
    virtual = 0
    for candidate_index in candidate_indices:
        candidate = candidates[candidate_index]
        for permutation_index, relabelling in enumerate(relabellings):
            virtual += 1
            signature = np.packbits(
                base[candidate_index, transports[permutation_index]]
            ).tobytes()
            code = observational_graph(candidate, relabelling)
            signature_to_codes[signature].add(code)
            signature_to_candidates[signature].add(candidate_index)
            signature_to_code_representatives[signature].setdefault(
                code, (candidate_index, relabelling)
            )
            collapsed = collapsed_graph(candidate, relabelling)
            if collapsed is not None:
                signature_to_collapsed[signature].add(collapsed)

    structural = {code for codes in signature_to_codes.values() for code in codes}
    collisions = {
        signature: codes
        for signature, codes in signature_to_codes.items()
        if len(codes) > 1
    }
    classes = []
    family_counts = Counter()
    for signature in sorted(signature_to_codes):
        codes = signature_to_codes[signature]
        collapsed = signature_to_collapsed[signature]
        representatives = signature_to_code_representatives[signature]
        if collapsed:
            assert len(collapsed) == 1
            assert all(
                collapsed_graph(candidates[index], relabelling) in collapsed
                for index, relabelling in representatives.values()
            )
            family = "C_root"
        elif len(codes) == 2:
            assert count == 5
            assert all(
                observational_graph(
                    candidates[index], omega_partner(candidates[index], relabelling)
                ) in codes
                for index, relabelling in representatives.values()
            )
            family = "Omega_chain_k3"
        else:
            assert len(codes) == 1
            family = "singleton"
        family_counts[family] += 1
        record = {
            "signature_sha256": sha256(signature).hexdigest(),
            "family": family,
            "theta_structure_sha256": sorted(code_digest(code) for code in codes),
            "cycle_structure_sha256": sorted(code_digest(code) for code in collapsed),
            "candidate_indices": sorted(signature_to_candidates[signature]),
        }
        if family != "singleton":
            record["representatives"] = [
                {
                    "candidate": index,
                    "relabelling": list(relabelling),
                }
                for index, relabelling in sorted(representatives.values())
            ]
        classes.append(record)

    if count == 5:
        assert virtual == 36480
        assert len(structural) == 1980
        assert len(signature_to_codes) == 1620
        assert Counter(map(len, collisions.values())) == {2: 60, 6: 60}
        assert family_counts == {"singleton": 1500, "Omega_chain_k3": 60, "C_root": 60}
        assert all(
            len(signature_to_codes[signature]) == 6
            for signature in signature_to_codes if signature_to_collapsed[signature]
        )
        assert len({code for values in signature_to_collapsed.values() for code in values}) == 60
    else:
        assert virtual == 155520
        assert len(structural) == 7380
        assert len(signature_to_codes) == 7380
        assert not collisions
        assert family_counts == {"singleton": 7380}
        assert not any(signature_to_collapsed.values())

    serialized = json.dumps(classes, sort_keys=True, separators=(",", ":"))
    return {
        "candidate_count": len(candidate_indices),
        "virtual_relative_labellings": virtual,
        "structural_classes_modulo_isomorphism_and_T": len(structural),
        "exact_signature_classes": len(signature_to_codes),
        "collision_size_distribution": {
            str(size): amount for size, amount in sorted(Counter(map(len, collisions.values())).items())
        },
        "family_counts": dict(sorted(family_counts.items())),
        "cycle_classes_added_by_C_root": len(
            {code for values in signature_to_collapsed.values() for code in values}
        ),
        "complete_class_table_sha256": sha256(serialized.encode()).hexdigest(),
        "classes": classes,
    }


def main():
    raw, lifted, old_count = enumerate_atlas_candidates()
    assert raw == 656 and len(lifted) == 520 and old_count == 496
    candidates = tuple(unlift(candidate) for candidate in lifted)
    by_count = {
        count: tuple(
            index for index, candidate in enumerate(candidates)
            if len(candidate["labels"]) == count
        )
        for count in (5, 6)
    }
    assert {count: len(items) for count, items in by_count.items()} == {5: 304, 6: 216}

    tensor_by_restriction = {}
    tensor_occurrences = Counter()
    for candidate_index, candidate in enumerate(candidates):
        count = len(candidate["labels"])
        for quartet_index, quartet in enumerate(quartets(count)):
            tensor_type = reduced_tensor_type(candidate, quartet)
            tensor_by_restriction[(candidate_index, quartet_index)] = tensor_type
            tensor_occurrences[tensor_type] += 1
    assert len(tensor_by_restriction) == 4760
    assert len(tensor_occurrences) == 411

    contexts = {}
    type_signatures = {
        tensor_type: exact_type_signature(tensor_type, contexts)
        for tensor_type in sorted(tensor_occurrences)
    }
    results = {
        str(count): classify_count(
            count, candidates, by_count[count], type_signatures, tensor_by_restriction
        )
        for count in (5, 6)
    }
    certificate = {
        "status": {
            "enumeration": "EXACTLY COMPUTED",
            "invariant_pullbacks": "EXACTLY COMPUTED",
            "bounded_root_bowtie_atlas": "PROVED",
        },
        "scope": (
            "Five/six-outgoing root theta support restrictions required by "
            "the arbitrary subdivision reduction; at most one triangle."
        ),
        "canonical_role_candidates": 520,
        "canonical_role_candidates_by_port_count": {
            str(count): len(items) for count, items in by_count.items()
        },
        "quartet_restrictions": len(tensor_by_restriction),
        "reduced_root_tensor_types": len(tensor_occurrences),
        "exact_invariant_pullbacks": len(tensor_occurrences) * len(ALL_INVARIANTS),
        "root_invariants_per_tensor_type": len(ALL_INVARIANTS),
        "results": results,
        "conclusion": (
            "Every bounded root support collision is generated by contextual "
            "C_root or Omega_chain; all remaining structures are separated by "
            "an exact four-port marginal invariant, modulo ordinary triangle "
            "redirection T."
        ),
        "one_sided_containments": "UNRESOLVED",
    }
    CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    summary = {**certificate, "results": {
        count: {key: value for key, value in result.items() if key != "classes"}
        for count, result in results.items()
    }}
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
