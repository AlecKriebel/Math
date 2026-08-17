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

    def test_exact_ghr_matrix_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            "            [-zeta_inverse, 0, zeta_inverse, 0],",
            "            [zeta_inverse, 0, zeta_inverse, 0],",
        )

    def test_exact_ghr_block_swap_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            """    ghr = block_diag(
        scalar_mul(ghr_prefactor, ghr_block_a),
        scalar_mul(ghr_prefactor, ghr_block_b),
    )""",
            """    ghr = block_diag(
        scalar_mul(ghr_prefactor, ghr_block_b),
        scalar_mul(ghr_prefactor, ghr_block_a),
    )""",
        )

    def test_exact_ghr_zeta_conjugation_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            "    zeta = CQ23(sqrt2 / 2, sqrt2 / 2)",
            "    zeta = CQ23(sqrt2 / 2, -sqrt2 / 2)",
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

    def test_current_release_records_are_in_the_source_archive(self):
        actual = {relative.as_posix() for _, relative in package_files()}
        self.assertTrue(
            {
                "RELEASE_NOTES_v1.1.3.md",
                "CORRECTION_AUDIT_v1.1.3.md",
            }.issubset(actual)
        )

    def test_current_textual_corrections_are_bound(self):
        manuscript = (ROOT / "main.tex").read_text(encoding="utf-8")
        doi = "10.5281/zenodo.21971507"
        self.assertNotIn("Galindo--Hong--Rowell localization conjecture", manuscript)
        self.assertIn("Rowell--Wang localization conjecture", manuscript)
        self.assertIn(
            r"\cite[Conjecture~3.1, p.~601]{RowellWang2012}", manuscript
        )
        self.assertIn(r"\cite[Conjecture~1.5]{GHR2013}", manuscript)
        self.assertNotIn("multiply relation~(3.1) of", manuscript)
        self.assertIn("multiply the displayed\nprojection-form Hecke relation", manuscript)
        self.assertIn("10.48550/arXiv.2603.20158", manuscript)
        self.assertIn("This realizes the smallest-dimensional", manuscript)
        self.assertNotIn("Corresponding author:", manuscript)
        self.assertNotIn("San Francisco, California", manuscript)
        self.assertIn(
            "\\end{proof}\n\n\\begin{remark}[Conventions in GHR",
            manuscript,
        )
        doi_files = (
            "main.tex",
            "README.md",
            "CITATION.cff",
            "MANIFEST.md",
            "ZENODO_DEPOSIT.md",
            "ARXIV_METADATA.md",
            "SUBMISSION_CHECKLIST.md",
            "RELEASE_NOTES_v1.1.3.md",
            "CORRECTION_AUDIT_v1.1.3.md",
        )
        for name in doi_files:
            with self.subTest(doi_file=name):
                self.assertIn(doi, (ROOT / name).read_text(encoding="utf-8"))
        current_texts = [manuscript]
        website_path = ROOT.parent / "docs/papers/exceptional-ybe-d4/index.html"
        if website_path.exists():
            website = website_path.read_text(encoding="utf-8")
            self.assertIn(doi, website)
            current_texts.append(website)
        for current_text in current_texts:
            normalized = " ".join(current_text.split())
            self.assertNotIn("GPT-5.6 Sol Pro", normalized)
            self.assertIn("GPT-5.6 Sol in Pro mode", normalized)
            self.assertIn("GPT-5.6 Sol in Ultra mode", normalized)

    def test_current_version_metadata_is_consistent(self):
        current_version = "1.1.3"
        current_files = {
            "README.md": f"Submission package version {current_version}",
            "MANIFEST.md": f"submission package version {current_version}",
            "CITATION.cff": f"version: {current_version}",
            "VERIFICATION_ENVIRONMENT.md": f"Version {current_version} was certified",
            "ZENODO_DEPOSIT.md": f"Version: `{current_version}`",
        }
        for name, marker in current_files.items():
            with self.subTest(name=name):
                self.assertIn(marker, (ROOT / name).read_text(encoding="utf-8"))
        self.assertEqual(package_submission.VERSION, current_version)
        epoch = "1786930200"
        self.assertIn(epoch, (ROOT / "build_paper.sh").read_text(encoding="utf-8"))
        self.assertIn(epoch, (ROOT / "VERIFICATION_ENVIRONMENT.md").read_text(encoding="utf-8"))
        website_path = ROOT.parent / "docs/papers/exceptional-ybe-d4/index.html"
        if website_path.exists():
            website = website_path.read_text(encoding="utf-8")
            self.assertIn(f'content="{current_version}"', website)
        workflow_path = ROOT.parent / ".github/workflows/exceptional-ybe-d4.yml"
        if workflow_path.exists():
            self.assertIn(epoch, workflow_path.read_text(encoding="utf-8"))
        self.assertEqual(package_submission.ZIP_TIME, (2026, 8, 16, 18, 30, 0))
        self.assertTrue(
            {
                "exceptional-ybe-d4-v1.1.2.pdf",
                "exceptional-ybe-d4-v1.1.2-source.zip",
                "exceptional-ybe-d4-v1.1.2-arxiv.zip",
            }.issubset(package_submission.DEPRECATED_OUTPUTS)
        )

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
