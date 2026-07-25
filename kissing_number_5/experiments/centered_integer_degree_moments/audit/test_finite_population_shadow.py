#!/usr/bin/env python3
"""Tamper tests for the finite-population incidence shadows."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .verify_finite_population_shadow import ROOT, verify


AUDIT = Path(__file__).resolve().parent
CERTIFICATE = AUDIT / "finite_population_shadow.json"
SOURCE = (
    ROOT
    / "experiments"
    / "centered_integer_degree_moments"
    / "repaired_pair_triple_local_3.json"
)


class FinitePopulationShadowTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(
            result["finite_incidence_shadow"]["feasible_triangle_counts"],
            10660,
        )
        self.assertEqual(
            result["graphical_degree_shadow"]["complete_graph_edges_colored"],
            820,
        )

    def test_tampered_triangle_count_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        section = certificate["finite_row_triangle_incidence_shadow"]
        section["feasible_triangle_orbit_counts"][4] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)

    def test_tampered_edge_color_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        graph = certificate["separate_colored_complete_graph_degree_shadow"]
        graph["edge_colors"][0][2] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)


if __name__ == "__main__":
    unittest.main()
