"""Tests for the structurally independent verifier B."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from itertools import combinations, permutations, product
from pathlib import Path


CAMPAIGN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN_ROOT / "src"))

from verifier_b import (  # noqa: E402
    EternalCertificate,
    Graph,
    Move,
    build_colored_configuration_digraph,
    chromatic_number,
    clique_cover_number,
    complete_graph,
    cycle_graph,
    domination_number,
    edgeless_graph,
    eternal_domination_decision,
    eternal_domination_number,
    independence_number,
    independent_domination_number,
    is_dominating,
    is_independent,
    is_well_covered,
    make_eternal_certificate,
    minimum_clique_partition,
    path_graph,
    verify_eternal_certificate,
    verify_eternal_family,
)


def all_labeled_graphs(order: int):
    possible_edges = tuple(combinations(range(order), 2))
    for choices in product((False, True), repeat=len(possible_edges)):
        yield Graph.from_edges(
            order,
            (
                edge
                for edge, chosen in zip(possible_edges, choices)
                if chosen
            ),
        )


def brute_domination_number(graph: Graph) -> int:
    for size in range(graph.order + 1):
        for candidate in combinations(graph.vertices, size):
            if all(
                vertex in candidate
                or any(neighbor in candidate for neighbor in graph.adjacency[vertex])
                for vertex in graph.vertices
            ):
                return size
    raise AssertionError


def brute_independence_number(graph: Graph) -> int:
    best = 0
    for size in range(graph.order + 1):
        for candidate in combinations(graph.vertices, size):
            if all(
                second not in graph.adjacency[first]
                for first, second in combinations(candidate, 2)
            ):
                best = max(best, size)
    return best


def brute_independent_domination_number(graph: Graph) -> int:
    for size in range(graph.order + 1):
        for candidate in combinations(graph.vertices, size):
            independent = all(
                second not in graph.adjacency[first]
                for first, second in combinations(candidate, 2)
            )
            dominating = all(
                vertex in candidate
                or any(neighbor in candidate for neighbor in graph.adjacency[vertex])
                for vertex in graph.vertices
            )
            if independent and dominating:
                return size
    raise AssertionError


def brute_chromatic_number(graph: Graph) -> int:
    if graph.order == 0:
        return 0
    for color_count in range(1, graph.order + 1):
        for assignment in product(range(color_count), repeat=graph.order):
            if all(
                assignment[first] != assignment[second]
                for first, second in graph.edges()
            ):
                return color_count
    raise AssertionError


def brute_eternal_decision(graph: Graph, guard_count: int) -> bool:
    """Very small oracle: enumerate every nonempty family."""

    configurations = tuple(
        frozenset(candidate)
        for candidate in combinations(graph.vertices, guard_count)
        if is_dominating(graph, candidate)
    )
    for family_size in range(1, len(configurations) + 1):
        for chosen_family in combinations(configurations, family_size):
            family = frozenset(chosen_family)
            if verify_eternal_family(graph, guard_count, family):
                return True
    return graph.order == 0 and guard_count == 0


def erroneous_all_guards_decision(graph: Graph, guard_count: int) -> bool:
    """A deliberately wrong all-guards-move implementation used as a trap."""

    configs = tuple(
        frozenset(candidate)
        for candidate in combinations(graph.vertices, guard_count)
        if is_dominating(graph, candidate)
    )
    alive = set(configs)

    def simultaneous_relocation(source, target) -> bool:
        for destination_order in permutations(target):
            if all(
                destination == guard or destination in graph.adjacency[guard]
                for guard, destination in zip(sorted(source), destination_order)
            ):
                return True
        return False

    while alive:
        doomed = set()
        for source in alive:
            for attack in set(graph.vertices) - set(source):
                if not any(
                    attack in target
                    and simultaneous_relocation(source, target)
                    for target in alive
                ):
                    doomed.add(source)
                    break
        if not doomed:
            return True
        alive.difference_update(doomed)
    return False


def erroneous_attacks_occupied_vertices(graph: Graph, guard_count: int) -> bool:
    """Wrongly require a genuine move even when the attacked vertex is occupied."""

    digraph = build_colored_configuration_digraph(graph, guard_count)
    alive = set(digraph.configurations)
    while alive:
        doomed = set()
        for source in alive:
            for attack in graph.vertices:  # Wrong: includes occupied vertices.
                if attack in source:
                    doomed.add(source)
                    break
                if not any(
                    move.target in alive
                    for move in digraph.moves(source, attack)
                ):
                    doomed.add(source)
                    break
        if not doomed:
            return True
        alive.difference_update(doomed)
    return False


class GraphRepresentationTests(unittest.TestCase):
    def test_rejects_loops_and_asymmetry(self):
        with self.assertRaises(ValueError):
            Graph.from_edges(2, [(0, 0)])
        with self.assertRaises(ValueError):
            Graph((frozenset({1}), frozenset()))

    def test_graph6_known_records(self):
        self.assertEqual(edgeless_graph(3).to_graph6(), "B?")
        self.assertEqual(complete_graph(3).to_graph6(), "Bw")
        self.assertEqual(path_graph(3).to_graph6(), "Bg")
        self.assertEqual(Graph.from_graph6("B?"), edgeless_graph(3))
        self.assertEqual(Graph.from_graph6(">>graph6<<Bw\n"), complete_graph(3))

    def test_graph6_round_trip_all_graphs_through_order_five(self):
        for order in range(6):
            for graph in all_labeled_graphs(order):
                self.assertEqual(Graph.from_graph6(graph.to_graph6()), graph)
                self.assertEqual(
                    Graph.from_graph6(graph.to_graph6(header=True)), graph
                )

    def test_graph6_rejects_bad_payload_and_padding(self):
        with self.assertRaises(ValueError):
            Graph.from_graph6("B")
        with self.assertRaises(ValueError):
            Graph.from_graph6("B@")  # Nonzero padding after three edge bits.
        with self.assertRaises(ValueError):
            Graph.from_graph6("~???")  # Noncanonical extended encoding of n=0.
        with self.assertRaises(ValueError):
            Graph.from_graph6("~~??????")  # Noncanonical 36-bit encoding.

    def test_complement_is_an_involution(self):
        graph = Graph.from_edges(5, [(0, 1), (0, 4), (2, 4)])
        self.assertEqual(graph.complement().complement(), graph)


class ExactInvariantTests(unittest.TestCase):
    def test_standard_graph_parameters(self):
        cases = (
            (complete_graph(4), (1, 1, 1, 1, 1)),
            (edgeless_graph(4), (4, 4, 4, 4, 4)),
            (path_graph(3), (1, 1, 2, 2, 2)),
            (path_graph(4), (2, 2, 2, 2, 2)),
            (path_graph(5), (2, 2, 3, 3, 3)),
            (cycle_graph(4), (2, 2, 2, 2, 2)),
            (cycle_graph(5), (2, 2, 2, 3, 3)),
            (cycle_graph(6), (2, 2, 3, 3, 3)),
        )
        for graph, expected in cases:
            actual = (
                domination_number(graph),
                independent_domination_number(graph),
                independence_number(graph),
                eternal_domination_number(graph),
                clique_cover_number(graph),
            )
            self.assertEqual(actual, expected, graph.to_graph6())

    def test_two_published_order_ten_near_misses(self):
        # MacGillivray--Mynhardt--Virgile (2022), Table 9.
        for record, edge_count in (("IEhbtj{ro", 26), ("IEhbtn{ro", 27)):
            graph = Graph.from_graph6(record)
            self.assertEqual(graph.order, 10)
            self.assertEqual(graph.size, edge_count)
            actual = (
                domination_number(graph),
                independent_domination_number(graph),
                independence_number(graph),
                eternal_domination_number(graph),
                clique_cover_number(graph),
            )
            self.assertEqual(actual, (2, 2, 3, 3, 4), record)

    def test_empty_graph_conventions(self):
        graph = edgeless_graph(0)
        self.assertEqual(domination_number(graph), 0)
        self.assertEqual(independent_domination_number(graph), 0)
        self.assertEqual(independence_number(graph), 0)
        self.assertEqual(eternal_domination_number(graph), 0)
        self.assertEqual(clique_cover_number(graph), 0)
        self.assertTrue(eternal_domination_decision(graph, 0))

    def test_clique_cover_really_colors_the_complement(self):
        clique = complete_graph(5)
        independent = edgeless_graph(5)
        self.assertEqual(chromatic_number(clique), 5)
        self.assertEqual(clique_cover_number(clique), 1)
        self.assertEqual(chromatic_number(independent), 1)
        self.assertEqual(clique_cover_number(independent), 5)

    def test_clique_partition_is_valid(self):
        graph = path_graph(7)
        partition = minimum_clique_partition(graph)
        self.assertEqual(len(partition), clique_cover_number(graph))
        self.assertEqual(set().union(*map(set, partition)), set(graph.vertices))
        self.assertEqual(sum(map(len, partition)), graph.order)
        for part in partition:
            self.assertTrue(
                all(
                    second in graph.adjacency[first]
                    for first, second in combinations(part, 2)
                )
            )

    def test_well_covered_examples(self):
        self.assertTrue(is_well_covered(complete_graph(5)))
        self.assertTrue(is_well_covered(cycle_graph(5)))
        self.assertFalse(is_well_covered(path_graph(3)))

    def test_against_transparent_oracles_all_graphs_through_order_four(self):
        for order in range(5):
            for graph in all_labeled_graphs(order):
                self.assertEqual(domination_number(graph), brute_domination_number(graph))
                self.assertEqual(
                    independent_domination_number(graph),
                    brute_independent_domination_number(graph),
                )
                self.assertEqual(
                    independence_number(graph), brute_independence_number(graph)
                )
                self.assertEqual(
                    chromatic_number(graph), brute_chromatic_number(graph)
                )
                self.assertEqual(
                    clique_cover_number(graph),
                    brute_chromatic_number(graph.complement()),
                )


class EternalDominationTests(unittest.TestCase):
    def test_decision_matches_family_enumeration_through_order_four(self):
        for order in range(5):
            for graph in all_labeled_graphs(order):
                for guard_count in range(order + 1):
                    self.assertEqual(
                        eternal_domination_decision(graph, guard_count),
                        brute_eternal_decision(graph, guard_count),
                        (graph.to_graph6(), guard_count),
                    )

    def test_attack_colors_are_exactly_unoccupied_vertices(self):
        graph = cycle_graph(5)
        digraph = build_colored_configuration_digraph(graph, 2)
        for source in digraph.configurations:
            self.assertEqual(
                set(digraph.attacks_from(source)),
                set(graph.vertices) - set(source),
            )

    def test_every_arc_is_one_edge_move_to_a_dominating_configuration(self):
        graph = cycle_graph(6)
        digraph = build_colored_configuration_digraph(graph, 3)
        for source in digraph.configurations:
            for attack in digraph.attacks_from(source):
                for move in digraph.moves(source, attack):
                    self.assertNotIn(attack, source)
                    self.assertIn(move.guard, source)
                    self.assertIn(attack, graph.adjacency[move.guard])
                    self.assertEqual(
                        move.target,
                        frozenset((source - {move.guard}) | {attack}),
                    )
                    self.assertEqual(
                        source.symmetric_difference(move.target),
                        frozenset((move.guard, attack)),
                    )
                    self.assertTrue(is_dominating(graph, move.target))

    def test_c5_traps_all_guards_move_variant(self):
        graph = cycle_graph(5)
        self.assertFalse(eternal_domination_decision(graph, 2))
        self.assertTrue(erroneous_all_guards_decision(graph, 2))
        self.assertEqual(eternal_domination_number(graph), 3)

    def test_occupied_attack_variant_is_detected(self):
        graph = complete_graph(2)
        self.assertTrue(eternal_domination_decision(graph, 1))
        self.assertFalse(erroneous_attacks_occupied_vertices(graph, 1))

    def test_resulting_configurations_must_dominate(self):
        graph = path_graph(3)
        center = frozenset({1})
        self.assertTrue(is_dominating(graph, center))
        self.assertFalse(eternal_domination_decision(graph, 1))
        digraph = build_colored_configuration_digraph(graph, 1)
        self.assertEqual(digraph.configurations, (center,))
        self.assertEqual(digraph.moves(center, 0), ())
        self.assertEqual(digraph.moves(center, 2), ())

    def test_certificate_round_trip_and_tamper_detection(self):
        graph = cycle_graph(6)
        certificate = make_eternal_certificate(graph, 3)
        self.assertIsNotNone(certificate)
        assert certificate is not None
        self.assertTrue(verify_eternal_certificate(graph, certificate))
        self.assertTrue(
            verify_eternal_family(
                graph, certificate.guard_count, certificate.family
            )
        )

        first = certificate.responses[0]
        bad_move = Move(
            source=first.source,
            attack=first.attack,
            guard=first.guard,
            target=first.source,
        )
        tampered = EternalCertificate(
            certificate.guard_count,
            certificate.family,
            (bad_move,) + certificate.responses[1:],
        )
        self.assertFalse(verify_eternal_certificate(graph, tampered))

    def test_rejects_non_dominating_proposed_family(self):
        graph = path_graph(3)
        self.assertFalse(verify_eternal_family(graph, 1, [{0}, {2}]))

    def test_out_of_range_guard_counts(self):
        graph = path_graph(4)
        self.assertFalse(eternal_domination_decision(graph, -1))
        self.assertFalse(eternal_domination_decision(graph, 5))
        self.assertFalse(eternal_domination_decision(graph, 0))


class CommandLineTests(unittest.TestCase):
    def test_cli_emits_checkable_one_guard_data(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "verifier_b.cli",
                cycle_graph(5).to_graph6(),
                "--family",
            ],
            cwd=CAMPAIGN_ROOT,
            env={
                **dict(os.environ),
                "PYTHONPATH": str(CAMPAIGN_ROOT / "src"),
            },
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(completed.stdout)
        self.assertEqual(data["gamma"], 2)
        self.assertEqual(data["gamma_infinity_one_guard"], 3)
        self.assertEqual(data["theta"], 3)
        self.assertTrue(data["eternal_family"])
        expected_response_count = sum(
            data["n"] - len(configuration)
            for configuration in data["eternal_family"]
        )
        self.assertEqual(len(data["responses"]), expected_response_count)


if __name__ == "__main__":
    unittest.main()
