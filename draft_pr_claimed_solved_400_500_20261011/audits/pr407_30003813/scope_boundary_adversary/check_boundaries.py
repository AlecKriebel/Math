#!/usr/bin/env python3
"""Independent exact scope/boundary falsification, no candidate imports.

The finite calculation is evidence only; it does not replace the all-n proof.
Generate direct cube points once and assign each to all admissible sign words.
This is independent of the candidate's original-coordinate dynamic program.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import permutations, product
from math import comb
from pathlib import Path
import hashlib
import json
import sys


def require(condition, detail):
    if not condition:
        raise RuntimeError(str(detail))


def descent_set(p):
    return tuple(i for i in range(len(p) - 1) if p[i] > p[i + 1])


def inverse(p):
    return tuple(p.index(j) for j in range(len(p)))


def word_histogram(alpha, inverse_sigmas):
    hist = [0] * len(alpha)
    for w in inverse_sigmas:
        hist[sum(alpha[w[j]] > alpha[w[j + 1]]
                 for j in range(len(w) - 1))] += 1
    return tuple(hist)


def sign_descent_set(signs):
    return tuple(i for i, s in enumerate(signs)
                 if (i % 2 == 0 and s == '+') or
                    (i % 2 == 1 and s == '-'))


def cube_assignments(x, m, strict=False):
    choices = []
    for a, b in zip(x, x[1:]):
        s = a + b
        if strict and s == m:
            return
        choices.append(('-',) if s < m else ('+',) if s > m else ('-', '+'))
    yield from product(*choices)


def direct_counts(n, m, strict=False):
    counts = Counter()
    count_points = 0
    for x in product(range(1, m) if strict else range(m + 1), repeat=n):
        count_points += 1
        counts.update(cube_assignments(x, m, strict))
    return counts, count_points


def ordinary_accept(x, signs, m):
    return all(0 <= a <= m for a in x) and all(
        (x[i] + x[i + 1] <= m) if s == '-'
        else (x[i] + x[i + 1] >= m) for i, s in enumerate(signs))


def run():
    started = datetime.now(timezone.utc).isoformat()
    stats = Counter()
    histograms = {}
    classes_by_n = {}
    invariance_not_pointwise = None
    inverse_negative = None
    # All natural labelings, and all relative-descent terms, through n=8.
    for n in range(1, 9):
        classes = defaultdict(list)
        for p in permutations(range(n)):
            classes[descent_set(p)].append(p)
            stats['permutations_classified'] += 1
        classes_by_n[n] = classes
        for signs in product('-+', repeat=n - 1):
            D = sign_descent_set(signs)
            sigmas = classes[D]
            invs = [inverse(p) for p in sigmas]
            alpha = sigmas[0]
            ref = word_histogram(alpha, invs)
            for beta in sigmas:
                got = word_histogram(beta, invs)
                require(got == ref, ('label distribution depends on choice', n, signs, beta))
                stats['natural_labelings_checked'] += 1
                stats['ordered_label_sigma_pairs'] += len(sigmas)
                if invariance_not_pointwise is None:
                    for sigma, w in zip(sigmas, invs):
                        da = len(descent_set(tuple(alpha[j] for j in w)))
                        db = len(descent_set(tuple(beta[j] for j in w)))
                        if da != db:
                            invariance_not_pointwise = dict(
                                n=n, signs=''.join(signs), alpha=[j+1 for j in alpha],
                                beta=[j+1 for j in beta], sigma=[j+1 for j in sigma],
                                descents_alpha=da, descents_beta=db, common_histogram=ref)
                            break
            require(ref[0] == 1, ('constant term', n, signs))
            histograms[n, signs] = ref
            if inverse_negative is None:
                wrong = word_histogram(alpha, sigmas)
                if wrong != ref:
                    inverse_negative = dict(n=n, signs=''.join(signs), alpha=[j+1 for j in alpha],
                                            correct=ref, wrong_uninverted=wrong)
            stats['sign_patterns_checked'] += 1
        print(json.dumps({'completed_label_dimension': n,
                          'ordered_pairs': stats['ordered_label_sigma_pairs']}), flush=True)

    # Original-coordinate grids, all signs simultaneously; no reflections or DP.
    for n in range(1, 7):
        signs_list = list(product('-+', repeat=n - 1))
        counts_at_m = []
        for m in range(n + 3):
            counts, points = direct_counts(n, m)
            counts_at_m.append(counts)
            stats['original_cube_points_examined'] += points
            for signs in signs_list:
                h = histograms[n, signs]
                predicted = sum(h[k] * comb(m + n - k, n)
                                for k in range(n) if m >= k)
                require(counts[signs] == predicted, ('lattice identity', n, signs, m))
                stats['direct_original_lattice_counts'] += 1
                if m == 0:
                    require(counts[signs] == 1, ('zero dilation', n, signs))
        for signs in signs_list:
            numerator = tuple(sum((-1)**j * comb(n+1, j) * counts_at_m[k-j][signs]
                                  for j in range(k+1)) for k in range(n+1))
            require(numerator == histograms[n, signs] + (0,),
                    ('independently extracted numerator', n, signs))
            stats['full_numerator_extractions'] += 1
        first_interior = {}
        for m in range(1, n + 3):
            counts, points = direct_counts(n, m, True)
            stats['strict_cube_points_examined'] += points
            for signs in signs_list:
                h = histograms[n, signs]
                reciprocal = sum(h[k] * comb(m + k - 1, n)
                                 for k in range(n) if m + k - 1 >= n)
                require(counts[signs] == reciprocal, ('interior reciprocity', n, signs, m))
                stats['strict_interior_counts'] += 1
                if counts[signs] and signs not in first_interior:
                    first_interior[signs] = m
        for signs in signs_list:
            degree = max(i for i, a in enumerate(histograms[n, signs]) if a)
            require(degree == n + 1 - first_interior[signs], ('observed codegree', n, signs))
            stats['observed_codegree_checks'] += 1
        print(json.dumps({'completed_grid_dimension': n,
                          'cube_points': stats['original_cube_points_examined']}), flush=True)

    # Boundary ties: use all labels through dimension 5. Check the *forward*
    # sort gives a unique permitted sigma and the exact descent-required gaps.
    # At m=0 and endpoint ties, every admissible labeling is exercised.
    for n in range(1, 6):
        for m in range(4):
            for x in product(range(m + 1), repeat=n):
                y = tuple(a if i % 2 == 0 else m-a for i, a in enumerate(x))
                for signs in cube_assignments(x, m):
                    D = sign_descent_set(signs)
                    for alpha in classes_by_n[n][D]:
                        w = tuple(sorted(range(n), key=lambda i: (y[i], alpha[i])))
                        sigma = inverse(w)
                        require(descent_set(sigma) == D, ('not permitted extension', x, signs, alpha))
                        values = tuple(y[j] for j in w)
                        labs = tuple(alpha[j] for j in w)
                        require(all(values[j] <= values[j+1] for j in range(n-1)), 'unsorted values')
                        require(all(values[j] < values[j+1] for j in descent_set(labs)), 'descent tie')
                        # The same coordinates reconstructed from (w,values)
                        # must recover the original point exactly.
                        restored = [None] * n
                        for j, vertex in enumerate(w):
                            restored[vertex] = values[j] if vertex % 2 == 0 else m-values[j]
                        require(tuple(restored) == x and ordinary_accept(restored, signs, m), 'inverse map')
                        stats['all_label_boundary_assignments'] += 1
                        stats['adjacent_equal_value_ties_checked'] += sum(
                            values[j] == values[j+1] for j in range(n-1))

    # Explicit falsifiable negative controls guard against target/convention changes.
    require(invariance_not_pointwise is not None, 'label invariance negative control absent')
    require(inverse_negative is not None, 'inverse composition negative control absent')
    n, signs, m = 3, ('-', '-'), 1
    raw_hist = word_histogram(tuple(range(n)), [inverse(s) for s in classes_by_n[n][(1,)]])
    require(raw_hist == (0, 2, 0), 'raw vertex labeling negative control')
    correct = histograms[n, signs]
    require(correct == (1, 1, 0), 'small signed example')
    weak_points = [x for x in product(range(2), repeat=3) if ordinary_accept(x, signs, 1)]
    wrapped_points = [x for x in weak_points if x[-1]+x[0] <= 1]
    require(len(weak_points) == 5 and len(wrapped_points) == 4, 'wrap edge negative control')
    weak_triangle = sum(ordinary_accept(x, ('-',), 1) for x in product(range(2), repeat=2))
    strict_triangle = sum(x[0]+x[1] < 1 for x in product(range(2), repeat=2))
    require((weak_triangle, strict_triangle) == (3, 1), 'weak endpoint negative control')
    require(ordinary_accept((0,2), ('-',), 2) and 1-2 < 0, 'T_1 vs T_m control')
    for (n, signs), h in histograms.items():
        complemented = tuple('+' if s == '-' else '-' for s in signs)
        require(h == histograms[n, complemented] == histograms[n, signs[::-1]], 'symmetry')
        stats['complement_and_reversal_checks'] += 1
    stats['negative_controls'] = 6
    examples = {str(n) + ':' + ''.join(signs): h for (n, signs), h in histograms.items() if n <= 4}
    return dict(verdict='PASS', started_at_utc=started,
                completed_at_utc=datetime.now(timezone.utc).isoformat(),
                coverage=dict(stats), examples=examples,
                label_invariance_is_distribution_only=invariance_not_pointwise,
                inverse_composition_negative_control=inverse_negative,
                wrap_edge_negative_control={'n':3,'signs':'--','m':1,'source_count':5,'wrong_wrap_count':4},
                independence='New standard-library checker, no candidate/checker imports; original-coordinate grid assignment rather than lattice DP.',
                limitations='Finite exact checks, not an all-dimensions proof or priority audit.')


if __name__ == '__main__':
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('RESULTS.json')
    require(not out.exists(), 'refuse overwrite of prior audit result')
    result = run()
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True, indent=2))
