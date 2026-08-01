#!/usr/bin/env python3
"""Exact dense block census for the final-slot DTH crossing.

This companion to ``agent_dth_last_crossing_exact.py`` forms the rational
highest-weight crossing ``C_5 = B_5 A^{-1}`` with SymPy exact arithmetic and
checks its reduced denominator, support, and every target/source block rank.
The bridge verifier remains the smaller way to apply the map; this file makes
the invariant block action explicit and auditable.
"""

from functools import reduce
import math
import sys

import sympy as sp

sys.path.insert(0, "verification")
import agent_dth_last_crossing_exact as last
import agent_dth_local_crossing_exact as bridge


EXPECTED_RANKS = (
    (1, 1, 0, 0, 0),
    (1, 16, 9, 9, 0),
    (0, 9, 9, 9, 0),
    (0, 9, 25, 36, 25),
    (0, 0, 4, 0, 4),
    (0, 0, 0, 9, 9),
)

EXPECTED_NONZEROS = (
    (1, 16, 0, 0, 0),
    (16, 256, 324, 324, 0),
    (0, 25, 100, 169, 0),
    (0, 169, 676, 1156, 952),
    (0, 0, 4, 0, 36),
    (0, 0, 0, 9, 9),
)


def ranges(multiplicities):
    output = []
    offset = 0
    for multiplicity in multiplicities:
        output.append((offset, offset + multiplicity * multiplicity))
        offset += multiplicity * multiplicity
    assert offset == 103
    return output


def main():
    holomorphic, target, _, _ = last.exact_last_restriction_bridge()
    hol_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, holomorphic
    )
    target_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, target
    )
    inverse_numerator, denominator = hol_domain.inv_den()
    numerator = (target_domain * inverse_numerator).to_Matrix()
    common = reduce(math.gcd,
                    [abs(int(value)) for value in numerator if value]
                    + [int(denominator)])
    denominator = int(denominator) // common
    numerator = numerator.applyfunc(lambda value: value / common)

    assert denominator == 14_400
    assert all(value.q == 1 for value in numerator)
    assert sum(bool(value) for value in numerator) == 4_242
    assert max(abs(int(value)) for value in numerator) == 86_400

    source_ranges = ranges(bridge.HOL_MULTS)
    target_ranges = ranges(last.LAST_MULTS)
    ranks = []
    nonzeros = []
    for row_start, row_stop in target_ranges:
        rank_row = []
        nonzero_row = []
        for column_start, column_stop in source_ranges:
            block = numerator[row_start:row_stop, column_start:column_stop]
            rank_row.append(block.rank())
            nonzero_row.append(sum(bool(value) for value in block))
        ranks.append(tuple(rank_row))
        nonzeros.append(tuple(nonzero_row))
    assert tuple(ranks) == EXPECTED_RANKS
    assert tuple(nonzeros) == EXPECTED_NONZEROS

    print("exact final-slot crossing block census passed")
    print("C_5 = numerator /", denominator)
    print("dense numerator nonzeros / max absolute:", 4242, "/", 86400)
    print("rows:", last.LAST_DYNKIN_WEIGHTS)
    print("columns:", bridge.HOL_SHAPES)
    print("exact block ranks:")
    for weight, row in zip(last.LAST_DYNKIN_WEIGHTS, ranks):
        print(" ", weight, row)


if __name__ == "__main__":
    main()
