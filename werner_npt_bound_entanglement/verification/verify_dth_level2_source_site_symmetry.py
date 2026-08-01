#!/usr/bin/env python3
"""Exact source-site symmetry census for the degree-three DTH lift.

The source consists of ordered triples of local S_7 shapes.  Physical-site
S_3 permutes those triples.  This verifier computes the stabilizer characters
on every post-Omega multiplicity space and hence the exact PSD-cone
decomposition of the invariant source.

Only Python standard-library arithmetic is used.  Character arithmetic is
imported from the independent exact S_7 census verifier.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import gcd

import verify_dth_level2_s7_census as census


S7 = tuple(census.partitions(7, max_parts=3))
S4 = ((4,), (3, 1), (2, 2), (2, 1, 1))
OMEGA_LOCAL = {3: 0, 5: 1, 6: 2, 7: 3}


def powered_cycle_type(cycle_type, power):
    out = []
    for length in cycle_type:
        common = gcd(length, power)
        out.extend([length // common] * common)
    return tuple(sorted(out, reverse=True))


def character(shape, cycle_type):
    return census.symmetric_group_character(shape, cycle_type)


def power_trace_average(degree, target, repeated, singleton=None,
                        power=2, lifted=False):
    """Character average for a site-cycle acting on tensor factors.

    A transposition of two equal factors contributes chi(g^2) chi_b(g).
    A three-cycle of three equal factors contributes chi(g^3).
    ``lifted`` appends the fixed z replica to an S_6 cycle type before
    evaluating the restricted S_7 character.
    """
    answer = Fraction(0)
    for cycle_type in census.partitions(degree):
        powered = powered_cycle_type(cycle_type, power)
        if lifted:
            powered += (1,)
            ordinary = tuple(cycle_type) + (1,)
        else:
            ordinary = cycle_type
        numerator = character(target, cycle_type) * character(
            repeated, powered
        )
        if singleton is not None:
            numerator *= character(singleton, ordinary)
        answer += Fraction(numerator, census.class_denominator(cycle_type))
    assert answer.denominator == 1
    return answer.numerator


def omega_rank(shapes):
    if any(index not in OMEGA_LOCAL for index in shapes):
        return 0
    return census.kronecker_coefficient(
        (2, 2), [S4[OMEGA_LOCAL[index]] for index in shapes], 4
    )


def post_omega_rank(shapes):
    return census.kronecker_coefficient(
        (3, 3), [S7[index] for index in shapes], 6
    ) - omega_rank(shapes)


def swap_trace(repeated, singleton):
    source = power_trace_average(
        6, (3, 3), S7[repeated], S7[singleton], power=2, lifted=True
    )
    if repeated not in OMEGA_LOCAL or singleton not in OMEGA_LOCAL:
        return source
    omega = power_trace_average(
        4, (2, 2), S4[OMEGA_LOCAL[repeated]],
        S4[OMEGA_LOCAL[singleton]], power=2, lifted=False
    )
    return source - omega


def cycle_trace(shape):
    source = power_trace_average(
        6, (3, 3), S7[shape], power=3, lifted=True
    )
    if shape not in OMEGA_LOCAL:
        return source
    omega = power_trace_average(
        4, (2, 2), S4[OMEGA_LOCAL[shape]], power=3, lifted=False
    )
    return source - omega


def invariant_components(shapes):
    """Return type and PSD component ranks for one unordered source orbit."""
    multiplicity = post_omega_rank(shapes)
    if not multiplicity:
        return None
    distinct = len(set(shapes))
    if distinct == 3:
        return "abc", (multiplicity,)
    if distinct == 2:
        repeated = next(index for index in shapes if shapes.count(index) == 2)
        singleton = next(index for index in shapes if shapes.count(index) == 1)
        trace = swap_trace(repeated, singleton)
        assert (multiplicity + trace) % 2 == 0
        components = (
            (multiplicity + trace) // 2,
            (multiplicity - trace) // 2,
        )
        assert sum(components) == multiplicity
        return "aab", tuple(value for value in components if value)

    shape = shapes[0]
    transposition_trace = swap_trace(shape, shape)
    three_cycle_trace = cycle_trace(shape)
    trivial = (
        multiplicity + 3 * transposition_trace + 2 * three_cycle_trace
    ) // 6
    sign = (
        multiplicity - 3 * transposition_trace + 2 * three_cycle_trace
    ) // 6
    standard = (multiplicity - three_cycle_trace) // 3
    assert trivial + sign + 2 * standard == multiplicity
    return "aaa", tuple(
        value for value in (trivial, sign, standard) if value
    )


def main():
    rows = []
    components = []
    for shapes in combinations_with_replacement(range(8), 3):
        result = invariant_components(shapes)
        if result is None:
            continue
        kind, ranks = result
        rows.append((shapes, post_omega_rank(shapes), kind, ranks))
        components.extend(ranks)

    assert len(rows) == 112
    assert Counter(row[2] for row in rows) == Counter({
        "abc": 55, "aab": 50, "aaa": 7,
    })
    assert len(components) == 171
    assert sum(components) == 3665
    assert max(components) == 106
    assert sum(rank * (rank + 1) // 2 for rank in components) == 87540
    assert sum(rank ** 3 for rank in components) == 11060723

    ordered_variables = sum(
        post_omega_rank(shapes) * (post_omega_rank(shapes) + 1) // 2
        for shapes in product(range(8), repeat=3)
    )
    assert ordered_variables == 519434

    all_equal = {
        shapes[0]: (multiplicity, ranks)
        for shapes, multiplicity, kind, ranks in rows if kind == "aaa"
    }
    assert all_equal == {
        1: (1, (1,)),
        2: (23, (6, 3, 7)),
        3: (26, (7, 3, 8)),
        4: (23, (7, 2, 7)),
        5: (298, (55, 47, 98)),
        6: (65, (15, 8, 21)),
        7: (62, (11, 11, 20)),
    }

    # Pin the complete orbit table without inflating this verifier with 112
    # literal rows.  The representation is deterministic and consists only
    # of tuples of small integers and the three type labels above.
    digest = sha256(repr(rows).encode("ascii")).hexdigest()
    assert digest == "b9e501fb43d44a2711f10fd752111d6c028d3e167cdc99fdafcaaa4d7bc5952e"

    print("exact degree-three source S3 census passed")
    print("ordered blocks / active orbits:", 487, len(rows))
    print("PSD components / rank sum:", len(components), sum(components))
    print("invariant symmetric variables:", 87540)
    print("maximum component rank / cube sum:", max(components),
          sum(rank ** 3 for rank in components))


if __name__ == "__main__":
    main()
