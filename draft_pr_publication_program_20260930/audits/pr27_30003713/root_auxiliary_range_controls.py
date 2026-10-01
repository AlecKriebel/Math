#!/usr/bin/env python3
"""Exact independent boundary controls for the printed Powell v4 Lemma 5.2.

The root constructed these after the fresh adversary reported a boundary issue.
No family or author code is imported. This is finite evidence; the group
generation argument in ROOT_POWELL_RANGE_ADDENDUM.md supplies the used range.
"""
import itertools
import json
import math
from pathlib import Path
import sympy as s


def wedge_sign(triple, letter):
    if letter in triple:
        return None, 0
    quad = tuple(sorted(triple + (letter,)))
    return quad, (-1) ** sum(x > letter for x in triple)


def hook_dimension(partition, dimension):
    value = s.Rational(1)
    for i, row in enumerate(partition):
        for j in range(row):
            hook = row - j + sum(other > j for other in partition[i+1:])
            value *= s.Rational(dimension + j - i, hook)
    assert value.q == 1
    return int(value)


records = []
for dimension in (3, 4):
    triples = list(itertools.combinations(range(dimension), 3))
    quads = list(itertools.combinations(range(dimension), 4))
    columns = [(triple, a, b) for triple in triples
               for a in range(dimension) for b in range(dimension)]
    target = [(quad, letter) for quad in quads for letter in range(dimension)]
    matrix = s.zeros(2 * len(target), len(columns))
    for column, (triple, a, b) in enumerate(columns):
        for block, letter, other in [(0, a, b), (1, b, a)]:
            quad, sign = wedge_sign(triple, letter)
            if sign:
                matrix[block*len(target)+target.index((quad, other)), column] = sign
    actual = len(columns) - matrix.rank()
    claimed = hook_dimension((3, 1, 1), dimension)
    assert actual != claimed
    records.append({"dimension": dimension, "n": 2,
                    "two_face_intersection_dimension": actual,
                    "printed_claim_hook_dimension": claimed,
                    "printed_n2_statement_false": True})

# For n>=3, symmetry of the first n-1 slots and its last-slot swap generates
# symmetry of ALL n slots. On that symmetric intersection the two exterior
# constraints coincide. Calculate the remaining wedge map using the actual
# orbit-sum basis of Gamma^n, without a hook-dimension assertion as input.
for dimension, n in [(3, 3), (3, 4), (4, 3), (4, 4)]:
    triples = list(itertools.combinations(range(dimension), 3))
    quads = list(itertools.combinations(range(dimension), 4))
    multisets = list(itertools.combinations_with_replacement(range(dimension), n))
    target = [(quad, word) for quad in quads
              for word in itertools.product(range(dimension), repeat=n-1)]
    columns = [(triple, multiset) for triple in triples for multiset in multisets]
    matrix = s.zeros(len(target), len(columns))
    for column, (triple, multiset) in enumerate(columns):
        for word in set(itertools.permutations(multiset)):
            quad, sign = wedge_sign(triple, word[0])
            if sign:
                matrix[target.index((quad, word[1:])), column] += sign
    actual = len(columns) - matrix.rank()
    expected = hook_dimension((n+1, 1, 1), dimension)
    assert actual == expected
    records.append({"dimension": dimension, "n": n,
                    "symmetric_intersection_wedge_kernel_dimension": actual,
                    "hook_dimension": expected, "used_range_check": True})

result = {"status": "passed", "arithmetic": "exact integer matrices and rational hook products",
          "records": records, "full_all_degree_homology_solved": False,
          "scope": "n2 printed auxiliary claim refuted; finite n>=3 controls supplement universal group-generation proof. Theorem1 induction uses r>3 and n=r-1>=3, with r3 separately proved."}
Path(__file__).with_name('root_auxiliary_range_results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
