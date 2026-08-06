#!/usr/bin/env python3
"""Deterministic calibrations for the global finite-episode Foster selector."""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Reaction  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.uniformization import select_episode  # type: ignore  # noqa:E402


def calibration_report() -> dict[str, object]:
    report: dict[str, object] = {}

    # 0 -> A+B -> B -> 0, evaluated after the B->0 return.
    stress = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    stress_rows = []
    for n in (10, 30, 100, 300, 1000):
        chosen = select_episode(stress, (n, 0), (0, 0))
        stress_rows.append((n, chosen.terminal, chosen.expected_drift))
    if not all(row[2] < 0 for row in stress_rows[1:]):
        raise AssertionError("canonical stress selector did not become negative")
    report["canonical_trigger_drain"] = stress_rows

    # Immigration-linear death 0 <-> A.
    immigration = (
        Reaction((0,), (1,), Fraction(7)),
        Reaction((1,), (0,), Fraction(2)),
    )
    imm_rows = []
    for n in (10, 100, 1000):
        chosen = select_episode(immigration, (n,), (0,))
        imm_rows.append((n, chosen.terminal, chosen.expected_drift))
    if not all(row[2] < 0 for row in imm_rows):
        raise AssertionError("immigration-death calibration failed")
    report["immigration_linear_death"] = imm_rows

    # Several top types and a regenerated service defect.
    typed = (
        Reaction((0, 0, 0), (1, 0, 1), Fraction(2)),  # 0 -> A+D
        Reaction((1, 0, 1), (0, 1, 1), Fraction(3)),  # A+D -> B+D
        Reaction((0, 1, 1), (0, 0, 1), Fraction(5)),  # B+D -> D
        Reaction((0, 0, 1), (0, 0, 0), Fraction(7)),  # D -> 0
    )
    typed_rows = []
    for n in (20, 100, 500):
        # Residual contains both I types; target 0 is present.
        chosen = select_episode(typed, (n, n, 0), (0, 0, 0))
        typed_rows.append((n, chosen.terminal, chosen.expected_drift))
    if not all(row[2] < 0 for row in typed_rows):
        raise AssertionError("multi-type calibration failed")
    report["several_I_types"] = typed_rows
    return report


def write_report(path: str | Path) -> dict[str, object]:
    report = calibration_report()
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def self_test() -> None:
    calibration_report()


if __name__ == "__main__":
    print(json.dumps(calibration_report(), indent=2, sort_keys=True))
