"""Fresh bounded manuscript-first arithmetic controls; no target imports or writes."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def primitive_points(dimension, bound):
    result = []
    for v in product(range(-bound, bound + 1), repeat=dimension + 1):
        nonzero = [x for x in v if x]
        if not nonzero or nonzero[0] < 0:
            continue
        common = 0
        for x in v:
            common = gcd(common, x)
        if common == 1:
            result.append(v)
    return result


def add(a, b, modulus):
    return [(x + y) % modulus for x, y in zip(a, b)]


def mul(a, b, modulus):
    out = [0] * len(a)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] = (out[i ^ j] + x * y) % modulus
    return out


def char_eval(a, character, modulus):
    return sum(x * (-1 if (i & character).bit_count() % 2 else 1)
               for i, x in enumerate(a)) % modulus


def main():
    points = {}
    chart_checks = 0
    for n in range(3):
        for bound in range(3):
            ps = primitive_points(n, bound)
            require(len(ps) == len(set(ps)), 'primitive duplicates')
            require(not ps if bound == 0 else bool(ps), 'height-zero boundary')
            for v in ps:
                # Every standard projective representative is in a chart; degree-two
                # homogeneous evaluation scales by exactly v[j]^2 in that chart.
                for j, pivot in enumerate(v):
                    if pivot:
                        chart = [F(x, pivot) for x in v]
                        q_hom = sum(x * x for x in v)
                        q_chart = sum(x * x for x in chart)
                        require(F(q_hom, pivot * pivot) == q_chart, 'chart scaling')
                        chart_checks += 1
            points[str((n, bound))] = len(ps)
    require(primitive_points(0, 2) == [(1,)], 'P0 coordinate')
    p2 = primitive_points(2, 1)
    infinity = [(x, y, z) for x, y, z in p2 if x*x + z*z == 0]
    require(infinity == [(0, 1, 0)], 'compactification boundary witness')
    affine_checks = 0
    for denominator in range(1, 6):
        for numerator in range(-8, 9):
            x = F(numerator, denominator)
            require(x*x + 1 > 0, 'affine x2+1')
            affine_checks += 1
    origin = (0, 0)
    require(sum(x*x for x in origin) == 0, 'singular rational origin evaluation')
    # The normalization's coefficient field Q(i) has no Q-map, witnessed by
    # i^2+1=0. Bounded x2+1 checks supplement the universal ordered-field proof.
    lam = F(-3)
    j = F(256) * (1-lam+lam*lam)**3 / (lam*lam*(1-lam)**2)
    require(j == F(35152, 9) and j.denominator != 1, 'exact j invariant')
    discriminants = []
    for ell in (1, 3, 7):
        roots = (0, ell, -3*ell)
        delta = 16
        for a, b in [(0, 1), (0, 2), (1, 2)]:
            delta *= (roots[a] - roots[b])**2
        require(delta == 2304 * ell**6, 'twist discriminant')
        discriminants.append([ell, delta])
    euler_cases = 0
    denominator_zero_controls = 0
    for q in (3, 5, 7, 11):
        for a in (-2, 0, 1, 2):
            for z in (F(-3), F(-1), F(1), F(2), F(3)):
                direct = 1 - F(a, q)*z + F(1, q)*z*z
                inverse = z*z - F(a, q)*z + F(1, q)
                require(direct-inverse == F(q-1, q)*(1-z*z), 'Euler identity')
                if inverse:
                    ratio = direct / inverse
                    require(ratio*inverse == direct, 'Euler ratio')
                    if z in (1, -1):
                        require(ratio == 1, 'central theta sign')
                else:
                    denominator_zero_controls += 1
                euler_cases += 1
    # A nonunit/zero denominator must remain an explicit hypothesis.
    q, a, z = 3, 4, F(1)
    require(z*z-F(a, q)*z+F(1, q) == 0, 'missing denominator control')
    denominator_zero_controls += 1
    group_cases = 0
    bad_character_projector = [F(1, 2), F(1, 2)]
    require(any(x.denominator % 2 == 0 for x in bad_character_projector),
            'character projector integrality negative control')
    for rank in (1, 2, 3):
        size, modulus = 2**rank, 8
        one = [1] + [0]*(size-1)
        for seed in range(12):
            k = [(seed + 3*i + i*i) % modulus for i in range(size)]
            for active_generator in (1, size-1):
                one_plus_g = one[:]
                one_plus_g[active_generator] += 1
                u = add(one, mul(k, one_plus_g, modulus), modulus)
                r = add(one, [(2*x) % modulus for x in k], modulus)
                for character in range(size):
                    sign = -1 if (active_generator & character).bit_count() % 2 else 1
                    expected = 1 if sign == -1 else char_eval(r, character, modulus)
                    require(char_eval(u, character, modulus) == expected, 'universal character values')
                # u^2=1 mod2 in this finite elementary-two-group ring. A finite
                # geometric series explicitly constructs its inverse mod8.
                u2 = mul(u, u, modulus)
                require(all((x-y) % 2 == 0 for x, y in zip(u2, one)), 'unit modulo2')
                nilpotent = [(x-y) % modulus for x, y in zip(one, u2)]
                power, series = one[:], one[:]
                for _ in range(2):
                    power = mul(power, nilpotent, modulus)
                    series = add(series, power, modulus)
                inverse_u = mul(u, series, modulus)
                require(mul(u, inverse_u, modulus) == one, 'integral group ring inverse mod8')
                group_cases += 1
    smoothing_cases = 0
    for c in (3, 5, 7, 9):
        for gamma in (F(1), F(2), F(3), F(5)):
            plus = c*c-c*gamma
            minus = c*c-c/gamma
            require(plus-gamma*minus == c*(c+1)*(1-gamma), 'smoothing identity')
            ratio = plus/(gamma*minus)
            if gamma == 1:
                require(ratio == 1, 'smoothing central value')
            # No unit claim is made at arbitrary scalar evaluations: those
            # need not extend to the localization in the manuscript.
            smoothing_cases += 1
    print(json.dumps({'status': 'PASS_BOUNDED_FRESH_CONTROLS',
                      'primitive_projective_counts': points,
                      'chart_scaling_comparisons': chart_checks,
                      'ordered_field_affine_checks': affine_checks,
                      'compactification_rational_boundary_witness': infinity,
                      'normalization_counterexample_scope': 'Origin evaluated. Q(i)[x] normalization and absence of a Q-map are manual algebra/ordered-field deductions in INITIAL, not a normalization algorithm run.',
                      'j_invariant': str(j), 'discriminants': discriminants,
                      'exact_Euler_identity_cases': euler_cases,
                      'zero_denominator_controls_kept': denominator_zero_controls,
                      'integral_group_ring_unit_and_character_cases_mod8': group_cases,
                      'nonintegral_character_projector_control': [str(x) for x in bad_character_projector],
                      'smoothing_identity_cases': smoothing_cases,
                      'scope': 'Bounded falsification/arithmetic only. No undecidability, deep arithmetic input, localization-unit hypothesis, or formal certification is proved by these tests.'}, indent=2))


if __name__ == '__main__':
    main()
