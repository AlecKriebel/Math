#!/usr/bin/env python3
"""Run final-v3 frozen tests that do not mutate repository source files."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
TEST_FILE = CAMPAIGN / "tests/test_order13_k3_production.py"
EXCLUDED = {
    "test_transitive_helper_source_mutations_refuse_before_child",
}
EXPECTED_SELECTED_COUNT = 22


def main() -> int:
    specification = importlib.util.spec_from_file_location(
        "order13_k3_production_final_v3_tests", TEST_FILE
    )
    if specification is None or specification.loader is None:
        raise AssertionError("could not load final-v3 frozen tests")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    test_class = module.Order13K3ProductionTests
    names = sorted(
        name
        for name in unittest.defaultTestLoader.getTestCaseNames(test_class)
        if name not in EXCLUDED
    )
    if len(names) != EXPECTED_SELECTED_COUNT:
        raise AssertionError(
            f"selected {len(names)} tests, expected {EXPECTED_SELECTED_COUNT}"
        )
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite(test_class(name) for name in names)
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
