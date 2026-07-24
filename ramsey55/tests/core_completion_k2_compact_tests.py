#!/usr/bin/env python3
"""Format, tamper, and producer-cap tests for compact k=2 shards."""

from __future__ import annotations

import hashlib
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_k2_compact import (  # noqa: E402
    CompactFormatError,
    HEADER_STRUCT,
    MAGIC,
    RECORD_STRUCT,
    iter_records,
    validate_file,
)


CATALOG = ROOT / "data" / "r55_42some.g6"
SOURCE = ROOT / "src" / "core_completion_k2_compact_screen_solver.cpp"
CATALOG_SHA256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()


def pair_at(offset: int) -> tuple[int, int]:
    cursor = 0
    for left in range(41):
        width = 41 - left
        if offset < cursor + width:
            return left, left + 1 + offset - cursor
        cursor += width
    raise AssertionError


def make_synthetic_shard(
    path: Path,
    *,
    bad_index_at: int | None = None,
    bad_status_at: int | None = None,
) -> None:
    header = HEADER_STRUCT.pack(
        MAGIC,
        64,
        48,
        1,
        1,
        861,
        123,
        40,
        3,
        bytes.fromhex(CATALOG_SHA256),
        b"\0" * 8,
    )
    payload = bytearray(header)
    for index in range(861):
        left, right = pair_at(index)
        status = 7 if index == bad_status_at else 0
        stored_index = index + 1 if index == bad_index_at else index
        payload.extend(
            RECORD_STRUCT.pack(
                1,
                left,
                right,
                status,
                0,
                780,
                390,
                390,
                0,
                0,
                0,
                0,
                390,
                390,
                1,
                0,
                1,
                0,
                1,
                stored_index,
            )
        )
    path.write_bytes(payload)


class CoreCompletionK2CompactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            raise unittest.SkipTest("no C++17 compiler available")
        cls.producer = cls.root / "producer"
        compiled = subprocess.run(
            (
                compiler,
                "-O2",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                str(SOURCE),
                "-o",
                str(cls.producer),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        if compiled.returncode:
            raise AssertionError(compiled.stderr)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_valid_exact_one_line_sequence(self) -> None:
        path = self.root / "valid.k2scrn"
        make_synthetic_shard(path)
        result = validate_file(
            path,
            expected_range=(1, 1),
            expected_catalog_sha256=CATALOG_SHA256,
            node_limit=100_000,
        )
        self.assertEqual(result["record_count"], 861)
        self.assertEqual(result["record_bytes"], 41_392)
        self.assertEqual(result["unsat_count"], 861)
        self.assertEqual(result["limit_count"], 0)
        records = list(iter_records(path))
        self.assertEqual(
            (
                records[-1].catalog_line,
                records[-1].deleted_left,
                records[-1].deleted_right,
                records[-1].record_index,
            ),
            (1, 40, 41, 860),
        )

    def test_bad_record_index_is_rejected(self) -> None:
        path = self.root / "bad-index.k2scrn"
        make_synthetic_shard(path, bad_index_at=17)
        with self.assertRaisesRegex(CompactFormatError, "stored index"):
            list(iter_records(path))

    def test_unknown_status_is_rejected(self) -> None:
        path = self.root / "bad-status.k2scrn"
        make_synthetic_shard(path, bad_status_at=23)
        with self.assertRaisesRegex(CompactFormatError, "invalid status"):
            list(iter_records(path))

    def test_header_width_tamper_is_rejected(self) -> None:
        path = self.root / "bad-header.k2scrn"
        make_synthetic_shard(path)
        raw = bytearray(path.read_bytes())
        struct.pack_into("<H", raw, 10, 49)
        path.write_bytes(raw)
        with self.assertRaisesRegex(CompactFormatError, "unsupported widths"):
            list(iter_records(path))

    def test_producer_rejects_byte_cap_before_creating_output(self) -> None:
        target = self.root / "cap-rejected.k2scrn"
        run = subprocess.run(
            (
                str(self.producer),
                "--graph",
                str(CATALOG),
                "--records",
                str(target),
                "--line-start",
                "1",
                "--line-end",
                "1",
                "--catalog-sha256",
                CATALOG_SHA256,
                "--node-limit",
                "100000",
                "--seconds-limit",
                "0.5",
                "--record-byte-cap",
                "41391",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(run.returncode, 1)
        self.assertIn("exceeds byte cap", run.stderr)
        self.assertFalse(target.exists())
        self.assertFalse(Path(f"{target}.partial").exists())


if __name__ == "__main__":
    unittest.main()
