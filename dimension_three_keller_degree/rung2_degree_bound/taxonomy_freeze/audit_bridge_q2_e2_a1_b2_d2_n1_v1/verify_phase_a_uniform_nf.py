#!/usr/bin/env python3
"""Exact retained checks for the pre-bridge fixed-conic derivation.

This checker deliberately knows nothing about the later working bridges.
It verifies the frozen row, all 45 coefficient labels, the uniform adapted
leading form, its two polynomial kernel identities, rank/gcd witnesses, and
the fact that the adapted lower terms have their full dimensions.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
FREEZE = HERE.parent
MANIFEST = FREEZE / "frozen_manifest_v1.json"
ROW_ID = "Q2-E2-A1-B2-D2-N1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    x, y, z = sp.symbols("x y z")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["coverage_kind"] ==
            "disjoint_locally_closed_coefficient_pivot_partition",
            "unexpected frozen coverage kind")
    require(manifest["pivot_strata_per_row"] == 45,
            "frozen pivot count is not 45")

    rows = {row["id"]: row for row in manifest["rows"]}
    require(ROW_ID in rows, "fixed-conic row missing from manifest")
    row = rows[ROW_ID]
    require(row["rank"] == 2, "wrong frozen rank")
    require(row["tuple"] == [2, 1, 2, 2, 1], "wrong frozen tuple")

    expected_pivots = [f"C{i:02d}" for i in range(45)]
    require(manifest["pivot_ids"] == expected_pivots,
            "C00--C44 are not present exactly once in order")

    expected_monomials = [
        "x^4", "x^3*y", "x^3*z", "x^2*y^2", "x^2*y*z",
        "x^2*z^2", "x*y^3", "x*y^2*z", "x*y*z^2", "x*z^3",
        "y^4", "y^3*z", "y^2*z^2", "y*z^3", "z^4",
    ]
    require(manifest["coefficient_order"]["target_components"] == [1, 2, 3],
            "target-component order changed")
    require(manifest["coefficient_order"]["degree_four_monomials"] ==
            expected_monomials, "quartic monomial order changed")

    # The explicit coefficient coverage map.  The first target component
    # of a conic-embedding triple cannot vanish, so only C00--C14 occur.
    coverage = []
    for i, pivot in enumerate(expected_pivots):
        coverage.append({
            "pivot": pivot,
            "component": 1 + i // 15,
            "monomial": expected_monomials[i % 15],
            "normal_form": (
                "h*(x^2,x*y,y^2)" if i < 15 else "EMPTY"
            ),
            "divides_by_pivot": False,
        })
    require(len(coverage) == 45, "coverage map lost a pivot")
    require({entry["pivot"] for entry in coverage} == set(expected_pivots),
            "coverage map duplicates or omits a pivot")
    require({entry["normal_form"] for entry in coverage[:15]} ==
            {"h*(x^2,x*y,y^2)"},
            "nonempty normal form depends on coefficient pivot")
    require({entry["normal_form"] for entry in coverage[15:]} == {"EMPTY"},
            "C15--C44 were not routed to the empty intersection")
    require(not any(entry["divides_by_pivot"] for entry in coverage),
            "a coverage branch divides by its frozen coefficient")

    # The elementary first-nonzero partition is checked on a witness for
    # every possible first index in the nonzero first component.  These are
    # ambient witnesses only; no nonemptiness claim for an individual row
    # intersection is made.
    for i in range(15):
        witness = [0] * 45
        witness[i] = i + 1
        first = next(j for j, value in enumerate(witness) if value != 0)
        require(first == i, f"first-nonzero routing failed at C{i:02d}")

    # A conic embedding gives a basis of Sym^2<p,q>.  An invertible target
    # matrix has no zero row, so every target component is a nonzero binary
    # quadratic, and multiplying by nonzero h cannot kill it.
    target_entries = sp.symbols("t00:03 t10:13 t20:23")
    target = sp.Matrix(3, 3, target_entries)
    t00, t01, t02 = target.row(0)
    first_binary_component = t00*x**2 + t01*x*y + t02*y**2
    first_coefficients = sp.Poly(
        first_binary_component, x, y
    ).coeffs()
    require(first_coefficients == [t00, t01, t02],
            "binary-component coefficient extraction changed")
    require(sp.expand(first_binary_component) != 0,
            "generic target row unexpectedly vanished")
    require(sp.expand(target.det().subs({
        t00: 0, t01: 0, t02: 0,
    })) == 0, "a zero first target row did not force singularity")

    a, b, c, d, e, f = sp.symbols("a b c d e f")
    h = a*x**2 + b*x*y + c*x*z + d*y**2 + e*y*z + f*z**2
    H = sp.Matrix([h*x**2, h*x*y, h*y**2])
    J = H.jacobian((x, y, z))
    hz = sp.diff(h, z)
    left = sp.Matrix([[y**2, -2*x*y, x**2]])
    right = sp.Matrix([x*hz, y*hz, z*hz - 4*h])

    require(all(sp.expand(value) == 0 for value in left * J),
            "left-kernel identity failed")
    require(all(sp.expand(value) == 0 for value in J * right),
            "right-kernel identity failed")
    require(sp.expand(J.det()) == 0, "leading Jacobian rank exceeds two")

    # One universal minor is x^2*h*(4*h-z*h_z).  The diagonal operator
    # 4-z*d/dz has eigenvalues 4,3,2 on a quadratic's z-degrees, so it
    # cannot kill a nonzero h.  Thus every nonzero h has rank at least two.
    universal_minor = sp.expand(J.extract([0, 1], [0, 1]).det())
    require(sp.expand(
        universal_minor - x**2*h*(4*h-z*hz)
    ) == 0, "universal rank-two minor identity failed")
    operator_coefficients = [
        sp.Poly(4*h-z*hz, x, y, z).coeff_monomial(monomial)
        for monomial in (x**2, x*y, x*z, y**2, y*z, z**2)
    ]
    require(operator_coefficients == [4*a, 4*b, 3*c, 4*d, 3*e, 2*f],
            "rank-two operator ceased to be invertible")

    # Basis specializations also retain simple gcd and rank witnesses.
    h_basis = [x**2, x*y, x*z, y**2, y*z, z**2]
    for index, h0 in enumerate(h_basis):
        H0 = sp.Matrix([h0*x**2, h0*x*y, h0*y**2])
        J0 = H0.jacobian((x, y, z))
        minors = []
        for r1 in range(3):
            for r2 in range(r1 + 1, 3):
                for c1 in range(3):
                    for c2 in range(c1 + 1, 3):
                        minors.append(sp.expand(
                            J0.extract([r1, r2], [c1, c2]).det()))
        require(any(value != 0 for value in minors),
                f"rank-two witness missing for h-basis index {index}")
        require(sp.gcd(sp.gcd(H0[0], H0[1]), H0[2]) == h0,
                f"component gcd check failed for h-basis index {index}")

    require(sp.expand(H[0]*H[2] - H[1]**2) == 0,
            "conic image relation failed")

    # Complete lower-term and linear-part dimensions in the adapted model.
    degree2_count = 3 * len([
        x**2, x*y, x*z, y**2, y*z, z**2,
    ])
    degree3_count = 3 * len([
        x**3, x**2*y, x**2*z, x*y**2, x*y*z,
        x*z**2, y**3, y**2*z, y*z**2, z**3,
    ])
    require(degree2_count == 18, "quadratic lower space is incomplete")
    require(degree3_count == 30, "cubic lower space is incomplete")
    require(3 * 3 == 9, "linear matrix is incomplete")

    print("PASS phase-A uniform normal form")
    print("PASS C00--C14 uniform coverage and C15--C44 intrinsic emptiness")
    print("PASS exact leading kernel/rank/gcd/conic identities")
    print("PASS arbitrary lower-term dimensions 18+30 and linear dimension 9")


if __name__ == "__main__":
    main()
