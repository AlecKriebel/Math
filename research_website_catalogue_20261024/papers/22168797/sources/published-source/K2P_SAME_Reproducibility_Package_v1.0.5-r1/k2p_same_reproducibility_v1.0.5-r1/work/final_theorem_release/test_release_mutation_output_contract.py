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


def expect_qualification_failure(
    result: subprocess.CompletedProcess[bytes], diagnostic: str
) -> None:
    try:
        suite.accepted_rejection("negative_control", result, diagnostic)
    except ReleaseFailure:
        return
    raise RuntimeError(f"outer qualifier accepted invalid rejection:{result}")


def main() -> None:
    if not __debug__:
        raise SystemExit("FINAL_RELEASE_MUTATION_OUTPUT_TEST_OPTIMIZED_MODE_FORBIDDEN")

    diagnostic = "FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN"
    marker = diagnostic.encode()
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
    alpha_row = suite.accepted_rejection("portable_rejection", alpha, diagnostic)
    beta_row = suite.accepted_rejection("portable_rejection", beta, diagnostic)
    require(alpha_row == beta_row, "raw child paths changed the semantic row")
    try:
        suite.build_report([alpha_row], [])
    except ReleaseFailure as error:
        require(
            "FINAL_MUTATION_CENSUS_FAIL" in str(error),
            f"wrong report-census diagnostic:{error}",
        )
    else:
        raise RuntimeError("outer report builder accepted an incomplete census")
    rows_alpha = [
        {**alpha_row, "name": f"portable_rejection_{index}"}
        for index in range(suite.REQUIRED_MUTATION_COUNT)
    ]
    rows_beta = [
        {**beta_row, "name": f"portable_rejection_{index}"}
        for index in range(suite.REQUIRED_MUTATION_COUNT)
    ]
    report_alpha = suite.build_report(rows_alpha, [])
    report_beta = suite.build_report(rows_beta, [])
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
    for attack in (
        subprocess.CompletedProcess(["child"], 2, stdout=marker, stderr=b""),
        subprocess.CompletedProcess(["child"], -9, stdout=marker, stderr=b""),
        subprocess.CompletedProcess(
            ["child"],
            1,
            stdout=b"Traceback (most recent call last):\nRuntimeError: " + marker,
            stderr=b"",
        ),
        subprocess.CompletedProcess(
            ["child"], 1, stdout=b"UNRELATED_FAILURE_CODE\n", stderr=b""
        ),
        subprocess.CompletedProcess(
            ["child"],
            1,
            stdout=marker + b"\nK2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS\n",
            stderr=b"",
        ),
    ):
        expect_qualification_failure(attack, diagnostic)

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
        external_alpha.parent.mkdir(parents=True, exist_ok=True)
        external_alpha.write_text('{"status":"PASS","stale":true}\n')
        suite.prepare_report_output(
            suite.validate_report_output_path(external_alpha)
        )
        require(
            not external_alpha.exists(),
            "failed outer preflight could retain stale PASS bytes",
        )

        optimized_output = root / "optimized-stale-pass.json"
        optimized_output.write_text('{"status":"PASS","stale":true}\n')
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(PROJECT / RUNNER),
                "--output",
                str(optimized_output),
            ],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            optimized.returncode != 0
            and "FINAL_RELEASE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN"
            in optimized.stdout
            and not optimized_output.exists(),
            f"optimized outer run retained stale PASS:{optimized.stdout}",
        )

        symlink = root / "outside-name-resolving-to-locked-source.json"
        symlink.symlink_to(PROJECT / LOCKED_COLLISION_TARGETS[2])
        expect_policy_failure(symlink)

        reverse_target = root / "reverse-symlink-external-target.json"
        reverse_target.write_text('{"outside":true}\n')
        reverse_hash = sha(reverse_target)
        with tempfile.TemporaryDirectory(
            prefix=".k2p-release-reverse-output-", dir=PROJECT
        ) as source_directory:
            reverse_symlink = Path(source_directory) / "inside-source.json"
            reverse_symlink.symlink_to(reverse_target)
            expect_policy_failure(reverse_symlink)
            reverse_cli = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(PROJECT / RUNNER),
                    "--output",
                    str(reverse_symlink),
                ],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                reverse_cli.returncode != 0
                and "FINAL_RELEASE_MUTATION_OUTPUT_POLICY_FAIL" in reverse_cli.stdout
                and reverse_symlink.is_symlink()
                and sha(reverse_target) == reverse_hash,
                f"outer CLI accepted reverse source symlink:{reverse_cli.stdout}",
            )

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
                "both_symlink_directions_rejected": True,
                "source_bytes_unchanged": True,
                "hardlink_and_late_symlink_safe": True,
                "stale_report_removed_before_preflight": True,
                "optimized_rejection_removes_stale_report": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
