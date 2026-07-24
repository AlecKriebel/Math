#!/usr/bin/env python3
"""Focused compile/run audit for the shell-four profile exclusion."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from verify_lp333_order3_char37_transfer import (
    pair_signature,
    profile_norm,
    row_sum_targets,
)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_lp333_order3_profile_shell_four.cpp"

EXPECTED_SOURCE_SHA256 = (
    "b76c700e459cbe36318904b9c46ed40302ee50fdbf0eca71a2bbfd362b2d93ab"
)
EXPECTED_STDOUT_SHA256 = (
    "a97dd5e6a5942f0b4e8deca5d2c563258cdc60df9ddf5ddb669bb614e6c5ffa9"
)

EXPECTED_TARGET_COUNTS = (
    15162,
    15162,
    13518,
    13518,
    14970,
    14970,
    15162,
    15162,
    19818,
    19818,
    14970,
    14970,
    15147,
    15147,
    19818,
    19818,
    14358,
    14358,
    14922,
    15147,
    15147,
    14922,
)


def source_targets() -> tuple[tuple[int, int, int, int], ...]:
    """Extract the standalone verifier's literal target catalog."""

    text = SOURCE.read_text(encoding="ascii")
    match = re.search(
        r"constexpr std::array<Target, 22> TARGETS = \{\{(.*?)\}\};",
        text,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("could not locate the C++ target catalog")
    rows = re.findall(
        r"\{\{\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*\}\}",
        match.group(1),
    )
    return tuple(tuple(map(int, row)) for row in rows)


class ShellFourProfileTest(unittest.TestCase):
    def test_local_medium_completeness_and_target_catalog(self) -> None:
        zero_id = 5
        medium_ids = tuple(
            index for index in range(10) if profile_norm(index) == 3
        )
        self.assertEqual(medium_ids, (1, 2, 4, 6, 7, 8))
        histogram: Counter[int] = Counter()
        masks: dict[int, set[int]] = {index: set() for index in range(5)}
        for quartet in product((zero_id, *medium_ids), repeat=4):
            if pair_signature(quartet[0], quartet[1]) != pair_signature(
                quartet[2], quartet[3]
            ):
                continue
            count = sum(value != zero_id for value in quartet)
            histogram[count] += 1
            masks[count].add(
                sum(
                    (value != zero_id) << index
                    for index, value in enumerate(quartet)
                )
            )
        self.assertEqual(
            histogram,
            Counter({0: 1, 2: 108, 3: 216, 4: 486}),
        )
        self.assertEqual(
            tuple(len(masks[index]) for index in range(5)),
            (1, 0, 6, 4, 1),
        )
        support_masks = 20 * 6**3 + 15 * 4**2 + 6 * 5 * 1 * 6
        medium_frames = (
            20 * 108**3 + 15 * 216**2 + 6 * 5 * 486 * 108
        )
        self.assertEqual(support_masks, 4_740)
        self.assertEqual(medium_frames, 27_468_720)
        self.assertEqual(source_targets(), row_sum_targets())

    def test_exhaustive_compiled_verifier(self) -> None:
        source_hash = sha256(SOURCE.read_bytes()).hexdigest()
        self.assertTrue(EXPECTED_SOURCE_SHA256)
        self.assertEqual(source_hash, EXPECTED_SOURCE_SHA256)
        compiler = os.environ.get("CXX")
        if compiler is None:
            compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            self.skipTest("no C++20 compiler is available")
        with tempfile.TemporaryDirectory(
            prefix="lp333-shell-four-"
        ) as temporary:
            executable = Path(temporary) / "verify"
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c++20",
                    "-O3",
                    "-DNDEBUG",
                    "-Wall",
                    "-Wextra",
                    "-pedantic",
                    str(SOURCE),
                    "-o",
                    str(executable),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                compile_result.returncode,
                0,
                compile_result.stdout + compile_result.stderr,
            )
            self.assertEqual(compile_result.stderr, "")
            result = subprocess.run(
                [str(executable)],
                check=False,
                capture_output=True,
                text=True,
                timeout=300,
            )
        self.assertEqual(
            result.returncode,
            0,
            result.stdout + result.stderr,
        )
        self.assertTrue(EXPECTED_STDOUT_SHA256)
        self.assertEqual(
            sha256(result.stdout.encode("ascii")).hexdigest(),
            EXPECTED_STDOUT_SHA256,
        )
        values = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                if value.isdigit():
                    values[key] = int(value)
        self.assertEqual(values["medium_support_masks"], 4_740)
        self.assertEqual(values["medium_frames"], 27_468_720)
        self.assertEqual(values["support_leaves"], 115_033_608)
        self.assertEqual(values["support_empty_gate"], 6_835_368)
        self.assertEqual(values["phase_solutions"], 12_835_512)
        self.assertEqual(values["modulo_nine_survivors"], 345_984)
        self.assertEqual(
            tuple(values[f"target[{index}]"] for index in range(22)),
            EXPECTED_TARGET_COUNTS,
        )
        self.assertEqual(
            {
                bad: values[f"bad_classes[{bad}]"]
                for bad in (4, 6, 8, 10, 12)
            },
            {4: 204, 6: 1_860, 8: 16_884, 10: 96_192, 12: 230_844},
        )
        self.assertEqual(values["exact_profiles"], 0)


if __name__ == "__main__":
    unittest.main()
