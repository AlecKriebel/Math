from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_croot_cover as production  # noqa: E402
import global_croot_cover_check as independent  # noqa: E402


def random_graph(order: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    adjacency = [0] * order
    for left in range(order):
        for right in range(left + 1, order):
            if rng.getrandbits(1):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return adjacency


class GlobalCrootCoverTests(unittest.TestCase):
    def test_zero_sum_and_complement_invariance_on_random_graphs(self) -> None:
        for order in (7, 9, 12):
            for seed in range(5):
                graph = random_graph(order, 100 * order + seed)
                graph_complement = production.complement(graph)
                excess = [
                    production.local_excess_twice(graph, vertex)
                    for vertex in range(order)
                ]
                self.assertEqual(sum(excess), 0)
                self.assertEqual(
                    excess,
                    [
                        production.local_excess_twice(
                            graph_complement, vertex
                        )
                        for vertex in range(order)
                    ],
                )

    def test_thresholds_and_literal_counts(self) -> None:
        self.assertEqual(
            [production.croot_threshold(d) for d in (18, 19, 20, 21)],
            [213, 206, 201, 200],
        )
        for degree in (18, 19, 20, 21):
            good = production.croot_good_literals(degree)
            self.assertEqual(
                len(good),
                degree * (degree - 1) // 2
                + (42 - degree) * (41 - degree) // 2,
            )
            self.assertEqual(
                set(good),
                set(independent.good_literals(degree)),
            )

    def test_basic_and_refined_records_match_independently(self) -> None:
        plan = production.build_plan()
        expected_basic = [
            independent.basic_record(degree) for degree in (18, 19, 20, 21)
        ]
        self.assertEqual(plan["basic_cover"]["branches"], expected_basic)
        expected_refined = [
            independent.refined_record(degree, mu)
            for mu in (18, 19, 20)
            for degree in (18, 19, 20, 21)
            if mu <= degree
        ]
        self.assertEqual(
            plan["optional_exact_mu_refinement"]["branches"],
            expected_refined,
        )
        self.assertEqual(len(expected_refined), 9)

    def test_exact_mu_selector_layout(self) -> None:
        for mu, degree in (
            (18, 18),
            (18, 21),
            (19, 19),
            (19, 21),
            (20, 20),
            (20, 21),
        ):
            counter, next_variable = production.croot_counter(degree)
            clauses, triggers, after = production.exact_mu_selector_clauses(
                degree, mu, next_variable
            )
            selectors = clauses[0]
            self.assertEqual(len(selectors), 86)
            self.assertEqual(len(clauses), 87)
            self.assertEqual(len(triggers), 86)
            self.assertEqual(after, next_variable + 86)
            self.assertEqual(counter.auxiliary_count, next_variable - 65_404)
            self.assertEqual(clauses[1][0], -selectors[0])
            self.assertEqual(clauses[2][0], -selectors[1])
            self.assertLessEqual(max(triggers), 65_403)

    def test_circulant_normalization_and_threshold_equivalence(self) -> None:
        graph = [0] * 43
        for left in range(43):
            for distance in range(1, 11):
                right = (left + distance) % 43
                graph[left] |= 1 << right
                graph[right] |= 1 << left
        self.assertTrue(all(degree == 20 for degree in production.graph_degrees(graph)))
        normalized, complemented, degree, excess_twice = (
            production.normalize_croot(graph)
        )
        self.assertFalse(complemented)
        self.assertEqual(degree, 20)
        self.assertEqual(excess_twice, 0)
        assignment = {
            production.variable_for_edge(43, left, right): bool(
                (normalized[left] >> right) & 1
            )
            for left in range(43)
            for right in range(left + 1, 43)
        }
        good_count = sum(
            assignment[abs(literal)] == (literal > 0)
            for literal in production.croot_good_literals(degree)
        )
        self.assertEqual(good_count, production.croot_threshold(degree))


if __name__ == "__main__":
    unittest.main()
