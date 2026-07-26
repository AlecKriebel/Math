#!/usr/bin/env python3
"""Fail-closed binding of the hostile audit to the candidate release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", choices=("contract",))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    release = here.parent / "d3_construction_search"
    primary = (release / "verify_ansatz_obstructions.py").read_text()
    pari = (release / "verify_independent_pari.gp").read_text()
    strict = (release / "verify_strict.sh").read_text()
    note = (release / "NOTE.md").read_text()
    scope = json.loads((release / "SCOPE.json").read_text())

    primary_r2_call = "verify_r2_kernel_zero(alpha, beta, label)"
    if args.mutation == "contract":
        primary_r2_call = "verify_r2_kernel_zero_is_missing(alpha, beta, label)"
    require(primary_r2_call in primary, "primary calls zero-r2-kernel check")
    require(
        "for degree in (9, 8, 7)" in primary
        and '"BB full E9/E8/E7 identities"' in primary,
        "primary explicitly replays E9/E8/E7",
    )
    require(
        '"BB zero r2-kernel first pivot"' in pari
        and '"BB zero r2-kernel second pivot"' in pari,
        "PARI independently replays zero-r2 pivots",
    )
    require(
        '"BB full arbitrary-binary E9"' in pari
        and '"BB full arbitrary-binary E8"' in pari
        and '"BB full arbitrary-binary E7"' in pari,
        "PARI explicitly replays E9/E8/E7",
    )
    require(
        "grep -Ei" in strict
        and "syntax error" in strict
        and "skipping file" in strict
        and "independent PARI emitted an interpreter error" in strict,
        "release wrapper rejects PARI interpreter errors",
    )
    require(
        "D3-BB-21" in scope["full_counterexample_exclusions"],
        "scope includes the audited BB21 exclusion",
    )
    require(
        "D3-BB-21 cannot contain a Keller counterexample" in note,
        "human note states exact family scope",
    )
    require(
        "does not by itself close the quartic row" in note
        or "no quartic-row exclusion" in note
        or (
            "This package does not claim:" in note
            and "a quartic-row exclusion or a new global degree bound" in note
        ),
        "human note disclaims global row closure",
    )
    print("D3_BB21_RELEASE_BINDING_PASS")


if __name__ == "__main__":
    main()
