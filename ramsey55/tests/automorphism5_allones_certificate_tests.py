#!/usr/bin/env python3
"""Structural tests for the order-5 all-ones 80-leaf certificate bundle."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "verify")]

import automorphism5_allones_certificate_bundle as producer  # noqa: E402
import automorphism5_allones_certificate_bundle_check as checker  # noqa: E402
from automorphism_orbit_cnf_check import independently_build  # noqa: E402


class Automorphism5AllonesCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.variable_count, parsed = producer.parse_dimacs(
            ROOT
            / "certificates"
            / "order43_automorphism5_eight_cycles.cnf"
        )
        cls.clauses = tuple(tuple(clause) for clause in parsed)
        (
            cls.edge_variable,
            cls.fixed,
            cls.orientations,
        ) = producer.cube_data()

    def test_independent_cover_agrees_and_partitions_all_256_vectors(self) -> None:
        independent = checker.independent_orientations()
        self.assertEqual(self.orientations, independent)
        self.assertEqual(len(independent), 80)
        masks = checker.allones_masks()
        cycle_of_mask = {mask: cycle for cycle, mask in enumerate(masks)}

        def endpoint_swap(bits: tuple[bool, ...]) -> tuple[bool, ...]:
            result = [False] * 8
            for old_cycle, mask in enumerate(masks):
                swapped_mask = (
                    (mask & ~3)
                    | ((mask & 1) << 1)
                    | ((mask & 2) >> 1)
                )
                result[cycle_of_mask[swapped_mask]] = bits[old_cycle]
            return tuple(result)

        covered: set[tuple[bool, ...]] = set()
        for representative in independent:
            swapped = endpoint_swap(representative)
            orbit = {
                representative,
                swapped,
                tuple(not value for value in representative),
                tuple(not value for value in swapped),
            }
            self.assertTrue(covered.isdisjoint(orbit))
            covered.update(orbit)
        self.assertEqual(
            covered, set(itertools.product((False, True), repeat=8))
        )

    def test_independent_fixed_cube_agrees(self) -> None:
        _, orbits, _ = independently_build(5, 8)
        independent_edge_variable = checker.edge_variable_from_orbits(orbits)
        self.assertEqual(
            self.fixed,
            checker.independent_fixed_assumptions(independent_edge_variable),
        )
        self.assertEqual(len(self.fixed), 27)
        self.assertEqual(len(set(map(abs, self.fixed))), 27)

    def test_every_leaf_assigns_43_distinct_variables(self) -> None:
        for orientation in self.orientations:
            internal = producer.split.internal_orientation_assumptions(
                orientation, self.edge_variable
            )
            cube = (*self.fixed, *internal)
            self.assertEqual(len(cube), 43)
            self.assertEqual(len(set(map(abs, cube))), 43)

    def test_residual_fingerprints_match_benchmarked_easy_and_hard_leaves(
        self,
    ) -> None:
        expectations = {
            (False,) * 8: (
                151_115,
                "613d5d6ab5c0d8ab54dba5d1cc4344ea14ed8cf8391fe3fe2ae998a9f753420d",
                5_672_859,
            ),
            (False, False, False, False, True, True, True, False): (
                151_120,
                "90de0e44cc8bdf1c1735670f9f9b47d633a1d498621f7261af2a20580bac69b8",
                5_690_754,
            ),
        }
        for orientation, expected in expectations.items():
            cube = (
                *self.fixed,
                *producer.split.internal_orientation_assumptions(
                    orientation, self.edge_variable
                ),
            )
            residual = producer.residual_clauses(self.clauses, cube)
            digest, byte_count = producer.dimacs_digest(
                self.variable_count, residual
            )
            self.assertEqual((len(residual), digest, byte_count), expected)

    def test_independent_residual_matches_producer(self) -> None:
        _, orbits, independent_base = independently_build(5, 8)
        edge_variable = checker.edge_variable_from_orbits(orbits)
        fixed = checker.independent_fixed_assumptions(edge_variable)
        orientation = checker.independent_orientations()[0]
        cube = (
            *fixed,
            *checker.independent_internal_assumptions(
                orientation, edge_variable
            ),
        )
        expected = checker.residual_clauses(independent_base, cube)
        actual = producer.residual_clauses(self.clauses, cube)
        self.assertEqual(actual, expected)
        self.assertEqual(
            checker.dimacs_digest(183, expected),
            producer.dimacs_digest(183, actual),
        )

    def test_frozen_protocol_has_no_per_leaf_resource_budget(self) -> None:
        self.assertEqual(
            producer.MAXIMUM_TOTAL_ARTIFACT_BYTES, 3_000_000_000
        )
        self.assertEqual(producer.MAXIMUM_TRANSIENT_BYTES, 2_000_000_000)
        self.assertEqual(
            producer.MINIMUM_FREE_BYTES_AFTER_COMPLETION, 2_147_483_648
        )
        required = (
            producer.MAXIMUM_TOTAL_ARTIFACT_BYTES
            + producer.MAXIMUM_TRANSIENT_BYTES
            + producer.MINIMUM_FREE_BYTES_AFTER_COMPLETION
        )
        self.assertEqual(required, 7_147_483_648)


if __name__ == "__main__":
    unittest.main()
