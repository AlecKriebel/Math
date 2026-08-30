#!/usr/bin/env python3
"""Targeted semantic mutations for the public reproducibility manifest."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import warnings
import zipfile
from pathlib import Path
from typing import Any, Callable

import build_zenodo_reproducibility_package as builder
import verify_zenodo_reproducibility_package as checker


HERE = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = checker.canonical_hash(value)


def current_reader(relative: str) -> bytes:
    return builder.regular_bytes(relative)


def expect_manifest_rejection(
    base: dict[str, Any],
    mutation_id: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_diagnostic: str,
) -> dict[str, str]:
    candidate = copy.deepcopy(base)
    mutate(candidate)
    reseal(candidate)
    data = json.dumps(candidate, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    try:
        checker.validate_manifest_and_reader(data, current_reader)
    except SystemExit as error:
        if str(error) != expected_diagnostic:
            fail(
                f"wrong rejection for {mutation_id}: expected "
                f"{expected_diagnostic!r}, observed {str(error)!r}"
            )
        return {
            "mutation_id": mutation_id,
            "status": "REJECTED",
            "diagnostic": str(error),
        }
    fail(f"mutation survived: {mutation_id}")


def update_file_aggregates(value: dict[str, Any]) -> None:
    files = value["files"]
    counts = {category: 0 for category in ("frozen_evidence", "publication_layer", "packaging_tools")}
    for row in files.values():
        category = row.get("category")
        if category in counts:
            counts[category] += 1
    value["category_counts"] = counts
    value["file_count_excluding_manifest"] = len(files)
    value["total_bytes_excluding_manifest"] = sum(int(row["bytes"]) for row in files.values())
    value["content_ledger_root_sha256"] = checker.canonical_hash(files)


def rejected_row(mutation_id: str, diagnostic: str) -> dict[str, str]:
    return {
        "mutation_id": mutation_id,
        "status": "REJECTED",
        "diagnostic": diagnostic,
    }


def expect_archive_rejection(
    mutation_id: str,
    entries: list[tuple[str, bytes, tuple[int, int, int, int, int, int], int]],
    expected_diagnostic: str,
) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="k2p-zenodo-zip-mutation-") as temporary:
        path = Path(temporary) / "mutant.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for relative, data, timestamp, mode in entries:
                    info = zipfile.ZipInfo(
                        f"{checker.ARCHIVE_ROOT}/{relative}", date_time=timestamp
                    )
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.create_system = 3
                    info.external_attr = mode << 16
                    archive.writestr(info, data)
        try:
            checker.verify_archive(path)
        except SystemExit as error:
            if str(error) != expected_diagnostic:
                fail(
                    f"wrong archive rejection for {mutation_id}: expected "
                    f"{expected_diagnostic!r}, observed {str(error)!r}"
                )
            return rejected_row(mutation_id, str(error))
    fail(f"archive mutation survived: {mutation_id}")


def main() -> None:
    reject_optimized_mode()
    rows = builder.collect_files()
    base = builder.build_manifest(rows)
    checker.validate_manifest_and_reader(builder.manifest_bytes(base), current_reader)
    results: list[dict[str, str]] = []

    def omitted(value: dict[str, Any]) -> None:
        value["files"].pop("LICENSES.md")
        update_file_aggregates(value)

    results.append(
        expect_manifest_rejection(
            base,
            "omitted_required_file",
            omitted,
            "manifest allowlist mismatch; missing=['LICENSES.md'] extra=[]",
        )
    )

    def changed_hash(value: dict[str, Any]) -> None:
        value["files"]["LICENSES.md"]["sha256"] = "0" * 64
        update_file_aggregates(value)

    results.append(
        expect_manifest_rejection(
            base,
            "changed_member_hash",
            changed_hash,
            "manifest byte binding mismatch: LICENSES.md",
        )
    )

    def changed_category(value: dict[str, Any]) -> None:
        value["files"]["LICENSES.md"]["category"] = "publication_layer"
        update_file_aggregates(value)

    results.append(
        expect_manifest_rejection(
            base,
            "changed_category",
            changed_category,
            "malformed manifest file row: LICENSES.md",
        )
    )

    def private_reinsertion(value: dict[str, Any]) -> None:
        relative = "proof_compression_submission/AI_REFEREE_PROMPT.md"
        data = b"synthetic private prompt fixture\n"
        value["files"][relative] = {
            "bytes": len(data),
            "category": "publication_layer",
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        update_file_aggregates(value)

    results.append(
        expect_manifest_rejection(
            base,
            "private_prompt_reinserted",
            private_reinsertion,
            "manifest allowlist mismatch; missing=[] extra=['proof_compression_submission/AI_REFEREE_PROMPT.md']",
        )
    )

    try:
        checker.safe_relative("../outside")
    except SystemExit as error:
        if str(error) != "unsafe archive path: '../outside'":
            fail(f"wrong traversal-path rejection: {error}")
        results.append(rejected_row("unsafe_path", str(error)))
    else:
        fail("unsafe traversal path survived")

    results.append(
        expect_manifest_rejection(
            base,
            "changed_frozen_root",
            lambda value: value["frozen_evidence"].__setitem__(
                "content_ledger_root_sha256", "0" * 64
            ),
            "manifest frozen-evidence authority mismatch",
        )
    )

    def altered_reader(relative: str) -> bytes:
        data = current_reader(relative)
        return data + b"altered" if relative == "LICENSES.md" else data

    try:
        checker.validate_manifest_and_reader(builder.manifest_bytes(base), altered_reader)
    except SystemExit as error:
        results.append(rejected_row("altered_member_bytes", str(error)))
    else:
        fail("altered member bytes survived")

    with tempfile.TemporaryDirectory(
        prefix="k2p-zenodo-root-mutation-", dir=builder.PROJECT.parent
    ) as temporary:
        root = Path(temporary)
        for relative in base["files"]:
            destination = root.joinpath(*Path(relative).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.link(builder.project_path(relative), destination)
        (root / checker.MANIFEST_NAME).write_bytes(builder.manifest_bytes(base))
        (root / "unexpected.txt").write_text("extra\n", encoding="utf-8")
        try:
            checker.verify_root(root)
        except SystemExit as error:
            expected = "extracted-tree allowlist mismatch; missing=[] extra=['unexpected.txt']"
            if str(error) != expected:
                fail(f"wrong extracted-root extra-file rejection: {error}")
            results.append(rejected_row("extracted_root_extra_file", str(error)))
        else:
            fail("extracted-root extra file survived")

    manifest_data = builder.manifest_bytes(base)
    good = checker.ZIP_TIMESTAMP
    mode = checker.ZIP_MODE
    with tempfile.TemporaryDirectory(
        prefix="k2p-zenodo-archive-extra-", dir=builder.PROJECT.parent
    ) as temporary:
        path = Path(temporary) / "mutant.zip"
        builder.write_archive(path, base)
        with zipfile.ZipFile(path, "a", compression=zipfile.ZIP_DEFLATED) as archive:
            relative = "zz_unexpected_private_review_prompt.md"
            info = zipfile.ZipInfo(f"{checker.ARCHIVE_ROOT}/{relative}", date_time=good)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, b"synthetic private prompt fixture\n")
        try:
            checker.verify_archive(path)
        except SystemExit as error:
            expected = "ZIP member count exceeds the 478-member bound"
            if str(error) != expected:
                fail(f"wrong archive extra-member rejection: {error}")
            results.append(rejected_row("archive_extra_member", str(error)))
        else:
            fail("archive extra member survived")
    results.append(
        expect_archive_rejection(
            "archive_wrong_timestamp",
            [(checker.MANIFEST_NAME, manifest_data, (2026, 8, 28, 0, 0, 0), mode)],
            (
                "ZIP timestamp mismatch: "
                "k2p_same_reproducibility_v1.0.5-r1/"
                "ZENODO_REPRODUCIBILITY_MANIFEST.json"
            ),
        )
    )
    results.append(
        expect_archive_rejection(
            "archive_wrong_mode",
            [(checker.MANIFEST_NAME, manifest_data, good, 0o100600)],
            (
                "ZIP member mode mismatch: "
                "k2p_same_reproducibility_v1.0.5-r1/"
                "ZENODO_REPRODUCIBILITY_MANIFEST.json"
            ),
        )
    )
    results.append(
        expect_archive_rejection(
            "archive_duplicate_member",
            [
                (checker.MANIFEST_NAME, manifest_data, good, mode),
                (checker.MANIFEST_NAME, manifest_data, good, mode),
            ],
            "duplicate ZIP member name",
        )
    )
    results.append(
        expect_manifest_rejection(
            base,
            "changed_publication_root",
            lambda value: value["publication_layer"].__setitem__(
                "content_ledger_root_sha256", "0" * 64
            ),
            "manifest publication-layer authority mismatch",
        )
    )
    results.append(
        expect_manifest_rejection(
            base,
            "changed_entrypoint",
            lambda value: value["entrypoints"].__setitem__("full_replay", "true"),
            "manifest entrypoint mismatch",
        )
    )
    results.append(
        expect_manifest_rejection(
            base,
            "changed_probe_binding",
            lambda value: value["accepted_bindings"]["probe_word_theorem"].__setitem__(
                "proof_compression_submission/probe/PROBE_WORD_COVERAGE.json", "0" * 64
            ),
            "manifest accepted bindings mismatch",
        )
    )
    results.append(
        expect_manifest_rejection(
            base,
            "changed_source_tag",
            lambda value: value["source_tags"].__setitem__("manuscript", "unbound"),
            "manifest source-tag mismatch",
        )
    )

    duplicate = b'{"schema":"first","schema":"second"}'
    try:
        checker.strict_json_bytes(duplicate, "duplicate-name mutation")
    except SystemExit as error:
        results.append(
            {
                "mutation_id": "duplicate_json_name",
                "status": "REJECTED",
                "diagnostic": str(error),
            }
        )
    else:
        fail("duplicate JSON name survived")

    try:
        checker.strict_json_bytes(b'{"value":NaN}', "nonfinite mutation")
    except SystemExit as error:
        results.append(
            {
                "mutation_id": "nonfinite_json_number",
                "status": "REJECTED",
                "diagnostic": str(error),
            }
        )
    else:
        fail("non-finite JSON number survived")

    for label, script, arguments in (
        (
            "optimized_builder",
            HERE / "build_zenodo_reproducibility_package.py",
            ["--check"],
        ),
        (
            "optimized_checker",
            HERE / "verify_zenodo_reproducibility_package.py",
            ["--self-test-optimized"],
        ),
    ):
        result = subprocess.run(
            [sys.executable, "-O", "-B", str(script), *arguments],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        diagnostic = (result.stdout + result.stderr).strip()
        if result.returncode != 1 or diagnostic != "optimized Python is forbidden":
            fail(f"optimized-mode mutation survived: {label}")
        results.append(
            {
                "mutation_id": label,
                "status": "REJECTED",
                "diagnostic": diagnostic,
            }
        )

    if len(results) != 20 or any(row["status"] != "REJECTED" for row in results):
        fail("mutation census mismatch")
    print(
        json.dumps(
            {
                "schema": "k2p-zenodo-reproducibility-mutations-v1",
                "status": "PASS",
                "mutation_count": len(results),
                "survivors": 0,
                "mutations": results,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
