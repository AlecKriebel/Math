from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from pathlib import Path
import sys
import unittest

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.three_step_kernel import (  # noqa: E402
    ForcedFailureCertificate,
    KernelGraph,
    build_failure_node,
    build_survival_node,
    failure_from_json,
    failure_to_json,
    forced_failure_from_json,
    forced_failure_to_json,
    independence_number,
    is_independent,
    kernel_profile,
    survival_from_json,
    survival_to_json,
    verify_failure_node,
    verify_forced_failure,
    verify_survival_node,
)


def _graph_from_code(order: int, code: int) -> KernelGraph:
    edges = tuple(combinations(range(order), 2))
    return KernelGraph.from_edges(
        order,
        (
            edge
            for position, edge in enumerate(edges)
            if code & (1 << position)
        ),
    )


def _tamper_first_leaf(value: dict[str, object], witness: int) -> bool:
    if value.get("kind") == "nondominating":
        value["undominated"] = witness
        return True
    branches = value.get("branches")
    if not isinstance(branches, list):
        return False
    for branch in branches:
        if (
            isinstance(branch, dict)
            and isinstance(branch.get("child"), dict)
            and _tamper_first_leaf(branch["child"], witness)
        ):
            return True
    return False


class ThreeStepKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = KernelGraph.cycle(15)
        self.profile = kernel_profile(self.graph, 7)
        self.state = sum(
            1 << vertex for vertex in (0, 2, 4, 6, 8, 10, 12)
        )

    def test_c15_strictly_separates_K2_and_K3(self) -> None:
        self.assertEqual(
            [len(self.profile.level(index)) for index in range(4)],
            [765, 120, 15, 0],
        )
        maximum = tuple(
            state
            for state in self.profile.level(0)
            if is_independent(self.graph, state)
        )
        self.assertEqual(len(maximum), 15)
        self.assertTrue(all(state in self.profile.level(2) for state in maximum))
        self.assertTrue(all(state not in self.profile.level(3) for state in maximum))

        survival = build_survival_node(
            self.graph, self.profile, self.state, 2
        )
        failure = build_failure_node(
            self.graph, self.profile, self.state, 3
        )
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertTrue(verify_survival_node(self.graph, 7, survival))
        self.assertTrue(
            verify_forced_failure(
                self.graph,
                ForcedFailureCertificate(7, 3, self.state, failure),
            )
        )

    def test_graph6_round_trip(self) -> None:
        record = self.graph.to_graph6()
        self.assertEqual(KernelGraph.from_graph6(record), self.graph)
        self.assertEqual(
            KernelGraph.from_graph6(">>graph6<<" + record), self.graph
        )
        for malformed in ("", "~???", record + "?"):
            with self.subTest(record=malformed):
                with self.assertRaises(ValueError):
                    KernelGraph.from_graph6(malformed)

    def test_certificate_serialization_round_trip(self) -> None:
        survival = build_survival_node(
            self.graph, self.profile, self.state, 2
        )
        failure = build_failure_node(
            self.graph, self.profile, self.state, 3
        )
        assert failure is not None
        forced = ForcedFailureCertificate(7, 3, self.state, failure)
        decoded_survival = survival_from_json(survival_to_json(survival))
        decoded_failure = forced_failure_from_json(
            forced_failure_to_json(forced)
        )
        self.assertTrue(
            verify_survival_node(self.graph, 7, decoded_survival)
        )
        self.assertTrue(verify_forced_failure(self.graph, decoded_failure))

    def test_failure_checker_rejects_decisive_mutations(self) -> None:
        failure = build_failure_node(
            self.graph, self.profile, self.state, 3
        )
        assert failure is not None
        original = failure_to_json(failure)

        occupied_attack = deepcopy(original)
        occupied_attack["attack"] = 0
        self.assertFalse(
            verify_failure_node(
                self.graph,
                7,
                failure_from_json(occupied_attack),
                expected_state=self.state,
                expected_horizon=3,
            )
        )

        missing_branch = deepcopy(original)
        assert isinstance(missing_branch["branches"], list)
        missing_branch["branches"].pop()
        self.assertFalse(
            verify_failure_node(
                self.graph,
                7,
                failure_from_json(missing_branch),
                expected_state=self.state,
                expected_horizon=3,
            )
        )

        wrong_guard = deepcopy(original)
        assert isinstance(wrong_guard["branches"], list)
        wrong_guard["branches"][0]["guard"] = True
        self.assertFalse(
            verify_failure_node(
                self.graph,
                7,
                failure_from_json(wrong_guard),
                expected_state=self.state,
                expected_horizon=3,
            )
        )

        wrong_leaf = deepcopy(original)
        self.assertTrue(_tamper_first_leaf(wrong_leaf, 0))
        self.assertFalse(
            verify_failure_node(
                self.graph,
                7,
                failure_from_json(wrong_leaf),
                expected_state=self.state,
                expected_horizon=3,
            )
        )

    def test_survival_checker_rejects_decisive_mutations(self) -> None:
        survival = build_survival_node(
            self.graph, self.profile, self.state, 2
        )
        original = survival_to_json(survival)

        missing_attack = deepcopy(original)
        missing_attack["responses"].pop()
        self.assertFalse(
            verify_survival_node(
                self.graph,
                7,
                survival_from_json(missing_attack),
                expected_state=self.state,
                expected_horizon=2,
            )
        )

        occupied_attack = deepcopy(original)
        occupied_attack["responses"][0]["attack"] = 0
        self.assertFalse(
            verify_survival_node(
                self.graph,
                7,
                survival_from_json(occupied_attack),
                expected_state=self.state,
                expected_horizon=2,
            )
        )

        wrong_guard = deepcopy(original)
        wrong_guard["responses"][0]["guard"] = True
        self.assertFalse(
            verify_survival_node(
                self.graph,
                7,
                survival_from_json(wrong_guard),
                expected_state=self.state,
                expected_horizon=2,
            )
        )

    def test_recursive_finder_and_checker_through_order_four(self) -> None:
        for order in range(1, 5):
            edge_count = order * (order - 1) // 2
            for code in range(1 << edge_count):
                graph = _graph_from_code(order, code)
                for guard_count in range(1, order + 1):
                    profile = kernel_profile(graph, guard_count)
                    for state in range(1 << order):
                        if state.bit_count() != guard_count:
                            continue
                        for horizon in range(4):
                            failure = build_failure_node(
                                graph, profile, state, horizon
                            )
                            rejected = state not in profile.level(horizon)
                            self.assertEqual(failure is not None, rejected)
                            if failure is not None:
                                self.assertTrue(
                                    verify_failure_node(
                                        graph,
                                        guard_count,
                                        failure,
                                        expected_state=state,
                                        expected_horizon=horizon,
                                    )
                                )
                            else:
                                survival = build_survival_node(
                                    graph, profile, state, horizon
                                )
                                self.assertTrue(
                                    verify_survival_node(
                                        graph,
                                        guard_count,
                                        survival,
                                        expected_state=state,
                                        expected_horizon=horizon,
                                    )
                                )

    def test_forced_checker_requires_exact_alpha(self) -> None:
        failure = build_failure_node(
            self.graph, self.profile, self.state, 3
        )
        assert failure is not None
        valid = ForcedFailureCertificate(7, 3, self.state, failure)
        self.assertEqual(independence_number(self.graph), 7)
        self.assertTrue(verify_forced_failure(self.graph, valid))
        self.assertFalse(
            verify_forced_failure(
                self.graph,
                ForcedFailureCertificate(6, 3, self.state, failure),
            )
        )


if __name__ == "__main__":
    unittest.main()
