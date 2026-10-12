#!/usr/bin/env python3
"""Independent exact checks for the q=32 parameter substitution.

This is not a group-ring witness or a numerical search for the random graphs.
It checks the fixed type data and all finite matrix certificates used in the
parameter audit. Only Python's standard library is needed.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import math


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build"


def quotient(q):
    v = q * q + q + 1
    p = F(q + 1, v)
    return (
        (7 * p * p, F(6, (q + 1) ** 2), F(v - 7, (q + 1) ** 2)),
        (F(6, 4), 7 * p * p, (v - 7) * p * p),
        (7 * p * p, F(7, (q + 1) ** 2), F(v - 8, (q + 1) ** 2)),
    )


def direct_quotient_check(q):
    """Enumerate all allowed successors in the actual signed alphabet.

    No quotient-matrix formula is used when computing each row's class sums.
    The result then compares every full-matrix row with the proposed formula.
    """
    v = q * q + q + 1
    total = v + 7
    classes = [0] * 7 + [1] * 7 + [2] * (v - 7)
    inverse = list(range(total))
    for i in range(7):
        inverse[i], inverse[i + 7] = i + 7, i
    for i in range(14, total, 2):
        inverse[i], inverse[i + 1] = i + 1, i
    assert all(inverse[inverse[t]] == t != inverse[t] for t in range(total))
    p2 = F(q + 1, v) ** 2
    ordinary2 = F(1, (q + 1) ** 2)
    extra2 = F(1, 4)
    expected = quotient(q)
    for t in range(total):
        # Count each of the three actual turn categories per successor class.
        counts = [[0, 0, 0] for _ in range(3)]
        bt = inverse[t]
        for u in range(total):
            if u == bt:
                continue
            if bt >= 7 and u >= 7:
                category = 0
            elif bt < 7 and u < 7:
                category = 2
            else:
                category = 1
            counts[classes[u]][category] += 1
        row = tuple(a * ordinary2 + b * p2 + c * extra2 for a, b, c in counts)
        assert row == expected[classes[t]], (q, t, row, expected[classes[t]])
    return {"q": q, "letters": total, "all_rows_checked": total}


def rational_certificates():
    results = []
    for q in (4, 8, 16, 32):
        matrix = quotient(q)
        f = (F(1), F(13, 5), F(1)) if q == 32 else (F(193, 500), F(1), F(97, 250))
        ratios = tuple(sum(x * y for x, y in zip(row, f)) / f[i] for i, row in enumerate(matrix))
        if q == 32:
            bound = F(987, 1000)
            assert all(r < bound for r in ratios)
            direction = "strictly_less"
        else:
            bound = F(503, 500)
            assert all(r > bound for r in ratios)
            direction = "strictly_greater"
        results.append({
            "q": q,
            "matrix": [[str(x) for x in row] for row in matrix],
            "vector": [str(x) for x in f],
            "coordinate_ratios": [str(x) for x in ratios],
            "bound": str(bound),
            "direction": direction,
            "direct_full_alphabet_check": direct_quotient_check(q),
        })
    return results


def binary_poly_mod(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def field_and_plane32():
    # x^5 + x^2 + 1; a reducible degree-five polynomial has a factor
    # of degree at most two, so these divisions prove irreducibility.
    modulus = 0b100101
    for degree in (1, 2):
        for lower in range(1 << degree):
            assert binary_poly_mod(modulus, (1 << degree) | lower) != 0

    def mul(a, b):
        product = 0
        while b:
            if b & 1:
                product ^= a
            b >>= 1
            a <<= 1
            if a & 32:
                a ^= modulus
        return product

    table = [[mul(a, b) for b in range(32)] for a in range(32)]
    for a in range(1, 32):
        assert sorted(table[a]) == list(range(32))
        assert 1 in table[a]
    triples = [(1, a, b) for a in range(32) for b in range(32)]
    triples += [(0, 1, a) for a in range(32)] + [(0, 0, 1)]
    assert len(set(triples)) == 1057
    lines = []
    for normal in triples:
        line = frozenset(i for i, point in enumerate(triples)
                         if table[normal[0]][point[0]] ^ table[normal[1]][point[1]] ^ table[normal[2]][point[2]] == 0)
        assert len(line) == 33
        lines.append(line)
    assert len(set(lines)) == 1057
    occurrences = Counter(point for line in lines for point in line)
    assert len(occurrences) == 1057 and set(occurrences.values()) == {33}
    pair_counts = Counter(pair for line in lines for pair in combinations(sorted(line), 2))
    assert len(pair_counts) == 1057 * 1056 // 2
    assert set(pair_counts.values()) == {1}
    for first, second in combinations(lines, 2):
        assert len(first & second) == 1
    return {
        "modulus": "x^5+x^2+1",
        "field_order": 32,
        "points": len(triples),
        "lines": len(lines),
        "line_size": 33,
        "point_degree": 33,
        "all_point_pairs_checked": len(pair_counts),
        "all_line_pairs_checked": len(lines) * (len(lines) - 1) // 2,
    }


def fano_and_type_checks():
    points = frozenset(range(1, 8))
    fano_lines = {frozenset((a, b, a ^ b)) for a, b in combinations(points, 2)}
    complements = tuple(sorted((points - line for line in fano_lines), key=lambda d: sorted(d)))
    assert len(complements) == 7
    assert {len(d) for d in complements} == {4}
    assert {len(d & e) for d, e in combinations(complements, 2)} == {2}
    assert {sum(point in d for d in complements) for point in points} == {4}
    assert {sum(first in d and second in d for d in complements)
            for first, second in combinations(points, 2)} == {2}
    # A concrete capacity and balance check. This is type data, not the
    # high-girth matching or protected-root construction.
    m = 13
    a_count, b_count = (33 * m - 1) // 4, 33 * (m - 1) // 4
    assert 4 * a_count + 1 == 33 * m
    assert 4 * b_count == 33 * (m - 1)
    assert 7 * math.ceil(a_count / 1057) + 1 < m - 1
    assert 7 * math.ceil(b_count / 1057) < m - 1
    return {
        "complements": [sorted(d) for d in complements],
        "capacity_coefficient": str(F(7 * 33, 4 * 1057)),
        "sample_admissible_m": m,
        "sample_a_count": a_count,
        "sample_b_count": b_count,
        "minimum_degree": 33,
        "maximum_degree": 40,
        "post_deletion_minimum_degree": 31,
        "expansion_exponent": str(F(33, 2) - 2),
        "small_k_expansion_exponent": str((F(33, 2) - 2) / 2),
    }


def constant_checks():
    c0 = F(1, 100)
    p = F(33, 1057)
    lam = F(987, 1000)
    delta = -math.log(float(lam)) / 4
    a0 = 2 * math.log(33)
    original_row1 = F(32, 33) + 7 * p * p + F(21, 33**2)
    original_row2 = F(6, 4) + (1057 + 21) * p * p
    assert original_row1 < 1 and original_row2 < 4
    # Integer and rational checks underpin the logarithmic assertions;
    # the displayed floating-point values are not needed for these proofs.
    assert F(2 * 1064, 1) / p < 2**17
    assert 40 < 2**6
    assert c0 * 17 < 1 and 2 * c0 * 6 < 1
    return {
        "c0": str(c0),
        "girth_log_bound": float(c0) * math.log(float(2 * 1064 / p)),
        "switching_log_bound": float(2 * c0) * math.log(40),
        "lambda": str(lam),
        "delta_decimal_for_display_only": delta,
        "a0_decimal_for_display_only": a0,
        "epsilon_decimal_for_display_only": min(1 / 4, delta / (16 * (1 + a0))),
        "source_original_crude_first_row": str(original_row1),
        "source_original_crude_second_row": str(original_row2),
        "exact_girth_sufficient_bound": "2*1064/(33/1057)=2249296/33 < 2^17 < exp(17); c0*17=17/100<1",
        "exact_switching_sufficient_bound": "40<2^6<exp(6); 2*c0*6=3/25<1",
    }


def main():
    constants = constant_checks()
    assert constants["girth_log_bound"] < 1
    assert constants["switching_log_bound"] < 1
    files = [SOURCE / "sections" / (name + ".tex") for name in
             ("introduction", "random", "patterns", "planar", "algebra", "topology", "assembly")]
    result = {
        "status": "all_independent_checks_passed",
        "scope": "fixed type data and exact matrix certificates; no numeric group-ring witness",
        "source_sha256": {str(path.relative_to(PROJECT)): sha256(path.read_bytes()).hexdigest() for path in files},
        "certificates": rational_certificates(),
        "field_and_plane": field_and_plane32(),
        "fano_and_types": fano_and_type_checks(),
        "constants": constants,
    }
    path = HERE / "parameter32_checks.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "receipt": str(path),
                      "plane": result["field_and_plane"], "constants": constants}, indent=2))


if __name__ == "__main__":
    main()
