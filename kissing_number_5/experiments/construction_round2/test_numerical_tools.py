import importlib.util
from pathlib import Path
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROUND2 = load("search_round2")
LINES = load("antipodal_lines")
PAIR_CYCLE = load("pair_cycle_ansatz")


class NumericalToolTests(unittest.TestCase):
    def test_higher_root_sources(self):
        for roots, shape in (
            (ROUND2.d_roots(6), (60, 6)),
            (ROUND2.e6_roots(), (72, 6)),
            (ROUND2.e7_roots(), (126, 7)),
        ):
            self.assertEqual(roots.shape, shape)
            self.assertLess(
                np.max(np.abs(np.sum(roots*roots, axis=1)-1)), 1e-12
            )
            self.assertLessEqual(ROUND2.max_ip(roots), .5+1e-12)

    def test_d5_line_calibration(self):
        lines = LINES.d5_lines()
        self.assertEqual(lines.shape, (20, 5))
        gram = lines @ lines.T
        ii, jj = np.triu_indices(20, 1)
        self.assertLessEqual(np.max(np.abs(gram[ii, jj])), .5+1e-14)

    def test_pair_cycle_start(self):
        parameters, _, _, _ = PAIR_CYCLE.make_initial(0)
        points = PAIR_CYCLE.full_points(parameters)
        self.assertEqual(points.shape, (41, 5))
        self.assertLess(np.max(np.abs(np.sum(points*points, axis=1)-1)), 1e-12)
        self.assertLess(np.max(np.abs(points[:18]+points[18:36])), 1e-12)
        pentagon = points[36:]
        deep = pentagon @ pentagon.T < -.5
        np.fill_diagonal(deep, False)
        self.assertTrue(np.all(np.sum(deep, axis=1) == 2))
        self.assertEqual(int(np.sum(deep)//2), 5)

    def test_pair_cycle_constraint_count(self):
        parameters, _, _, _ = PAIR_CYCLE.make_initial(7)
        values, records = PAIR_CYCLE.target_graph_violations(parameters)
        self.assertEqual(len(values), 506)
        self.assertEqual(len(records), 506)


if __name__ == "__main__":
    unittest.main()
