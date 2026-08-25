#!/usr/bin/env python3
"""Focused output-safety regressions for the composite mutation runner."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from composite_support import ARTIFACTS, HERE, PROJECT, sha_file
from run_composite_mutations import atomic_write_bytes


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise SystemExit(marker)


def invoke(output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(HERE / "run_composite_mutations.py"),
            "--family",
            "raw4",
            "--output",
            str(output),
            *extra,
        ],
        cwd=PROJECT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(
        prefix="k2p-composite-output-safety-"
    ) as directory:
        root = Path(directory)

        hardlink_source = root / "hardlink-source.json"
        hardlink_output = root / "hardlink-output.json"
        hardlink_source.write_bytes(b"locked-source\n")
        os.link(hardlink_source, hardlink_output)
        atomic_write_bytes(hardlink_output, b"new-report\n")
        require(
            hardlink_source.read_bytes() == b"locked-source\n"
            and hardlink_output.read_bytes() == b"new-report\n"
            and not os.path.samefile(hardlink_source, hardlink_output),
            "ATOMIC_HARDLINK_REPLACEMENT_FAIL",
        )

        symlink_source = root / "symlink-source.json"
        symlink_output = root / "symlink-output.json"
        symlink_source.write_bytes(b"locked-symlink-source\n")
        symlink_output.symlink_to(symlink_source)
        atomic_write_bytes(symlink_output, b"new-symlink-report\n")
        require(
            symlink_source.read_bytes() == b"locked-symlink-source\n"
            and symlink_output.read_bytes() == b"new-symlink-report\n"
            and not symlink_output.is_symlink(),
            "ATOMIC_SYMLINK_REPLACEMENT_FAIL",
        )

        canonical = ARTIFACTS / "raw4_corrected_composite_mutations.json"
        canonical_before = sha_file(canonical)
        alias = root / "authoritative-alias.json"
        alias.symlink_to(canonical)
        alias_result = invoke(alias, "--allow-authoritative-output")
        require(
            alias_result.returncode != 0
            and "OUTPUT_MUST_BE_CALLER_OWNED_DISPOSABLE"
            in (alias_result.stdout + alias_result.stderr)
            and sha_file(canonical) == canonical_before,
            "AUTHORITATIVE_SYMLINK_ALIAS_GUARD_FAIL",
        )

        summary = ARTIFACTS / "raw4_corrected_composite_summary.json"
        summary_before = sha_file(summary)
        hardlink_alias = root / "source-hardlink.json"
        os.link(summary, hardlink_alias)
        hardlink_result = invoke(hardlink_alias)
        require(
            hardlink_result.returncode != 0
            and "OUTPUT_HARDLINK_COLLIDES_WITH_SOURCE_INPUT"
            in (hardlink_result.stdout + hardlink_result.stderr)
            and sha_file(summary) == summary_before,
            "SOURCE_HARDLINK_GUARD_FAIL",
        )

        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(HERE / "run_composite_mutations.py"),
                "--family",
                "raw4",
                "--output",
                str(root / "optimized.json"),
            ],
            cwd=PROJECT,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        require(
            optimized.returncode != 0
            and "COMPOSITE_MUTATION_RUNNER_OPTIMIZED_MODE_FORBIDDEN"
            in (optimized.stdout + optimized.stderr),
            "MUTATION_RUNNER_OPTIMIZED_MODE_GUARD_FAIL",
        )

    print(
        "K2P_COMPOSITE_MUTATION_OUTPUT_SAFETY_PASS "
        "atomic_hardlink=1 atomic_symlink=1 authoritative_alias=1 "
        "source_hardlink=1 optimized_mode=1"
    )


if __name__ == "__main__":
    main()
