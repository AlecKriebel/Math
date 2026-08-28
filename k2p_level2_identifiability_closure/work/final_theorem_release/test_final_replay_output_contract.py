#!/usr/bin/env python3
"""Focused fail-closed output regression for the unified replay entry point."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import verify_final_theorem_release as replay
from release_common import PROJECT, ReleaseFailure


RUNNER = PROJECT / "work/final_theorem_release/verify_final_theorem_release.py"
LOCKED_TARGETS = (
    RUNNER,
    PROJECT / "work/final_theorem_release/release_common.py",
    PROJECT / "work/final_theorem_release/RELEASE_LOCK.json",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect_policy_failure(output: Path, allow: bool = False) -> None:
    try:
        replay.validate_report_output_path(output, allow)
    except ReleaseFailure as error:
        require(
            "FINAL_REPLAY_OUTPUT_POLICY_FAIL" in str(error),
            f"wrong output-policy diagnostic:{error}",
        )
        return
    raise RuntimeError(f"unsafe final replay output accepted:{output}")


def main() -> None:
    if not __debug__:
        raise SystemExit("FINAL_REPLAY_OUTPUT_TEST_OPTIMIZED_MODE_FORBIDDEN")
    require(
        replay.validate_report_output_path(None, False) is None,
        "optional output contract drift",
    )
    try:
        replay.validate_report_output_path(None, True)
    except ReleaseFailure as error:
        require(
            "FINAL_REPLAY_OUTPUT_POLICY_FAIL" in str(error),
            f"wrong missing-authoritative-output diagnostic:{error}",
        )
    else:
        raise RuntimeError("authoritative override accepted without --output")
    for target in LOCKED_TARGETS:
        expect_policy_failure(target)
    require(
        replay.validate_report_output_path(replay.AUTHORITATIVE_REPORT, True)
        == replay.AUTHORITATIVE_REPORT.parent.resolve()
        / replay.AUTHORITATIVE_REPORT.name,
        "canonical authoritative override rejected",
    )

    with tempfile.TemporaryDirectory(prefix="k2p-final-replay-output-") as directory:
        root = Path(directory)
        external = root / "external/report.json"
        require(
            replay.validate_report_output_path(external, False) == external.resolve(),
            "external report rejected",
        )
        expect_policy_failure(external, True)
        external.parent.mkdir(parents=True)
        external.write_text('{"status":"PASS","stale":true}\n')
        replay.prepare_report_output(
            replay.validate_report_output_path(external, False)
        )
        require(not external.exists(), "stale external PASS report survived preflight")

        optimized_output = root / "optimized-stale-pass.json"
        optimized_output.write_text('{"status":"PASS","stale":true}\n')
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(RUNNER),
                "--quick",
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
            and "FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN" in optimized.stdout
            and not optimized_output.exists(),
            f"optimized replay retained stale PASS:{optimized.stdout}",
        )

        source_alias = root / "source-alias.json"
        source_alias.symlink_to(LOCKED_TARGETS[2])
        expect_policy_failure(source_alias)

        reverse_target = root / "reverse-symlink-external-target.json"
        reverse_target.write_text('{"outside":true}\n')
        reverse_hash = sha(reverse_target)
        with tempfile.TemporaryDirectory(
            prefix=".k2p-replay-reverse-output-", dir=PROJECT
        ) as source_directory:
            reverse_alias = Path(source_directory) / "inside-source.json"
            reverse_alias.symlink_to(reverse_target)
            expect_policy_failure(reverse_alias)
            reverse_cli = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(RUNNER),
                    "--quick",
                    "--output",
                    str(reverse_alias),
                ],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                reverse_cli.returncode != 0
                and "FINAL_REPLAY_OUTPUT_POLICY_FAIL" in reverse_cli.stdout
                and reverse_alias.is_symlink()
                and sha(reverse_target) == reverse_hash,
                f"replay accepted reverse source symlink:{reverse_cli.stdout}",
            )
        before = sha(LOCKED_TARGETS[2])
        rejected = subprocess.run(
            [
                sys.executable,
                "-B",
                str(RUNNER),
                "--quick",
                "--output",
                str(source_alias),
            ],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            rejected.returncode != 0
            and "FINAL_REPLAY_OUTPUT_POLICY_FAIL" in rejected.stdout
            and sha(LOCKED_TARGETS[2]) == before,
            f"source alias accepted or changed:{rejected.stdout}",
        )

        copied_source = root / "copied-source.py"
        shutil.copy2(RUNNER, copied_source)
        copied_hash = sha(copied_source)
        copied_inode = copied_source.stat().st_ino
        hardlink_output = root / "hardlink-output.json"
        os.link(copied_source, hardlink_output)
        validated_hardlink = replay.validate_report_output_path(
            hardlink_output, False
        )
        require(validated_hardlink is not None, "hardlink output validation failed")
        replay.atomic_write_text(validated_hardlink, "safe-output\n")
        require(
            sha(copied_source) == copied_hash
            and copied_source.stat().st_ino == copied_inode
            and hardlink_output.stat().st_ino != copied_inode,
            "atomic replay writer truncated a hardlinked source",
        )

        late_swap = root / "late-symlink-output.json"
        validated_late = replay.validate_report_output_path(late_swap, False)
        require(validated_late is not None, "late-swap validation failed")
        late_swap.symlink_to(copied_source)
        replay.atomic_write_text(validated_late, "late-safe-output\n")
        require(
            not late_swap.is_symlink()
            and late_swap.read_text() == "late-safe-output\n"
            and sha(copied_source) == copied_hash,
            "atomic replay writer followed a late output symlink",
        )

    print("K2P_FINAL_REPLAY_OUTPUT_CONTRACT_PASS")


if __name__ == "__main__":
    main()
