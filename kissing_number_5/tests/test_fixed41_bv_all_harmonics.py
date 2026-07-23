import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = (
    ROOT / "verifiers" / "verify_fixed41_bv_all_harmonics.py"
)
SPEC = importlib.util.spec_from_file_location(
    "verify_fixed41_bv_all_harmonics", VERIFIER_PATH
)
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class Fixed41BVAllHarmonicsTest(unittest.TestCase):
    def test_exact_all_degree_certificate(self) -> None:
        source = (
            ROOT
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        )
        certificate = (
            ROOT
            / "certificates"
            / "fixed41_bv_all_harmonics_certificate.json"
        )
        result = VERIFIER.verify(source, certificate)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["w0_rank"], 7)
        self.assertEqual(result["finite_harmonic_check"], "1..505")
        self.assertEqual(result["analytic_harmonic_tail"], "k>=506")
        self.assertEqual(
            result["conclusion"], "W_k is PSD for every k>=0"
        )
        self.assertEqual(result["pair_moment_finite_check"], "1..114")
        self.assertEqual(result["pair_moment_analytic_tail"], "k>=115")
        self.assertEqual(result["minimum_finite_pair_moment_degree"], 3)

    def test_integer_square_root_bound(self) -> None:
        self.assertEqual(
            VERIFIER.ceil_sqrt_fraction(VERIFIER.Q(49, 16)), 2
        )
        self.assertEqual(
            VERIFIER.ceil_sqrt_fraction(VERIFIER.Q(9, 4)), 2
        )


if __name__ == "__main__":
    unittest.main()
