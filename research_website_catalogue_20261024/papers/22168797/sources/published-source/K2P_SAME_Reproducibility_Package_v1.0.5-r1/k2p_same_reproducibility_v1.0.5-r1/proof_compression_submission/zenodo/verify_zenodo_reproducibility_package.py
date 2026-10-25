#!/usr/bin/env python3
"""Independent fail-closed checker for the public K2P-SAME archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import stat
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable


ARCHIVE_ROOT = "k2p_same_reproducibility_v1.0.5-r1"
MANIFEST_NAME = "ZENODO_REPRODUCIBILITY_MANIFEST.json"
ZIP_TIMESTAMP = (2026, 8, 29, 0, 0, 0)
ZIP_MODE = 0o100644
FROZEN_LEDGER_RELATIVE = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
RELEASE_LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
EXPECTED_FROZEN_COUNT = 408
EXPECTED_FROZEN_BYTES = 479_383_009
EXPECTED_FROZEN_ROOT = "ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73"
EXPECTED_LOCK_SHA256 = "bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53"
EXPECTED_LOCK_PAYLOAD = "3a0c89c4cedb7202161289eab7b3671c004ae638bcf90eba837e45e3e1890fc5"
EXPECTED_PUBLICATION_BYTES = 4_027_522
EXPECTED_PUBLICATION_ROOT = "4ecc42ce7682e4aa196c197d91b4ac4862b6c6e7c555de329a21970884fc5249"


PUBLIC_SUBMISSION_FILES = {
    "output/referee/REFEREE_BUNDLE_CONTENTS.json",
    "output/referee/build_referee_bundle.py",
    "proof_compression_submission/COMPRESSED_BOUNDED_THEOREM.md",
    "proof_compression_submission/COMPRESSION_GATES.md",
    "proof_compression_submission/PDF_BUILD_REPORT.json",
    "proof_compression_submission/PDF_BUILD_REPORT.md",
    "proof_compression_submission/PROOF_COMPRESSION_RESULT.json",
    "proof_compression_submission/PROOF_COMPRESSION_RESULT.md",
    "proof_compression_submission/THEOREM_TO_TEMPLATE_CROSSWALK.json",
    "proof_compression_submission/THEOREM_TO_TEMPLATE_CROSSWALK.md",
    "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
    "proof_compression_submission/adversarial_review/audit_article_sources.py",
    "proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py",
    "proof_compression_submission/analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json",
    "proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md",
    "proof_compression_submission/analysis/PROOF_COMPRESSION_BASELINE.json",
    "proof_compression_submission/analysis/PROOF_COMPRESSION_BASELINE.md",
    "proof_compression_submission/analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json",
    "proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py",
    "proof_compression_submission/analysis/compression_common.py",
    "proof_compression_submission/analysis/derive_baseline_and_universe.py",
    "proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py",
    "proof_compression_submission/analysis/verify_family_coverage_equivalence.py",
    "proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py",
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/build_clean_full_replay_telemetry.py",
    "proof_compression_submission/build_compressed_release.py",
    "proof_compression_submission/build_submission_pdfs.py",
    "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json",
    "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md",
    "proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py",
    "proof_compression_submission/crosswalk/test_strict_json.py",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json",
    "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json",
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf",
    "proof_compression_submission/output/logs/article.log",
    "proof_compression_submission/output/logs/supplement.log",
    "proof_compression_submission/probe/PROBE_WORD_COVERAGE.json",
    "proof_compression_submission/probe/PROBE_WORD_THEOREM.md",
    "proof_compression_submission/probe/verify_probe_word_theorem.py",
    "proof_compression_submission/restoration/RESTORATION_ARCHETYPES.json",
    "proof_compression_submission/restoration/RESTORATION_ARCHETYPES.md",
    "proof_compression_submission/restoration/RESTORATION_ARCHETYPE_VERIFICATION.json",
    "proof_compression_submission/restoration/analyze_restoration_archetypes.py",
    "proof_compression_submission/restoration/verify_restoration_archetypes.py",
    "proof_compression_submission/results/COMPRESSION_MUTATION_RESULT.json",
    "proof_compression_submission/results/OLD_NEW_EQUIVALENCE_RESULT.json",
    "proof_compression_submission/run_compression_mutations.py",
    "proof_compression_submission/supplement/certificate_appendix.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json",
    "proof_compression_submission/templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.md",
    "proof_compression_submission/templates/PRINTED_CERTIFICATE_APPENDIX.json",
    "proof_compression_submission/templates/build_printed_certificate_appendix.py",
    "proof_compression_submission/templates/derive_direct_templates.py",
    "proof_compression_submission/templates/test_printed_certificate_appendix_mutations.py",
    "proof_compression_submission/templates/verify_printed_certificate_appendix.py",
    "proof_compression_submission/test_clean_full_replay_telemetry.py",
    "proof_compression_submission/verify_compressed_release.py",
    "proof_compression_submission/verify_old_new_equivalence.py",
}


PACKAGING_FILES = {
    "proof_compression_submission/zenodo/README.md",
    "proof_compression_submission/zenodo/build_zenodo_reproducibility_package.py",
    "proof_compression_submission/zenodo/verify_zenodo_reproducibility_package.py",
    "proof_compression_submission/zenodo/test_zenodo_reproducibility_mutations.py",
    "proof_compression_submission/zenodo/build_zenodo_upload_set.py",
}


EXCLUDED_PRIVATE_PATHS = {
    "output/referee/README.md",
    "proof_compression_submission/README.md",
    "proof_compression_submission/crosswalk/README.md",
    "proof_compression_submission/AI_REFEREE_PROMPT.md",
    "proof_compression_submission/FEEDBACK_DISPOSITION.md",
    "proof_compression_submission/FRESH_ADVERSARIAL_R2_DISPOSITION.md",
    "proof_compression_submission/FRESH_ADVERSARIAL_R3_DISPOSITION.md",
    "proof_compression_submission/FRESH_ADVERSARIAL_R4_DISPOSITION.md",
    "proof_compression_submission/FRESH_REVIEW_DISPOSITION.md",
    "proof_compression_submission/RESEARCH_LOG.md",
    "proof_compression_submission/adversarial_review/ADVERSARIAL_ARTICLE_AUDIT.md",
    "proof_compression_submission/adversarial_review/RESEARCH_LOG.md",
    "proof_compression_submission/analysis/RESEARCH_LOG.md",
    "proof_compression_submission/crosswalk/CROSSWALK_BUNDLE_MUTATION_REPORT.json",
    "proof_compression_submission/crosswalk/RESEARCH_LOG.md",
    "proof_compression_submission/crosswalk/build_revised_referee_bundle.py",
    "proof_compression_submission/crosswalk/check_revised_referee_bundle.py",
    "proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py",
    "proof_compression_submission/probe/RESEARCH_LOG.md",
    "proof_compression_submission/restoration/RESEARCH_LOG.md",
    "proof_compression_submission/results/.gitkeep",
    "proof_compression_submission/results/VERIFICATION_TRANSCRIPT.md",
}


EXPECTED_MANUSCRIPT_HASHES = {
    "proof_compression_submission/article/main.tex": "43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d",
    "proof_compression_submission/article/references.bib": "781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6",
    "proof_compression_submission/supplement/supplement.tex": "d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33",
    "proof_compression_submission/supplement/compression_tables.tex": "22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81",
    "proof_compression_submission/supplement/certificate_appendix.tex": "1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649",
}


EXPECTED_PDF_HASHES = {
    "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf": "e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4",
    "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf": "0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d",
}


EXPECTED_EXECUTION_HASHES = {
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json": "0d2fd0206181fe4c08ebff1367592809d0b8126d58aee3d91980941bfa55a95e",
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json": "eab3c1d6a096ef469b3db4844ea567a49e8e8ea6e62a6c8a2506814773cb6d50",
    "proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json": "0bc92a5f1f8328b6ce51945233a5152f5a28e96a99f538568bf9d057f92a8a55",
    "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json": "92b58bb3b518c257c2f78fcc77d92c5a0d547a9dfaf25ca06215c47a0616fc62",
    "proof_compression_submission/results/COMPRESSION_MUTATION_RESULT.json": "e0713d04eb49b7946a36f02f5a13411fe24f1c0e3adb79f97e9ba459b2ffe62f",
    "proof_compression_submission/results/OLD_NEW_EQUIVALENCE_RESULT.json": "e7e0842c74b084652beb71f8df91b026f46dc762003b9f83dd1d333eb07bed8b",
}


EXPECTED_PROBE_HASHES = {
    "proof_compression_submission/probe/PROBE_WORD_COVERAGE.json": "c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660",
    "proof_compression_submission/probe/PROBE_WORD_THEOREM.md": "f095c3169efb24f5e0bff35c039b081f957815f116d0eeb10fb6aa7a20b5ad61",
    "proof_compression_submission/probe/verify_probe_word_theorem.py": "8dcc191cc3af59a5b4f5950d6b15202823c943015be30cdd5ee21db62482ed28",
}


EXPECTED_TAGS = {
    "manuscript": "k2p-same-biorxiv-v1.0.5",
    "accepted_evidence": "k2p-same-referee-package-v1.0.5-r1",
    "zenodo_package": "k2p-same-zenodo-v1.0.5-r1",
}


EXPECTED_ENTRYPOINTS = {
    "extracted_root_check": (
        "python3 -B proof_compression_submission/zenodo/"
        "verify_zenodo_reproducibility_package.py --root ."
    ),
    "frozen_ledger_check": "python3 -B output/referee/build_referee_bundle.py --check-only",
    "quick_replay": (
        ".venv/bin/python -B work/final_theorem_release/"
        "verify_final_theorem_release.py --quick"
    ),
    "full_replay": (
        ".venv/bin/python -B work/final_theorem_release/"
        "verify_final_theorem_release.py --full"
    ),
    "release_mutations": (
        ".venv/bin/python -B work/final_theorem_release/"
        "run_release_mutations.py"
    ),
}


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (RecursionError, TypeError, ValueError) as error:
        fail(f"canonical JSON failure: {error}")


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def strict_json_bytes(data: bytes, label: str) -> Any:
    if len(data) > 64 * 1024 * 1024:
        fail(f"JSON byte limit exceeded: {label}")

    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                fail(f"duplicate JSON name in {label}: {key!r}")
            result[key] = value
        return result

    def reject_constant(token: str) -> None:
        fail(f"non-finite JSON number in {label}: {token}")

    def finite_float(token: str) -> float:
        value = float(token)
        if not math.isfinite(value):
            reject_constant(token)
        return value

    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"invalid JSON in {label}: {error}")


def safe_relative(value: str) -> PurePosixPath:
    if (
        not isinstance(value, str)
        or "\\" in value
        or "\x00" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
        or unicodedata.normalize("NFC", value) != value
    ):
        fail(f"unsafe archive path: {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail(f"unsafe archive path: {value!r}")
    return path


def manifest_precheck(manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        fail("manifest is not an object")
    expected_keys = {
        "accepted_bindings",
        "accepted_censuses",
        "archive_manifest_name",
        "archive_root",
        "category_counts",
        "content_ledger_root_sha256",
        "creator",
        "entrypoints",
        "excluded_private_paths",
        "file_count_excluding_manifest",
        "files",
        "frozen_evidence",
        "git_provenance",
        "payload_sha256",
        "publication_layer",
        "release_date",
        "schema",
        "scope",
        "source_tags",
        "title",
        "total_bytes_excluding_manifest",
        "version",
        "zip_policy",
    }
    if set(manifest) != expected_keys:
        fail("manifest top-level field set mismatch")
    payload = manifest.get("payload_sha256")
    unsigned = dict(manifest)
    unsigned.pop("payload_sha256", None)
    if not isinstance(payload, str) or payload != canonical_hash(unsigned):
        fail("manifest payload seal mismatch")
    if manifest.get("schema") != "k2p-zenodo-reproducibility-manifest-v1":
        fail("manifest schema mismatch")
    if manifest.get("title") != "K2P-SAME principal-domain reproducibility package":
        fail("manifest title mismatch")
    if manifest.get("scope") != (
        "Positive-Fourier K2P principal domain D_plus, strict continuous time, "
        "and the 4n-3 weak-class sharpness theorem"
    ):
        fail("manifest scope mismatch")
    if manifest.get("version") != "1.0.5-r1" or manifest.get("release_date") != "2026-08-29":
        fail("manifest version or date mismatch")
    if manifest.get("archive_root") != ARCHIVE_ROOT or manifest.get("archive_manifest_name") != MANIFEST_NAME:
        fail("manifest archive identity mismatch")
    if manifest.get("creator") != {"name": "Alec Kriebel", "orcid": "0009-0001-9320-500X"}:
        fail("manifest creator mismatch")
    if manifest.get("source_tags") != EXPECTED_TAGS:
        fail("manifest source-tag mismatch")
    if manifest.get("entrypoints") != EXPECTED_ENTRYPOINTS:
        fail("manifest entrypoint mismatch")
    if manifest.get("git_provenance") != {
        "manuscript_tag_object": "0023a8461dcb71f826fc1537c7757c5af09dc3dd",
        "manuscript_commit": "5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e",
        "accepted_evidence_tag_object": "6c9c89d38f4f4cdc9c328d8bb1237458c617136d",
        "accepted_evidence_commit": "e2f6e32e6fe885e90c8e83a8c5b00785e663a4ae",
    }:
        fail("manifest Git provenance mismatch")
    excluded = manifest.get("excluded_private_paths")
    if (
        not isinstance(excluded, list)
        or len(excluded) != len(EXCLUDED_PRIVATE_PATHS)
        or set(excluded) != EXCLUDED_PRIVATE_PATHS
    ):
        fail("manifest private-exclusion list mismatch")
    if manifest.get("accepted_bindings") != {
        "manuscript_sources": EXPECTED_MANUSCRIPT_HASHES,
        "rendered_pdfs": EXPECTED_PDF_HASHES,
        "execution_and_crosswalk": EXPECTED_EXECUTION_HASHES,
        "probe_word_theorem": EXPECTED_PROBE_HASHES,
    }:
        fail("manifest accepted bindings mismatch")
    if manifest.get("accepted_censuses") != {
        "clean_full_replay_layers": 41,
        "theorem_crosswalk_claims": 13,
        "release_mutations_rejected": 25,
        "compression_mutations_rejected": 20,
    }:
        fail("manifest accepted census mismatch")
    if manifest.get("frozen_evidence") != {
        "file_count": EXPECTED_FROZEN_COUNT,
        "total_bytes": EXPECTED_FROZEN_BYTES,
        "content_ledger_root_sha256": EXPECTED_FROZEN_ROOT,
        "release_lock_sha256": EXPECTED_LOCK_SHA256,
        "release_lock_payload_sha256": EXPECTED_LOCK_PAYLOAD,
    }:
        fail("manifest frozen-evidence authority mismatch")
    if manifest.get("publication_layer") != {
        "file_count": 64,
        "total_bytes": EXPECTED_PUBLICATION_BYTES,
        "content_ledger_root_sha256": EXPECTED_PUBLICATION_ROOT,
    }:
        fail("manifest publication-layer authority mismatch")
    if manifest.get("zip_policy") != {
        "compression": "deflate level 9",
        "member_mode_octal": "100644",
        "member_order": "UTF-8 path lexicographic",
        "member_timestamp": "2026-08-29 00:00:00",
        "archive_comment": "empty",
        "member_extra_fields": "empty",
    }:
        fail("manifest ZIP policy mismatch")
    return manifest


def validate_frozen_ledger(data: bytes) -> dict[str, dict[str, Any]]:
    ledger = strict_json_bytes(data, FROZEN_LEDGER_RELATIVE)
    if not isinstance(ledger, dict):
        fail("frozen ledger is not an object")
    expected = {
        "schema": "k2p-principal-d-plus-referee-content-ledger-v1",
        "file_count": EXPECTED_FROZEN_COUNT,
        "total_bytes": EXPECTED_FROZEN_BYTES,
        "content_ledger_root_sha256": EXPECTED_FROZEN_ROOT,
        "release_lock_sha256": EXPECTED_LOCK_SHA256,
        "release_lock_payload_sha256": EXPECTED_LOCK_PAYLOAD,
    }
    for key, value in expected.items():
        if ledger.get(key) != value:
            fail(f"frozen ledger {key} mismatch")
    files = ledger.get("files")
    if not isinstance(files, dict) or len(files) != EXPECTED_FROZEN_COUNT:
        fail("frozen ledger file map mismatch")
    canonical: dict[str, dict[str, Any]] = {}
    for relative in sorted(files):
        safe_relative(relative)
        row = files[relative]
        if (
            not isinstance(row, dict)
            or set(row) != {"bytes", "sha256"}
            or not isinstance(row.get("bytes"), int)
            or row["bytes"] < 0
            or not isinstance(row.get("sha256"), str)
            or len(row["sha256"]) != 64
            or any(character not in "0123456789abcdef" for character in row["sha256"])
        ):
            fail(f"malformed frozen ledger row: {relative}")
        canonical[relative] = row
    if canonical_hash(canonical) != EXPECTED_FROZEN_ROOT:
        fail("frozen ledger content root mismatch")
    if sum(row["bytes"] for row in canonical.values()) != EXPECTED_FROZEN_BYTES:
        fail("frozen ledger byte census mismatch")
    return canonical


def validate_rows(
    manifest: dict[str, Any], read: Callable[[str], bytes]
) -> dict[str, dict[str, Any]]:
    files = manifest.get("files")
    if not isinstance(files, dict):
        fail("manifest file map missing")
    declared_total = manifest.get("total_bytes_excluding_manifest")
    if (
        not isinstance(declared_total, int)
        or declared_total < EXPECTED_FROZEN_BYTES
        or declared_total > 600 * 1024 * 1024
    ):
        fail("manifest total-byte safety bound mismatch")
    ledger_bytes = read(FROZEN_LEDGER_RELATIVE)
    frozen = validate_frozen_ledger(ledger_bytes)
    expected_paths = set(frozen) | PUBLIC_SUBMISSION_FILES | PACKAGING_FILES
    if set(files) != expected_paths:
        missing = sorted(expected_paths - set(files))
        extra = sorted(set(files) - expected_paths)
        fail(f"manifest allowlist mismatch; missing={missing[:3]} extra={extra[:3]}")
    if len(PUBLIC_SUBMISSION_FILES) != 64 or len(PACKAGING_FILES) != 5:
        fail("checker allowlist census mismatch")
    folded: dict[str, str] = {}
    for relative in sorted(files):
        safe_relative(relative)
        key = relative.casefold()
        previous = folded.get(key)
        if previous is not None and previous != relative:
            fail(f"case-folding path collision: {previous!r} and {relative!r}")
        folded[key] = relative
        row = files[relative]
        expected_category = (
            "frozen_evidence"
            if relative in frozen
            else "publication_layer"
            if relative in PUBLIC_SUBMISSION_FILES
            else "packaging_tools"
        )
        if (
            not isinstance(row, dict)
            or set(row) != {"bytes", "category", "sha256"}
            or row.get("category") != expected_category
            or not isinstance(row.get("bytes"), int)
            or row["bytes"] < 0
            or not isinstance(row.get("sha256"), str)
            or len(row["sha256"]) != 64
            or any(character not in "0123456789abcdef" for character in row["sha256"])
        ):
            fail(f"malformed manifest file row: {relative}")
        data = read(relative)
        if len(data) != row["bytes"] or sha256_bytes(data) != row["sha256"]:
            fail(f"manifest byte binding mismatch: {relative}")
        if relative in frozen and row != {**frozen[relative], "category": "frozen_evidence"}:
            fail(f"manifest/frozen-ledger mismatch: {relative}")
    if EXCLUDED_PRIVATE_PATHS & set(files):
        fail("private review artifact included")
    expected_counts = {
        "frozen_evidence": EXPECTED_FROZEN_COUNT,
        "publication_layer": 64,
        "packaging_tools": 5,
    }
    if manifest.get("category_counts") != expected_counts:
        fail("manifest category census mismatch")
    if manifest.get("file_count_excluding_manifest") != len(files):
        fail("manifest file census mismatch")
    if manifest.get("total_bytes_excluding_manifest") != sum(row["bytes"] for row in files.values()):
        fail("manifest total-byte census mismatch")
    if manifest.get("content_ledger_root_sha256") != canonical_hash(files):
        fail("manifest content-ledger root mismatch")
    publication = {
        relative: {"bytes": files[relative]["bytes"], "sha256": files[relative]["sha256"]}
        for relative in sorted(PUBLIC_SUBMISSION_FILES)
    }
    if sum(row["bytes"] for row in publication.values()) != EXPECTED_PUBLICATION_BYTES:
        fail("accepted publication-layer byte census mismatch")
    if canonical_hash(publication) != EXPECTED_PUBLICATION_ROOT:
        fail("accepted publication-layer content root mismatch")
    return files


def require_payload(value: dict[str, Any], expected: str, label: str) -> None:
    payload = value.get("payload_sha256")
    unsigned = dict(value)
    unsigned.pop("payload_sha256", None)
    if payload != expected or payload != canonical_hash(unsigned):
        fail(f"{label} payload mismatch")


def validate_semantics(read: Callable[[str], bytes]) -> None:
    lock_data = read(RELEASE_LOCK_RELATIVE)
    if sha256_bytes(lock_data) != EXPECTED_LOCK_SHA256:
        fail("release lock byte hash mismatch")
    lock = strict_json_bytes(lock_data, RELEASE_LOCK_RELATIVE)
    if not isinstance(lock, dict):
        fail("release lock is not an object")
    require_payload(lock, EXPECTED_LOCK_PAYLOAD, "release lock")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("release lock is not promotion-ready")

    for relative, expected in {
        **EXPECTED_MANUSCRIPT_HASHES,
        **EXPECTED_PDF_HASHES,
        **EXPECTED_EXECUTION_HASHES,
        **EXPECTED_PROBE_HASHES,
    }.items():
        if sha256_bytes(read(relative)) != expected:
            fail(f"accepted semantic binding mismatch: {relative}")

    full = strict_json_bytes(
        read("proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"),
        "full replay",
    )
    if (
        not isinstance(full, dict)
        or full.get("schema") != "k2p-principal-d-plus-final-theorem-replay-report-v1"
        or full.get("status") != "PASS"
        or full.get("mode") != "full"
        or full.get("promotion_ready") is not True
        or full.get("blockers") != []
        or not isinstance(full.get("layer_replays"), list)
        or len(full["layer_replays"]) != 41
        or any(
            not isinstance(row, dict) or row.get("status") != "PASS"
            for row in full["layer_replays"]
        )
    ):
        fail("stored full replay semantic mismatch")

    telemetry = strict_json_bytes(
        read("proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"),
        "full replay telemetry",
    )
    if (
        not isinstance(telemetry, dict)
        or telemetry.get("schema") != "k2p-final-clean-full-replay-telemetry-v1"
        or telemetry.get("status") != "PASS"
        or telemetry.get("clean_detached_checkout") is not True
        or telemetry.get("report", {}).get("sha256") != EXPECTED_EXECUTION_HASHES[
            "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
        ]
        or telemetry.get("report", {}).get("layer_count") != 41
        or telemetry.get("release_lock", {}).get("sha256") != EXPECTED_LOCK_SHA256
    ):
        fail("stored full replay telemetry semantic mismatch")

    mutations = strict_json_bytes(
        read("proof_compression_submission/output/FINAL_RELEASE_MUTATIONS.json"),
        "release mutations",
    )
    if not isinstance(mutations, dict):
        fail("release mutation report is not an object")
    require_payload(
        mutations,
        "a12b19d10abde01fc1f51c17aad5d5e9b35550ec8f019f7ba3a11f4fca65b81a",
        "release mutations",
    )
    if (
        mutations.get("schema") != "k2p-principal-d-plus-final-release-mutations-v2"
        or mutations.get("status") != "PASS"
        or mutations.get("required_mutation_count") != 25
        or mutations.get("observed_mutation_count") != 25
        or mutations.get("survivors") != 0
        or mutations.get("blockers") != []
        or len(mutations.get("mutations", [])) != 25
        or any(row.get("status") != "REJECTED" for row in mutations.get("mutations", []))
    ):
        fail("release mutation semantic mismatch")

    crosswalk = strict_json_bytes(
        read("proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"),
        "theorem crosswalk",
    )
    if not isinstance(crosswalk, dict):
        fail("theorem crosswalk is not an object")
    require_payload(
        crosswalk,
        "8b77b1b73aaac6dc058bd187e34ed7efed1f210faaed34bbf9152712141cf3f2",
        "theorem crosswalk",
    )
    if (
        crosswalk.get("schema") != "k2p-theorem-artifact-reproducibility-crosswalk-v2"
        or crosswalk.get("status") != "PASS_PC_PARTIAL"
        or len(crosswalk.get("claims", [])) != 13
    ):
        fail("theorem crosswalk semantic mismatch")

    compression = strict_json_bytes(
        read("proof_compression_submission/results/COMPRESSION_MUTATION_RESULT.json"),
        "compression mutations",
    )
    if not isinstance(compression, dict):
        fail("compression mutation report is not an object")
    require_payload(
        compression,
        "684e8be68dc19f63505ecf111a02a81015d33852f01301bd0dcf2cf5c750cbe5",
        "compression mutations",
    )
    if (
        compression.get("schema") != "k2p-pc-partial-compression-mutation-result-v1"
        or compression.get("status") != "PASS"
        or compression.get("accepted_mutations") != 0
        or compression.get("rejected_mutations") != 20
        or len(compression.get("mutations", [])) != 20
        or any(row.get("status") != "REJECTED_AS_REQUIRED" for row in compression.get("mutations", []))
    ):
        fail("compression mutation semantic mismatch")
    if compression.get("probe_current_binding") != {
        "coverage_path": "probe/PROBE_WORD_COVERAGE.json",
        "coverage_payload_sha256": "d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49",
        "coverage_schema": "k2p-probe-word-theorem-coverage-v1",
        "coverage_sha256": EXPECTED_PROBE_HASHES[
            "proof_compression_submission/probe/PROBE_WORD_COVERAGE.json"
        ],
        "theorem_path": "probe/PROBE_WORD_THEOREM.md",
    }:
        fail("compression/probe current-authority binding mismatch")

    coverage = strict_json_bytes(
        read("proof_compression_submission/probe/PROBE_WORD_COVERAGE.json"),
        "probe word coverage",
    )
    if not isinstance(coverage, dict):
        fail("probe word coverage is not an object")
    require_payload(
        coverage,
        "d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49",
        "probe word coverage",
    )
    if coverage.get("schema") != "k2p-probe-word-theorem-coverage-v1" or coverage.get("status") != "PASS":
        fail("probe word coverage semantic mismatch")
    theorem_text = read("proof_compression_submission/probe/PROBE_WORD_THEOREM.md").decode("utf-8")
    for digest in (
        EXPECTED_PROBE_HASHES["proof_compression_submission/probe/PROBE_WORD_COVERAGE.json"],
        "d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49",
    ):
        if digest not in theorem_text:
            fail("probe theorem printed authority binding mismatch")

    equivalence = strict_json_bytes(
        read("proof_compression_submission/results/OLD_NEW_EQUIVALENCE_RESULT.json"),
        "old/new equivalence",
    )
    if not isinstance(equivalence, dict):
        fail("old/new equivalence report is not an object")
    require_payload(
        equivalence,
        "09a6976c9460c2c070f67b0bdf71403980eea44d82718a5f0832442b5f84b090",
        "old/new equivalence",
    )
    if equivalence.get("status") != "PASS" or equivalence.get("unresolved_mathematical_records") != 0:
        fail("old/new equivalence semantic mismatch")

    for relative, schema in (
        (
            "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
            "k2p-submission-article-static-audit-v3",
        ),
        (
            "proof_compression_submission/PDF_BUILD_REPORT.json",
            "k2p-submission-pdf-build-report-v3",
        ),
    ):
        value = strict_json_bytes(read(relative), relative)
        if not isinstance(value, dict) or value.get("schema") != schema or value.get("status") != "PASS":
            fail(f"stored PASS result mismatch: {relative}")


def validate_manifest_and_reader(
    manifest_data: bytes, read: Callable[[str], bytes]
) -> dict[str, Any]:
    manifest = manifest_precheck(strict_json_bytes(manifest_data, MANIFEST_NAME))
    expected_pretty = json.dumps(
        manifest,
        allow_nan=False,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    if manifest_data != expected_pretty:
        fail("manifest byte representation is not canonical pretty JSON")
    validate_rows(manifest, read)
    validate_semantics(read)
    return manifest


def verify_root(root: Path) -> dict[str, Any]:
    if root.is_symlink():
        fail("extracted root must not be a symlink")
    root = root.resolve()
    manifest_path = root / MANIFEST_NAME
    if not manifest_path.is_file() or manifest_path.is_symlink():
        fail("missing or symbolic extracted manifest")
    if manifest_path.stat().st_size > 4 * 1024 * 1024:
        fail("extracted manifest exceeds byte limit")

    provisional = manifest_precheck(strict_json_bytes(manifest_path.read_bytes(), MANIFEST_NAME))
    declared = provisional.get("files")
    if not isinstance(declared, dict):
        fail("extracted manifest file map missing")
    expected_files = set(declared) | {MANIFEST_NAME}
    actual_files: set[str] = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            fail(f"symlink in extracted tree: {path.relative_to(root).as_posix()}")
        if path.is_dir():
            continue
        if not path.is_file():
            fail(f"special entry in extracted tree: {path.relative_to(root).as_posix()}")
        relative = path.relative_to(root).as_posix()
        safe_relative(relative)
        actual_files.add(relative)
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        fail(f"extracted-tree allowlist mismatch; missing={missing[:3]} extra={extra[:3]}")

    def read(relative: str) -> bytes:
        path = root.joinpath(*safe_relative(relative).parts)
        if not path.is_file() or path.is_symlink():
            fail(f"missing, symbolic, or non-regular extracted member: {relative}")
        return path.read_bytes()

    manifest = validate_manifest_and_reader(manifest_path.read_bytes(), read)
    for relative in EXCLUDED_PRIVATE_PATHS:
        if root.joinpath(*PurePosixPath(relative).parts).exists():
            fail(f"private review artifact present in extracted tree: {relative}")
    return {
        "mode": "root",
        "status": "PASS",
        "file_count_excluding_manifest": manifest["file_count_excluding_manifest"],
        "content_ledger_root_sha256": manifest["content_ledger_root_sha256"],
        "manifest_payload_sha256": manifest["payload_sha256"],
    }


def verify_archive(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        fail("archive path must not be a symlink")
    path = path.parent.resolve() / path.name
    if not path.is_file() or path.is_symlink():
        fail("missing, symbolic, or non-regular archive")
    with zipfile.ZipFile(path, "r") as archive:
        if archive.comment != b"":
            fail("archive comment is not empty")
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(infos) > 478:
            fail("ZIP member count exceeds the 478-member bound")
        if len(names) != len(set(names)):
            fail("duplicate ZIP member name")
        if names != sorted(names):
            fail("ZIP member order mismatch")
        folded: dict[str, str] = {}
        relative_infos: dict[str, zipfile.ZipInfo] = {}
        prefix = f"{ARCHIVE_ROOT}/"
        for info in infos:
            name = info.filename
            if not name.startswith(prefix):
                fail(f"ZIP member has wrong archive root: {name!r}")
            relative = name[len(prefix):]
            safe_relative(relative)
            key = relative.casefold()
            previous = folded.get(key)
            if previous is not None and previous != relative:
                fail(f"case-folding ZIP collision: {previous!r} and {relative!r}")
            folded[key] = relative
            if info.is_dir() or name.endswith("/"):
                fail(f"directory member is forbidden: {name}")
            if info.date_time != ZIP_TIMESTAMP:
                fail(f"ZIP timestamp mismatch: {name}")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                fail(f"ZIP compression mismatch: {name}")
            if info.create_system != 3:
                fail(f"ZIP creator-system mismatch: {name}")
            mode = info.external_attr >> 16
            if mode != ZIP_MODE or not stat.S_ISREG(mode):
                fail(f"ZIP member mode mismatch: {name}")
            if info.flag_bits & 0x1:
                fail(f"encrypted ZIP member: {name}")
            if info.extra != b"" or info.comment != b"":
                fail(f"ZIP member metadata mismatch: {name}")
            relative_infos[relative] = info
        if len(infos) != 478:
            fail("ZIP member census mismatch")
        if MANIFEST_NAME not in relative_infos:
            fail("archive manifest member missing")
        if relative_infos[MANIFEST_NAME].file_size > 4 * 1024 * 1024:
            fail("archive manifest exceeds byte limit")
        manifest_data = archive.read(relative_infos[MANIFEST_NAME])
        provisional = manifest_precheck(strict_json_bytes(manifest_data, MANIFEST_NAME))
        declared = provisional.get("files")
        if not isinstance(declared, dict):
            fail("archive manifest file map missing")
        declared_sizes = [row.get("bytes") for row in declared.values() if isinstance(row, dict)]
        if (
            len(declared_sizes) != len(declared)
            or any(not isinstance(size, int) or size < 0 for size in declared_sizes)
            or sum(declared_sizes) > 600 * 1024 * 1024
        ):
            fail("archive declared-size safety bound mismatch")
        expected_names = set(declared) | {MANIFEST_NAME}
        if set(relative_infos) != expected_names:
            fail("ZIP member allowlist mismatch")
        for relative, row in declared.items():
            info = relative_infos[relative]
            if info.file_size != row.get("bytes"):
                fail(f"ZIP declared size mismatch: {relative}")

        def read(relative: str) -> bytes:
            info = relative_infos.get(relative)
            if info is None:
                fail(f"missing ZIP member: {relative}")
            return archive.read(info)

        manifest = validate_manifest_and_reader(manifest_data, read)
    return {
        "mode": "archive",
        "status": "PASS",
        "archive_bytes": path.stat().st_size,
        "archive_sha256": sha256_bytes(path.read_bytes()),
        "file_count_excluding_manifest": manifest["file_count_excluding_manifest"],
        "content_ledger_root_sha256": manifest["content_ledger_root_sha256"],
        "manifest_payload_sha256": manifest["payload_sha256"],
    }


def verify_optimized_mode_contract() -> None:
    result = subprocess.run(
        [sys.executable, "-O", "-B", str(Path(__file__).resolve()), "--self-test-optimized"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    diagnostic = (result.stdout + result.stderr).strip()
    if result.returncode != 1 or diagnostic != "optimized Python is forbidden":
        fail("optimized-mode rejection contract mismatch")


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--archive", type=Path)
    group.add_argument("--root", type=Path)
    group.add_argument("--self-test-optimized", action="store_true")
    args = parser.parse_args()
    if args.self_test_optimized:
        fail("self-test unexpectedly reached non-optimized execution")
    verify_optimized_mode_contract()
    result = verify_archive(args.archive) if args.archive is not None else verify_root(args.root)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
