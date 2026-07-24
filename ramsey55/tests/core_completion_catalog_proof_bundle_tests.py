#!/usr/bin/env python3
"""Tests for replay-safe fixed-core proof bundles."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "r55_42some.g6"
PRODUCER_SOURCE = (
    ROOT / "src" / "core_completion_catalog_proof_bundle_solver.cpp"
)
CHECKER_SOURCE = (
    ROOT / "verify" / "core_completion_catalog_proof_bundle_check.cpp"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CoreCompletionCatalogProofBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            raise unittest.SkipTest("no C++17 compiler available")
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        cls.producer = cls.root / "producer"
        cls.checker = cls.root / "checker"
        for source, output in (
            (PRODUCER_SOURCE, cls.producer),
            (CHECKER_SOURCE, cls.checker),
        ):
            built = subprocess.run(
                (
                    compiler,
                    "-O2",
                    "-std=c++17",
                    "-Wall",
                    "-Wextra",
                    str(source),
                    "-o",
                    str(output),
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            if built.returncode:
                raise AssertionError(built.stderr)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def make_valid_bundle(
        self, name: str
    ) -> tuple[Path, Path, Path, str]:
        case = self.root / name
        case.mkdir()
        pairs = case / "pairs.txt"
        pairs.write_text("1 0\n328 34\n", encoding="ascii")
        bundle = case / "proofs.c2dpb"
        pairs_sha256 = sha256(pairs)
        produced = subprocess.run(
            (
                str(self.producer),
                "--graph",
                str(CATALOG),
                "--pairs",
                str(pairs),
                "--bundle",
                str(bundle),
                "--catalog-sha256",
                sha256(CATALOG),
                "--pairs-sha256",
                pairs_sha256,
                "--node-limit",
                "1000000",
                "--seconds-limit",
                "10",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            produced.returncode, 0, produced.stdout + produced.stderr
        )
        records = [
            json.loads(line)
            for line in produced.stdout.splitlines()
            if line.strip()
        ]
        self.assertEqual(len(records), 3)
        self.assertEqual(
            records[-1]["status"], "UNSAT_BUNDLE_COMPLETE"
        )
        self.assertTrue(bundle.is_file())
        self.assertFalse(Path(str(bundle) + ".partial").exists())
        return case, pairs, bundle, pairs_sha256

    def run_checker(
        self,
        *,
        case: Path,
        pairs: Path,
        bundle: Path,
        pairs_sha256: str,
        transcript_name: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            (
                str(self.checker),
                "--graph",
                str(CATALOG),
                "--pairs",
                str(pairs),
                "--bundle",
                str(bundle),
                "--transcript",
                str(case / transcript_name),
                "--catalog-sha256",
                sha256(CATALOG),
                "--pairs-sha256",
                pairs_sha256,
            ),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_bundle_is_fully_replayed(self) -> None:
        case, pairs, bundle, pairs_sha256 = self.make_valid_bundle("valid")
        transcript = case / "checked.jsonl"
        checked = self.run_checker(
            case=case,
            pairs=pairs,
            bundle=bundle,
            pairs_sha256=pairs_sha256,
            transcript_name=transcript.name,
        )
        self.assertEqual(
            checked.returncode, 0, checked.stdout + checked.stderr
        )
        result = json.loads(checked.stdout)
        self.assertEqual(
            result["status"], "VERIFIED_UNSAT_FIXED_CORE_BUNDLE"
        )
        self.assertEqual(result["pair_count"], 2)
        records = [
            json.loads(line)
            for line in transcript.read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(
            [
                (record["catalog_line"], record["deleted_vertex"])
                for record in records
            ],
            [(1, 0), (328, 34)],
        )
        self.assertTrue(
            all(
                record["status"]
                == "VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_COMPLETION"
                for record in records
            )
        )

    def test_tree_tamper_is_rejected(self) -> None:
        case, pairs, bundle, pairs_sha256 = self.make_valid_bundle("tree")
        tampered = case / "tampered.c2dpb"
        raw = bytearray(bundle.read_bytes())
        raw[-1] ^= 1
        tampered.write_bytes(raw)
        checked = self.run_checker(
            case=case,
            pairs=pairs,
            bundle=tampered,
            pairs_sha256=pairs_sha256,
            transcript_name="tampered.jsonl",
        )
        self.assertNotEqual(checked.returncode, 0)
        self.assertFalse((case / "tampered.jsonl").exists())

    def test_pair_order_tamper_is_rejected(self) -> None:
        case, pairs, bundle, pairs_sha256 = self.make_valid_bundle("pair")
        tampered = case / "wrong-pair.c2dpb"
        raw = bytearray(bundle.read_bytes())
        self.assertEqual(raw[76:80], b"\x01\x00\x00\x00")
        raw[76] = 2
        tampered.write_bytes(raw)
        checked = self.run_checker(
            case=case,
            pairs=pairs,
            bundle=tampered,
            pairs_sha256=pairs_sha256,
            transcript_name="wrong-pair.jsonl",
        )
        self.assertNotEqual(checked.returncode, 0)

    def test_hash_binding_is_enforced(self) -> None:
        case, pairs, bundle, pairs_sha256 = self.make_valid_bundle("hash")
        checked = self.run_checker(
            case=case,
            pairs=pairs,
            bundle=bundle,
            pairs_sha256="0" * 64,
            transcript_name="wrong-hash.jsonl",
        )
        self.assertNotEqual(checked.returncode, 0)

    def test_bundle_byte_limit_stops_before_record_write(self) -> None:
        case = self.root / "byte-limit"
        case.mkdir()
        pairs = case / "pairs.txt"
        pairs.write_text("1 0\n", encoding="ascii")
        bundle = case / "limited.c2dpb"
        produced = subprocess.run(
            (
                str(self.producer),
                "--graph",
                str(CATALOG),
                "--pairs",
                str(pairs),
                "--bundle",
                str(bundle),
                "--catalog-sha256",
                sha256(CATALOG),
                "--pairs-sha256",
                sha256(pairs),
                "--node-limit",
                "1000000",
                "--seconds-limit",
                "10",
                "--bundle-byte-limit",
                "76",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(produced.returncode, 2)
        self.assertFalse(bundle.exists())
        partial = Path(str(bundle) + ".partial")
        self.assertTrue(partial.is_file())
        self.assertEqual(partial.stat().st_size, 76)
        result = json.loads(produced.stdout.splitlines()[-1])
        self.assertEqual(
            result["status"], "ABORTED_BUNDLE_BYTE_LIMIT"
        )


if __name__ == "__main__":
    unittest.main()
