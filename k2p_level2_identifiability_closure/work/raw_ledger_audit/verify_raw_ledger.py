#!/usr/bin/env python3
"""Fail-closed structural and full primitive replay of the raw ledger."""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import itertools
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

STRICT_JSON_DIR = Path(__file__).resolve().parents[1] / "final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)

from ledger_common import (
    AUDIT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    canonical_json_bytes,
    fail,
    load_json,
    sha_file,
    sha_object,
)
from rank_upper_binding import validate_bundle_manifest


RAW_TOTAL = 405216
RAW_PER_SOURCE = 67536
TARGET_COUNT = 2814
PERMUTATION_COUNT = 24
EXPECTED_SOURCE_COUNTS = (536, 747, 276, 276, 64, 32)
EXPECTED_SOURCE_RANKS = (13, 14, 14, 14, 15, 16)
EXPECTED_PARTITION = {
    "topology_excluded": 377382,
    "rank_excluded": 23822,
    "retained_terminal": 1472,
    "restoration_obligation": 2540,
}
EXPECTED_SOURCE_PARTITIONS = (
    (60942, 5678, 732, 184),
    (65160, 288, 26, 2062),
    (62820, 4260, 316, 140),
    (62820, 4260, 316, 140),
    (62820, 4652, 52, 12),
    (62820, 4684, 30, 2),
)
EXPECTED_TOPOLOGY_REASONS = (
    {"quartet": 59064, "tree_sunlet": 1878},
    {"quartet": 65088, "tree_sunlet": 72},
    {"quartet": 59064, "tree_sunlet": 3756},
    {"quartet": 59064, "tree_sunlet": 3756},
    {"quartet": 59064, "tree_sunlet": 3756},
    {"quartet": 59064, "tree_sunlet": 3756},
)
CATEGORIES = tuple(EXPECTED_PARTITION)
DEFAULT_RANK_UPPER_ROOT = AUDIT_ROOT.parent / "rank_upper_certificates"


def read_gzip_bytes(path: Path) -> tuple[bytes, str]:
    digest = hashlib.sha256()
    chunks = []
    try:
        with gzip.open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
                chunks.append(chunk)
    except (OSError, EOFError) as exc:
        fail("RAW_LEDGER_GZIP_FAIL", f"{path}: {exc}")
    return b"".join(chunks), digest.hexdigest()


def validate_artifact_binding(artifact_root: Path, summary: dict, name: str) -> Path:
    metadata = summary.get("artifacts", {}).get(name)
    if not isinstance(metadata, dict):
        fail("RAW_LEDGER_ARTIFACT_METADATA_FAIL", name)
    path = artifact_root / name
    if not path.is_file():
        fail("RAW_LEDGER_ARTIFACT_MISSING", name)
    if sha_file(path) != metadata.get("sha256"):
        fail("RAW_LEDGER_ARTIFACT_HASH_FAIL", name)
    plain, plain_hash = read_gzip_bytes(path)
    if plain_hash != metadata.get("uncompressed_sha256"):
        fail("RAW_LEDGER_ARTIFACT_PLAIN_HASH_FAIL", name)
    if len(plain) != metadata.get("uncompressed_bytes"):
        fail("RAW_LEDGER_ARTIFACT_PLAIN_SIZE_FAIL", name)
    return path


def validate_rank_catalog(path: Path):
    try:
        payload = load_canonical_gzip_json(path, label=str(path))
    except (OSError, StrictJSONError) as exc:
        fail("RAW_LEDGER_RANK_STRICT_JSON_FAIL", exc)
    if payload.get("schema") != "k2p-four-port-regenerated-rank-lower-certificates-v1":
        fail("RAW_LEDGER_RANK_SCHEMA_FAIL")
    rows = payload.get("descriptors")
    if not isinstance(rows, list) or len(rows) != payload.get("descriptor_count") or len(rows) != 4379:
        fail("RAW_LEDGER_RANK_CENSUS_FAIL")
    catalog = {}
    histogram = collections.Counter()
    for row in rows:
        digest = row.get("descriptor_sha256")
        rank = row.get("rank")
        if not isinstance(digest, str) or len(digest) != 64 or digest in catalog:
            fail("RAW_LEDGER_RANK_DESCRIPTOR_ID_FAIL", digest)
        if not isinstance(rank, int) or rank <= 0:
            fail("RAW_LEDGER_RANK_VALUE_FAIL", (digest, rank))
        pivot_rows = row.get("pivot_rows")
        pivot_columns = row.get("pivot_columns")
        if (
            not isinstance(pivot_rows, list)
            or not isinstance(pivot_columns, list)
            or len(pivot_rows) != rank
            or len(pivot_columns) != rank
            or len(set(pivot_rows)) != rank
            or len(set(pivot_columns)) != rank
            or row.get("minor_determinant") in {None, "0", 0}
        ):
            fail("RAW_LEDGER_RANK_LOWER_CERTIFICATE_SHAPE_FAIL", digest)
        parameter_count = row.get("parameter_count")
        if parameter_count != 2 * row.get("edge_class_count") + row.get("retic_count"):
            fail("RAW_LEDGER_RANK_PARAMETER_COUNT_FAIL", digest)
        if rank > parameter_count:
            fail("RAW_LEDGER_RANK_EXCEEDS_PARAMETERS", digest)
        catalog[digest] = row
        histogram[rank] += 1
    expected_histogram = {8: 647, 10: 810, 12: 1167, 13: 420, 14: 1007, 15: 72, 16: 256}
    if dict(histogram) != expected_histogram:
        fail("RAW_LEDGER_RANK_HISTOGRAM_FAIL", dict(histogram))
    return catalog


def validate_rank_upper_binding(path: Path, rank_catalog, bundle_root: Path):
    try:
        payload = load_canonical_gzip_json(path, label=str(path))
    except (OSError, StrictJSONError) as exc:
        fail("RAW_LEDGER_UPPER_STRICT_JSON_FAIL", exc)
    if (
        payload.get("schema")
        != "k2p-four-port-regenerated-rank-upper-binding-v1"
        or payload.get("descriptor_count") != 4379
        or payload.get("base_ansatz_descriptor_count") != 3515
        or payload.get("exceptional_transport_descriptor_count") != 864
        or payload.get("exceptional_representative_count") != 75
        or payload.get("zero_unresolved") is not True
    ):
        fail("RAW_LEDGER_UPPER_CENSUS_FAIL")
    manifest = validate_bundle_manifest(bundle_root)
    bundle = payload.get("bundle", {})
    if (
        bundle.get("manifest_sha256")
        != sha_file(bundle_root / "manifest.json")
        or bundle.get("aggregate_sha256") != manifest.get("aggregate_sha256")
        or bundle.get("file_count") != manifest.get("file_count")
        or bundle.get("coverage_sha256")
        != sha_file(bundle_root / "rank_upper_coverage.json")
    ):
        fail("RAW_LEDGER_UPPER_BUNDLE_BINDING_FAIL")
    representatives = payload.get("representatives")
    if (
        not isinstance(representatives, dict)
        or set(representatives) != {str(index) for index in range(75)}
    ):
        fail("RAW_LEDGER_UPPER_REPRESENTATIVE_CENSUS_FAIL")
    rows = payload.get("descriptors")
    if not isinstance(rows, list) or len(rows) != 4379:
        fail("RAW_LEDGER_UPPER_ROW_CENSUS_FAIL")
    binding = {}
    indices = set()
    mechanisms = collections.Counter()
    for row in rows:
        raw_digest = row.get("raw_ledger_descriptor_sha256")
        descriptor = rank_catalog.get(raw_digest)
        index = row.get("descriptor_index")
        if (
            descriptor is None
            or raw_digest in binding
            or not isinstance(index, int)
            or index in indices
            or descriptor["rank"] != row.get("exact_rank")
            or descriptor["parameter_count"] != row.get("parameter_count")
        ):
            fail("RAW_LEDGER_UPPER_ROW_BINDING_FAIL", raw_digest)
        mechanism = row.get("upper_mechanism")
        if mechanism == "multilinear_lambda_polynomial_vector_fields":
            if (
                row.get("stacked_system_rank")
                - row.get("coefficient_system_rank")
                != row.get("independent_kernel_fields")
                or row["parameter_count"] - row["independent_kernel_fields"]
                != row["exact_rank"]
            ):
                fail("RAW_LEDGER_UPPER_BASE_CERTIFICATE_FAIL", raw_digest)
            mechanisms["base"] += 1
        elif mechanism == "base_fields_plus_primitive_log_field_port_transport":
            orbit = row.get("representative_orbit_index")
            representative = representatives.get(str(orbit))
            permutation = row.get("representative_to_member_port_permutation")
            if (
                representative is None
                or representative.get("representative_descriptor_sha256")
                != row.get("representative_descriptor_sha256")
                or representative.get("exact_rank") != row.get("exact_rank")
                or representative.get("certificate_sha256")
                != row.get("representative_certificate_sha256")
                or not isinstance(permutation, list)
                or sorted(permutation) != [0, 1, 2, 3]
            ):
                fail("RAW_LEDGER_UPPER_TRANSPORT_CERTIFICATE_FAIL", raw_digest)
            mechanisms["transport"] += 1
        else:
            fail("RAW_LEDGER_UPPER_MECHANISM_FAIL", raw_digest)
        indices.add(index)
        binding[raw_digest] = row
    if indices != set(range(4379)) or mechanisms != collections.Counter(
        {"base": 3515, "transport": 864}
    ):
        fail("RAW_LEDGER_UPPER_PARTITION_FAIL", dict(mechanisms))
    if set(binding) != set(rank_catalog):
        fail("RAW_LEDGER_UPPER_DESCRIPTOR_COVERAGE_FAIL")
    return binding


def validate_class_partition(path: Path, rank_catalog):
    try:
        payload = load_canonical_gzip_json(path, label=str(path))
    except (OSError, StrictJSONError) as exc:
        fail("RAW_LEDGER_CLASS_STRICT_JSON_FAIL", exc)
    rows = payload.get("classes")
    if not isinstance(rows, list) or len(rows) != 1931:
        fail("RAW_LEDGER_CLASS_CENSUS_FAIL")
    classes = {}
    per_source = collections.Counter()
    categories = collections.Counter()
    for row in rows:
        key = (row.get("source_index"), row.get("canonical_class_id"))
        if key in classes:
            fail("RAW_LEDGER_CLASS_DUPLICATE", key)
        source_index, class_id = key
        if (
            not isinstance(source_index, int)
            or not 0 <= source_index < 6
            or not isinstance(class_id, int)
        ):
            fail("RAW_LEDGER_CLASS_ID_FAIL", key)
        descriptor = rank_catalog.get(row.get("descriptor_sha256"))
        if descriptor is None or descriptor["rank"] != row.get("target_rank"):
            fail("RAW_LEDGER_CLASS_RANK_BINDING_FAIL", key)
        category = row.get("ledger_category")
        obligation = row.get("restoration_obligation_id")
        if category == "restoration_obligation":
            if obligation != f"source_{source_index}:class_{class_id:06d}":
                fail("RAW_LEDGER_OBLIGATION_ID_FAIL", key)
        elif category == "retained_terminal":
            if obligation is not None:
                fail("RAW_LEDGER_TERMINAL_OBLIGATION_FAIL", key)
        else:
            fail("RAW_LEDGER_CLASS_CATEGORY_FAIL", key)
        classes[key] = row
        per_source[source_index] += 1
        categories[category] += 1
    if tuple(per_source[i] for i in range(6)) != EXPECTED_SOURCE_COUNTS:
        fail("RAW_LEDGER_CLASS_SOURCE_CENSUS_FAIL", dict(per_source))
    if categories != collections.Counter({"retained_terminal": 934, "restoration_obligation": 997}):
        fail("RAW_LEDGER_CLASS_PARTITION_FAIL", dict(categories))
    return classes


def validate_ledger(path: Path, rank_catalog, rank_upper, classes, summary: dict):
    permutations = tuple(itertools.permutations(range(4)))
    category_counts = collections.Counter()
    source_category_counts = [collections.Counter() for _ in range(6)]
    source_topology_reasons = [collections.Counter() for _ in range(6)]
    class_member_counts = collections.Counter()
    row_count = 0
    try:
        rows = iter_canonical_gzip_jsonl(path, label=str(path))
        for expected_raw_id, row in enumerate(rows):
            if row.get("raw_id") != expected_raw_id:
                fail(
                    "RAW_LEDGER_RAW_ID_CENSUS_FAIL",
                    (expected_raw_id, row.get("raw_id")),
                )
            source_index = expected_raw_id // RAW_PER_SOURCE
            within_source = expected_raw_id % RAW_PER_SOURCE
            target_index = within_source // PERMUTATION_COUNT
            permutation_index = within_source % PERMUTATION_COUNT
            if (
                row.get("source_index") != source_index
                or row.get("target_index") != target_index
                or row.get("permutation_index") != permutation_index
                or row.get("port_permutation") != list(permutations[permutation_index])
                or row.get("source_rank") != EXPECTED_SOURCE_RANKS[source_index]
            ):
                fail("RAW_LEDGER_RAW_COORDINATE_FAIL", expected_raw_id)
            category = row.get("category")
            if category not in CATEGORIES:
                fail("RAW_LEDGER_CATEGORY_FAIL", (expected_raw_id, category))
            category_counts[category] += 1
            source_category_counts[source_index][category] += 1
            if category == "topology_excluded":
                topology_reason = row.get("topology_exclusion_reason")
                if topology_reason not in {"quartet", "tree_sunlet"}:
                    fail("RAW_LEDGER_TOPOLOGY_REASON_FAIL", expected_raw_id)
                source_topology_reasons[source_index][topology_reason] += 1
            elif category == "rank_excluded":
                descriptor = rank_catalog.get(row.get("descriptor_sha256"))
                upper = rank_upper.get(row.get("descriptor_sha256"))
                if (
                    descriptor is None
                    or upper is None
                    or descriptor["rank"] != row.get("target_rank")
                    or upper["exact_rank"] != row.get("target_rank")
                ):
                    fail("RAW_LEDGER_RANK_ROW_BINDING_FAIL", expected_raw_id)
                if not row["target_rank"] < row["source_rank"]:
                    fail("RAW_LEDGER_FALSE_RANK_EXCLUSION", expected_raw_id)
            else:
                key = (source_index, row.get("class_id"))
                class_row = classes.get(key)
                if class_row is None:
                    fail("RAW_LEDGER_CLASS_REFERENCE_FAIL", (expected_raw_id, key))
                expected = {
                    "category": class_row["ledger_category"],
                    "descriptor_sha256": class_row["descriptor_sha256"],
                    "target_rank": class_row["target_rank"],
                    "status": class_row["status_before_direct_overlay"],
                    "restoration_obligation_id": class_row["restoration_obligation_id"],
                }
                if any(row.get(field) != value for field, value in expected.items()):
                    fail("RAW_LEDGER_CLASS_REFERENCE_BINDING_FAIL", expected_raw_id)
                class_member_counts[key] += 1
            row_count += 1
    except (OSError, StrictJSONError) as exc:
        fail("RAW_LEDGER_ROW_STRICT_JSON_FAIL", exc)
    if row_count != RAW_TOTAL:
        fail("RAW_LEDGER_ROW_COUNT_FAIL", row_count)
    if dict(category_counts) != EXPECTED_PARTITION:
        fail("RAW_LEDGER_PARTITION_CENSUS_FAIL", dict(category_counts))
    for source_index, expected_tuple in enumerate(EXPECTED_SOURCE_PARTITIONS):
        observed_tuple = tuple(source_category_counts[source_index][name] for name in CATEGORIES)
        if observed_tuple != expected_tuple:
            fail("RAW_LEDGER_SOURCE_PARTITION_FAIL", (source_index, observed_tuple))
        observed_reasons = dict(source_topology_reasons[source_index])
        if observed_reasons != EXPECTED_TOPOLOGY_REASONS[source_index]:
            fail(
                "RAW_LEDGER_TOPOLOGY_REASON_CENSUS_FAIL",
                (source_index, observed_reasons),
            )
        summary_reasons = summary.get("sources", [])[source_index].get(
            "topology_exclusion_reasons"
        )
        if summary_reasons != EXPECTED_TOPOLOGY_REASONS[source_index]:
            fail("RAW_LEDGER_SUMMARY_TOPOLOGY_REASON_FAIL", source_index)
    for key, class_row in classes.items():
        if class_member_counts[key] != class_row.get("raw_presentation_count"):
            fail("RAW_LEDGER_CLASS_MEMBER_COUNT_FAIL", key)
    if summary.get("partition_counts") != EXPECTED_PARTITION:
        fail("RAW_LEDGER_SUMMARY_PARTITION_FAIL")
    return category_counts


def full_regeneration(
    package_root: Path,
    artifact_root: Path,
    rank_upper_root: Path,
    timeout_seconds: float,
) -> None:
    with tempfile.TemporaryDirectory(prefix="k2p_raw_ledger_replay_") as temporary:
        replay_root = Path(temporary) / "artifacts"
        command = [
            sys.executable,
            "-B",
            str(AUDIT_ROOT / "generate_raw_ledger.py"),
            "--package-root",
            str(package_root),
            "--output-root",
            str(replay_root),
            "--rank-upper-root",
            str(rank_upper_root),
        ]
        environment = dict(os.environ)
        environment.pop("PYTHONOPTIMIZE", None)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            result = subprocess.run(
                command,
                cwd=AUDIT_ROOT,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            fail("RAW_LEDGER_FULL_REPLAY_TIMEOUT", timeout_seconds)
        if result.returncode != 0:
            fail(
                "RAW_LEDGER_FULL_REPLAY_FAIL",
                (result.stdout + result.stderr).decode(errors="replace")[-5000:],
            )
        if b"RAW_LEDGER_PRIMITIVE_REGENERATION_PASS" not in result.stdout.splitlines():
            fail("RAW_LEDGER_FULL_REPLAY_TERMINAL_FAIL")
        for name in (
            "raw_directional_ledger.jsonl.gz",
            "rank_lower_certificates.json.gz",
            "rank_upper_binding.json.gz",
            "retained_class_partition.json.gz",
        ):
            if (replay_root / name).read_bytes() != (artifact_root / name).read_bytes():
                fail(
                    "RAW_LEDGER_FULL_REPLAY_BYTE_MISMATCH",
                    {
                        "file": name,
                        "observed": sha_file(replay_root / name),
                        "expected": sha_file(artifact_root / name),
                    },
                )
    print("RAW_LEDGER_FULL_PRIMITIVE_REPLAY_PASS byte_identical=true")


def main() -> None:
    if not __debug__:
        fail("RAW_LEDGER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--artifact-root", type=Path, default=AUDIT_ROOT / "artifacts")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=600.0)
    parser.add_argument(
        "--rank-upper-root", type=Path, default=DEFAULT_RANK_UPPER_ROOT
    )
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        fail("RAW_LEDGER_TIMEOUT_FAIL")
    artifact_root = args.artifact_root.resolve()
    summary_path = artifact_root / "raw_ledger_summary.json"
    summary = load_json(summary_path)
    expected_payload = summary.get("payload_sha256_without_hash")
    without_hash = {key: value for key, value in summary.items() if key != "payload_sha256_without_hash"}
    if expected_payload != sha_object(without_hash):
        fail("RAW_LEDGER_SUMMARY_PAYLOAD_HASH_FAIL")
    if summary.get("primitive_counts", {}).get("raw_total") != RAW_TOTAL:
        fail("RAW_LEDGER_SUMMARY_RAW_TOTAL_FAIL")
    rank_path = validate_artifact_binding(
        artifact_root, summary, "rank_lower_certificates.json.gz"
    )
    upper_path = validate_artifact_binding(
        artifact_root, summary, "rank_upper_binding.json.gz"
    )
    class_path = validate_artifact_binding(
        artifact_root, summary, "retained_class_partition.json.gz"
    )
    ledger_path = validate_artifact_binding(
        artifact_root, summary, "raw_directional_ledger.jsonl.gz"
    )
    rank_catalog = validate_rank_catalog(rank_path)
    rank_upper = validate_rank_upper_binding(
        upper_path, rank_catalog, args.rank_upper_root.resolve()
    )
    classes = validate_class_partition(class_path, rank_catalog)
    validate_ledger(ledger_path, rank_catalog, rank_upper, classes, summary)
    print("RAW_LEDGER_STRUCTURAL_REPLAY_PASS rows=405216 classes=1931 descriptors=4379")
    if not args.quick:
        full_regeneration(
            args.package_root.resolve(),
            artifact_root,
            args.rank_upper_root.resolve(),
            args.timeout_seconds,
        )
    if summary.get("scope", {}).get("rank_upper_status") != "PROVED_SYMBOLIC_UPPER_CERTIFICATES":
        fail("RAW_LEDGER_RANK_UPPER_STATUS_FAIL")
    print("RAW_LEDGER_EXACT_RANK_UPPER_PASS descriptors=4379 unresolved=0")


if __name__ == "__main__":
    main()
