#!/usr/bin/env python3
"""Independent exact finite controls for problem 4400001.

No author functions or source data are imported. Infinite-space topology and
Salo's extension theorem are not certified by this program.
"""
import itertools
import json


def mobius(n):
    sign = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            sign = -sign
            if n % p == 0:
                return 0
        while n % p == 0:
            n //= p
        p += 1
    return -sign if n > 1 else sign


def least_period(word):
    return next(d for d in range(1, len(word) + 1)
                if word[d:] + word[:d] == word)


def allowed(word, colors, cyclic=False):
    if colors == 2:  # Binary full shift, not the two-coloring shift.
        return True
    return all(word[i] != word[i + 1] for i in range(len(word) - 1)) and (
        not cyclic or word[-1] != word[0])


def cyclic_count(colors, n):
    return 2 ** n if colors == 2 else 2 ** n + 2 * (-1) ** n


def run():
    assertions = 0
    def require(condition, label):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(label)

    tables = []
    examined = 0
    for colors in (2, 3):
        for n in range(1, 12):
            language = closed = primitive = 0
            for word in itertools.product(range(colors), repeat=n):
                examined += 1
                language += allowed(word, colors)
                if allowed(word, colors, cyclic=True):
                    closed += 1
                    primitive += least_period(word) == n
            mu_count = sum(mobius(n // d) * cyclic_count(colors, d)
                           for d in range(1, n + 1) if n % d == 0)
            require(language == (2 ** n if colors == 2 else 3 * 2 ** (n - 1)),
                    'direct word language')
            require(closed == cyclic_count(colors, n), 'direct cyclic language')
            require(primitive == mu_count, 'direct rotation versus Mobius')
            require(primitive % n == 0, 'primitive orbits are integral')
            tables.append({'system': 'X' if colors == 2 else 'Y', 'n': n,
                           'linear_words': language, 'fixed_by_shift_n': closed,
                           'least_period_n': primitive})

    # Walk dynamic programming from each start state; not the author's matrix power routine.
    endpoints = {}
    for colors in (2, 3):
        paths = [[int(i == j) for j in range(colors)] for i in range(colors)]
        for n in range(1, 65):
            paths = [[sum(paths[s][v] for v in range(colors)
                          if colors == 2 or v != t)
                      for t in range(colors)] for s in range(colors)]
            require(sum(paths[s][s] for s in range(colors)) == cyclic_count(colors, n),
                    'dynamic closed walks')
            require(sum(sum(row) for row in paths) == colors * 2 ** n,
                    'dynamic open paths')
            if n >= 2:
                require(min(min(row) for row in paths) > 0, 'primitive transition matrix')
            e = sum(mobius(n // d) * cyclic_count(colors, d)
                    for d in range(1, n + 1) if n % d == 0)
            require(e >= 0 and e % n == 0, 'Mobius primitive orbit control')
            if n in (1, 2, 3, 64):
                endpoints[str(colors) + ':' + str(n)] = paths

    # Explicit symbol relabelings preserve all finite allowed transitions and periods.
    relabelings = 0
    for colors in (2, 3):
        for perm in itertools.permutations(range(colors)):
            relabelings += 1
            for word in itertools.product(range(colors), repeat=4):
                mapped = tuple(perm[c] for c in word)
                require(allowed(word, colors, True) == allowed(mapped, colors, True),
                        'relabeling preserves proper cyclic legality')
                require(least_period(word) == least_period(mapped),
                        'relabeling preserves least period')

    # Stress test the elementary insertion step used in the read proof.
    # This bounded test is supplemented by the mathematical half-tail argument in AUDIT.md.
    insertion_cases = 0
    for n in range(2, 8):
        for word in itertools.product(range(2), repeat=n):
            if least_period(word) == 1:
                continue
            for at in range(n):
                def inserted(i):
                    return word[(i if i <= at else i - 1) % n]
                for q in range(1, 2 * n + 1):
                    require(any(inserted(i) != inserted(i + q)
                                for i in range(-4 * n, 4 * n)),
                            'single insertion fails bounded periods')
                    insertion_cases += 1

    # This third system is the proper TWO-coloring shift, a finite two-cycle.
    two_color_counts = [sum(all(w[i] != w[i + 1] for i in range(n - 1))
                            for w in itertools.product(range(2), repeat=n))
                        for n in range(1, 13)]
    require(two_color_counts == [2] * 12, 'two-coloring finite-system control')

    # Each statement here is deliberately false; require its rejection.
    false_claims = {
        'equal_entropy_forces_equal_full_fixed_point_counts': cyclic_count(2, 1) == cyclic_count(3, 1),
        'proper_coloring_has_a_shift_fixed_point': any(allowed((a,), 3, True) for a in range(3)),
        'linear_0120_is_a_closed_proper_word': allowed((0, 1, 2, 0), 3, True),
        'least_period_two_binary_count_is_four': sum(least_period(w) == 2 for w in itertools.product(range(2), repeat=2)) == 4,
        'removing_fixed_points_also_removes_binary_period_two': least_period((0, 1)) == 1,
        'binary_full_shift_is_binary_proper_coloring': all(w[0] != w[1] for w in itertools.product(range(2), repeat=2)),
        'adding_one_coloring_loop_preserves_fixed_count': 1 == cyclic_count(3, 1),
        'two_color_proper_shift_has_growing_language_in_test_range': max(two_color_counts) > min(two_color_counts),
        'two_color_proper_shift_is_mixing_at_all_large_gaps': any(all(int((i + n) % 2 == j) > 0 for i in range(2) for j in range(2)) for n in range(2, 20)),
        'equal_free_part_period_counts_prove_equal_ambient_period_counts': 0 == 0 and cyclic_count(2, 2) == cyclic_count(3, 2),
        'one_sided_1000_tail_stays_nonperiodic_after_one_shift': any((1 if i + 1 == 0 else 0) != 0 for i in range(20)),
        'one_finite_defect_from_zero_is_periodic_with_period_one': (1 if 0 == 0 else 0) == (1 if 1 == 0 else 0),
    }
    for name, false_claim in false_claims.items():
        require(not false_claim, 'deliberate negative: ' + name)

    require(examined == 269813, 'exact independent work count')
    return {
        'status': 'pass', 'assertions': assertions,
        'candidate_words_examined': examined,
        'exhaustive_length_range': [1, 11], 'walk_dp_range': [1, 64],
        'relabelings': relabelings, 'insertion_period_probes': insertion_cases,
        'two_color_control_words_examined': sum(2 ** n for n in range(1, 13)),
        'two_color_control_language_counts': two_color_counts,
        'negative_controls_rejected': sorted(false_claims),
        'tables': tables, 'selected_walk_matrices': endpoints,
        'imports_author_code': False,
        'scope': 'Exact finite regression checks only; does not certify the imported extension theorem or infinite-space continuity.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
