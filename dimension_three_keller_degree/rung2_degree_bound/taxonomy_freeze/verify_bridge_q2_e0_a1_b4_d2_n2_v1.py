#!/usr/bin/env python3
"""Fail-closed exact replay for the post-freeze conic-double-cover bridge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RUNG = HERE.parent

EXPECTED_HASHES = {
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    RUNG / "WORKING_CONIC_DOUBLE_COVER_EXIT.md":
        "087f682b708e3c339eb6f315d517e861fac8af1a8d754620520da0cb76cedbad",
    RUNG / "verify_conic_double_cover_exit_sympy.py":
        "884b37ffd54c4f27f834139cefd6ce345548f4f24f376f967201572537060577",
    RUNG / "audit_conic_double_cover_hostile" / "RESEARCH_LOG.md":
        "d4b97d26ddf01d707132b7ded678a22b0da686e8448a8047f42b117091240f91",
    RUNG / "audit_conic_double_cover_hostile" /
    "audit_conic_double_cover_pari.gp":
        "bed2c80f1b73dcc92aac81e21148bf6cfa4584feea4a240dfef2e655c5985b33",
    RUNG / "audit_conic_double_cover_hostile" /
    "audit_conic_double_cover_pari_strict.sh":
        "5d151bff683bc86963844d984df4093e2b6f6404098799589a406569b640f30f",
}

EXPECTED_MONOMIALS = [
    "x^4", "x^3*y", "x^3*z", "x^2*y^2", "x^2*y*z",
    "x^2*z^2", "x*y^3", "x*y^2*z", "x*y*z^2", "x*z^3",
    "y^4", "y^3*z", "y^2*z^2", "y*z^3", "z^4",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    require(__debug__, "refusing optimized Python: fail-closed checks required")

    for path, expected in EXPECTED_HASHES.items():
        require(digest(path) == expected, f"pinned-input hash mismatch: {path}")

    manifest = json.loads((HERE / "frozen_manifest_v1.json").read_text())
    require(manifest["version"] == 1, "wrong freeze version")
    require(manifest["frozen_row_count"] == 14, "wrong frozen denominator")
    require(
        manifest["coefficient_order"]["degree_four_monomials"]
        == EXPECTED_MONOMIALS,
        "wrong frozen monomial order",
    )
    require(
        manifest["pivot_ids"] == [f"C{i:02d}" for i in range(45)],
        "pivot IDs are not exactly C00--C44",
    )

    matches = [
        row for row in manifest["rows"]
        if row["id"] == "Q2-E0-A1-B4-D2-N2"
    ]
    require(len(matches) == 1, "target frozen row missing or duplicated")
    row = matches[0]
    require(row["rank"] == 2, "target row has wrong rank")
    require(row["tuple"] == [0, 1, 4, 2, 2], "target tuple mismatch")

    # Canonical leading triple: primitive, rank two, and on a nondegenerate
    # conic.  These checks reconstruct the endpoint of the geometric bridge.
    x, y, z = sp.symbols("x y z")
    h = sp.Matrix([x**4, x**2 * y**2, y**4])
    require(sp.gcd(sp.gcd(h[0], h[1]), h[2]) == 1, "canonical gcd is not one")
    require(sp.expand(h[1] ** 2 - h[0] * h[2]) == 0, "conic relation failed")
    jac = h.jacobian([x, y, z])
    require(jac.rank() == 2, "canonical Jacobian does not have rank two")
    require(
        sp.expand(jac.extract([0, 2], [0, 1]).det()) != 0,
        "canonical rank-two minor vanished",
    )

    # Every PGL2 automorphism of the parameter line lifts invertibly to the
    # conic.  Reconstruct the determinant identity exactly.
    a, b, c, d = sp.symbols("a b c d")
    sym2 = sp.Matrix([
        [a**2, 2 * a * b, b**2],
        [a * c, a * d + b * c, b * d],
        [c**2, 2 * c * d, d**2],
    ])
    require(
        sp.expand(sym2.det() - (a * d - b * c) ** 3) == 0,
        "symmetric-square determinant identity failed",
    )

    # The pivot partition has three blocks of fifteen.  Since a conic image
    # spans P^2, its component triple is linearly independent; hence its
    # first component is nonzero and the first pivot is in C00--C14.
    require(len(EXPECTED_MONOMIALS) == 15, "wrong component block size")
    possible_first_component_pivots = [f"C{i:02d}" for i in range(15)]
    forced_empty_later_pivots = [f"C{i:02d}" for i in range(15, 45)]
    require(
        possible_first_component_pivots + forced_empty_later_pivots
        == manifest["pivot_ids"],
        "pivot block routing does not cover the frozen partition",
    )

    bridge = (HERE / "BRIDGE_Q2_E0_A1_B4_D2_N2_v1.md").read_text()
    for token in (
        "R/\\mathrm C_{00}",
        "R/\\mathrm C_{14}",
        "R/\\mathrm C_{15}",
        "R/\\mathrm C_{44}",
        "\\det\\operatorname{Sym}^2(M)=(\\det M)^3",
        "never divides by the first nonzero frozen coefficient",
    ):
        require(token in bridge, f"bridge coverage token missing: {token}")

    print("PASS: frozen conic-double-cover bridge and pinned exact inputs")


if __name__ == "__main__":
    main()
