#!/usr/bin/env python3
"""Regenerate the complete primitive theta2 five-port directional closure.

The computation starts from the graph grammar and never opens a frozen
descriptor or rank pickle.  It enumerates all 2,946,240 labelled directions,
records a pointwise topology witness for every topology exclusion, rebuilds
all polynomial descriptors, proves exact rank equality from lower minors and
coefficientwise symbolic upper certificates, and closes every surviving
rank-eligible class by an exact quadratic or an explicit labelled
semi-directed graph isomorphism.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import time
from pathlib import Path

from syzygy_upper import upper_certificate
from restoration_closure import generate_restoration_payload
from theta2_common import (
    ARTIFACT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    PERMUTATION_COUNT,
    RAW_PER_SOURCE,
    RAW_TOTAL,
    SOURCE_COUNT,
    TARGET_COUNT,
    atomic_json,
    canonical_json_bytes,
    canonicalizer_sha256,
    descriptor_sha256,
    deterministic_gzip,
    exact_isomorphism_mapping,
    fail,
    load_atlas,
    load_json,
    record_metadata,
    sha_file,
    sha_object,
    topology_decision,
    witness_id,
)


SUMMARY_SCHEMA = "k2p-theta2-five-port-closure-summary-v1"
LEDGER_SCHEMA = "k2p-theta2-five-port-raw-directional-ledger-v1"
RANK_SCHEMA = "k2p-theta2-five-port-exact-rank-certificates-v1"
PROOF_SCHEMA = "k2p-theta2-five-port-direct-proof-certificates-v1"
CLASS_SCHEMA = "k2p-theta2-five-port-class-partition-v1"

EXPECTED_TOPOLOGY_PER_SOURCE = {
    "displayed_quartet_mismatch": 735648,
    "tree_sunlet_strict_sign": 632,
}
EXPECTED_RAW_PER_SOURCE = {
    "quartet_pointwise_excluded": 735648,
    "tree_sunlet_pointwise_excluded": 632,
    "rank_excluded": 200,
    "quadratic_separated": 60,
    "isomorphic": 20,
}
EXPECTED_CLASSES_PER_SOURCE = {
    "rank_excluded": 88,
    "quadratic_separated": 24,
    "isomorphic": 8,
}
PAPER_PDF_SHA256 = "3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5"
TREE_SUNLET_REPLAYER_SHA256 = "3b6c69caf6e72818fe5d931b1c30beabb7860c0c3686d300aff998c48741ccd6"


def topology_universe(atlas):
    sources = tuple(atlas.source_supports(("theta2",)))
    selected_targets = tuple(atlas.target_completions(5, True))
    marginalized_targets = tuple(atlas.target_completions(5, False))
    targets = selected_targets + marginalized_targets
    permutations = tuple(itertools.permutations(range(5)))
    if (
        len(sources) != SOURCE_COUNT
        or len(selected_targets) != 1983
        or len(marginalized_targets) != 4155
        or len(targets) != TARGET_COUNT
        or len(permutations) != PERMUTATION_COUNT
    ):
        fail(
            "THETA2_PRIMITIVE_CENSUS_FAIL",
            (
                len(sources),
                len(selected_targets),
                len(marginalized_targets),
                len(permutations),
            ),
        )
    target_signatures = tuple(
        atlas.topology_signature(atlas.selected_graph_from_completion(target))
        for target in targets
    )
    compatible_by_source = []
    reason_counts_by_source = []
    topology_witnesses = {}
    for source_index, source in enumerate(sources):
        source_signature = atlas.topology_signature(source.graph)
        compatible = []
        reasons = collections.Counter()
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                permuted = atlas.permute_signature(target_signature, permutation)
                content = topology_decision(source_signature, permuted)
                accepted, compiler_reason = atlas.immediate_compatible(
                    source_signature, permuted
                )
                if content is None:
                    if not accepted or compiler_reason is not None:
                        fail(
                            "THETA2_TOPOLOGY_COMPILER_DISAGREEMENT",
                            (source_index, target_index, permutation_index),
                        )
                    compatible.append((target_index, permutation_index))
                else:
                    expected_reason = (
                        "quartet"
                        if content["reason"] == "displayed_quartet_mismatch"
                        else "tree_sunlet"
                    )
                    if accepted or compiler_reason != expected_reason:
                        fail(
                            "THETA2_TOPOLOGY_WITNESS_DISAGREEMENT",
                            (source_index, target_index, permutation_index),
                        )
                    identifier = witness_id(content)
                    previous = topology_witnesses.setdefault(identifier, content)
                    if previous != content:
                        fail("THETA2_TOPOLOGY_WITNESS_HASH_COLLISION", identifier)
                    reasons[content["reason"]] += 1
        if len(compatible) != 280 or dict(reasons) != EXPECTED_TOPOLOGY_PER_SOURCE:
            fail(
                "THETA2_TOPOLOGY_CENSUS_FAIL",
                (source_index, len(compatible), dict(reasons)),
            )
        compatible_by_source.append(tuple(compatible))
        reason_counts_by_source.append(reasons)
        print(
            json.dumps(
                {
                    "source_index": source_index,
                    "topology_survivors": len(compatible),
                    "topology_exclusions": dict(reasons),
                },
                sort_keys=True,
            ),
            flush=True,
        )
    return (
        sources,
        targets,
        permutations,
        target_signatures,
        compatible_by_source,
        reason_counts_by_source,
        topology_witnesses,
    )


def compile_descriptors(atlas, sources, targets, permutations, compatible_by_source):
    compatible_keys = sorted(set().union(*map(set, compatible_by_source)))
    if len(compatible_keys) != 280:
        fail("THETA2_COMPATIBLE_KEY_UNION_FAIL", len(compatible_keys))
    relabelled_records = {}
    descriptors = {}
    descriptors_by_digest = {}
    for target_index, permutation_index in compatible_keys:
        record = atlas.relabel_record(
            targets[target_index], permutations[permutation_index]
        )
        descriptor = atlas.model_descriptor_fast2(record.graph)
        digest = descriptor_sha256(descriptor)
        previous = descriptors_by_digest.setdefault(digest, descriptor)
        if previous != descriptor:
            fail("THETA2_DESCRIPTOR_HASH_COLLISION", digest)
        key = (target_index, permutation_index)
        relabelled_records[key] = record
        descriptors[key] = descriptor
    source_descriptors = []
    for source in sources:
        descriptor = atlas.model_descriptor_fast2(source.graph)
        digest = descriptor_sha256(descriptor)
        previous = descriptors_by_digest.setdefault(digest, descriptor)
        if previous != descriptor:
            fail("THETA2_SOURCE_DESCRIPTOR_HASH_COLLISION", digest)
        source_descriptors.append(descriptor)
    if len(descriptors_by_digest) != 120:
        fail("THETA2_DESCRIPTOR_CENSUS_FAIL", len(descriptors_by_digest))
    return (
        tuple(source_descriptors),
        relabelled_records,
        descriptors,
        descriptors_by_digest,
    )


def rank_certificates(atlas, descriptors_by_digest):
    rows = []
    rank_by_digest = {}
    for ordinal, digest in enumerate(sorted(descriptors_by_digest)):
        descriptor = descriptors_by_digest[digest]
        lower = atlas.rank_certificate(descriptor, salt=0)
        upper = upper_certificate(
            descriptor,
            atlas.output_sparse_polynomials,
            atlas.default_exact_point,
        )
        lower_rank = int(lower["rank"])
        upper_rank = int(upper["certified_rank_upper"])
        if lower_rank != upper_rank:
            fail(
                "THETA2_EXACT_RANK_GAP",
                (digest, lower_rank, upper_rank),
            )
        rank_by_digest[digest] = lower_rank
        rows.append(
            {
                "descriptor_sha256": digest,
                "retic_count": descriptor.retic_count,
                "edge_class_count": descriptor.edge_class_count,
                "parameter_count": 2 * descriptor.edge_class_count
                + descriptor.retic_count,
                "exact_generic_rank": lower_rank,
                "lower_certificate": {
                    "point_recipe": "atlas.default_exact_point(descriptor,salt=0)",
                    "pivot_rows": list(lower["rows"]),
                    "pivot_columns": list(lower["columns"]),
                    "minor_determinant": lower["determinant"],
                },
                "upper_certificate": {
                    **upper,
                    "method": "coefficientwise-polynomial-vector-field-kernel",
                    "identity": "J_f*V=0 over Z[parameters]",
                },
            }
        )
        if (ordinal + 1) % 20 == 0:
            print(
                json.dumps(
                    {
                        "exact_rank_certificates": ordinal + 1,
                        "rank_certificate_total": len(descriptors_by_digest),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    histogram = collections.Counter(rank_by_digest.values())
    if dict(sorted(histogram.items())) != {14: 8, 16: 80, 18: 32}:
        fail("THETA2_RANK_HISTOGRAM_FAIL", dict(histogram))
    return rows, rank_by_digest


def quadratic_certificate(atlas, source_descriptor, target_descriptor):
    result = atlas.quadratic_separator_fast(source_descriptor, target_descriptor)
    if result is None:
        return None
    coordinate_pairs = tuple(tuple(pair) for pair in result["coordinate_pairs"])
    coefficients = tuple(int(value) for value in result["coefficients"])
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    target_products = [
        atlas.sparse_mul(target_outputs[left], target_outputs[right])
        for left, right in coordinate_pairs
    ]
    if atlas.sparse_lincomb(target_products, coefficients):
        fail("THETA2_QUADRATIC_TARGET_NONZERO")
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    source_products = [
        atlas.sparse_mul(source_outputs[left], source_outputs[right])
        for left, right in coordinate_pairs
    ]
    source_pullback = atlas.sparse_lincomb(source_products, coefficients)
    if not source_pullback:
        fail("THETA2_QUADRATIC_SOURCE_ZERO")
    pullback_rows = [
        {"exponent": list(exponent), "coefficient": coefficient}
        for exponent, coefficient in sorted(source_pullback.items())
    ]
    content = {
        "degree": 2,
        "weight": list(result["weight"]),
        "coordinate_pairs": [list(pair) for pair in coordinate_pairs],
        "coefficients": list(coefficients),
        "target_pullback": "identically_zero",
        "source_pullback_terms": pullback_rows,
        "source_pullback_sha256": sha_object(pullback_rows),
    }
    return content


def build_classes(
    atlas,
    sources,
    targets,
    permutations,
    source_descriptors,
    relabelled_records,
    descriptors,
    compatible_by_source,
    rank_by_digest,
):
    class_rows = []
    bindings_by_source = []
    quadratic_certificates = {}
    isomorphism_certificates = {}
    for source_index, source in enumerate(sources):
        source_descriptor = source_descriptors[source_index]
        source_digest = descriptor_sha256(source_descriptor)
        source_rank = rank_by_digest[source_digest]
        if source_rank != 18:
            fail("THETA2_SOURCE_RANK_FAIL", (source_index, source_rank))
        members_by_digest = collections.defaultdict(list)
        for key in compatible_by_source[source_index]:
            members_by_digest[descriptor_sha256(descriptors[key])].append(key)
        class_digests = sorted(members_by_digest)
        if len(class_digests) != 120:
            fail("THETA2_CLASS_CENSUS_FAIL", (source_index, len(class_digests)))
        prepared_source = atlas.prepare_mixed_source(source.graph)
        bindings = {}
        category_counts = collections.Counter()
        raw_counts = collections.Counter()
        for class_id, digest in enumerate(class_digests):
            member_keys = tuple(sorted(members_by_digest[digest]))
            descriptor = descriptors[member_keys[0]]
            target_rank = rank_by_digest[digest]
            certificate_id = f"R:{digest}"
            if target_rank < source_rank:
                category = "rank_excluded"
            else:
                relations = set()
                for key in member_keys:
                    selected_graph = atlas.selected_graph_from_completion(
                        relabelled_records[key]
                    )
                    relations.add(
                        atlas.mixed_relation_exact_prepared(
                            prepared_source, selected_graph
                        )
                    )
                if len(relations) != 1:
                    fail(
                        "THETA2_CLASS_RELATION_NOT_CONSTANT",
                        (source_index, class_id, sorted(relations)),
                    )
                relation = next(iter(relations))
                if relation == "triangle":
                    fail("THETA2_UNEXPECTED_TRIANGLE", (source_index, class_id))
                if relation == "isomorphic":
                    category = "isomorphic"
                    representative = member_keys[0]
                    target_graph = atlas.selected_graph_from_completion(
                        relabelled_records[representative]
                    )
                    mapping = exact_isomorphism_mapping(
                        atlas, source.graph, target_graph
                    )
                    if mapping is None:
                        fail(
                            "THETA2_ISOMORPHISM_MAPPING_MISSING",
                            (source_index, class_id),
                        )
                    content = {
                        "source_index": source_index,
                        "class_id": class_id,
                        "source_descriptor_sha256": source_digest,
                        "target_descriptor_sha256": digest,
                        "representative": {
                            "target_index": representative[0],
                            "permutation_index": representative[1],
                            "port_permutation": list(
                                permutations[representative[1]]
                            ),
                            "target_record": record_metadata(
                                relabelled_records[representative]
                            ),
                        },
                        "mixed_vertex_mapping_source_to_target": mapping,
                        "relation": "exact_labelled_semi_directed_isomorphism",
                    }
                    certificate_id = f"I:{sha_object(content)}"
                    isomorphism_certificates[certificate_id] = content
                elif relation == "none":
                    category = "quadratic_separated"
                    content = quadratic_certificate(
                        atlas, source_descriptor, descriptor
                    )
                    if content is None:
                        fail(
                            "THETA2_UNRESOLVED_RANK_ELIGIBLE_CLASS",
                            (source_index, class_id, digest),
                        )
                    content.update(
                        {
                            "source_index": source_index,
                            "class_id": class_id,
                            "source_descriptor_sha256": source_digest,
                            "target_descriptor_sha256": digest,
                            "direction": "source_not_contained_in_target",
                        }
                    )
                    certificate_id = f"Q:{sha_object(content)}"
                    quadratic_certificates[certificate_id] = content
                else:
                    fail(
                        "THETA2_UNKNOWN_RELATION",
                        (source_index, class_id, relation),
                    )
            member_rows = [
                {
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "raw_id": source_index * RAW_PER_SOURCE
                    + target_index * PERMUTATION_COUNT
                    + permutation_index,
                }
                for target_index, permutation_index in member_keys
            ]
            class_row = {
                "source_index": source_index,
                "source_repair_index": source.repair_index,
                "class_id": class_id,
                "source_descriptor_sha256": source_digest,
                "target_descriptor_sha256": digest,
                "source_rank": source_rank,
                "target_rank": target_rank,
                "category": category,
                "certificate_id": certificate_id,
                "raw_presentation_count": len(member_rows),
                "raw_members": member_rows,
            }
            class_rows.append(class_row)
            for key in member_keys:
                bindings[key] = {
                    "category": category,
                    "class_id": class_id,
                    "target_descriptor_sha256": digest,
                    "target_rank": target_rank,
                    "certificate_id": certificate_id,
                }
            category_counts[category] += 1
            raw_counts[category] += len(member_keys)
        if dict(category_counts) != EXPECTED_CLASSES_PER_SOURCE:
            fail(
                "THETA2_CLASS_PARTITION_FAIL",
                (source_index, dict(category_counts)),
            )
        expected_compatible_raw = {
            key: EXPECTED_RAW_PER_SOURCE[key]
            for key in ("rank_excluded", "quadratic_separated", "isomorphic")
        }
        if dict(raw_counts) != expected_compatible_raw:
            fail(
                "THETA2_CLASS_RAW_PARTITION_FAIL",
                (source_index, dict(raw_counts)),
            )
        bindings_by_source.append(bindings)
        print(
            json.dumps(
                {
                    "source_index": source_index,
                    "class_counts": dict(category_counts),
                    "class_raw_counts": dict(raw_counts),
                },
                sort_keys=True,
            ),
            flush=True,
        )
    if len(quadratic_certificates) != 96 or len(isomorphism_certificates) != 32:
        fail(
            "THETA2_DIRECT_CERTIFICATE_CENSUS_FAIL",
            (len(quadratic_certificates), len(isomorphism_certificates)),
        )
    return (
        class_rows,
        tuple(bindings_by_source),
        quadratic_certificates,
        isomorphism_certificates,
    )


def raw_rows(
    atlas,
    sources,
    target_signatures,
    permutations,
    source_descriptors,
    bindings_by_source,
    topology_witnesses,
):
    for source_index, source in enumerate(sources):
        source_signature = atlas.topology_signature(source.graph)
        source_digest = descriptor_sha256(source_descriptors[source_index])
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                raw_id = (
                    source_index * RAW_PER_SOURCE
                    + target_index * PERMUTATION_COUNT
                    + permutation_index
                )
                base = {
                    "raw_id": raw_id,
                    "source_index": source_index,
                    "source_repair_index": source.repair_index,
                    "source_descriptor_sha256": source_digest,
                    "source_rank": 18,
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                }
                content = topology_decision(
                    source_signature,
                    atlas.permute_signature(target_signature, permutation),
                )
                if content is not None:
                    identifier = witness_id(content)
                    if topology_witnesses.get(identifier) != content:
                        fail("THETA2_RAW_TOPOLOGY_WITNESS_MISSING", raw_id)
                    category = (
                        "quartet_pointwise_excluded"
                        if content["reason"] == "displayed_quartet_mismatch"
                        else "tree_sunlet_pointwise_excluded"
                    )
                    row = {
                        **base,
                        "category": category,
                        "topology_witness_id": identifier,
                    }
                else:
                    binding = bindings_by_source[source_index].get(
                        (target_index, permutation_index)
                    )
                    if binding is None:
                        fail("THETA2_RAW_CLASS_BINDING_MISSING", raw_id)
                    row = {**base, **binding}
                yield canonical_json_bytes(row) + b"\n"


def artifact_metadata(path: Path, plain_sha: str, plain_bytes: int):
    return {
        "sha256": sha_file(path),
        "uncompressed_sha256": plain_sha,
        "uncompressed_bytes": plain_bytes,
    }


def main() -> None:
    if not __debug__:
        fail("THETA2_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--output-root", type=Path, default=ARTIFACT_ROOT)
    args = parser.parse_args()
    started = time.monotonic()
    package_root = args.package_root.resolve()
    output_root = args.output_root.resolve()
    lock = load_json(package_root / "INPUT_LOCK.json")
    atlas = load_atlas(package_root)
    compiler_sha = sha_file(package_root / "atlas/k2p_atlas_core.py")
    canonicalizer_sha = canonicalizer_sha256(atlas)
    if compiler_sha != lock.get("compiler_sha256"):
        fail("THETA2_COMPILER_LOCK_FAIL", compiler_sha)
    if canonicalizer_sha != lock.get("canonicalizer_sha256"):
        fail("THETA2_CANONICALIZER_LOCK_FAIL", canonicalizer_sha)

    (
        sources,
        targets,
        permutations,
        target_signatures,
        compatible_by_source,
        reason_counts_by_source,
        topology_witnesses,
    ) = topology_universe(atlas)
    (
        source_descriptors,
        relabelled_records,
        descriptors,
        descriptors_by_digest,
    ) = compile_descriptors(
        atlas, sources, targets, permutations, compatible_by_source
    )
    rank_rows, rank_by_digest = rank_certificates(atlas, descriptors_by_digest)
    (
        class_rows,
        bindings_by_source,
        quadratic_certificates,
        isomorphism_certificates,
    ) = build_classes(
        atlas,
        sources,
        targets,
        permutations,
        source_descriptors,
        relabelled_records,
        descriptors,
        compatible_by_source,
        rank_by_digest,
    )

    rank_payload = {
        "schema": RANK_SCHEMA,
        "claim": "Exact generic rank equality: nonzero point minor plus coefficientwise symbolic fibre fields.",
        "descriptor_count": len(rank_rows),
        "compiler_sha256": compiler_sha,
        "syzygy_engine_sha256": sha_file(Path(__file__).with_name("syzygy_upper.py")),
        "descriptors": rank_rows,
    }
    proof_payload = {
        "schema": PROOF_SCHEMA,
        "claim_scope": "The strict positive-eigenvalue K2P domain D_plus only.",
        "topology_theorems": {
            "displayed_quartet": {
                "statement": "Unequal displayed-quartet sets have disjoint strict positive K2P images.",
                "citation": "Englander et al. v4, Propositions 2.9-2.10 and Theorem 2.11",
                "reviewed_pdf_sha256": PAPER_PDF_SHA256,
                "mechanism": "zero-versus-strict-positive Fourier linear invariant on a four-leaf marginal",
            },
            "tree_sunlet": {
                "statement": "A three-leaf K2P tree and strict three-sunlet have disjoint D_plus images.",
                "mechanism": "T3 is zero on the tree and has an explicitly strictly negative sunlet pullback",
                "archived_exact_replayer_sha256": TREE_SUNLET_REPLAYER_SHA256,
            },
        },
        "topology_witnesses": {
            key: topology_witnesses[key] for key in sorted(topology_witnesses)
        },
        "quadratic_certificates": {
            key: quadratic_certificates[key]
            for key in sorted(quadratic_certificates)
        },
        "isomorphism_certificates": {
            key: isomorphism_certificates[key]
            for key in sorted(isomorphism_certificates)
        },
        "isomorphic_terminal_anchors": [
            {
                "source_index": row["source_index"],
                "source_repair_index": row["source_repair_index"],
                "class_id": row["class_id"],
                "source_descriptor_sha256": row["source_descriptor_sha256"],
                "target_descriptor_sha256": row["target_descriptor_sha256"],
                "certificate_id": row["certificate_id"],
                "raw_presentation_count": row["raw_presentation_count"],
                "raw_members": row["raw_members"],
                "mixed_vertex_mapping_source_to_target": isomorphism_certificates[
                    row["certificate_id"]
                ]["mixed_vertex_mapping_source_to_target"],
            }
            for row in class_rows
            if row["category"] == "isomorphic"
        ],
    }
    class_payload = {
        "schema": CLASS_SCHEMA,
        "claim": "Every topology-compatible descriptor class occurs exactly once per source repair.",
        "classes": class_rows,
    }
    restoration_payload = generate_restoration_payload(
        atlas,
        sources,
        targets,
        permutations,
        class_rows,
        compiler_sha,
        canonicalizer_sha,
    )

    artifact_meta = {}
    for name, payload in (
        ("exact_rank_certificates.json.gz", rank_payload),
        ("direct_proof_certificates.json.gz", proof_payload),
        ("class_partition.json.gz", class_payload),
        ("fixed_full_restoration_closure.json.gz", restoration_payload),
    ):
        path = output_root / name
        plain_sha, plain_bytes = deterministic_gzip(
            path, (canonical_json_bytes(payload), b"\n")
        )
        artifact_meta[name] = artifact_metadata(path, plain_sha, plain_bytes)

    ledger_path = output_root / "raw_directional_ledger.jsonl.gz"
    ledger_sha, ledger_bytes = deterministic_gzip(
        ledger_path,
        raw_rows(
            atlas,
            sources,
            target_signatures,
            permutations,
            source_descriptors,
            bindings_by_source,
            topology_witnesses,
        ),
    )
    artifact_meta[ledger_path.name] = artifact_metadata(
        ledger_path, ledger_sha, ledger_bytes
    )

    global_raw = {
        key: SOURCE_COUNT * value for key, value in EXPECTED_RAW_PER_SOURCE.items()
    }
    global_classes = {
        key: SOURCE_COUNT * value
        for key, value in EXPECTED_CLASSES_PER_SOURCE.items()
    }
    source_rows = []
    for source_index, source in enumerate(sources):
        source_rows.append(
            {
                "source_index": source_index,
                "core_id": source.core_id,
                "repair_index": source.repair_index,
                "source_descriptor_sha256": descriptor_sha256(
                    source_descriptors[source_index]
                ),
                "source_exact_rank": 18,
                "raw_count": RAW_PER_SOURCE,
                "topology_exclusion_counts": dict(
                    reason_counts_by_source[source_index]
                ),
                "raw_partition": EXPECTED_RAW_PER_SOURCE,
                "class_partition": EXPECTED_CLASSES_PER_SOURCE,
            }
        )
    summary = {
        "schema": SUMMARY_SCHEMA,
        "claim_scope": {
            "proved": "Complete local directed source-to-target closure for all four minimum-repaired primitive theta2 five-port supports under K2P on D_plus, including fixed-full 6/7-port restoration of every dummy-bearing isomorphism anchor.",
            "not_claimed": "This artifact alone is not the global strongly-tree-child level-2 theorem; non-theta2 restoration, gluing, bridge, genericity, and reconstruction remain separate gates.",
        },
        "bindings": {
            "compiler_sha256": compiler_sha,
            "canonicalizer_sha256": canonicalizer_sha,
            "input_lock_sha256": sha_file(package_root / "INPUT_LOCK.json"),
            "syzygy_engine_sha256": sha_file(
                Path(__file__).with_name("syzygy_upper.py")
            ),
            "reviewed_quartet_theorem_pdf_sha256": PAPER_PDF_SHA256,
            "tree_sunlet_exact_replayer_sha256": TREE_SUNLET_REPLAYER_SHA256,
        },
        "primitive_counts": {
            "sources": SOURCE_COUNT,
            "selected_incoming_targets": 1983,
            "marginalized_incoming_targets": 4155,
            "targets": TARGET_COUNT,
            "port_permutations": PERMUTATION_COUNT,
            "raw_per_source": RAW_PER_SOURCE,
            "raw_total": RAW_TOTAL,
            "topology_survivors_per_source": 280,
            "union_topology_survivor_keys": 280,
            "unique_descriptors_including_sources": 120,
        },
        "rank_histogram_unique_descriptors": {"14": 8, "16": 80, "18": 32},
        "raw_partition": global_raw,
        "class_partition": global_classes,
        "unresolved_class_count": 0,
        "restoration_closure": restoration_payload["census"],
        "sources": source_rows,
        "artifacts": artifact_meta,
    }
    summary["payload_sha256_without_hash"] = sha_object(summary)
    atomic_json(output_root / "theta2_five_port_summary.json", summary)
    print(
        "THETA2_FIVE_PORT_PRIMITIVE_CLOSURE_PASS "
        f"raw={RAW_TOTAL} classes={sum(global_classes.values())} unresolved=0 "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
