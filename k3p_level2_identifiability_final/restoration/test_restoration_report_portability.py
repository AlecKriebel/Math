#!/usr/bin/env python3
"""Regression: the generated restoration report is relocation invariant."""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import regenerate_k3p_restoration as producer  # noqa: E402


class PortabilityFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PortabilityFailure(message)


def main() -> int:
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    manifest = json.loads((HERE / "RESTORATION_MANIFEST.json").read_text())
    original_here = producer.HERE
    baseline = producer.theorem_report(manifest)
    try:
        producer.HERE = Path("/relocated/workspace/with/a/different/path/restoration")
        relocated = producer.theorem_report(manifest)
    finally:
        producer.HERE = original_here

    require(baseline == relocated, "report bytes depend on workspace location")
    require(str(original_here) not in baseline, "absolute source path embedded in report")
    require("/relocated/workspace" not in baseline, "absolute relocated path embedded in report")
    require("cd restoration" in baseline, "relative reproduction command missing")
    require(baseline == (HERE / "K3P_RESTORATION_THEOREM_REPORT.md").read_text(),
            "sealed report differs from canonical renderer")
    print("K3P_RESTORATION_REPORT_PORTABILITY_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PortabilityFailure, KeyError, OSError, ValueError) as error:
        raise SystemExit(f"K3P_RESTORATION_REPORT_PORTABILITY_FAIL:{error}") from error
