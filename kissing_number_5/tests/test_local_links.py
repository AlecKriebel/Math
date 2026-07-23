import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_local_links.py"
SPEC = importlib.util.spec_from_file_location("verify_local_links", MODULE_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class LocalLinkVerifierTests(unittest.TestCase):
    def test_s3_polynomial_certificate(self):
        VERIFY.verify_polynomial()

    def test_contact_clique_projection(self):
        VERIFY.verify_contact_clique_projection()

    def test_rational_stereographic_map(self):
        # The full exact witnesses are exercised by main; this smoke test
        # verifies that the map itself lands on the unit sphere without floats.
        from fractions import Fraction as F

        p = VERIFY.stereographic((F(-10, 11), F(-7, 12)))
        self.assertEqual(VERIFY.dot(p, p), 1)

    def test_contact_free_maximal_certificate(self):
        self.assertEqual(VERIFY.verify_contact_free_maximal_code(), 26)

    def test_all_local_certificates(self):
        VERIFY.main()


if __name__ == "__main__":
    unittest.main()
