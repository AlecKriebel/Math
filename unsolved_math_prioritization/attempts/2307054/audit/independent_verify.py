#!/usr/bin/env python3
"""Independent exact audit. Does not import or execute the submitted verifier.

Rows are computed using repeated EGF polynomial multiplication and division
by the power index, rather than the submitted exponential derivative recurrence.
All quotient remainders are checked. No floating-point operations are used.
"""
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json

D = 200
BAND = 100
PROFILE_D = 40
EXPECTED_MANIFEST = 'bc440603567a5e83bcfb91466bb3196e741bb5d57cabca2726585174d6f47f6d'


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def egf_power_rows(degree, initial=-1):
    """Compute exp(g)-1 as sum of the polynomials g^m/m! in EGF basis."""
    binomials = [[comb(k, j) for j in range(k + 1)]
                 for k in range(degree + 1)]
    rows = [[initial] + [0] * degree]
    divisions = 0
    for n in range(1, degree + 1):
        previous = rows[-1]
        g = [(j, j * previous[j - 1])
             for j in range(1, degree + 1) if previous[j - 1]]
        power = [1] + [0] * degree
        result = [0] * (degree + 1)
        for m in range(1, degree + 1):
            support = [(k, value) for k, value in enumerate(power) if value]
            product = [0] * (degree + 1)
            for j, g_j in g:
                for k, p_k in support:
                    if j + k > degree:
                        break
                    product[j + k] += binomials[j + k][j] * g_j * p_k
            if not any(product):
                break
            power = []
            for value in product:
                quotient, remainder = divmod(value, m)
                require(remainder == 0, 'Nonintegral divided exponential power')
                power.append(quotient)
                divisions += 1
            result = [a + b for a, b in zip(result, power)]
        rows.append(result)
    return rows, divisions


def signed_profiles(degree):
    """Enumerate every nondecreasing positive level profile of sum <= degree."""
    S = [[0] * (degree + 1) for _ in range(degree + 1)]
    S[0][0] = 1
    for a in range(1, degree + 1):
        for b in range(1, a + 1):
            S[a][b] = S[a - 1][b - 1] + b * S[a - 1][b]
    rows = [[Fraction(0)] * (degree + 1) for _ in range(degree + 1)]
    rows[0][0] = Fraction(-1)
    profile_count = 0

    def visit(previous, total, depth, stirling_product):
        nonlocal profile_count
        for next_layer in range(previous, degree - total + 1):
            new_total = total + next_layer
            product = stirling_product * S[next_layer][previous]
            rows[depth + 1][new_total] += Fraction(
                (-1) ** next_layer * product, factorial(next_layer))
            profile_count += 1
            visit(next_layer, new_total, depth + 1, product)

    visit(1, 0, 0, 1)
    return rows, profile_count, S


def interval(value, scale=10**12):
    low = value.numerator * scale // value.denominator
    require(Fraction(low, scale) < value < Fraction(low + 1, scale),
            'Strict enclosure endpoint equality')
    return [str(Fraction(low, scale)), str(Fraction(low + 1, scale))]


def main():
    public = Path(__file__).resolve().parent.parent / 'public'
    manifest = public / 'SHA256SUMS'
    require(sha256(manifest.read_bytes()).hexdigest() == EXPECTED_MANIFEST,
            'Frozen manifest mismatch')
    manifest_count = 0
    for line in manifest.read_text().splitlines():
        checksum, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        require('/' not in name and '\\' not in name, 'Unexpected manifest path')
        require(sha256((public / name).read_bytes()).hexdigest() == checksum,
                'Frozen file mismatch: ' + name)
        manifest_count += 1
    require(manifest_count == 6, 'Unexpected manifest size')

    rows, divisions = egf_power_rows(D)
    facts = [factorial(k) for k in range(D + 1)]
    maximum = Fraction(0)
    maximizers = []
    for n in range(1, D + 1):
        require(all(value == 0 for value in rows[n][:n]), 'Valuation failure')
        require(rows[n][n] == -facts[n], 'Leading coefficient failure')
        for k in range(D + 1):
            value = Fraction(rows[n][k], facts[k])
            require(abs(value) <= 1, f'Unit bound failure {(n,k)}')
            if k > n and abs(value) >= maximum:
                if abs(value) > maximum:
                    maximum = abs(value)
                    maximizers = []
                maximizers.append([n, k, str(value)])
    require(maximum == Fraction(2663, 4480), 'Maximum mismatch')
    require(maximizers == [[6, 13, '-2663/4480']], 'Maximizer mismatch')

    profiles, profile_count, S = signed_profiles(PROFILE_D)
    for n in range(PROFILE_D + 1):
        for k in range(PROFILE_D + 1):
            require(profiles[n][k] == Fraction(rows[n][k], facts[k]),
                    f'Level-profile mismatch {(n,k)}')

    stabilization_pairs = 0
    for j in range(BAND + 1):
        for n in range(max(1, j), D - j):
            require(Fraction(rows[n][n + j], facts[n + j]) ==
                    Fraction(rows[n+1][n+1+j], facts[n+1+j]),
                    f'Stabilization failure {(n,j)}')
            stabilization_pairs += 1
    # Offset j=2 first becomes stable at n=2; n=1 is genuinely different.
    require(Fraction(rows[1][3], facts[3]) != Fraction(rows[2][4], facts[4]),
            'Boundary witness failure')

    Q = Fraction
    inequalities = {
        'e_geometric_tail': Q(8,3) + Q(5,96) == Q(87,32) < Q(11,4) < 3,
        'radius_11_10_first': Q(11,4) * Q(10,9) < Q(31,10),
        'radius_11_10_second': Q(11,4)**2 * Q(100,69) < 11,
        'first_three_cutoff': Q(11,10)**128 > 3**11,
        'radius_23_20_first': Q(87,32) * Q(20,17) < Q(16,5),
        'square_root_bound': Q(11,4) < Q(5,3)**2,
        'radius_23_20_second': Q(11,4)**2 * Q(5,3) * Q(100,97) < 13,
        'fourth_cutoff': Q(21,20)**136 > 3**6,
    }
    for label, ok in inequalities.items():
        require(ok, label)
    r, q = Q(21,20), Q(21,23)
    polynomial = sum((Q(abs(rows[3][k]), facts[k]) * r**k for k in range(D+1)), Q(0))
    tail = Q(11,4)**14 * q**201 / (1-q)
    require(Q(4620,1000) < polynomial + tail < Q(4621,1000) < 5,
            'Weighted-norm certificate failure')
    positive, _ = egf_power_rows(6, initial=1)
    require(Q(positive[3][6], facts[6]) == Q(25,24), 'Positive majorant mismatch')
    require(Q(rows[3][6], facts[6]) == Q(1,24), 'Signed coefficient mismatch')
    require(Q(S[6][3] * S[9][6] * S[12][9], factorial(12)) == Q(2835,256),
            'Single profile mismatch')
    # Check the claimed complement logically on a larger finite domain; the
    # unbounded equivalence is supplied by elementary inequality negation.
    for n in range(1, 351):
        for k in range(501):
            covered = k < n or k <= 200 or 0 <= k - n <= 100 or n <= 4
            remainder = n >= 5 and k >= 201 and k - n >= 101
            require(covered != remainder, 'Coverage complement mismatch')

    output = {
        'verdict': 'PASS: stated partial bounds only; universal problem remains unresolved',
        'frozen_manifest_sha256': EXPECTED_MANIFEST,
        'frozen_file_count': manifest_count,
        'algorithm': 'EGF polynomial powers g^m/m!, exact integer convolution and checked division',
        'floating_point_used': False,
        'rectangle_pairs': D * (D+1),
        'coefficient_matrix_sha256': sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest(),
        'checked_integer_divisions': divisions,
        'largest_off_leading_modulus': str(maximum),
        'all_maximizers': maximizers,
        'signed_level_profile_crosscheck': {
            'maximum_degree_and_iterate': PROFILE_D,
            'coefficient_pairs': (PROFILE_D+1)**2,
            'profiles_enumerated': profile_count,
        },
        'stabilization_adjacent_pairs': stabilization_pairs,
        'offset_2_before_stability': {'a_1_3': str(Q(rows[1][3], facts[3])),
                                    'a_2_4': str(Q(rows[2][4], facts[4]))},
        'analytic_rational_checks': inequalities,
        'polynomial_strict_enclosure': interval(polynomial),
        'tail_bound_strict_enclosure': interval(tail),
        'norm_upper_bound_strict_enclosure': interval(polynomial+tail),
        'validated_remaining_region': 'n >= 5, k >= 201, k-n >= 101',
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
