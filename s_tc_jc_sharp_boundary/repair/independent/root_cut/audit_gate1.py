#!/usr/bin/env python3
"""Clean-room structural audit of the frozen Gate 1 root certificate.

The program treats all status strings as inert.  It checks every rooted
network actually serialized in the frozen JSON under both:

* the literal one-root-suppression semi-directed convention in Englander et
  al., Definition 2.2; and
* the broader merge/resuppress normalization used by the historical audit.

It deliberately imports no project graph, Fourier, atlas, or rank module.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Iterator, Mapping, Sequence

from graph_conventions import (
    broad_artifact_reduction,
    canonical_mixed_code,
    ordinary_triangle_status,
    ordinary_triangle_quotient,
    rooted_checks,
    serialize_edges,
    suppress_root_once,
    validate_literal_standard,
)


DEFAULT_PROJECT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability"
)


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def network_rows(value: object, path: tuple[object, ...] = ()) -> Iterator[tuple[tuple[object, ...], Mapping[str, object]]]:
    if isinstance(value, Mapping):
        network = value.get("network")
        if isinstance(network, Mapping):
            yield path, network
        for key, child in value.items():
            yield from network_rows(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from network_rows(child, path + (index,))


def labels_for(network: Mapping[str, object]) -> dict[str, int]:
    raw = network.get("selected_leaf_labels", network.get("leaf_labels", {}))
    labels = {str(leaf): int(label) for leaf, label in dict(raw).items()}
    next_label = max(labels.values(), default=0) + 1
    for leaf in network.get("unselected_completion_leaves", []):
        labels[str(leaf)] = next_label
        next_label += 1
    return labels


def broad_reticulation_count(edges) -> int:
    incoming = Counter(vertex for edge in edges for vertex in edge.arrowheads)
    return sum(count == 2 for count in incoming.values())


def static_checker_audit(script: Path) -> dict[str, object]:
    source = script.read_text()
    merge_definition = source.index("def merge_parallel")
    reduction_definition = source.index("def standard_reduction")
    parallel_test = source.index('"parallel_mixed_edges": len(edges) != len({edge.ends for edge in edges})')
    reduction_slice = source[reduction_definition:source.index("def mixed_relation")]
    long_start = source.index("def long_word_attack")
    long_end = source.index("def bit_direction_proof_fixture")
    long_body = source[long_start:long_end]
    return {
        "merge_helper_precedes_reducer": merge_definition < reduction_definition,
        "reducer_returns_merge_parallel": "return merge_parallel(edges), labels" in reduction_slice,
        "parallel_test_occurs_after_reducer_definition": parallel_test > reduction_definition,
        "no_parallel_predicate_is_tautological_on_reducer_output": (
            "return merge_parallel(edges), labels" in reduction_slice
            and 'len(edges) != len({edge.ends for edge in edges})' in source
        ),
        "long_word_attack_accepts_no_model_or_deck_argument": "def long_word_attack(core_data):" in long_body,
        "long_word_attack_builds_comparisons_from_the_words_it_reconstructs": (
            "for segment, word in enumerate(words):" in long_body
            and "comparisons[(label, other)] = position < other_position" in long_body
            and "tuple(reconstructed) != tuple(words)" in long_body
        ),
        "long_word_attack_is_not_an_independent_observational_test": True,
    }


def reduced_record(network: Mapping[str, object]):
    root = str(network["root"])
    arcs = tuple((str(tail), str(head)) for tail, head in network["arcs"])
    labels = labels_for(network)
    literal, _reticulations = suppress_root_once(root, arcs)
    broad = broad_artifact_reduction(root, arcs, labels)
    return labels, literal, broad


def common_representative_audit(frozen: Mapping[str, object]) -> dict[str, object]:
    """Audit the five serialized six-port common-signature representatives."""

    level = frozen["levels"]["6"]
    source = {
        str(record["signature_sha256"]): record
        for record in level["source"]["signature_class_representatives"]
    }
    target = {
        str(record["signature_sha256"]): record
        for record in level["target"]["signature_class_representatives"]
    }
    rows = []
    counts = Counter()
    for common in level["common_signature_rows"]:
        signature = str(common["signature_sha256"])
        source_record = source[signature]
        target_record = target[signature]
        source_labels, source_literal, source_broad = reduced_record(
            source_record["network"]
        )
        target_labels, target_literal, target_broad = reduced_record(
            target_record["network"]
        )
        source_valid = validate_literal_standard(source_literal, source_labels)
        target_valid = validate_literal_standard(target_literal, target_labels)
        both_valid = bool(
            source_valid["valid_standard_strong"]
            and target_valid["valid_standard_strong"]
        )
        literal_isomorphic = False
        literal_T = False
        if both_valid:
            literal_isomorphic = canonical_mixed_code(
                source_literal, source_labels
            ) == canonical_mixed_code(target_literal, target_labels)
            literal_T = canonical_mixed_code(
                ordinary_triangle_quotient(source_literal, source_labels),
                source_labels,
            ) == canonical_mixed_code(
                ordinary_triangle_quotient(target_literal, target_labels),
                target_labels,
            )
            counts["literal_isomorphic" if literal_isomorphic else "literal_T_only"] += 1
        else:
            counts["outside_literal_standard_class"] += 1
        broad_isomorphic = canonical_mixed_code(
            source_broad, source_labels
        ) == canonical_mixed_code(target_broad, target_labels)
        broad_T = canonical_mixed_code(
            ordinary_triangle_quotient(source_broad, source_labels), source_labels
        ) == canonical_mixed_code(
            ordinary_triangle_quotient(target_broad, target_labels), target_labels
        )
        rows.append(
            {
                "signature_sha256": signature,
                "source_literal_failures": source_valid["failures"],
                "target_literal_failures": target_valid["failures"],
                "both_literal_standard_strong": both_valid,
                "literal_labelled_isomorphic": literal_isomorphic,
                "literal_ordinary_T_equivalent": literal_T,
                "broad_labelled_isomorphic": broad_isomorphic,
                "broad_ordinary_T_equivalent": broad_T,
            }
        )
    return {
        "status": "EXACTLY COMPUTED",
        "serialized_common_signature_representatives": len(rows),
        "counts": dict(sorted(counts.items())),
        "all_literal_valid_representative_pairs_are_isomorphic_or_T": all(
            (not row["both_literal_standard_strong"])
            or row["literal_labelled_isomorphic"]
            or row["literal_ordinary_T_equivalent"]
            for row in rows
        ),
        "all_broad_representative_pairs_are_isomorphic_or_T": all(
            row["broad_labelled_isomorphic"]
            or row["broad_ordinary_T_equivalent"]
            for row in rows
        ),
        "scope_limit": (
            "The final JSON serializes one representative per signature, not all "
            "rooted parameterizations counted in each common class."
        ),
        "rows": rows,
    }


def audit(project: Path, failure_directory: Path) -> dict[str, object]:
    frozen_path = project / "AUDIT/INDEPENDENT_IMPLEMENTATION/gate1_root_full_completion_audit.json"
    review_path = project / "AUDIT/REVIEWS/gate1_root_closure_adversarial_crosscheck.json"
    script_path = project / "AUDIT/REVIEWS/gate1_root_closure_adversarial_crosscheck.py"
    frozen = json.loads(frozen_path.read_text())
    review = json.loads(review_path.read_text())

    serialized = list(network_rows(frozen))
    failures: list[dict[str, object]] = []
    literal_counts: Counter[tuple[str, ...]] = Counter()
    rooted_failure_counts: Counter[str] = Counter()
    triangle_counts: Counter[str] = Counter()
    broad_reticulation_drops = 0
    all_broad_triangles_ordinary = True
    unique_payloads: set[str] = set()

    for path, network in serialized:
        root = str(network["root"])
        arcs = tuple((str(tail), str(head)) for tail, head in network["arcs"])
        labels = labels_for(network)
        unique_payloads.add(json.dumps(network, sort_keys=True, separators=(",", ":")))
        rooted = rooted_checks(root, arcs, labels)
        for reason in rooted["failures"]:
            rooted_failure_counts[str(reason)] += 1

        literal_edges, rooted_reticulations = suppress_root_once(root, arcs)
        literal = validate_literal_standard(literal_edges, labels)
        reasons = tuple(str(reason) for reason in literal["failures"])
        literal_counts[reasons] += 1

        broad_edges = broad_artifact_reduction(root, arcs, labels)
        broad_reticulations = broad_reticulation_count(broad_edges)
        if len(rooted_reticulations) != broad_reticulations:
            broad_reticulation_drops += 1
        triangle = ordinary_triangle_status(broad_edges, labels)
        triangle_counts[
            "none" if triangle["triangle_count"] == 0 else "ordinary" if triangle["ordinary"] else "nonordinary"
        ] += 1
        all_broad_triangles_ordinary &= bool(triangle["ordinary"])

        if reasons:
            failures.append(
                {
                    "certificate_path": list(path),
                    "literal_failures": list(reasons),
                    "rooted_check": rooted,
                    "rooted_reticulation_count": len(rooted_reticulations),
                    "broad_reduced_reticulation_count": broad_reticulations,
                    "network": network,
                    "literal_root_suppression": serialize_edges(literal_edges),
                    "broad_artifact_reduction": serialize_edges(broad_edges),
                }
            )

    failure_directory.mkdir(parents=True, exist_ok=True)
    failure_path = failure_directory / "gate1_nonstandard_root_suppression_failures.json"
    failure_payload = {
        "status": "FALSE",
        "meaning": (
            "These serialized rooted presentations do not produce a valid "
            "parallel-free binary semi-directed network after the single former-root "
            "suppression of the cited standard convention.  They pass only after the "
            "historical broader parallel-merge/resuppression normalization."
        ),
        "failure_count": len(failures),
        "failures": failures,
    }
    failure_path.write_text(json.dumps(failure_payload, indent=2, sort_keys=True) + "\n")

    frozen_universe_size = sum(
        int(frozen["levels"][str(port)][side]["rooted_types"])
        for port in (6, 7, 8)
        for side in ("source", "target")
    )
    nine = review.get("nine_port_correction", {})
    common_representatives = common_representative_audit(frozen)
    return {
        "inputs": {
            str(frozen_path): file_hash(frozen_path),
            str(review_path): file_hash(review_path),
            str(script_path): file_hash(script_path),
        },
        "literal_standard_convention": {
            "reference_operation": (
                "forget non-reticulation directions and suppress the former root once; "
                "the resulting semi-directed network itself may not have parallel edges"
            ),
            "serialized_network_records": len(serialized),
            "unique_serialized_network_records": len(unique_payloads),
            "declared_full_6_7_8_rooted_universe": frozen_universe_size,
            "serialized_fraction_is_representatives_only": len(serialized) < frozen_universe_size,
            "valid_after_literal_root_suppression": literal_counts[()],
            "invalid_after_literal_root_suppression": len(failures),
            "failure_reason_counts": {
                "+".join(reasons): count
                for reasons, count in sorted(literal_counts.items())
                if reasons
            },
            "rooted_failure_counts": dict(sorted(rooted_failure_counts.items())),
            "rooted_to_broad_reticulation_count_drops": broad_reticulation_drops,
            "status_of_claim_all_generated_networks_are_in_standard_class": "FALSE",
        },
        "ordinary_triangle_redirection": {
            "broad_reduced_serialized_triangle_counts": dict(sorted(triangle_counts.items())),
            "all_serialized_triangles_have_exactly_one_internal_reticulation_and_ordinary_arms": all_broad_triangles_ordinary,
            "status_on_serialized_records": "EXACTLY COMPUTED",
            "warning": (
                "The historical quotient erases all triangle arrowheads in general.  "
                "That overbroad operation happens to agree with ordinary T on every "
                "serialized triangle checked here, but its implementation is not the definition of T."
            ),
        },
        "common_collision_representatives": common_representatives,
        "static_checker_findings": static_checker_audit(script_path),
        "nine_port_certificate_scope": {
            "declared_raw_attempts": nine.get("raw_theta_four_block_attempts"),
            "declared_signature_checks": nine.get("exact_labelled_signature_checks"),
            "preserved_matching_fixtures": len(nine.get("fixtures", [])),
            "nonmatching_network_encodings_preserved_in_json": False,
            "status_from_final_json_alone": "UNRESOLVED",
        },
        "arbitrary_subdivision_promotion": {
            "finite_checks_do_not_by_themselves_quantify_over_arbitrary_words": True,
            "the_long_word_routine_reconstructs_from_self_generated_oracle_comparisons": True,
            "topology_to_polynomial_binding_under_the_literal_standard_convention": False,
            "status": "UNRESOLVED",
        },
        "preserved_failure_file": str(failure_path),
        "conclusions": {
            "finite_class_membership_claim": "FALSE",
            "ordinary_T_shape_on_serialized_broad_reductions": "EXACTLY COMPUTED",
            "root_collision_closure_as_a_standard_semi_directed_manuscript_lemma": "UNRESOLVED",
            "safe_as_manuscript_lemma": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--failures", type=Path, required=True)
    arguments = parser.parse_args()
    result = audit(arguments.project.resolve(), arguments.failures.resolve())
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["conclusions"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
