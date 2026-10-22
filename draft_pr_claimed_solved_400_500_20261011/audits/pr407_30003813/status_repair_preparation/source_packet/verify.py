#!/usr/bin/env python3
"""Exact, dependency-free checks for the signed adjacent-sum certificate.

This is a finite regression test, not a replacement for the general proof.
Run: python3 verify.py [--max-n 8] [--output verification.json]
"""
from argparse import ArgumentParser
from collections import Counter
from itertools import permutations, product
from math import comb, factorial
import json


def relations(signs):
    """Return directed edges (lower, upper), with vertices numbered from zero."""
    result = []
    for i, sign in enumerate(signs):
        increasing = (sign == '-') if i % 2 == 0 else (sign == '+')
        result.append((i, i + 1) if increasing else (i + 1, i))
    return result


def natural_labels(signs, reverse=False):
    """A natural labeling, using least/greatest available original vertex."""
    n = len(signs) + 1
    edges = relations(signs)
    remaining = set(range(n))
    labels = [None] * n
    for rank in range(1, n + 1):
        available = [v for v in remaining
                     if all(a not in remaining for a, b in edges if b == v)]
        assert available
        vertex = (max if reverse else min)(available)
        labels[vertex] = rank
        remaining.remove(vertex)
    assert all(labels[a] < labels[b] for a, b in edges)
    return labels


def lattice_count(signs, m):
    """Dynamic program in the original x coordinates; no poset input."""
    counts = [1] * (m + 1)
    for sign in signs:
        prefix = [0]
        for count in counts:
            prefix.append(prefix[-1] + count)
        if sign == '-':
            counts = [prefix[m - value + 1] for value in range(m + 1)]
        else:
            counts = [prefix[-1] - prefix[m - value] for value in range(m + 1)]
    return sum(counts)


def in_original(point, signs, m):
    return all((point[i] + point[i + 1] <= m) if sign == '-'
               else (point[i] + point[i + 1] >= m)
               for i, sign in enumerate(signs))


def descents(word, labels):
    return sum(labels[a] > labels[b] for a, b in zip(word, word[1:]))


def trim(coefficients):
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return coefficients


def run(max_n):
    patterns_checked = 0
    permutations_checked = 0
    ehrhart_evaluations = 0
    pointwise_reflection_checks = 0
    tie_sort_checks = 0
    examples = {}
    for n in range(1, max_n + 1):
        patterns = list(product('-+', repeat=n - 1))
        labels = {s: natural_labels(s) for s in patterns}
        alternative = {s: natural_labels(s, reverse=True) for s in patterns}
        distributions = {s: Counter() for s in patterns}
        distributions2 = {s: Counter() for s in patterns}

        # Every total ordering determines exactly one orientation of the path.
        # Grouping all n! words avoids separately scanning n! words per pattern.
        for word in permutations(range(n)):
            position = [0] * n
            for index, vertex in enumerate(word):
                position[vertex] = index
            signs = tuple('-' if ((position[i] < position[i + 1]) == (i % 2 == 0))
                          else '+' for i in range(n - 1))
            assert all(position[a] < position[b] for a, b in relations(signs))
            distributions[signs][descents(word, labels[signs])] += 1
            distributions2[signs][descents(word, alternative[signs])] += 1
            permutations_checked += 1

        assert sum(sum(c.values()) for c in distributions.values()) == factorial(n)
        for signs in patterns:
            histogram = distributions[signs]
            assert histogram == distributions2[signs], ('label dependence', signs)
            coefficient_list = [histogram[k] for k in range(n + 1)]
            counts = [lattice_count(signs, m) for m in range(n + 3)]
            from_counts = [sum((-1) ** j * comb(n + 1, j) * counts[k - j]
                               for j in range(k + 1)) for k in range(n + 1)]
            assert coefficient_list == from_counts, ('numerator mismatch', signs)
            for m, count in enumerate(counts):
                predicted = sum(number * comb(m + n - d, n)
                                for d, number in histogram.items() if m >= d)
                assert count == predicted, ('Ehrhart mismatch', signs, m)
                ehrhart_evaluations += 1
            assert histogram[0] == 1
            assert histogram == distributions[tuple('+' if s == '-' else '-' for s in signs)]
            assert histogram == distributions[signs[::-1]]
            if all(signs[i] != signs[i + 1] for i in range(len(signs) - 1)):
                assert histogram == Counter({0: 1})
            patterns_checked += 1

            # Exhaustive direct original-coordinate and dilation checks.
            if n <= 5:
                for m in range(5):
                    count = 0
                    for point in product(range(m + 1), repeat=n):
                        transformed = tuple(value if i % 2 == 0 else m - value
                                            for i, value in enumerate(point))
                        original_ok = in_original(point, signs, m)
                        reflected_ok = all(transformed[a] <= transformed[b]
                                           for a, b in relations(signs))
                        assert original_ok == reflected_ok
                        pointwise_reflection_checks += 1
                        if original_ok:
                            count += 1
                            word = sorted(range(n), key=lambda v: (transformed[v], labels[signs][v]))
                            position = {v: index for index, v in enumerate(word)}
                            assert all(position[a] < position[b] for a, b in relations(signs))
                            for a, b in zip(word, word[1:]):
                                assert transformed[a] <= transformed[b]
                                if labels[signs][a] > labels[signs][b]:
                                    assert transformed[a] < transformed[b]
                            tie_sort_checks += 1
                    assert count == lattice_count(signs, m)

            if n <= 4 or ''.join(signs) in ['--++', '---+', '--+-']:
                examples[f'n={n}, signs={"".join(signs)}'] = {
                    'natural_labels': labels[signs],
                    'h_star': trim(coefficient_list.copy()),
                    'L_0_through_n_plus_2': counts,
                }

    # Negative control: unrelabeled original vertex labels are not generally natural.
    # n=3, -- has order 1<2>3, with extension words 132 and 312.
    # Their raw descent polynomial is 2z, whereas the answer is 1+z.
    raw = Counter()
    signs = ('-', '-')
    for word in permutations(range(3)):
        p = {v: i for i, v in enumerate(word)}
        if all(p[a] < p[b] for a, b in relations(signs)):
            raw[descents(word, [1, 2, 3])] += 1
    assert raw == Counter({1: 2})
    assert lattice_count(signs, 1) - 4 == 1
    return {
        'status': 'PASS',
        'arithmetic': 'exact Python integers; standard library only',
        'max_dimension': max_n,
        'sign_patterns_checked': patterns_checked,
        'permutation_words_checked': permutations_checked,
        'ehrhart_evaluations_checked': ehrhart_evaluations,
        'pointwise_reflection_checks': pointwise_reflection_checks,
        'tie_sort_checks': tie_sort_checks,
        'checks': [
            'all sign patterns in every tested dimension',
            'two natural labelings give the same descent histogram',
            'histogram equals numerator extracted from original-coordinate lattice counts',
            'Ehrhart binomial identity at m=0,...,n+2',
            'reflection and tie sorting at every grid point for n<=5 and m<=4',
            'global sign complementation and reversal invariance',
            'alternating signs produce a simplex with h*=1',
            'raw original labels negative control fails as expected',
        ],
        'examples': examples,
        'scope': 'Finite checks support the separately written all-dimensions proof; no novelty assertion.'
    }


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--max-n', type=int, default=8)
    parser.add_argument('--output', default='verification.json')
    args = parser.parse_args()
    assert 1 <= args.max_n <= 9, 'Keep this regression test modest (1<=max-n<=9).'
    result = run(args.max_n)
    with open(args.output, 'w') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'examples'}, indent=2))
