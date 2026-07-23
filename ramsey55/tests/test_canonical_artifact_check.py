#!/usr/bin/env python3
"""Adversarial tests for the independent canonical artifact validator."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from canonical_artifact_check import validate_bytes  # noqa: E402


ARTIFACTS = (
    ROOT / "data" / "exoo42_constructed.canonical.json",
    ROOT / "results" / "best_candidates" / "exoo_seed_20260724.canonical.json",
)


def serialize(document: Any) -> bytes:
    return (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")


class CanonicalArtifactCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = json.loads(ARTIFACTS[0].read_text(encoding="utf-8"))

    def assert_tamper_fails(
        self, mutation: Any, expected_failed_check: str
    ) -> dict[str, Any]:
        changed = copy.deepcopy(self.source)
        mutation(changed)
        report = validate_bytes(serialize(changed), "tampered")
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"][expected_failed_check])
        return report

    def test_both_recorded_artifacts_pass_every_check(self) -> None:
        for path in ARTIFACTS:
            with self.subTest(path=path.name):
                report = validate_bytes(path.read_bytes(), str(path))
                self.assertEqual(report["status"], "PASS", report["errors"])
                self.assertTrue(all(report["checks"].values()))

    def test_tampered_graph6_is_detected(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            payload = bytearray(document["graph6"].encode("ascii"))
            payload[1] = 63 + ((payload[1] - 63) ^ 32)
            document["graph6"] = payload.decode("ascii")

        self.assert_tamper_fails(mutate, "adjacency_list_matches_graph6")

    def test_tampered_adjacency_list_is_detected(self) -> None:
        self.assert_tamper_fails(
            lambda document: document["adjacency_list"][0].pop(),
            "adjacency_list_matches_graph6",
        )

    def test_tampered_edge_list_is_detected(self) -> None:
        self.assert_tamper_fails(
            lambda document: document["edge_list"].pop(0),
            "edge_list_matches_graph6",
        )

    def test_tampered_adjacency_matrix_is_detected(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            row = document["adjacency_matrix_rows"][0]
            replacement = "0" if row[1] == "1" else "1"
            document["adjacency_matrix_rows"][0] = (
                row[:1] + replacement + row[2:]
            )

        report = self.assert_tamper_fails(
            mutate, "adjacency_matrix_matches_graph6"
        )
        self.assertFalse(report["checks"]["adjacency_matrix_symmetric"])

    def test_tampered_edge_count_is_detected(self) -> None:
        self.assert_tamper_fails(
            lambda document: document.__setitem__(
                "edge_count", document["edge_count"] + 1
            ),
            "edge_count_matches_graph6",
        )

    def test_tampered_degree_sequence_is_detected(self) -> None:
        self.assert_tamper_fails(
            lambda document: document["degree_sequence"].__setitem__(
                0, document["degree_sequence"][0] - 1
            ),
            "degree_sequence_matches_graph6",
        )

    def test_tampered_n_is_detected(self) -> None:
        self.assert_tamper_fails(
            lambda document: document.__setitem__("n", document["n"] + 1),
            "n_matches_graph6",
        )

    def test_loop_and_asymmetry_are_detected(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["adjacency_list"][0].insert(0, 0)

        self.assert_tamper_fails(mutate, "adjacency_list_well_formed")

    def test_noncanonical_edge_order_is_detected(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            document["edge_list"][0], document["edge_list"][1] = (
                document["edge_list"][1],
                document["edge_list"][0],
            )

        self.assert_tamper_fails(mutate, "edge_list_well_formed")

    def test_noncanonical_json_serialization_is_detected(self) -> None:
        raw = json.dumps(self.source, separators=(",", ":")).encode("utf-8")
        report = validate_bytes(raw, "noncanonical")
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["canonical_json_serialization"])
        self.assertTrue(report["checks"]["adjacency_list_matches_graph6"])

    def test_duplicate_json_key_is_detected(self) -> None:
        raw = b'{"schema":"ramsey55.graph.v1","schema":"duplicate"}\n'
        report = validate_bytes(raw, "duplicate-key")
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["json_parse_and_unique_keys"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
