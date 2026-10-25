#!/usr/bin/env python3
"""Regenerate the complete four-port directional ledger from primitive graphs.

This generator deliberately never opens ``descriptors_4.pkl`` or
``rank_certs_4.pkl``.  The frozen manifests are consulted only after primitive
graph generation, descriptor compilation, and exact point-rank computation,
to bind regenerated descriptor classes to the currently published terminal or
restoration classifications.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import hashlib
import itertools
import json
import time
from pathlib import Path

from ledger_common import (
    AUDIT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    atomic_json,
    canonical_json_bytes,
    canonicalizer_sha256,
    deterministic_gzip,
    fail,
    load_atlas,
    load_json,
    sha_file,
    sha_object,
)
from rank_upper_binding import verify_and_bind_rank_upper


SCHEMA = "k2p-four-port-raw-directional-ledger-v1"
RANK_SCHEMA = "k2p-four-port-regenerated-rank-lower-certificates-v1"
SUMMARY_SCHEMA = "k2p-four-port-raw-ledger-summary-v1"
SOURCE_COUNT = 6
TARGET_COUNT = 2814
PERMUTATION_COUNT = 24
RAW_PER_SOURCE = TARGET_COUNT * PERMUTATION_COUNT
RAW_TOTAL = SOURCE_COUNT * RAW_PER_SOURCE
EXPECTED_SOURCE_CLASS_COUNTS = (536, 747, 276, 276, 64, 32)
EXPECTED_SOURCE_RANKS = (13, 14, 14, 14, 15, 16)
EXPECTED_STATUS_COUNTS = {
    "separated": 845,
    "isomorphic": 20,
    "triangle": 35,
    "restoration_parent": 997,
    "unresolved": 34,
    "error": 0,
}


def descriptor_hash(descriptor) -> str:
    return sha_object(descriptor)


def topology_universe(atlas):
    sources = tuple(atlas.source_supports())
    selected_targets = tuple(atlas.target_completions(4, True))
    marginalized_targets = tuple(atlas.target_completions(4, False))
    targets = selected_targets + marginalized_targets
    permutations = tuple(itertools.permutations(range(4)))
    if (
        len(sources) != SOURCE_COUNT
        or len(selected_targets) != 831
        or len(marginalized_targets) != 1983
        or len(targets) != TARGET_COUNT
        or len(permutations) != PERMUTATION_COUNT
    ):
        fail(
            "RAW_LEDGER_PRIMITIVE_CENSUS_FAIL",
            (len(sources), len(selected_targets), len(marginalized_targets), len(permutations)),
        )
    target_signatures = tuple(
        atlas.topology_signature(atlas.selected_graph_from_completion(target))
        for target in targets
    )
    compatible_by_source: list[list[tuple[int, tuple[int, ...]]]] = []
    exclusion_reason_counts: list[collections.Counter[str]] = []
    for source in sources:
        source_signature = atlas.topology_signature(source.graph)
        compatible = []
        reasons: collections.Counter[str] = collections.Counter()
        for target_index, target_signature in enumerate(target_signatures):
            for permutation in permutations:
                accepted, reason = atlas.immediate_compatible(
                    source_signature,
                    atlas.permute_signature(target_signature, permutation),
                )
                if accepted:
                    compatible.append((target_index, permutation))
                else:
                    if reason not in {"quartet", "tree_sunlet"}:
                        fail("RAW_LEDGER_TOPOLOGY_REASON_FAIL", reason)
                    reasons[reason] += 1
        compatible_by_source.append(compatible)
        exclusion_reason_counts.append(reasons)
    return (
        sources,
        targets,
        permutations,
        target_signatures,
        compatible_by_source,
        exclusion_reason_counts,
    )


def compile_descriptors(atlas, sources, targets, compatible_by_source):
    source_descriptors = tuple(atlas.model_descriptor_fast2(source.graph) for source in sources)
    compatible_keys = sorted(set().union(*map(set, compatible_by_source)))
    target_descriptors = {}
    descriptors_by_hash = {}
    for ordinal, (target_index, permutation) in enumerate(compatible_keys):
        relabelled = atlas.relabel_record(targets[target_index], permutation)
        descriptor = atlas.model_descriptor_fast2(relabelled.graph)
        digest = descriptor_hash(descriptor)
        previous = descriptors_by_hash.setdefault(digest, descriptor)
        if previous != descriptor:
            fail("RAW_LEDGER_DESCRIPTOR_HASH_COLLISION", digest)
        target_descriptors[(target_index, permutation)] = descriptor
        if ordinal and ordinal % 1000 == 0:
            print(
                json.dumps(
                    {
                        "descriptor_keys_compiled": ordinal,
                        "compatible_key_total": len(compatible_keys),
                        "unique_descriptors": len(descriptors_by_hash),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    for descriptor in source_descriptors:
        digest = descriptor_hash(descriptor)
        previous = descriptors_by_hash.setdefault(digest, descriptor)
        if previous != descriptor:
            fail("RAW_LEDGER_SOURCE_DESCRIPTOR_HASH_COLLISION", digest)
    return source_descriptors, target_descriptors, descriptors_by_hash


def regenerate_rank_lower_certificates(atlas, descriptors_by_hash):
    rows = []
    rank_by_hash = {}
    for ordinal, digest in enumerate(sorted(descriptors_by_hash)):
        descriptor = descriptors_by_hash[digest]
        certificate = atlas.rank_certificate(descriptor, salt=0)
        rank = int(certificate["rank"])
        rank_by_hash[digest] = rank
        rows.append(
            {
                "descriptor_sha256": digest,
                "retic_count": descriptor.retic_count,
                "edge_class_count": descriptor.edge_class_count,
                "parameter_count": 2 * descriptor.edge_class_count + descriptor.retic_count,
                "rank": rank,
                "pivot_rows": list(certificate["rows"]),
                "pivot_columns": list(certificate["columns"]),
                "minor_determinant": certificate["determinant"],
                "point_recipe": "atlas.default_exact_point(descriptor,salt=0)",
            }
        )
        if ordinal and ordinal % 500 == 0:
            print(
                json.dumps(
                    {"rank_certificates": ordinal, "rank_total": len(descriptors_by_hash)},
                    sort_keys=True,
                ),
                flush=True,
            )
    return rows, rank_by_hash


def load_manifest_bindings(package_root: Path):
    result_root = package_root / "results/four_port_release_v4"
    manifests = []
    status_counts: collections.Counter[str] = collections.Counter()
    for source_index, expected_count in enumerate(EXPECTED_SOURCE_CLASS_COUNTS):
        manifest = load_json(result_root / f"source_{source_index}/residual_manifest.json")
        records = manifest.get("records")
        if (
            manifest.get("source_index") != source_index
            or manifest.get("canonical_class_count") != expected_count
            or not isinstance(records, list)
            or len(records) != expected_count
            or [row.get("canonical_class_id") for row in records] != list(range(expected_count))
        ):
            fail("RAW_LEDGER_MANIFEST_CENSUS_FAIL", source_index)
        status_counts.update(row.get("status") for row in records)
        manifests.append(manifest)
    observed_status_counts = {
        status: status_counts.get(status, 0) for status in EXPECTED_STATUS_COUNTS
    }
    if observed_status_counts != EXPECTED_STATUS_COUNTS:
        fail("RAW_LEDGER_MANIFEST_STATUS_FAIL", observed_status_counts)

    overlay = load_json(
        package_root / "proofs/four_port_direct_residual_closure_certificate.json"
    )
    if overlay.get("remaining_unproved_among_36") != 0:
        fail("RAW_LEDGER_DIRECT_OVERLAY_INCOMPLETE")
    covered = {tuple(row) for row in overlay.get("covered_candidate_classes", [])}
    unresolved = {
        (source_index, row["canonical_class_id"])
        for source_index, manifest in enumerate(manifests)
        for row in manifest["records"]
        if row["status"] == "unresolved"
    }
    if not unresolved <= covered:
        fail("RAW_LEDGER_UNRESOLVED_NOT_OVERLAID", sorted(unresolved - covered))
    return manifests, overlay


def build_classes(
    source_descriptors,
    target_descriptors,
    compatible_by_source,
    rank_by_hash,
    manifests,
):
    raw_bindings = []
    class_rows = []
    rank_excluded_by_source = []
    for source_index, (source_descriptor, compatible, manifest) in enumerate(
        zip(source_descriptors, compatible_by_source, manifests)
    ):
        source_digest = descriptor_hash(source_descriptor)
        source_rank = rank_by_hash[source_digest]
        if source_rank != EXPECTED_SOURCE_RANKS[source_index]:
            fail("RAW_LEDGER_SOURCE_RANK_FAIL", (source_index, source_rank))
        seen = {}
        members: list[list[tuple[int, tuple[int, ...]]]] = []
        rank_excluded = set()
        for raw_key in compatible:
            target_descriptor = target_descriptors[raw_key]
            target_digest = descriptor_hash(target_descriptor)
            target_rank = rank_by_hash[target_digest]
            if target_rank < source_rank:
                rank_excluded.add(raw_key)
                continue
            if target_descriptor not in seen:
                seen[target_descriptor] = len(members)
                members.append([])
            members[seen[target_descriptor]].append(raw_key)
        if len(members) != EXPECTED_SOURCE_CLASS_COUNTS[source_index]:
            fail("RAW_LEDGER_REGENERATED_CLASS_CENSUS_FAIL", (source_index, len(members)))
        if len(manifest["records"]) != len(members):
            fail("RAW_LEDGER_CLASS_MANIFEST_LENGTH_FAIL", source_index)
        source_binding = {}
        for class_id, class_members in enumerate(members):
            descriptor = target_descriptors[class_members[0]]
            digest = descriptor_hash(descriptor)
            manifest_row = manifest["records"][class_id]
            if manifest_row.get("descriptor_sha256") != digest:
                fail(
                    "RAW_LEDGER_CLASS_DESCRIPTOR_BINDING_FAIL",
                    (source_index, class_id, digest, manifest_row.get("descriptor_sha256")),
                )
            status = manifest_row.get("status")
            category = (
                "restoration_obligation"
                if status == "restoration_parent"
                else "retained_terminal"
            )
            obligation_id = (
                f"source_{source_index}:class_{class_id:06d}"
                if category == "restoration_obligation"
                else None
            )
            for raw_key in class_members:
                source_binding[raw_key] = {
                    "category": category,
                    "class_id": class_id,
                    "status": status,
                    "descriptor_sha256": digest,
                    "target_rank": rank_by_hash[digest],
                    "restoration_obligation_id": obligation_id,
                }
            class_rows.append(
                {
                    "source_index": source_index,
                    "canonical_class_id": class_id,
                    "descriptor_sha256": digest,
                    "target_rank": rank_by_hash[digest],
                    "status_before_direct_overlay": status,
                    "ledger_category": category,
                    "raw_presentation_count": len(class_members),
                    "restoration_obligation_id": obligation_id,
                }
            )
        if len(source_binding) + len(rank_excluded) != len(compatible):
            fail("RAW_LEDGER_ELIGIBLE_PARTITION_FAIL", source_index)
        raw_bindings.append(source_binding)
        rank_excluded_by_source.append(rank_excluded)
    return raw_bindings, rank_excluded_by_source, class_rows


def raw_rows(
    atlas,
    sources,
    targets,
    permutations,
    target_signatures,
    source_descriptors,
    target_descriptors,
    rank_by_hash,
    raw_bindings,
    rank_excluded_by_source,
):
    for source_index, source in enumerate(sources):
        source_signature = atlas.topology_signature(source.graph)
        source_digest = descriptor_hash(source_descriptors[source_index])
        source_rank = rank_by_hash[source_digest]
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                raw_id = (
                    source_index * RAW_PER_SOURCE
                    + target_index * PERMUTATION_COUNT
                    + permutation_index
                )
                raw_key = (target_index, permutation)
                accepted, reason = atlas.immediate_compatible(
                    source_signature,
                    atlas.permute_signature(target_signature, permutation),
                )
                base = {
                    "raw_id": raw_id,
                    "source_index": source_index,
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                    "source_descriptor_sha256": source_digest,
                    "source_rank": source_rank,
                }
                if not accepted:
                    row = {
                        **base,
                        "category": "topology_excluded",
                        "topology_exclusion_reason": reason,
                    }
                elif raw_key in rank_excluded_by_source[source_index]:
                    target_descriptor = target_descriptors[raw_key]
                    target_digest = descriptor_hash(target_descriptor)
                    row = {
                        **base,
                        "category": "rank_excluded",
                        "descriptor_sha256": target_digest,
                        "target_rank": rank_by_hash[target_digest],
                    }
                else:
                    binding = raw_bindings[source_index].get(raw_key)
                    if binding is None:
                        fail("RAW_LEDGER_RAW_BINDING_MISSING", (source_index, raw_key))
                    row = {**base, **binding}
                yield canonical_json_bytes(row) + b"\n"


def main() -> None:
    if not __debug__:
        fail("RAW_LEDGER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--output-root", type=Path, default=AUDIT_ROOT / "artifacts")
    parser.add_argument(
        "--rank-upper-root",
        type=Path,
        default=AUDIT_ROOT.parent / "rank_upper_certificates",
    )
    args = parser.parse_args()
    started = time.monotonic()
    package_root = args.package_root.resolve()
    output_root = args.output_root.resolve()
    lock = load_json(package_root / "INPUT_LOCK.json")
    atlas = load_atlas(package_root)
    compiler_sha = sha_file(package_root / "atlas/k2p_atlas_core.py")
    canon_sha = canonicalizer_sha256(atlas)
    if compiler_sha != lock.get("compiler_sha256"):
        fail("RAW_LEDGER_COMPILER_LOCK_FAIL", compiler_sha)
    if canon_sha != lock.get("canonicalizer_sha256"):
        fail("RAW_LEDGER_CANONICALIZER_LOCK_FAIL", canon_sha)

    (
        sources,
        targets,
        permutations,
        target_signatures,
        compatible_by_source,
        exclusion_reason_counts,
    ) = topology_universe(atlas)
    source_descriptors, target_descriptors, descriptors_by_hash = compile_descriptors(
        atlas, sources, targets, compatible_by_source
    )
    rank_rows, rank_by_hash = regenerate_rank_lower_certificates(
        atlas, descriptors_by_hash
    )
    rank_upper_payload = verify_and_bind_rank_upper(
        atlas,
        descriptors_by_hash,
        rank_by_hash,
        args.rank_upper_root.resolve(),
    )
    manifests, overlay = load_manifest_bindings(package_root)
    raw_bindings, rank_excluded_by_source, class_rows = build_classes(
        source_descriptors,
        target_descriptors,
        compatible_by_source,
        rank_by_hash,
        manifests,
    )

    rank_payload = {
        "schema": RANK_SCHEMA,
        "claim_scope": "Exact lower bounds only; upper-bound closure is a separate required certificate.",
        "compiler_sha256": compiler_sha,
        "canonicalizer_sha256": canon_sha,
        "descriptor_count": len(rank_rows),
        "descriptors": rank_rows,
    }
    rank_plain_sha, rank_plain_bytes = deterministic_gzip(
        output_root / "rank_lower_certificates.json.gz",
        (canonical_json_bytes(rank_payload), b"\n"),
    )
    upper_plain_sha, upper_plain_bytes = deterministic_gzip(
        output_root / "rank_upper_binding.json.gz",
        (canonical_json_bytes(rank_upper_payload), b"\n"),
    )
    class_plain_sha, class_plain_bytes = deterministic_gzip(
        output_root / "retained_class_partition.json.gz",
        (canonical_json_bytes({"schema": SCHEMA, "classes": class_rows}), b"\n"),
    )
    ledger_path = output_root / "raw_directional_ledger.jsonl.gz"
    ledger_plain_sha, ledger_plain_bytes = deterministic_gzip(
        ledger_path,
        raw_rows(
            atlas,
            sources,
            targets,
            permutations,
            target_signatures,
            source_descriptors,
            target_descriptors,
            rank_by_hash,
            raw_bindings,
            rank_excluded_by_source,
        ),
    )

    category_counts = collections.Counter()
    source_rows = []
    restoration_classes = 0
    terminal_classes = 0
    for source_index in range(SOURCE_COUNT):
        topology_compatible = len(compatible_by_source[source_index])
        rank_excluded = len(rank_excluded_by_source[source_index])
        binding_counts = collections.Counter(
            row["category"] for row in raw_bindings[source_index].values()
        )
        topology_excluded = RAW_PER_SOURCE - topology_compatible
        row_counts = {
            "topology_excluded": topology_excluded,
            "rank_excluded": rank_excluded,
            "retained_terminal": binding_counts["retained_terminal"],
            "restoration_obligation": binding_counts["restoration_obligation"],
        }
        if sum(row_counts.values()) != RAW_PER_SOURCE:
            fail("RAW_LEDGER_SOURCE_PARTITION_SUM_FAIL", (source_index, row_counts))
        category_counts.update(row_counts)
        source_class_rows = [row for row in class_rows if row["source_index"] == source_index]
        source_restoration_classes = sum(
            row["ledger_category"] == "restoration_obligation"
            for row in source_class_rows
        )
        source_terminal_classes = len(source_class_rows) - source_restoration_classes
        restoration_classes += source_restoration_classes
        terminal_classes += source_terminal_classes
        source_rows.append(
            {
                "source_index": source_index,
                "source_core": sources[source_index].core_id,
                "source_repair_index": sources[source_index].repair_index,
                "source_rank": rank_by_hash[descriptor_hash(source_descriptors[source_index])],
                "raw_count": RAW_PER_SOURCE,
                "topology_compatible": topology_compatible,
                "topology_exclusion_reasons": dict(sorted(exclusion_reason_counts[source_index].items())),
                "partition_counts": row_counts,
                "retained_class_count": len(source_class_rows),
                "terminal_class_count": source_terminal_classes,
                "restoration_obligation_count": source_restoration_classes,
            }
        )
    if sum(category_counts.values()) != RAW_TOTAL:
        fail("RAW_LEDGER_GLOBAL_PARTITION_SUM_FAIL", dict(category_counts))
    if restoration_classes != 997 or terminal_classes != 934:
        fail(
            "RAW_LEDGER_RETAINED_CLASS_PARTITION_FAIL",
            (terminal_classes, restoration_classes),
        )

    rank_histogram = collections.Counter(row["rank"] for row in rank_rows)
    summary = {
        "schema": SUMMARY_SCHEMA,
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generation_seconds": time.monotonic() - started,
        "scope": {
            "claim": "Primitive regeneration and exact raw partition using matched lower-minor and symbolic rank-upper certificates.",
            "rank_upper_status": "PROVED_SYMBOLIC_UPPER_CERTIFICATES",
            "rank_upper_pickle_policy": "No frozen descriptor, lower-rank, or representative pickle is opened by this generator.",
        },
        "bindings": {
            "compiler_sha256": compiler_sha,
            "canonicalizer_sha256": canon_sha,
            "input_lock_sha256": sha_file(package_root / "INPUT_LOCK.json"),
            "semantic_sweep_sha256": overlay.get("semantic_sweep_sha256"),
            "direct_overlay_sha256": sha_file(
                package_root / "proofs/four_port_direct_residual_closure_certificate.json"
            ),
            "rank_upper_bundle_manifest_sha256": rank_upper_payload["bundle"][
                "manifest_sha256"
            ],
            "rank_upper_bundle_aggregate_sha256": rank_upper_payload["bundle"][
                "aggregate_sha256"
            ],
        },
        "primitive_counts": {
            "sources": len(sources),
            "selected_incoming_targets": 831,
            "marginalized_incoming_targets": 1983,
            "targets": len(targets),
            "port_permutations": len(permutations),
            "raw_per_source": RAW_PER_SOURCE,
            "raw_total": RAW_TOTAL,
            "union_topology_compatible_target_permutation_keys": len(target_descriptors),
            "unique_descriptors_including_sources": len(descriptors_by_hash),
        },
        "rank_histogram_unique_descriptors": {
            str(rank): count for rank, count in sorted(rank_histogram.items())
        },
        "partition_counts": dict(sorted(category_counts.items())),
        "retained_class_counts": {
            "terminal": terminal_classes,
            "restoration_obligation": restoration_classes,
            "total": terminal_classes + restoration_classes,
        },
        "sources": source_rows,
        "artifacts": {
            "raw_directional_ledger.jsonl.gz": {
                "sha256": sha_file(ledger_path),
                "uncompressed_sha256": ledger_plain_sha,
                "uncompressed_bytes": ledger_plain_bytes,
            },
            "rank_lower_certificates.json.gz": {
                "sha256": sha_file(output_root / "rank_lower_certificates.json.gz"),
                "uncompressed_sha256": rank_plain_sha,
                "uncompressed_bytes": rank_plain_bytes,
            },
            "rank_upper_binding.json.gz": {
                "sha256": sha_file(output_root / "rank_upper_binding.json.gz"),
                "uncompressed_sha256": upper_plain_sha,
                "uncompressed_bytes": upper_plain_bytes,
            },
            "retained_class_partition.json.gz": {
                "sha256": sha_file(output_root / "retained_class_partition.json.gz"),
                "uncompressed_sha256": class_plain_sha,
                "uncompressed_bytes": class_plain_bytes,
            },
        },
    }
    summary["payload_sha256_without_hash"] = sha_object(summary)
    atomic_json(output_root / "raw_ledger_summary.json", summary)
    print("RAW_LEDGER_PRIMITIVE_REGENERATION_PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
