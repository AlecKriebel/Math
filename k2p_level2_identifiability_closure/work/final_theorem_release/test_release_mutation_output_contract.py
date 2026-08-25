#!/usr/bin/env python3
"""Focused portability and output-collision regression for the outer suite."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import run_release_mutations as suite
from release_common import PROJECT, ReleaseFailure


RUNNER = Path("work/final_theorem_release/run_release_mutations.py")
LOCKED_COLLISION_TARGETS = (
    RUNNER,
    Path("work/final_theorem_release/release_common.py"),
    Path("work/final_theorem_release/RELEASE_LOCK.json"),
    Path("proof_compression_submission/article/main.tex"),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect_policy_failure(output: Path) -> None:
    try:
        suite.validate_report_output_path(output)
    except ReleaseFailure as error:
        require(
            "FINAL_RELEASE_MUTATION_OUTPUT_POLICY_FAIL" in str(error),
            f"wrong output-policy diagnostic:{error}",
        )
        return
    raise RuntimeError(f"unsafe outer report output accepted:{output}")


def main() -> None:
    if not __debug__:
        raise SystemExit("FINAL_RELEASE_MUTATION_OUTPUT_TEST_OPTIMIZED_MODE_FORBIDDEN")

    marker = b"FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN"
    alpha = subprocess.CompletedProcess(
        ["child"],
        1,
        stdout=b"/tmp/extraction_alpha/trace\n" + marker + b"\n",
        stderr=b"",
    )
    beta = subprocess.CompletedProcess(
        ["child"],
        1,
        stdout=(
            b"/tmp/extraction_beta_with_a_deliberately_different_length/trace\n"
            + marker
            + b"\n"
        ),
        stderr=b"",
    )
    alpha_row = suite.accepted_rejection("portable_rejection", alpha, (marker,))
    beta_row = suite.accepted_rejection("portable_rejection", beta, (marker,))
    require(alpha_row == beta_row, "raw child paths changed the semantic row")
    report_alpha = suite.build_report([alpha_row], [])
    report_beta = suite.build_report([beta_row], [])
    bytes_alpha = (
        json.dumps(report_alpha, indent=2, sort_keys=True) + "\n"
    ).encode()
    bytes_beta = (
        json.dumps(report_beta, indent=2, sort_keys=True) + "\n"
    ).encode()
    require(bytes_alpha == bytes_beta, "two-path outer reports differ")
    require(
        b"elapsed_seconds" not in bytes_alpha
        and b"output_sha256" not in bytes_alpha
        and b"extraction_alpha" not in bytes_alpha,
        "outer report retained unstable runtime or raw-output evidence",
    )

    require(suite.validate_report_output_path(None) is None, "optional output drift")
    for relative in LOCKED_COLLISION_TARGETS:
        expect_policy_failure(PROJECT / relative)

    with tempfile.TemporaryDirectory(
        prefix="k2p-final-mutation-output-contract-"
    ) as directory:
        root = Path(directory)
        external_alpha = root / "extraction_alpha/report.json"
        external_beta = (
            root
            / "extraction_beta_with_a_deliberately_different_length/report.json"
        )
        require(
            suite.validate_report_output_path(external_alpha) == external_alpha.resolve()
            and suite.validate_report_output_path(external_beta)
            == external_beta.resolve(),
            "external caller-owned reports rejected",
        )

        symlink = root / "outside-name-resolving-to-locked-source.json"
        symlink.symlink_to(PROJECT / LOCKED_COLLISION_TARGETS[2])
        expect_policy_failure(symlink)

        for target in (PROJECT / LOCKED_COLLISION_TARGETS[0], symlink):
            locked = target.resolve()
            before = sha(locked)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(PROJECT / RUNNER),
                    "--output",
                    str(target),
                ],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                completed.returncode != 0
                and "FINAL_RELEASE_MUTATION_OUTPUT_POLICY_FAIL" in completed.stdout,
                f"outer CLI accepted source collision:{target}:{completed.stdout}",
            )
            require(sha(locked) == before, f"outer CLI changed locked source:{locked}")

        copied_source = root / "copied-locked-release-source.py"
        shutil.copy2(PROJECT / RUNNER, copied_source)
        copied_hash = sha(copied_source)
        copied_inode = copied_source.stat().st_ino
        hardlink_output = root / "external-hardlink-report.json"
        os.link(copied_source, hardlink_output)
        validated_hardlink = suite.validate_report_output_path(hardlink_output)
        require(validated_hardlink is not None, "external hardlink rejected")
        suite.atomic_write_text(validated_hardlink, bytes_alpha.decode("utf-8"))
        require(
            sha(copied_source) == copied_hash
            and copied_source.stat().st_ino == copied_inode
            and hardlink_output.stat().st_ino != copied_inode
            and hardlink_output.read_bytes() == bytes_alpha,
            "outer atomic writer truncated a hardlinked source",
        )

        late_swap_output = root / "late-symlink-swap-report.json"
        validated_late_output = suite.validate_report_output_path(late_swap_output)
        require(validated_late_output is not None, "late output validation failed")
        late_swap_output.symlink_to(copied_source)
        suite.atomic_write_text(validated_late_output, bytes_alpha.decode("utf-8"))
        require(
            not late_swap_output.is_symlink()
            and late_swap_output.read_bytes() == bytes_alpha
            and sha(copied_source) == copied_hash,
            "outer atomic writer followed a late output symlink",
        )

    print("K2P_FINAL_RELEASE_MUTATION_OUTPUT_CONTRACT_PASS")
    print(
        json.dumps(
            {
                "report_schema": report_alpha["schema"],
                "report_sha256": hashlib.sha256(bytes_alpha).hexdigest(),
                "two_path_reports_identical": True,
                "direct_and_symlink_collisions_rejected": True,
                "source_bytes_unchanged": True,
                "hardlink_and_late_symlink_safe": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
