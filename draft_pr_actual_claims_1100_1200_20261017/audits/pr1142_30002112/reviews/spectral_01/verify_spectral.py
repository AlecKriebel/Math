#!/usr/bin/env python3
"""Independent exact finite controls, not a smooth-hypersurface construction.

All tested numeric quantities are integers or fractions. Mathematical proofs in
REPORT.md establish the infinite and geometric claims. No runtime assert is used.
"""
import ast
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

class VerificationError(RuntimeError):
    pass

def require(condition, label, fields=None):
    if not condition:
        raise VerificationError(json.dumps({'label': label, 'fields': fields}, sort_keys=True))

def rational(x):
    x = Fraction(x)
    return {'numerator': x.numerator, 'denominator': x.denominator}

def in_scope(m, q):
    require(isinstance(m, int) and m >= 2, 'dimension_out_of_scope', {'m': m})
    require(isinstance(q, int) and q >= 1, 'parameter_out_of_scope', {'q': q})

def choose_nonnegative(n, k):
    return comb(n, k) if n >= k >= 0 else 0

def harmonic_dimension(m, ell):
    require(m >= 2 and ell >= 0, 'harmonic_input')
    return comb(ell + m, m) - choose_nonnegative(ell + m - 2, m)

def count_formula(m, q):
    in_scope(m, q)
    return comb(q + m - 1, m) + choose_nonnegative(q + m - 2, m)

def compositions(total, n):
    if n == 1:
        return [(total,)]
    return [(j,) + tail for j in range(total + 1)
            for tail in compositions(total - j, n - 1)]

def exact_rank(matrix):
    if not matrix:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    pivot = 0
    for column in range(len(rows[0])):
        candidate = next((i for i in range(pivot, len(rows)) if rows[i][column]), None)
        if candidate is None:
            continue
        rows[pivot], rows[candidate] = rows[candidate], rows[pivot]
        scale = rows[pivot][column]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            if rows[i][column]:
                scale = rows[i][column]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot

def harmonic_kernel_by_laplacian(m, ell):
    """Build actual Laplacian on enumerated monomials and rank it over Q."""
    basis = compositions(ell, m + 1)
    target = compositions(ell - 2, m + 1) if ell >= 2 else []
    target_index = {a: i for i, a in enumerate(target)}
    matrix = [[0 for _ in basis] for _ in target]
    for column, monomial in enumerate(basis):
        for coordinate, exponent in enumerate(monomial):
            if exponent >= 2:
                reduced = list(monomial)
                reduced[coordinate] -= 2
                matrix[target_index[tuple(reduced)]][column] += exponent * (exponent - 1)
    rank = exact_rank(matrix)
    return {'m': m, 'ell': ell, 'monomial_count': len(basis),
            'target_monomial_count': len(target), 'laplacian_rank': rank,
            'kernel_dimension': len(basis) - rank,
            'matrix_sha256': hashlib.sha256(json.dumps(matrix, separators=(',', ':')).encode()).hexdigest()}

def sphere_blocks(m, largest_degree):
    return [(Fraction(ell * (ell + m - 1)), harmonic_dimension(m, ell))
            for ell in range(largest_degree + 1)]

def multiset_snapshot(m, q, candidate, cavity_blocks):
    in_scope(m, q)
    counts = defaultdict(int)
    for value, multiplicity in sphere_blocks(m, q + 1) + cavity_blocks:
        require(multiplicity >= 0, 'negative_multiplicity')
        counts[Fraction(value)] += multiplicity
    target = Fraction(q * (q + m - 1))
    below = sum(number for value, number in counts.items() if value < target)
    equal = counts[target]
    require(isinstance(candidate, int) and candidate >= 1, 'invalid_one_based_index')
    total = 0
    value_at_candidate = None
    for value, number in sorted(counts.items()):
        total += number
        if total >= candidate:
            value_at_candidate = value
            break
    require(value_at_candidate is not None, 'truncated_multiset_index')
    return {'m': m, 'q': q, 'target': rational(target), 'candidate': candidate,
            'actual_below': below, 'actual_equal': equal, 'first_target_index': below + 1,
            'last_target_index': below + equal, 'actual_value': rational(value_at_candidate),
            'identity_holds': value_at_candidate == target,
            'candidate_is_first': candidate == below + 1,
            'zero_multiplicity': counts[Fraction(0)],
            'cavity_blocks': [{'value': rational(v), 'multiplicity': n} for v, n in cavity_blocks]}

def verify_index(snapshot, first=True):
    require(snapshot['identity_holds'], 'wrong_eigenvalue_at_candidate', snapshot)
    if first:
        require(snapshot['candidate_is_first'], 'candidate_is_not_first_target', snapshot)
    return snapshot

def verify_multiplicity(actual, candidate, fields):
    require(actual == candidate, 'wrong_harmonic_multiplicity', dict(fields, actual=actual, candidate=candidate))

def expect_rejection(name, operation, fields):
    try:
        operation()
    except VerificationError as error:
        return {'name': name, 'rejected': True, 'fields': fields, 'diagnostic': str(error)}
    raise VerificationError('Negative control unexpectedly accepted: ' + name)

def geometric_envelope(m):
    """R>=rho, b<=v, J>=v^-((m+2)/(m+1)), by cube inclusions."""
    n = m + 1
    omega_lower = Fraction(2, n) ** n
    v_lower = omega_lower * (1 - Fraction(1, 2 ** n))
    rho_upper = n * 2 ** n
    J = max(Fraction(1), 1 / (v_lower ** 2))
    require(v_lower > 0 and J >= 1, 'nonpositive_envelope')
    require(Fraction(m + 2, m + 1) <= 2, 'volume_power_envelope')
    require(Fraction(2) + Fraction(4, m) <= 4, 'C_m_at_most_16')
    return rho_upper, v_lower, J

def threshold_control(m, a, b):
    R, v_lower, J = geometric_envelope(m)
    M = max(Fraction(0), Fraction(a), Fraction(b))
    envelope_coefficient = 2 * J + 16
    target = envelope_coefficient * M
    t = isqrt(target.numerator // target.denominator) + 1
    while t ** m < max(m, R):
        t += 1
    q = t ** m
    lower_quotient = Fraction(t * t, 1) / envelope_coefficient
    require(q >= max(m, R), 'threshold_domain')
    require(lower_quotient > M, 'threshold_not_strict')
    # t^2 > (2J+16)M is an exact sufficient condition, not an evaluated surface ratio.
    return {'m': m, 'a': rational(a), 'b': rational(b), 'M': rational(M),
            'rho_upper_R': R, 'volume_lower_b': rational(v_lower), 'K_upper_J': rational(J),
            't': t, 'q': q, 'certified_quotient_lower': rational(lower_quotient),
            'strictly_exceeds_max_0_a_b': True,
            'meaning': 'Analytic envelope threshold; no numeric smooth surface or actual boundary spectrum constructed.'}

def main(destination):
    ast_tree = ast.parse(Path(__file__).read_text())
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast_tree)), 'runtime_assert_found')
    ranks = []
    for m in range(2, 5):
        for ell in range(7):
            row = harmonic_kernel_by_laplacian(m, ell)
            verify_multiplicity(row['kernel_dimension'], harmonic_dimension(m, ell), {'m': m, 'ell': ell})
            require(row['laplacian_rank'] == row['target_monomial_count'], 'laplacian_not_surjective', row)
            ranks.append(row)

    counts = []
    cases = [(m, q) for m in range(2, 33) for q in range(1, 129)]
    cases += [(m, q) for m in [64, 128, 256] for q in [1, 2, m - 1, m, m + 1, 2 * m, 10 ** 6]]
    for m, q in cases:
        N = count_formula(m, q)
        # Direct sum is independent of endpoint telescoping; extreme q uses an independent hockey-stick form.
        if q <= 512:
            independent = sum(harmonic_dimension(m, ell) for ell in range(q))
            method = 'direct_sum_of_harmonic_dimensions'
        else:
            independent = comb(q + m, m + 1) - choose_nonnegative(q + m - 2, m + 1)
            method = 'difference_of_hockey_stick_sums'
        require(N == independent, 'count_mismatch', {'m': m, 'q': q, 'N': N, 'independent': independent})
        k = N + 2
        row = {'m': m, 'q': q, 'N_formula': N, 'N_independent': independent, 'method': method,
               'k': k, 'power_bound_applicable': q >= m}
        if q >= m:
            bound = 2 ** (m + 2) * q ** m
            # This is exactly equivalent to k^(2/m) <= 2^(2+4/m) q^2.
            powered_lhs = k * k
            powered_rhs = 2 ** (2 * m + 4) * q ** (2 * m)
            require(k <= bound and powered_lhs <= powered_rhs, 'index_power_bound', row)
            row.update({'k_upper': bound, 'k_square': powered_lhs, 'powered_rhs': powered_rhs})
        counts.append(row)

    indices = []
    for m in range(2, 11):
        for q in range(1, 17):
            next_level = (q + 1) * (q + m)
            cavity = [(Fraction(0), 1), (Fraction(next_level + 1), 1)]
            row = multiset_snapshot(m, q, count_formula(m, q) + 2, cavity)
            verify_index(row)
            require(row['zero_multiplicity'] == 2, 'missing_boundary_zero', row)
            require(row['actual_below'] == count_formula(m, q) + 1, 'below_count', row)
            indices.append(row)

    negatives = []
    m, q = 2, 2
    N = count_formula(m, q)
    T = q * (q + m - 1)
    high = (q + 1) * (q + m) + 1
    normal_cavity = [(Fraction(0), 1), (Fraction(high), 1)]
    for name, candidate, cavity in [
        ('omit_cavity_zero_in_index', N + 1, normal_cavity),
        ('count_sphere_modes_leq_instead_of_lt', N + harmonic_dimension(m, q) + 2, normal_cavity),
        ('replace_multiplicity_by_distinct_level_count', q + 2, normal_cavity),
        ('omit_second_binomial_in_N', comb(q + m - 1, m) + 2, normal_cavity),
        ('additional_low_positive_cavity_mode', N + 2, [(Fraction(0), 1), (Fraction(T - 1), 1)]),
        ('two_cavity_zeros', N + 2, [(Fraction(0), 2), (Fraction(high), 1)]),
        ('mistake_cavity_first_positive_for_boundary_lambda_2', 2, normal_cavity),
        ('mistake_boundary_first_positive_for_target_at_q_2', 3, normal_cavity)
    ]:
        row = multiset_snapshot(m, q, candidate, cavity)
        negatives.append(expect_rejection(name, lambda row=row: verify_index(row), row))
    # Equality alone cannot detect this offset, because the target eigenvalue is multiple.
    extra_offset = multiset_snapshot(m, q, N + 3, normal_cavity)
    verify_index(extra_offset, first=False)
    negatives.append(expect_rejection('extra_offset_detected_only_by_first_index_check',
                                     lambda: verify_index(extra_offset), extra_offset))
    lap = next(row for row in ranks if row['m'] == 2 and row['ell'] == 2)
    wrong_d = comb(4, 2)
    negatives.append(expect_rejection('forget_harmonic_trace_subtraction',
                                     lambda: verify_multiplicity(lap['kernel_dimension'], wrong_d, {'m': 2, 'ell': 2}),
                                     {'actual_kernel': lap['kernel_dimension'], 'wrong_candidate': wrong_d}))
    for bad_m, bad_q in [(1, 2), (0, 2), (2, 0), (2, -1)]:
        negatives.append(expect_rejection('scope_rejection_m_%d_q_%d' % (bad_m, bad_q),
                                         lambda bad_m=bad_m, bad_q=bad_q: count_formula(bad_m, bad_q),
                                         {'m': bad_m, 'q': bad_q, 'meaning': 'Input scope check only, not evidence of mathematical failure outside scope.'}))
    # A tie at T is a positive robustness control: >= rather than > suffices for counting.
    tie_control = multiset_snapshot(m, q, N + 2, [(Fraction(0), 1), (Fraction(T), 3)])
    verify_index(tie_control)
    require(tie_control['actual_equal'] == harmonic_dimension(m, q) + 3, 'tie_multiplicity')

    scalings = []
    for m in range(2, 65):
        a = Fraction(1) + Fraction(2, m)
        volume_exponent = Fraction(m, m + 1) * a
        normalized_lambda_exponent = -2 + m * Fraction(2, m)
        isoperimetric_exponent = m - (m + 1) * Fraction(m, m + 1)
        correct_X_exponent = m * a - (m + 1) * volume_exponent
        wrong_volume_exponent = a
        wrong_X_exponent = m * a - (m + 1) * wrong_volume_exponent
        require(volume_exponent == Fraction(m + 2, m + 1), 'volume_exponent_algebra')
        require(normalized_lambda_exponent == isoperimetric_exponent == correct_X_exponent == 0, 'scaling_failure')
        require(wrong_X_exponent != 0, 'wrong_volume_power_not_detected')
        scalings.append({'m': m, 'alpha': rational(a), 'correct_volume_exponent': rational(volume_exponent),
                         'normalized_lambda_scaling_exponent': rational(normalized_lambda_exponent),
                         'isoperimetric_scaling_exponent': rational(isoperimetric_exponent),
                         'correct_X_scaling_exponent': rational(correct_X_exponent),
                         'wrong_volume_exponent': rational(wrong_volume_exponent),
                         'wrong_X_scaling_exponent': rational(wrong_X_exponent)})
    # The actual wrong exponent is sent through the same invariant-exponent checking primitive.
    def invariant_exponent(exponent, fields):
        require(exponent == 0, 'noninvariant_term', fields)
    wrong_row = scalings[0]
    negatives.append(expect_rejection('wrong_volume_power_breaks_scaling',
                                     lambda: invariant_exponent(Fraction(**{'numerator': wrong_row['wrong_X_scaling_exponent']['numerator'], 'denominator': wrong_row['wrong_X_scaling_exponent']['denominator']}), wrong_row),
                                     wrong_row))

    envelopes = []
    for m in [2, 3, 4, 8, 16, 32, 64]:
        R, b, J = geometric_envelope(m)
        for t in [max(m, R), max(m, R) + 1]:
            q = t ** m
            E1 = J * Fraction(q + R, q * q)
            E2 = Fraction(16, t * t)
            bound = (2 * J + 16) / (t * t)
            require(E1 + E2 <= bound, 'rational_divergence_envelope')
            envelopes.append({'m': m, 'R': R, 'b': rational(b), 'J': rational(J), 't': t, 'q': q,
                              'denominator_over_numerator_upper': rational(E1 + E2),
                              'simplified_upper': rational(bound),
                              'certified_quotient_lower': rational(1 / bound)})

    coefficient_pairs = [(0, 0), (-1, -2), (-10 ** 6, 0), (0, 3), (Fraction(7, 3), Fraction(-2, 5)),
                         (Fraction(-3, 7), Fraction(11, 2)), (10 ** 100, 10 ** 99)]
    thresholds = [threshold_control(m, a, b) for m in [2, 3, 4, 8, 16] for a, b in coefficient_pairs]
    result = {
        'schema': 'spectral_01_exact_controls_v1',
        'status': 'all_required_checks_passed',
        'arithmetic': 'integer_and_Fraction_only',
        'runtime_assert_count': 0,
        'mathematical_scope': 'fixed integer m>=2; integer q>=1; moving domain/metric family',
        'limitations': [
            'Finite controls supplement the general mathematical proof; they do not prove an infinite limit.',
            'Synthetic boundary multisets check counting and indexing only; no smooth hypersurface is numerically built.',
            'Negative controls are explicit wrong alternatives through checking functions, not general mutation coverage.',
            'The extra-offset identity is true inside a multiple eigenspace and is rejected only as an incorrect first-index claim.',
            'Scope rejections merely enforce intended input range.'
        ],
        'summary': {'harmonic_rank_cases': len(ranks), 'count_cases': len(counts),
                    'index_cases': len(indices), 'negative_rejections': len(negatives),
                    'scaling_cases': len(scalings), 'rational_envelope_cases': len(envelopes),
                    'coefficient_threshold_cases': len(thresholds), 'tie_control_cases': 1},
        'harmonic_rank_controls': ranks, 'count_and_power_controls': counts,
        'multiset_index_controls': indices, 'negative_controls': negatives,
        'target_tie_robustness_control': tie_control, 'scaling_controls': scalings,
        'rational_envelope_controls': envelopes, 'all_sign_coefficient_threshold_controls': thresholds
    }
    encoded = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    Path(destination).write_bytes(encoded)
    print(json.dumps({'output': str(destination), 'sha256': hashlib.sha256(encoded).hexdigest(),
                      'bytes': len(encoded), 'summary': result['summary']}, sort_keys=True))

if __name__ == '__main__':
    require(len(sys.argv) == 2, 'expected_output_path')
    main(sys.argv[1])
