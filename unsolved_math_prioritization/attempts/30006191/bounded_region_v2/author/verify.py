#!/usr/bin/env python3
"""Finite sanity tests and integrity checks; not a substitute for the proof."""
import argparse
import cmath
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def determinant(matrix):
    n = len(matrix)
    total = 0j
    for permutation in itertools.permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i + 1, n))
        product = complex((-1) ** inversions)
        for i, j in enumerate(permutation):
            product *= matrix[i][j]
        total += product
    return total


def slater_moments():
    # Fourier orbitals make q non-diagonal in the occupied-space basis.
    dimension = 6
    unitary = [[cmath.exp(2j * math.pi * i * j / dimension) / math.sqrt(dimension)
                for j in range(dimension)] for i in range(dimension)]
    outside = set(range(3, 6))
    max_error = 0.0
    cases = []
    for occupied in [(0,), (0, 2), (0, 1, 3)]:
        particle_number = len(occupied)
        coefficients = {}
        for sites in itertools.combinations(range(dimension), particle_number):
            coefficient = determinant([[unitary[i][j] for j in occupied] for i in sites])
            coefficients[sites] = coefficient
        norm_squared = sum(abs(x) ** 2 for x in coefficients.values())
        assert abs(norm_squared - 1) < 1e-13
        mean = sum(abs(x) ** 2 * len(set(sites) & outside)
                   for sites, x in coefficients.items())
        second = sum(abs(x) ** 2 * len(set(sites) & outside) ** 2
                     for sites, x in coefficients.items())
        projection = [[sum(unitary[i][j] * unitary[k][j].conjugate() for j in occupied)
                       for k in range(dimension)] for i in range(dimension)]
        trace_pq = sum(projection[i][i].real for i in outside)
        trace_pqpq = sum(abs(projection[i][j]) ** 2 for i in outside for j in outside)
        predicted_second = trace_pq ** 2 + trace_pq - trace_pqpq
        error = max(abs(mean - trace_pq), abs(second - predicted_second))
        max_error = max(max_error, error)
        assert error < 1e-13
        variance = second - mean ** 2
        assert variance >= -1e-13 and variance <= mean + 1e-13
        assert math.sqrt(second) <= math.sqrt(mean) + mean + 1e-13
        cases.append({"particles": particle_number, "mean": mean,
                      "variance": variance, "second_moment": second})
    return {"status": "pass", "max_moment_identity_error": max_error, "cases": cases}


def sector_polynomials_and_phases():
    max_phase_error = 0.0
    sector_cases = 0
    for sigma in [0, 1]:
        for n in range(1, 65):
            for leaked in range(n + 1):
                local_number = n - leaked
                difference = local_number * (local_number - sigma) - n * (n - sigma)
                assert difference == -leaked * (2 * n - sigma - leaked)
                assert abs(difference) <= 2 * n * leaked
                sector_cases += 1
            gap = (n + 1) * (n + 1 - sigma) - n * (n - sigma)
            assert gap == 2 * n + 1 - sigma
            time = math.pi / gap
            max_phase_error = max(max_phase_error, abs(cmath.exp(1j * time * gap) + 1))
    assert max_phase_error < 1e-14

    # A diagonal one-particle h gives the exact reference matrix element.
    # This probes the sign and the creation-sector phase simultaneously.
    eigenvalue = Fraction(3, 7)
    for sigma in [0, 1]:
        for n in [1, 2, 5, 31]:
            t = math.pi / (2 * n + 1 - sigma)
            direct = cmath.exp(1j * t * (float(eigenvalue) +
                                          (n + 1) * (n + 1 - sigma) - n * (n - sigma)))
            predicted = -cmath.exp(1j * t * float(eigenvalue))
            assert abs(direct - predicted) < 1e-13
    return {"status": "pass", "sector_cases": sector_cases,
            "max_phase_error": max_phase_error,
            "ordering_conventions_checked": ["density-density", "normal-ordered"]}


def exponents_and_potential():
    d = 3
    kinetic = 1 + Fraction(2, d)
    first = 1 + kinetic / 2 - 2
    second = 1 + kinetic - 3
    assert kinetic == Fraction(5, 3)
    assert first == Fraction(-1, 6)
    assert second == Fraction(-1, 3)
    assert first < 0 and second < 0
    assert 1 + (1 + Fraction(2, 2)) / 2 - 2 == 0
    assert 1 + (1 + Fraction(2, 1)) / 2 - 2 > 0
    def bump(s):
        return math.exp(-1 / s) if s > 0 else 0.0
    def potential(radius):
        a, b = bump(81 - radius ** 2), bump(radius ** 2 - 64)
        assert a + b > 0
        return a / (a + b)
    assert all(potential(r) == 1 for r in [0, 1, 4, 7.9, 8])
    assert all(potential(r) == 0 for r in [9, 10, 20])
    assert all(0 <= potential(j / 100) <= 1 for j in range(2001))
    # These algebraic exponents, rather than finite tests, are the decay mechanism.
    return {"status": "pass", "kinetic_exponent": str(kinetic),
            "comparison_decay_exponents": [str(first), str(second)],
            "dimension_two_boundary_checked": True, "plateau_and_support_samples": "pass"}


def verify_manifest():
    manifest = json.loads((ROOT / "AUTHOR_MANIFEST.json").read_text())
    assert manifest["self_excluded"] == "AUTHOR_MANIFEST.json"
    expected = set(manifest["files"]) | {"AUTHOR_MANIFEST.json"}
    present = {path.name for path in ROOT.iterdir() if path.is_file()}
    assert expected == present, f"Unexpected file set: {expected ^ present}"
    for name, record in manifest["files"].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == record["bytes"], name
        assert hashlib.sha256(data).hexdigest() == record["sha256"], name
    assert not any(name.endswith((".pdf", ".html")) for name in present)
    return "pass"


def verify_sources(source_dir):
    metadata = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text())
    for record in metadata["sources"]:
        data = (source_dir / record["file_label"]).read_bytes()
        assert data.startswith(b"%PDF-")
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
    return {"status": "pass", "count": len(metadata["sources"])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    result = {"slater_moments": slater_moments(),
              "sector_polynomials_and_phases": sector_polynomials_and_phases(),
              "exponents_and_potential": exponents_and_potential(),
              "manifest": verify_manifest(),
              "scope": "Finite sanity tests and provenance checks; the analytic proof establishes norm discontinuity."}
    if args.source_dir:
        result["source_bytes"] = verify_sources(args.source_dir)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
