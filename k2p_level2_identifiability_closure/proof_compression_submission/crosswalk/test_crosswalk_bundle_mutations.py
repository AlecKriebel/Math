#!/usr/bin/env python3
"""Mutation tests for the theorem crosswalk and revised referee manifest."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

import build_revised_referee_bundle as builder
import check_revised_referee_bundle as checker


HERE = Path(__file__).resolve().parent
REPORT = HERE / "CROSSWALK_BUNDLE_MUTATION_REPORT.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def canonical_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = canonical_hash(value)


def reject_mutation(
    base: dict[str, Any],
    mutation_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, str]:
    candidate = copy.deepcopy(base)
    mutate(candidate)
    reseal(candidate)
    with tempfile.TemporaryDirectory(prefix="k2p-crosswalk-mutation-") as temporary:
        path = Path(temporary) / "manifest.json"
        path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        try:
            checker.validate(path)
        except SystemExit as error:
            return {"mutation_id": mutation_id, "rejection": str(error), "status": "REJECTED"}
    fail(f"mutation survived: {mutation_id}")


def first_key(value: dict[str, Any]) -> str:
    keys = sorted(value)
    if not keys:
        fail("mutation fixture unexpectedly empty")
    return keys[0]


def count_assert_statements(path: Path) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.Assert))


def run() -> dict[str, Any]:
    reject_optimized_mode()
    base = builder.build_manifest()
    mutations: list[dict[str, str]] = []

    def omit_frozen(value: dict[str, Any]) -> None:
        files = value["frozen_evidence"]["files"]
        files.pop(first_key(files))

    mutations.append(reject_mutation(base, "omitted_frozen_evidence_file", omit_frozen))

    def false_frozen_hash(value: dict[str, Any]) -> None:
        files = value["frozen_evidence"]["files"]
        files[first_key(files)]["sha256"] = "0" * 64

    mutations.append(reject_mutation(base, "false_frozen_evidence_hash", false_frozen_hash))

    def omit_source(value: dict[str, Any]) -> None:
        files = value["submission_sources"]["files"]
        files.pop("proof_compression_submission/article/main.tex", None)

    mutations.append(reject_mutation(base, "omitted_submission_source", omit_source))

    def unsafe_source(value: dict[str, Any]) -> None:
        files = value["submission_sources"]["files"]
        row = files.pop(first_key(files))
        files["../outside"] = row

    mutations.append(reject_mutation(base, "unsafe_source_path", unsafe_source))

    def wrong_status(value: dict[str, Any]) -> None:
        value["status"] = "SUBMISSION_READY"

    mutations.append(reject_mutation(base, "premature_submission_ready_status", wrong_status))

    def missing_pending_metadata(value: dict[str, Any]) -> None:
        value["pending_human_metadata"] = value["pending_human_metadata"][:-1]

    mutations.append(reject_mutation(base, "omitted_pending_metadata", missing_pending_metadata))

    def false_combined_root(value: dict[str, Any]) -> None:
        value["combined_content_root_sha256"] = "f" * 64

    mutations.append(reject_mutation(base, "false_combined_content_root", false_combined_root))

    def false_crosswalk_binding(value: dict[str, Any]) -> None:
        path = "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json"
        value["submission_sources"]["files"][path]["sha256"] = "1" * 64

    mutations.append(reject_mutation(base, "false_crosswalk_binding", false_crosswalk_binding))

    def false_clean_full_runtime(value: dict[str, Any]) -> None:
        value["runtime_boundary"]["end_to_end_full_runtime_seconds"] = 1.0

    mutations.append(reject_mutation(base, "false_clean_full_runtime", false_clean_full_runtime))

    def omit_article_pdf(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
            None,
        )

    mutations.append(reject_mutation(base, "omitted_article_pdf", omit_article_pdf))

    def false_supplement_pdf_hash(value: dict[str, Any]) -> None:
        path = "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf"
        value["submission_sources"]["files"][path]["sha256"] = "2" * 64

    mutations.append(reject_mutation(base, "false_supplement_pdf_hash", false_supplement_pdf_hash))

    crosswalk_scripts = [
        HERE / "build_theorem_artifact_crosswalk.py",
        HERE / "build_revised_referee_bundle.py",
        HERE / "check_revised_referee_bundle.py",
        HERE / "test_crosswalk_bundle_mutations.py",
    ]
    assert_count = sum(count_assert_statements(path) for path in crosswalk_scripts)
    if assert_count != 0:
        fail(f"Python assert statements found in crosswalk package: {assert_count}")

    optimized = subprocess.run(
        [sys.executable, "-O", str(HERE / "check_revised_referee_bundle.py")],
        cwd=builder.PROJECT,
        capture_output=True,
        text=True,
        check=False,
    )
    optimized_text = optimized.stdout + optimized.stderr
    if optimized.returncode == 0 or "optimized Python is forbidden" not in optimized_text:
        fail("optimized-mode checker mutation was not rejected")

    value: dict[str, Any] = {
        "schema": "k2p-crosswalk-bundle-mutation-report-v1",
        "status": "PASS",
        "assert_statement_count": assert_count,
        "optimized_mode_rejected": True,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    value["payload_sha256"] = canonical_hash(value)
    return value


def main() -> None:
    reject_optimized_mode()
    arguments = sys.argv[1:]
    if any(argument not in {"--write", "--check"} for argument in arguments):
        fail("usage: test_crosswalk_bundle_mutations.py [--write|--check]")
    if "--write" in arguments and "--check" in arguments:
        fail("--write and --check are mutually exclusive")
    value = run()
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if "--write" in arguments:
        REPORT.write_text(encoded, encoding="utf-8")
    elif "--check" in arguments:
        if not REPORT.is_file() or REPORT.is_symlink() or REPORT.read_text(encoding="utf-8") != encoded:
            fail("crosswalk bundle mutation report is stale")
    print(json.dumps({"mutation_count": value["mutation_count"], "payload_sha256": value["payload_sha256"], "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
