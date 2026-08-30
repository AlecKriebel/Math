#!/usr/bin/env python3
"""Build the deterministic public K2P-SAME reproducibility archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[2]
ARCHIVE_ROOT = "k2p_same_reproducibility_v1.0.5-r1"
MANIFEST_NAME = "ZENODO_REPRODUCIBILITY_MANIFEST.json"
ZIP_TIMESTAMP = (2026, 8, 29, 0, 0, 0)
ZIP_MODE = 0o100644
FROZEN_LEDGER_RELATIVE = "output/referee/REFEREE_BUNDLE_CONTENTS.json"
EXPECTED_FROZEN_COUNT = 408
EXPECTED_FROZEN_BYTES = 479_383_009
EXPECTED_FROZEN_ROOT = "ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73"
EXPECTED_LOCK_SHA256 = "bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53"
EXPECTED_LOCK_PAYLOAD = "3a0c89c4cedb7202161289eab7b3671c004ae638bcf90eba837e45e3e1890fc5"
EXPECTED_PUBLICATION_BYTES = 4_027_522
EXPECTED_PUBLICATION_ROOT = "4ecc42ce7682e4aa196c197d91b4ac4862b6c6e7c555de329a21970884fc5249"


PUBLIC_SUBMISSION_FILES = (
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
)


PACKAGING_FILES = (
    "proof_compression_submission/zenodo/README.md",
    "proof_compression_submission/zenodo/build_zenodo_reproducibility_package.py",
    "proof_compression_submission/zenodo/verify_zenodo_reproducibility_package.py",
    "proof_compression_submission/zenodo/test_zenodo_reproducibility_mutations.py",
    "proof_compression_submission/zenodo/build_zenodo_upload_set.py",
)


EXCLUDED_PRIVATE_PATHS = (
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
)


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
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
        or unicodedata.normalize("NFC", value) != value
    ):
        fail(f"unsafe or noncanonical relative path: {value!r}")
    return path


def project_path(relative: str) -> Path:
    return PROJECT.joinpath(*safe_relative(relative).parts)


def regular_bytes(relative: str) -> bytes:
    path = project_path(relative)
    if not path.is_file() or path.is_symlink():
        fail(f"missing, symbolic, or non-regular package input: {relative}")
    return path.read_bytes()


def check_unique_paths(paths: list[str]) -> None:
    if len(paths) != len(set(paths)):
        fail("duplicate package path")
    folded: dict[str, str] = {}
    for relative in paths:
        safe_relative(relative)
        key = relative.casefold()
        previous = folded.get(key)
        if previous is not None and previous != relative:
            fail(f"case-folding path collision: {previous!r} and {relative!r}")
        folded[key] = relative


def load_frozen_ledger() -> dict[str, dict[str, int | str]]:
    value = strict_json_bytes(regular_bytes(FROZEN_LEDGER_RELATIVE), FROZEN_LEDGER_RELATIVE)
    if not isinstance(value, dict):
        fail("frozen ledger is not an object")
    expected_header = {
        "schema": "k2p-principal-d-plus-referee-content-ledger-v1",
        "file_count": EXPECTED_FROZEN_COUNT,
        "total_bytes": EXPECTED_FROZEN_BYTES,
        "content_ledger_root_sha256": EXPECTED_FROZEN_ROOT,
        "release_lock_sha256": EXPECTED_LOCK_SHA256,
        "release_lock_payload_sha256": EXPECTED_LOCK_PAYLOAD,
    }
    for key, expected in expected_header.items():
        if value.get(key) != expected:
            fail(f"frozen ledger {key} mismatch")
    files = value.get("files")
    if not isinstance(files, dict) or len(files) != EXPECTED_FROZEN_COUNT:
        fail("frozen ledger file map mismatch")
    check_unique_paths(list(files))
    actual: dict[str, dict[str, int | str]] = {}
    for relative in sorted(files):
        row = files[relative]
        if not isinstance(row, dict) or set(row) != {"bytes", "sha256"}:
            fail(f"malformed frozen row: {relative}")
        data = regular_bytes(relative)
        actual_row = {"bytes": len(data), "sha256": sha256_bytes(data)}
        if row != actual_row:
            fail(f"frozen file mismatch: {relative}")
        actual[relative] = actual_row
    if sum(int(row["bytes"]) for row in actual.values()) != EXPECTED_FROZEN_BYTES:
        fail("frozen total-byte mismatch")
    if canonical_hash(actual) != EXPECTED_FROZEN_ROOT:
        fail("frozen content-root mismatch")
    return actual


def check_expected_hashes(rows: dict[str, dict[str, Any]]) -> None:
    for relative, expected in {
        **EXPECTED_MANUSCRIPT_HASHES,
        **EXPECTED_PDF_HASHES,
        **EXPECTED_EXECUTION_HASHES,
        **EXPECTED_PROBE_HASHES,
    }.items():
        if rows.get(relative, {}).get("sha256") != expected:
            fail(f"accepted binding mismatch: {relative}")


def collect_files() -> dict[str, dict[str, Any]]:
    if len(PUBLIC_SUBMISSION_FILES) != 64:
        fail("public submission allowlist census mismatch")
    if len(PACKAGING_FILES) != 5:
        fail("packaging-tool allowlist census mismatch")
    frozen = load_frozen_ledger()
    overlap = set(frozen) & (set(PUBLIC_SUBMISSION_FILES) | set(PACKAGING_FILES))
    if overlap:
        fail(f"package category overlap: {sorted(overlap)[:3]}")
    rows: dict[str, dict[str, Any]] = {}
    for relative, row in frozen.items():
        rows[relative] = {**row, "category": "frozen_evidence"}
    for category, relatives in (
        ("publication_layer", PUBLIC_SUBMISSION_FILES),
        ("packaging_tools", PACKAGING_FILES),
    ):
        for relative in relatives:
            data = regular_bytes(relative)
            rows[relative] = {
                "bytes": len(data),
                "category": category,
                "sha256": sha256_bytes(data),
            }
    check_unique_paths(list(rows))
    for relative in EXCLUDED_PRIVATE_PATHS:
        if relative in rows:
            fail(f"private review artifact entered public package: {relative}")
    check_expected_hashes(rows)
    publication = {
        relative: {"bytes": rows[relative]["bytes"], "sha256": rows[relative]["sha256"]}
        for relative in sorted(PUBLIC_SUBMISSION_FILES)
    }
    if sum(int(row["bytes"]) for row in publication.values()) != EXPECTED_PUBLICATION_BYTES:
        fail("accepted publication-layer byte census mismatch")
    if canonical_hash(publication) != EXPECTED_PUBLICATION_ROOT:
        fail("accepted publication-layer content root mismatch")
    return dict(sorted(rows.items()))


def build_manifest(rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts = {
        category: sum(row["category"] == category for row in rows.values())
        for category in ("frozen_evidence", "publication_layer", "packaging_tools")
    }
    manifest: dict[str, Any] = {
        "schema": "k2p-zenodo-reproducibility-manifest-v1",
        "title": "K2P-SAME principal-domain reproducibility package",
        "version": "1.0.5-r1",
        "release_date": "2026-08-29",
        "archive_root": ARCHIVE_ROOT,
        "archive_manifest_name": MANIFEST_NAME,
        "scope": (
            "Positive-Fourier K2P principal domain D_plus, strict continuous time, "
            "and the 4n-3 weak-class sharpness theorem"
        ),
        "creator": {
            "name": "Alec Kriebel",
            "orcid": "0009-0001-9320-500X",
        },
        "source_tags": {
            "manuscript": "k2p-same-biorxiv-v1.0.5",
            "accepted_evidence": "k2p-same-referee-package-v1.0.5-r1",
            "zenodo_package": "k2p-same-zenodo-v1.0.5-r1",
        },
        "git_provenance": {
            "manuscript_tag_object": "0023a8461dcb71f826fc1537c7757c5af09dc3dd",
            "manuscript_commit": "5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e",
            "accepted_evidence_tag_object": "6c9c89d38f4f4cdc9c328d8bb1237458c617136d",
            "accepted_evidence_commit": "e2f6e32e6fe885e90c8e83a8c5b00785e663a4ae",
        },
        "frozen_evidence": {
            "file_count": EXPECTED_FROZEN_COUNT,
            "total_bytes": EXPECTED_FROZEN_BYTES,
            "content_ledger_root_sha256": EXPECTED_FROZEN_ROOT,
            "release_lock_sha256": EXPECTED_LOCK_SHA256,
            "release_lock_payload_sha256": EXPECTED_LOCK_PAYLOAD,
        },
        "publication_layer": {
            "file_count": len(PUBLIC_SUBMISSION_FILES),
            "total_bytes": EXPECTED_PUBLICATION_BYTES,
            "content_ledger_root_sha256": EXPECTED_PUBLICATION_ROOT,
        },
        "accepted_bindings": {
            "manuscript_sources": EXPECTED_MANUSCRIPT_HASHES,
            "rendered_pdfs": EXPECTED_PDF_HASHES,
            "execution_and_crosswalk": EXPECTED_EXECUTION_HASHES,
            "probe_word_theorem": EXPECTED_PROBE_HASHES,
        },
        "accepted_censuses": {
            "clean_full_replay_layers": 41,
            "theorem_crosswalk_claims": 13,
            "release_mutations_rejected": 25,
            "compression_mutations_rejected": 20,
        },
        "excluded_private_paths": list(EXCLUDED_PRIVATE_PATHS),
        "entrypoints": {
            "extracted_root_check": (
                "python3 -B proof_compression_submission/zenodo/"
                "verify_zenodo_reproducibility_package.py --root ."
            ),
            "frozen_ledger_check": (
                "python3 -B output/referee/build_referee_bundle.py --check-only"
            ),
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
        },
        "zip_policy": {
            "compression": "deflate level 9",
            "member_mode_octal": "100644",
            "member_order": "UTF-8 path lexicographic",
            "member_timestamp": "2026-08-29 00:00:00",
            "archive_comment": "empty",
            "member_extra_fields": "empty",
        },
        "category_counts": counts,
        "file_count_excluding_manifest": len(rows),
        "total_bytes_excluding_manifest": sum(int(row["bytes"]) for row in rows.values()),
        "content_ledger_root_sha256": canonical_hash(rows),
        "files": rows,
    }
    manifest["payload_sha256"] = canonical_hash(manifest)
    return manifest


def manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return json.dumps(
        manifest,
        allow_nan=False,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"


def archive_bytes_map(manifest: dict[str, Any]) -> dict[str, bytes]:
    members = {relative: regular_bytes(relative) for relative in manifest["files"]}
    members[MANIFEST_NAME] = manifest_bytes(manifest)
    return members


def write_archive(output: Path, manifest: dict[str, Any]) -> str:
    if output.is_symlink():
        fail("archive output path must not be a symlink")
    output = output.parent.resolve() / output.name
    output.parent.mkdir(parents=True, exist_ok=True)
    members = archive_bytes_map(manifest)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            allowZip64=True,
        ) as archive:
            for relative in sorted(members):
                name = f"{ARCHIVE_ROOT}/{relative}"
                info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = ZIP_MODE << 16
                info.extra = b""
                info.comment = b""
                archive.writestr(
                    info,
                    members[relative],
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return sha256_bytes(output.read_bytes())


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None and not args.check:
        parser.error("provide --output, --manifest-output, or --check")
    rows = collect_files()
    manifest = build_manifest(rows)
    result: dict[str, Any] = {
        "status": "PASS",
        "file_count_excluding_manifest": len(rows),
        "content_ledger_root_sha256": manifest["content_ledger_root_sha256"],
        "manifest_payload_sha256": manifest["payload_sha256"],
    }
    if args.manifest_output is not None:
        if args.manifest_output.is_symlink():
            fail("manifest output path must not be a symlink")
        manifest_output = args.manifest_output.parent.resolve() / args.manifest_output.name
        manifest_output.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{manifest_output.name}.", suffix=".tmp", dir=manifest_output.parent
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            temporary.write_bytes(manifest_bytes(manifest))
            temporary.replace(manifest_output)
        finally:
            temporary.unlink(missing_ok=True)
        result["manifest_path"] = str(manifest_output)
    if args.output is not None:
        result["archive_path"] = str(args.output)
        result["archive_sha256"] = write_archive(args.output, manifest)
        result["archive_bytes"] = args.output.stat().st_size
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
