#!/usr/bin/env python3
"""Exact checker for cyclic 41-vector real harmonic UNTFs in R^5."""

from __future__ import annotations

from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys


sys.set_int_max_str_digits(0)


ORDER = 41
DIMENSION = 5
FREQUENCIES = range(1, 21)
ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = (
    ROOT
    / "experiments"
    / "construction_round8_tight_frames"
    / "results"
    / "cyclic_exhaustive.json"
)


def arctangent_bounds(inverse: int, terms: int) -> tuple[Q, Q]:
    x = Q(1, inverse)
    partial = sum(
        (
            (-1 if index % 2 else 1)
            * x ** (2 * index + 1)
            / (2 * index + 1)
            for index in range(terms)
        ),
        Q(0),
    )
    next_magnitude = x ** (2 * terms + 1) / (2 * terms + 1)
    if terms % 2 == 0:
        return partial, partial + next_magnitude
    return partial - next_magnitude, partial


def pi_bounds(terms_5: int, terms_239: int) -> tuple[Q, Q]:
    a_lower, a_upper = arctangent_bounds(5, terms_5)
    b_lower, b_upper = arctangent_bounds(239, terms_239)
    return 16 * a_lower - 4 * b_upper, 16 * a_upper - 4 * b_lower


def cosine_at_rational_bounds(x: Q, terms: int) -> tuple[Q, Q]:
    assert 0 <= x < Q(22, 7)
    partial = sum(
        (
            (-1 if index % 2 else 1)
            * x ** (2 * index)
            / math.factorial(2 * index)
            for index in range(terms)
        ),
        Q(0),
    )
    next_magnitude = x ** (2 * terms) / math.factorial(2 * terms)
    if terms % 2 == 0:
        return partial, partial + next_magnitude
    return partial - next_magnitude, partial


def cosine_residue_bounds(
    residue: int,
    pi_interval: tuple[Q, Q],
    cosine_terms: int,
) -> tuple[Q, Q]:
    residue %= ORDER
    residue = min(residue, ORDER - residue)
    if residue == 0:
        return Q(1), Q(1)
    assert 1 <= residue <= 20
    pi_lower, pi_upper = pi_interval
    x_lower = Q(2 * residue, ORDER) * pi_lower
    x_upper = Q(2 * residue, ORDER) * pi_upper
    lower, _ = cosine_at_rational_bounds(x_upper, cosine_terms)
    _, upper = cosine_at_rational_bounds(x_lower, cosine_terms)
    return lower, upper


def pair_inner_product_bounds(
    a: int,
    b: int,
    difference: int,
    cosine_bounds: dict[int, tuple[Q, Q]],
) -> tuple[Q, Q]:
    residues = []
    for frequency in (a, b):
        residue = frequency * difference % ORDER
        residues.append(min(residue, ORDER - residue))
    first = cosine_bounds[residues[0]]
    second = cosine_bounds[residues[1]]
    return (
        (Q(1) + 2 * first[0] + 2 * second[0]) / DIMENSION,
        (Q(1) + 2 * first[1] + 2 * second[1]) / DIMENSION,
    )


def minimax_interval(
    a: int,
    b: int,
    cosine_bounds: dict[int, tuple[Q, Q]],
) -> tuple[Q, Q, list[int]]:
    values = [
        pair_inner_product_bounds(a, b, difference, cosine_bounds)
        for difference in range(1, 21)
    ]
    lower = max(item[0] for item in values)
    upper = max(item[1] for item in values)
    possible_maximizers = [
        difference
        for difference, (_low, high) in enumerate(values, start=1)
        if high >= lower
    ]
    return lower, upper, possible_maximizers


def sign_switch_obstruction_difference(
    a: int,
    b: int,
    cosine_bounds: dict[int, tuple[Q, Q]],
) -> int:
    """Return a difference whose whole exact interval lies above 1/2."""
    for difference in range(1, (ORDER + 1) // 2):
        lower, _upper = pair_inner_product_bounds(
            a, b, difference, cosine_bounds
        )
        if lower > Q(1, 2):
            return difference
    raise AssertionError("no exact odd-cycle sign-switch obstruction")


def reduced_frequency(value: int) -> int:
    value %= ORDER
    return min(value, ORDER - value)


def orbit(pair: tuple[int, int]) -> set[tuple[int, int]]:
    a, b = pair
    return {
        tuple(
            sorted(
                (
                    reduced_frequency(multiplier * a),
                    reduced_frequency(multiplier * b),
                )
            )
        )
        for multiplier in range(1, 21)
    }


def verify(result_path: Path = RESULT_PATH) -> dict[str, object]:
    data = json.loads(result_path.read_text())
    assert data["schema"] == "cyclic-real-harmonic-untf-41x5-v2"
    assert data["order"] == ORDER
    assert data["dimension"] == DIMENSION
    assert data["pi_method"] == "Machin directed alternating series"
    settings = data["interval_settings"]
    assert settings == {
        "atan_1_over_5_terms": 20,
        "atan_1_over_239_terms": 6,
        "cosine_terms": 20,
    }

    pi_interval = pi_bounds(
        settings["atan_1_over_5_terms"],
        settings["atan_1_over_239_terms"],
    )
    assert Q(3) < pi_interval[0] < pi_interval[1] < Q(22, 7)
    cosine_bounds = {
        residue: cosine_residue_bounds(
            residue, pi_interval, settings["cosine_terms"]
        )
        for residue in range(21)
    }

    entries = data["pairs"]
    assert len(entries) == math.comb(20, 2) == 190
    seen = set()
    recomputed = {}
    for entry in entries:
        a, b = entry["frequencies"]
        assert 1 <= a < b <= 20
        assert (a, b) not in seen
        seen.add((a, b))
        lower, upper, maximizers = minimax_interval(
            a, b, cosine_bounds
        )
        assert Q(entry["maximum_lower"]) == lower
        assert Q(entry["maximum_upper"]) == upper
        assert entry["possible_maximizing_differences"] == maximizers
        assert lower > Q(1, 2)
        witness = sign_switch_obstruction_difference(
            a, b, cosine_bounds
        )
        assert entry["sign_switch_obstruction_difference"] == witness
        witness_lower, _witness_upper = pair_inner_product_bounds(
            a, b, witness, cosine_bounds
        )
        assert witness_lower > Q(1, 2)

        # If row j is multiplied by s_j in {+1,-1}, this positive Gram
        # entry forces s_{j+witness}=-s_j for every j.  Since 41 is prime,
        # the nonzero witness generates all residues.  The resulting cycle
        # has odd length 41, so its product of edge relations is -1 rather
        # than the necessary +1.
        cycle = [(step * witness) % ORDER for step in range(ORDER)]
        assert len(set(cycle)) == ORDER
        assert (ORDER * witness) % ORDER == 0
        assert (-1) ** ORDER == -1
        recomputed[(a, b)] = lower, upper, maximizers
    assert seen == {
        (a, b) for a in FREQUENCIES for b in FREQUENCIES if a < b
    }

    best_orbit = orbit((1, 9))
    assert len(best_orbit) == 10
    assert sorted(best_orbit) == [
        tuple(pair) for pair in data["globally_best_frequency_pairs"]
    ]
    best_lower, best_upper, _ = recomputed[(1, 9)]
    assert Q(data["global_optimum_lower"]) == best_lower
    assert Q(data["global_optimum_upper"]) == best_upper
    for pair in best_orbit:
        assert recomputed[pair][:2] == (best_lower, best_upper)
    assert all(
        recomputed[pair][0] > best_upper
        for pair in recomputed
        if pair not in best_orbit
    )
    assert best_lower > Q(1, 2)
    assert data["arbitrary_row_sign_flips_feasible_frequency_pairs"] == 0

    # Algebraic frame facts: the five coordinate characters are the
    # distinct frequencies 0,+/-a,+/-b modulo the prime order 41.  Character
    # orthogonality gives X^T X=(41/5)I exactly, while the displayed
    # cos/sin identity gives unit row norm exactly.
    assert all(
        len({0, a, ORDER - a, b, ORDER - b}) == DIMENSION
        for a, b in seen
    )

    return {
        "status": "PASS",
        "pairs_checked": len(entries),
        "feasible_pairs": 0,
        "switchable_frequency_pairs": 0,
        "odd_cycle_witnesses": len(entries),
        "globally_best_frequency_pairs": len(best_orbit),
        "global_optimum_lower": best_lower,
        "global_optimum_upper": best_upper,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        if isinstance(value, Q):
            value = f"{float(value):.18g}"
        print(f"{key}: {value}")
