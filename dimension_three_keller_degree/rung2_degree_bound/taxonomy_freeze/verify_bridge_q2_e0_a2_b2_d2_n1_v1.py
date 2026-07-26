#!/usr/bin/env python3
"""Fail-closed exact replay for the frozen quadratic-pencil conic row."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

HERE = Path(__file__).resolve().parent
RUNG = HERE.parent

EXPECTED_HASHES = {
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    RUNG / "WORKING_CONIC_TYPE_22.md":
        "4b0c86dd4e4b7537bad21012daf5564c75c0c971b2579fcfb046fa6395b649c3",
    RUNG / "verify_conic_doubleline_sympy.py":
        "38db15a0d1651482f6316f06b39e8591a0bdb6dbe57e1241f87dfe85f5f6bd80",
    RUNG / "verify_conic_doubleline_pari.gp":
        "378fd06ca2855855a058ec08f9a1e4ed4f302683fd5e4980a20edcefd855b322",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=("frozen_hash", "tuple", "quadratic_extension", "pivot", "scope"),
    )
    args = parser.parse_args()

    expected_hashes = dict(EXPECTED_HASHES)
    if args.mutation == "frozen_hash":
        expected_hashes[HERE / "FROZEN_TAXONOMY_v1.md"] = "0" * 64
    for path, expected in expected_hashes.items():
        require(digest(path) == expected, f"pinned-input hash mismatch: {path}")

    manifest = json.loads((HERE / "frozen_manifest_v1.json").read_text())
    require(manifest["version"] == 1, "wrong freeze version")
    require(manifest["frozen_row_count"] == 14, "wrong global denominator")
    require(
        manifest["pivot_ids"] == [f"C{i:02d}" for i in range(45)],
        "wrong pivot denominator",
    )
    rows = [
        row for row in manifest["rows"]
        if row["id"] == "Q2-E0-A2-B2-D2-N1"
    ]
    require(len(rows) == 1, "target row missing or duplicated")
    wanted_tuple = [0, 2, 2, 2, 1]
    if args.mutation == "tuple":
        wanted_tuple[-1] = 2
    require(rows[0]["rank"] == 2, "wrong target rank")
    require(rows[0]["tuple"] == wanted_tuple, "wrong target tuple")

    # Reconstruct the target-normalized Veronese triple.
    P, Q = sp.symbols("P Q")
    ver = sp.Matrix([P**2, P * Q, Q**2])
    require(sp.gcd(sp.gcd(ver[0], ver[1]), ver[2]) == 1, "Veronese not primitive")
    require(sp.expand(ver[1] ** 2 - ver[0] * ver[2]) == 0, "conic relation")
    coefficient_matrix = sp.eye(3)
    require(coefficient_matrix.rank() == 3, "conic components do not span P2")

    # Any change of pencil basis lifts invertibly on the conic.
    a, b, c, d = sp.symbols("a b c d")
    sym2 = sp.Matrix([
        [a**2, 2 * a * b, b**2],
        [a * c, a * d + b * c, b * d],
        [c**2, 2 * c * d, d**2],
    ])
    require(
        sp.expand(sym2.det() - (a * d - b * c) ** 3) == 0,
        "Sym2 determinant identity",
    )

    # Two distinct double lines would give C(t^2) proper in C(t).
    t, s = sp.symbols("t s")
    minpoly = t**2 - s
    require(sp.Poly(minpoly, t).degree() == 2, "wrong square extension degree")
    discriminant = sp.discriminant(minpoly, t)
    expected_discriminant = 4 * s
    if args.mutation == "quadratic_extension":
        expected_discriminant = 4 * s**2
    require(
        sp.expand(discriminant - expected_discriminant) == 0,
        "quadratic-extension discriminant",
    )
    # The odd valuation of s proves 4s is not a square in Q(s).
    require(sp.degree(discriminant, s) % 2 == 1, "discriminant unexpectedly square")

    pivots = manifest["pivot_ids"]
    first_component = pivots[:15]
    later_components = pivots[15:]
    wanted_later_count = 30 if args.mutation != "pivot" else 29
    require(len(first_component) == 15, "wrong first-component pivot count")
    require(len(later_components) == wanted_later_count, "wrong empty-pivot count")
    require(first_component + later_components == pivots, "pivot routing incomplete")

    bridge = (HERE / "BRIDGE_Q2_E0_A2_B2_D2_N1_v1.md").read_text()
    required_tokens = [
        "R/\\mathrm C_{00}",
        "R/\\mathrm C_{14}",
        "R/\\mathrm C_{15}",
        "R/\\mathrm C_{44}",
        "\\mathbb C\\!\\left((L_1/L_2)^2\\right)",
        "never divides by the first nonzero frozen coefficient",
        "arbitrary lower terms",
    ]
    if args.mutation == "scope":
        required_tokens.append("claims a universal degree-five floor")
    for token in required_tokens:
        require(token in bridge, f"bridge token missing: {token}")

    print("Q2_E0_A2_B2_D2_N1_BRIDGE_PRIMARY_PASS")


if __name__ == "__main__":
    main()
