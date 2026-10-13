#!/usr/bin/env python3
"""Independent exact finite controls for nested speed records and conditioning."""
from fractions import Fraction
from itertools import combinations, product
import json

checks = 0
histories = 0
record_tests = 0
def check(statement):
    global checks
    assert statement
    checks += 1

# Independent increments are discrete speed records. This finite surrogate is
# not a Poisson-line network. Unlike a composition identity alone it computes
# actual dependent nested-maxima probabilities and all record intersections.
for m in range(5):
    outcomes = tuple(range(-1, m + 1))
    states = []
    mass = Fraction(1, len(outcomes) ** (m + 1))
    for increments in product(outcomes, repeat=m + 1):
        maxima = tuple(max(increments[:j + 1]) for j in range(m + 1))
        states.append(maxima)
        histories += 1
    probability = lambda predicate: mass * sum(predicate(h) for h in states)
    h_event = lambda h: all(h[j] >= j for j in range(m + 1))
    exact_h = probability(h_event)
    record_union_probability = Fraction(0)
    sum_product_bound = Fraction(0)
    for k in range(m + 1):
        for interior in combinations(range(1, m + 1), k):
            sequence = (0,) + interior + (m + 1,)
            record = lambda h, s=sequence, k=k: (
                all(s[i + 1] - 1 <= h[s[i]] < s[i + 1] for i in range(k))
                and h[s[k]] >= m)
            intersection_probability = probability(record)
            product_bound = Fraction(1)
            for i in range(k + 1):
                index, threshold = sequence[i], sequence[i + 1] - 1
                product_bound *= probability(lambda h, j=index, t=threshold: h[j] >= t)
            check(intersection_probability <= product_bound)
            record_union_probability += intersection_probability
            sum_product_bound += product_bound
            record_tests += 1
    check(exact_h == record_union_probability)
    check(exact_h <= sum_product_bound)
    check(Fraction(0) <= exact_h <= 1)
    # Conditioning on the speed-constraint event itself demonstrates the
    # invalid shortcut P(H | B) <= P(H), while joint inclusion remains valid.
    check(exact_h > 0)
    check(exact_h < 1)
    conditional_h_given_h = exact_h / exact_h
    check(conditional_h_given_h > exact_h)

# Check strict thresholds without rounding real gamma to integers.
thresholds = []
for d in [2, 3, 4]:
    for epsilon in [Fraction(1, 1000), Fraction(1, 10), Fraction(1), Fraction(5)]:
        gamma = d + epsilon
        q, a = gamma - 1, gamma - d
        check(a > 0)
        check(q > 1)
        p = Fraction(1)
        kappa = (p + q) / 2
        check(p < kappa < q)
        check(p / kappa - 1 < 0)
        check((q / a) * (-a) + q == 0)
        thresholds.append({'d':d, 'gamma':str(gamma), 'radial_moment_limit':str(a),
                           'multiscale_moment_limit':str(q),
                           'first_moment_multiscale':True, 'first_moment_one_radius':a > 1})

print(json.dumps({'status':'PASS', 'exact_assertions':checks,
                  'finite_increment_histories':histories, 'record_intersections':record_tests,
                  'parameter_thresholds':thresholds,
                  'scope':'Exact dependent nested-maxima record probabilities, conditioning counter-control, strict moment threshold checks. No Poisson-line simulation, SIRSN realization, or formal continuum verification.'}, indent=2))
