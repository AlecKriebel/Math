#!/usr/bin/env python3
"""Focused regression for the scratch four-high skeleton certificate."""

from __future__ import annotations

from hashlib import sha256
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parent / "verify_lp333_order3_profile_shell_four.cpp"
CENSUS = HERE / "census_h4_skeleton.cpp"
MITM = HERE / "verify_h4_skeleton_mitm.cpp"

EXPECTED_HASHES = {
    PRODUCTION: "b76c700e459cbe36318904b9c46ed40302ee50fdbf0eca71a2bbfd362b2d93ab",
    CENSUS: "5735d18fba619590219654be788c5f5fd7d2832ae0dcf281d0ff833d35a0a918",
    MITM: "734b3de505f313cb565cea77f6cb1ba390753bc8c030a2a9e56a1524336de26c",
}
EXPECTED_STDOUT_HASH = (
    "5b57f2187da536974436c1894fc1171c9e863a92d10cb3cf26770cf5cebdb97b"
)


class H4SkeletonMitmTest(unittest.TestCase):
    def test_pinned_sources_and_complete_replay(self) -> None:
        for path, expected in EXPECTED_HASHES.items():
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), expected)

        compiler = os.environ.get("CXX")
        if compiler is None:
            compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            self.skipTest("no C++20 compiler is available")

        with tempfile.TemporaryDirectory(prefix="h4-skeleton-mitm-") as tmp:
            executable = Path(tmp) / "verify"
            compiled = subprocess.run(
                [
                    compiler,
                    "-std=c++20",
                    "-O3",
                    "-DNDEBUG",
                    "-Wall",
                    "-Wextra",
                    "-pedantic",
                    str(MITM),
                    "-o",
                    str(executable),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                compiled.returncode,
                0,
                compiled.stdout + compiled.stderr,
            )
            self.assertEqual(compiled.stderr, "")
            replay = subprocess.run(
                [str(executable)],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )

        self.assertEqual(
            replay.returncode,
            0,
            replay.stdout + replay.stderr,
        )
        self.assertEqual(
            sha256(replay.stdout.encode("ascii")).hexdigest(),
            EXPECTED_STDOUT_HASH,
        )
        values: dict[str, int] = {}
        for line in replay.stdout.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if value.isdigit():
                values[key] = int(value)
        self.assertEqual(values["signed_skeletons"], 37_680)
        self.assertEqual(values["signed_skeleton_orbits"], 1_704)
        self.assertEqual(values["mod9_assignment_orbits"], 14_443)
        self.assertEqual(values["raw_mod9_survivors"], 345_984)
        self.assertEqual(values["exact_profiles"], 0)
        self.assertEqual(
            {
                bad: values[f"bad_classes[{bad}]"]
                for bad in (4, 6, 8, 10, 12)
            },
            {4: 204, 6: 1_860, 8: 16_884, 10: 96_192, 12: 230_844},
        )


if __name__ == "__main__":
    unittest.main()
