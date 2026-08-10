from fractions import Fraction
from itertools import permutations
import unittest

from exact_shielded_seam import (
    COMPLEXES,
    EXPECTED_EXACT_SEAM_SUPPORTS,
    NAMES,
    SIGNED_SUPPORTS,
    UNSUPPORTED_MULTI_VERTEX_SUPPORTS,
    autonomous_c_weight,
    certificate,
    exact_seam_supports,
    positive_invariant_shielded_supports,
    residual_busy_period_hazards,
    reversible_pair_divergence_bound,
    single_linkage_deficiency,
    triple_fluid_coefficients,
)


class ExactShieldedSeamEnumeration(unittest.TestCase):
    def test_exact_seven_support_filter(self) -> None:
        positive = positive_invariant_shielded_supports()
        self.assertEqual(len(positive), 25)
        self.assertEqual(exact_seam_supports(), EXPECTED_EXACT_SEAM_SUPPORTS)
        self.assertEqual(len(exact_seam_supports()), 7)

    def test_direct_and_uncovered_partition(self) -> None:
        result = certificate()
        self.assertEqual(result["two_vertex_supports"], 16)
        self.assertEqual(result["direct_fast_bound_supports"], 17)
        self.assertEqual(
            frozenset(tuple(item) for item in result["unsupported_multi_vertex_supports"]),
            UNSUPPORTED_MULTI_VERTEX_SUPPORTS,
        )
        self.assertEqual(len(UNSUPPORTED_MULTI_VERTEX_SUPPORTS), 8)

    def test_deficiency_one_and_signed_supports(self) -> None:
        deficiency_one = {
            support
            for support in positive_invariant_shielded_supports()
            if single_linkage_deficiency(support) == 1
        }
        self.assertEqual(
            deficiency_one,
            {
                ("0", "C", "2C"),
                ("2A", "2B", "AB"),
                ("A", "B", "AC", "BC"),
            },
        )
        self.assertEqual(len(SIGNED_SUPPORTS), 4)
        for support in SIGNED_SUPPORTS:
            vectors = [COMPLEXES[NAMES.index(name)] for name in support]
            invariant_values = {vector[1] - vector[2] for vector in vectors}
            self.assertEqual(invariant_values, {0})


class ExactGeneratorAlgebra(unittest.TestCase):
    def test_residual_busy_period_refutes_one_target_service_margin(self) -> None:
        for population in (10, 100, 10_000):
            positive, negative, flat = residual_busy_period_hazards(population)
            self.assertEqual(positive, (population - 2) * (population - 3) + 1)
            self.assertEqual(negative, population - 1)
            self.assertEqual(flat, 2)
            self.assertEqual(positive - negative, population**2 - 6 * population + 8)
        positive, negative, flat = residual_busy_period_hazards(10_000)
        self.assertGreater(Fraction(positive, positive + negative + flat), Fraction(999, 1000))

    def test_reversible_pair_log_bound_is_only_affine(self) -> None:
        # The exact seam 2B <-> A+B pair, with deliberately unequal rates.
        source = COMPLEXES[NAMES.index("2B")]
        target = COMPLEXES[NAMES.index("AB")]
        alpha = Fraction(3, 7)
        beta = Fraction(11, 5)
        values = []
        for population in range(4, 80):
            state = (population // 3, population - population // 3, 5)
            bound = reversible_pair_divergence_bound(
                state,
                source,
                target,
                alpha,
                beta,
            )
            values.append(abs(bound) / (1 + sum(state)))
        self.assertLess(max(values), 10)

    def test_every_two_vertex_divergence_is_affine_in_the_interior(self) -> None:
        two_vertex = [
            support
            for support in positive_invariant_shielded_supports()
            if len(support) == 2
        ]
        self.assertEqual(len(two_vertex), 16)
        alpha = Fraction(3, 7)
        beta = Fraction(11, 5)
        base = (10, 11, 12)

        def add(state, coordinate, amount=1):
            return tuple(
                value + (amount if index == coordinate else 0)
                for index, value in enumerate(state)
            )

        for support in two_vertex:
            source = COMPLEXES[NAMES.index(support[0])]
            target = COMPLEXES[NAMES.index(support[1])]

            def value(state):
                return reversible_pair_divergence_bound(
                    state,
                    source,
                    target,
                    alpha,
                    beta,
                )

            for coordinate in range(3):
                self.assertEqual(
                    value(add(base, coordinate, 2))
                    - 2 * value(add(base, coordinate))
                    + value(base),
                    0,
                    support,
                )
            for first in range(3):
                for second in range(first + 1, 3):
                    mixed = tuple(
                        base[index]
                        + (1 if index == first else 0)
                        + (1 if index == second else 0)
                        for index in range(3)
                    )
                    self.assertEqual(
                        value(mixed)
                        - value(add(base, first))
                        - value(add(base, second))
                        + value(base),
                        0,
                        support,
                    )

    def test_triple_endpoint_coefficients_for_every_strong_digraph(self) -> None:
        directed_edges = tuple(permutations((0, 1, 2), 2))
        strongly_connected_count = 0
        for edge_mask in range(1, 1 << len(directed_edges)):
            edges = [
                directed_edges[index]
                for index in range(len(directed_edges))
                if edge_mask >> index & 1
            ]
            reach = [[False] * 3 for _ in range(3)]
            for source, target in edges:
                reach[source][target] = True
            for middle in range(3):
                for source in range(3):
                    for target in range(3):
                        reach[source][target] |= reach[source][middle] and reach[middle][target]
            if not all(reach[source][target] for source in range(3) for target in range(3) if source != target):
                continue
            strongly_connected_count += 1
            weighted_edges = [
                (source, target, Fraction(index + 1, index + 2))
                for index, (source, target) in enumerate(edges)
            ]
            gamma_zero, _, gamma_two = triple_fluid_coefficients(weighted_edges)
            self.assertGreater(gamma_zero, 0)
            self.assertLess(gamma_two, 0)
        self.assertGreater(strongly_connected_count, 0)

    def test_autonomous_c_detailed_balance(self) -> None:
        alpha = Fraction(7, 3)
        beta = Fraction(5, 11)
        for parity in (0, 1):
            for population in range(parity, 30, 2):
                left = autonomous_c_weight(parity, population, alpha, beta) * alpha
                right = (
                    autonomous_c_weight(parity, population + 2, alpha, beta)
                    * beta
                    * (population + 2)
                    * (population + 1)
                )
                self.assertEqual(left, right)


if __name__ == "__main__":
    unittest.main()
