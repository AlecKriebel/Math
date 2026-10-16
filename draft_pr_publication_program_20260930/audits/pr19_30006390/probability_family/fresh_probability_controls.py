#!/usr/bin/env python3
"""Fresh exact probability controls; no imported author/reviewer code or plane builder.

Universal proofs are in REPORT.md. These controls check algebra and finite
realizations of those proofs; no finite-to-asymptotic extrapolation is used.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import platform

checks = Counter()


def check(condition, family):
    checks[family] += 1
    if not condition:
        raise AssertionError(family)


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def product_linear(slope, offsets):
    result = [1]
    for intercept in offsets:
        result = mul(result, [intercept, slope])
    return result


def shifted(coeffs, shift):
    answer = [0] * len(coeffs)
    for degree, coeff in enumerate(coeffs):
        for power in range(degree + 1):
            answer[power] += coeff * comb(degree, power) * shift ** (degree - power)
    return answer


# Universal pencil distribution: its center, and q+1 disjoint q-point petals.
# Conditional on a missing center, empty-line indicators are independent;
# without conditioning, their distribution is a nontrivial binomial mixture.
pencil_rows = []
for q in range(2, 33):
    m = q + 1
    petal_empty = Fraction(1, 2 ** q)
    distribution = [Fraction(1, 2) * comb(m, k) * petal_empty ** k
                    * (1 - petal_empty) ** (m - k) for k in range(m + 1)]
    distribution[0] += Fraction(1, 2)
    check(sum(distribution) == 1, 'pencil_mixture')
    mean = sum(k * prob for k, prob in enumerate(distribution))
    factorial_second = sum(k * (k - 1) * prob for k, prob in enumerate(distribution))
    p = Fraction(1, 2 ** (q + 1))
    check(mean == m * p, 'pencil_mixture')
    check(factorial_second == m * (m - 1) * 2 * p * p, 'pencil_mixture')
    check(1 - distribution[0] == Fraction(1, 2) * (1 - (1 - petal_empty) ** m), 'pencil_mixture')
    check(1 - distribution[0] <= m * p, 'pencil_mixture')
    if q <= 4:
        counts = Counter()
        vertices = 1 + q * m
        petal_masks = [((1 << q) - 1) << (1 + i * q) for i in range(m)]
        for retained in range(1 << vertices):
            empty = 0 if retained & 1 else sum(not (retained & mask) for mask in petal_masks)
            counts[empty] += 1
        check([Fraction(counts[k], 1 << vertices) for k in range(m + 1)] == distribution,
              'direct_pencil_enumeration')
    if q in (2, 3, 4, 8, 16, 32):
        pencil_rows.append({'q': q, 'expected_empty_lines': str(mean),
                            'joint_over_product': '2',
                            'zero_empty_line_probability_denominator_bits': distribution[0].denominator.bit_length()})

# One whole-line candidate gives an exact contrast between the two sampling models.
# This candidate is intentionally in the exceptional full-line event of the
# baseline lower bound; it attacks model transfer, not the claimed lower bound.
model_contrast_rows = []
for q in range(2, 65):
    n = q * q + q + 1
    shared_point_containment = Fraction(1, 2 ** (q + 1))
    independent_incidence_hitting = Fraction(1, 2 ** (n - 1)) * (1 - shared_point_containment)
    ratio = shared_point_containment / independent_incidence_hitting
    check(ratio == Fraction(2 ** (q * q - 1), 1) / (1 - shared_point_containment),
          'independent_incidence_model_contrast')
    check(shared_point_containment > independent_incidence_hitting,
          'independent_incidence_model_contrast')
    if q in (2, 3, 4, 8):
        model_contrast_rows.append({'q': q, 'whole_line_containment_shared_points': str(shared_point_containment),
                                   'whole_line_hits_all_independent_sections': str(independent_incidence_hitting),
                                   'ratio': str(ratio)})

# All empty-line / whole-line events are globally disjoint: a full line meets
# every candidate empty line. Complementation gives equal probabilities.
# Bonferroni's first two terms give a uniform asymptotically exact control.
exception_rows = []
for q in range(2, 65):
    n = q * q + q + 1
    p = Fraction(1, 2 ** (q + 1))
    bonferroni_empty_lower = n * p - n * (n - 1) * p * p
    combined_upper = 2 * n * p
    combined_lower = 2 * bonferroni_empty_lower
    check(combined_lower <= combined_upper, 'exceptional_event_bonferroni')
    check(combined_lower / combined_upper == 1 - (n - 1) * p, 'exceptional_event_bonferroni')
    # Monochromatic-line events happen to be pairwise independent at retention 1/2.
    # This does NOT make all line sections jointly independent.
    same_kind_joint = 2 * p * p
    opposite_kind_joint = Fraction(0)
    check(2 * same_kind_joint + 2 * opposite_kind_joint == (2 * p) ** 2,
          'exceptional_event_bonferroni')
    if q in (2, 3, 4, 8, 16, 32, 64):
        exception_rows.append({'q': q, 'empty_or_full_event_lower': str(combined_lower),
                               'empty_or_full_event_upper': str(combined_upper),
                               'lower_over_upper': str(combined_lower / combined_upper)})

# A selected singleton has fixed cardinality one but is not a fixed witness.
for vertices in range(2, 25):
    adaptive_containment_probability = 1 - Fraction(1, 2 ** vertices)
    check(adaptive_containment_probability > Fraction(1, 2), 'adaptive_witness_negative_control')

# Correlations *conditional on a fixed R* in the alteration argument.
for rho in (Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(1)):
    for r in range(1, 13):
        for s in range(1, 13):
            joint = (1 - rho) ** (r + s - 1)
            product = (1 - rho) ** (r + s)
            check(joint - product == rho * (1 - rho) ** (r + s - 1), 'conditional_thinning')
            check(joint >= product, 'conditional_thinning')
            # If the common point is absent from R, the nonempty sections are disjoint.
            check((1 - rho) ** r * (1 - rho) ** s == product, 'conditional_thinning')


def repair_average(vertices, sections, rho):
    """Enumerate thinning outcomes and perform deterministic, possibly colliding repairs."""
    expectation = Fraction(0)
    best = vertices + 1
    weight_total = Fraction(0)
    for temporary in range(1 << vertices):
        size = temporary.bit_count()
        weight = rho ** size * (1 - rho) ** (vertices - size)
        repaired = temporary
        missed = [section for section in sections if not (temporary & section)]
        for section in missed:
            repaired |= section & -section
        check(all(repaired & section for section in sections), 'deterministic_repairs')
        check(repaired.bit_count() <= size + len(missed), 'deterministic_repairs')
        expectation += weight * repaired.bit_count()
        weight_total += weight
        if weight:
            best = min(best, repaired.bit_count())
    exact_upper = rho * vertices + sum((1 - rho) ** section.bit_count() for section in sections)
    check(weight_total == 1, 'deterministic_repairs')
    check(expectation <= exact_upper, 'deterministic_repairs')
    check(best <= expectation, 'deterministic_repairs')
    return {'actual_repair_expectation': str(expectation), 'linear_expectation_upper': str(exact_upper),
            'best_positive_probability_outcome': best}


repair_rows = []
systems = [('shared_center', 6, [1 | (1 << i) for i in range(1, 6)]),
           ('identical_sections', 5, [31] * 7),
           ('singletons', 5, [1 << i for i in range(5)]),
           ('cycle_sections', 7, [(1 << i) | (1 << ((i + 1) % 7)) for i in range(7)]),
           ('no_sections', 3, [])]
for name, vertices, sections in systems:
    for rho in (Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(1)):
        repair_rows.append({'system': name, 'rho': str(rho), **repair_average(vertices, sections, rho)})

# Antichain of minimal blockers in a NON-projective hypergraph: t forced core
# vertices plus t out of 4t optional vertices. Every (3t+1)-subset of optional
# vertices is an edge, together with the t singleton core edges.
overlap_rows = []
for t in range(1, 41):
    first_moment = Fraction(comb(4 * t, t), 2 ** (2 * t))
    union_probability = Fraction(sum(comb(4 * t, j) for j in range(t, 4 * t + 1)), 2 ** (5 * t))
    check(union_probability <= Fraction(1, 2 ** t), 'minimal_witness_overlap')
    check(union_probability <= first_moment, 'minimal_witness_overlap')
    if t >= 3:
        next_moment = Fraction(comb(4 * (t + 1), t + 1), 2 ** (2 * (t + 1)))
        check(next_moment >= 2 * first_moment, 'minimal_witness_overlap')
    if t <= 2:
        core = (1 << t) - 1
        optional = list(range(t, 5 * t))
        edges = [1 << i for i in range(t)]
        edges += [sum(1 << i for i in chosen) for chosen in combinations(optional, 3 * t + 1)]
        minimal = []
        for mask in range(1 << (5 * t)):
            if all(mask & edge for edge in edges):
                if all(not all((mask ^ (1 << i)) & edge for edge in edges)
                       for i in range(5 * t) if mask & (1 << i)):
                    minimal.append(mask)
        check(len(minimal) == comb(4 * t, t), 'minimal_witness_construction')
        check(all(mask & core == core and mask.bit_count() == 2 * t for mask in minimal),
              'minimal_witness_construction')
    if t in (1, 2, 3, 5, 10, 20, 40):
        overlap_rows.append({'t': t, 'minimal_witness_first_moment': str(first_moment),
                             'exact_containment_probability': str(union_probability),
                             'containment_probability_upper': f'2^-{t}'})

# Check a positivity certificate proving W_(t+1)/W_t >=2 for EVERY integer t>=3.
numerator = product_linear(4, (1, 2, 3, 4))
denominator_times_two = [8 * x for x in mul([1, 1], product_linear(3, (1, 2, 3)))]
ratio_difference = [a - b for a, b in zip(numerator, denominator_times_two)]
shifted_difference = shifted(ratio_difference, 3)
check(ratio_difference == [-24, -112, -136, -8, 40], 'universal_polynomial_certificate')
check(shifted_difference == [1440, 3176, 1952, 472, 40], 'universal_polynomial_certificate')
check(all(x > 0 for x in shifted_difference), 'universal_polynomial_certificate')

# Quantifier controls: divergence in probability does not assert a logarithmic rate.
with localcontext() as ctx:
    ctx.prec = 60
    quantifier_rows = []
    for q in (4096, 65536, 10 ** 6, 10 ** 9, 10 ** 30):
        dq = Decimal(q)
        n = dq * dq + dq + 1
        line_size = dq + 1
        logarithm = dq.ln()
        t = (3 * line_size * logarithm).sqrt()
        s = (3 * n * logarithm).sqrt()
        lower_m = line_size / 2 - t
        rho_bound = line_size.ln() / lower_m
        upper = (n / 2 + s) * line_size.ln() / lower_m + n / line_size
        check(0 < rho_bound < 1, 'explicit_upper_bound')
        quantifier_rows.append({'q': q, 'deterministic_upper_over_q_ln_q': str(upper / (dq * logarithm)),
                               'rho_upper_on_good_event': str(rho_bound),
                               'concentration_failure_bound_exact': str(Fraction(2 * (int(n) + 1), q ** 6)),
                               'sqrt_ln_q_over_ln_q': str(1 / logarithm.sqrt())})

report = {'description': 'Fresh exact controls and algebra certificates; universal proofs in REPORT.md',
          'python': platform.python_version(), 'all_checks_passed': True,
          'checks_by_family': dict(sorted(checks.items())), 'total_checks': sum(checks.values()),
          'universal_ratio_difference_coefficients_ascending': ratio_difference,
          'universal_shift_t_equals_u_plus_3_coefficients_ascending': shifted_difference,
          'pencil_rows': pencil_rows, 'model_contrast_rows': model_contrast_rows,
          'exceptional_event_bonferroni_rows': exception_rows, 'repair_rows': repair_rows,
          'minimal_witness_overlap_rows_non_projective': overlap_rows,
          'explicit_upper_bound_decimal_diagnostics': quantifier_rows}
path = Path(__file__).with_name('fresh_probability_results.json')
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'all_checks_passed': True, 'total_checks': sum(checks.values()),
                  'checks_by_family': dict(sorted(checks.items())),
                  'results_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}, indent=2))
