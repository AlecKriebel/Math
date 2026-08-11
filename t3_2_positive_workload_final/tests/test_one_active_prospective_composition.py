import unittest

import one_active_prospective_composition as prospective


class OneActiveProspectiveCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = prospective.certificate()

    def test_current_remainder_is_reproduced(self):
        self.assertEqual(
            self.payload["current_remainder"],
            {"positive": 1820, "signed": 187},
        )
        self.assertFalse(
            any(
                self.payload["certified_branch_pairwise_overlaps"].values()
            )
        )

    def test_only_current_overlap_is_critical_fifteen(self):
        self.assertEqual(
            self.payload["candidate_current_overlap"],
            {
                "positive": 15,
                "signed": 0,
                "total": 15,
                "branch": "critical_one_active_15",
            },
        )
        nonzero = {
            name: count
            for name, count in self.payload[
                "candidate_overlap_by_certified_branch"
            ].items()
            if count
        }
        self.assertEqual(nonzero, {"critical_one_active_15": 15})

    def test_prospective_arithmetic(self):
        self.assertEqual(
            self.payload["candidate_1227"],
            {"positive": 1076, "signed": 151, "total": 1227},
        )
        self.assertEqual(
            self.payload["prospective_new_contribution"],
            {"positive": 1061, "signed": 151, "total": 1212},
        )
        self.assertEqual(
            self.payload["prospective_after_remainder"],
            {"positive": 759, "signed": 36, "total": 795},
        )

    def test_frozen_fingerprints(self):
        hashes = self.payload["fingerprints"]
        self.assertEqual(
            hashes["candidate_1227"], prospective.EXPECTED_CANDIDATE_SHA256
        )
        self.assertEqual(
            hashes["prospective_new_1212"], prospective.EXPECTED_NEW_SHA256
        )
        self.assertEqual(
            hashes["prospective_after_795"], prospective.EXPECTED_AFTER_SHA256
        )

    def test_pair_composition_is_certified_but_global_stays_false(self):
        self.assertTrue(
            self.payload["prospective_composition_recurrence_certified"]
        )
        self.assertTrue(self.payload["candidate_1227_recurrence_certified"])
        self.assertFalse(self.payload["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
