"""Calibration tests for discovery-only spherical-code programs."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy.optimize import check_grad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import analyze_refine_coordinates as analyzer
import search_spherical5 as search


class NumericalToolTests(unittest.TestCase):
    def test_d5_calibration(self) -> None:
        points = search.d5()
        self.assertEqual(points.shape, (40, 5))
        gram = points @ points.T
        off_diagonal = gram[np.triu_indices(40, 1)]
        self.assertAlmostEqual(float(np.max(off_diagonal)), 0.5, places=14)
        np.testing.assert_allclose(
            np.sum(points * points, axis=1), 1.0, atol=3e-15, rtol=0
        )
        np.testing.assert_allclose(
            np.linalg.eigvalsh(points.T @ points),
            np.full(5, 8.0),
            atol=3e-14,
            rtol=0,
        )

    def test_smooth_max_gradient(self) -> None:
        rng = np.random.default_rng(7)
        raw = rng.normal(size=35)
        error = check_grad(
            lambda value: search.smoothmax_fun_grad(value, 7, 20.0)[0],
            lambda value: search.smoothmax_fun_grad(value, 7, 20.0)[1],
            raw,
        )
        self.assertLess(error, 2e-6)

    def test_coordinate_parser_both_formats(self) -> None:
        points = search.d5()[:2]
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            line_path = directory_path / "lines.txt"
            token_path = directory_path / "tokens.txt"
            line_path.write_text(
                "\n".join(",".join(map(str, row)) for row in points) + "\n",
                encoding="utf-8",
            )
            token_path.write_text(
                " ".join(",".join(map(str, row)) for row in points),
                encoding="utf-8",
            )
            parsed_lines, _ = analyzer.read_coordinate_text(line_path)
            parsed_tokens, _ = analyzer.read_coordinate_text(token_path)
        np.testing.assert_array_equal(parsed_lines, points)
        np.testing.assert_array_equal(parsed_tokens, points)


if __name__ == "__main__":
    unittest.main()
