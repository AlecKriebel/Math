#!/usr/bin/env python3
"""Fresh exact bounded controls, not a test of the imported analytic theorem.

Standard library only; no source/project imports, network or filesystem writes.
The continuous all-phase statements are proved separately. This finite grid,
finite torus and scalar examples only test their selected interfaces.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json

CHECKS = 0


def require(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise RuntimeError(message)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def divide(x, n):
    return (x[0] / n, x[1] / n)


def variation_cube(sequence, allowed=None, anchored=False):
    indices = list(range(len(sequence))) if allowed is None else allowed
    maximum = F(0)
    for length in range(2, len(indices) + 1):
        for endpoints in combinations(indices, length):
            if anchored and endpoints[0] != 0:
                continue
            value = sum(abs(sequence[b] - sequence[a]) ** 3
                        for a, b in zip(endpoints, endpoints[1:]))
            maximum = max(maximum, value)
    return maximum


def main():
    h, q = F(1, 8), F(1, 16)
    phases = [F(i, 128) for i in range(-8, 9)]
    phase_pairs = off_diagonal_pairs = annular_windows = integrand_samples = 0
    for a, b in product(phases, repeat=2):
        lower, upper = -h - min(a, b), h - max(a, b)
        length = upper - lower
        require(F(1, 8) <= length <= F(1, 4), 'Positive overlap length')
        require(length == 2 * h - abs(a - b), 'Exact overlap length')
        require(max(abs(lower), abs(upper)) <= F(3, 16), 'Uniform window radius')
        reflected = (-h - min(-a, -b), h - max(-a, -b))
        require(reflected == (-upper, -lower), 'Reflection convention')
        for k, ell in product(range(-3, 4), repeat=2):
            left = max(k - h - a, ell - h - b)
            right = min(k + h - a, ell + h - b)
            if left <= right:
                require(k == ell, 'Off-diagonal cell overlap')
                require((left, right) == (k + lower, k + upper), 'Same-cell interval')
            if k != ell:
                require(left > right, 'Different integer windows must be disjoint')
                off_diagonal_pairs += 1
        for k in range(-12, 13):
            if k:
                require(min(abs(k + lower), abs(k + upper)) >= F(13, 16) * abs(k),
                        'Signed denominator lower bound')
                for sample in (lower, (lower + upper) / 2, upper):
                    difference = F(1, 1) / (k + sample) - F(1, k)
                    require(difference == -sample / (k * (k + sample)), 'Reciprocal identity')
                    require(abs(difference) <= F(3, 13 * k * k), 'Error envelope sample')
                    integrand_samples += 1
            left, right = k + lower, k + upper
            if left >= 0:
                radial_lower, radial_upper = left, right
            elif right <= 0:
                radial_lower, radial_upper = -right, -left
            else:
                radial_lower, radial_upper = F(0), max(abs(left), abs(right))
            for first in range(4):
                for last in range(first + 1, 5):
                    inner, outer = F(2 * first + 1, 2), F(2 * last + 1, 2)
                    selected = first < abs(k) <= last
                    if selected:
                        require(inner < radial_lower and radial_upper < outer,
                                'Entire signed annular window')
                    else:
                        require(radial_upper <= inner or radial_lower >= outer,
                                'Excluded signed/zero window')
                    annular_windows += 1
        phase_pairs += 1
    input_area, output_area = 4 * h * h, 4 * q * q
    require(input_area == F(1, 16) and output_area == F(1, 64), 'Cell areas')
    require(input_area / output_area == 4, 'Area ratio')
    coefficient_cube = 8 ** 3 * (input_area / output_area) ** 2
    require(coefficient_cube == 8192, 'Analytic coefficient cubed')

    def action(x, i, j):
        return ((x[0] + i) % 3, (x[1] + j) % 4)

    def f(x):
        u, v = x
        return (F(u - 2 * v), F(u + v - 2))

    def g(x):
        u, v = x
        return (F(2 * u + v + 1), F(v - u))

    def ergodic(x, cutoff):
        answer = (F(0), F(0))
        for n in range(-cutoff, cutoff + 1):
            if n:
                answer = add(answer, divide(mul(f(action(x, n, 0)),
                                                g(action(x, 0, n))), n))
        return answer

    orbit_identities = 0
    for x in product(range(3), range(4)):
        for radius in (1, 2):
            for maximum in (1, 2):
                extent = radius + maximum
                indices = list(product(range(-extent, extent + 1), repeat=2))
                array_a = {(i, j): f(action(x, i, j)) for i, j in indices}
                array_b = {(i, j): g(action(x, i, j)) for i, j in indices}
                for i, j in product(range(-radius, radius + 1), repeat=2):
                    for cutoff in range(maximum + 1):
                        answer = (F(0), F(0))
                        for n in range(-cutoff, cutoff + 1):
                            if n:
                                answer = add(answer, divide(mul(array_a[(i + n, j)],
                                                                array_b[(i, j + n)]), n))
                        require(answer == ergodic(action(x, i, j), cutoff),
                                'Finite-window commuting orbit-array identity')
                        orbit_identities += 1

    variation_records = []
    for maximum in range(1, 13):
        sequence = [F(index % 2) for index in range(maximum + 1)]
        full = variation_cube(sequence)
        allowed = [0] + [2 ** power for power in range(4) if 2 ** power <= maximum]
        dyadic = variation_cube(sequence, allowed)
        require(full == maximum, 'Alternation full variation cube')
        require(max(sequence) == 1 and dyadic <= 2, 'Maximal/dyadic negative control')
        variation_records.append({'last_index': maximum, 'full_variation_cube': int(full),
                                  'dyadic_variation_cube': int(dyadic)})
    anchor_sequences = [[F(0), F(3), F(-2), F(7), F(0)],
                        [F(0), F(1, 3), F(-2, 7), F(3, 5)],
                        [F(0)] * 5]
    for sequence in anchor_sequences:
        require(variation_cube(sequence) == variation_cube(sequence, anchored=True),
                'Anchored homogeneous variation')

    atom_contributions = [F(1, 2 ** (3 * j)) * 2 ** (3 * j) for j in range(1, 9)]
    require(atom_contributions == [1] * 8 and sum(atom_contributions) == 8,
            'Partition-norm/supremum-norm negative control')

    def permutation_power(permutation, x, exponent):
        if exponent < 0:
            inverse = [0] * len(permutation)
            for i, value in enumerate(permutation):
                inverse[value] = i
            return permutation_power(inverse, x, -exponent)
        for unused in range(exponent):
            x = permutation[x]
        return x

    s, t = [1, 2, 0], [1, 0, 2]
    fv, gv = [F(1), F(3), F(-2)], [F(4), F(-1), F(5)]

    def noncommuting_action(x, i, j):
        return permutation_power(s, permutation_power(t, x, j), i)

    orbit_base = noncommuting_action(0, 1, 0)
    lattice = sum(fv[noncommuting_action(0, 1 + n, 0)] *
                  gv[noncommuting_action(0, 1, n)] / n for n in (-1, 1))
    original = sum(fv[permutation_power(s, orbit_base, n)] *
                   gv[permutation_power(t, orbit_base, n)] / n for n in (-1, 1))
    require(lattice == -15 and original == -12 and lattice != original,
            'Noncommutation must break the transfer identity')
    for cutoff in range(1, 21):
        require(sum(F(1, n) + F(1, -n) for n in range(1, cutoff + 1)) == 0,
                'Identity-action symmetric cancellation')
    for power in range(1, 9):
        require(sum(F(1, n) for n in range(1, 2 ** power + 1)) >= F(power, 2),
                'One-sided harmonic boundary control')
    print(json.dumps({'status': 'OWN_BOUNDED_EXACT_CONTROLS_PASS', 'checks': CHECKS,
                      'phase_pairs_in_closed_rational_grid': phase_pairs,
                      'off_diagonal_integer_cell_pairs': off_diagonal_pairs,
                      'signed_and_zero_annular_window_cases': annular_windows,
                      'reciprocal_error_integrand_samples': integrand_samples,
                      'input_area': str(input_area), 'output_area': str(output_area),
                      'continuous_coefficient_cube_after_factoring_Cr': int(coefficient_cube),
                      'commuting_finite_torus_sequence_identities': orbit_identities,
                      'full_versus_dyadic_variation_controls': variation_records,
                      'noncommuting_lattice_value': str(lattice),
                      'noncommuting_original_value': str(original),
                      'scope': 'Finite exact interface controls only; no native program or imported analytic theorem tested.',
                      'universal_proof_reference': 'PREEXPOSURE_PROOF.md'}, indent=2))


if __name__ == '__main__':
    main()
