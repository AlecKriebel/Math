from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_k4_candidate.checker import (  # noqa: E402
    ANCHOR,
    CandidateFormatError,
    Graph,
    ImperfectionCertificate,
    MinorCertificate,
    SCHEMA,
    _cycle_certificate_is_valid,
    _classify_checks,
    _first_dominating_set,
    _first_maximum_independent_set,
    _maximal_independent_profile,
    _minor_certificate_is_valid,
    anchored_four_color_search,
    canonical_edges_bytes,
    check_eternal_family,
    graph6_sha256,
    load_candidate,
    parse_candidate,
    verify_candidate,
)


def pendant_triangle_product() -> tuple[Graph, tuple[tuple[int, ...], ...]]:
    """A connected exact gamma=alpha=gamma-infinity=4 positive control.

    It has theta=4, so it is deliberately not a counterexample.
    """

    fibers = (
        (0, 4, 8),
        (1, 5, 9),
        (2, 6, 10),
        (3, 7, 11),
    )
    edges: set[tuple[int, int]] = set()
    for fiber in fibers:
        edges.update(combinations(fiber, 2))
    edges.update(combinations((4, 5, 6, 7), 2))
    graph = Graph.from_edges(12, sorted(edges))
    family = tuple(
        sorted(
            {
                tuple(sorted(chosen))
                for chosen in product(*fibers)
            }
        )
    )
    return graph, family


def candidate_dict() -> dict[str, object]:
    graph, family = pendant_triangle_product()
    edges = graph.edges()
    graph6 = graph.to_graph6()
    return {
        "schema": SCHEMA,
        "order": 12,
        "edges": [list(edge) for edge in edges],
        "graph6": graph6,
        "graph6_sha256": graph6_sha256(graph6),
        "edges_sha256": sha256(canonical_edges_bytes(edges)).hexdigest(),
        "claims": {
            "gamma": 4,
            "independent_domination": 4,
            "alpha": 4,
            "eternal_domination": 4,
            "theta_lower_bound": 5,
        },
        "dominating_set": list(ANCHOR),
        "independent_set": list(ANCHOR),
        "eternal_family": [list(state) for state in family],
        # Syntactically valid but semantically false in this planar graph.
        "nonplanarity_minor": {
            "kind": "K5",
            "branch_sets": [[4], [5], [6], [7], [8]],
        },
        # Syntactically canonical but not an induced odd cycle here.
        "imperfection_witness": {
            "kind": "odd_hole",
            "vertices": [0, 1, 4, 5, 2],
        },
    }


class GraphAndParameterTests(unittest.TestCase):
    def test_graph6_against_hand_derived_standard_records(self) -> None:
        examples = (
            (Graph.from_edges(4, ()), "C?"),
            (Graph.from_edges(4, combinations(range(4), 2)), "C~"),
            (Graph.from_edges(4, ((0, 1), (1, 2), (2, 3))), "Ch"),
            (
                Graph.from_edges(
                    4,
                    ((0, 1), (1, 2), (2, 3), (0, 3)),
                ),
                "Cl",
            ),
            (
                Graph.from_edges(
                    5,
                    ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
                ),
                "Dhc",
            ),
        )
        for graph, expected in examples:
            with self.subTest(expected=expected):
                self.assertEqual(graph.to_graph6(), expected)

    def test_connected_product_control_has_exact_static_parameters(self) -> None:
        graph, _ = pendant_triangle_product()
        self.assertTrue(graph.is_connected())
        self.assertTrue(graph.is_independent(ANCHOR))
        self.assertEqual(_first_dominating_set(graph), (4, ANCHOR))
        self.assertEqual(_first_maximum_independent_set(graph), (4, ANCHOR))
        sizes, count = _maximal_independent_profile(graph)
        self.assertEqual(sizes, (4,))
        self.assertEqual(count, 48)

    def test_eternal_checker_uses_unoccupied_one_guard_edge_moves(self) -> None:
        graph, family = pendant_triangle_product()
        result = check_eternal_family(graph, family)
        self.assertTrue(result.passed, result.failures)
        self.assertEqual(result.family_size, 81)
        self.assertEqual(result.unoccupied_attacks_checked, 81 * 8)
        self.assertEqual(result.occupied_attacks_excluded, 81 * 4)
        self.assertEqual(result.independent_four_sets, 48)
        self.assertFalse(result.forced_independent_states_missing)
        empty = check_eternal_family(graph, ())
        self.assertFalse(empty.passed)
        self.assertIn("eternal family is empty", empty.failures)
        malformed = check_eternal_family(graph, ((0, 1, 2, 2),))
        self.assertFalse(malformed.passed)
        self.assertEqual(malformed.states_checked, 0)

        # Deleting one state destroys literal closure and the forced-state
        # check; an all-guards or merely reachability-based checker could miss
        # this mutation.
        deleted = check_eternal_family(graph, family[1:])
        self.assertFalse(deleted.passed)
        self.assertIn(ANCHOR, deleted.forced_independent_states_missing)
        self.assertTrue(
            any("no one-edge, one-guard response" in item for item in deleted.failures)
        )

        # Removing a traversed edge makes the same product family illegal.
        mutated_edges = tuple(edge for edge in graph.edges() if edge != (0, 4))
        edge_mutant = Graph.from_edges(12, mutated_edges)
        self.assertFalse(check_eternal_family(edge_mutant, family).passed)

        # A selected but nondominating four-state is rejected independently
        # of closure.
        bad_state = (0, 1, 4, 8)
        bad_family = tuple(sorted(set(family) | {bad_state}))
        bad = check_eternal_family(graph, bad_family)
        self.assertFalse(bad.passed)
        self.assertTrue(
            any("does not dominate" in item for item in bad.failures)
        )

    def test_minor_and_imperfection_certificates(self) -> None:
        k5 = Graph.from_edges(5, combinations(range(5), 2))
        valid, _ = _minor_certificate_is_valid(
            k5,
            MinorCertificate("K5", ((0,), (1,), (2,), (3,), (4,))),
        )
        self.assertTrue(valid)

        k33 = Graph.from_edges(
            6,
            ((left, right) for left in range(3) for right in range(3, 6)),
        )
        valid, _ = _minor_certificate_is_valid(
            k33,
            MinorCertificate(
                "K3,3",
                ((0,), (1,), (2,), (3,), (4,), (5,)),
            ),
        )
        self.assertTrue(valid)
        invalid, reason = _minor_certificate_is_valid(
            k33,
            MinorCertificate(
                "K5",
                ((0,), (1,), (2,), (3,), (4,)),
            ),
        )
        self.assertFalse(invalid)
        self.assertIn("no edge joins", reason)

        c5 = Graph.from_edges(
            5,
            ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
        )
        self.assertTrue(
            _cycle_certificate_is_valid(
                c5,
                ImperfectionCertificate("odd_hole", (0, 1, 2, 3, 4)),
            )
        )
        # C5 is self-complementary on the same cyclic order only after a
        # different ordering; the literal wrong kind/order is caught.
        self.assertFalse(
            _cycle_certificate_is_valid(
                c5,
                ImperfectionCertificate(
                    "odd_antihole",
                    (0, 1, 2, 3, 4),
                ),
            )
        )


class ColoringTraceTests(unittest.TestCase):
    def test_complete_trace_is_reproducible_and_exhausts_all_rows(self) -> None:
        graph, _ = pendant_triangle_product()
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "control.gt4trace"
            first = anchored_four_color_search(graph, trace_path=trace)
            second = anchored_four_color_search(graph)
            self.assertEqual(first, second)
            self.assertEqual(first.rows_checked, 4**8)
            self.assertEqual(first.proper_rows, 1)
            self.assertEqual(
                first.first_proper_coloring,
                (0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3),
            )
            self.assertEqual(
                first.trace_sha256,
                "73a64c176c178f978232718b8e62a77e29327c018b87445094b4849cb5399185",
            )
            raw = trace.read_bytes()
            self.assertEqual(sha256(raw).hexdigest(), first.trace_sha256)
            lines = raw.decode("ascii").splitlines()
            self.assertEqual(len(lines), 5 + 4**8 + 1)
            self.assertEqual(lines[0], "GT4TRACE 1")
            self.assertEqual(lines[4], "rows 65536")
            self.assertTrue(lines[5].startswith("r 00000 00000000 "))
            self.assertTrue(lines[-1].startswith("summary rows 65536 proper "))
            with self.assertRaises(FileExistsError):
                anchored_four_color_search(graph, trace_path=trace)

    def test_uncolorable_complement_control_has_no_proper_row(self) -> None:
        # H has a K5 on 0..4.  G is its complement, so the anchored search
        # must reject every row regardless of the other seven vertices.
        h_edges = set(combinations(range(5), 2))
        g_edges = tuple(
            pair
            for pair in combinations(range(12), 2)
            if pair not in h_edges
        )
        graph = Graph.from_edges(12, g_edges)
        self.assertTrue(graph.is_independent(ANCHOR))
        result = anchored_four_color_search(graph)
        self.assertEqual(result.rows_checked, 4**8)
        self.assertEqual(result.proper_rows, 0)
        self.assertIsNone(result.first_proper_coloring)
        self.assertEqual(
            result.trace_sha256,
            "00edf731b2cb422c6b1d0bd4ad28f1972344da5e3878591ddf53e382ee67b444",
        )

    def test_coloring_is_of_the_complement_not_the_input_graph(self) -> None:
        # G is the join of K5 with four disjoint cliques covering seven
        # vertices.  Thus chi(G) >= 5, while complement(G) is the disjoint
        # union of an edgeless five-set and a four-colorable graph.
        anchor_cliques = ((0, 9), (1, 10), (2, 11), (3,))
        k5_vertices = tuple(range(4, 9))
        edges: set[tuple[int, int]] = set(combinations(k5_vertices, 2))
        for clique in anchor_cliques:
            edges.update(combinations(clique, 2))
        for left in k5_vertices:
            for right in tuple(range(4)) + (9, 10, 11):
                edges.add(tuple(sorted((left, right))))
        graph = Graph.from_edges(12, sorted(edges))
        self.assertTrue(graph.is_independent(ANCHOR))
        search = anchored_four_color_search(graph)
        self.assertGreater(search.proper_rows, 0)


class FormatAndEndToEndMutationTests(unittest.TestCase):
    def test_strict_parser_rejects_schema_mutations(self) -> None:
        baseline = candidate_dict()
        parsed = parse_candidate(baseline)
        self.assertEqual(parsed.order, 12)
        self.assertEqual(parsed.independent_set, ANCHOR)

        extra = dict(baseline)
        extra["unexpected"] = 1
        with self.assertRaises(CandidateFormatError):
            parse_candidate(extra)

        boolean_vertex = json.loads(json.dumps(baseline))
        boolean_vertex["edges"][0][0] = False
        with self.assertRaises(CandidateFormatError):
            parse_candidate(boolean_vertex)

        unsorted_family = json.loads(json.dumps(baseline))
        unsorted_family["eternal_family"].reverse()
        with self.assertRaises(CandidateFormatError):
            parse_candidate(unsorted_family)

        noncanonical_cycle = json.loads(json.dumps(baseline))
        noncanonical_cycle["imperfection_witness"]["vertices"] = [1, 4, 5, 2, 0]
        with self.assertRaises(CandidateFormatError):
            parse_candidate(noncanonical_cycle)

    def test_duplicate_json_keys_and_oversized_files_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            duplicate = root / "duplicate.json"
            duplicate.write_text('{"schema":"a","schema":"b"}')
            with self.assertRaises(CandidateFormatError):
                load_candidate(duplicate)

            oversized = root / "oversized.json"
            oversized.write_bytes(b" " * 2_000_001)
            with self.assertRaises(CandidateFormatError):
                load_candidate(oversized)

            deeply_nested = root / "deeply-nested.json"
            deeply_nested.write_bytes(
                b"[" * 500_000 + b"]" * 500_000
            )
            with self.assertRaisesRegex(
                CandidateFormatError,
                "nesting is too deep",
            ):
                load_candidate(deeply_nested)

    def test_near_target_passes_decisive_equalities_but_is_not_accepted(self) -> None:
        parsed = parse_candidate(candidate_dict())
        report = verify_candidate(parsed)
        self.assertFalse(report["accepted"])
        self.assertEqual(
            report["status"],
            "REJECTED_NO_COUNTEREXAMPLE_VERIFIED",
        )
        self.assertTrue(report["checks"]["connected"]["passed"])
        self.assertTrue(report["checks"]["gamma_equals_4"]["passed"])
        self.assertTrue(report["checks"]["alpha_equals_4"]["passed"])
        self.assertTrue(report["checks"]["one_guard_eternal_family"]["passed"])
        self.assertTrue(
            report["checks"]["independent_domination_and_well_covered"]["passed"]
        )
        self.assertFalse(report["checks"]["theta_at_least_5"]["passed"])
        self.assertFalse(report["checks"]["nonplanar"]["passed"])
        self.assertFalse(
            report["checks"]["induced_odd_hole_or_antihole"]["passed"]
        )
        self.assertEqual(
            set(report["failed_checks"]),
            {
                "theta_at_least_5",
                "nonplanar",
                "induced_odd_hole_or_antihole",
            },
        )

    def test_identity_and_family_mutations_are_detected(self) -> None:
        parsed = parse_candidate(candidate_dict())

        identity_mutant = replace(parsed, graph6_sha256="0" * 64)
        identity_report = verify_candidate(identity_mutant)
        self.assertFalse(identity_report["checks"]["graph_identity"]["passed"])

        family_mutant = replace(
            parsed,
            eternal_family=parsed.eternal_family[1:],
        )
        family_report = verify_candidate(family_mutant)
        self.assertFalse(
            family_report["checks"]["one_guard_eternal_family"]["passed"]
        )

        wrong_anchor = replace(parsed, independent_set=(0, 1, 2, 4))
        anchor_report = verify_candidate(wrong_anchor)
        self.assertFalse(
            anchor_report["checks"]["anchored_complement_K4"]["passed"]
        )
        # The actual graph anchor remains valid, so the complete coloring
        # search still runs.  A bad redundant declaration cannot suppress a
        # definition-level graph check.
        self.assertEqual(
            anchor_report["checks"]["theta_at_least_5"][
                "anchor_normalized_rows_checked"
            ],
            4**8,
        )

    def test_definition_level_result_survives_consistency_alerts(self) -> None:
        checks = {
            "graph_identity": {"passed": True},
            "connected": {"passed": False},
            "gamma_equals_4": {"passed": True},
            "alpha_equals_4": {"passed": False},
            "one_guard_eternal_family": {"passed": True},
            "theta_at_least_5": {"passed": True},
        }
        mathematical, complete, status, consistency = _classify_checks(checks)
        self.assertTrue(mathematical)
        self.assertFalse(complete)
        self.assertEqual(
            status,
            "VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS",
        )
        self.assertEqual(consistency, ("connected", "alpha_equals_4"))

        checks["theta_at_least_5"]["passed"] = False
        mathematical, complete, status, _ = _classify_checks(checks)
        self.assertFalse(mathematical)
        self.assertFalse(complete)
        self.assertEqual(status, "REJECTED_NO_COUNTEREXAMPLE_VERIFIED")

    def test_cli_exit_codes_trace_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidate_path = root / "candidate.json"
            candidate_path.write_text(
                json.dumps(candidate_dict(), sort_keys=True, indent=2) + "\n"
            )
            trace = root / "candidate.gt4trace"
            environment = {
                "PYTHONPATH": str(CAMPAIGN / "src"),
                "PATH": "/usr/bin:/bin",
            }
            command = [
                sys.executable,
                "-m",
                "verifier_k4_candidate",
                str(candidate_path),
                "--color-trace",
                str(trace),
            ]
            result = subprocess.run(
                command,
                cwd=CAMPAIGN,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(
                report["status"],
                "REJECTED_NO_COUNTEREXAMPLE_VERIFIED",
            )
            self.assertTrue(trace.is_file())
            original = trace.read_bytes()

            repeated = subprocess.run(
                command,
                cwd=CAMPAIGN,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,
                check=False,
            )
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(trace.read_bytes(), original)
            self.assertEqual(
                json.loads(repeated.stdout)["status"],
                "MALFORMED_OR_IO_ERROR",
            )


if __name__ == "__main__":
    unittest.main()
