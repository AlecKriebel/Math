#!/usr/bin/env python3
"""Disposable fail-closed attacks on the outer referee-bundle boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


MANIFEST = Path("proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json")
BUILDER = Path("proof_compression_submission/crosswalk/build_revised_referee_bundle.py")
CHECKER = Path("proof_compression_submission/crosswalk/check_revised_referee_bundle.py")
PDF_REPORT = Path("proof_compression_submission/PDF_BUILD_REPORT.json")
BIB = Path("proof_compression_submission/article/references.bib")
PORTABLE_LEDGER = Path("output/referee/REFEREE_BUNDLE_CONTENTS.json")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(root: Path, python: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(python), "-B", *arguments],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    python = root / ".venv/bin/python"
    originals = {
        relative: (root / relative).read_bytes()
        for relative in (MANIFEST, PDF_REPORT, BIB, PORTABLE_LEDGER)
    }
    results: list[dict[str, object]] = []
    try:
        # A physical alias of a required source must be rejected.
        bib = root / BIB
        backup = root / BIB.with_suffix(".bib.alias-source")
        backup.write_bytes(originals[BIB])
        bib.unlink()
        bib.symlink_to(backup.name)
        alias = run(root, python, str(BUILDER), "--check")
        results.append(
            {
                "case": "physical_source_symlink",
                "exit": alias.returncode,
                "output": alias.stdout.strip(),
                "rejected_for_intended_reason": alias.returncode != 0
                and "non-regular submission source" in alias.stdout,
            }
        )
        bib.unlink()
        bib.write_bytes(originals[BIB])
        backup.unlink()

        # Physical omission of the bibliography must be rejected by the
        # source-set gate (independently of whether TeX emits a PDF).
        bib.unlink()
        missing_bib = run(root, python, str(BUILDER), "--check")
        results.append(
            {
                "case": "missing_bibliography_source",
                "exit": missing_bib.returncode,
                "output": missing_bib.stdout.strip(),
                "rejected_for_intended_reason": missing_bib.returncode != 0
                and "required submission source missing" in missing_bib.stdout
                and str(BIB) in missing_bib.stdout,
            }
        )
        bib.write_bytes(originals[BIB])

        # Physical omission of the portable content ledger must be rejected.
        ledger = root / PORTABLE_LEDGER
        ledger.unlink()
        missing = run(root, python, str(BUILDER), "--check")
        results.append(
            {
                "case": "missing_portable_content_ledger",
                "exit": missing.returncode,
                "output": missing.stdout.strip(),
                "rejected_for_intended_reason": missing.returncode != 0
                and "missing or symbolic supplemental execution dependency" in missing.stdout,
            }
        )
        ledger.write_bytes(originals[PORTABLE_LEDGER])

        # Syntax-invalid manifest must not reach PASS.
        manifest = root / MANIFEST
        manifest.write_bytes(originals[MANIFEST] + b"garbage\n")
        malformed = run(root, python, str(CHECKER), "--manifest", str(manifest))
        results.append(
            {
                "case": "syntax_invalid_manifest",
                "exit": malformed.returncode,
                "output_tail": malformed.stdout[-500:].strip(),
                "rejected_for_intended_reason": malformed.returncode != 0
                and "JSONDecodeError" in malformed.stdout,
            }
        )
        manifest.write_bytes(originals[MANIFEST])

        # Duplicate JSON names are semantically ambiguous. Add a same-valued
        # duplicate to a submission report, reseal through the submitted
        # builder, and see whether both submitted checks still accept it.
        report = root / PDF_REPORT
        text = originals[PDF_REPORT].decode("utf-8")
        assert text.startswith("{\n")
        report.write_text('{\n  "status": "PASS",\n' + text[2:], encoding="utf-8")
        write = run(root, python, str(BUILDER), "--write")
        check = run(root, python, str(BUILDER), "--check")
        independent = run(root, python, str(CHECKER))
        results.append(
            {
                "case": "duplicate_same_value_json_key_in_pdf_report",
                "builder_write_exit": write.returncode,
                "builder_check_exit": check.returncode,
                "independent_checker_exit": independent.returncode,
                "accepted": write.returncode == check.returncode == independent.returncode == 0,
                "builder_check_output": check.stdout.strip(),
                "checker_output": independent.stdout.strip(),
            }
        )
    finally:
        for relative, data in originals.items():
            path = root / relative
            if path.is_symlink():
                path.unlink()
            path.write_bytes(data)
        extra = root / BIB.with_suffix(".bib.alias-source")
        extra.unlink(missing_ok=True)

    restored = {
        str(relative): sha((root / relative).read_bytes()) == sha(data)
        for relative, data in originals.items()
    }
    print(json.dumps({"results": results, "restored": restored}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
