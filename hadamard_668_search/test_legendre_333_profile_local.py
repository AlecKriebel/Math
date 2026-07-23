from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from legendre_333 import CRT_INDEX_TABLE
from legendre_333_profile_catalog import (
    EXACT_COMBINED_PAF,
    ROW_SUM_PROFILES,
    canonical_profile,
    combined_paf,
    validate_catalog,
)
from verify_legendre_333_profile_local import verify_profile_checkpoint


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "output" / "legendre_333_profile0_local_60s.json"


class Legendre333ProfileLocalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(FIXTURE.read_text())

    def test_catalog_profiles_are_exact_and_orbit_distinct(self) -> None:
        validate_catalog()
        self.assertEqual(len(ROW_SUM_PROFILES), 21)
        self.assertTrue(
            all(combined_paf(profile) == EXACT_COMBINED_PAF
                for profile in ROW_SUM_PROFILES)
        )
        self.assertEqual(
            len({canonical_profile(*profile) for profile in ROW_SUM_PROFILES}),
            len(ROW_SUM_PROFILES),
        )

    def test_profile_checkpoint_is_strictly_verified_as_nonexact(self) -> None:
        self.assertEqual(
            verify_profile_checkpoint(self.payload),
            {
                "energy_half_paf": 2416,
                "bad_lag_count": 136,
                "max_abs_paf_residual": 16,
                "l1_paf_residual": 1032,
            },
        )

    def test_declared_profile_and_metrics_are_not_trusted(self) -> None:
        wrong_profile = copy.deepcopy(self.payload)
        wrong_profile["profile"] = 1
        with self.assertRaisesRegex(ValueError, "row_sums_a"):
            verify_profile_checkpoint(wrong_profile)

        wrong_column = copy.deepcopy(self.payload)
        wrong_column["column_sums_a"][0] += 2
        with self.assertRaisesRegex(ValueError, "column_sums_a"):
            verify_profile_checkpoint(wrong_column)

        wrong_paf = copy.deepcopy(self.payload)
        wrong_paf["periodic_correlation_sums_1_through_166"][17] += 4
        with self.assertRaisesRegex(ValueError, "periodic correlation"):
            verify_profile_checkpoint(wrong_paf)

        wrong_energy = copy.deepcopy(self.payload)
        wrong_energy["energy_half_paf"] += 1
        with self.assertRaisesRegex(ValueError, "energy_half_paf"):
            verify_profile_checkpoint(wrong_energy)

    def test_emitted_plus_counts_are_strictly_verified(self) -> None:
        for field in (
            "row_plus_counts_a",
            "row_plus_counts_b",
            "column_plus_counts_a",
            "column_plus_counts_b",
        ):
            with self.subTest(field=field, mutation="value"):
                wrong_value = copy.deepcopy(self.payload)
                wrong_value[field][0] += 1
                with self.assertRaisesRegex(ValueError, field):
                    verify_profile_checkpoint(wrong_value)

            with self.subTest(field=field, mutation="boolean"):
                wrong_type = copy.deepcopy(self.payload)
                wrong_type[field][0] = True
                with self.assertRaisesRegex(ValueError, field):
                    verify_profile_checkpoint(wrong_type)

            with self.subTest(field=field, mutation="length"):
                wrong_length = copy.deepcopy(self.payload)
                wrong_length[field].pop()
                with self.assertRaisesRegex(ValueError, field):
                    verify_profile_checkpoint(wrong_length)

    def test_margin_preserving_switch_still_requires_paf_replay(self) -> None:
        switched = copy.deepcopy(self.payload)
        sequence = switched["a"]
        found = False
        for first_row in range(9):
            for second_row in range(first_row + 1, 9):
                for first_column in range(37):
                    for second_column in range(first_column + 1, 37):
                        positions = (
                            CRT_INDEX_TABLE[first_row][first_column],
                            CRT_INDEX_TABLE[first_row][second_column],
                            CRT_INDEX_TABLE[second_row][first_column],
                            CRT_INDEX_TABLE[second_row][second_column],
                        )
                        values = tuple(sequence[index] for index in positions)
                        if values[0] == values[3] and values[1] == values[2] \
                                and values[0] != values[1]:
                            for index in positions:
                                sequence[index] *= -1
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        self.assertTrue(found)
        with self.assertRaisesRegex(ValueError, "periodic correlation"):
            verify_profile_checkpoint(switched)

    def test_schema_exact_firewall_and_strict_integer_types(self) -> None:
        mislabeled = copy.deepcopy(self.payload)
        mislabeled["exact"] = True
        with self.assertRaisesRegex(ValueError, "nonexact near misses"):
            verify_profile_checkpoint(mislabeled)

        boolean_metric = copy.deepcopy(self.payload)
        boolean_metric["energy_half_paf"] = True
        with self.assertRaisesRegex(ValueError, "must be an integer"):
            verify_profile_checkpoint(boolean_metric)


if __name__ == "__main__":
    unittest.main()
