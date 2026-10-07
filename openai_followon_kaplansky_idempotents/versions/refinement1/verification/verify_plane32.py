#!/usr/bin/env python3
"""Exact, deterministic finite label-model certificate for q = 32.

This checks F_32 = F_2[z]/(z^5 + z^2 + 1), PG(2,32), the seven
Fano-complement extra labels, and a fixed-point-free inverse-letter pairing.
It does not select a random matching, give a finite group presentation,
verify torsion-freeness, or certify any group-algebra multiplication.

Run with Python 3.10 or later; only the standard library is used.  The
optional --write-incidence flag creates the companion JSON file without
overwriting an existing file.  An existing companion is always checked.
"""

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


Q = 32
MODULUS = 0b100101  # z^5 + z^2 + 1; coefficient of z^i is bit i.
V = Q * Q + Q + 1
EXPECTED_DATA_SHA256 = "12791c8fbad11b6af08ec76adffef476ec01abdcd65c6b0aa9ee69ea5492b4e1"
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "plane32_incidence.json"


def check(condition, message):
    """Checks remain active even under python -O."""
    if not condition:
        raise ValueError(message)


def polynomial_remainder(dividend, divisor):
    check(divisor > 0, "polynomial divisor must be nonzero")
    while dividend.bit_length() >= divisor.bit_length():
        dividend ^= divisor << (dividend.bit_length() - divisor.bit_length())
    return dividend


def polynomial_product(left, right):
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def multiply(left, right):
    """Shift-and-reduce multiplication, independently checked below."""
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & Q:
            left ^= MODULUS
    return result


def verify_field():
    # A reducible polynomial of degree five has a factor of degree <= 2.
    # Degree-three monic candidates are checked too, as an additional check.
    trial_divisors = []
    for degree in (1, 2, 3):
        for divisor in range(1 << degree, 1 << (degree + 1)):
            check(polynomial_remainder(MODULUS, divisor) != 0,
                  f"modulus has monic factor {divisor:b}")
            trial_divisors.append(divisor)
    check(MODULUS.bit_length() - 1 == 5, "modulus degree is not five")

    table = [[multiply(x, y) for y in range(Q)] for x in range(Q)]
    for x, y in product(range(Q), repeat=2):
        check(table[x][y] == polynomial_remainder(polynomial_product(x, y), MODULUS),
              "independent multiplication implementations disagree")
        check(0 <= table[x][y] < Q, "multiplication leaves the field set")
        check(table[x][y] == table[y][x], "multiplication is not commutative")
    inverses = [0] * Q
    for x in range(Q):
        check(table[x][0] == 0 and table[x][1] == x, "zero or unit law fails")
        check((x ^ 0) == x and (x ^ x) == 0, "addition law fails")
        if x:
            candidates = [y for y in range(Q) if table[x][y] == 1]
            check(len(candidates) == 1, "nonzero element lacks a unique inverse")
            inverses[x] = candidates[0]
    for x, y, z in product(range(Q), repeat=3):
        check(table[table[x][y]][z] == table[x][table[y][z]],
              "multiplication associativity fails")
        check(table[x][y ^ z] == (table[x][y] ^ table[x][z]),
              "distributivity fails")
        check((x ^ y) ^ z == x ^ (y ^ z), "addition associativity fails")
    return table, inverses, trial_divisors


def verify_plane(table, inverses):
    def normalize(vector):
        first = next((coordinate for coordinate in vector if coordinate), None)
        check(first is not None, "cannot normalize a zero vector")
        scale = inverses[first]
        return tuple(table[coordinate][scale] for coordinate in vector)

    points = sorted([(1, y, z) for y, z in product(range(Q), repeat=2)]
                    + [(0, 1, z) for z in range(Q)] + [(0, 0, 1)])
    check(len(points) == V == 1057 and len(set(points)) == V,
          "wrong number of canonical projective points")
    check(all(normalize(point) == point for point in points),
          "canonical point normalization fails")
    classes = Counter(normalize(vector) for vector in product(range(Q), repeat=3)
                      if vector != (0, 0, 0))
    check(set(classes) == set(points) and set(classes.values()) == {Q - 1},
          "projective classes do not partition the nonzero vectors into size 31")

    # Covectors use the same normalization, but constitute the dual point set.
    covectors = list(points)
    rows = []
    row_bits = []
    column_bits = [0] * V
    for line_index, (a, b, c) in enumerate(covectors):
        incident = []
        bits = 0
        for point_index, (x, y, z) in enumerate(points):
            if table[a][x] ^ table[b][y] ^ table[c][z] == 0:
                incident.append(point_index)
                bits |= 1 << point_index
                column_bits[point_index] |= 1 << line_index
        check(len(incident) == Q + 1 == 33, "line does not have 33 points")
        rows.append(incident)
        row_bits.append(bits)
    check(all(bits.bit_count() == Q + 1 for bits in column_bits),
          "point does not lie on 33 lines")
    pair_count = 0
    for i in range(V):
        for j in range(i):
            check((row_bits[i] & row_bits[j]).bit_count() == 1,
                  "two distinct lines do not meet in exactly one point")
            check((column_bits[i] & column_bits[j]).bit_count() == 1,
                  "two distinct points do not determine exactly one line")
            pair_count += 1
    check(pair_count == V * (V - 1) // 2 == 558096, "wrong pair-check count")
    return points, covectors, rows, pair_count


def verify_fano_and_pairing():
    fano_points = set(range(1, 8))
    fano_lines = sorted({tuple(sorted((a, b, a ^ b)))
                         for a, b in combinations(sorted(fano_points), 2)})
    complements = [sorted(fano_points - set(line)) for line in fano_lines]
    check(len(fano_lines) == 7 and all(len(line) == 3 for line in fano_lines),
          "wrong Fano-line data")
    check(all(len(complement) == 4 for complement in complements),
          "Fano complement does not have four points")
    for point in fano_points:
        check(sum(point in complement for complement in complements) == 4,
              "Fano point does not occur in four complements")
    for a, b in combinations(sorted(fano_points), 2):
        check(sum(a in complement and b in complement for complement in complements) == 2,
              "Fano point pair does not occur in two complements")
    for left, right in combinations(complements, 2):
        check(len(set(left) & set(right)) == 2,
              "distinct Fano complements do not intersect in two points")

    # Ordinary letters are indexed 0..1056, extras 1057..1063.  The Fano
    # point j names extra letter 1056+j.  Pair the seven extras with the
    # first seven ordinary letters, and the remaining ordinary letters in order.
    extra_indices = list(range(V, V + 7))
    pairs = [[i, V + i] for i in range(7)]
    pairs += [[i, i + 1] for i in range(7, V, 2)]
    inverse = [-1] * (V + 7)
    for left, right in pairs:
        check(left != right and inverse[left] == inverse[right] == -1,
              "inverse-letter pairs overlap or have a fixed point")
        inverse[left], inverse[right] = right, left
    check(len(inverse) == 1064 and len(pairs) == 532,
          "wrong directed-letter or inverse-pair count")
    check(all(0 <= inverse[i] < len(inverse) and inverse[i] != i
              and inverse[inverse[i]] == i for i in range(len(inverse))),
          "inverse-letter map is not a fixed-point-free involution")
    check(all(inverse[V + i] == i for i in range(7)),
          "an extra label is not paired with its selected ordinary label")
    return fano_lines, complements, extra_indices, pairs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-incidence", action="store_true",
                        help="create data/plane32_incidence.json; refuse to overwrite")
    args = parser.parse_args()
    table, inverses, trial_divisors = verify_field()
    points, covectors, rows, pair_count = verify_plane(table, inverses)
    fano_lines, complements, extra_indices, pairs = verify_fano_and_pairing()
    payload = {
        "schema": "plane32-label-model-v1",
        "scope": "Finite field, projective incidence, Fano extras and inverse letters only; no random matching or group-algebra witness.",
        "field": {"characteristic": 2, "degree": 5, "order": Q,
                  "modulus_bits": MODULUS, "modulus": "z^5+z^2+1",
                  "element_encoding": "Bit i is the coefficient of z^i."},
        "normalization": "Scale the first nonzero coordinate to 1; sort tuples lexicographically.",
        "points": points,
        "line_covectors": covectors,
        "line_point_indices": rows,
        "fano_points": list(range(1, 8)),
        "fano_lines": fano_lines,
        "fano_complements": complements,
        "extra_letter_indices": extra_indices,
        "paired_ordinary_indices": list(range(7)),
        "inverse_pairs": pairs,
    }
    data_bytes = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    digest = hashlib.sha256(data_bytes).hexdigest()
    check(digest == EXPECTED_DATA_SHA256, "regenerated incidence data hash changed")
    if args.write_incidence:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DATA_PATH.open("xb") as handle:
            handle.write(data_bytes)
    companion_status = "absent; all checks used freshly reconstructed data"
    if DATA_PATH.exists():
        supplied = DATA_PATH.read_bytes()
        check(supplied == data_bytes, "companion incidence data differs from reconstruction")
        check(hashlib.sha256(supplied).hexdigest() == digest,
              "companion incidence data hash changed")
        companion_status = "byte-identical to freshly reconstructed data"
    print(json.dumps({
        "status": "passed",
        "scope": payload["scope"],
        "monic_factor_candidates_checked": len(trial_divisors),
        "field_elements": Q,
        "multiplication_pairs_checked": Q * Q,
        "field_triples_checked": Q ** 3,
        "nonzero_vectors_checked": Q ** 3 - 1,
        "points": V,
        "lines": V,
        "points_per_line": Q + 1,
        "lines_per_point": Q + 1,
        "line_pairs_checked": pair_count,
        "point_pairs_checked": pair_count,
        "incidences": sum(map(len, rows)),
        "fano_complements": len(complements),
        "directed_letters": V + 7,
        "inverse_pairs": len(pairs),
        "incidence_json_bytes": len(data_bytes),
        "incidence_json_sha256": digest,
        "companion_file": companion_status,
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
