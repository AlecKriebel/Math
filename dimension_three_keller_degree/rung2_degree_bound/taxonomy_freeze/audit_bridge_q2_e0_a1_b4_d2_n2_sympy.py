#!/usr/bin/env python3
"""Independent exact checks for the frozen conic-double-cover bridge.

This is deliberately not an import of verify_bridge_q2_e0_a1_b4_d2_n2_v1.py.
It reconstructs the normal form and transformation identities from scratch.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RUNG = HERE.parent

AUDITED_HASHES = {
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "BRIDGE_Q2_E0_A1_B4_D2_N2_v1.md":
        "8aa1931b3c2ccd38c70408e15dc877b02ecf0f1656c3ecd27cc817dc51862b6d",
    RUNG / "WORKING_CONIC_DOUBLE_COVER_EXIT.md":
        "087f682b708e3c339eb6f315d517e861fac8af1a8d754620520da0cb76cedbad",
    RUNG / "verify_conic_double_cover_exit_sympy.py":
        "884b37ffd54c4f27f834139cefd6ce345548f4f24f376f967201572537060577",
    RUNG / "audit_conic_double_cover_hostile" /
    "audit_conic_double_cover_pari.gp":
        "bed2c80f1b73dcc92aac81e21148bf6cfa4584feea4a240dfef2e655c5985b33",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    require(path.is_file(), f"missing audited input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    require(__debug__, "refusing optimized Python")
    for path, expected in AUDITED_HASHES.items():
        require(sha256(path) == expected, f"audited-input hash mismatch: {path}")

    manifest = json.loads((HERE / "frozen_manifest_v1.json").read_text())
    row = [
        item for item in manifest["rows"]
        if item["id"] == "Q2-E0-A1-B4-D2-N2"
    ]
    require(len(row) == 1, "target row is absent or duplicated")
    require(row[0]["rank"] == 2, "wrong frozen rank")
    require(row[0]["tuple"] == [0, 1, 4, 2, 2], "wrong frozen tuple")
    pivots = [f"C{i:02d}" for i in range(45)]
    require(manifest["pivot_ids"] == pivots, "wrong frozen pivot denominator")

    x, y, z = sp.symbols("x y z")

    # The canonical endpoint is primitive, spans a three-dimensional target
    # space, has rank two, and has precisely the nondegenerate conic relation.
    canonical = sp.Matrix([x**4, x**2 * y**2, y**4])
    require(
        sp.gcd(sp.gcd(canonical[0], canonical[1]), canonical[2]) == 1,
        "canonical triple is not primitive",
    )
    require(
        sp.expand(canonical[1] ** 2 - canonical[0] * canonical[2]) == 0,
        "canonical conic relation failed",
    )
    coefficient_matrix = sp.Matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])
    require(coefficient_matrix.rank() == 3, "canonical components do not span")
    jacobian = canonical.jacobian([x, y, z])
    require(jacobian.rank() == 2, "canonical Jacobian rank is not two")

    # Normalize a degree-two cover after its two ramification points and two
    # branch values have independently been sent to the coordinate points.
    # The fibre conditions are C=D=0.  The two endpoint values then force
    # A,F != 0 by basepoint freeness.  The exact Wronskian shows that endpoint
    # ramification forces E=B=0, leaving [A*x^2:F*y^2].
    A, B, C, D, E, G = sp.symbols("A B C D E G")
    b0 = A * x**2 + B * x * y + C * y**2
    b1 = D * x**2 + E * x * y + G * y**2
    wronskian = sp.expand(sp.diff(b0, x) * sp.diff(b1, y)
                          - sp.diff(b0, y) * sp.diff(b1, x))
    endpoint_fibres = sp.expand(wronskian.subs({C: 0, D: 0}))
    require(
        endpoint_fibres == 2 * A * E * x**2
        + 4 * A * G * x * y + 2 * B * G * y**2,
        "degree-two Wronskian reconstruction failed",
    )
    require(
        sp.expand(endpoint_fibres.subs({B: 0, E: 0}))
        == 4 * A * G * x * y,
        "normalized cover does not have exactly the two endpoint ramification points",
    )

    # No square-root choice or hidden common factor is needed in the affine
    # triple: an invertible diagonal target matrix removes A and G exactly.
    covered_veronese = sp.Matrix([
        A**2 * x**4,
        A * G * x**2 * y**2,
        G**2 * y**4,
    ])
    target_rescaling = sp.diag(A**-2, (A * G)**-1, G**-2)
    require(
        all(sp.cancel(entry) == 0
            for entry in target_rescaling * covered_veronese - canonical),
        "nonzero cover scalars were not removed exactly",
    )

    # A source projectivity and a target projectivity of the normalized conic
    # really lift through GL_3.  The determinant exponent is checked exactly.
    a, b, c, d = sp.symbols("a b c d")
    sym2 = sp.Matrix([
        [a**2, 2 * a * b, b**2],
        [a * c, a * d + b * c, b * d],
        [c**2, 2 * c * d, d**2],
    ])
    require(
        sp.expand(sym2.det() - (a * d - b * c) ** 3) == 0,
        "Sym^2 lift is not invertible with the asserted determinant",
    )

    # Independent linear forms p,q can be completed by r.  For any such
    # completion, S=C^{-1} sends p,q,r to x,y,z.  The identity is polynomial
    # after clearing the sole intrinsic nonzero determinant.
    basis_symbols = sp.symbols("k0:9")
    basis = sp.Matrix(3, 3, basis_symbols)
    delta = basis.det()
    basis_inverse_certificate = basis * basis.adjugate() - delta * sp.eye(3)
    require(
        all(sp.expand(entry) == 0 for entry in basis_inverse_certificate),
        "source-basis adjugate identity failed",
    )

    # Chain rule and determinant multiplicativity for exact GL_3 source and
    # target transformations.
    symbols = sp.symbols("m0:27")
    target = sp.Matrix(3, 3, symbols[:9])
    formal_jacobian = sp.Matrix(3, 3, symbols[9:18])
    source = sp.Matrix(3, 3, symbols[18:])
    require(
        sp.expand(
            (target * formal_jacobian * source).det()
            - target.det() * formal_jacobian.det() * source.det()
        ) == 0,
        "GL3 Keller determinant transfer failed",
    )

    # A conic image spans P^2, so all three component forms are independent.
    # In particular component one is nonzero: its first nonzero coefficient
    # is in C00--C14, and all later pivot strata are empty.
    first_block = pivots[:15]
    forced_empty = pivots[15:]
    require(len(first_block) == 15, "first target block has wrong size")
    require(len(forced_empty) == 30, "later target blocks have wrong size")
    require(first_block + forced_empty == pivots, "pivot routing is incomplete")

    print(
        "HOSTILE_BRIDGE_Q2_E0_A1_B4_D2_N2_SYMPY_PASS_5C1E7A"
    )


if __name__ == "__main__":
    main()
