from __future__ import annotations

import ast
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from edge_toggle_coverage_checker.audit import (  # noqa: E402
    AuditError,
    AuditPaths,
    EXPECTED_ORIGINS,
    _chain_step,
    _expected_origins,
    _validate_origin,
    load_seed_universe,
)
from edge_toggle_coverage_checker.graph import Graph  # noqa: E402


def _paths() -> AuditPaths:
    return AuditPaths(
        campaign_root=CAMPAIGN,
        seed_input=CAMPAIGN / "results" / "extensions_unique.csv",
        extension_coverage_audit=(
            CAMPAIGN / "results" / "extension_coverage_audit.json"
        ),
        extension_evaluation_audit=(
            CAMPAIGN / "results" / "extensions_evaluation_audit.json"
        ),
        database=(
            CAMPAIGN / "results" / "checkpoints" / "edge_toggles.sqlite3"
        ),
        checkpoint=(
            CAMPAIGN / "results" / "checkpoints" / "edge_toggles.json"
        ),
        provenance_csv=CAMPAIGN / "results" / "edge_toggles_provenance.csv",
        unique_csv=CAMPAIGN / "results" / "edge_toggles_unique.csv",
        candidate_directory=(
            CAMPAIGN / "certificates" / "frozen_edge_toggle_candidates"
        ),
        state_database=(
            CAMPAIGN
            / "results"
            / "checkpoints"
            / "edge_toggle_coverage_audit.sqlite3"
        ),
        report=CAMPAIGN / "results" / "edge_toggle_coverage_audit.json",
    )


class EdgeToggleCoverageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = _paths()
        cls.seeds = load_seed_universe(cls.paths)

    def test_exact_independent_seed_scope(self) -> None:
        self.assertEqual(len(self.seeds), 391)
        self.assertEqual(
            Counter(seed.order for seed in self.seeds),
            Counter({11: 15, 12: 376}),
        )
        self.assertEqual(
            Counter(seed.source_category for seed in self.seeds),
            Counter(
                {
                    "eternal_false_without_private_obstruction": 285,
                    "private_obstruction_eternal_false": 106,
                }
            ),
        )
        self.assertEqual(
            sum(seed.raw_expected for seed in self.seeds), EXPECTED_ORIGINS
        )
        digest = hashlib.sha256()
        for seed in self.seeds:
            digest.update(
                (
                    f"{seed.index},{seed.seed_id},{seed.graph6},{seed.order},"
                    f"{seed.size},{seed.source_category}\n"
                ).encode("ascii")
            )
        self.assertEqual(
            digest.hexdigest(),
            "60aee3b57d16a8cfc9f5b84ca4a8580d236679196011eded9b4b054aa010beb5",
        )

    def test_every_seed_pair_occurs_once_in_lexicographic_order(self) -> None:
        origins = _expected_origins(self.seeds)
        self.assertEqual(len(origins), EXPECTED_ORIGINS)
        self.assertEqual(
            len(
                {
                    (seed.seed_id, pair_index)
                    for _, seed, pair_index, _, _ in origins
                }
            ),
            EXPECTED_ORIGINS,
        )
        for global_index, (stored_index, seed, pair_index, first, second) in (
            enumerate(origins)
        ):
            self.assertEqual(global_index, stored_index)
            self.assertEqual((first, second), seed.pairs[pair_index])

    def test_origin_reconstruction_accepts_independent_relabeling(self) -> None:
        expected = _expected_origins(self.seeds)[0]
        _, seed, pair_index, first, second = expected
        seed_graph = Graph.from_graph6(seed.graph6)
        raw = seed_graph.toggled(first, second)
        permutation = tuple(reversed(range(seed.order)))
        canonical = raw.relabeled(permutation)
        row = (
            seed.index,
            seed.seed_id,
            pair_index,
            first,
            second,
            "delete" if seed_graph.has_edge(first, second) else "add",
            raw.to_graph6(),
            canonical.to_graph6(),
            "gamma_below_eternal",
        )
        action, raw_graph6, canonical_graph6, mapping = _validate_origin(
            expected, row
        )
        self.assertEqual(action, row[5])
        self.assertEqual(raw_graph6, row[6])
        self.assertEqual(canonical_graph6, row[7])
        self.assertEqual(raw.relabeled(mapping), canonical)

    def test_origin_reconstruction_detects_wrong_action_raw_and_key(self) -> None:
        expected = _expected_origins(self.seeds)[1]
        _, seed, pair_index, first, second = expected
        seed_graph = Graph.from_graph6(seed.graph6)
        raw = seed_graph.toggled(first, second).to_graph6()
        action = "delete" if seed_graph.has_edge(first, second) else "add"
        base = [
            seed.index,
            seed.seed_id,
            pair_index,
            first,
            second,
            action,
            raw,
            raw,
            "gamma_below_eternal",
        ]
        wrong = list(base)
        wrong[5] = "add" if action == "delete" else "delete"
        with self.assertRaises(AuditError):
            _validate_origin(expected, wrong)
        wrong = list(base)
        wrong[6] = seed.graph6
        with self.assertRaises(AuditError):
            _validate_origin(expected, wrong)
        wrong = list(base)
        wrong[7] = seed.graph6
        with self.assertRaises(AuditError):
            _validate_origin(expected, wrong)

    def test_receipt_chain_binds_every_field(self) -> None:
        initial = hashlib.sha256(
            b"gamma-theta-edge-toggle-origin-chain-v1\0"
        ).hexdigest()
        fields = {
            "global_index": 0,
            "seed_index": 0,
            "seed_id": "ET-0001",
            "pair_index": 0,
            "first": 0,
            "second": 1,
            "action": "add",
            "raw_graph6": "A_",
            "canonical_graph6": "A_",
            "category": "gamma_below_eternal",
            "mapping": (0, 1),
        }
        baseline = _chain_step(initial, **fields)
        changed = dict(fields)
        changed["pair_index"] = 1
        self.assertNotEqual(baseline, _chain_step(initial, **changed))
        changed = dict(fields)
        changed["mapping"] = (1, 0)
        self.assertNotEqual(baseline, _chain_step(initial, **changed))

    def test_seed_byte_pin_rejects_modified_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            modified = Path(temporary) / "extensions_unique.csv"
            modified.write_bytes(self.paths.seed_input.read_bytes() + b"\n")
            paths = replace(self.paths, seed_input=modified)
            with self.assertRaisesRegex(AuditError, "seed table differs"):
                load_seed_universe(paths)

    def test_checker_has_no_forbidden_imports(self) -> None:
        forbidden = {
            "search",
            "verifier_a",
            "verifier_b",
            "coverage_checker",
        }
        package = CAMPAIGN / "src" / "edge_toggle_coverage_checker"
        for path in package.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = {alias.name.split(".")[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = {node.module.split(".")[0]}
                else:
                    continue
                self.assertFalse(
                    names & forbidden,
                    f"forbidden import in {path.name}: {names & forbidden}",
                )


if __name__ == "__main__":
    unittest.main()
