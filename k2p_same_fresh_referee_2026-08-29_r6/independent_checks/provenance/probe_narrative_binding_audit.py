#!/usr/bin/env python3
"""Independently compare the probe theorem's printed current binding to bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


THEOREM = "proof_compression_submission/probe/PROBE_WORD_THEOREM.md"
COVERAGE = "proof_compression_submission/probe/PROBE_WORD_COVERAGE.json"
CROSSWALK = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
MANIFEST = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
TEMPLATE_CROSSWALK = "proof_compression_submission/THEOREM_TO_TEMPLATE_CROSSWALK.json"
COMPRESSION_RESULT = "proof_compression_submission/PROOF_COMPRESSION_RESULT.json"
VERIFIER = "proof_compression_submission/probe/verify_probe_word_theorem.py"
STATIC_AUDITOR = "proof_compression_submission/adversarial_review/audit_article_sources.py"
BUNDLE_CHECKER = "proof_compression_submission/crosswalk/check_revised_referee_bundle.py"
COMPRESSION_BUILDER = "proof_compression_submission/build_compressed_release.py"
COMPRESSION_VERIFIER = "proof_compression_submission/verify_compressed_release.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def occurrence_count(text: str, needle: str) -> int:
    return len(re.findall(re.escape(needle), text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()

    theorem_path = root / THEOREM
    coverage_path = root / COVERAGE
    theorem_text = theorem_path.read_text(encoding="utf-8")
    theorem_lines = theorem_text.splitlines()

    section = re.search(
        r"Current coverage artifact:\s*\n\s*\n"
        r"- file SHA-256:\s*\n\s*`([0-9a-f]{64})`;\s*\n"
        r"- logical payload:\s*\n\s*`([0-9a-f]{64})`\.",
        theorem_text,
    )
    if section is None:
        raise RuntimeError("current coverage artifact section is absent or malformed")
    printed_file_sha, printed_payload_sha = section.groups()
    section_line = theorem_text[: section.start()].count("\n") + 1
    printed_file_line = next(
        index for index, line in enumerate(theorem_lines, 1)
        if printed_file_sha in line
    )
    printed_payload_line = next(
        index for index, line in enumerate(theorem_lines, 1)
        if printed_payload_sha in line
    )

    coverage = load_object(coverage_path)
    actual_file_sha = sha256_file(coverage_path)
    declared_payload_sha = coverage.get("payload_sha256")
    unsigned_coverage = dict(coverage)
    unsigned_coverage.pop("payload_sha256", None)
    replayed_payload_sha = sha256_bytes(canonical_bytes(unsigned_coverage))
    if declared_payload_sha != replayed_payload_sha:
        raise RuntimeError("coverage certificate payload does not replay")

    crosswalk = load_object(root / CROSSWALK)
    claims = crosswalk.get("claims")
    if not isinstance(claims, list):
        raise RuntimeError("crosswalk claims list absent")
    c09_rows = [
        row for row in claims
        if isinstance(row, dict)
        and row.get("claim_id") == "C09-coherent-probe-word-reconstruction"
    ]
    if len(c09_rows) != 1:
        raise RuntimeError(f"expected one C09 crosswalk row, observed {len(c09_rows)}")
    c09 = c09_rows[0]
    authoritative = c09.get("authoritative_artifacts")
    if not isinstance(authoritative, list):
        raise RuntimeError("C09 authoritative artifact list absent")
    c09_bindings = {
        row.get("path"): row
        for row in authoritative
        if isinstance(row, dict) and row.get("path") in {THEOREM, COVERAGE}
    }
    if set(c09_bindings) != {THEOREM, COVERAGE}:
        raise RuntimeError("C09 does not bind both theorem and coverage")

    manifest = load_object(root / MANIFEST)
    submission_sources = manifest.get("submission_sources")
    if not isinstance(submission_sources, dict):
        raise RuntimeError("submission source manifest absent")
    manifest_files = submission_sources.get("files")
    if not isinstance(manifest_files, dict):
        raise RuntimeError("submission source file map absent")
    manifest_bindings = {path: manifest_files.get(path) for path in (THEOREM, COVERAGE)}

    template = load_object(root / TEMPLATE_CROSSWALK)
    template_rows = template.get("rows")
    if not isinstance(template_rows, list):
        raise RuntimeError("template crosswalk rows absent")
    cbt5_rows = [
        row for row in template_rows
        if isinstance(row, dict) and row.get("theorem_id") == "CBT-5"
    ]
    if len(cbt5_rows) != 1:
        raise RuntimeError(f"expected one CBT-5 row, observed {len(cbt5_rows)}")

    compression = load_object(root / COMPRESSION_RESULT)
    compression_rows: list[dict[str, object]] = []
    stack: list[object] = [compression]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            if value.get("path") in {"probe/PROBE_WORD_THEOREM.md", "probe/PROBE_WORD_COVERAGE.json"}:
                compression_rows.append(value)
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)

    code_checks: dict[str, dict[str, int]] = {}
    for relative in (
        VERIFIER,
        STATIC_AUDITOR,
        BUNDLE_CHECKER,
        COMPRESSION_BUILDER,
        COMPRESSION_VERIFIER,
    ):
        code = (root / relative).read_text(encoding="utf-8")
        code_checks[relative] = {
            "theorem_path_occurrences": occurrence_count(code, "PROBE_WORD_THEOREM.md"),
            "current_section_occurrences": occurrence_count(code, "Current coverage artifact"),
            "printed_file_sha_occurrences": occurrence_count(code, printed_file_sha),
            "printed_payload_sha_occurrences": occurrence_count(code, printed_payload_sha),
        }

    stale_text_occurrences: dict[str, list[dict[str, object]]] = {
        printed_file_sha: [],
        printed_payload_sha: [],
    }
    submission_root = root / "proof_compression_submission"
    text_suffixes = {".bib", ".json", ".md", ".py", ".tex", ".txt"}
    for path in sorted(submission_root.rglob("*")):
        if not path.is_file() or path.suffix not in text_suffixes:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        relative = str(path.relative_to(root))
        for line_number, line in enumerate(lines, 1):
            for stale in stale_text_occurrences:
                if stale in line:
                    stale_text_occurrences[stale].append({
                        "path": relative,
                        "line": line_number,
                    })

    mismatches = []
    if printed_file_sha != actual_file_sha:
        mismatches.append({
            "field": "current coverage file SHA-256",
            "printed": printed_file_sha,
            "actual": actual_file_sha,
            "line": printed_file_line,
        })
    if printed_payload_sha != declared_payload_sha:
        mismatches.append({
            "field": "current coverage logical payload",
            "printed": printed_payload_sha,
            "actual": declared_payload_sha,
            "line": printed_payload_line,
        })

    theorem_sha = sha256_file(theorem_path)
    expected_bindings = {
        THEOREM: theorem_sha,
        COVERAGE: actual_file_sha,
    }
    for path, expected in expected_bindings.items():
        c09_row = c09_bindings[path]
        if c09_row.get("sha256") != expected:
            raise RuntimeError(f"C09 byte binding drift: {path}")
        manifest_row = manifest_bindings[path]
        if not isinstance(manifest_row, dict) or manifest_row.get("sha256") != expected:
            raise RuntimeError(f"submission manifest byte binding drift: {path}")

    result: dict[str, object] = {
        "schema": "k2p-r6-probe-narrative-binding-audit-v1",
        "status": "FAIL" if mismatches else "PASS",
        "finding_id": "R6-M1-PROBE-WORD-NARRATIVE-BINDING",
        "classification": "reproducibility-blocking current-proof narrative contradiction",
        "effect": (
            "The C09 authoritative uniform word theorem identifies a stale coverage "
            "file and stale logical payload as current. Byte manifests bind both the "
            "stale prose and the different current certificate but do not reconcile them."
        ),
        "theorem": {
            "path": THEOREM,
            "bytes": theorem_path.stat().st_size,
            "sha256": theorem_sha,
            "current_section_line": section_line,
            "printed_file_sha256": printed_file_sha,
            "printed_file_sha256_line": printed_file_line,
            "printed_payload_sha256": printed_payload_sha,
            "printed_payload_sha256_line": printed_payload_line,
        },
        "actual_coverage": {
            "path": COVERAGE,
            "bytes": coverage_path.stat().st_size,
            "sha256": actual_file_sha,
            "schema": coverage.get("schema"),
            "status": coverage.get("status"),
            "declared_payload_sha256": declared_payload_sha,
            "replayed_payload_sha256": replayed_payload_sha,
            "payload_replays": declared_payload_sha == replayed_payload_sha,
        },
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "authority_and_current_bindings": {
            "C09_proof_status": c09.get("proof_status"),
            "C09_compression_status": c09.get("compression_status"),
            "C09_artifacts": c09_bindings,
            "revised_submission_manifest": manifest_bindings,
            "CBT_5_row": cbt5_rows[0],
            "compression_result_rows": sorted(
                compression_rows, key=lambda row: str(row.get("path"))
            ),
        },
        "semantic_gate_coverage": {
            "inspected_code": code_checks,
            "stale_hash_text_occurrences_in_submission": stale_text_occurrences,
            "conclusion": (
                "The word verifier regenerates the JSON certificate, while the static "
                "auditor and bundle checker do not parse the theorem's printed current "
                "coverage hashes. The normal checks can therefore PASS this mismatch."
            ),
        },
        "minimal_reproducer": {
            "comparison_1": f"{THEOREM}:{printed_file_line} != sha256({COVERAGE})",
            "comparison_2": f"{THEOREM}:{printed_payload_line} != {COVERAGE}.payload_sha256",
        },
        "smallest_adequate_remedy": [
            "Replace the two printed hashes in the Current coverage artifact section with the current certificate file and payload hashes.",
            "Add a semantic gate and mutations that compare this named current section to the certificate bytes and canonical payload.",
            "Regenerate the compressed result, theorem-artifact crosswalk, revised submission manifest, referee archive/digest, commit, and annotated tag whose byte graph includes the corrected theorem narrative; rerun unchanged package gates as well.",
        ],
    }
    unsigned = dict(result)
    result["payload_sha256"] = sha256_bytes(canonical_bytes(unsigned))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "finding_id": result["finding_id"],
        "mismatch_count": len(mismatches),
        "payload_sha256": result["payload_sha256"],
    }, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
