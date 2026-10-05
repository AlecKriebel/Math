#!/usr/bin/env python3
"""Independent finite arithmetic checks. No realization claim or author imports.

Run with Python's standard library. This script writes nothing unless --output
is supplied. Never direct output into the frozen author directory.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from math import factorial, ceil
import argparse
import json


assert __debug__, 'Do not run controls with assertions disabled'


def cycle_lengths(perm):
    unseen = set(range(len(perm)))
    lengths = []
    while unseen:
        start = min(unseen)
        current = start
        size = 0
        while current in unseen:
            unseen.remove(current)
            size += 1
            current = perm[current]
        assert current == start
        lengths.append(size)
    return tuple(sorted(lengths))


def orbit_data(lengths):
    degree = sum(lengths)
    # Different evaluation from the author's sum of (k*k-1)/(3*k).
    weight = (degree - sum((F(1, k) for k in lengths), F(0))) / 3
    return degree - len(lengths), weight


def invariants(chis, eulers, lengths):
    assert len(chis) == len(eulers) == len(lengths)
    degree = sum(lengths[0])
    assert all(sum(p) == degree for p in lengths)
    # Stratified Euler evaluation, rather than the author's defect evaluation.
    chi = degree * (2 - sum(chis)) + sum(len(p) * x for p, x in zip(lengths, chis))
    sigma = -sum((e * orbit_data(p)[1] for e, p in zip(eulers, lengths)), F(0))
    return chi, sigma


def main():
    counts = Counter()
    histograms = {}
    for degree in range(1, 9):
        histogram = Counter(cycle_lengths(p) for p in permutations(range(degree)))
        histograms[degree] = histogram
        for lengths, multiplicity in histogram.items():
            denom = 1
            for k, v in Counter(lengths).items():
                denom *= k ** v * factorial(v)
            assert multiplicity == factorial(degree) // denom
            r, a = orbit_data(lengths)
            assert r == sum(k - 1 for k in lengths)
            assert a == sum((F(k * k - 1, 3 * k) for k in lengths), F(0))
            assert 0 <= r <= degree - 1
            assert (r == 0) == (a == 0)
            assert F(r, 3) <= a <= F(r, 2)
            assert (a == F(r, 2)) == all(k <= 2 for k in lengths)
            counts['permutation_cycle_types'] += 1
        counts['permutations_enumerated'] += sum(histogram.values())
    assert counts['permutations_enumerated'] == sum(factorial(i) for i in range(1, 9))

    # Independent generating-function count for the author's partition range.
    p = [1] + [0] * 18
    for part in range(1, 19):
        for total in range(part, 19):
            p[total] += p[total - part]
    assert sum(p[1:]) == 1596
    for degree, histogram in histograms.items():
        assert len(histogram) == p[degree]
    counts['partition_count_comparisons'] = 9  # 8 per-degree and one total.

    # Work with cycle COUNTS, independently of the author's partition iterator.
    for degree in range(2, 11):
        for chis in product(range(-3, 3), repeat=3):
            positive_mass = sum(x for x in chis if x > 0)
            for orbit_counts in product(range(1, degree), repeat=3):
                chi = degree * (2 - sum(chis)) + sum(c * x for c, x in zip(orbit_counts, chis))
                bound = 2 * degree - (degree - 1) * positive_mass
                assert chi >= bound
                counts['euler_bound_cases'] += 1

    for degree in range(2, 9):
        types = [q for q in histograms[degree] if len(q) < degree]
        for p1, p2 in product(types, repeat=2):
            for e1, e2 in product(range(-6, 7, 2), repeat=2):
                if (e1 >= 0 and e2 >= 0 or e1 <= 0 and e2 <= 0) and (e1 or e2):
                    sig = -(e1 * orbit_data(p1)[1] + e2 * orbit_data(p2)[1])
                    assert sig != 0
                    counts['same_sign_cases'] += 1
            for x, y in product(range(-5, 2), repeat=2):
                chi, _ = invariants((x, y), (2, -2), (p1, p2))
                assert chi >= 2
                counts['two_nonorientable_cases'] += 1

    # Independently compare upstairs bundle and downstairs cycle contributions.
    for k, m, e in product(range(2, 17), range(1, 8), range(-32, 33)):
        if m * e % k:
            continue
        upstairs_e = m * e // k
        upstairs = F(k * k - 1, 3) * upstairs_e
        downstairs = F(k * k - 1, 3 * k) * m * e
        assert upstairs == downstairs
        counts['normal_euler_conversion_cases'] += 1

    for mass, genus, degree in product(range(3, 18), range(1, 151), range(1, 41)):
        feasible = 2 - 2 * genus >= (2 - mass) * degree + mass
        threshold = 1 + ceil(F(2 * genus, mass - 2))
        assert feasible == (degree >= threshold)
        counts['degree_growth_equivalences'] += 1

    # Counted orientation checks: both choices of ambient orientation.
    for e in (-2, 2):
        assert invariants((1,), (e,), ((2,),)) == (3, -e // 2)
        counts['normalization_cases'] += 1
    assert invariants((2,), (0,), ((2,),)) == (2, 0)
    counts['normalization_cases'] += 1
    for degree in range(2, 101):
        assert invariants((0, 2, 2), (0, 0, 0), ((degree,),) * 3)[1] == 0
        counts['orientable_double_cases'] += 1

    negative = {}
    def reject(name, correct, mutant):
        assert correct != mutant, name
        negative[name] = {'status': 'REJECTED', 'correct': str(correct), 'mutant': str(mutant)}
    cp2_signature = invariants((1,), (-2,), ((2,),))[1]
    k, downstairs_e = 2, -2
    reject('omit_downstairs_index_divisor', cp2_signature, -downstairs_e * F(k*k-1, 3))
    reject('use_3k_upstairs_then_divide_again', cp2_signature, -downstairs_e * F(k*k-1, 3*k*k))
    reject('reverse_signature_sign', cp2_signature, downstairs_e * orbit_data((2,))[1])
    reject('omit_fixed_points_from_cycle_count', orbit_data((1, 2))[0], 3 - 1)
    reject('confuse_index_two_only_with_simple', orbit_data((2, 2))[0], 1)
    # Relaxed dummy-component data: invalidates strict positivity without exactness.
    assert orbit_data((1, 1))[1] == 0
    dummy_signature = invariants((2, 1), (0, 2), ((2,), (1, 1)))[1]
    assert dummy_signature == 0
    negative['drop_exact_locus_hypothesis'] = {'status':'REJECTED', 'formal_same_sign_signature':'0 with nonzero-e component unbranched', 'geometric_realization_claimed':False}
    # The scalar feasible set is not empty; this is no geometric construction.
    relaxed = invariants((1, 1, 2), (2, -2, 0), ((1, 2), (1, 2), (3,)))
    assert relaxed == (0, 0)
    negative['promote_scalar_obstructions_to_global_nonexistence'] = {'status':'REJECTED', 'scalar_witness_chi_sigma':[0, 0], 'geometric_realization_claimed':False}
    reject('omit_connected_sum_euler_correction', 2 - 2 * 2, 0 + 0)
    # A generated permutation group can fail to be transitive despite valid cycles.
    generators = ((1, 0, 2), (1, 0, 2))
    orbit = {0}
    while True:
        enlarged = orbit | {g[x] for g in generators for x in orbit}
        if enlarged == orbit:
            break
        orbit = enlarged
    assert len(orbit) == 2
    reject('infer_transitivity_from_nontrivial_meridians', len(orbit), 3)
    negative['assert_fixed_signature_for_all_index_two_covers'] = {'status':'REJECTED', 'weight_one_transposition':str(orbit_data((2, 1, 1))[1]), 'weight_two_transpositions':str(orbit_data((2, 2))[1])}
    assert orbit_data((2, 1, 1))[1] != orbit_data((2, 2))[1]

    report = {
        'status':'PASS', 'author_code_imported':False,
        'arithmetic':'exact integer and fractions.Fraction',
        'counts':dict(sorted(counts.items())),
        'negative_controls':negative, 'negative_control_count':len(negative),
        'limitations':'Finite arithmetic controls only. No surface embedding, complete complement representation, branched completion, manifold identification, topology theorem or universality claim is certified by computation.'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    rendered = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        from pathlib import Path
        out = Path(args.output).resolve()
        author = Path(__file__).resolve().parent.parent / 'author'
        assert author != out and author not in out.parents, 'frozen author directory is read-only'
        out.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
