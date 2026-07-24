#!/usr/bin/env python3
"""Small exact verifier for the 28-point D5 completion.

No floating-point arithmetic, NumPy, solver, or optimized-away ``assert`` is
used.  The input JSON is treated as untrusted certificate data.
"""

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

from support import ROOTS, WEIGHTS, dot


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "known_28_completion.json"


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, "duplicate JSON key: %r" % (key,))
        answer[key] = value
    return answer


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def parse_fraction(value, field):
    require(type(value) is str, "%s must be a string" % field)
    try:
        answer = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("%s is not a rational" % field) from exc
    require(answer.denominator > 0, "%s has invalid denominator" % field)
    return answer


def parse_root(value, index):
    require(type(value) is list and len(value) == 5, "root shape mismatch")
    answer = []
    for coordinate in value:
        require(type(coordinate) is int, "root coordinate must be an integer")
        require(coordinate in (-1, 0, 1), "root coordinate outside D5 alphabet")
        answer.append(coordinate)
    answer = tuple(answer)
    require(sum(x * x for x in answer) == 2, "root does not have squared norm 2")
    return answer


def matrix_rank(matrix):
    work = [[Fraction(x) for x in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [x / scale for x in work[rank]]
        for r in range(rows):
            if r != rank and work[r][col]:
                factor = work[r][col]
                work[r] = [
                    work[r][j] - factor * work[rank][j] for j in range(cols)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def verify(path=DEFAULT_CERTIFICATE):
    data = load_json(path)
    expected_keys = {
        "schema",
        "status",
        "roots",
        "claimed_centroid_scaled",
        "claimed_frame_diagonal",
        "claimed_frame_potential",
        "claimed_v_trace",
        "claimed_profile_rank",
        "claimed_ordered_gram_distribution",
        "claimed_weighted_column_energy",
    }
    require(set(data) == expected_keys, "certificate top-level keys mismatch")
    require(
        data["schema"] == "kissing5.realized_d5_extension.known28.v1",
        "schema mismatch",
    )
    require(
        data["status"] == "EXACT_CERTIFICATE_FOR_KNOWN_28_COMPLETION",
        "status mismatch",
    )

    roots_raw = data["roots"]
    require(type(roots_raw) is list and len(roots_raw) == 28, "need 28 roots")
    roots = tuple(parse_root(value, i) for i, value in enumerate(roots_raw))
    require(len(set(roots)) == 28, "duplicate completion root")
    require(set(roots).isdisjoint(ROOTS), "completion intersects fixed support")

    full = set(roots) | set(ROOTS)
    require(len(full) == 40, "support plus completion does not have size 40")
    for i, left in enumerate(tuple(full)):
        for right in tuple(full)[i + 1 :]:
            require(dot(left, right) <= 1, "D5 kissing inequality failed")

    centroid = tuple(sum(root[j] for root in roots) for j in range(5))
    claimed_centroid = data["claimed_centroid_scaled"]
    require(
        type(claimed_centroid) is list
        and len(claimed_centroid) == 5
        and all(type(x) is int for x in claimed_centroid),
        "claimed centroid malformed",
    )
    require(tuple(claimed_centroid) == centroid, "centroid claim mismatch")
    require(centroid == (0, 0, 0, 0, 0), "completion is not centered")

    frame = [
        [
            sum(Fraction(root[i] * root[j], 2) for root in roots)
            for j in range(5)
        ]
        for i in range(5)
    ]
    claimed_diagonal = data["claimed_frame_diagonal"]
    require(
        type(claimed_diagonal) is list and len(claimed_diagonal) == 5,
        "frame diagonal claim malformed",
    )
    claimed_diagonal = tuple(
        parse_fraction(x, "claimed_frame_diagonal") for x in claimed_diagonal
    )
    require(
        all(frame[i][j] == 0 for i in range(5) for j in range(5) if i != j),
        "claimed diagonal frame has a nonzero off-diagonal entry",
    )
    require(
        tuple(frame[i][i] for i in range(5)) == claimed_diagonal,
        "frame diagonal mismatch",
    )

    frame_potential = sum(
        frame[i][j] * frame[j][i] for i in range(5) for j in range(5)
    )
    require(
        frame_potential
        == parse_fraction(data["claimed_frame_potential"], "frame potential"),
        "frame-potential claim mismatch",
    )
    require(frame_potential == 158, "unexpected exact frame potential")
    v_trace = frame[0][0] + frame[4][4]
    require(
        v_trace == parse_fraction(data["claimed_v_trace"], "V trace"),
        "V-trace claim mismatch",
    )
    require(v_trace == 10, "unexpected V trace")
    require(
        frame_potential
        == Fraction((28 - v_trace) ** 2, 3) + Fraction(v_trace**2, 2),
        "3+2 block-frame equality failed",
    )

    gram_distribution = Counter(
        Fraction(dot(left, right), 2) for left in roots for right in roots
    )
    claimed_distribution_raw = data["claimed_ordered_gram_distribution"]
    require(type(claimed_distribution_raw) is dict, "distribution malformed")
    claimed_distribution = Counter()
    for key, value in claimed_distribution_raw.items():
        require(type(value) is int and value >= 0, "distribution count malformed")
        claimed_distribution[Fraction(key)] = value
    require(gram_distribution == claimed_distribution, "Gram distribution mismatch")

    support_gram = [
        [Fraction(dot(left, right), 2) for right in ROOTS] for left in ROOTS
    ]
    profiles = [
        [Fraction(dot(support_root, root), 2) for support_root in ROOTS]
        for root in roots
    ]
    require(
        type(data["claimed_profile_rank"]) is int,
        "claimed profile rank must be an integer",
    )
    require(
        matrix_rank(profiles) == data["claimed_profile_rank"] == 5,
        "profile rank mismatch",
    )

    for a, profile in enumerate(profiles):
        second = sum(p * h * h for p, h in zip(WEIGHTS, profile))
        require(second == Fraction(1, 5), "profile second moment failed")
        projected = sum(
            profile[i]
            * WEIGHTS[i]
            * support_gram[i][j]
            * WEIGHTS[j]
            * profile[j]
            for i in range(12)
            for j in range(12)
        )
        require(projected == Fraction(1, 25), "projection membership failed")
        reconstructed = [
            5
            * sum(
                support_gram[i][j] * WEIGHTS[j] * profile[j]
                for j in range(12)
            )
            for i in range(12)
        ]
        require(reconstructed == profile, "profile column-space equation failed")
        for b in range(a):
            cross = sum(
                WEIGHTS[i] * profile[i] * profiles[b][i] for i in range(12)
            )
            require(cross == Fraction(dot(roots[a], roots[b]), 10), "cross identity")
            require(cross <= Fraction(1, 10), "profile kissing bound failed")

    column_energies = [
        sum(profile[i] * profile[i] for profile in profiles) for i in range(12)
    ]
    weighted_energy = sum(
        p * energy for p, energy in zip(WEIGHTS, column_energies)
    )
    require(
        weighted_energy
        == parse_fraction(
            data["claimed_weighted_column_energy"], "weighted column energy"
        ),
        "weighted column-energy claim mismatch",
    )
    require(weighted_energy == Fraction(28, 5), "column-energy identity failed")

    return {
        "points": 28,
        "profile_rank": 5,
        "frame_potential": str(frame_potential),
        "v_trace": str(v_trace),
        "weighted_column_energy": str(weighted_energy),
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    require(len(arguments) <= 1, "usage: verify_known_28.py [certificate.json]")
    path = Path(arguments[0]) if arguments else DEFAULT_CERTIFICATE
    result = verify(path)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
