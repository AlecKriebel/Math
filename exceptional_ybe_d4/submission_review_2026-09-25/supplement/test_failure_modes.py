#!/usr/bin/env python3
# Online Resource 1 — Algebras and Representation Theory submission.
# A five-word Pauli–Clifford normal form for an exceptional unitary Hecke Yang–Baxter operator
# Alec Kriebel; Independent researcher, San Francisco, USA; me@aleckriebel.com
# ORCID: https://orcid.org/0009-0001-9320-500X
# Curated submission supplement, 25 September 2026. See README.md and LICENSE-CODE.txt.
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


ROOT = Path(__file__).resolve().parent
SUPPORTED = (
    "verify_exact.py",
    "verify_tensor_words.py",
    "verify_supplied.py",
    "verify_concurrent_equivalence.py",
    "verify_braid_link.py",
)
OPTIMIZATION_GUARDED = SUPPORTED + ("verify_checksums.py",)


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
        self.assertIn(
            "AssertionError:",
            result.stderr,
            f"{source_name} failed without an explicit scientific check:\n{result.stderr}",
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

    def test_exact_common_matrix_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_exact.py",
            "            [-zeta_inverse, 0, zeta_inverse, 0],",
            "            [zeta_inverse, 0, zeta_inverse, 0],",
        )

    def test_exact_common_block_swap_mutation_fails(self):
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

    def test_exact_common_zeta_conjugation_mutation_fails(self):
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

    def test_concurrent_unitary_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_concurrent_equivalence.py",
            "[two + SQRT2, -IUNIT * SQRT2, IUNIT * SQRT2, two - SQRT2],",
            "[two + SQRT2, IUNIT * SQRT2, IUNIT * SQRT2, two - SQRT2],",
        )

    def test_concurrent_site_swap_omission_fails(self):
        self.assert_mutation_fails(
            "verify_concurrent_equivalence.py",
            "    opposite = mmul(mmul(sigma, r_gr), sigma)",
            "    opposite = r_gr",
        )

    def test_concurrent_zeta_conjugation_fails(self):
        self.assert_mutation_fails(
            "verify_concurrent_equivalence.py",
            "    zeta = (SQRT3 + IUNIT) / 2",
            "    zeta = (SQRT3 - IUNIT) / 2",
        )

    def test_concurrent_tensor_placement_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_concurrent_equivalence.py",
            "    p_z = kron(I2, Z, Z, I2)",
            "    p_z = kron(Z, I2, I2, Z)",
        )

    def test_concurrent_minus_i_omission_fails(self):
        self.assert_mutation_fails(
            "verify_concurrent_equivalence.py",
            "        equal(intrinsic_sum, smul(-IUNIT * SQRT3, h)),",
            "        equal(intrinsic_sum, smul(SQRT3, h)),",
        )

    def test_braid_link_quarter_turn_order_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            "    quarter_product = pauli_sum_product(quarter_z, quarter_x)",
            "    quarter_product = pauli_sum_product(quarter_x, quarter_z)",
        )

    def test_braid_link_wrong_writhe_factor_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            "    hopf_writhe_factor = scalar_power(kappa, -2)",
            "    hopf_writhe_factor = scalar_power(kappa, 2)",
        )

    def test_braid_link_kappa_replacement_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            "    enhancement_positive = 2 * kappa",
            "    enhancement_positive = 2 * q",
        )

    def test_braid_link_homflypt_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            '    require(q * kappa_inverse * kappa_inverse == -ONE, "HOMFLYPT skein sign")',
            '    require(q * kappa_inverse * kappa_inverse == ONE, "HOMFLYPT skein sign")',
        )

    def test_braid_link_reversal_index_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            "            target = strand_count - 2 - site",
            "            target = site",
        )

    def test_braid_link_garside_word_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            "        for site in range(last - 1, -1, -1)",
            "        for site in range(last - 1, 0, -1)",
        )

    def test_braid_link_standard_frame_witness_sign_mutation_fails(self):
        self.assert_mutation_fails(
            "verify_braid_link.py",
            '        "YIYY": SQRT2 / 4,',
            '        "YIYY": -SQRT2 / 4,',
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
