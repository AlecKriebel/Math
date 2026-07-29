#!/usr/bin/env python3
"""Run the exact central verifier suite for the structural-frontier paper.

This runner is deliberately read-only.  It invokes a fixed ordered list of
deterministic exact-arithmetic programs, captures their output, and reports
success exactly when every child process exits with status zero.  It does not
run numerical searches and does not create or update evidence files.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# The order follows the manuscript's logical progression: abstract tower,
# three-strand blocks, low Schmidt rank, unrestricted OSR four, restrictions,
# local primitivity, and the two principal model classes.
VERIFIERS = (
    (
        "tower-multiplicities",
        "scripts/hecke_multiplicity_spectrum.py",
    ),
    (
        "two-projection-blocks",
        "verifiers/verify_two_projection_blocks.py",
    ),
    (
        "controlled-leg-divisibility",
        "verifiers/verify_controlled_leg_divisibility.py",
    ),
    (
        "low-schmidt-obstruction",
        "verifiers/verify_low_schmidt_control_obstruction.py",
    ),
    (
        "osr4-joint-sandwich",
        "verifiers/verify_osr4_joint_sandwich_degeneracy.py",
    ),
    (
        "restrictable-four-strand",
        "verifiers/verify_restrictable_four_strand_obstruction.py",
    ),
    (
        "d6-common-leg-intersection",
        "verifiers/verify_d6_two_block_leg_types.py",
    ),
    (
        "primitive-weyl-bell",
        "verifiers/verify_weyl_bell_diagonal_divisibility.py",
    ),
    (
        "fixed-d4-bell-exhaustion",
        "verifiers/verify_d4_bell_diagonal_exhaustive.py",
    ),
    (
        "four-product-clifford-frame",
        "verifiers/verify_osr4_clifford_frame_parity.py",
    ),
)


def child_environment() -> dict[str, str]:
    """Return a deterministic environment with assertions enabled."""

    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "0"
    environment["LC_ALL"] = "C"
    environment["LANG"] = "C"
    environment["TZ"] = "UTC"
    return environment


def emit_stream(text: str, label: str) -> None:
    """Print a captured child stream without changing its substantive text."""

    if not text:
        return
    print(f"  {label}:")
    for line in text.rstrip("\n").splitlines():
        print(f"    {line}" if line else "")


def main() -> int:
    environment = child_environment()
    failures: list[str] = []

    print("Exceptional YBE structural-frontier exact verifier suite")
    print(f"Programs: {len(VERIFIERS)}")

    for index, (name, relative_path) in enumerate(VERIFIERS, start=1):
        program = PROJECT_ROOT / relative_path
        print(f"[{index:02d}/{len(VERIFIERS):02d}] RUN  {name}")

        if not program.is_file():
            print(f"  FAIL: missing program {relative_path}")
            failures.append(name)
            continue

        completed = subprocess.run(
            [sys.executable, "-B", str(program)],
            cwd=PROJECT_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        emit_stream(completed.stdout, "stdout")
        emit_stream(completed.stderr, "stderr")

        if completed.returncode == 0:
            print(f"[{index:02d}/{len(VERIFIERS):02d}] PASS {name}")
        else:
            print(
                f"[{index:02d}/{len(VERIFIERS):02d}] FAIL {name} "
                f"(exit status {completed.returncode})"
            )
            failures.append(name)

    if failures:
        print(
            "SUITE FAIL: "
            f"{len(failures)} of {len(VERIFIERS)} programs failed: "
            + ", ".join(failures)
        )
        return 1

    print(f"SUITE PASS: {len(VERIFIERS)} of {len(VERIFIERS)} programs passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
