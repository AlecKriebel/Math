#!/usr/bin/env python3
"""Run the original symbolic regression and negative-control suites honestly."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUITES = (
    ("symbolic_regression", "test_core_exact"),
    ("negative_controls", "test_core_mutations"),
)


def main() -> None:
    summaries = []
    failed = False
    for role, module_name in SUITES:
        module = importlib.import_module(module_name)
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        result = unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(suite)
        summary = {
            "errors": len(result.errors),
            "failures": len(result.failures),
            "module": f"{module_name}.py",
            "role": role,
            "skipped": len(result.skipped),
            "tests_run": result.testsRun,
        }
        summaries.append(summary)
        if result.errors or result.failures or result.skipped:
            failed = True

    report = {
        "completion_marker": "CORE_REGRESSION_AND_NEGATIVE_CONTROLS_PASS",
        "status": "FAIL" if failed else "PASS",
        "suites": summaries,
        "total_tests": sum(item["tests_run"] for item in summaries),
    }
    (ROOT / "certificates").mkdir(exist_ok=True)
    (ROOT / "certificates/core_test_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    if failed:
        raise SystemExit(1)
    print(report["completion_marker"])


if __name__ == "__main__":
    main()
