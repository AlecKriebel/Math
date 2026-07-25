import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree11.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_one_sided_cap_degree11", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OneSidedCapDegree11Tests(unittest.TestCase):
    def test_exact_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["dual_objective"], MODULE.Q(11303, 323))
        self.assertLess(result["dual_objective"], 35)
        self.assertEqual(result["one_sided_kissing_upper_bound"], 34)
        self.assertEqual(result["domain_bernstein_leaves"], 5995)
        self.assertEqual(result["maximum_leaf_depth"], 31)

    def _assert_tamper_rejected(self, mutate):
        certificate = json.loads(MODULE.CERTIFICATE_PATH.read_text())
        mutate(certificate)
        previous_path = MODULE.CERTIFICATE_PATH
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(certificate))
            MODULE.CERTIFICATE_PATH = path
            try:
                with self.assertRaises(AssertionError):
                    MODULE.verify()
            finally:
                MODULE.CERTIFICATE_PATH = previous_path

    def test_factor_tamper_is_rejected_before_domain_audit(self):
        def mutate(certificate):
            certificate["blocks"][0]["factor_integer_columns"][0][0] += 1

        self._assert_tamper_rejected(mutate)

    def test_tree_manifest_tamper_is_rejected_before_domain_audit(self):
        def mutate(certificate):
            certificate["bernstein_tree_manifest"][
                "leaf_digest_sha256"
            ] = "0" * 64

        self._assert_tamper_rejected(mutate)


if __name__ == "__main__":
    unittest.main()
