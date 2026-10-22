#!/usr/bin/env python3
"""Exact independent convention audit of odd-stratum completion; not a proof verifier.
No input files, external processes, network, filesystem writes, or assertions.
Run with normal Python, -O, and -OO. Output is a public mathematical audit only.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from math import factorial
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def odd_df(n):
    require(type(n) is int and n >= -1 and n % 2 == 1, 'invalid odd double factorial')
    z = 1
    for j in range(1, n + 1, 2):
        z *= j
    return z


def compositions(total, length):
    if length == 0:
        if total == 0:
            yield ()
        return
    if length == 1:
        if total > 0:
            yield (total,)
        return
    for a in range(1, total - length + 2):
        for rest in compositions(total - a, length - 1):
            yield (a,) + rest


def change(k):
    require(type(k) is int and -1 <= k <= 41 and k % 2 == 1, 'not an odd integrable order')
    out = defaultdict(Q)
    out[(k, ())] = Q(1)
    for G in range(1, (k + 1) // 4 + 1):
        kp = k - 4 * G
        for h in range(1, G + 1):
            prefactor = Q((kp + 2) * odd_df(k), odd_df(k - 2 * h + 2) * factorial(h) * 2 ** h)
            for gs in compositions(G, h):
                weight = 1
                for g in gs:
                    weight *= 2 * g - 1
                out[(kp, tuple(sorted(2 * g - 2 for g in gs)))] += prefactor * weight
    return dict(out)


def expansion(signature):
    require(type(signature) is tuple and 1 <= len(signature) <= 6, 'signature length guard')
    out = defaultdict(Q)
    for terms in product(*(list(change(k).items()) for k in signature)):
        base = tuple(sorted(t[0][0] for t in terms))
        tails = tuple(sorted(a for t in terms for a in t[0][1]))
        weight = Q(1)
        for t in terms:
            weight *= t[1]
        out[(base, tails)] += weight
    return dict(out)


# Independent literal coefficient transcription of OWR Conjecture 2.
# The unmodified +/-1 entries of nu are suppressed.
OWR = {
    (3,): {((-1,), (0,)): Q(1)},
    (5,): {((1,), (0,)): Q(3)},
    (7,): {((3,), (0,)): Q(5), ((-1,), (2,)): Q(3), ((-1,), (0, 0)): Q(7, 2)},
    (9,): {((5,), (0,)): Q(7), ((1,), (2,)): Q(9), ((1,), (0, 0)): Q(27, 2)},
    (3, 3): {((-1, 3), (0,)): Q(2), ((-1, -1), (0, 0)): Q(1)},
    (5, 3): {((1, 3), (0,)): Q(3), ((-1, 5), (0,)): Q(1), ((-1, 1), (0, 0)): Q(3)},
    (11,): {((7,), (0,)): Q(9), ((3,), (2,)): Q(15), ((-1,), (4,)): Q(5),
            ((3,), (0, 0)): Q(55, 2), ((-1,), (0, 2)): Q(33), ((-1,), (0, 0, 0)): Q(33, 2)},
}




def f2(a, n):
    require(type(a) is int and a % 2 == 1 and a >= -1, 'invalid finite-area odd order')
    require(type(n) is int and n >= 1, 'invalid f2 index')
    if n == 1:
        return Q(1, a + 2)
    value = Q(1)
    for j in range(n - 2):
        value *= a - 2 * j
    return value


def star_bottom(m1, m2, gs):
    require(type(gs) is tuple and 1 <= len(gs) <= 6 and all(type(g) is int and g > 0 for g in gs), 'invalid star genera')
    require(m1 + m2 == 4 * sum(gs) - 4, 'star order sum')
    h = len(gs)
    value = Q(0)
    for mask in range(1 << h):
        I = tuple(i for i in range(h) if mask & (1 << i))
        c = m1 + 2 - 4 * sum(gs[i] for i in I)
        if c > 0:
            value += c * f2(m1, len(I) + 1) * f2(m2, h - len(I) + 1)
    return value


def cycle_joinings(m1, m2, gs):
    # Independent finite count BEFORE MP's inclusion-exclusion rearrangement.
    # Sum the two cases in Proposition 6.7, enumerating the bounded l_i choices.
    h = len(gs)
    es = tuple(2 * g - 1 for g in gs)
    total = Q(0)
    for labels in product(range(3), repeat=h):
        I = tuple(i for i in range(h) if labels[i] == 0)
        J = tuple(i for i in range(h) if labels[i] == 1)
        K = tuple(i for i in range(h) if labels[i] == 2)
        c1 = m1 + 2 - 4 * sum(gs[i] for i in I)
        c2 = m2 + 2 - 4 * sum(gs[i] for i in J)
        if not K or min(c1, c2) <= 0:
            continue
        tree_factor = f2(m1, len(I) + 1) * f2(m2, len(J) + 1)
        if labels[-1] == 2:
            target = (c2 - 1) // 2
            ranges = tuple(range(0 if i == h - 1 else 1, es[i] + 1) for i in K)
            choices = sum(sum(ls) == target for ls in product(*ranges))
            total += tree_factor * c1 * c2 * 2 ** (len(K) - 1) * factorial(len(K) - 1) * choices
        else:
            face = c1 if labels[-1] == 0 else c2
            other_face = c2 if labels[-1] == 0 else c1
            target = (face - 1) // 2
            choices = sum(sum(ls) == target for ls in product(*(range(1, es[i] + 1) for i in K)))
            total += tree_factor * other_face * 2 ** len(K) * factorial(len(K) - 1) * target * choices
    return total


def multiply_series(left, right, degree):
    out = [Q(0)] * (degree + 1)
    for i, a in enumerate(left[:degree + 1]):
        for j, b in enumerate(right[:degree - i + 1]):
            out[i + j] += a * b
    return out


def power_series(base, exponent, degree):
    out = [Q(1)]
    for _ in range(exponent):
        out = multiply_series(out, base, degree)
    return out


def minimal_abelian_intersections(max_genus):
    # Sauvaget Theorem 1.6. Use x=t^2; invert sin(t/2)/(t/2) exactly.
    denom = [Q((-1) ** i, 2 ** (2 * i) * factorial(2 * i + 1)) for i in range(max_genus + 1)]
    S = [Q(1)]
    for i in range(1, max_genus + 1):
        S.append(-sum(denom[j] * S[i - j] for j in range(1, i + 1)))
    F = [Q(1)]
    integrals = {}
    for g in range(1, max_genus + 1):
        lower = power_series(F, 2 * g, g)[g]
        ag = (factorial(2 * g) * S[g] - lower) / (2 * g * (2 * g - 1))
        F.append((2 * g - 1) * ag)
        require(power_series(F, 2 * g, g)[g] == factorial(2 * g) * S[g], 'Sauvaget recursion')
        integrals[g] = (-1) ** g * ag
    return integrals


def cq(g, n):
    dim = 2 * g - 2 + n
    require(dim > 0 and n % 2 == 0, 'invalid quadratic dimension')
    return Q(2 ** (2 * g + 1) * (-1) ** (g - 1 + n // 2), factorial(dim - 1))


def ch(g):
    return Q(2 ** (2 * g + 1) * (-1) ** g, factorial(2 * g - 1))


def power_tail_factor(g):
    require(type(g) is int and g >= 1, 'invalid tail genus')
    return 2 ** (2 * g - 1)

def run():
    rows = []
    for sig, expected in OWR.items():
        actual = expansion(sig)
        require(actual.pop((tuple(sorted(sig)), ())) == 1, 'diagonal not one')
        require(set(actual) == set(expected), 'correction support differs')
        for key in sorted(expected):
            h = len(key[1])
            require(actual[key] * 2 ** h == expected[key], 'OWR to DGY factor differs')
            require(actual[key] != expected[key], 'unexpected literal equality')
            rows.append({'orders': sig, 'quadratic_core': key[0], 'abelian_orders': key[1],
                         'owr_printed_coefficient': str(expected[key]),
                         'dgy_coefficient': str(actual[key]), 'required_product_volume_divisor': 2 ** h})
    require(len(rows) == 19, 'lost an OWR correction coefficient')

    # Compare ordered-composition summation to a second, multiplicity-based formula.
    coefficient_checks = 0
    for k in range(-1, 42, 2):
        for (kp, tail), c in change(k).items():
            if not tail:
                require(kp == k and c == 1, 'bad diagonal')
                continue
            gs = tuple((t + 2) // 2 for t in tail)
            h = len(gs)
            mult = 1
            for value in Counter(gs).values():
                mult *= factorial(value)
            p = 1
            for g in gs:
                p *= 2 * g - 1
            alternate = Q((kp + 2) * odd_df(k) * p, odd_df(k - 2 * h + 2) * 2 ** h * mult)
            require(c == alternate, 'ordered/unordered symmetry mismatch')
            require(kp >= -1 and k - kp == 4 * sum(gs), 'invalid genus/order recursion')
            coefficient_checks += 1

    # Finite triangular recursion audit with labels retained by the input factors.
    genus_checks = 0
    for n in (4, 6):
        for sig in product((-1, 1, 3, 5), repeat=n):
            if (sum(sig) + 4) % 4:
                continue
            g = (sum(sig) + 4) // 4
            if g < 0 or 2 * g - 2 + n <= 0:
                continue
            d = 2 * g - 2 + n
            for (core, tail), c in expansion(sig).items():
                G = sum((t + 2) // 2 for t in tail)
                core_g = (sum(core) + 4) // 4
                require(core_g == g - G, 'genus not reduced by tail genera')
                require(2 * core_g - 2 + n + 2 * G == d, 'product dimension mismatch')
                require(c > 0, 'nonpositive completion coefficient')
                if tail:
                    require(core_g < g, 'nonterminating claimed genus recursion')
                genus_checks += 1

    # DGY section 1.2, using its equation (32) product convention.
    actual = Q(5, 9)  # coefficient of pi^4
    completed = Q(2, 3)
    mixed_product = Q(1, 2) * Q(factorial(1) * 4 * factorial(1), factorial(3)) * 2 * Q(1, 3)
    correction = Q(1, 2) * mixed_product
    require(mixed_product == Q(2, 9), 'DGY product calibration')
    require(actual + correction == completed, 'DGY worked example does not close')

    # Independent minimal-stratum values from the imported generating-series theorem.
    ab = minimal_abelian_intersections(6)
    require([ab[g] for g in (1, 2, 3)] == [Q(-1, 24), Q(1, 640), Q(-305, 580608)], 'minimal abelian calibration')
    power_ab = {g: power_tail_factor(g) * ab[g] for g in ab}
    require([power_ab[g] for g in (1, 2, 3)] == [Q(-1, 12), Q(1, 80), Q(-305, 18144)], 'quadratic-power tail calibration')

    # The old diagnostic substituted abelian rather than quadratic-power classes.
    # Retain it explicitly as a rejected convention, not a theorem counterexample.
    mp_C = cq(1, 4)
    core_intersection = Q(-1)
    bottom_intersection = Q(1)
    graph_weight = Q(1 * 2, 2)
    old_wrong_convention = mp_C * graph_weight * bottom_intersection * core_intersection * ab[1]
    mp_correction = mp_C * graph_weight * bottom_intersection * core_intersection * power_ab[1]
    require(old_wrong_convention == Q(1, 18), 'historical diagnostic changed')
    require(mp_correction == correction == Q(1, 9), 'repaired MP/DGY calibration')
    require(actual + mp_correction == completed, 'repaired completed volume')

    # Exact all-genus algebra instantiated on a bounded grid. Pi exponents factor out.
    conversion_checks = 0
    conversion_samples = []
    for total in range(1, 7):
        for h in range(1, total + 1):
            for gs in compositions(total, h):
                expected_factor = 2 ** (2 * total - h)
                observed_factor = 1
                for a in gs:
                    observed_factor *= power_tail_factor(a)
                require(expected_factor == observed_factor, 'tail-power factor')
                for g0 in range(4):
                    for n in (2, 4, 6):
                        d0 = 2 * g0 - 2 + n
                        if d0 <= 0:
                            continue
                        d = d0 + 2 * total
                        plain = Q(factorial(d0 - 1), factorial(d - 1)) * cq(g0, n)
                        for a in gs:
                            plain *= factorial(2 * a - 1) * ch(a)
                        require(plain / cq(g0 + total, n) == 2 ** h, 'factorial convolution scaling')
                        dgy_scale = expected_factor * plain / (cq(g0 + total, n) * 2 ** (2 * h))
                        repaired_mp_scale = Q(observed_factor, 2 ** h)
                        require(dgy_scale == repaired_mp_scale == 2 ** (2 * total - 2 * h), 'all-sunflower conversion')
                        conversion_checks += 1
                if gs in ((1,), (2,), (3,), (1, 1), (1, 2), (1, 1, 1)):
                    conversion_samples.append({'tail_genera': gs, 'quadratic_power_over_abelian_intersections': expected_factor})

    # MP (58),(60): compare local graph weights with DGY without using volume values.
    graph_coefficient_checks = 0
    for m in range(3, 42, 2):
        for (mp, tails), coefficient in change(m).items():
            if not tails:
                continue
            gs = tuple((t + 2) // 2 for t in tails)
            h = len(gs)
            automorphisms = 1
            for multiplicity in Counter(gs).values():
                automorphisms *= factorial(multiplicity)
            prongs = mp + 2
            for a in gs:
                prongs *= 4 * a - 2
            bottom = Q(odd_df(m), odd_df(m - 2 * (h - 1)))
            require(coefficient == Q(prongs, 2 ** (2 * h) * automorphisms) * bottom, 'local graph/DGY coefficient')
            graph_coefficient_checks += 1

    # MP (64), imported from CGPT Theorem 1.2, versus direct finite cycle joinings.
    star_checks = 0
    for total in range(1, 7):
        for h in range(1, min(total, 4) + 1):
            for gs in compositions(total, h):
                for m1 in range(-1, 4 * total - 2, 2):
                    m2 = 4 * total - 4 - m1
                    b = star_bottom(m1, m2, gs)
                    require(b == star_bottom(m2, m1, gs), 'star marking symmetry')
                    require(b == cycle_joinings(m1, m2, gs), 'star bottom/cycle joining equality')
                    require(b >= 0 and b.denominator == 1, 'star count integrality')
                    star_checks += 1

    # Reconstruct rather than merely add MP's three Q(5,3) special-star rows.
    star_rows = []
    for gs, expected_bottom, expected_product, expected_term in (
        ((3,), Q(1), Q(-305, 18144), Q(-1525, 18144)),
        ((2, 1), Q(6), Q(-1, 160), Q(-3, 160)),
        ((1, 1, 1), Q(30), Q(-5, 288), Q(-5, 1728)),
    ):
        b = star_bottom(5, 3, gs)
        require(b == expected_bottom, 'Q53 star bottom')
        vertex_product, prongs, aut = b, 1, 1
        for a in gs:
            vertex_product *= power_ab[a]
            prongs *= 4 * a - 2
        for multiplicity in Counter(gs).values():
            aut *= factorial(multiplicity)
        term = Q(prongs, 2 ** len(gs) * aut) * vertex_product
        require(vertex_product == expected_product and term == expected_term, 'Q53 reconstructed star row')
        star_rows.append({'tail_genera': gs, 'bottom_intersection': str(b), 'vertex_product': str(vertex_product), 'prong_product': prongs, 'automorphisms': aut, 'contribution': str(term)})

    # OWR's seven displayed families at total marking count two.
    empty_cores = {(-1, 1), (1, 3)}
    owr_two_point_cases = []
    for initial in OWR:
        for nu in product((-1, 1), repeat=2 - len(initial)):
            target = tuple(sorted(initial + nu))
            if (sum(target) + 4) % 4:
                continue
            unavailable = sorted({tuple(sorted(core + nu)) for core, tail in OWR[initial] if tuple(sorted(core + nu)) in empty_cores})
            require(bool(unavailable), 'unexpected all-existing two-point OWR case')
            owr_two_point_cases.append({'target': target, 'target_known_empty': target in empty_cores, 'known_empty_listed_correction_cores': unavailable})
    require(len(owr_two_point_cases) == 6, 'OWR two-point scope count')

    # The main and nonzero sunflower entries are source inputs, not recomputed geometry.
    mp_terms = [Q(-35, 648)] + [Q(row['contribution']) for row in star_rows] + [Q(-7, 2160), Q(0), Q(0)]
    require(sum(mp_terms) == Q(-73, 448), 'MP page 5 row sum')
    special_star = sum(mp_terms[1:4])
    require(special_star == Q(-19177, 181440), 'special-star subtotal')
    pi_exponent = 2 * 3 - 2 + 2
    scale = cq(3, 2)
    require(scale * sum(mp_terms) == Q(73, 420), 'MP page 5 rational coefficient')
    require(pi_exponent == 6 and pi_exponent != 4, 'MP printed pi-power discrepancy')

    return {
        'status': 'PASS_CORRECTED_CONVENTION_AUDIT_WITH_OWR_SCOPE_HOLD', 'proof_turns': 0,
        'scope': 'Exact finite arithmetic and cited theorem-application checks; not formal certification of geometric theorems.',
        'owr_terms_checked': len(rows), 'coefficient_checks': coefficient_checks,
        'genus_dimension_recursion_checks': genus_checks, 'owr_coefficients': rows,
        'minimal_abelian_intersections': {str(g): str(ab[g]) for g in ab},
        'quadratic_power_intersections': {str(g): str(power_ab[g]) for g in ab},
        'dgy_Q3m111': {'actual_pi4': str(actual), 'completed_pi4': str(completed), 'mixed_product_pi4': str(mixed_product), 'correction_pi4': str(correction)},
        'mp_Q3m111_repair': {'rejected_abelian_class_substitution_pi4': str(old_wrong_convention), 'quadratic_power_tail_intersection': str(power_ab[1]), 'corrected_correction_pi4': str(mp_correction), 'corrected_completed_pi4': str(actual + mp_correction)},
        'all_sunflower_conversion_checks': conversion_checks, 'graph_coefficient_checks': graph_coefficient_checks,
        'tail_conversion_samples': conversion_samples,
        'two_singularity_bottom_vs_direct_cycle_checks': star_checks,
        'owr_two_point_scope_cases': owr_two_point_cases,
        'mp_Q53': {'reconstructed_special_star_rows': star_rows, 'IT_sum': str(sum(mp_terms)), 'special_star_IT_subtotal': str(special_star), 'MV_rational_coefficient': str(scale * sum(mp_terms)), 'pi_power_from_equation_56': pi_exponent, 'printed_pi_power': 4},
        'limitations': ['OWR mixed-product normalization remains unspecified; the 2^h coefficient ratio is not a source declaration.', 'The all-target OWR existence clause remains unresolved; special stars are necessary in the n=2 extension.', 'The MP correction is an authored convention repair, not a verified author erratum.', 'No geometric theorem or unbounded graph enumeration is certified by finite tests.', 'No novelty, unconditional complete resolution, or journal acceptance claim.']
    }


if __name__ == '__main__':
    require(len(sys.argv) == 1, 'This verifier takes no arguments and never writes files.')
    print(json.dumps(run(), indent=2, sort_keys=True))
