#!/usr/bin/env python3
"""Mutation tests for the theorem crosswalk and revised referee manifest."""

from __future__ import annotations

import ast
import copy
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

import build_revised_referee_bundle as builder
import build_theorem_artifact_crosswalk as crosswalk_builder
import check_revised_referee_bundle as checker


HERE = Path(__file__).resolve().parent
REPORT = HERE / "CROSSWALK_BUNDLE_MUTATION_REPORT.json"
MUTATION_COMMAND_TIMEOUT_SECONDS = 300


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


def duplicate_top_level_status(original: bytes, duplicate_value: str) -> bytes:
    if not original.startswith(b"{") or original.count(b'"status": "PASS"') != 1:
        fail("duplicate-name mutation fixture has no unique PASS status")
    inserted = f'\n  "status": {json.dumps(duplicate_value)},'.encode("utf-8")
    return original[:1] + inserted + original[1:]


def reseal_submission_member(
    base: dict[str, Any], relative: str, data: bytes
) -> dict[str, Any]:
    candidate = copy.deepcopy(base)
    files = candidate["submission_sources"]["files"]
    if relative not in files:
        fail(f"duplicate-name fixture is absent from submission ledger: {relative}")
    files[relative] = {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    candidate["submission_sources"]["content_ledger_root_sha256"] = canonical_hash(files)
    candidate["submission_sources"]["total_bytes"] = sum(
        int(row["bytes"]) for row in files.values()
    )
    candidate["combined_content_root_sha256"] = canonical_hash(
        {
            "frozen_evidence": candidate["frozen_evidence"]["files"],
            "submission_sources": files,
        }
    )
    reseal(candidate)
    unsigned = dict(candidate)
    payload = unsigned.pop("payload_sha256", None)
    if payload != canonical_hash(unsigned):
        fail("duplicate-name outer reseal is invalid")
    return candidate


def reseal_frozen_member(
    base: dict[str, Any], relative: str, data: bytes
) -> tuple[dict[str, Any], bytes]:
    candidate = copy.deepcopy(base)
    files = candidate["frozen_evidence"]["files"]
    if relative not in files:
        fail(f"compressed mutation fixture is absent from frozen ledger: {relative}")
    lock_path = builder.project_path(builder.LOCK_RELATIVE)
    lock = json.loads(lock_path.read_bytes())
    if relative not in lock.get("files", {}):
        fail(f"compressed mutation fixture is absent from release lock: {relative}")
    lock["files"][relative] = {
        **lock["files"][relative],
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    reseal(lock)
    lock_data = (
        json.dumps(lock, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    files[relative] = {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    files[builder.LOCK_RELATIVE] = {
        "bytes": len(lock_data),
        "sha256": hashlib.sha256(lock_data).hexdigest(),
    }
    candidate["frozen_evidence"]["release_lock_sha256"] = hashlib.sha256(
        lock_data
    ).hexdigest()
    candidate["frozen_evidence"]["release_lock_payload_sha256"] = lock[
        "payload_sha256"
    ]
    candidate["frozen_evidence"]["content_ledger_root_sha256"] = canonical_hash(files)
    candidate["frozen_evidence"]["total_bytes"] = sum(
        int(row["bytes"]) for row in files.values()
    )
    candidate["combined_content_root_sha256"] = canonical_hash(
        {
            "frozen_evidence": files,
            "submission_sources": candidate["submission_sources"]["files"],
        }
    )
    reseal(candidate)
    unsigned = dict(candidate)
    payload = unsigned.pop("payload_sha256", None)
    if payload != canonical_hash(unsigned):
        fail("compressed outer reseal is invalid")
    return candidate, lock_data


def mutate_first_compressed_jsonl(original: bytes, mode: str) -> bytes:
    lines = gzip.decompress(original).splitlines(keepends=True)
    if not lines or not lines[0].startswith(b"{") or not lines[0].endswith(b"\n"):
        fail("compressed mutation fixture has no canonical first row")
    row = json.loads(lines[0])
    name = "parent_anchor_id"
    if name not in row:
        fail("compressed mutation fixture omits parent_anchor_id")
    if mode == "same":
        value = row[name]
        mutant = (
            b"{"
            + json.dumps(name).encode()
            + b":"
            + json.dumps(value).encode()
            + b","
            + lines[0][1:]
        )
    elif mode == "conflicting":
        mutant = (
            b"{"
            + json.dumps(name).encode()
            + b':"K2P-CONFLICTING-EARLIER-VALUE",'
            + lines[0][1:]
        )
    elif mode == "noncanonical":
        mutant = b"{ " + lines[0][1:]
    else:
        fail(f"unknown compressed mutation mode: {mode}")
    if json.loads(mutant) != row:
        fail(f"compressed mutation changed effective semantics: {mode}")
    lines[0] = mutant
    return gzip.compress(b"".join(lines), compresslevel=6, mtime=0)


def reject_resealed_compressed_jsonl(
    base: dict[str, Any], mutation_id: str, mode: str, diagnostic: str
) -> dict[str, str]:
    relative = "work/probe_coherence_corrected/one_port_ledger.jsonl.gz"
    mutant = mutate_first_compressed_jsonl(builder.project_path(relative).read_bytes(), mode)
    candidate, lock_data = reseal_frozen_member(base, relative, mutant)
    with tempfile.TemporaryDirectory(
        prefix="k2p-crosswalk-compressed-", dir=builder.PROJECT.parent
    ) as temporary:
        root = Path(temporary)
        manifest = hardlink_resealed_project(
            root,
            base,
            candidate,
            relative,
            mutant,
            additional_mutants={builder.LOCK_RELATIVE: lock_data},
        )
        commands = (
            (
                "producer",
                [
                    sys.executable,
                    "-B",
                    str(
                        root
                        / "proof_compression_submission/crosswalk/"
                        "build_revised_referee_bundle.py"
                    ),
                    "--check",
                ],
            ),
            (
                "checker",
                [
                    sys.executable,
                    "-B",
                    str(
                        root
                        / "proof_compression_submission/crosswalk/"
                        "check_revised_referee_bundle.py"
                    ),
                    "--manifest",
                    str(manifest),
                ],
            ),
        )
        rejections: list[str] = []
        for label, command in commands:
            result = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                timeout=MUTATION_COMMAND_TIMEOUT_SECONDS,
                check=False,
            )
            observed = (result.stdout + result.stderr).strip()
            if result.returncode == 0:
                fail(f"compressed mutation survived {label}: {mutation_id}")
            if diagnostic not in observed:
                fail(
                    f"compressed mutation had wrong {label} diagnostic:"
                    f"{mutation_id}:{observed}"
                )
            rejections.append(f"{label}:{observed}")
    return {
        "mutation_id": mutation_id,
        "outer_reseal": "VALID",
        "rejection": ";".join(rejections),
        "status": "REJECTED",
    }


def hardlink_resealed_project(
    root: Path,
    base: dict[str, Any],
    candidate: dict[str, Any],
    mutant_relative: str,
    mutant_data: bytes,
    additional_mutants: dict[str, bytes] | None = None,
) -> Path:
    members = set(base["frozen_evidence"]["files"])
    members.update(base["submission_sources"]["files"])
    members.discard(builder.MANIFEST_RELATIVE)
    for relative in sorted(members):
        source = builder.project_path(relative)
        destination = root.joinpath(*Path(relative).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.link(source, destination)
    mutants = {mutant_relative: mutant_data}
    mutants.update(additional_mutants or {})
    for relative, data in mutants.items():
        mutant = root.joinpath(*Path(relative).parts)
        mutant.unlink()
        mutant.write_bytes(data)
    manifest = root.joinpath(*Path(builder.MANIFEST_RELATIVE).parts)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def reject_resealed_duplicate_name(
    base: dict[str, Any], mutation_id: str, duplicate_value: str
) -> dict[str, str]:
    relative = "proof_compression_submission/PDF_BUILD_REPORT.json"
    original = builder.project_path(relative).read_bytes()
    mutant = duplicate_top_level_status(original, duplicate_value)
    candidate = reseal_submission_member(base, relative, mutant)
    with tempfile.TemporaryDirectory(
        prefix="k2p-crosswalk-duplicate-", dir=builder.PROJECT.parent
    ) as temporary:
        root = Path(temporary)
        manifest = hardlink_resealed_project(
            root, base, candidate, relative, mutant
        )
        commands = (
            (
                "producer",
                [
                    sys.executable,
                    "-B",
                    str(
                        root
                        / "proof_compression_submission/crosswalk/"
                        "build_revised_referee_bundle.py"
                    ),
                    "--check",
                ],
            ),
            (
                "checker",
                [
                    sys.executable,
                    "-B",
                    str(
                        root
                        / "proof_compression_submission/crosswalk/"
                        "check_revised_referee_bundle.py"
                    ),
                    "--manifest",
                    str(manifest),
                ],
            ),
        )
        rejections: list[str] = []
        for label, command in commands:
            result = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                timeout=MUTATION_COMMAND_TIMEOUT_SECONDS,
                check=False,
            )
            diagnostic = (result.stdout + result.stderr).strip()
            if result.returncode == 0:
                fail(f"resealed duplicate-name mutation survived {label}: {mutation_id}")
            if "STRICT_JSON_DUPLICATE_NAME" not in diagnostic:
                fail(
                    f"resealed duplicate-name mutation had wrong {label} rejection: "
                    f"{mutation_id}: {diagnostic}"
                )
            rejections.append(f"{label}:{diagnostic}")
    return {
        "mutation_id": mutation_id,
        "outer_reseal": "VALID",
        "rejection": ";".join(rejections),
        "status": "REJECTED",
    }


def reject_telemetry_binding_mutation(
    mutation_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, str]:
    _, builder_lock_sha, builder_lock_payload = builder.release_context()
    _, checker_lock_sha, checker_lock_payload = checker.release_context()
    if (
        builder_lock_sha != checker_lock_sha
        or builder_lock_payload != checker_lock_payload
    ):
        fail("builder/checker release contexts disagree")
    telemetry = builder.read_json(
        "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    )
    telemetry["submission_sources"] = (
        builder.expected_telemetry_submission_sources()
    )
    telemetry["release_lock"] = builder.expected_telemetry_release_lock(
        builder_lock_sha, builder_lock_payload
    )
    mutate(telemetry)
    rejections: list[str] = []
    for label, validator in (
        ("builder", builder.validate_telemetry_checkout_bindings),
        ("checker", checker.validate_telemetry_checkout_bindings),
        ("crosswalk", crosswalk_builder.validate_telemetry_checkout_bindings),
    ):
        try:
            validator(telemetry, builder_lock_sha, builder_lock_payload)
        except SystemExit as error:
            rejections.append(f"{label}:{error}")
            continue
        fail(f"telemetry mutation survived {label}: {mutation_id}")
    return {
        "mutation_id": mutation_id,
        "rejection": ";".join(rejections),
        "status": "REJECTED",
    }


def reject_c02_scope_mutation(
    mutation_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, str]:
    crosswalk_path = HERE / "THEOREM_ARTIFACT_CROSSWALK.json"
    candidate = json.loads(crosswalk_path.read_text(encoding="utf-8"))
    claims = candidate.get("claims")
    if not isinstance(claims, list):
        fail("crosswalk mutation fixture has no claim list")
    matches = [
        claim
        for claim in claims
        if isinstance(claim, dict)
        and claim.get("claim_id") == "C02-quartet-tree-of-blobs"
    ]
    if len(matches) != 1:
        fail("crosswalk mutation fixture has no unique C02 claim")
    try:
        checker.verify_c02_scope(matches[0])
    except SystemExit as error:
        fail(f"crosswalk mutation fixture fails C02 scope before mutation: {error}")
    mutate(matches[0])
    reseal(candidate)
    try:
        checker.verify_c02_scope(matches[0])
    except SystemExit as error:
        return {
            "mutation_id": mutation_id,
            "rejection": str(error),
            "status": "REJECTED",
        }
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

    def restore_overbroad_c02_claim(value: dict[str, Any]) -> None:
        value["claim"] = (
            "Pointwise quartet signs, labelled tree-of-blobs recovery, and "
            "source-to-target topology direction."
        )

    mutations.append(
        reject_c02_scope_mutation(
            "overbroad_c02_topology_authority", restore_overbroad_c02_claim
        )
    )

    def erase_c02_exclusion_boundary(value: dict[str, Any]) -> None:
        for row in value.get("authoritative_artifacts", []):
            if row.get("path") == (
                "work/adversarial_proof_review/"
                "topology_direction_certificate.json"
            ):
                row["role"] = "direction certificate"
                return
        fail("C02 mutation fixture omits topology direction certificate")

    mutations.append(
        reject_c02_scope_mutation(
            "erased_c02_exclusion_boundary", erase_c02_exclusion_boundary
        )
    )

    def omit_frozen(value: dict[str, Any]) -> None:
        files = value["frozen_evidence"]["files"]
        files.pop(first_key(files))

    mutations.append(reject_mutation(base, "omitted_frozen_evidence_file", omit_frozen))

    for mutation_id, relative in (
        (
            "omitted_quartet_terminal_binding",
            "work/quartet_separation_closure/quartet_terminal_binding_certificate.json",
        ),
        (
            "omitted_canonicalizer_completeness_certificate",
            "work/canonicalizer_completeness/canonicalizer_completeness_certificate.json",
        ),
        (
            "omitted_graph_parameter_transport_ledger",
            "work/canonicalizer_completeness/inheritance_transport/probe_relation_parameter_transports.jsonl.gz",
        ),
        (
            "omitted_shared_strict_json_parser",
            "work/final_theorem_release/strict_json.py",
        ),
        ("omitted_approved_license_terms", "LICENSES.md"),
    ):
        def omit_named_frozen(
            value: dict[str, Any], *, target: str = relative
        ) -> None:
            files = value["frozen_evidence"]["files"]
            if target not in files:
                fail(f"mutation fixture omits required frozen evidence: {target}")
            files.pop(target)

        mutations.append(reject_mutation(base, mutation_id, omit_named_frozen))

    def false_frozen_hash(value: dict[str, Any]) -> None:
        files = value["frozen_evidence"]["files"]
        files[first_key(files)]["sha256"] = "0" * 64

    mutations.append(reject_mutation(base, "false_frozen_evidence_hash", false_frozen_hash))

    def omit_source(value: dict[str, Any]) -> None:
        files = value["submission_sources"]["files"]
        files.pop("proof_compression_submission/article/main.tex", None)

    mutations.append(reject_mutation(base, "omitted_submission_source", omit_source))

    def omit_compression_table(value: dict[str, Any]) -> None:
        files = value["submission_sources"]["files"]
        files.pop(
            "proof_compression_submission/supplement/compression_tables.tex",
            None,
        )

    mutations.append(
        reject_mutation(base, "omitted_compression_table", omit_compression_table)
    )

    def omit_bibliography(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/article/references.bib",
            None,
        )

    mutations.append(
        reject_mutation(base, "omitted_bibliography", omit_bibliography)
    )

    def omit_certificate_appendix(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/supplement/certificate_appendix.tex",
            None,
        )

    mutations.append(
        reject_mutation(base, "omitted_certificate_appendix", omit_certificate_appendix)
    )

    def unsafe_source(value: dict[str, Any]) -> None:
        files = value["submission_sources"]["files"]
        row = files.pop(first_key(files))
        files["../outside"] = row

    mutations.append(reject_mutation(base, "unsafe_source_path", unsafe_source))

    def wrong_status(value: dict[str, Any]) -> None:
        value["status"] = "DRAFT_PC_PARTIAL_PENDING_HUMAN_METADATA"

    mutations.append(reject_mutation(base, "stale_pending_human_status", wrong_status))

    def wrong_email(value: dict[str, Any]) -> None:
        value["submission_metadata"]["corresponding_email"] = "unapproved@example.invalid"

    mutations.append(reject_mutation(base, "unapproved_corresponding_email", wrong_email))

    def false_doi_claim(value: dict[str, Any]) -> None:
        value["submission_metadata"]["doi"] = "10.0000/not-created"

    mutations.append(reject_mutation(base, "false_doi_claim", false_doi_claim))

    def wrong_release_tag(value: dict[str, Any]) -> None:
        value["submission_metadata"]["versioned_annotated_source_tag"] = "mutable-main"

    mutations.append(reject_mutation(base, "wrong_versioned_source_tag", wrong_release_tag))

    def false_release_action(value: dict[str, Any]) -> None:
        value["submission_metadata"]["release_boundary"] = "Zenodo release created."

    mutations.append(reject_mutation(base, "false_external_release_claim", false_release_action))

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

    def false_clean_full_layer_count(value: dict[str, Any]) -> None:
        value["runtime_boundary"]["layer_count"] += 1

    mutations.append(reject_mutation(base, "false_clean_full_layer_count", false_clean_full_layer_count))

    def false_telemetry_source_binding(value: dict[str, Any]) -> None:
        value["submission_sources"][
            "proof_compression_submission/article/main.tex"
        ]["sha256"] = "0" * 64

    mutations.append(
        reject_telemetry_binding_mutation(
            "false_telemetry_submission_source_binding",
            false_telemetry_source_binding,
        )
    )

    def false_telemetry_lock_binding(value: dict[str, Any]) -> None:
        value["release_lock"]["sha256"] = "f" * 64

    mutations.append(
        reject_telemetry_binding_mutation(
            "false_telemetry_release_lock_binding",
            false_telemetry_lock_binding,
        )
    )

    def omit_article_pdf(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf",
            None,
        )

    mutations.append(reject_mutation(base, "omitted_article_pdf", omit_article_pdf))

    def omit_static_article_audit(value: dict[str, Any]) -> None:
        value["submission_sources"]["files"].pop(
            "proof_compression_submission/adversarial_review/STATIC_AUDIT_RESULT.json",
            None,
        )

    mutations.append(
        reject_mutation(base, "omitted_static_article_audit", omit_static_article_audit)
    )

    for mutation_id, relative in (
        (
            "omitted_neutral_referee_prompt",
            "proof_compression_submission/AI_REFEREE_PROMPT.md",
        ),
        (
            "omitted_portable_content_ledger",
            "output/referee/REFEREE_BUNDLE_CONTENTS.json",
        ),
        (
            "omitted_portable_bundle_checker",
            "output/referee/build_referee_bundle.py",
        ),
        (
            "omitted_portable_bundle_readme",
            "output/referee/README.md",
        ),
    ):
        def omit_execution_dependency(
            value: dict[str, Any], *, target: str = relative
        ) -> None:
            files = value["submission_sources"]["files"]
            if target not in files:
                fail(f"mutation fixture omits execution dependency: {target}")
            files.pop(target)

        mutations.append(
            reject_mutation(base, mutation_id, omit_execution_dependency)
        )

    def false_supplement_pdf_hash(value: dict[str, Any]) -> None:
        path = "proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf"
        value["submission_sources"]["files"][path]["sha256"] = "2" * 64

    mutations.append(reject_mutation(base, "false_supplement_pdf_hash", false_supplement_pdf_hash))

    mutations.append(
        reject_resealed_duplicate_name(
            base,
            "same_valued_duplicate_json_name_after_reseal",
            "PASS",
        )
    )
    mutations.append(
        reject_resealed_compressed_jsonl(
            base,
            "same_valued_duplicate_compressed_jsonl_after_reseal",
            "same",
            "STRICT_JSON_DUPLICATE_NAME",
        )
    )
    mutations.append(
        reject_resealed_compressed_jsonl(
            base,
            "conflicting_duplicate_compressed_jsonl_after_reseal",
            "conflicting",
            "STRICT_JSON_DUPLICATE_NAME",
        )
    )
    mutations.append(
        reject_resealed_compressed_jsonl(
            base,
            "noncanonical_compressed_jsonl_after_reseal",
            "noncanonical",
            "STRICT_JSON_NONCANONICAL_BYTES",
        )
    )
    mutations.append(
        reject_resealed_duplicate_name(
            base,
            "conflicting_valued_duplicate_json_name_after_reseal",
            "FAIL",
        )
    )

    crosswalk_scripts = [
        HERE / "build_theorem_artifact_crosswalk.py",
        HERE / "build_revised_referee_bundle.py",
        HERE / "check_revised_referee_bundle.py",
        HERE / "test_crosswalk_bundle_mutations.py",
        HERE.parent / "adversarial_review" / "audit_article_sources.py",
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

    optimized_audit = subprocess.run(
        [
            sys.executable,
            "-O",
            str(HERE.parent / "adversarial_review" / "audit_article_sources.py"),
            "--check",
        ],
        cwd=builder.PROJECT,
        capture_output=True,
        text=True,
        check=False,
    )
    optimized_audit_text = optimized_audit.stdout + optimized_audit.stderr
    if optimized_audit.returncode == 0 or "OPTIMIZED_PYTHON_FORBIDDEN" not in optimized_audit_text:
        fail("optimized-mode article audit mutation was not rejected")

    value: dict[str, Any] = {
        "schema": "k2p-crosswalk-bundle-mutation-report-v2",
        "status": "PASS",
        "assert_statement_count": assert_count,
        "optimized_mode_rejected": True,
        "optimized_article_audit_rejected": True,
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
