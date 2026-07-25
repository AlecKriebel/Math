from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.private_obstruction import (  # noqa: E402
    FailedGuard,
    PrivateObstruction,
    find_private_obstruction,
    verify_private_obstruction,
)
from verifier_a.core import BitGraph  # noqa: E402


class PrivateObstructionTests(unittest.TestCase):
    def test_c5_has_checkable_obstruction(self) -> None:
        graph = BitGraph.cycle(5)
        obstruction = find_private_obstruction(graph)
        self.assertIsNotNone(obstruction)
        assert obstruction is not None
        self.assertTrue(verify_private_obstruction(graph, obstruction))

    def test_equal_examples_have_no_obstruction(self) -> None:
        for graph in (
            BitGraph.complete(6),
            BitGraph.edgeless(6),
            BitGraph.path(6),
            BitGraph.cycle(6),
        ):
            with self.subTest(graph6=graph.to_graph6()):
                self.assertIsNone(find_private_obstruction(graph))

    def test_published_alpha_equal_near_misses_pass_local_test(self) -> None:
        for record in ("IEhbtj{ro", "IEhbtn{ro"):
            graph = BitGraph.from_graph6(record)
            self.assertIsNone(find_private_obstruction(graph))

    def test_local_condition_is_not_sufficient(self) -> None:
        # This canonical geng record is a relabeling of C7. It passes every
        # maximum-independent-state check although alpha=3 and gamma_inf=4.
        graph = BitGraph.from_graph6("FCp`_")
        self.assertIsNone(find_private_obstruction(graph))

    def test_malformed_obstruction_fails_closed(self) -> None:
        graph = BitGraph.cycle(5)
        obstruction = find_private_obstruction(graph)
        self.assertIsNotNone(obstruction)
        assert obstruction is not None

        for attack in (-1, graph.n, graph.n + 7, True):
            with self.subTest(attack=attack):
                self.assertFalse(
                    verify_private_obstruction(
                        graph, replace(obstruction, attack=attack)
                    )
                )

        valid_record = obstruction.failed_guards[0]
        invalid_record = FailedGuard(
            valid_record.guard, newly_undominated=graph.n
        )
        for duplicate_records in (
            (invalid_record,) + obstruction.failed_guards,
            obstruction.failed_guards + (invalid_record,),
        ):
            self.assertFalse(
                verify_private_obstruction(
                    graph,
                    replace(
                        obstruction, failed_guards=duplicate_records
                    ),
                )
            )

        self.assertFalse(
            verify_private_obstruction(
                BitGraph.edgeless(0), PrivateObstruction(0, 0, ())
            )
        )


if __name__ == "__main__":
    unittest.main()
