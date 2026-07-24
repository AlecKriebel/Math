#!/usr/bin/env python3
"""Exact verifier for a counterexample to uniform full-conflict charging.

The certificate is untrusted JSON.  This verifier uses only rational
arithmetic and explicit checks; it does not use a solver or ``assert``.

Coordinates are in the scaled convention z = sqrt(2) y.  Thus a point has
squared norm 2, the kissing inequality is z_i dot z_j <= 1, and a completion
root v is a *full conflict* precisely when v dot z > 1.  Notice that the
conflict inequality is strict: contacts with v dot z = 1 are not conflicts.
"""

from fractions import Fraction
import json
from pathlib import Path
import sys

from support import ROOTS, completion_roots, dot


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "uniform_conflict_charge_counterexample.json"


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
    require(answer.denominator > 0, "%s has an invalid denominator" % field)
    return answer


def parse_point(value, index):
    require(type(value) is list and len(value) == 5, "point shape mismatch")
    return tuple(
        parse_fraction(coordinate, "points_scaled[%d][%d]" % (index, j))
        for j, coordinate in enumerate(value)
    )


def parse_conflict_set(value, index, number_of_centers):
    require(type(value) is list and value, "conflict set must be a nonempty list")
    answer = []
    for center in value:
        require(type(center) is int, "conflict index must be an integer")
        require(0 <= center < number_of_centers, "conflict index out of range")
        answer.append(center)
    require(answer == sorted(set(answer)), "conflict set is not sorted and unique")
    return tuple(answer)


def verify(path=DEFAULT_CERTIFICATE):
    data = load_json(path)
    expected_keys = {
        "schema",
        "status",
        "points_scaled",
        "claimed_full_conflict_sets",
        "claimed_overloaded_center_index",
        "claimed_uniform_charge",
    }
    require(set(data) == expected_keys, "certificate top-level keys mismatch")
    require(
        data["schema"]
        == "kissing5.realized_d5_extension.uniform_conflict_charge_counterexample.v1",
        "schema mismatch",
    )
    require(data["status"] == "EXACT_RATIONAL_COUNTEREXAMPLE", "status mismatch")

    raw_points = data["points_scaled"]
    require(type(raw_points) is list and len(raw_points) == 4, "need four points")
    points = tuple(parse_point(value, i) for i, value in enumerate(raw_points))
    require(len(set(points)) == 4, "points are not distinct")

    for i, point in enumerate(points):
        require(dot(point, point) == 2, "point %d has wrong scaled norm" % i)
        for support_index, root in enumerate(ROOTS):
            require(
                dot(root, point) <= 1,
                "point %d violates support polar inequality %d"
                % (i, support_index),
            )
    for i, left in enumerate(points):
        for j, right in enumerate(points[:i]):
            require(
                dot(left, right) <= 1,
                "points %d and %d violate the kissing inequality" % (j, i),
            )

    centers = completion_roots()
    raw_claims = data["claimed_full_conflict_sets"]
    require(
        type(raw_claims) is list and len(raw_claims) == len(points),
        "need one conflict-set claim per point",
    )
    claims = tuple(
        parse_conflict_set(value, i, len(centers))
        for i, value in enumerate(raw_claims)
    )
    actual = tuple(
        tuple(index for index, center in enumerate(centers) if dot(center, point) > 1)
        for point in points
    )
    require(actual == claims, "full conflict-set claim mismatch")

    overloaded = data["claimed_overloaded_center_index"]
    require(type(overloaded) is int, "overloaded center index must be an integer")
    require(0 <= overloaded < len(centers), "overloaded center index out of range")
    require(
        all(overloaded in conflict_set for conflict_set in actual),
        "claimed center is not common to all points",
    )
    uniform_charge = sum(
        Fraction(1, len(conflict_set))
        for conflict_set in actual
        if overloaded in conflict_set
    )
    claimed_charge = parse_fraction(
        data["claimed_uniform_charge"], "claimed uniform charge"
    )
    require(uniform_charge == claimed_charge, "uniform-charge claim mismatch")
    require(uniform_charge == Fraction(13, 12), "unexpected exact charge")
    require(uniform_charge > 1, "claimed center is not overloaded")

    # The strict/non-strict boundary is checked independently: membership in
    # `actual` used > 1 above, while every omitted center is required <= 1.
    for point, conflict_set in zip(points, actual):
        conflict_lookup = set(conflict_set)
        for index, center in enumerate(centers):
            value = dot(center, point)
            if index in conflict_lookup:
                require(value > 1, "listed full conflict is not strict")
            else:
                require(value <= 1, "an omitted full conflict lies above boundary")

    return {
        "status": "REFUTED_BY_EXACT_RATIONAL_COUNTEREXAMPLE",
        "points": len(points),
        "conflict_degrees": [len(conflict_set) for conflict_set in actual],
        "overloaded_center_index": overloaded,
        "overloaded_center": list(centers[overloaded]),
        "uniform_charge": str(uniform_charge),
        "maximum_pair_scaled_dot": str(
            max(dot(left, right) for i, left in enumerate(points) for right in points[:i])
        ),
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    require(
        len(arguments) <= 1,
        "usage: verify_uniform_conflict_charge_counterexample.py [certificate.json]",
    )
    path = Path(arguments[0]) if arguments else DEFAULT_CERTIFICATE
    print(json.dumps(verify(path), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
