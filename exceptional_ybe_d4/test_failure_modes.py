#!/usr/bin/env python3
"""Negative tests for the scientific verifiers.

These tests ensure that optimization and deliberate witness/algebra mutations
cannot produce a false successful verification run.
"""

import ast
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import package_submission
from package_submission import package_files


ROOT = Path(__file__).resolve().parent
SUPPORTED = ("verify_exact.py", "verify_tensor_words.py", "verify_supplied.py")
OPTIMIZATION_GUARDED = SUPPORTED + ("verify_checksums.py", "package_submission.py")


def run_script(path, *, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.append(str(path))
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class FailureModeTests(unittest.TestCase):
    def test_supported_paths_reject_optimized_python(self):
        for name in OPTIMIZATION_GUARDED:
            with self.subTest(name=name):
                result = run_script(ROOT / name, optimized=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("optimized Python", result.stderr)

    def test_supported_verifiers_have_no_assert_statements(self):
        for name in SUPPORTED:
            with self.subTest(name=name):
                tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
                self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))

    def test_original_attachment_is_preserved_byte_for_byte(self):
        digest = hashlib.sha256((ROOT / "verify_supplied_original.py").read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            "df5ccbc8807c20a2f782762681100e3ad06cb95a750b7e052839584006fe3677",
        )

    def assert_mutation_fails(self, source_name, old, new):
        source = (ROOT / source_name).read_text(encoding="utf-8")
        self.assertEqual(source.count(old), 1, f"mutation anchor changed in {source_name}")
        mutated = source.replace(old, new)
        with tempfile.TemporaryDirectory(prefix="exceptional-ybe-mutation-") as temp_dir:
            path = Path(temp_dir) / source_name
            path.write_text(mutated, encoding="utf-8")
            result = run_script(path)
        self.assertNotEqual(
            result.returncode,
            0,
            f"{source_name} accepted a deliberate mutation:\n{result.stdout}",
        )

    def test_exact_witness_coefficient_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            '("ZIZZ", -INV_SQRT_6),',
            '("ZIZZ", INV_SQRT_6),',
        )

    def test_exact_obstruction_norm_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            "        tl_norm == CQ23(Fraction(1, 18)),",
            "        tl_norm == ZERO,",
        )

    def test_exact_q_conjugation_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            "    q = (ONE + CQ23(0, Q23(0, 0, 1, 0))) / 2",
            "    q = (ONE - CQ23(0, Q23(0, 0, 1, 0))) / 2",
        )

    def test_tensor_multiplication_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_tensor_words.py",
            '("X", "Z"): (1, "J"),',
            '("X", "Z"): (-1, "J"),',
        )

    def test_sympy_witness_coefficient_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_supplied.py",
            "    -kron(Z, I2, Z, Z) / sp.sqrt(6)",
            "    +kron(Z, I2, Z, Z) / sp.sqrt(6)",
        )

    def test_sympy_beta_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_supplied.py",
            "    -kron(X, I2, X, X) / sp.sqrt(3)",
            "    +kron(X, I2, X, X) / sp.sqrt(3)",
        )

    def test_sympy_q_conjugation_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_supplied.py",
            "q = sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2",
            "q = sp.Rational(1, 2) - sp.I * sp.sqrt(3) / 2",
        )

    def test_generic_converse_branches_are_exercised(self):
        result = run_script(ROOT / "verify_tensor_words.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "alpha=0, beta=0, and nondegenerate converse branches are certified",
            result.stdout,
        )

    def test_checksum_verifier_rejects_malformed_unsafe_and_mismatched_entries(self):
        checker = (ROOT / "verify_checksums.py").read_text(encoding="utf-8")
        payload_digest = hashlib.sha256(b"payload\n").hexdigest()
        cases = {
            "malformed": ("not a checksum line\n", "malformed line"),
            "unsafe": (f"{'0' * 64}  ../outside\n", "unsafe path"),
            "noncanonical": (
                f"{payload_digest}  ./payload.txt\n",
                "unsafe path",
            ),
            "mismatch": (f"{'0' * 64}  payload.txt\n", "hash mismatch"),
        }
        for label, (manifest, expected_error) in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix="exceptional-ybe-checksum-"
            ) as temp_dir:
                root = Path(temp_dir)
                (root / "verify_checksums.py").write_text(checker, encoding="utf-8")
                (root / "payload.txt").write_text("payload\n", encoding="utf-8")
                (root / "SHA256SUMS").write_text(manifest, encoding="utf-8")
                result = run_script(root / "verify_checksums.py")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("checksum verification failed", result.stderr)
                self.assertIn(expected_error, result.stderr)

    def test_source_archive_allowlist_is_exactly_the_checksum_manifest(self):
        expected = {"SHA256SUMS"}
        for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            _, name = line.split("  ", 1)
            expected.add(name)
        actual = {relative.as_posix() for _, relative in package_files()}
        self.assertEqual(actual, expected)

    def test_packager_rejects_unexpected_outputs_and_symlink_directory(self):
        with tempfile.TemporaryDirectory(
            prefix="exceptional-ybe-package-boundary-"
        ) as temp_dir:
            root = Path(temp_dir)
            out = root / "submission"
            out.mkdir()
            (out / "unexpected.txt").write_text("do not package\n", encoding="utf-8")
            with (
                mock.patch.object(package_submission, "OUT", out),
                mock.patch.object(package_submission, "verify_package_checksums"),
                self.assertRaisesRegex(RuntimeError, "unexpected files"),
            ):
                package_submission.main()

            out.unlink() if out.is_symlink() else None
            for child in out.iterdir():
                child.unlink()
            out.rmdir()
            target = root / "external"
            target.mkdir()
            out.symlink_to(target, target_is_directory=True)
            with (
                mock.patch.object(package_submission, "OUT", out),
                mock.patch.object(package_submission, "verify_package_checksums"),
                self.assertRaisesRegex(RuntimeError, "must not be a symbolic link"),
            ):
                package_submission.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
