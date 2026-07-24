from __future__ import annotations

import unittest

from experiments.quadratic_positive_locus.audit_construction_scan import audit


class DiscoveryAuditTest(unittest.TestCase):
    def test_construction_scan_recomputes(self) -> None:
        self.assertTrue(audit()["status"].startswith("PASS"))


if __name__ == "__main__":
    unittest.main()
