#!/usr/bin/env python3
"""Offline arithmetic controls, not a proof of the moduli-space statement."""
import json
from pathlib import Path


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


def cover_genus(degree, quotient_genus, total_ramification):
    twice = degree * (2 * quotient_genus - 2) + total_ramification + 2
    assert twice % 2 == 0
    return twice // 2


def compute():
    assert 3 * 4 - 3 == 9
    assert 9 - 2 == 7
    assert cover_genus(2, 2, 2) == 4
    assert cover_genus(2, 4, 2) == 8
    triples = []
    # Hurwitz's bound |Aut(C)| <= 84(g-1) = 252 is only a finite control
    # cutoff here. The printed proof already forces h <= 2 and the same
    # short list by the equation itself.
    for p in range(2, 253):
        if not is_prime(p):
            continue
        for h in range(5):
            remainder = 6 - p * (2 * h - 2)
            if remainder >= 0 and remainder % (p - 1) == 0:
                triples.append([p, h, remainder // (p - 1)])
    expected = [[2,0,10],[2,1,6],[2,2,2],[3,0,6],[3,1,3],
                [3,2,0],[5,0,4],[7,1,1]]
    assert triples == expected
    assert all(h <= 2 for p, h, r in triples)
    assert all(a % 7 != 0 for a in range(1, 7))
    assert 7 - 7 == 0  # Boundary B intersected by seven hyperplanes.
    assert 7 - 8 < 0   # Eight general hyperplanes can avoid B.
    assert 10 - 8 == 2 and 9 - 8 == 1
    assert 8 - 4 == 4
    assert 2 - 2 * 2 == -2

    def must_reject(label, bad_test):
        try:
            assert bad_test
        except AssertionError:
            return label
        raise AssertionError("Negative control was not rejected: " + label)

    rejected = [
        must_reject("genus-four moduli dimension is not four", 3*4-3 == 4),
        must_reject("seven hyperplanes do not dimensionally avoid B", 7-7 < 0),
        must_reject("genus-eight double cover does not itself have genus four",
                    cover_genus(2,4,2) == 4),
        must_reject("a nonzero divisor section does not retain surface dimension", 2-1 == 2),
        must_reject("the smoothing normal degree is not positive", 2-2*2 > 0),
    ]
    return {
        "all_controls_passed": True,
        "target_solved": False,
        "moduli_dimension": 9,
        "surface_codimension": 7,
        "rh_arithmetic_possibilities": triples,
        "single_branch_case_excluded_by_monodromy": [7,1,1],
        "double_cover_genus": 4,
        "iterated_cover_genus": 8,
        "prym_dimension": 4,
        "satake_bad_locus_dimension": 7,
        "normal_degree_on_each_ruling": -2,
        "negative_controls_rejected": rejected,
        "scope": "Exact arithmetic only; no formal mathematical proof validation."
    }


if __name__ == "__main__":
    result = compute()
    expected_path = Path(__file__).with_name("CONTROL_RESULTS.json")
    if expected_path.exists():
        assert result == json.loads(expected_path.read_text())
    print(json.dumps(result, indent=2, sort_keys=True))
