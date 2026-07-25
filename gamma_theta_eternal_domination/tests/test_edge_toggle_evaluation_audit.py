from __future__ import annotations

import ast
from itertools import combinations
import sqlite3
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from coverage_checker.graph import Graph  # noqa: E402
from edge_toggle_evaluation_checker.audit import (  # noqa: E402
    AuditPaths,
    EXPECTED_PARSER_SHA256,
    EXPECTED_ROWS,
    LedgerRow,
    ThirdAuditError,
    _validate_paths,
    collect_binding,
    generate_record,
    iter_ledger_rows,
    sha256_file,
    strict_json_loads,
    verify_record,
)


def cycle(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )


def ledger_row(graph: Graph, gamma: int, eternal: int) -> LedgerRow:
    values: tuple[object, ...] = (
        graph.to_graph6(),
        graph.order,
        graph.size,
        1,
        1,
        "TEST-SEED",
        0,
        graph.to_graph6(),
        gamma,
        gamma,
        3,
        3,
        eternal,
        eternal,
        eternal,
        eternal,
        "gamma_below_eternal",
        1,
        "0" * 64,
    )
    return LedgerRow(0, values, graph)


def production_paths() -> AuditPaths:
    return AuditPaths(
        campaign_root=ROOT,
        database=ROOT / "results/checkpoints/edge_toggles.sqlite3",
        checkpoint=ROOT / "results/checkpoints/edge_toggles.json",
        provenance_csv=ROOT / "results/edge_toggles_provenance.csv",
        unique_csv=ROOT / "results/edge_toggles_unique.csv",
        coverage_report=ROOT / "results/edge_toggle_coverage_audit.json",
        certificate=(
            ROOT / "results/edge_toggle_third_evaluation_certificates.ndjson"
        ),
        report=ROOT / "results/edge_toggle_third_evaluation_audit.json",
    )


class PerRowCertificateTests(unittest.TestCase):
    def test_c5_and_c7_records_generate_and_replay(self) -> None:
        for row in (ledger_row(cycle(5), 2, 3), ledger_row(cycle(7), 3, 4)):
            record = generate_record(row)
            gamma, initial, rounds = verify_record(row, record)
            self.assertEqual(gamma, row.values[8])
            self.assertGreater(initial, 0)
            self.assertGreater(rounds, 0)

    def test_blocker_trace_and_ledger_tampering_fail(self) -> None:
        row = ledger_row(cycle(7), 3, 4)
        record = generate_record(row)

        blocker_tamper = dict(record)
        blockers = [
            list(item) for item in blocker_tamper["lower_blockers"]
        ]
        blockers.pop()
        blocker_tamper["lower_blockers"] = blockers
        with self.assertRaisesRegex(ThirdAuditError, "domination proof"):
            verify_record(row, blocker_tamper)

        trace_tamper = dict(record)
        rounds = [
            [list(item) for item in round_]
            for round_ in trace_tamper["deletion_rounds"]
        ]
        rounds[0].pop()
        trace_tamper["deletion_rounds"] = rounds
        with self.assertRaisesRegex(ThirdAuditError, "fixed-point"):
            verify_record(row, trace_tamper)

        digest_tamper = dict(record)
        digest_tamper["ledger_row_sha256"] = "0" * 64
        with self.assertRaisesRegex(ThirdAuditError, "ledger_row_sha256"):
            verify_record(row, digest_tamper)

    def test_stored_gamma_and_category_are_reconciled_after_proof(self) -> None:
        graph = cycle(5)
        wrong_gamma = ledger_row(graph, 3, 4)
        with self.assertRaisesRegex(ThirdAuditError, "stored gamma"):
            generate_record(wrong_gamma)
        values = list(ledger_row(graph, 2, 3).values)
        values[16] = "candidate_eternal"
        wrong_category = LedgerRow(0, tuple(values), graph)
        with self.assertRaisesRegex(ThirdAuditError, "category"):
            generate_record(wrong_category)


class BindingAndIndependenceTests(unittest.TestCase):
    def test_production_binding_and_unique_row_count(self) -> None:
        paths = production_paths()
        binding = collect_binding(paths)
        self.assertEqual(binding["expected_rows"], EXPECTED_ROWS)
        self.assertEqual(
            binding["parser"]["sha256"], EXPECTED_PARSER_SHA256
        )
        connection = sqlite3.connect(
            paths.database.resolve().as_uri() + "?mode=ro&immutable=1",
            uri=True,
        )
        try:
            self.assertEqual(
                sum(1 for _ in iter_ledger_rows(connection, paths.unique_csv)),
                EXPECTED_ROWS,
            )
        finally:
            connection.close()

    def test_output_alias_to_database_is_rejected(self) -> None:
        paths = production_paths()
        bad = AuditPaths(
            campaign_root=paths.campaign_root,
            database=paths.database,
            checkpoint=paths.checkpoint,
            provenance_csv=paths.provenance_csv,
            unique_csv=paths.unique_csv,
            coverage_report=paths.coverage_report,
            certificate=paths.database,
            report=paths.report,
        )
        with self.assertRaisesRegex(ThirdAuditError, "alias"):
            _validate_paths(bad, verify_only=False)

    def test_strict_json_rejects_duplicate_keys_and_nonfinite_values(self) -> None:
        for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(ThirdAuditError):
                strict_json_loads(text, "test")

    def test_reused_parser_is_exactly_pinned(self) -> None:
        self.assertEqual(
            sha256_file(ROOT / "src/coverage_checker/graph.py"),
            EXPECTED_PARSER_SHA256,
        )

    def test_checker_imports_no_search_verifier_or_earlier_evaluator(self) -> None:
        forbidden: list[tuple[str, str]] = []
        checker = ROOT / "src/edge_toggle_evaluation_checker"
        for path in sorted(checker.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                modules: tuple[str, ...] = ()
                if isinstance(node, ast.Import):
                    modules = tuple(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules = (node.module,)
                for module in modules:
                    if module == "search" or module.startswith(
                        (
                            "search.",
                            "verifier_a",
                            "verifier_b",
                            "evaluation_checker",
                        )
                    ):
                        forbidden.append((path.name, module))
        self.assertEqual(forbidden, [])


if __name__ == "__main__":
    unittest.main()
