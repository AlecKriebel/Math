#!/usr/bin/env python3
"""Exact finite verifier for the small-union Hall proof.

The continuous inequalities are proved in ``small_union_hall.md``.  This
verifier independently checks every finite classification used there:
the five pair types, the support stabilizer, the 18 coordinate-cycle
triangles, and their four stabilizer orbits.
"""

from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

from support import ROOTS, all_d5_roots, completion_roots, dot


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "small_union_hall_certificate.json"


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


def load(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def support(root):
    return frozenset(i for i, value in enumerate(root) if value)


def act(root, permutation, signs):
    return tuple(signs[i] * root[permutation[i]] for i in range(5))


def support_stabilizer():
    fixed = frozenset(ROOTS)
    answer = []
    for permutation in permutations(range(5)):
        for signs in product((-1, 1), repeat=5):
            image = frozenset(act(root, permutation, signs) for root in ROOTS)
            if image == fixed:
                answer.append((permutation, signs))
    return tuple(answer)


def coordinate_cycle_triples(omitted):
    answer = []
    for indices in combinations(range(len(omitted)), 3):
        roots = tuple(omitted[i] for i in indices)
        if not all(dot(a, b) == 1 for a, b in combinations(roots, 2)):
            continue
        degrees = [
            sum(coordinate in support(root) for root in roots)
            for coordinate in range(5)
        ]
        if sorted(degrees) == [0, 0, 2, 2, 2]:
            answer.append(indices)
    return tuple(answer)


def stabilizer_orbits(triples, omitted, stabilizer):
    index = {root: i for i, root in enumerate(omitted)}
    triple_set = set(triples)
    unseen = set(triples)
    answer = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(
                sorted(
                    index[act(omitted[i], permutation, signs)]
                    for i in representative
                )
            )
            for permutation, signs in stabilizer
        }
        require(orbit <= triple_set, "stabilizer left coordinate-cycle set")
        answer.append((representative, frozenset(orbit)))
        unseen -= orbit
    return tuple(answer)


def parse_signature(key):
    require(type(key) is str, "pair signature key is not a string")
    pieces = key.split(",")
    require(len(pieces) == 2, "pair signature key malformed")
    try:
        return tuple(int(piece) for piece in pieces)
    except ValueError as exc:
        raise VerificationError("pair signature key malformed") from exc


def parse_triples(value, field):
    require(type(value) is list, "%s must be a list" % field)
    answer = []
    for row in value:
        require(type(row) is list and len(row) == 3, "%s row malformed" % field)
        require(all(type(item) is int for item in row), "%s item malformed" % field)
        require(row == sorted(row) and len(set(row)) == 3, "%s row not sorted" % field)
        require(all(0 <= item < 28 for item in row), "%s index out of range" % field)
        answer.append(tuple(row))
    require(len(set(answer)) == len(answer), "%s contains duplicates" % field)
    return tuple(answer)


def verify(path=DEFAULT_CERTIFICATE):
    data = load(path)
    expected_keys = {
        "schema",
        "status",
        "full_root_count",
        "support_count",
        "omitted_count",
        "pair_signature_counts",
        "support_stabilizer_order",
        "coordinate_cycle_triples",
        "support_stabilizer_orbits",
        "proved_hall_union_size",
    }
    require(set(data) == expected_keys, "certificate keys mismatch")
    require(
        data["schema"] == "kissing5.realized_d5_extension.small_union_hall.v1",
        "schema mismatch",
    )
    require(
        data["status"] == "EXACT_FINITE_CLASSIFICATION_SUPPORTING_HUMAN_PROOF",
        "status mismatch",
    )

    full = all_d5_roots()
    omitted = completion_roots()
    require(type(data["full_root_count"]) is int, "root count type")
    require(type(data["support_count"]) is int, "support count type")
    require(type(data["omitted_count"]) is int, "omitted count type")
    require(len(full) == data["full_root_count"] == 40, "full root count")
    require(len(ROOTS) == data["support_count"] == 12, "support count")
    require(len(omitted) == data["omitted_count"] == 28, "omitted count")
    require(set(ROOTS).isdisjoint(omitted), "support and omitted roots overlap")
    require(set(ROOTS) | set(omitted) == set(full), "root partition failed")

    pair_counts = Counter(
        (dot(left, right), len(support(left) & support(right)))
        for left, right in combinations(full, 2)
    )
    claimed_pair_raw = data["pair_signature_counts"]
    require(type(claimed_pair_raw) is dict, "pair counts malformed")
    claimed_pair = Counter()
    for key, value in claimed_pair_raw.items():
        require(type(value) is int and value >= 0, "pair count malformed")
        claimed_pair[parse_signature(key)] = value
    require(pair_counts == claimed_pair, "pair signature counts mismatch")
    require(sum(pair_counts.values()) == 780, "pair count total mismatch")

    stabilizer = support_stabilizer()
    require(
        type(data["support_stabilizer_order"]) is int,
        "stabilizer order type",
    )
    require(
        len(stabilizer) == data["support_stabilizer_order"] == 16,
        "support stabilizer order mismatch",
    )

    triples = coordinate_cycle_triples(omitted)
    claimed_triples = parse_triples(
        data["coordinate_cycle_triples"], "coordinate_cycle_triples"
    )
    require(triples == claimed_triples, "coordinate-cycle triple list mismatch")
    require(len(triples) == 18, "coordinate-cycle triple count mismatch")

    orbits = stabilizer_orbits(triples, omitted, stabilizer)
    claimed_orbits_raw = data["support_stabilizer_orbits"]
    require(type(claimed_orbits_raw) is list, "orbit list malformed")
    claimed_orbits = []
    for row in claimed_orbits_raw:
        require(
            type(row) is dict and set(row) == {"representative", "size"},
            "orbit record malformed",
        )
        representative = parse_triples(
            [row["representative"]], "orbit representative"
        )[0]
        require(type(row["size"]) is int and row["size"] > 0, "orbit size")
        claimed_orbits.append((representative, row["size"]))
    actual_orbits = [(representative, len(orbit)) for representative, orbit in orbits]
    require(actual_orbits == claimed_orbits, "stabilizer orbit mismatch")
    require(sum(size for _, size in actual_orbits) == 18, "orbit total mismatch")

    require(
        type(data["proved_hall_union_size"]) is int
        and data["proved_hall_union_size"] == 3,
        "Hall-union claim mismatch",
    )
    return {
        "full_roots": 40,
        "pair_types": len(pair_counts),
        "support_stabilizer_order": len(stabilizer),
        "coordinate_cycle_triples": len(triples),
        "triple_orbit_sizes": [size for _, size in actual_orbits],
        "proved_hall_union_size": 3,
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    require(len(arguments) <= 1, "usage: verify_small_union_hall.py [certificate]")
    path = Path(arguments[0]) if arguments else DEFAULT_CERTIFICATE
    print(json.dumps(verify(path), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
