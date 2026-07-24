#!/usr/bin/env python3
"""Tests for the independent incident-LNS candidate acceptance checker."""

from __future__ import annotations

import argparse
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from incident_lns_candidate_check import graph6_line, run  # noqa: E402

BASE = ROOT / "results" / "best_candidates" / "exoo_seed_20260724.g6"
METADATA = ROOT / "certificates" / "residual_lns_incident_six.metadata.json"
CNF = ROOT / "certificates" / "residual_lns_incident_six.cnf"
CHECKER = ROOT / "verify" / "incident_lns_candidate_check.py"
INCIDENT = "3,4,7,38,41,42"


def encode_graph6(adjacency: list[int]) -> str:
    n = len(adjacency)
    bits: list[int] = []
    for right in range(1, n):
        for left in range(right):
            bits.append((adjacency[left] >> right) & 1)
    while len(bits) % 6:
        bits.append(0)
    payload = "".join(
        chr(63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6)))
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + n) + payload


def flip_edge(adjacency: list[int], left: int, right: int) -> None:
    adjacency[left] ^= 1 << right
    adjacency[right] ^= 1 << left


class IncidentLnsCandidateCheckTests(unittest.TestCase):
    def run_checker(
        self,
        candidate: Path,
        *extra: str,
        base: Path = BASE,
        metadata: Path = METADATA,
        incident: str = INCIDENT,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                str(candidate),
                "--base",
                str(base),
                "--metadata",
                str(metadata),
                "--incident-vertices",
                incident,
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def small_fixture(
        self, directory: Path
    ) -> tuple[Path, Path, list[int]]:
        adjacency = [0] * 6
        base = directory / "base.g6"
        base.write_text(encode_graph6(adjacency) + "\n", encoding="ascii")
        incident = {0, 1}
        free_edges = [
            [left, right]
            for left in range(6)
            for right in range(left + 1, 6)
            if left in incident or right in incident
        ]
        metadata = directory / "metadata.json"
        metadata.write_text(
            json.dumps(
                {
                    "base_file_sha256": hashlib.sha256(base.read_bytes()).hexdigest(),
                    "base_graph6": graph6_line(base),
                    "variable_count": len(free_edges),
                    "free_edges": free_edges,
                    "base_true_variables": [],
                }
            ),
            encoding="utf-8",
        )
        return base, metadata, adjacency

    def test_production_base_rejected_only_as_invalid_candidate(self) -> None:
        completed = self.run_checker(BASE, "--cnf", str(CNF))
        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["metadata_valid"])
        self.assertTrue(result["cnf_metadata_valid"])
        self.assertTrue(result["fixed_boundary_valid"])
        self.assertEqual(result["expected_free_edge_count"], 237)
        self.assertEqual(result["changed_edge_count"], 0)
        self.assertEqual(result["clique_count"], 0)
        self.assertEqual(result["independent_count"], 2)
        self.assertEqual(result["cnf_unsatisfied_clause_count"], 2)
        self.assertFalse(result["accepted"])

    def test_free_edge_change_preserves_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base, metadata, adjacency = self.small_fixture(root)
            flip_edge(adjacency, 0, 2)
            candidate = root / "free-change.g6"
            candidate.write_text(encode_graph6(adjacency) + "\n", encoding="ascii")
            completed = self.run_checker(
                candidate, base=base, metadata=metadata, incident="0,1"
            )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["fixed_boundary_valid"])
        self.assertEqual(result["changed_free_edge_count"], 1)
        self.assertEqual(result["changed_fixed_edge_count"], 0)

    def test_fixed_edge_change_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base, metadata, adjacency = self.small_fixture(root)
            flip_edge(adjacency, 2, 3)
            candidate = root / "fixed-change.g6"
            candidate.write_text(encode_graph6(adjacency) + "\n", encoding="ascii")
            completed = self.run_checker(
                candidate, base=base, metadata=metadata, incident="0,1"
            )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["fixed_boundary_valid"])
        self.assertEqual(result["changed_fixed_edge_count"], 1)
        self.assertEqual(result["changed_fixed_edges"], [[2, 3]])

    def test_wrong_incident_set_is_a_metadata_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base, metadata, _ = self.small_fixture(root)
            result = run(
                argparse.Namespace(
                    base=base,
                    candidate=base,
                    metadata=metadata,
                    cnf=None,
                    search_json=None,
                    incident_vertices="0",
                    k=5,
                    base_line=1,
                    candidate_line=1,
                )
            )
        self.assertFalse(result["metadata_valid"])
        self.assertFalse(result["metadata_checks"]["free_edges_exactly_expected"])

    def test_search_stdout_crosscheck_detects_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base, metadata, _ = self.small_fixture(root)
            search_json = root / "search.json"
            record = {
                "mode": "search",
                "algorithm": "incident_six_lns_v1",
                "graph6": graph6_line(base),
                "C5": 0,
                "I5": 6,
                "E": 6,
                "edge_count": 0,
                "degree_sequence": [0] * 6,
                "free_edge_count": 9,
                "fixed_edge_count": 6,
                "fixed_edges_preserved": True,
                "changed_free_edges": 0,
            }
            search_json.write_text(json.dumps(record), encoding="utf-8")
            arguments = argparse.Namespace(
                base=base,
                candidate=base,
                metadata=metadata,
                cnf=None,
                search_json=search_json,
                incident_vertices="0,1",
                k=5,
                base_line=1,
                candidate_line=1,
            )
            self.assertTrue(run(arguments)["search_output_valid"])
            record["E"] = 5
            search_json.write_text(json.dumps(record), encoding="utf-8")
            mismatched = run(arguments)
        self.assertFalse(mismatched["search_output_valid"])
        self.assertFalse(mismatched["search_output_checks"]["E"])


if __name__ == "__main__":
    unittest.main()
