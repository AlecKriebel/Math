from fractions import Fraction as Q
import unittest

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility


class StoichiometricFlagCriterionTests(unittest.TestCase):
    def test_same_order_codivergence_and_constant_coordinate(self) -> None:
        codivergence_space = (
            (Q(1), Q(1), Q(0)),
            (Q(1), Q(0), Q(1)),
        )
        succeeds = feasibility.subspace_weight_certificate(
            codivergence_space, (2, 2, 1)
        )
        fails = feasibility.subspace_weight_certificate(
            codivergence_space, (2, 1, 1)
        )
        self.assertTrue(succeeds.feasible)
        self.assertFalse(fails.feasible)
        witness = next(level.invariant for level in fails.levels if not level.feasible)
        self.assertIsNotNone(witness)
        self.assertEqual(sum(witness[index] * codivergence_space[0][index] for index in range(3)), 0)
        self.assertEqual(sum(witness[index] * codivergence_space[1][index] for index in range(3)), 0)

        constant_a_space = (
            (Q(0), Q(1), Q(0)),
            (Q(0), Q(0), Q(1)),
        )
        constant_fails = feasibility.subspace_weight_certificate(
            constant_a_space, (1, 0, 0)
        )
        self.assertFalse(constant_fails.feasible)
        self.assertEqual(constant_fails.levels[0].invariant, (Q(1), Q(0), Q(0)))

    def test_fixed_class_cap_condition(self) -> None:
        pair = (
            closure.mask(("0", "B")),
            closure.mask(("C", "2C")),
        )
        descriptor = tier._descriptor_with_key(((0, 1, 0), (0, 2, 0)))
        self.assertTrue(feasibility.descriptor_feasible(pair, descriptor))
        self.assertTrue(
            feasibility.fixed_class_descriptor_feasible(
                pair, descriptor, (0, 0, 0)
            )
        )
        self.assertFalse(
            feasibility.fixed_class_descriptor_feasible(
                pair, descriptor, (1, 0, 0)
            )
        )

    def test_every_level_certificate_is_exact(self) -> None:
        positive = tier.tier_split(closure.POSITIVE_SHIELDED_MASKS)[1]
        signed = tier.tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
        for pair in positive | signed:
            space = feasibility.stoichiometric_basis(pair)
            invariants = feasibility.invariant_basis(pair)
            for descriptor in tier.tier_descriptors():
                if tier.universal_orientation_tier_condition(pair, descriptor):
                    continue
                certificate = feasibility.pair_weight_certificate(
                    pair, descriptor.weight
                )
                for level in certificate.levels:
                    lower = tuple(
                        index
                        for index, value in enumerate(descriptor.weight)
                        if value < level.level
                    )
                    if level.feasible:
                        self.assertIsNotNone(level.direction)
                        direction = level.direction
                        for invariant in invariants:
                            self.assertEqual(
                                sum(
                                    invariant[index] * direction[index]
                                    for index in range(3)
                                ),
                                0,
                            )
                        for index in lower:
                            self.assertEqual(direction[index], 0)
                        for index in level.equal_coordinates:
                            self.assertGreater(direction[index], 0)
                    else:
                        self.assertIsNotNone(level.invariant)
                        invariant = level.invariant
                        for vector in space:
                            self.assertEqual(
                                sum(
                                    invariant[index] * vector[index]
                                    for index in range(3)
                                ),
                                0,
                            )
                        for index in level.higher_coordinates:
                            self.assertEqual(invariant[index], 0)
                        self.assertTrue(
                            any(
                                invariant[index] > 0
                                for index in level.equal_coordinates
                            )
                        )
                        for index in level.equal_coordinates:
                            self.assertGreaterEqual(invariant[index], 0)


class StoichiometricGateEnumerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = feasibility.certificate()

    def test_complete_residual_split(self) -> None:
        self.assertEqual(self.result["input_residual_pairs"], 2511)
        self.assertEqual(self.result["input_positive_pairs"], 2312)
        self.assertEqual(self.result["input_signed_pairs"], 199)
        self.assertEqual(
            self.result["failing_pair_descriptor_incidences"], 12886
        )
        self.assertEqual(
            self.result["stoichiometrically_feasible_incidences"], 9913
        )
        self.assertEqual(
            self.result["stoichiometrically_infeasible_incidences"], 2973
        )
        self.assertEqual(
            self.result["pairs_with_a_feasible_failing_descriptor"], 2360
        )
        self.assertEqual(
            self.result["pairs_without_a_feasible_failing_descriptor"], 151
        )
        self.assertEqual(
            self.result["classwise_tier_foster_branch"],
            {
                "input": 2511,
                "certified": 151,
                "remaining": 2360,
                "positive": {"input": 2312, "certified": 143, "remaining": 2169},
                "signed": {"input": 199, "certified": 8, "remaining": 191},
            },
        )

    def test_family_counts_and_hashes(self) -> None:
        self.assertEqual(
            self.result["positive"],
            {
                "with_feasible_obstruction": 2169,
                "without_feasible_obstruction": 143,
                "with_feasible_sha256": "6763a44c9c312c440997a054f7966347d101e3236cdef9ecb90599226de10458",
                "without_feasible_sha256": "f48882aa1ff52c1594a71fd217fa559492c7010e950285a9fa2e60e02b487b76",
            },
        )
        self.assertEqual(
            self.result["signed"],
            {
                "with_feasible_obstruction": 191,
                "without_feasible_obstruction": 8,
                "with_feasible_sha256": "f5c7a694bec0241a67b5cf588e1d074c11e00fb9ae3fbc1cee5570f84e9b4483",
                "without_feasible_sha256": "aead73fd44d08789019326cffcd706a776addf0cbc841979a3d54e8c80c5f88d",
            },
        )
        self.assertEqual(
            self.result["without_feasible_sha256"],
            "55e243945f86d106b920a27e2249a20b7077b5dc718ec06918cca4368e4a6c96",
        )
        self.assertEqual(
            self.result["feasible_incidence_sha256"],
            "2ef26eb13a33bf6e4339b92d001ea78c8c63efa6b8a16dfb9e9463c48e686c6b",
        )
        self.assertEqual(
            self.result["certificate_sha256"],
            "d330193b1a1a835118f5f1ce5c26031ea2948ab5665a2f67ed38ec4dadb3c2f5",
        )

    def test_ordered_affine_then_zero_cap_support_table(self) -> None:
        table = self.result["ordered_affine_then_zero_cap_support_table"]
        self.assertEqual(table["affine_infeasible"], 151)
        self.assertEqual(table["zero_cap_axis_after_affine"], 747)
        self.assertEqual(table["overlap"], 0)
        self.assertEqual(table["remaining"], 1613)
        self.assertEqual(
            table["positive"],
            {
                "input": 2312,
                "affine_infeasible": 143,
                "zero_cap_axis_after_affine": 596,
                "overlap": 0,
                "remaining": 1573,
                "closed_union_sha256": "366cc072bf69a3dc09277695573504b0d3091ba998c7c1ee3db93236e5d25c32",
                "remaining_sha256": "3c2b74280989e14aa235452f5b69d433706c132004f9643e02892e3fdb65c529",
            },
        )
        self.assertEqual(
            table["signed"],
            {
                "input": 199,
                "affine_infeasible": 8,
                "zero_cap_axis_after_affine": 151,
                "overlap": 0,
                "remaining": 40,
                "closed_union_sha256": "9bdcf7ca1c3ea6a0d9be4f5967f6d07f392b9ef37fef5c6e2fe18b34a5045178",
                "remaining_sha256": "a1dadb77c44b63fb6593f0e42726722d3ad6f89206593aaab398800d7cdbaf83",
            },
        )

    def test_active_coordinate_and_gate_counts(self) -> None:
        self.assertEqual(
            self.result["incidences_by_active_coordinate_count"],
            {
                "1": {"failing": 8365, "feasible": 6256, "infeasible": 2109},
                "2": {"failing": 3028, "feasible": 2388, "infeasible": 640},
                "3": {"failing": 1493, "feasible": 1269, "infeasible": 224},
            },
        )
        expected = (
            (653, 598, 55),
            (1026, 933, 93),
            (37, 32, 5),
            (206, 191, 15),
            (26, 20, 6),
            (54, 25, 29),
            (180, 144, 36),
            (3, 1, 2),
            (23, 22, 1),
            (2, 1, 1),
            (165, 159, 6),
            (23, 23, 0),
        )
        self.assertEqual(
            tuple(
                (
                    row["listed_pair_orbits"],
                    row["stoichiometrically_feasible"],
                    row["stoichiometrically_infeasible"],
                )
                for row in self.result["canonical_gate_rows"]
            ),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
