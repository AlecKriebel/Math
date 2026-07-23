#!/usr/bin/env python3
"""Compile with sanitizers and check small published Turyn cases."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def parse_output(output: str) -> dict[str, str]:
    return dict(
        line.split("=", 1)
        for line in output.splitlines()
        if "=" in line and not line.startswith("nodes_by_depth=")
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="clang++")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).with_name("enumerate_tu.cpp"),
    )
    parser.add_argument(
        "--cubes",
        type=Path,
        default=Path(__file__).with_name("cubes_depth5.txt"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="tu41-regression-") as temporary:
        executable = Path(temporary) / "enumerate_tu_sanitized"
        compile_command = [
            args.compiler,
            "-std=c++17",
            "-O1",
            "-g",
            "-Wall",
            "-Wextra",
            "-pedantic",
            "-fsanitize=address,undefined",
            "-fno-omit-frame-pointer",
            str(args.source.resolve()),
            "-o",
            str(executable),
        ]
        subprocess.run(compile_command, check=True)

        expected = {3: (10, "1"), 7: (10, "1"), 9: (20, "0")}
        for n, (returncode, solutions) in expected.items():
            result = subprocess.run(
                [str(executable), "--n", str(n), "--no-row-sums"],
                check=False,
                capture_output=True,
                text=True,
            )
            parsed = parse_output(result.stdout)
            if result.returncode != returncode:
                raise AssertionError(
                    f"n={n}: return code {result.returncode}, expected {returncode}"
                )
            if parsed.get("complete") != "true" or parsed.get("solutions") != solutions:
                raise AssertionError(f"n={n}: unexpected result {parsed}")
            print(f"PASS n={n}: solutions={solutions}")

        emitted = subprocess.run(
            [
                str(executable),
                "--n",
                "41",
                "--emit-step-depth",
                "5",
                "--bounds-depth",
                "5",
                "--cubes-only",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        committed = args.cubes.read_text(encoding="utf-8")
        if emitted != committed:
            raise AssertionError("sanitized enumerator does not reproduce cube file")
        if len(emitted.splitlines()) != 461:
            raise AssertionError("unexpected cube count")
        print("PASS sanitized TU(41) cube generation: 461 prefixes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
