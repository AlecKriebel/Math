#!/usr/bin/env python3
"""Independent focused audit of the shell-three modulo-27 exclusion."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from verify_lp333_order3_char37_transfer import (  # noqa: E402
    CLASSES,
    profile_norm,
)
from verify_lp333_order3_profile9 import (  # noqa: E402
    profile_column_values,
    profile_correlation_table,
)


SOURCE = HERE / "verify_lp333_order3_profile_shell_three_mod27.cpp"
CERTIFICATE = HERE / "shell_three_mod27_certificate.json"

EXPECTED_SOURCE_SHA256 = (
    "a6aac0af88e9ba1045da137ce71815c6a41341c981d9f6af5c757ec63958e091"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "241880b51d5fb24f717d56bceb389043a2abeb4521ceb5a3bcf952d3fc51c56a"
)
EXPECTED_LIMIT_ONE_STDOUT_SHA256 = (
    "4cc77bd847fa1d3840c66c2634d78fe62eb9a7cdfcb269b10d4f35a4f476e3e3"
)

TARGETS = (
    (-3, -3, -4, -2), (-3, -3, -2, 2), (-3, 0, -3, -3),
    (-3, 0, 0, 3), (-1, -2, -5, -1), (-1, -2, -4, 1),
    (0, 3, -4, -2), (0, 3, -2, 2), (1, -1, 2, -2),
    (1, -1, 4, 2), (1, 2, -5, -1), (1, 2, -4, 1),
    (2, -2, -4, -2), (2, -2, -2, 2), (2, 1, 2, -2),
    (2, 1, 4, 2), (3, 0, 0, -3), (3, 0, 3, 3),
    (4, -1, 0, 0), (4, 2, -4, -2), (4, 2, -2, 2),
    (5, 1, 0, 0),
)

EXPECTED_CENSUS = {
    "signed_skeletons": 908_800,
    "canonical_skeletons": 38_296,
    "canonical_skeleton_target_loops": 93_564,
    "support_trials": 17_424_680,
    "extendible_supports": 1_817_356,
    "medium_records": 470_489_796,
    "high_records": 49_068_612,
    "mod9_exact_aggregate_survivors": 479_850,
    "mod27_survivors": 2,
    "cubic37_survivors": 13_004,
    "mod27_cubic37_survivors": 0,
    "exact_replays": 479_850,
    "exact_survivors": 0,
}


def e_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def e_scale(factor: int, value: tuple[int, int]) -> tuple[int, int]:
    return factor * value[0], factor * value[1]


def e_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0] - value[1], -value[1]


def determinant(left: tuple[int, int], right: tuple[int, int]) -> int:
    return left[0] * right[1] - left[1] * right[0]


def class_aggregate(
    channel: int, identifiers: tuple[int, ...]
) -> tuple[int, int]:
    values = profile_column_values(channel, identifiers)
    total = (0, 0)
    for part in CLASSES:
        total = e_add(total, values[part[0]])
    return total


def cubic_j(
    identifiers_a: tuple[int, ...],
    identifiers_b: tuple[int, ...],
    target: tuple[int, int, int, int],
) -> int:
    moments = []
    for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
        values = profile_column_values(channel, identifiers)
        moment = (0, 0)
        for class_index, part in enumerate(CLASSES):
            moment = e_add(
                moment,
                e_scale(pow(8, class_index, 37), values[part[0]]),
            )
        moments.append(moment)
    physical_a = (-1 + 3 * target[0], 3 * target[1])
    physical_b = (2 + 3 * target[2], 3 * target[3])
    return (
        determinant(moments[0], physical_a)
        + determinant(moments[1], physical_b)
    ) % 37


def transform_target(
    target: tuple[int, int, int, int],
    star_a: bool,
    star_b: bool,
) -> tuple[int, int, int, int]:
    result = list(target)
    if star_a:
        result[0], result[1] = target[0] - target[1], -target[1]
    if star_b:
        result[2], result[3] = target[2] - target[3], -target[3]
    return tuple(result)  # type: ignore[return-value]


class ShellThreeMod27Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = json.loads(CERTIFICATE.read_text())

    def test_hashes_and_complete_counts(self) -> None:
        self.assertEqual(
            sha256(SOURCE.read_bytes()).hexdigest(),
            EXPECTED_SOURCE_SHA256,
        )
        self.assertEqual(
            sha256(CERTIFICATE.read_bytes()).hexdigest(),
            EXPECTED_CERTIFICATE_SHA256,
        )
        self.assertEqual(self.certificate["census"], EXPECTED_CENSUS)
        self.assertEqual(self.certificate["source_sha256"], EXPECTED_SOURCE_SHA256)

    def test_target_set_is_closed_under_both_channel_stars(self) -> None:
        target_set = set(TARGETS)
        self.assertEqual(len(target_set), 22)
        for target in TARGETS:
            for star_a in (False, True):
                for star_b in (False, True):
                    self.assertIn(
                        transform_target(target, star_a, star_b),
                        target_set,
                    )
        self.assertEqual(93_564 - 92_968, 596)

    def test_two_mod27_near_witnesses_replay_exactly(self) -> None:
        witnesses = self.certificate["mod27_near_witnesses"]
        self.assertEqual(len(witnesses), 2)
        for witness in witnesses:
            ids_a = tuple(witness["a_ids"])
            ids_b = tuple(witness["b_ids"])
            target = tuple(witness["target"])
            identifiers = ids_a + ids_b
            self.assertEqual(
                sum(profile_norm(profile_id) == 9 for profile_id in identifiers),
                3,
            )
            self.assertEqual(
                sum(profile_norm(profile_id) == 3 for profile_id in identifiers),
                9,
            )
            self.assertEqual(
                sum(profile_norm(profile_id) == 0 for profile_id in identifiers),
                12,
            )
            self.assertEqual(
                class_aggregate(0, ids_a) + class_aggregate(1, ids_b),
                target,
            )

            table = profile_correlation_table(ids_a, ids_b)
            expected = tuple(
                tuple(value) for value in witness["exact_c0_to_c5"]
            )
            self.assertEqual(table[1:7], expected)
            self.assertEqual(
                table[7:13],
                tuple(e_conjugate(value) for value in expected),
            )
            self.assertTrue(
                all(
                    coordinate % 27 == 0
                    for value in table[1:]
                    for coordinate in value
                )
            )
            self.assertTrue(any(value != (0, 0) for value in table[1:]))

            value_j = cubic_j(ids_a, ids_b, target)
            self.assertEqual(value_j, witness["cubic_j_mod37"])
            moment = (0, 0)
            for class_index, value in enumerate(table[1:]):
                moment = e_add(
                    moment,
                    e_scale(3 * pow(8, class_index, 37), value),
                )
            self.assertEqual(
                (moment[0] % 37, moment[1] % 37),
                ((-3 * value_j) % 37, (-6 * value_j) % 37),
            )
            self.assertNotEqual(value_j, 0)

    def test_compiled_one_skeleton_fixture(self) -> None:
        compiler = (
            os.environ.get("CXX")
            or shutil.which("clang++")
            or shutil.which("c++")
        )
        if compiler is None:
            self.skipTest("no C++20 compiler is available")
        with tempfile.TemporaryDirectory(prefix="lp333-shell3-mod27-") as temp:
            executable = Path(temp) / "verify"
            compiled = subprocess.run(
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
                compiled.returncode,
                0,
                compiled.stdout + compiled.stderr,
            )
            self.assertEqual(compiled.stderr, "")
            result = subprocess.run(
                [str(executable), "--limit", "1"],
                check=False,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(
                sha256(result.stdout).hexdigest(),
                EXPECTED_LIMIT_ONE_STDOUT_SHA256,
            )


if __name__ == "__main__":
    unittest.main()
