#!/usr/bin/env python3
"""Compile-and-replay tests for the two sparse order-three profile sectors."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_lp333_order3_profile_sparse_shells.cpp"

EXPECTED_H6_HASH = (
    "981f1a39c7858271e9588b7606dece1c6d408b31506381c71eecc9dbc85d410e"
)
EXPECTED_H5_HASH = (
    "e917360e36cbf57b96e5f0a8d842017eaeab9a73c4cdff804bdad719d898090e"
)


def parse_output(output: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


class SparseProfileShellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        requested = os.environ.get("CXX")
        compiler = requested or shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            raise unittest.SkipTest("a C++20 compiler is required")
        cls.temporary = tempfile.TemporaryDirectory(
            prefix="h668-sparse-shells-"
        )
        binary = Path(cls.temporary.name) / "verify_sparse_shells"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-Werror",
                str(SOURCE),
                "-o",
                str(binary),
            ],
            check=True,
            cwd=HERE,
            text=True,
            capture_output=True,
            timeout=120,
        )
        completed = subprocess.run(
            [str(binary)],
            check=True,
            cwd=HERE,
            text=True,
            capture_output=True,
            timeout=180,
        )
        cls.output = completed.stdout
        cls.values = parse_output(cls.output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_quartet_sparse_geometry(self) -> None:
        self.assertEqual(self.values["quartet_legal_rows"], "3334")
        self.assertEqual(
            self.values["quartet_medium_count_support"], "0,2,3,4"
        )
        self.assertEqual(self.values["quartet_triple_medium_rows"], "864")

    def test_six_high_sector(self) -> None:
        self.assertEqual(self.values["h6_aggregate_candidates"], "1653840")
        self.assertEqual(self.values["h6_mod9_candidates"], "288")
        self.assertEqual(
            self.values["h6_aggregate_by_target"],
            "(-3,0,-3,-3):413460;(-3,0,0,3):413460;"
            "(3,0,0,-3):413460;(3,0,3,3):413460",
        )
        self.assertEqual(
            self.values["h6_mod9_by_target"],
            "(-3,0,-3,-3):72;(-3,0,0,3):72;"
            "(3,0,0,-3):72;(3,0,3,3):72",
        )
        self.assertEqual(self.values["h6_bad_part_histogram"], "10:24;12:264")
        self.assertEqual(self.values["h6_exact_survivors"], "0")
        self.assertEqual(
            self.values["h6_replay_certificate_sha256"], EXPECTED_H6_HASH
        )

    def test_five_high_sector(self) -> None:
        self.assertEqual(self.values["h5_aggregate_candidates"], "34634136")
        self.assertEqual(self.values["h5_mod9_candidates"], "552")
        self.assertEqual(
            self.values["h5_aggregate_by_target"],
            "(-3,-3,-4,-2):5748834;(-3,-3,-2,2):5748834;"
            "(0,3,-4,-2):5748834;(0,3,-2,2):5748834;"
            "(4,-1,0,0):5819400;(5,1,0,0):5819400",
        )
        self.assertEqual(
            self.values["h5_mod9_by_target"],
            "(-3,-3,-4,-2):42;(-3,-3,-2,2):42;"
            "(0,3,-4,-2):42;(0,3,-2,2):42;"
            "(4,-1,0,0):192;(5,1,0,0):192",
        )
        self.assertEqual(
            self.values["h5_bad_part_histogram"], "6:24;10:144;12:384"
        )
        self.assertEqual(self.values["h5_exact_survivors"], "0")
        self.assertEqual(
            self.values["h5_replay_certificate_sha256"], EXPECTED_H5_HASH
        )

    def test_scope_is_explicit(self) -> None:
        self.assertIn(
            "PASS: exact h=5 and h=6 profile sectors excluded", self.output
        )
        self.assertIn(
            "STATUS: no profile survivor, LP(333), or H(668) asserted",
            self.output,
        )


if __name__ == "__main__":
    unittest.main()
