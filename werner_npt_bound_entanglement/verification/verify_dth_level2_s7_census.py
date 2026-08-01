#!/usr/bin/env python3
"""Exact character census for the degree-three DTH moment lift.

The seven replicas are grouped as three copies of a bivector and one copy of
z.  Quotienting the Pluecker ideal puts the first six replicas in the
S_(3,3) module.  This verifier computes, using only integer/Fraction
arithmetic,

* every local S_7 Schur--Weyl carrier and Specht multiplicity;
* the reduced multiplicity rank of S_(3,3)(H) tensor H in each local triple;
* the target ranks of the prolonged Omega map to S_(2,2)(H);
* the ordinary two-box S_7 -> S_5 branching table relevant to contraction;
* the smallest union of level-two blocks that can feed the recorded negative
  five-replica sectors.

No floating point arithmetic or third-party package is used.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations, product
from math import factorial


def partitions(n, max_parts=None, ceiling=None):
    """Partitions of n as decreasing positive tuples."""
    if max_parts is None:
        max_parts = n
    if ceiling is None:
        ceiling = n

    def rec(left, cap, slots, prefix):
        if left == 0:
            yield tuple(prefix)
            return
        if slots == 0:
            return
        for first in range(min(cap, left), 0, -1):
            yield from rec(left - first, first, slots - 1, prefix + [first])

    yield from rec(n, ceiling, max_parts, [])


def pad(shape, length=3):
    return tuple(shape) + (0,) * (length - len(shape))


def permutation_sign(p):
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def symmetric_group_character(shape, cycle_type, variables=3):
    """Frobenius coefficient formula for chi^shape(cycle_type).

    It is the coefficient of x^(shape+delta) in
        Delta(x) product_j p_{cycle_type[j]}(x),
    where Delta = product_{i<j}(x_i-x_j).
    """
    lam = pad(shape, variables)
    delta = tuple(variables - 1 - i for i in range(variables))
    target = tuple(lam[i] + delta[i] for i in range(variables))

    polynomial = defaultdict(int)
    for perm in permutations(range(variables)):
        exponent = tuple(delta[perm[i]] for i in range(variables))
        polynomial[exponent] += permutation_sign(perm)

    for degree in cycle_type:
        updated = defaultdict(int)
        for exponent, coefficient in polynomial.items():
            for i in range(variables):
                new_exp = list(exponent)
                new_exp[i] += degree
                if all(new_exp[j] <= target[j] for j in range(variables)):
                    updated[tuple(new_exp)] += coefficient
        polynomial = updated
    return polynomial[target]


def class_denominator(cycle_type):
    counts = Counter(cycle_type)
    answer = 1
    for cycle_length, multiplicity in counts.items():
        answer *= cycle_length ** multiplicity * factorial(multiplicity)
    return answer


def specht_dimension(shape):
    n = sum(shape)
    hooks = 1
    for i, row_length in enumerate(shape):
        for j in range(row_length):
            below = sum(j < shape[k] for k in range(i + 1, len(shape)))
            hooks *= row_length - j + below
    return factorial(n) // hooks


def schur_dimension(shape, ambient_dimension):
    answer = Fraction(1)
    for i, row_length in enumerate(shape):
        for j in range(row_length):
            below = sum(j < shape[k] for k in range(i + 1, len(shape)))
            hook = row_length - j + below
            answer *= Fraction(ambient_dimension + j - i, hook)
    assert answer.denominator == 1
    return answer.numerator


def gl3_dimension(shape):
    lam = pad(shape, 3)
    answer = Fraction(1)
    for i in range(3):
        for j in range(i + 1, 3):
            answer *= Fraction(lam[i] - lam[j] + j - i, j - i)
    assert answer.denominator == 1
    return answer.numerator


def kronecker_coefficient(target, factors, degree):
    """<chi^target, product chi^factor> in S_degree.

    A factor may be a partition of ``degree + 1``.  In that case its
    character is first restricted from S_(degree+1) to the subgroup fixing
    the final letter, so its cycle type is ``cycle_type + (1,)``.
    """
    answer = Fraction(0)
    for cycle_type in partitions(degree):
        numerator = symmetric_group_character(target, cycle_type)
        for shape in factors:
            if sum(shape) == degree:
                restricted_cycle_type = cycle_type
            else:
                assert sum(shape) == degree + 1
                restricted_cycle_type = tuple(cycle_type) + (1,)
            numerator *= symmetric_group_character(shape, restricted_cycle_type)
        answer += Fraction(numerator, class_denominator(cycle_type))
    assert answer.denominator == 1
    return answer.numerator


def removable_shapes(shape):
    out = []
    for i in range(len(shape)):
        if i + 1 < len(shape) and shape[i] == shape[i + 1]:
            continue
        candidate = list(shape)
        candidate[i] -= 1
        if candidate[i] == 0:
            candidate.pop(i)
        out.append(tuple(candidate))
    return out


def two_box_branching_paths(source, target):
    return sum(target in removable_shapes(mid) for mid in removable_shapes(source))


def cells(shape):
    return {(row, column) for row, length in enumerate(shape) for column in range(length)}


def two_box_strip_types(source, target):
    """S_5 x S_2 branching types H=[2], V=[1,1]."""
    source_cells = cells(source)
    target_cells = cells(target)
    removed = source_cells - target_cells
    if not target_cells <= source_cells or len(removed) != 2:
        return frozenset()
    out = set()
    if len({column for row, column in removed}) == 2:
        out.add("H")
    if len({row for row, column in removed}) == 2:
        out.add("V")
    return frozenset(out)


def orbit(seed):
    return set(permutations(seed))


def main():
    s7 = list(partitions(7, max_parts=3))
    expected_s7 = [
        (7,), (6, 1), (5, 2), (5, 1, 1),
        (4, 3), (4, 2, 1), (3, 3, 1), (3, 2, 2),
    ]
    assert s7 == expected_s7
    specht7 = [specht_dimension(shape) for shape in s7]
    carrier7 = [gl3_dimension(shape) for shape in s7]
    assert specht7 == [1, 6, 14, 15, 14, 35, 21, 21]
    assert carrier7 == [36, 48, 42, 15, 24, 15, 6, 3]
    assert sum(a * b for a, b in zip(specht7, carrier7)) == 3 ** 7
    assert sum(a * a for a in specht7) == 2761

    source_ranks = {}
    for triple in product(range(len(s7)), repeat=3):
        source_ranks[triple] = kronecker_coefficient(
            (3, 3), [s7[i] for i in triple], 6
        )

    assert sum(rank > 0 for rank in source_ranks.values()) == 487
    assert sum(source_ranks.values()) == 14572
    assert max(source_ranks.values()) == 300
    assert source_ranks[(5, 5, 5)] == 300
    assert sum(rank * (rank + 1) // 2 for rank in source_ranks.values()) == 526070
    assert sum(rank * rank for rank in source_ranks.values()) == 1037568

    full_source_dimension = sum(
        rank * carrier7[i] * carrier7[j] * carrier7[k]
        for (i, j, k), rank in source_ranks.items()
    )
    assert schur_dimension((3, 3), 27) == 2992626
    assert full_source_dimension == 27 * 2992626 == 80800902

    # The prolonged equation Omega(w,z) w^2 maps to S_(2,2)(H).  Locally,
    # epsilon contraction subtracts one determinant column (1,1,1), hence only
    # the four three-row S_7 shapes occur and map to the following S_4 shapes.
    s4_output = [(4,), (3, 1), (2, 2), (2, 1, 1)]
    omega_local_map = {3: 0, 5: 1, 6: 2, 7: 3}
    omega_output_ranks = {}
    after_omega_ranks = dict(source_ranks)
    for local_output in product(range(4), repeat=3):
        rank = kronecker_coefficient(
            (2, 2), [s4_output[i] for i in local_output], 4
        )
        omega_output_ranks[local_output] = rank
        local_input = tuple([3, 5, 6, 7][i] for i in local_output)
        assert source_ranks[local_input] >= rank
        after_omega_ranks[local_input] -= rank

    assert sum(rank > 0 for rank in omega_output_ranks.values()) == 39
    assert sum(omega_output_ranks.values()) == 61
    assert max(omega_output_ranks.values()) == 3
    assert sum(after_omega_ranks.values()) == 14511
    assert all(rank >= 0 for rank in after_omega_ranks.values())
    assert sum(rank > 0 for rank in after_omega_ranks.values()) == 487
    assert sum(rank * (rank + 1) // 2 for rank in after_omega_ranks.values()) == 519434
    assert sum(rank * rank for rank in after_omega_ranks.values()) == 1024357

    full_output_dimension = schur_dimension((2, 2), 27)
    assert full_output_dimension == 44226
    after_omega_dimension = sum(
        rank * carrier7[i] * carrier7[j] * carrier7[k]
        for (i, j, k), rank in after_omega_ranks.items()
    )
    assert after_omega_dimension == full_source_dimension - full_output_dimension
    assert after_omega_dimension == 80756676

    # Ordinary restriction from S_7 to S_5, with multiplicity equal to the
    # number of two-step paths in Young's lattice.
    s5 = [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1)]
    branch_table = {}
    expected_branch_table = {
        0: [(0, 1), (1, 2), (2, 1), (3, 1)],
        1: [(1, 1), (2, 2), (3, 2), (4, 1), (5, 2)],
        2: [(2, 1), (4, 2), (5, 2), (6, 2), (7, 1)],
        3: [(3, 1), (5, 2), (6, 1), (7, 1)],
        4: [(5, 1), (6, 1), (7, 2)],
    }
    for target_index, target in enumerate(s5):
        branch_table[target_index] = [
            (source_index, two_box_branching_paths(source, target))
            for source_index, source in enumerate(s7)
            if two_box_branching_paths(source, target)
        ]
    assert branch_table == expected_branch_table

    # Refinement by the S_2 type of the removed bivector pair.  The global
    # pair is antisymmetric, so a three-site contraction uses precisely the
    # channel triples containing an odd number of vertical (V) strips.
    strip_table = {
        target_index: [
            (source_index, "".join(sorted(two_box_strip_types(source, target))))
            for source_index, source in enumerate(s7)
            if two_box_strip_types(source, target)
        ]
        for target_index, target in enumerate(s5)
    }
    expected_strip_table = {
        0: [(0, "H"), (1, "HV"), (2, "H"), (3, "V")],
        1: [(1, "H"), (2, "HV"), (3, "HV"), (4, "H"), (5, "HV")],
        2: [(2, "H"), (4, "HV"), (5, "HV"), (6, "HV"), (7, "H")],
        3: [(3, "H"), (5, "HV"), (6, "H"), (7, "V")],
        4: [(5, "H"), (6, "V"), (7, "HV")],
    }
    assert strip_table == expected_strip_table

    # Five-replica blocks singled out by the exact negative pseudomoment.
    target_families = {
        "worst_ratio_444": orbit((4, 4, 4)),
        "worst_ratio_333": orbit((3, 3, 3)),
        "worst_ratio_433": orbit((4, 3, 3)),
        "largest_raw_141": orbit((1, 4, 1)),
        "largest_raw_331": orbit((3, 3, 1)),
        "largest_raw_321": orbit((3, 2, 1)),
    }

    def pair_antisymmetric_reachable(source, target):
        local_types = [
            two_box_strip_types(s7[source_site], s5[target_site])
            for source_site, target_site in zip(source, target)
        ]
        if not all(local_types):
            return False
        return any(
            sum(channel == "V" for channel in channels) % 2 == 1
            for channels in product(*local_types)
        )

    family_stats = {}
    reachable_union = set()
    for family, targets in target_families.items():
        candidates = set()
        for target in targets:
            for source in product(range(8), repeat=3):
                if (after_omega_ranks[source] > 0
                        and pair_antisymmetric_reachable(source, target)):
                    candidates.add(source)
        reachable_union.update(candidates)
        family_stats[family] = (
            len(candidates),
            sum(after_omega_ranks[source] for source in candidates),
            sum(
                after_omega_ranks[source] * (after_omega_ranks[source] + 1) // 2
                for source in candidates
            ),
        )

    # These fixed integers make the pruning calculation independently auditable.
    expected_family_stats = {
        "worst_ratio_444": (23, 2530, 162213),
        "worst_ratio_333": (50, 4704, 287350),
        "worst_ratio_433": (60, 5174, 299377),
        "largest_raw_141": (199, 9331, 382879),
        "largest_raw_331": (170, 10188, 451993),
        "largest_raw_321": (274, 12907, 496192),
    }
    assert family_stats == expected_family_stats
    assert len(reachable_union) == 301
    assert sum(after_omega_ranks[source] for source in reachable_union) == 13660
    assert sum(
        after_omega_ranks[source] * (after_omega_ranks[source] + 1) // 2
        for source in reachable_union
    ) == 514945

    # Print once before pinning the values; the assertions below are populated
    # in the committed verifier.
    print("S7 shapes:", s7)
    print("Specht dimensions:", specht7)
    print("GL3 carrier dimensions:", carrier7)
    print("active source blocks / reduced rank:", 487, 14572)
    print("pre-Omega symmetric variables:", 526070)
    print("Omega output active blocks / reduced rank:", 39, 61)
    print("after-Omega reduced rank / symmetric variables:", 14511, 519434)
    print("full dimensions before/after:", full_source_dimension, after_omega_dimension)
    print("S7 -> S5 two-box branching:", branch_table)
    print("S7 -> S5 horizontal/vertical strip refinement:", strip_table)
    print("targeted family statistics:")
    for family in target_families:
        print(" ", family, family_stats[family])
    print(
        "targeted union blocks/reduced rank/symmetric variables:",
        len(reachable_union),
        sum(after_omega_ranks[source] for source in reachable_union),
        sum(
            after_omega_ranks[source] * (after_omega_ranks[source] + 1) // 2
            for source in reachable_union
        ),
    )
    print("PASS: exact degree-three DTH S7 census")


if __name__ == "__main__":
    main()
