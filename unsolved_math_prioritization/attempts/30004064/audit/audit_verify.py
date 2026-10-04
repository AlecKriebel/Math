#!/usr/bin/env python3
"""Independent exact checks and read-only replay of a frozen candidate.

Run from any directory. Optional first argument is the candidate public directory.
No network, floating-point optimizer, source corpus, or external dependency.
"""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys

FROZEN_HASH = "22b5cbbe1abebdfc10e068cf433382bb3b802b22376d9e8bfb17e5fcae73af0d"


def inner(a, b):
    assert len(a) == len(b)
    return sum(x * y for x, y in zip(a, b))


def apply(a, x):
    return tuple(inner(row, x) for row in a)


def transpose(a):
    return tuple(zip(*a))


def line_matrix(k, redundant=False):
    positions = tuple(itertools.product(range(k), repeat=2))
    return tuple(tuple(int(i == q) for i, j in positions) for q in range(k)) + tuple(
        tuple(int(j == q) for i, j in positions) for q in range(k if redundant else k - 1)
    )


def matrix_rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    pivot_row = 0
    for col in range(len(rows[0])):
        candidates = [r for r in range(pivot_row, len(rows)) if rows[r][col]]
        if not candidates:
            continue
        r = candidates[0]
        rows[pivot_row], rows[r] = rows[r], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [x / scale for x in rows[pivot_row]]
        for r in range(pivot_row + 1, len(rows)):
            scale = rows[r][col]
            rows[r] = [x - scale * y for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def common(images):
    return tuple(values[0] if min(values) == max(values) else 0 for values in zip(*images))


def objective(a, y, u):
    residual = tuple(x - z for x, z in zip(u, y))
    return inner(residual, residual) / Q(2) + sum(abs(t) for t in apply(transpose(a), u))


def main():
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "public"
    manifest_bytes = (public / "FROZEN_MANIFEST.json").read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest() == FROZEN_HASH
    manifest = json.loads(manifest_bytes)
    for entry in manifest["files"]:
        content = (public / entry["path"]).read_bytes()
        assert len(content) == entry["bytes"]
        assert hashlib.sha256(content).hexdigest() == entry["sha256"]
    replay = subprocess.run([sys.executable, "verify.py"], cwd=public, capture_output=True, check=True)
    assert replay.stdout == (public / "verification_results.json").read_bytes()
    replay_result = json.loads(replay.stdout)
    assert [replay_result[key] for key in ("binary_images_checked", "objective_identity_checks", "projected_objective_checks", "scalar_approximation_checks")] == [1044, 1458, 729, 8]

    # Build every 3-by-3 fiber independently, then challenge both signs of fixed pixels.
    a = line_matrix(3)
    fibers = {}
    for image in itertools.product((-1, 1), repeat=9):
        fibers.setdefault(apply(a, image), []).append(image)
    assert matrix_rank(a) == 5
    tests = (
        ((3, 1, 1, 3, 1), (1, 1, 1, 1, 0, 0, 1, 0, 0)),
        ((-3, -1, -1, -3, -1), (-1, -1, -1, -1, 0, 0, -1, 0, 0)),
        ((3, -1, -1, -1, 1), (1, 1, 1, -1, 0, 0, -1, 0, 0)),
    )
    for data, expected in tests:
        assert len(fibers[data]) == 2
        assert common(fibers[data]) == expected
        assert sum(value != 0 for value in expected) == 5
    assert fibers[(3, 3, 3, 3, 3)] == [(1,) * 9]
    a2 = line_matrix(2)
    mixed = (1, 1, -1, -1)
    assert [s for s in itertools.product((-1, 1), repeat=4) if apply(a2, s) == apply(a2, mixed)] == [mixed]

    # Direct objective expansion for signed/rank-deficient matrices and fractional box points.
    matrices = (((1,),), ((-2, 1),), ((1, 1), (1, -1)), ((1, 2), (2, 4)))
    identities = 0
    for matrix in matrices:
        for s in itertools.product((Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)), repeat=len(matrix[0])):
            y = apply(matrix, s)
            zero = (Q(0),) * len(matrix)
            for u in itertools.product((Q(-2), Q(-1, 3), Q(0), Q(1, 3), Q(2)), repeat=len(matrix)):
                back = apply(transpose(matrix), u)
                slack = sum(abs(t) - x * t for x, t in zip(s, back))
                difference = objective(matrix, y, u) - objective(matrix, y, zero)
                assert difference == inner(u, u) / Q(2) + slack
                assert slack >= 0
                assert (difference == 0) == (u == zero)
                identities += 1

    # Check full row rank and actual incidence of the arbitrary-size extension.
    for k in range(3, 10):
        assert matrix_rank(line_matrix(k)) == 2 * k - 1
        for value in (-1, 1):
            s = [1] * (k * k)
            for row, col, entry in ((k-2, k-2, value), (k-2, k-1, -value), (k-1, k-2, -value), (k-1, k-1, value)):
                s[k * row + col] = entry
            measured = apply(line_matrix(k, True), s)
            assert measured == (k,) * (k-2) + (k-2, k-2) + (k,) * (k-2) + (k-2, k-2)

    # The common vector itself is an admissible auxiliary box/subgradient variable.
    # This shows why the multiplier conclusion must not be transferred to sign(z).
    for data, expected in tests:
        assert apply(a, expected) == data
        assert all(-1 <= value <= 1 for value in expected)

    return {
        "verdict": "all_audit_checks_passed",
        "frozen_manifest_sha256": FROZEN_HASH,
        "frozen_authored_files_verified": len(manifest["files"]),
        "frozen_replay_byte_identical": True,
        "frozen_replay_counts": {key: replay_result[key] for key in ("binary_images_checked", "objective_identity_checks", "projected_objective_checks", "scalar_approximation_checks")},
        "independent_binary_images_enumerated": 528,
        "independent_3x3_data_fibers": len(fibers),
        "independent_3x3_unique_images": sum(len(images) == 1 for images in fibers.values()),
        "two_solution_fibers_with_five_fixed_pixels": len(tests),
        "mixed_positive_negative_fixed_pixels_checked": True,
        "independent_box_objective_identity_checks": identities,
        "arbitrary_size_rank_examples_checked": 7,
        "auxiliary_subgradient_distinction_checked": True,
        "universal_mathematical_claim_proved_by": "Direct algebraic inequality, not finite tests",
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
