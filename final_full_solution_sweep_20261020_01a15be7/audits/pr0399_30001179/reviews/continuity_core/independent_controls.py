#!/usr/bin/env python3
"""Independent exact finite support/adjoint controls; no infinite-proof certification."""
from bisect import bisect_right
from fractions import Fraction as F
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def nonincreasing(word):
    return all(a >= b for a, b in zip(word, word[1:]))


def runwise_decreasing(word, cuts):
    colors = [bisect_right(cuts, x) for x in word]
    return all(colors[i] != colors[i + 1] or word[i] > word[i + 1]
               for i in range(len(word) - 1))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def scale(a, value):
    return tuple(x * value for x in a)


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def unit(u):
    return ((1 - u * u) / (1 + u * u), 2 * u / (1 + u * u))


def calculate():
    labels = tuple(F(i, 6) for i in range(1, 6))
    all_cuts = tuple((a + b) / 2 for a, b in zip(labels, labels[1:]))
    partitions = [c for size in range(len(all_cuts) + 1)
                  for c in combinations(all_cuts, size)]
    core_words = 0
    partition_tests = 0
    free_cover_words = 0
    tensor_core_words = 0
    for m in range(7):
        for word in product(labels, repeat=m):
            accepts_all = True
            for cuts in partitions:
                colors = tuple(bisect_right(cuts, x) for x in word)
                accepts_all &= nonincreasing(colors)
                partition_tests += 1
            expected = nonincreasing(word)
            require(accepts_all == expected, 'Partition intersection differs from label order')
            core_words += 1
            tensor_core_words += int(expected)
            if len(set(word)) == len(word):
                require(runwise_decreasing(word, all_cuts), 'Separated tuple not in free hull support')
                free_cover_words += 1
    # A sole coarse cut misses a genuine rise: multiple/dense cuts are essential.
    rising = (F(1, 6), F(2, 6))
    require(nonincreasing(tuple(bisect_right((F(3, 4),), x) for x in rising)),
            'Coarse-cut negative control did not pass')
    require(not nonincreasing(rising), 'Rising negative control malformed')
    # The unrestricted free hull is strictly larger than its ordered tensor core.
    require(runwise_decreasing(rising, all_cuts), 'Free hull must include separated rising tuple')
    # Ties can violate strict-run membership; the analytic proof excludes diagonals a.e.
    tied = (F(1, 6), F(1, 6))
    require(nonincreasing(tied) and not runwise_decreasing(tied, all_cuts),
            'Tie boundary control malformed')
    # Exact norm-square identity for rank-one partial isometries V=p*q^T.
    angles = tuple(F(i, 3) for i in range(-3, 4))
    maps = [(unit(u), unit(v)) for u in angles for v in angles]
    vectors = [(F(1), F(0)), (F(0), F(1)), (F(2, 3), F(-5, 7))]
    adjoint_checks = 0
    for p, q in maps:
        require(dot(p, p) == 1 and dot(q, q) == 1, 'Rational unit vector invalid')
        for old_p, old_q in maps:
            for h in vectors:
                current = scale(q, dot(p, h))
                previous = scale(old_q, dot(old_p, h))
                lhs = dot(subtract(current, previous), subtract(current, previous))
                rhs = dot(p, h) ** 2 + dot(old_p, h) ** 2
                rhs -= 2 * dot(p, h) * dot(q, old_q) * dot(old_p, h)
                require(lhs == rhs, 'Adjoint norm-square identity failed')
                adjoint_checks += 1
    zero_checks = 0
    for m in range(1, 7):
        for n in range(1, 65):
            projected_norm_square = F(1, n) ** m
            require(projected_norm_square <= F(1, n), 'Zero-time projection bound failed')
            zero_checks += 1
    # Uniform Chebyshev union bound for the infinite-sector properness event.
    bound = F(3, 625)
    properness_checks = 0
    for terms in range(1, 25):
        partial = sum((F(9, 2500 * 4 ** j) for j in range(terms)), F(0))
        require(partial == bound * (1 - F(1, 4 ** terms)), 'Tail bound geometric identity failed')
        require(partial < bound < 1, 'Positive-probability bound failed')
        properness_checks += 1
    return {
        'status': 'PASS',
        'rational_labels': 5,
        'maximum_finite_word_length': 6,
        'all_grid_partitions': len(partitions),
        'finite_words': core_words,
        'individual_partition_membership_tests': partition_tests,
        'nonincreasing_core_words': tensor_core_words,
        'distinct_coordinate_free_hull_cover_cases': free_cover_words,
        'exact_adjoint_identity_checks': adjoint_checks,
        'zero_time_norm_bound_checks': zero_checks,
        'properness_geometric_bound_checks': properness_checks,
        'infinite_gaussian_failure_bound': str(bound),
        'uniform_success_lower_bound': str(1 - bound),
        'successful_parameter_measure_lower_bound_in_units_t_log2': str((1 - bound) / 3),
        'negative_controls': ['single_coarse_cut_accepts_a_rise',
                              'free_hull_contains_rising_tuple_outside_tensor_core',
                              'tie_diagonal_requires_a.e._qualification'],
        'scope': 'Exact finite controls and an elementary bound; infinite-dimensional continuity, measure theory and a.e. arguments are proved analytically in the reconstruction.'
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2, sort_keys=True))
