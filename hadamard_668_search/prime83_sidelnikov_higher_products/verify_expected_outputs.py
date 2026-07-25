#!/usr/bin/env python3
"""Byte-compare the frozen degree-three/four Sidelnikov theorem replays."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


DIRECTORY = Path(__file__).resolve().parent
EXPECTED_PYTHON_SEMANTIC_SHA256 = (
    "272a898b43ace01056aa24a83f490c8ba2d6f25d0ed953d758d5e9a86bf9b0f5"
)


def run(command: list[str]) -> bytes:
    completed = subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        raise AssertionError(
            f"unexpected stderr from {command!r}: "
            f"{completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout


def compare(command: list[str], expected_name: str) -> None:
    observed = run(command)
    expected = (DIRECTORY / expected_name).read_bytes()
    if observed != expected:
        raise AssertionError(
            f"byte mismatch for {command!r} against {expected_name}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--binary",
        required=True,
        help="compiled audit_independent_decimations executable",
    )
    args = parser.parse_args()

    python_output = run(
        ["python3", str(DIRECTORY / "verify_degree3_sidelnikov_fold.py")]
    ).decode()
    semantic_line = (
        f"semantic_sha256={EXPECTED_PYTHON_SEMANTIC_SHA256}\n"
    )
    if semantic_line not in python_output:
        raise AssertionError("Python semantic certificate changed")
    if not python_output.endswith(
        "PASS exact degree-three Sidelnikov prime-fold exclusion\n"
    ):
        raise AssertionError("Python replay did not report PASS")

    compare(
        [args.binary],
        "EXPECTED_INDEPENDENT_DEGREE3.txt",
    )
    compare(
        [args.binary, "--degree4-undecimated"],
        "EXPECTED_UNDECIMATED_DEGREE4.txt",
    )
    print(
        "PASS frozen Python semantic certificate and byte-stable "
        "degree-three/four C++ outputs"
    )


if __name__ == "__main__":
    main()
