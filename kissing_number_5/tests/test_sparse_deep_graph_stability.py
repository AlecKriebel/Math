import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_sparse_deep_graph_stability.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_sparse_deep_graph_stability", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SparseDeepGraphStabilityTests(unittest.TestCase):
    def test_full_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["vertices"], 41)
        self.assertEqual(result["edge_23_type"], "C5+18K2")
        self.assertEqual(result["edge_24_type_count"], 3)
        self.assertEqual(result["countermodel_rank"], 20)
        self.assertEqual(result["row_envelopes_checked"], 41)
        self.assertEqual(result["root_zero_slack_cases_checked"], 3)
        self.assertEqual(result["d5_two_line_deletion_orbits_checked"], 3)
        self.assertTrue(result["hypercube_c5_probe_checked"])
        self.assertTrue(result["aggregate_kernel_psd"])
        self.assertEqual(result["smallest_subset_margin"], "3/28")

    def test_quadratic_field_signs(self):
        root_five = MODULE.Qsqrt5(0, 1)
        self.assertGreater(root_five, 2)
        self.assertGreater(3, root_five)
        self.assertEqual(root_five * root_five, 5)

    def test_graph_arithmetic(self):
        result = MODULE.graph_classification_arithmetic()
        self.assertEqual(result["edge_23_type"], "C5+18K2")
        self.assertEqual(
            set(result["edge_24_types"]),
            {"C7+17K2", "C5_tail2+17K2", "C5+P4+16K2"},
        )

    def test_row_energy_envelopes(self):
        self.assertEqual(MODULE.row_energy_envelope(1), MODULE.Q(3, 4))
        self.assertEqual(MODULE.row_energy_envelope(2), MODULE.Q(49, 64))
        self.assertEqual(MODULE.row_energy_envelope(3), MODULE.Q(9, 8))
        self.assertEqual(MODULE.row_energy_envelope(4), MODULE.Q(5, 4))

    def test_root_slot_shortage(self):
        MODULE.verify_root_system_zero_slack_counts()
        MODULE.verify_d5_two_line_saturation_envelopes()

    def test_hypercube_c5_probe(self):
        import json

        with MODULE.CERTIFICATE.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        MODULE.verify_hypercube_c5_probe(data)


if __name__ == "__main__":
    unittest.main()
