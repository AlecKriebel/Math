#!/usr/bin/env python3
"""Dependency-free checker for the exported Discovery 07 certificate."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "output" / "unified_every_order.json"


def q_coefficient(m: int) -> Fraction:
    residue = m % 3
    if residue == 0:
        k = m // 3
        return Fraction((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
    if residue == 1:
        k = (m - 1) // 3
        return Fraction(
            (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
            (3 * k + 1) * 2 ** (2 * k + 1),
        )
    k = (m - 2) // 3
    return Fraction((-1) ** k * comb(3 * k + 4, k + 1), 2 ** (2 * k + 3))


def r_coefficient(m: int) -> Fraction:
    residue = m % 3
    if residue == 0:
        k = m // 3
        return Fraction((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
    if residue == 1:
        k = (m - 1) // 3
        return Fraction(
            (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
            (3 * k + 1) * 2 ** (2 * k + 1),
        )
    k = (m - 2) // 3
    return Fraction(
        (-1) ** k * 3 * comb(3 * k + 2, k), 2 ** (2 * k + 2)
    )


def check_sparse(companion, expected_variables, expected_terms, degrees) -> None:
    assert len(companion["variables"]) == expected_variables
    assert companion["number_of_terms"] == expected_terms
    assert len(companion["terms"]) == expected_terms
    seen = set()
    observed_degrees = set()
    for term in companion["terms"]:
        powers = tuple(term["powers"])
        assert len(powers) == expected_variables
        assert all(isinstance(power, int) and power >= 0 for power in powers)
        assert powers not in seen
        seen.add(powers)
        real, imaginary = map(Fraction, term["coefficient_qi"])
        assert real or imaginary
        observed_degrees.add(sum(powers))
    assert observed_degrees == set(degrees)


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    payload = json.loads(raw)
    assert payload["format"] == "unified-every-order-certificate-v1"

    for precursor in payload["precursors"].values():
        path = (HERE / precursor["path"]).resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == precursor["sha256"]
    quartic = json.loads(
        (HERE / payload["precursors"]["quartic44"]["path"]).resolve().read_text()
    )
    unipotent = json.loads(
        (HERE / payload["precursors"]["unipotent14"]["path"]).resolve().read_text()
    )
    assert quartic["degree"] == 4 and quartic["number_of_terms"] == 538
    assert len(quartic["variables"]) == 44 and len(quartic["terms"]) == 538
    assert len(unipotent["variables"]) == 14
    assert sum(len(component) for component in unipotent["g"]) == 24
    print("[1/4] precursor hashes and sparse certificates")

    data14 = payload["unipotent14"]
    assert data14["weights"] == [1, 1, 1, 2, 3, 2, 3, 4, 5, 2, 3, 4, 5, 6]
    assert data14["homogeneous_jordan_type"] == [14, 1]
    assert data14["fiber_groebner_basis"] == [
        "-27*x^2+4*z+1", "3*x+2*y", "x^3-x"
    ]
    points = []
    for x in (Fraction(-1), Fraction(0), Fraction(1)):
        y = -3 * x / 2
        z = (27 * x * x - 1) / 4
        assert -27 * x * x + 4 * z + 1 == 0
        assert 3 * x + 2 * y == 0
        assert x**3 - x == 0
        points.append((x, y, z))
    assert len(set(points)) == 3
    print("[2/4] exact reduced three-point source fiber data")

    inverse = payload["inverse_series"]
    assert inverse["q_target14"] == ["1/2", "0", "1"] + ["0"] * 11
    assert inverse["r_target22"] == [
        "1/2", "0", "1", "0", "0", "0", "-2",
    ] + ["0"] * 14 + ["1"]
    for m in range(1000):
        assert q_coefficient(m) and r_coefficient(m)
    print("[3/4] closed q_m and r_m formulas are nonzero through m=999")

    companions = payload["companions"]
    check_sparse(companions["nonhomogeneous28"], 28, 178, range(2, 9))
    check_sparse(companions["homogeneous30"], 30, 608, (8,))
    assert companions["homogeneous30"]["inverse_target15"] == [
        "1/2", "0", "1",
    ] + ["0"] * 11 + ["1"]
    print("[4/4] 28D and 30D expanded Hessian companions")
    print(f"PASS {CERTIFICATE.name} sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
