#!/usr/bin/env python3
"""Exact orientation count for the delayed E1-origin equation.

For profile h2-422220-0 the 42 grouped terms of E1(origin), after dividing
their common factor 3, split over 22 disjoint local blocks as

    -sum_{i=1}^{12} omega**a_i
      + (1-omega) sum_{j=1}^{10} omega**b_j.

Each a_i and b_j independently has three orientations.  This verifier
derives that reduction from the actual phase forms, counts exact solutions
by two independent finite dynamic programs, and emits all admissible pairs
of orientation histograms.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from math import factorial
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import solve_lambda_prefix_sat as prefix  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


ROOTS = ((1, 0), (0, 1), (-1, -1))
LAMBDA_ROOTS = ((1, -1), (1, 2), (-2, -1))
EXPECTED_ORIENTATION_SOLUTIONS = 596_095_200


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def compositions(total: int):
    for first in range(total + 1):
        for second_value in range(total - first + 1):
            yield first, second_value, total - first - second_value


def multinomial(counts) -> int:
    result = factorial(sum(counts))
    for value in counts:
        result //= factorial(value)
    return result


def weighted_sum(counts, values):
    return tuple(
        sum(count * value[coordinate] for count, value in zip(counts, values))
        for coordinate in range(2)
    )


def derive_local_blocks():
    candidate = second.CANDIDATES[1]
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    target, grouped = prefix.grouped_term_rows(profiles)[7]
    if target != 0 or len(grouped) != 42:
        raise AssertionError("the E1-origin grouped row changed")
    coordinates = second.active_trit_coordinates(profiles)
    blocks = defaultdict(list)
    for form, multiplicity in grouped:
        if multiplicity not in (-3, 3):
            raise AssertionError("a multiplicity left +/-3")
        touched = {
            coordinates[variable][:2] for variable, _ in form[1]
        }
        if len(touched) != 1:
            raise AssertionError("a term crossed local blocks")
        blocks[next(iter(touched))].append((form, multiplicity // 3))
    if Counter(map(len, blocks.values())) != Counter({1: 12, 3: 10}):
        raise AssertionError("the local block sizes changed")

    singleton_catalogs = Counter()
    triple_catalogs = Counter()
    for block in blocks.values():
        variables = tuple(
            sorted(
                {
                    variable
                    for (_, coefficients), _ in block
                    for variable, _ in coefficients
                }
            )
        )
        exact = Counter()
        for values in itertools.product(range(3), repeat=len(variables)):
            assignment = dict(zip(variables, values))
            result = [0, 0]
            for (constant, coefficients), epsilon in block:
                exponent = (
                    constant
                    + sum(
                        coefficient * assignment[variable]
                        for variable, coefficient in coefficients
                    )
                ) % 3
                result[0] += epsilon * ROOTS[exponent][0]
                result[1] += epsilon * ROOTS[exponent][1]
            exact[tuple(result)] += 1
        if len(block) == 1:
            singleton_catalogs[tuple(sorted(exact.items()))] += 1
        else:
            triple_catalogs[tuple(sorted(exact.items()))] += 1

    expected_singleton = tuple(
        sorted(((-first, -second_value), 3) for first, second_value in ROOTS)
    )
    expected_triple = tuple(sorted((value, 9) for value in LAMBDA_ROOTS))
    if singleton_catalogs != Counter({expected_singleton: 12}):
        raise AssertionError("the singleton exact catalog changed")
    if triple_catalogs != Counter({expected_triple: 10}):
        raise AssertionError("the three-cycle exact catalog changed")
    return blocks


def composition_count():
    admissible = []
    total = 0
    for singleton_counts in compositions(12):
        singleton_sum = weighted_sum(singleton_counts, ROOTS)
        for triple_counts in compositions(10):
            triple_sum = weighted_sum(triple_counts, LAMBDA_ROOTS)
            if tuple(
                -singleton_sum[index] + triple_sum[index]
                for index in range(2)
            ) != (0, 0):
                continue
            orientations = (
                multinomial(singleton_counts) * multinomial(triple_counts)
            )
            total += orientations
            admissible.append(
                {
                    "singleton_counts": singleton_counts,
                    "three_cycle_counts": triple_counts,
                    "orientations": orientations,
                }
            )
    return total, tuple(admissible)


def direct_dp_count() -> tuple[int, int]:
    states = {(0, 0): 1}
    for _ in range(12):
        following = defaultdict(int)
        for state, multiplicity in states.items():
            for root in ROOTS:
                following[
                    (state[0] - root[0], state[1] - root[1])
                ] += multiplicity
        states = dict(following)
    singleton_state_count = len(states)
    for _ in range(10):
        following = defaultdict(int)
        for state, multiplicity in states.items():
            for root in LAMBDA_ROOTS:
                following[
                    (state[0] + root[0], state[1] + root[1])
                ] += multiplicity
        states = dict(following)
    return states.get((0, 0), 0), singleton_state_count


def audit() -> dict[str, object]:
    blocks = derive_local_blocks()
    composition_total, admissible = composition_count()
    dp_total, intermediate_states = direct_dp_count()
    if not (
        composition_total
        == dp_total
        == EXPECTED_ORIENTATION_SOLUTIONS
    ):
        raise AssertionError("the exact orientation count changed")
    if len(admissible) != 30:
        raise AssertionError("the admissible histogram-pair count changed")
    total_orientations = 3**22
    result = {
        "schema": "lp333-order3-e1-origin-exact-dp-v1",
        "label": second.CANDIDATES[1][0],
        "displayed_row": 7,
        "local_blocks": len(blocks),
        "exact_reduction": (
            "-sum_(i=1)^12 omega^a_i "
            "+(1-omega)sum_(j=1)^10 omega^b_j=0"
        ),
        "orientation_space": total_orientations,
        "exact_orientation_solutions": composition_total,
        "exact_fraction_numerator": composition_total,
        "exact_fraction_denominator": total_orientations,
        "decimal_fraction": composition_total / total_orientations,
        "admissible_histogram_pairs": len(admissible),
        "composition_pairs_tested": 91 * 66,
        "independent_dp_intermediate_states": intermediate_states,
        "admissible_pairs": admissible,
    }
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
