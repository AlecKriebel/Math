#!/usr/bin/env python3
"""Fail-closed structural and full primitive replay of the theta2 closure."""

from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import io
import itertools
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)

from theta2_common import (
    ARTIFACT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    PERMUTATION_COUNT,
    RAW_PER_SOURCE,
    RAW_TOTAL,
    SOURCE_COUNT,
    TARGET_COUNT,
    canonical_json_bytes,
    canonicalizer_sha256,
    fail,
    load_atlas,
    pretty_json_bytes,
    sha_file,
    sha_object,
    witness_id,
)


EXPECTED_RAW_PER_SOURCE = {
    "quartet_pointwise_excluded": 735648,
    "tree_sunlet_pointwise_excluded": 632,
    "rank_excluded": 200,
    "quadratic_separated": 60,
    "isomorphic": 20,
}
EXPECTED_RAW_GLOBAL = {
    key: SOURCE_COUNT * value for key, value in EXPECTED_RAW_PER_SOURCE.items()
}
EXPECTED_CLASS_PER_SOURCE = {
    "rank_excluded": 88,
    "quadratic_separated": 24,
    "isomorphic": 8,
}
EXPECTED_CLASS_GLOBAL = {
    key: SOURCE_COUNT * value for key, value in EXPECTED_CLASS_PER_SOURCE.items()
}
EXPECTED_RANK_HISTOGRAM = {14: 8, 16: 80, 18: 32}
ARTIFACT_NAMES = (
    "exact_rank_certificates.json.gz",
    "direct_proof_certificates.json.gz",
    "class_partition.json.gz",
    "fixed_full_restoration_closure.json.gz",
    "raw_directional_ledger.jsonl.gz",
)

LEGACY_COMPILER_SHA256 = (
    "5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483"
)
LEGACY_CANONICALIZER_SHA256 = (
    "16ed7c6e125b7171268ae5187b0710702d5024f9ff4615b21d9d6b4ee53a4ca4"
)
LEGACY_INPUT_LOCK_SHA256 = (
    "03b938261c77fe9760241628c0b7cd90ffc1985787503f4a27663707f5c3b2ea"
)
CURRENT_COMPILER_SHA256 = (
    "afafe6c4289870a02226516e2b7ff207c57b844f4c45fc6864cedf826e9ec742"
)
CURRENT_CANONICALIZER_SHA256 = (
    "517a056cca7a2973d9b64646630671dfcfaf9fd2c8e2335e4f24d7efec9630f5"
)
CURRENT_INPUT_LOCK_SHA256 = (
    "332af9756d079d31d6b8ee2fab100c2b82ad938f24373780cf24e32dcc4d6032"
)


def deterministic_gzip_bytes(plain: bytes) -> bytes:
    """Encode bytes exactly as the theta2 producer does (empty name, mtime zero)."""
    target = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as handle:
        handle.write(plain)
    return target.getvalue()


def gzip_metadata(encoded: bytes, plain: bytes) -> dict[str, object]:
    return {
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "uncompressed_bytes": len(plain),
    }


def load_plain_json(path: Path) -> dict:
    try:
        value = decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as exc:
        fail("THETA2_PLAIN_JSON_FAIL", f"{path}: {exc}")
    return value


def rebound_payload(
    payload: dict,
    replacements: tuple[tuple[tuple[str, ...], str, str], ...],
) -> dict:
    """Change only explicitly enumerated provenance fields, fail-closed."""
    result = copy.deepcopy(payload)
    for path, legacy, current in replacements:
        cursor = result
        for key in path[:-1]:
            cursor = cursor[key]
        if cursor.get(path[-1]) != legacy:
            fail("THETA2_LEGACY_REBIND_SOURCE_FAIL", ".".join(path))
        cursor[path[-1]] = current

    restored = copy.deepcopy(result)
    for path, legacy, _current in replacements:
        cursor = restored
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = legacy
    if restored != payload:
        fail("THETA2_PROVENANCE_ONLY_REBIND_FAIL")
    return result


def current_generator_bindings(package_root: Path) -> dict[str, str]:
    compiler = sha_file(package_root / "atlas/k2p_atlas_core.py")
    if compiler != CURRENT_COMPILER_SHA256:
        fail("THETA2_CURRENT_COMPILER_BINDING_FAIL", compiler)
    atlas = load_atlas(package_root)
    canonicalizer = canonicalizer_sha256(atlas)
    if canonicalizer != CURRENT_CANONICALIZER_SHA256:
        fail("THETA2_CURRENT_CANONICALIZER_BINDING_FAIL", canonicalizer)
    lock_path = package_root / "INPUT_LOCK.json"
    lock = load_plain_json(lock_path)
    input_lock_sha256 = sha_file(lock_path)
    if input_lock_sha256 != CURRENT_INPUT_LOCK_SHA256:
        fail("THETA2_CURRENT_INPUT_LOCK_BINDING_FAIL", input_lock_sha256)
    if lock.get("compiler_sha256") != compiler:
        fail("THETA2_CURRENT_COMPILER_LOCK_BINDING_FAIL")
    if lock.get("canonicalizer_sha256") != canonicalizer:
        fail("THETA2_CURRENT_CANONICALIZER_LOCK_BINDING_FAIL")
    return {
        "compiler_sha256": compiler,
        "canonicalizer_sha256": canonicalizer,
        "input_lock_sha256": input_lock_sha256,
    }


def digest_gzip(path: Path) -> tuple[str, int]:
    """Hash and count an uncompressed stream without retaining it in memory."""
    digest = hashlib.sha256()
    byte_count = 0
    try:
        with gzip.open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
                byte_count += len(chunk)
    except (OSError, EOFError) as exc:
        fail("THETA2_GZIP_FAIL", f"{path}: {exc}")
    return digest.hexdigest(), byte_count


def read_gzip_json(path: Path) -> dict:
    try:
        value = load_canonical_gzip_json(path, label=path.name)
    except (OSError, StrictJSONError) as exc:
        fail("THETA2_ARTIFACT_JSON_FAIL", f"{path}: {exc}")
    if not isinstance(value, dict):
        fail("THETA2_ARTIFACT_OBJECT_FAIL", path)
    return value


def strict_ledger_rows(path: Path):
    try:
        yield from iter_canonical_gzip_jsonl(path, label=path.name)
    except OSError as exc:
        fail("THETA2_LEDGER_OPEN_FAIL", exc)
    except StrictJSONError as exc:
        fail("THETA2_LEDGER_ROW_JSON_FAIL", exc)


def validate_summary(artifact_root: Path) -> dict:
    summary = load_plain_json(artifact_root / "theta2_five_port_summary.json")
    if summary.get("schema") != "k2p-theta2-five-port-closure-summary-v1":
        fail("THETA2_SUMMARY_SCHEMA_FAIL")
    bindings = summary.get("bindings", {})
    if bindings.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_SUMMARY_LEGACY_COMPILER_BINDING_FAIL")
    if bindings.get("canonicalizer_sha256") != LEGACY_CANONICALIZER_SHA256:
        fail("THETA2_SUMMARY_LEGACY_CANONICALIZER_BINDING_FAIL")
    if bindings.get("input_lock_sha256") != LEGACY_INPUT_LOCK_SHA256:
        fail("THETA2_SUMMARY_LEGACY_INPUT_LOCK_BINDING_FAIL")
    expected_payload = summary.get("payload_sha256_without_hash")
    payload = {
        key: value
        for key, value in summary.items()
        if key != "payload_sha256_without_hash"
    }
    if expected_payload != sha_object(payload):
        fail("THETA2_SUMMARY_PAYLOAD_HASH_FAIL")
    primitive = summary.get("primitive_counts", {})
    if (
        primitive.get("sources") != SOURCE_COUNT
        or primitive.get("targets") != TARGET_COUNT
        or primitive.get("port_permutations") != PERMUTATION_COUNT
        or primitive.get("raw_total") != RAW_TOTAL
        or primitive.get("unique_descriptors_including_sources") != 120
    ):
        fail("THETA2_SUMMARY_PRIMITIVE_CENSUS_FAIL", primitive)
    if summary.get("raw_partition") != EXPECTED_RAW_GLOBAL:
        fail("THETA2_SUMMARY_RAW_PARTITION_FAIL")
    if summary.get("class_partition") != EXPECTED_CLASS_GLOBAL:
        fail("THETA2_SUMMARY_CLASS_PARTITION_FAIL")
    if summary.get("unresolved_class_count") != 0:
        fail("THETA2_SUMMARY_UNRESOLVED_FAIL")
    if summary.get("claim_scope", {}).get("not_claimed") is None:
        fail("THETA2_SUMMARY_SCOPE_GUARD_FAIL")
    for name in ARTIFACT_NAMES:
        metadata = summary.get("artifacts", {}).get(name)
        path = artifact_root / name
        if not isinstance(metadata, dict) or not path.is_file():
            fail("THETA2_ARTIFACT_MISSING", name)
        if sha_file(path) != metadata.get("sha256"):
            fail("THETA2_ARTIFACT_HASH_FAIL", name)
        digest, plain_bytes = digest_gzip(path)
        if digest != metadata.get("uncompressed_sha256"):
            fail("THETA2_ARTIFACT_PLAIN_HASH_FAIL", name)
        if plain_bytes != metadata.get("uncompressed_bytes"):
            fail("THETA2_ARTIFACT_PLAIN_SIZE_FAIL", name)
    return summary


def validate_rank_payload(payload: dict):
    if payload.get("schema") != "k2p-theta2-five-port-exact-rank-certificates-v1":
        fail("THETA2_RANK_SCHEMA_FAIL")
    if payload.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_RANK_LEGACY_COMPILER_BINDING_FAIL")
    rows = payload.get("descriptors")
    if not isinstance(rows, list) or len(rows) != 120 or payload.get("descriptor_count") != 120:
        fail("THETA2_RANK_CENSUS_FAIL")
    catalog = {}
    histogram = collections.Counter()
    for row in rows:
        digest = row.get("descriptor_sha256")
        rank = row.get("exact_generic_rank")
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or digest in catalog
            or rank not in {14, 16, 18}
        ):
            fail("THETA2_RANK_ROW_ID_FAIL", digest)
        lower = row.get("lower_certificate", {})
        upper = row.get("upper_certificate", {})
        pivot_rows = lower.get("pivot_rows")
        pivot_columns = lower.get("pivot_columns")
        if (
            not isinstance(pivot_rows, list)
            or not isinstance(pivot_columns, list)
            or len(pivot_rows) != rank
            or len(pivot_columns) != rank
            or len(set(pivot_rows)) != rank
            or len(set(pivot_columns)) != rank
            or lower.get("minor_determinant") in {None, 0, "0"}
        ):
            fail("THETA2_RANK_LOWER_SHAPE_FAIL", digest)
        parameter_count = row.get("parameter_count")
        if (
            parameter_count
            != 2 * row.get("edge_class_count") + row.get("retic_count")
            or rank > parameter_count
            or upper.get("parameter_count") != parameter_count
            or upper.get("certified_rank_upper") != rank
            or upper.get("stacked_system_rank")
            - upper.get("coefficient_system_rank")
            != upper.get("independent_kernel_fields")
            or parameter_count - upper.get("independent_kernel_fields") != rank
            or upper.get("method")
            != "coefficientwise-polynomial-vector-field-kernel"
        ):
            fail("THETA2_RANK_UPPER_BINDING_FAIL", digest)
        catalog[digest] = row
        histogram[rank] += 1
    if dict(sorted(histogram.items())) != EXPECTED_RANK_HISTOGRAM:
        fail("THETA2_RANK_HISTOGRAM_FAIL", dict(histogram))
    return catalog


def _split_set(value):
    return {
        tuple(sorted((tuple(row[0]), tuple(row[1]))))
        for row in value
    }


def validate_topology_witness(identifier: str, content: dict):
    if witness_id(content) != identifier:
        fail("THETA2_TOPOLOGY_WITNESS_ID_FAIL", identifier)
    reason = content.get("reason")
    if reason == "displayed_quartet_mismatch":
        source = _split_set(content.get("source_displayed_splits", []))
        target = _split_set(content.get("target_displayed_splits", []))
        split = tuple(
            sorted(
                (
                    tuple(content.get("distinguished_split", [[], []])[0]),
                    tuple(content.get("distinguished_split", [[], []])[1]),
                )
            )
        )
        if not source or not target or source == target:
            fail("THETA2_QUARTET_WITNESS_SET_FAIL", identifier)
        zero = source if content.get("zero_on") == "source" else target
        positive = target if content.get("strictly_positive_on") == "target" else source
        if {content.get("zero_on"), content.get("strictly_positive_on")} != {"source", "target"}:
            fail("THETA2_QUARTET_WITNESS_SIDE_FAIL", identifier)
        kind = content.get("invariant_kind")
        if kind == "I_singleton":
            if len(zero) != 1 or split not in zero or not any(item != split for item in positive):
                fail("THETA2_QUARTET_I_WITNESS_FAIL", identifier)
        elif kind == "J_membership":
            if split in zero or split not in positive:
                fail("THETA2_QUARTET_J_WITNESS_FAIL", identifier)
        else:
            fail("THETA2_QUARTET_WITNESS_KIND_FAIL", identifier)
    elif reason == "tree_sunlet_strict_sign":
        if (
            {content.get("source_type"), content.get("target_type")}
            != {"tree", "sunlet"}
            or {content.get("zero_on"), content.get("strictly_negative_on")}
            != {"source", "target"}
            or content.get("invariant") != "T3=V^2*X_g-X_s^2*Y_g*Z_g"
            or "delta*(1-delta)" not in content.get("sunlet_pullback", "")
        ):
            fail("THETA2_TREE_SUNLET_WITNESS_FAIL", identifier)
    else:
        fail("THETA2_TOPOLOGY_WITNESS_REASON_FAIL", identifier)


def validate_tree_sunlet_identity():
    try:
        import sympy as sp
    except Exception as exc:
        fail("THETA2_SYMPY_REQUIRED", exc)
    inheritance, d_g, e_g, f_g = sp.symbols("inheritance d_g e_g f_g")
    complement = 1 - inheritance
    n_value = inheritance * d_g + complement * e_g
    left_value = inheritance * d_g + complement * f_g * e_g
    right_value = inheritance * f_g * d_g + complement * e_g
    identity = sp.expand(
        f_g * n_value**2
        - left_value * right_value
        + inheritance * complement * d_g * e_g * (1 - f_g) ** 2
    )
    if identity != 0:
        fail("THETA2_TREE_SUNLET_SYMBOLIC_IDENTITY_FAIL")


def validate_proof_payload(payload: dict):
    if payload.get("schema") != "k2p-theta2-five-port-direct-proof-certificates-v1":
        fail("THETA2_PROOF_SCHEMA_FAIL")
    topology = payload.get("topology_witnesses")
    quadratics = payload.get("quadratic_certificates")
    isomorphisms = payload.get("isomorphism_certificates")
    anchors = payload.get("isomorphic_terminal_anchors")
    if not isinstance(topology, dict) or not topology:
        fail("THETA2_TOPOLOGY_WITNESS_CATALOG_FAIL")
    if not isinstance(quadratics, dict) or len(quadratics) != 96:
        fail("THETA2_QUADRATIC_CERTIFICATE_CENSUS_FAIL")
    if not isinstance(isomorphisms, dict) or len(isomorphisms) != 32:
        fail("THETA2_ISOMORPHISM_CERTIFICATE_CENSUS_FAIL")
    if (
        not isinstance(anchors, list)
        or len(anchors) != 32
        or sum(row.get("raw_presentation_count", -1) for row in anchors) != 80
    ):
        fail("THETA2_ISOMORPHIC_ANCHOR_CENSUS_FAIL")
    for identifier, content in topology.items():
        validate_topology_witness(identifier, content)
    for identifier, content in quadratics.items():
        if (
            identifier != f"Q:{sha_object(content)}"
            or content.get("degree") != 2
            or content.get("target_pullback") != "identically_zero"
            or not content.get("source_pullback_terms")
            or content.get("source_pullback_sha256")
            != sha_object(content.get("source_pullback_terms"))
            or content.get("direction") != "source_not_contained_in_target"
        ):
            fail("THETA2_QUADRATIC_CERTIFICATE_SHAPE_FAIL", identifier)
    for identifier, content in isomorphisms.items():
        mapping = content.get("mixed_vertex_mapping_source_to_target")
        if (
            identifier != f"I:{sha_object(content)}"
            or content.get("relation")
            != "exact_labelled_semi_directed_isomorphism"
            or not isinstance(mapping, list)
            or not mapping
            or len({row[0] for row in mapping}) != len(mapping)
            or len({row[1] for row in mapping}) != len(mapping)
        ):
            fail("THETA2_ISOMORPHISM_CERTIFICATE_SHAPE_FAIL", identifier)
    anchor_keys = set()
    for anchor in anchors:
        key = (anchor.get("source_index"), anchor.get("class_id"))
        certificate = isomorphisms.get(anchor.get("certificate_id"))
        if (
            key in anchor_keys
            or certificate is None
            or anchor.get("mixed_vertex_mapping_source_to_target")
            != certificate.get("mixed_vertex_mapping_source_to_target")
            or anchor.get("source_descriptor_sha256")
            != certificate.get("source_descriptor_sha256")
            or anchor.get("target_descriptor_sha256")
            != certificate.get("target_descriptor_sha256")
            or len(anchor.get("raw_members", []))
            != anchor.get("raw_presentation_count")
        ):
            fail("THETA2_ISOMORPHIC_ANCHOR_BINDING_FAIL", key)
        anchor_keys.add(key)
    validate_tree_sunlet_identity()
    return topology, quadratics, isomorphisms, anchors


def validate_classes(payload: dict, rank_catalog, quadratics, isomorphisms, anchors):
    if payload.get("schema") != "k2p-theta2-five-port-class-partition-v1":
        fail("THETA2_CLASS_SCHEMA_FAIL")
    rows = payload.get("classes")
    if not isinstance(rows, list) or len(rows) != 480:
        fail("THETA2_CLASS_CENSUS_FAIL")
    classes = {}
    source_ids = collections.defaultdict(list)
    source_categories = [collections.Counter() for _ in range(SOURCE_COUNT)]
    for row in rows:
        key = (row.get("source_index"), row.get("class_id"))
        if key in classes:
            fail("THETA2_CLASS_DUPLICATE", key)
        source_index, class_id = key
        if (
            not isinstance(source_index, int)
            or not 0 <= source_index < SOURCE_COUNT
            or not isinstance(class_id, int)
            or not 0 <= class_id < 120
        ):
            fail("THETA2_CLASS_ID_FAIL", key)
        source_ids[source_index].append(class_id)
        source_rank = rank_catalog.get(row.get("source_descriptor_sha256"))
        target_rank = rank_catalog.get(row.get("target_descriptor_sha256"))
        if (
            source_rank is None
            or target_rank is None
            or source_rank["exact_generic_rank"] != row.get("source_rank")
            or target_rank["exact_generic_rank"] != row.get("target_rank")
            or row.get("source_rank") != 18
        ):
            fail("THETA2_CLASS_RANK_BINDING_FAIL", key)
        category = row.get("category")
        certificate = row.get("certificate_id")
        if category == "rank_excluded":
            if not row["target_rank"] < row["source_rank"] or certificate != f"R:{row['target_descriptor_sha256']}":
                fail("THETA2_FALSE_RANK_EXCLUSION", key)
        elif category == "quadratic_separated":
            proof = quadratics.get(certificate)
            if (
                proof is None
                or proof.get("source_index") != source_index
                or proof.get("class_id") != class_id
                or proof.get("source_descriptor_sha256")
                != row.get("source_descriptor_sha256")
                or proof.get("target_descriptor_sha256")
                != row.get("target_descriptor_sha256")
            ):
                fail("THETA2_CLASS_QUADRATIC_REFERENCE_FAIL", key)
        elif category == "isomorphic":
            proof = isomorphisms.get(certificate)
            if (
                proof is None
                or proof.get("source_index") != source_index
                or proof.get("class_id") != class_id
                or proof.get("source_descriptor_sha256")
                != row.get("source_descriptor_sha256")
                or proof.get("target_descriptor_sha256")
                != row.get("target_descriptor_sha256")
            ):
                fail("THETA2_CLASS_ISOMORPHISM_REFERENCE_FAIL", key)
        else:
            fail("THETA2_CLASS_CATEGORY_FAIL", key)
        members = row.get("raw_members")
        if (
            not isinstance(members, list)
            or len(members) != row.get("raw_presentation_count")
            or len({member.get("raw_id") for member in members}) != len(members)
        ):
            fail("THETA2_CLASS_MEMBER_SHAPE_FAIL", key)
        for member in members:
            expected_raw_id = (
                source_index * RAW_PER_SOURCE
                + member.get("target_index") * PERMUTATION_COUNT
                + member.get("permutation_index")
            )
            if member.get("raw_id") != expected_raw_id:
                fail("THETA2_CLASS_MEMBER_RAW_ID_FAIL", key)
        classes[key] = row
        source_categories[source_index][category] += 1
    for source_index in range(SOURCE_COUNT):
        if sorted(source_ids[source_index]) != list(range(120)):
            fail("THETA2_CLASS_ID_CENSUS_FAIL", source_index)
        if dict(source_categories[source_index]) != EXPECTED_CLASS_PER_SOURCE:
            fail(
                "THETA2_CLASS_SOURCE_PARTITION_FAIL",
                (source_index, dict(source_categories[source_index])),
            )
    anchor_by_key = {
        (row["source_index"], row["class_id"]): row for row in anchors
    }
    isomorphic_keys = {
        key for key, row in classes.items() if row["category"] == "isomorphic"
    }
    if set(anchor_by_key) != isomorphic_keys:
        fail("THETA2_ISOMORPHIC_ANCHOR_CLASS_COVERAGE_FAIL")
    for key in isomorphic_keys:
        anchor = anchor_by_key[key]
        class_row = classes[key]
        if (
            anchor["certificate_id"] != class_row["certificate_id"]
            or anchor["raw_members"] != class_row["raw_members"]
            or anchor["raw_presentation_count"]
            != class_row["raw_presentation_count"]
        ):
            fail("THETA2_ISOMORPHIC_ANCHOR_CLASS_BINDING_FAIL", key)
    return classes


def validate_restoration_payload(payload: dict, class_payload: dict, classes):
    if payload.get("schema") != "k2p-theta2-fixed-full-restoration-closure-v1":
        fail("THETA2_RESTORATION_SCHEMA_FAIL")
    bindings = payload.get("bindings", {})
    if bindings.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_RESTORATION_LEGACY_COMPILER_BINDING_FAIL")
    if bindings.get("canonicalizer_sha256") != LEGACY_CANONICALIZER_SHA256:
        fail("THETA2_RESTORATION_LEGACY_CANONICALIZER_BINDING_FAIL")
    if payload.get("bindings", {}).get("base_class_rows_sha256") != sha_object(
        class_payload.get("classes")
    ):
        fail("THETA2_RESTORATION_BASE_CLASS_BINDING_FAIL")
    expected_census = {
        "base_isomorphic_raw_anchors": 80,
        "no_dummy_physical_anchors": 24,
        "dummy_restoration_roots": 56,
        "one_dummy_roots": 40,
        "two_dummy_roots": 16,
        "first_layer_role_requests": 72,
        "first_insertion_candidates_per_request": 8,
        "six_port_children": 576,
        "six_port_isomorphic_continuations": 32,
        "second_insertion_candidates_per_continuation": 9,
        "seven_port_children": 288,
        "physical_isomorphic_restoration_terminals": 72,
        "unresolved_paths": 0,
    }
    census = payload.get("census", {})
    for key, expected in expected_census.items():
        if census.get(key) != expected:
            fail("THETA2_RESTORATION_CENSUS_FAIL", (key, census.get(key)))
    if census.get("six_port_categories") != {
        "isomorphic": 72,
        "quartet_pointwise_excluded": 504,
    }:
        fail("THETA2_RESTORATION_SIX_PORT_PARTITION_FAIL")
    if census.get("six_port_categories_by_remaining_roles") != {
        "0:isomorphic": 40,
        "0:quartet_pointwise_excluded": 280,
        "1:isomorphic": 32,
        "1:quartet_pointwise_excluded": 224,
    }:
        fail("THETA2_RESTORATION_SIX_PORT_REMAINING_FAIL")
    if census.get("seven_port_categories") != {
        "isomorphic": 32,
        "quartet_pointwise_excluded": 256,
    }:
        fail("THETA2_RESTORATION_SEVEN_PORT_PARTITION_FAIL")

    no_dummy = payload.get("no_dummy_anchors")
    roots = payload.get("restoration_roots")
    first_rows = payload.get("six_port_rows")
    second_rows = payload.get("seven_port_rows")
    topology = payload.get("topology_witnesses")
    isomorphisms = payload.get("isomorphism_certificates")
    if (
        not isinstance(no_dummy, list)
        or len(no_dummy) != 24
        or not isinstance(roots, list)
        or len(roots) != 56
        or not isinstance(first_rows, list)
        or len(first_rows) != 576
        or not isinstance(second_rows, list)
        or len(second_rows) != 288
        or not isinstance(topology, dict)
        or not isinstance(isomorphisms, dict)
    ):
        fail("THETA2_RESTORATION_COLLECTION_SHAPE_FAIL")

    base_isomorphic_raw = {}
    for key, class_row in classes.items():
        if class_row["category"] != "isomorphic":
            continue
        for member in class_row["raw_members"]:
            base_isomorphic_raw[member["raw_id"]] = {
                "source_index": key[0],
                "class_id": key[1],
                "target_index": member["target_index"],
                "permutation_index": member["permutation_index"],
                "certificate_id": class_row["certificate_id"],
            }
    anchors = no_dummy + roots
    if len(base_isomorphic_raw) != 80 or {
        row.get("base_raw_id") for row in anchors
    } != set(base_isomorphic_raw):
        fail("THETA2_RESTORATION_BASE_RAW_COVERAGE_FAIL")
    anchor_by_id = {}
    multiplicity = collections.Counter()
    for anchor in anchors:
        identifier = anchor.get("anchor_id")
        content = {key: value for key, value in anchor.items() if key != "anchor_id"}
        if identifier != f"A:{sha_object(content)}" or identifier in anchor_by_id:
            fail("THETA2_RESTORATION_ANCHOR_ID_FAIL", identifier)
        base = base_isomorphic_raw.get(anchor.get("base_raw_id"))
        if (
            base is None
            or anchor.get("source_index") != base["source_index"]
            or anchor.get("class_id") != base["class_id"]
            or anchor.get("target_index") != base["target_index"]
            or anchor.get("permutation_index") != base["permutation_index"]
            or anchor.get("base_certificate_id") != base["certificate_id"]
        ):
            fail("THETA2_RESTORATION_ANCHOR_BASE_BINDING_FAIL", identifier)
        roles = anchor.get("dummy_roles")
        if not isinstance(roles, list) or len(roles) not in {0, 1, 2}:
            fail("THETA2_RESTORATION_ANCHOR_ROLE_FAIL", identifier)
        multiplicity[len(roles)] += 1
        if roles:
            candidates = anchor.get("source_first_insertion_candidates")
            if not isinstance(candidates, list) or len(candidates) != 8:
                fail("THETA2_RESTORATION_ANCHOR_CANDIDATE_FAIL", identifier)
        anchor_by_id[identifier] = anchor
    if multiplicity != collections.Counter({0: 24, 1: 40, 2: 16}):
        fail("THETA2_RESTORATION_ANCHOR_MULTIPLICITY_FAIL", dict(multiplicity))

    for identifier, content in topology.items():
        validate_topology_witness(identifier, content)
    for identifier, content in isomorphisms.items():
        mapping = content.get("mixed_vertex_mapping_source_to_target")
        if (
            identifier != f"RI:{sha_object(content)}"
            or content.get("relation")
            != "exact_labelled_semi_directed_isomorphism"
            or not isinstance(mapping, list)
            or not mapping
            or len({row[0] for row in mapping}) != len(mapping)
            or len({row[1] for row in mapping}) != len(mapping)
        ):
            fail("THETA2_RESTORATION_ISOMORPHISM_CERTIFICATE_FAIL", identifier)

    first_by_path = {}
    first_per_anchor = collections.Counter()
    continuation_paths = set()
    relation_counts = collections.Counter()
    relation_categories = collections.defaultdict(set)
    first_counts = collections.Counter()
    first_remaining = collections.Counter()
    for row in first_rows:
        path_id = row.get("path_id")
        path_content = {
            key: row.get(key)
            for key in (
                "layer",
                "anchor_id",
                "restored_role",
                "source_insertion_index",
            )
        }
        anchor = anchor_by_id.get(row.get("anchor_id"))
        if (
            path_id != f"P6:{sha_object(path_content)}"
            or path_id in first_by_path
            or anchor is None
            or row.get("layer") != 1
            or row.get("port_count") != 6
            or row.get("restored_role") not in anchor["dummy_roles"]
            or not 0 <= row.get("source_insertion_index", -1) < 8
        ):
            fail("THETA2_RESTORATION_FIRST_ROW_ID_FAIL", path_id)
        remaining = row.get("remaining_roles")
        expected_remaining = [
            role
            for role in anchor["dummy_roles"]
            if role != row.get("restored_role")
        ]
        if remaining != expected_remaining:
            fail("THETA2_RESTORATION_FIRST_REMAINING_FAIL", path_id)
        category = row.get("category")
        certificate = row.get("certificate_id")
        if category == "quartet_pointwise_excluded":
            if topology.get(certificate, {}).get("reason") != "displayed_quartet_mismatch":
                fail("THETA2_RESTORATION_FIRST_QUARTET_REFERENCE_FAIL", path_id)
        elif category == "isomorphic":
            proof = isomorphisms.get(certificate)
            if (
                proof is None
                or proof.get("path_id") != path_id
                or proof.get("remaining_roles") != remaining
            ):
                fail("THETA2_RESTORATION_FIRST_ISOMORPHISM_REFERENCE_FAIL", path_id)
            if remaining:
                continuation_paths.add(path_id)
        else:
            fail("THETA2_RESTORATION_FIRST_CATEGORY_FAIL", path_id)
        pair = (
            row.get("source_mixed_graph_class"),
            row.get("target_mixed_graph_class"),
        )
        relation_counts[pair] += 1
        relation_categories[pair].add(category)
        first_by_path[path_id] = row
        first_per_anchor[row["anchor_id"]] += 1
        first_counts[category] += 1
        first_remaining[(len(remaining), category)] += 1
    for identifier, anchor in anchor_by_id.items():
        if not anchor["dummy_roles"]:
            continue
        expected = 8 * len(anchor["dummy_roles"])
        if first_per_anchor[identifier] != expected:
            fail("THETA2_RESTORATION_FIRST_ANCHOR_COVERAGE_FAIL", identifier)
    if first_counts != collections.Counter(
        {"quartet_pointwise_excluded": 504, "isomorphic": 72}
    ) or first_remaining != collections.Counter(
        {
            (0, "quartet_pointwise_excluded"): 280,
            (0, "isomorphic"): 40,
            (1, "quartet_pointwise_excluded"): 224,
            (1, "isomorphic"): 32,
        }
    ):
        fail("THETA2_RESTORATION_FIRST_REPLAY_CENSUS_FAIL")

    second_counts = collections.Counter()
    second_per_parent = collections.Counter()
    second_paths = set()
    physical_terminal_paths = {
        row["path_id"]
        for row in first_rows
        if row["category"] == "isomorphic" and not row["remaining_roles"]
    }
    for row in second_rows:
        path_id = row.get("path_id")
        path_content = {
            key: row.get(key)
            for key in (
                "layer",
                "parent_path_id",
                "restored_role",
                "source_insertion_index",
            )
        }
        parent = first_by_path.get(row.get("parent_path_id"))
        if (
            path_id != f"P7:{sha_object(path_content)}"
            or path_id in second_paths
            or parent is None
            or parent["path_id"] not in continuation_paths
            or row.get("layer") != 2
            or row.get("port_count") != 7
            or row.get("remaining_roles") != []
            or row.get("restored_role") != parent["remaining_roles"][0]
            or not 0 <= row.get("source_insertion_index", -1) < 9
        ):
            fail("THETA2_RESTORATION_SECOND_ROW_ID_FAIL", path_id)
        category = row.get("category")
        certificate = row.get("certificate_id")
        if category == "quartet_pointwise_excluded":
            if topology.get(certificate, {}).get("reason") != "displayed_quartet_mismatch":
                fail("THETA2_RESTORATION_SECOND_QUARTET_REFERENCE_FAIL", path_id)
        elif category == "isomorphic":
            proof = isomorphisms.get(certificate)
            if (
                proof is None
                or proof.get("path_id") != path_id
                or proof.get("remaining_roles") != []
            ):
                fail("THETA2_RESTORATION_SECOND_ISOMORPHISM_REFERENCE_FAIL", path_id)
            physical_terminal_paths.add(path_id)
        else:
            fail("THETA2_RESTORATION_SECOND_CATEGORY_FAIL", path_id)
        pair = (
            row.get("source_mixed_graph_class"),
            row.get("target_mixed_graph_class"),
        )
        relation_counts[pair] += 1
        relation_categories[pair].add(category)
        second_counts[category] += 1
        second_per_parent[parent["path_id"]] += 1
        second_paths.add(path_id)
    if set(second_per_parent) != continuation_paths or any(
        count != 9 for count in second_per_parent.values()
    ):
        fail("THETA2_RESTORATION_SECOND_PARENT_COVERAGE_FAIL")
    if second_counts != collections.Counter(
        {"quartet_pointwise_excluded": 256, "isomorphic": 32}
    ):
        fail("THETA2_RESTORATION_SECOND_REPLAY_CENSUS_FAIL")
    if physical_terminal_paths != set(
        payload.get("physical_isomorphic_terminal_path_ids", [])
    ) or len(physical_terminal_paths) != 72:
        fail("THETA2_RESTORATION_PHYSICAL_TERMINAL_PATH_FAIL")

    expected_relation_counts = {
        f"{left}:{right}": count
        for (left, right), count in sorted(relation_counts.items())
    }
    expected_relation_categories = {
        f"{left}:{right}": sorted(relation_categories[(left, right)])
        for left, right in sorted(relation_categories)
    }
    if (
        expected_relation_counts
        != payload.get("relation_class_presentation_counts")
        or expected_relation_categories
        != payload.get("relation_class_categories")
        or any(len(value) != 1 for value in relation_categories.values())
        or len(relation_counts) != census.get("exact_directed_relation_classes")
    ):
        fail("THETA2_RESTORATION_RELATION_CLASS_REPLAY_FAIL")
    return payload


def validate_ledger(path: Path, classes, topology_witnesses):
    permutations = tuple(itertools.permutations(range(5)))
    category_counts = collections.Counter()
    source_counts = [collections.Counter() for _ in range(SOURCE_COUNT)]
    class_member_counts = collections.Counter()
    row_count = 0
    for expected_raw_id, row in enumerate(strict_ledger_rows(path)):
            source_index = expected_raw_id // RAW_PER_SOURCE
            within_source = expected_raw_id % RAW_PER_SOURCE
            target_index = within_source // PERMUTATION_COUNT
            permutation_index = within_source % PERMUTATION_COUNT
            if (
                row.get("raw_id") != expected_raw_id
                or row.get("source_index") != source_index
                or row.get("source_repair_index") != source_index
                or row.get("target_index") != target_index
                or row.get("permutation_index") != permutation_index
                or row.get("port_permutation")
                != list(permutations[permutation_index])
                or row.get("source_rank") != 18
            ):
                fail("THETA2_LEDGER_RAW_COORDINATE_FAIL", expected_raw_id)
            category = row.get("category")
            if category not in EXPECTED_RAW_GLOBAL:
                fail("THETA2_LEDGER_CATEGORY_FAIL", (expected_raw_id, category))
            if category in {
                "quartet_pointwise_excluded",
                "tree_sunlet_pointwise_excluded",
            }:
                witness = topology_witnesses.get(row.get("topology_witness_id"))
                expected_reason = (
                    "displayed_quartet_mismatch"
                    if category == "quartet_pointwise_excluded"
                    else "tree_sunlet_strict_sign"
                )
                if witness is None or witness.get("reason") != expected_reason:
                    fail("THETA2_LEDGER_TOPOLOGY_REFERENCE_FAIL", expected_raw_id)
            else:
                key = (source_index, row.get("class_id"))
                class_row = classes.get(key)
                if class_row is None:
                    fail("THETA2_LEDGER_CLASS_REFERENCE_FAIL", expected_raw_id)
                for field, expected in (
                    ("category", class_row["category"]),
                    (
                        "target_descriptor_sha256",
                        class_row["target_descriptor_sha256"],
                    ),
                    ("target_rank", class_row["target_rank"]),
                    ("certificate_id", class_row["certificate_id"]),
                ):
                    if row.get(field) != expected:
                        fail("THETA2_LEDGER_CLASS_BINDING_FAIL", expected_raw_id)
                class_member_counts[key] += 1
            category_counts[category] += 1
            source_counts[source_index][category] += 1
            row_count += 1
    if row_count != RAW_TOTAL:
        fail("THETA2_LEDGER_ROW_CENSUS_FAIL", row_count)
    if dict(category_counts) != EXPECTED_RAW_GLOBAL:
        fail("THETA2_LEDGER_GLOBAL_PARTITION_FAIL", dict(category_counts))
    for source_index in range(SOURCE_COUNT):
        if dict(source_counts[source_index]) != EXPECTED_RAW_PER_SOURCE:
            fail(
                "THETA2_LEDGER_SOURCE_PARTITION_FAIL",
                (source_index, dict(source_counts[source_index])),
            )
    for key, class_row in classes.items():
        if class_member_counts[key] != class_row.get("raw_presentation_count"):
            fail("THETA2_LEDGER_CLASS_MEMBER_COUNT_FAIL", key)
    return category_counts


def expected_rebound_replay_bytes(
    package_root: Path, artifact_root: Path
) -> dict[str, bytes]:
    """Rebind only legacy provenance to the locked current compiler."""
    current = current_generator_bindings(package_root)
    rank_name = "exact_rank_certificates.json.gz"
    restoration_name = "fixed_full_restoration_closure.json.gz"

    rank_path = artifact_root / rank_name
    frozen_rank = read_gzip_json(rank_path)
    if frozen_rank.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_RANK_LEGACY_COMPILER_BINDING_FAIL")
    frozen_rank_plain = canonical_json_bytes(frozen_rank) + b"\n"
    if deterministic_gzip_bytes(frozen_rank_plain) != rank_path.read_bytes():
        fail("THETA2_RANK_LEGACY_CANONICAL_BYTES_FAIL")
    current_rank = rebound_payload(
        frozen_rank,
        (
            (
                ("compiler_sha256",),
                LEGACY_COMPILER_SHA256,
                current["compiler_sha256"],
            ),
        ),
    )
    current_rank_plain = canonical_json_bytes(current_rank) + b"\n"
    current_rank_gzip = deterministic_gzip_bytes(current_rank_plain)

    restoration_path = artifact_root / restoration_name
    frozen_restoration = read_gzip_json(restoration_path)
    restoration_bindings = frozen_restoration.get("bindings", {})
    if restoration_bindings.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_RESTORATION_LEGACY_COMPILER_BINDING_FAIL")
    if (
        restoration_bindings.get("canonicalizer_sha256")
        != LEGACY_CANONICALIZER_SHA256
    ):
        fail("THETA2_RESTORATION_LEGACY_CANONICALIZER_BINDING_FAIL")
    frozen_restoration_plain = canonical_json_bytes(frozen_restoration) + b"\n"
    if (
        deterministic_gzip_bytes(frozen_restoration_plain)
        != restoration_path.read_bytes()
    ):
        fail("THETA2_RESTORATION_LEGACY_CANONICAL_BYTES_FAIL")
    current_restoration = rebound_payload(
        frozen_restoration,
        (
            (
                ("bindings", "compiler_sha256"),
                LEGACY_COMPILER_SHA256,
                current["compiler_sha256"],
            ),
            (
                ("bindings", "canonicalizer_sha256"),
                LEGACY_CANONICALIZER_SHA256,
                current["canonicalizer_sha256"],
            ),
        ),
    )
    current_restoration_plain = canonical_json_bytes(current_restoration) + b"\n"
    current_restoration_gzip = deterministic_gzip_bytes(current_restoration_plain)

    summary_path = artifact_root / "theta2_five_port_summary.json"
    frozen_summary = load_plain_json(summary_path)
    if pretty_json_bytes(frozen_summary) != summary_path.read_bytes():
        fail("THETA2_SUMMARY_LEGACY_CANONICAL_BYTES_FAIL")
    summary_bindings = frozen_summary.get("bindings", {})
    if summary_bindings.get("compiler_sha256") != LEGACY_COMPILER_SHA256:
        fail("THETA2_SUMMARY_LEGACY_COMPILER_BINDING_FAIL")
    if (
        summary_bindings.get("canonicalizer_sha256")
        != LEGACY_CANONICALIZER_SHA256
    ):
        fail("THETA2_SUMMARY_LEGACY_CANONICALIZER_BINDING_FAIL")
    if summary_bindings.get("input_lock_sha256") != LEGACY_INPUT_LOCK_SHA256:
        fail("THETA2_SUMMARY_LEGACY_INPUT_LOCK_BINDING_FAIL")
    current_summary = rebound_payload(
        frozen_summary,
        (
            (
                ("bindings", "compiler_sha256"),
                LEGACY_COMPILER_SHA256,
                current["compiler_sha256"],
            ),
            (
                ("bindings", "canonicalizer_sha256"),
                LEGACY_CANONICALIZER_SHA256,
                current["canonicalizer_sha256"],
            ),
            (
                ("bindings", "input_lock_sha256"),
                LEGACY_INPUT_LOCK_SHA256,
                current["input_lock_sha256"],
            ),
        ),
    )
    current_summary["artifacts"][rank_name] = gzip_metadata(
        current_rank_gzip, current_rank_plain
    )
    current_summary["artifacts"][restoration_name] = gzip_metadata(
        current_restoration_gzip, current_restoration_plain
    )
    current_summary.pop("payload_sha256_without_hash", None)
    current_summary["payload_sha256_without_hash"] = sha_object(current_summary)

    return {
        rank_name: current_rank_gzip,
        restoration_name: current_restoration_gzip,
        "theta2_five_port_summary.json": pretty_json_bytes(current_summary),
    }


def full_regeneration(package_root: Path, artifact_root: Path, timeout_seconds: float):
    rebound_expected = expected_rebound_replay_bytes(package_root, artifact_root)
    with tempfile.TemporaryDirectory(prefix="k2p_theta2_five_port_replay_") as temporary:
        replay_root = Path(temporary) / "artifacts"
        command = [
            sys.executable,
            "-B",
            str(Path(__file__).with_name("generate_theta2_ledger.py")),
            "--package-root",
            str(package_root),
            "--output-root",
            str(replay_root),
        ]
        environment = dict(os.environ)
        environment.pop("PYTHONOPTIMIZE", None)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            result = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parent,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            fail("THETA2_FULL_REPLAY_TIMEOUT", timeout_seconds)
        if result.returncode != 0:
            fail(
                "THETA2_FULL_REPLAY_FAIL",
                (result.stdout + result.stderr).decode(errors="replace")[-5000:],
            )
        if b"THETA2_FIVE_PORT_PRIMITIVE_CLOSURE_PASS" not in result.stdout:
            fail("THETA2_FULL_REPLAY_TERMINAL_FAIL")
        for name in ARTIFACT_NAMES + ("theta2_five_port_summary.json",):
            expected = artifact_root / name
            observed = replay_root / name
            expected_bytes = rebound_expected.get(name)
            if expected_bytes is None:
                expected_bytes = expected.read_bytes()
            if observed.read_bytes() != expected_bytes:
                fail(
                    "THETA2_FULL_REPLAY_BYTE_MISMATCH",
                    {
                        "name": name,
                        "expected": hashlib.sha256(expected_bytes).hexdigest(),
                        "observed": sha_file(observed),
                    },
                )
    print(
        "THETA2_FULL_PRIMITIVE_REPLAY_PASS "
        "raw=2946240 descriptors=120 classes=480 "
        "legacy_provenance_rebound=true other_artifacts_byte_identical=true"
    )


def main() -> None:
    if not __debug__:
        fail("THETA2_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=900.0)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        fail("THETA2_TIMEOUT_FAIL")
    artifact_root = args.artifact_root.resolve()
    summary = validate_summary(artifact_root)
    rank_catalog = validate_rank_payload(
        read_gzip_json(artifact_root / "exact_rank_certificates.json.gz")
    )
    topology, quadratics, isomorphisms, anchors = validate_proof_payload(
        read_gzip_json(artifact_root / "direct_proof_certificates.json.gz")
    )
    class_payload = read_gzip_json(artifact_root / "class_partition.json.gz")
    classes = validate_classes(
        class_payload,
        rank_catalog,
        quadratics,
        isomorphisms,
        anchors,
    )
    restoration = validate_restoration_payload(
        read_gzip_json(
            artifact_root / "fixed_full_restoration_closure.json.gz"
        ),
        class_payload,
        classes,
    )
    validate_ledger(
        artifact_root / "raw_directional_ledger.jsonl.gz",
        classes,
        topology,
    )
    if summary.get("unresolved_class_count") != 0:
        fail("THETA2_UNRESOLVED_FAIL")
    if summary.get("restoration_closure") != restoration.get("census"):
        fail("THETA2_SUMMARY_RESTORATION_BINDING_FAIL")
    print(
        "THETA2_STRUCTURAL_REPLAY_PASS "
        "raw=2946240 descriptors=120 classes=480 restoration_children=864 unresolved=0"
    )
    if not args.quick:
        full_regeneration(
            args.package_root.resolve(), artifact_root, args.timeout_seconds
        )


if __name__ == "__main__":
    main()
