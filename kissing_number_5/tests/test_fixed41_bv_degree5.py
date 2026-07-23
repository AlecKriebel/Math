import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "verifiers" / "verify_fixed41_bv_degree5.py"
SPEC = importlib.util.spec_from_file_location("verify_fixed41_bv_degree5", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class Fixed41BVDegree5Test(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        certificate = (
            ROOT
            / "certificates"
            / "fixed41_bv_degree5_pseudodistribution.json"
        )
        result = VERIFIER.verify(certificate)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["alpha_mass"], "40")
        self.assertEqual(result["nu_mass"], "1560")
        self.assertEqual(result["harmonic_block_sizes"], [6, 5, 4, 3, 2, 1])
        self.assertTrue(
            result["degree_6_obstruction_determinant"].startswith("-")
        )

    def test_transverse_recurrence(self) -> None:
        q2 = VERIFIER.transverse_q(
            2,
            VERIFIER.Fraction(0),
            VERIFIER.Fraction(0),
            VERIFIER.Fraction(1, 2),
        )
        self.assertEqual(q2, 0)

    def test_exact_degree_6_certificate(self) -> None:
        certificate = (
            ROOT
            / "certificates"
            / "fixed41_bv_degree6_pseudodistribution.json"
        )
        result = VERIFIER.verify(certificate)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["bv_total_degree"], 6)
        self.assertEqual(result["two_point_degree"], 30)
        self.assertEqual(
            result["harmonic_block_sizes"], [7, 6, 5, 4, 3, 2, 1]
        )

    def test_exact_full_radial_k8_certificate(self) -> None:
        certificate = (
            ROOT
            / "certificates"
            / "fixed41_bv_fullradial_k8_pseudodistribution.json"
        )
        result = VERIFIER.verify(certificate)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["harmonic_mode"], "full_radial")
        self.assertEqual(result["bv_full_radial_harmonic_degree"], 8)
        self.assertEqual(result["two_point_degree"], 50)
        self.assertEqual(result["harmonic_block_sizes"], [7] + [6] * 8)

    def test_exact_full_radial_k16_certificate(self) -> None:
        certificate = (
            ROOT
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        )
        result = VERIFIER.verify(certificate)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["harmonic_mode"], "full_radial")
        self.assertEqual(result["bv_full_radial_harmonic_degree"], 16)
        self.assertEqual(result["two_point_degree"], 100)
        self.assertEqual(result["harmonic_block_sizes"], [7] + [6] * 16)


if __name__ == "__main__":
    unittest.main()
