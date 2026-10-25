#!/usr/bin/env python3
"""Stream the authoritative corrected raw-four and theta2 composites.

Primitive source/target encodings and permutations are regenerated from the
graph grammar.  Historical selector ledgers are byte-bound provenance only:
their selected rows receive new whole-map evidence and their historical
classification fields are never copied into an authoritative row.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path
from typing import Any

from composite_support import (
    ARTIFACTS,
    HERE,
    PACKAGE,
    PROJECT,
    SERIALIZATION,
    atomic_json,
    canonical_bytes,
    deterministic_jsonl_gzip,
    load_gzip_json,
    load_json,
    sha_file,
    sha_object,
    with_payload_hash,
)

STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    iter_canonical_gzip_jsonl,
)


RAW4_TOTAL = 405_216
THETA2_TOTAL = 2_946_240
FORBIDDEN = (
    "tree_sunlet",
    "strict_tree_sunlet_sign",
    "tree_sunlet_pointwise_excluded",
    "tree_sunlet_REVOKED",
)


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise RuntimeError(code if detail is None else f"{code}:{detail}")


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "MODULE_IMPORT_FAIL", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_atlas(name: str):
    return import_module(PACKAGE / "atlas/k2p_atlas_core.py", name)


def split_rows(values) -> list[list[list[int]]]:
    return sorted([[list(split[0]), list(split[1])] for split in values])


def quartet_content(source_signature, permuted_target_signature) -> dict[str, Any] | None:
    _labels, source_quartets, _source_triples = source_signature
    target_quartets, _target_triples = permuted_target_signature
    for (quad, source_set), (target_quad, target_set) in zip(source_quartets, target_quartets):
        require(quad == target_quad, "QUARTET_LABEL_ALIGNMENT_FAIL", (quad, target_quad))
        if source_set == target_set:
            continue
        source_values = set(source_set)
        target_values = set(target_set)
        require(source_values and target_values, "EMPTY_DISPLAYED_QUARTET_SET", quad)
        if len(source_values) == 1:
            split = next(iter(source_values))
            zero_on, positive_on, invariant_kind = "source", "target", "I_singleton"
        elif len(target_values) == 1:
            split = next(iter(target_values))
            zero_on, positive_on, invariant_kind = "target", "source", "I_singleton"
        else:
            difference = target_values - source_values
            if difference:
                split = min(difference, key=repr)
                zero_on, positive_on = "source", "target"
            else:
                split = min(source_values - target_values, key=repr)
                zero_on, positive_on = "target", "source"
            invariant_kind = "J_membership"
        return {
            "distinguished_split": [list(split[0]), list(split[1])],
            "invariant_kind": invariant_kind,
            "quartet": list(quad),
            "reason": "displayed_quartet_mismatch",
            "source_displayed_splits": split_rows(source_values),
            "strictly_positive_on": positive_on,
            "target_displayed_splits": split_rows(target_values),
            "zero_on": zero_on,
        }
    return None


def compact_quartet_binding(content: dict[str, Any]) -> dict[str, Any]:
    digest = sha_object(content)
    return {
        "kind": "exact_displayed_quartet_witness",
        "witness_id": f"Q:{digest}",
        "witness_payload_sha256": digest,
        "quartet": content["quartet"],
        "distinguished_split": content["distinguished_split"],
        "invariant_kind": content["invariant_kind"],
        "zero_on": content["zero_on"],
        "strictly_positive_on": content["strictly_positive_on"],
        "source_displayed_splits_sha256": sha_object(content["source_displayed_splits"]),
        "target_displayed_splits_sha256": sha_object(content["target_displayed_splits"]),
    }


def row_base(
    family: str,
    raw_id: int,
    source_index: int,
    source_descriptor_sha256: str,
    target_index: int,
    permutation_index: int,
    permutation: tuple[int, ...],
) -> dict[str, Any]:
    return {
        "schema": f"k2p-{family}-corrected-composite-row-v1",
        "raw_id": raw_id,
        "source_index": source_index,
        "source_descriptor_sha256": source_descriptor_sha256,
        "target_index": target_index,
        "permutation_index": permutation_index,
        "port_permutation": list(permutation),
    }


def add_classification(
    row: dict[str, Any], category: str, exact_reason: str, evidence: dict[str, Any]
) -> dict[str, Any]:
    row["corrected_category"] = category
    row["exact_reason"] = exact_reason
    row["evidence_binding"] = evidence
    encoded = canonical_bytes(row)
    require(not any(item.encode() in encoded for item in FORBIDDEN), "FORBIDDEN_AUTHORITATIVE_ROW", row["raw_id"])
    return row


def raw4_inputs() -> dict[str, Path]:
    return {
        "atlas": PACKAGE / "atlas/k2p_atlas_core.py",
        "historical_raw_ledger_provenance": PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz",
        "rank_lower": PROJECT / "work/raw_ledger_audit/artifacts/rank_lower_certificates.json.gz",
        "rank_upper": PROJECT / "work/raw_ledger_audit/artifacts/rank_upper_binding.json.gz",
        "class_partition": PROJECT / "work/raw_ledger_audit/artifacts/retained_class_partition.json.gz",
        "whole_map_overlay": PROJECT / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json",
        "whole_map_adversarial_truth": PROJECT / "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json",
        "terminal_registry": ARTIFACTS / "raw4_terminal_certificate_registry.json.gz",
        "restoration_forest": PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    }


def theta2_inputs() -> dict[str, Path]:
    return {
        "atlas": PACKAGE / "atlas/k2p_atlas_core.py",
        "historical_raw_ledger_provenance": PROJECT / "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz",
        "rank_certificates": PROJECT / "work/theta2_five_port_closure/artifacts/exact_rank_certificates.json.gz",
        "direct_certificates": PROJECT / "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz",
        "whole_map_adversarial_truth": PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json",
        "restoration_closure": PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
    }


def raw4_whole_map_binding(overlay: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], dict[str, int]]:
    class_keys = sorted(overlay["canonical_relation_class_multiplicities"])
    class_id = {key: number for number, key in enumerate(class_keys)}
    result = {}
    for item in overlay["coverage"]:
        source_hash = item["source_pullback_sha256"]
        target_hash = item["target_pullback_sha256"]
        key = f"{source_hash}:{target_hash}"
        sign_entry = overlay["sign_certificates"][source_hash]
        sign = sign_entry["sign_certificate"]
        result[int(item["raw_id"])] = {
            "kind": "exact_whole_map_Ti_zero_sign_certificate",
            "Ti_relation_class_id": class_id[key],
            "coordinate_triple": item["source_triple"],
            "chosen_T_orientation_label": item["source_T_orientation_label"],
            "source_pullback_sha256": source_hash,
            "source_pullback_term_count": item["source_pullback_term_count"],
            "source_strict_sign": sign["conclusion"],
            "target_pullback_sha256": target_hash,
            "target_pullback_term_count": 0,
            "target_identically_zero": True,
            "coefficient_certificate_sha256": sign["certificate_sha256"],
            "Bernstein_multidegree": sign["Bernstein_multidegree"],
            "Bernstein_coefficient_count": sign["Bernstein_coefficient_count"],
            "negative_coefficients": sign["negative_coefficients"],
            "zero_coefficients": sign["zero_coefficients"],
            "positive_coefficients": sign["positive_coefficients"],
            "exact_full_graph_relation": item["exact_full_graph_relation"],
            "overlay_evidence_sha256": sha_object({key: value for key, value in item.items() if key != "historical_reason"}),
        }
    require(len(result) == 16_974, "RAW4_WHOLE_MAP_CENSUS", len(result))
    return result, class_id


def forest_root_bindings(forest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for item in forest["first_coverage"]:
        grouped[item["root_id"]].append(item)
    result = {}
    for root_id, children in grouped.items():
        children.sort(key=lambda row: int(row["ordinal"]))
        result[root_id] = {
            "first_child_count": len(children),
            "first_child_row_hash_root": sha_object([row["row_sha256"] for row in children]),
            "first_child_transport_hash_root": sha_object(
                [
                    [row["source_parent_transport_id"], row["target_parent_transport_id"]]
                    for row in children
                ]
            ),
        }
    require(len(result) == 2_540, "RAW4_FOREST_MEMBER_ROOT_CENSUS", len(result))
    return result


def generate_raw4(output: Path, verifier_path: Path) -> dict[str, Any]:
    start = time.monotonic()
    inputs = raw4_inputs()
    for path in inputs.values():
        require(path.is_file(), "RAW4_INPUT_MISSING", path)
    atlas = load_atlas("corrected_composite_raw4_atlas")
    sources = tuple(atlas.source_supports())
    targets = tuple(atlas.target_completions(4, True) + atlas.target_completions(4, False))
    permutations = tuple(itertools.permutations(range(4)))
    require((len(sources), len(targets), len(permutations)) == (6, 2814, 24), "RAW4_PRIMITIVE_CENSUS")
    source_signatures = tuple(atlas.topology_signature(source.graph) for source in sources)
    target_signatures = tuple(atlas.topology_signature(atlas.selected_graph_from_completion(target)) for target in targets)

    lower_payload = load_gzip_json(inputs["rank_lower"])
    upper_payload = load_gzip_json(inputs["rank_upper"])
    lower = {row["descriptor_sha256"]: row for row in lower_payload["descriptors"]}
    upper = {row["raw_ledger_descriptor_sha256"]: row for row in upper_payload["descriptors"]}
    require(set(lower) == set(upper), "RAW4_RANK_DESCRIPTOR_SET")
    class_payload = load_gzip_json(inputs["class_partition"])
    classes = {(row["source_index"], row["canonical_class_id"]): row for row in class_payload["classes"]}
    terminal_payload = load_gzip_json(inputs["terminal_registry"])
    terminal_registry = {
        (row["source_index"], row["class_id"]): row for row in terminal_payload["rows"]
    }
    overlay = load_json(inputs["whole_map_overlay"])
    whole_map, _whole_map_classes = raw4_whole_map_binding(overlay)
    forest = load_json(inputs["restoration_forest"])
    forest_members = forest_root_bindings(forest)

    source_descriptors = tuple(atlas.model_descriptor_fast2(source.graph) for source in sources)
    source_digests = tuple(sha_object(descriptor) for descriptor in source_descriptors)
    source_ranks = tuple(int(lower[digest]["rank"]) for digest in source_digests)
    require(source_ranks == (13, 14, 14, 14, 15, 16), "RAW4_SOURCE_RANKS", source_ranks)
    target_descriptor_cache: dict[tuple[int, int], tuple[str, int]] = {}
    class_by_source: list[dict[str, int]] = [dict() for _ in sources]
    stats: collections.Counter[str] = collections.Counter()
    terminal_classes: set[str] = set()
    terminal_memberships: list[list[Any]] = []
    parent_ids: set[str] = set()
    parent_memberships: list[list[Any]] = []

    def target_descriptor(target_index: int, permutation_index: int) -> tuple[str, int]:
        key = (target_index, permutation_index)
        cached = target_descriptor_cache.get(key)
        if cached is None:
            record = atlas.relabel_record(targets[target_index], permutations[permutation_index])
            descriptor = atlas.model_descriptor_fast2(record.graph)
            digest = sha_object(descriptor)
            require(digest in lower and digest in upper, "RAW4_RANK_BINDING_MISSING", digest)
            require(int(lower[digest]["rank"]) == int(upper[digest]["exact_rank"]), "RAW4_RANK_LOWER_UPPER_GAP", digest)
            cached = (digest, int(lower[digest]["rank"]))
            target_descriptor_cache[key] = cached
        return cached

    def rows():
        for raw_id in range(RAW4_TOTAL):
            source_index, remainder = divmod(raw_id, 2814 * 24)
            target_index, permutation_index = divmod(remainder, 24)
            permutation = permutations[permutation_index]
            base = row_base("raw4", raw_id, source_index, source_digests[source_index], target_index, permutation_index, permutation)
            content = quartet_content(source_signatures[source_index], atlas.permute_signature(target_signatures[target_index], permutation))
            if content is not None:
                category = "displayed_quartet_exclusion"
                row = add_classification(base, category, "source_target_displayed_quartet_sets_differ", compact_quartet_binding(content))
            elif raw_id in whole_map:
                category = "full_map_Ti_strict_sign"
                row = add_classification(base, category, "whole_map_source_strict_sign_target_zero", whole_map[raw_id])
            else:
                target_digest, target_rank = target_descriptor(target_index, permutation_index)
                base["target_descriptor_sha256"] = target_digest
                if target_rank < source_ranks[source_index]:
                    category = "exact_rank_exclusion"
                    row = add_classification(
                        base,
                        category,
                        "target_exact_generic_rank_below_source",
                        {
                            "kind": "matched_exact_rank_lower_symbolic_upper",
                            "source_exact_rank": source_ranks[source_index],
                            "target_exact_rank": target_rank,
                            "target_descriptor_sha256": target_digest,
                            "source_lower_certificate_sha256": sha_object(lower[source_digests[source_index]]),
                            "source_lower_minor_determinant": lower[source_digests[source_index]]["minor_determinant"],
                            "target_lower_certificate_sha256": sha_object(lower[target_digest]),
                            "target_upper_certificate_sha256": sha_object(upper[target_digest]),
                            "target_lower_minor_determinant": lower[target_digest]["minor_determinant"],
                            "target_upper_mechanism": upper[target_digest]["upper_mechanism"],
                        },
                    )
                else:
                    class_map = class_by_source[source_index]
                    if target_digest not in class_map:
                        class_map[target_digest] = len(class_map)
                    class_id = class_map[target_digest]
                    class_row = classes.get((source_index, class_id))
                    require(class_row is not None and class_row["descriptor_sha256"] == target_digest, "RAW4_CLASS_BINDING", (source_index, class_id))
                    class_identifier = f"source_{source_index}:class_{class_id:06d}"
                    if class_row["ledger_category"] == "retained_terminal":
                        category = "direct_terminal_presentation"
                        certificate = terminal_registry.get((source_index, class_id))
                        require(certificate is not None, "RAW4_TERMINAL_CERTIFICATE_MISSING", class_identifier)
                        terminal_classes.add(class_identifier)
                        terminal_memberships.append([raw_id, class_identifier, target_index, list(permutation)])
                        evidence = {
                            "kind": "exact_terminal_class_and_direct_certificate",
                            "terminal_class_id": class_identifier,
                            "terminal_certificate_binding_sha256": certificate["certificate_binding_sha256"],
                            "terminal_certificate_kind": certificate["terminal_certificate"]["kind"],
                            "terminal_registry_payload_sha256": terminal_payload["payload_sha256"],
                        }
                        row = add_classification(base, category, "direct_terminal_certificate", evidence)
                    else:
                        require(class_row["ledger_category"] == "restoration_obligation", "RAW4_CLASS_CATEGORY", class_row)
                        category = "restoration_member_presentation"
                        parent_id = class_row["restoration_obligation_id"]
                        member_root_id = f"s{source_index}:c{class_id}:t{target_index}:p{''.join(map(str, permutation))}"
                        root_binding = forest_members.get(member_root_id)
                        require(root_binding is not None, "RAW4_FOREST_MEMBER_MISSING", member_root_id)
                        transport = {
                            "canonical_parent_id": parent_id,
                            "physical_member_root_id": member_root_id,
                            "source_descriptor_sha256": source_digests[source_index],
                            "target_descriptor_sha256": target_digest,
                            "port_permutation": list(permutation),
                            "direction": "source_to_target",
                        }
                        parent_ids.add(parent_id)
                        parent_memberships.append([raw_id, parent_id, member_root_id, sha_object(transport)])
                        evidence = {
                            "kind": "exact_restoration_parent_and_physical_transport",
                            "restoration_parent_id": parent_id,
                            "physical_member_root_id": member_root_id,
                            "presentation_transport_sha256": sha_object(transport),
                            "forest_payload_sha256": forest["payload_sha256"],
                            **root_binding,
                        }
                        row = add_classification(base, category, "physical_restoration_required", evidence)
            stats[category] += 1
            if (raw_id + 1) % 100_000 == 0:
                print(json.dumps({"family": "raw4", "rows": raw_id + 1, "categories": dict(stats)}, sort_keys=True), flush=True)
            yield row

    roots = deterministic_jsonl_gzip(output, rows())
    expected = {
        "displayed_quartet_exclusion": 360_408,
        "full_map_Ti_strict_sign": 16_974,
        "exact_rank_exclusion": 23_822,
        "direct_terminal_presentation": 1_472,
        "restoration_member_presentation": 2_540,
    }
    require(dict(stats) == expected, "RAW4_CATEGORY_CENSUS", dict(stats))
    terminal_hist = collections.Counter(class_id for _, class_id, _, _ in terminal_memberships)
    parent_hist = collections.Counter(parent for _, parent, _, _ in parent_memberships)
    terminal_mult = {str(key): value for key, value in sorted(collections.Counter(terminal_hist.values()).items())}
    parent_mult = {str(key): value for key, value in sorted(collections.Counter(parent_hist.values()).items())}
    require(len(terminal_classes) == 934 and len(parent_ids) == 997, "RAW4_CLASS_CENSUS")
    summary = {
        "schema": "k2p-raw4-corrected-composite-summary-v1",
        "row_schema": "k2p-raw4-corrected-composite-row-v1",
        "status": "PASS",
        "total_rows": RAW4_TOTAL,
        "distinct_raw_ids": RAW4_TOTAL,
        "raw_id_min": 0,
        "raw_id_max": RAW4_TOTAL - 1,
        "duplicate_raw_ids": 0,
        "missing_raw_ids": 0,
        "missing_evidence_bindings": 0,
        "multiple_evidence_bindings": 0,
        "unresolved": 0,
        "forbidden_rooted_field_count": 0,
        "forbidden_rooted_reason_count": 0,
        "category_counts": expected,
        "serialization": SERIALIZATION,
        "gzip_compresslevel": 6,
        "ledger_sha256": sha_file(output),
        "generator_sha256": sha_file(Path(__file__)),
        "verifier_sha256": sha_file(verifier_path),
        **roots.record(),
        "input_artifact_sha256": {name: sha_file(path) for name, path in inputs.items()},
        "rows_with_source_target_permutation": RAW4_TOTAL,
        "rows_with_evidence_binding": RAW4_TOTAL,
        "quartet_witness_rows": expected["displayed_quartet_exclusion"],
        "full_map_Ti_coverage": {
            "rows": 16_974,
            "whole_map_pullbacks_replayed": 16_974,
            "exact_graph_relation_none_rows": 16_974,
            "coefficient_certificate_rows": 16_974,
            "source_strict_sign_rows": 16_974,
            "target_zero_rows": 16_974,
            "unresolved": 0,
        },
        "rank_certificate_coverage": {
            "rows": 23_822,
            "exact_lower_rows": 23_822,
            "symbolic_upper_rows": 23_822,
            "matched_lower_upper_rows": 23_822,
            "unresolved": 0,
        },
        "terminal_class_bindings": {
            "presentation_rows": 1_472,
            "rows_with_terminal_certificate": 1_472,
            "distinct_class_count": len(terminal_classes),
            "class_multiplicity_histogram": terminal_mult,
            "class_id_hash_root": sha_object(sorted(terminal_classes)),
            "presentation_membership_hash_root": sha_object(terminal_memberships),
            "missing_class_links": 0,
            "multiple_class_links": 0,
            "unresolved": 0,
        },
        "restoration_member_bindings": {
            "presentation_rows": 2_540,
            "rows_with_exactly_one_parent": 2_540,
            "rows_with_transport_binding": 2_540,
            "distinct_parent_count": len(parent_ids),
            "parent_multiplicity_histogram": parent_mult,
            "parent_id_hash_root": sha_object(sorted(parent_ids)),
            "presentation_membership_hash_root": sha_object(parent_memberships),
            "missing_parent_links": 0,
            "multiple_parent_links": 0,
            "unresolved": 0,
        },
    }
    return with_payload_hash(summary)


def theta2_nonquartet_provenance(path: Path) -> dict[int, dict[str, Any]]:
    result = {}
    for row in iter_canonical_gzip_jsonl(path, label=path.name):
        if row.get("category") == "quartet_pointwise_excluded":
            continue
        result[int(row["raw_id"])] = row
    require(len(result) == 3_648, "THETA2_NONQUARTET_PROVENANCE_CENSUS", len(result))
    return result


def theta2_whole_map_bindings(
    atlas,
    sources,
    targets,
    selected_rows: list[dict[str, Any]],
    direct_proofs: dict[str, Any],
    truth: dict[str, Any],
) -> dict[int, dict[str, Any]]:
    core = import_module(
        PROJECT / "work/theta2_sign_reclassification/verify_theta2_full_map_independent.py",
        "corrected_composite_theta2_whole_map_core",
    )
    witnesses = direct_proofs["topology_witnesses"]
    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    metadata = []
    needs: dict[int, set[tuple[int, ...]]] = collections.defaultdict(set)
    for row in selected_rows:
        witness = witnesses[row["topology_witness_id"]]
        triple = tuple(witness["triple"])
        permutation = tuple(row["port_permutation"])
        relabelled = atlas.relabel_record(targets[row["target_index"]], permutation)
        selected = atlas.selected_graph_from_completion(relabelled)
        relation = atlas.mixed_relation_exact_prepared(prepared_sources[row["source_index"]], selected)
        require(relation == "none", "THETA2_WHOLE_MAP_GRAPH_RELATION", (row["raw_id"], relation))
        inverse = {new: old for old, new in enumerate(permutation)}
        mapped_triple = tuple(sorted(inverse[label] for label in triple))
        needs[row["target_index"]].add(mapped_triple)
        metadata.append((row, triple, mapped_triple, permutation))

    source_polynomials = {}
    for source_index, source in enumerate(sources):
        descriptor = atlas.model_descriptor_fast2(source.graph)
        outputs = atlas.output_sparse_polynomials(descriptor)
        triples = {item[1] for item in metadata if item[0]["source_index"] == source_index}
        for triple in triples:
            for orientation in triple:
                polynomial = core.t_pullback(atlas, descriptor, outputs, triple, orientation)
                require(not polynomial, "THETA2_WHOLE_MAP_SOURCE_NONZERO", (source_index, triple, orientation))
                source_polynomials[(source_index, triple, orientation)] = polynomial

    target_polynomials = {}
    chosen = {}
    generated_signs = {}
    for target_index, triples in sorted(needs.items()):
        descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
        outputs = atlas.output_sparse_polynomials(descriptor)
        for triple in sorted(triples):
            candidates = []
            for orientation in triple:
                polynomial = core.t_pullback(atlas, descriptor, outputs, triple, orientation)
                target_polynomials[(target_index, triple, orientation)] = polynomial
                candidates.append((len(polynomial), orientation, polynomial))
            for _, orientation, polynomial in sorted(candidates, key=lambda item: (item[0], item[1])):
                try:
                    sign = core.bernstein_certificate(polynomial)
                except core.Failure:
                    continue
                digest = core.sparse_hash(polynomial)
                generated_signs[digest] = sign
                chosen[(target_index, triple)] = orientation
                break
            require((target_index, triple) in chosen, "THETA2_WHOLE_MAP_NO_SIGN", (target_index, triple))

    class_keys = sorted(truth["canonical_relation_class_multiplicities"])
    class_id = {key: number for number, key in enumerate(class_keys)}
    ordered_truth_hashes = []
    result = {}
    zero_hash = core.sparse_hash({})
    for row, triple, mapped_triple, permutation in metadata:
        mapped_orientation = chosen[(row["target_index"], mapped_triple)]
        relabelled_orientation = permutation[mapped_orientation]
        source_polynomial = source_polynomials[(row["source_index"], triple, relabelled_orientation)]
        target_polynomial = target_polynomials[(row["target_index"], mapped_triple, mapped_orientation)]
        source_hash = core.sparse_hash(source_polynomial)
        target_hash = core.sparse_hash(target_polynomial)
        truth_row = {
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "permutation_index": row["permutation_index"],
            "legacy_witness_triple": list(triple),
            "chosen_T_orientation_label": relabelled_orientation,
            "source_pullback_sha256": source_hash,
            "target_pullback_sha256": target_hash,
            "exact_full_graph_relation": "none",
            "result": "source_zero_strict_target_negative",
        }
        ordered_truth_hashes.append(core.sha(truth_row))
        require(source_hash == zero_hash, "THETA2_WHOLE_MAP_SOURCE_ZERO", row["raw_id"])
        certificate = truth["sign_certificates"].get(target_hash)
        require(certificate is not None, "THETA2_SIGN_CERTIFICATE_MISSING", target_hash)
        sign = certificate["sign"]
        require(generated_signs[target_hash]["certificate_sha256"] == sign["certificate_sha256"], "THETA2_SIGN_CERTIFICATE_DRIFT", target_hash)
        relation_key = f"{source_hash}:{target_hash}"
        result[int(row["raw_id"])] = {
            "kind": "exact_whole_map_Ti_zero_sign_certificate",
            "Ti_relation_class_id": class_id[relation_key],
            "coordinate_triple": list(triple),
            "chosen_T_orientation_label": relabelled_orientation,
            "source_pullback_sha256": source_hash,
            "source_pullback_term_count": 0,
            "source_identically_zero": True,
            "target_pullback_sha256": target_hash,
            "target_pullback_term_count": certificate["pullback_term_count"],
            "target_strict_sign": sign["conclusion"],
            "coefficient_certificate_sha256": sign["certificate_sha256"],
            "Bernstein_multidegree": sign["Bernstein_multidegree"],
            "Bernstein_coefficient_count": sign["Bernstein_coefficient_count"],
            "negative_coefficients": sign["negative_coefficients"],
            "zero_coefficients": sign["zero_coefficients"],
            "positive_coefficients": sign["positive_coefficients"],
            "exact_full_graph_relation": "none",
        }
    require(ordered_truth_hashes == truth["ordered_truth_row_hashes"], "THETA2_ORDERED_WHOLE_MAP_TRUTH_DRIFT")
    require(len(result) == 2_528, "THETA2_WHOLE_MAP_CENSUS", len(result))
    return result


def restoration_descendant_summary(closure: dict[str, Any]) -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    roots = {int(row["base_raw_id"]): row for row in closure["restoration_roots"]}
    require(len(roots) == 56, "THETA2_RESTORATION_ROOT_CENSUS", len(roots))
    six = closure["six_port_rows"]
    seven = closure["seven_port_rows"]
    all_rows = list(six) + list(seven)
    child_ids = [row["path_id"] for row in all_rows]
    require(len(child_ids) == len(set(child_ids)) == 864, "THETA2_DESCENDANT_ID_CENSUS")
    edges = []
    transports = []
    first_by_raw: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    leaves = collections.Counter()
    for row in six:
        first_by_raw[int(row["base_raw_id"])].append(row)
        edges.append([f"raw:{row['base_raw_id']}", row["path_id"]])
        transports.append(
            {
                "child_id": row["path_id"],
                "parent_id": f"raw:{row['base_raw_id']}",
                "restored_label": row["restored_label"],
                "restored_role": row["restored_role"],
                "source_insertion": row["source_insertion"],
                "certificate_id": row["certificate_id"],
            }
        )
        if row["category"] == "quartet_pointwise_excluded":
            leaves["displayed_quartet_exclusion"] += 1
        elif not row["remaining_roles"]:
            leaves["labelled_isomorphism"] += 1
    for row in seven:
        edges.append([row["parent_path_id"], row["path_id"]])
        transports.append(
            {
                "child_id": row["path_id"],
                "parent_id": row["parent_path_id"],
                "restored_label": row["restored_label"],
                "restored_role": row["restored_role"],
                "source_insertion": row["source_insertion"],
                "certificate_id": row["certificate_id"],
            }
        )
        leaves["displayed_quartet_exclusion" if row["category"] == "quartet_pointwise_excluded" else "labelled_isomorphism"] += 1
    require(leaves == {"displayed_quartet_exclusion": 760, "labelled_isomorphism": 72}, "THETA2_DESCENDANT_LEAVES", leaves)
    per_root = {}
    for raw_id, root in roots.items():
        children = sorted(first_by_raw[raw_id], key=lambda row: row["path_id"])
        require(children, "THETA2_ROOT_NO_CHILD", raw_id)
        per_root[raw_id] = {
            "anchor_id": root["anchor_id"],
            "descendant_root_sha256": sha_object(root),
            "first_child_count": len(children),
            "first_child_id_hash_root": sha_object([row["path_id"] for row in children]),
        }
    summary = {
        "root_count": len(roots),
        "covered_root_count": len(per_root),
        "generated_child_count": len(all_rows),
        "distinct_child_ids": len(set(child_ids)),
        "children_with_exactly_one_parent": len(all_rows),
        "edge_count": len(edges),
        "transport_restrictions_replayed": len(transports),
        "leaf_count": sum(leaves.values()),
        "leaf_category_counts": dict(leaves),
        "child_id_hash_root": sha_object(sorted(child_ids)),
        "parent_child_edge_hash_root": sha_object(sorted(edges)),
        "transport_restriction_hash_root": sha_object(sorted(transports, key=lambda row: row["child_id"])),
        "duplicate_child_ids": 0,
        "missing_parent_links": 0,
        "multiple_parent_links": 0,
        "missing_continuation_layers": 0,
        "cycles": 0,
        "unresolved": 0,
    }
    return summary, per_root


def generate_theta2(output: Path, verifier_path: Path) -> dict[str, Any]:
    start = time.monotonic()
    inputs = theta2_inputs()
    for path in inputs.values():
        require(path.is_file(), "THETA2_INPUT_MISSING", path)
    atlas = load_atlas("corrected_composite_theta2_atlas")
    sources = tuple(atlas.source_supports(("theta2",)))
    targets = tuple(atlas.target_completions(5, True) + atlas.target_completions(5, False))
    permutations = tuple(itertools.permutations(range(5)))
    require((len(sources), len(targets), len(permutations)) == (4, 6138, 120), "THETA2_PRIMITIVE_CENSUS")
    source_signatures = tuple(atlas.topology_signature(source.graph) for source in sources)
    target_signatures = tuple(atlas.topology_signature(atlas.selected_graph_from_completion(target)) for target in targets)
    source_digests = tuple(sha_object(atlas.model_descriptor_fast2(source.graph)) for source in sources)
    remaining = theta2_nonquartet_provenance(inputs["historical_raw_ledger_provenance"])
    direct = load_gzip_json(inputs["direct_certificates"])
    rank_payload = load_gzip_json(inputs["rank_certificates"])
    ranks = {row["descriptor_sha256"]: row for row in rank_payload["descriptors"]}
    truth = load_json(inputs["whole_map_adversarial_truth"])
    selected = sorted(
        (row for row in remaining.values() if row["category"] == "tree_sunlet_pointwise_excluded"),
        key=lambda row: row["raw_id"],
    )
    whole_map = theta2_whole_map_bindings(atlas, sources, targets, selected, direct, truth)
    closure = load_gzip_json(inputs["restoration_closure"])
    descendant_summary, descendant_roots = restoration_descendant_summary(closure)
    stats: collections.Counter[str] = collections.Counter()
    direct_rows = 0

    def rows():
        nonlocal direct_rows
        for raw_id in range(THETA2_TOTAL):
            source_index, remainder = divmod(raw_id, 6138 * 120)
            target_index, permutation_index = divmod(remainder, 120)
            permutation = permutations[permutation_index]
            base = row_base("theta2", raw_id, source_index, source_digests[source_index], target_index, permutation_index, permutation)
            content = quartet_content(source_signatures[source_index], atlas.permute_signature(target_signatures[target_index], permutation))
            if content is not None:
                category = "displayed_quartet_exclusion"
                row = add_classification(base, category, "source_target_displayed_quartet_sets_differ", compact_quartet_binding(content))
            else:
                old = remaining.get(raw_id)
                require(old is not None, "THETA2_NONQUARTET_ROW_MISSING", raw_id)
                if raw_id in whole_map:
                    category = "full_map_Ti_strict_sign"
                    row = add_classification(base, category, "whole_map_source_zero_target_strict_sign", whole_map[raw_id])
                elif old["category"] == "rank_excluded":
                    category = "exact_rank_exclusion"
                    target_digest = old["target_descriptor_sha256"]
                    certificate = ranks[target_digest]
                    require(int(certificate["exact_generic_rank"]) == int(old["target_rank"]), "THETA2_RANK_BINDING", raw_id)
                    base["target_descriptor_sha256"] = target_digest
                    row = add_classification(
                        base,
                        category,
                        "target_exact_generic_rank_below_source",
                        {
                            "kind": "matched_exact_rank_lower_symbolic_upper",
                            "source_exact_rank": old["source_rank"],
                            "target_exact_rank": certificate["exact_generic_rank"],
                            "target_descriptor_sha256": target_digest,
                            "source_lower_certificate_sha256": sha_object(ranks[source_digests[source_index]]["lower_certificate"]),
                            "source_lower_minor_determinant": ranks[source_digests[source_index]]["lower_certificate"]["minor_determinant"],
                            "target_lower_certificate_sha256": sha_object(certificate["lower_certificate"]),
                            "target_upper_certificate_sha256": sha_object(certificate["upper_certificate"]),
                            "target_lower_minor_determinant": certificate["lower_certificate"]["minor_determinant"],
                            "target_upper_mechanism": certificate["upper_certificate"]["method"],
                        },
                    )
                elif old["category"] == "quadratic_separated":
                    category = "direct_quadratic_separator"
                    certificate = direct["quadratic_certificates"][old["certificate_id"]]
                    base["target_descriptor_sha256"] = old["target_descriptor_sha256"]
                    direct_rows += 1
                    row = add_classification(
                        base,
                        category,
                        "exact_quadratic_target_zero_source_nonzero",
                        {
                            "kind": "exact_multihomogeneous_quadratic_separator",
                            "certificate_id": old["certificate_id"],
                            "certificate_sha256": sha_object(certificate),
                            "degree": certificate["degree"],
                            "source_pullback_sha256": certificate["source_pullback_sha256"],
                            "target_pullback": certificate["target_pullback"],
                            "class_id": old["class_id"],
                        },
                    )
                elif old["category"] == "isomorphic":
                    category = "labelled_isomorphism"
                    certificate = direct["isomorphism_certificates"][old["certificate_id"]]
                    base["target_descriptor_sha256"] = old["target_descriptor_sha256"]
                    evidence = {
                        "kind": "exact_labelled_semi_directed_isomorphism",
                        "certificate_id": old["certificate_id"],
                        "certificate_sha256": sha_object(certificate),
                        "mixed_vertex_mapping_sha256": sha_object(certificate["mixed_vertex_mapping_source_to_target"]),
                        "class_id": old["class_id"],
                    }
                    if raw_id in descendant_roots:
                        evidence["physical_restoration_descendants"] = descendant_roots[raw_id]
                    direct_rows += 1
                    row = add_classification(base, category, "exact_labelled_graph_isomorphism", evidence)
                else:
                    raise RuntimeError(f"THETA2_UNEXPECTED_NONQUARTET_CATEGORY:{raw_id}:{old['category']}")
            stats[category] += 1
            if (raw_id + 1) % 500_000 == 0:
                print(json.dumps({"family": "theta2", "rows": raw_id + 1, "categories": dict(stats)}, sort_keys=True), flush=True)
            yield row

    roots = deterministic_jsonl_gzip(output, rows())
    expected = {
        "displayed_quartet_exclusion": 2_942_592,
        "full_map_Ti_strict_sign": 2_528,
        "exact_rank_exclusion": 800,
        "direct_quadratic_separator": 240,
        "labelled_isomorphism": 80,
    }
    require(dict(stats) == expected, "THETA2_CATEGORY_CENSUS", dict(stats))
    require(direct_rows == 320, "THETA2_DIRECT_CENSUS", direct_rows)
    summary = {
        "schema": "k2p-theta2-corrected-composite-summary-v1",
        "row_schema": "k2p-theta2-corrected-composite-row-v1",
        "status": "PASS",
        "total_rows": THETA2_TOTAL,
        "distinct_raw_ids": THETA2_TOTAL,
        "raw_id_min": 0,
        "raw_id_max": THETA2_TOTAL - 1,
        "duplicate_raw_ids": 0,
        "missing_raw_ids": 0,
        "missing_evidence_bindings": 0,
        "multiple_evidence_bindings": 0,
        "unresolved": 0,
        "forbidden_rooted_field_count": 0,
        "forbidden_rooted_reason_count": 0,
        "category_counts": expected,
        "serialization": SERIALIZATION,
        "gzip_compresslevel": 6,
        "ledger_sha256": sha_file(output),
        "generator_sha256": sha_file(Path(__file__)),
        "verifier_sha256": sha_file(verifier_path),
        **roots.record(),
        "input_artifact_sha256": {name: sha_file(path) for name, path in inputs.items()},
        "rows_with_source_target_permutation": THETA2_TOTAL,
        "rows_with_evidence_binding": THETA2_TOTAL,
        "quartet_witness_rows": expected["displayed_quartet_exclusion"],
        "full_map_Ti_coverage": {
            "rows": 2_528,
            "whole_map_pullbacks_replayed": 2_528,
            "exact_graph_relation_none_rows": 2_528,
            "coefficient_certificate_rows": 2_528,
            "source_zero_rows": 2_528,
            "target_strict_sign_rows": 2_528,
            "unresolved": 0,
        },
        "rank_certificate_coverage": {
            "rows": 800,
            "exact_lower_rows": 800,
            "symbolic_upper_rows": 800,
            "matched_lower_upper_rows": 800,
            "unresolved": 0,
        },
        "direct_certificate_rows": direct_rows,
        "restoration_descendants": descendant_summary,
    }
    return with_payload_hash(summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("raw4", "theta2", "all"), default="all")
    parser.add_argument("--artifacts", type=Path, default=ARTIFACTS)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "verify_corrected_composites_independent.py",
    )
    args = parser.parse_args()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    families = ("raw4", "theta2") if args.family == "all" else (args.family,)
    for family in families:
        ledger = args.artifacts / f"{family}_corrected_composite_ledger.jsonl.gz"
        summary_path = args.artifacts / f"{family}_corrected_composite_summary.json"
        summary = generate_raw4(ledger, args.verifier) if family == "raw4" else generate_theta2(ledger, args.verifier)
        atomic_json(summary_path, summary)
        print(json.dumps({"family": family, "status": "PASS", "rows": summary["total_rows"], "ledger_sha256": summary["ledger_sha256"], "payload_sha256": summary["payload_sha256"]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (
        StrictJSONError,
        KeyError,
        OSError,
        ValueError,
        RuntimeError,
        json.JSONDecodeError,
    ) as error:
        raise SystemExit(f"CORRECTED_COMPOSITE_GENERATION_FAIL:{error}") from error
