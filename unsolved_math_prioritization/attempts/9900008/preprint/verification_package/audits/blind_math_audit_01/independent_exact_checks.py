#!/usr/bin/env python3
"""Independent finite exact diagnostics; the universal proof is in REPORT.md.

No candidate modules are imported. No network or writes occur.
"""
from fractions import Fraction as F
from itertools import product
import json


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def push_residues(b0, b1, weights=(F(1), F(2))):
    result = {}
    for r, w in ((b0 % 1, weights[0]), ((F(1, 2)+b1) % 1, weights[1])):
        result[r] = result.get(r, F(0)) + w
    return result


def run():
    labels = [F(0), F(1, 2), F(1, 3), F(2, 3)]
    quotient_survivors = []
    for a, b in product(labels, repeat=2):
        received = {}
        for r, w in ((a, F(1)), (b, F(2))):
            received[r] = received.get(r, F(0)) + w
        if received == {F(0): F(1), F(1, 2): F(2)}:
            quotient_survivors.append([str(a), str(b)])
    check(quotient_survivors == [['0', '1/2']], 'quotient rigidity failure')

    translations = [F(j, 12) for j in range(-24, 25)]
    balanced = 0
    for b0, b1 in product(translations, repeat=2):
        yes = push_residues(b0, b1) == {F(0): F(1), F(1, 2): F(2)}
        check(yes == (b0.denominator == 1 and b1.denominator == 1),
              'translation grid failure')
        balanced += int(yes)

    # At even-denominator grid approximations to U2, verify the entire
    # phase-and-recentered-vertical-coordinate joint distribution exactly.
    # Half-open boundaries U2=0 and U2=1/2 are included.
    sampled_u = 0
    for n in range(2, 129, 2):
        observed = {}
        for j in range(n):
            u = F(j, n)
            lines = [F(k, 2) for k in range(-3, 4) if -u <= F(k, 2) < 1-u]
            check(len(lines) == 2, 'window line count')
            light = [y for y in lines if y.denominator == 1]
            heavy = [y for y in lines if y.denominator == 2]
            check(light == [F(0)] and len(heavy) == 1, 'window family count')
            for y, w in ((light[0], F(1)), (heavy[0], F(2))):
                phase, z = y % 1, u+y
                check(0 <= z < 1, 'recentered point outside C')
                key = (phase, z)
                observed[key] = observed.get(key, F(0)) + w/(3*n)
            sampled_u += 1
        expected = {(phase, F(j, n)): w/(3*n)
                    for phase, w in ((F(0), F(1)), (F(1, 2), F(2)))
                    for j in range(n)}
        check(observed == expected, 'joint product-law grid diagnostic failure')

    # Equal weights allow a swap in the formal two-family quotient model.
    equal_weight_survivors = []
    for a, b in product((F(0), F(1, 2)), repeat=2):
        received = {}
        for r in (a, b):
            received[r] = received.get(r, 0) + 1
        if received == {F(0): 1, F(1, 2): 1}:
            equal_weight_survivors.append([str(a), str(b)])
    check(len(equal_weight_survivors) == 2, 'equal-weight boundary diagnostic')

    return {
        'status': 'pass',
        'quotient_label_pairs_checked': 16,
        'quotient_survivors': quotient_survivors,
        'translation_pairs_checked': len(translations)**2,
        'balanced_translation_pairs': balanced,
        'exact_vertical_uniform_grid_inputs': sampled_u,
        'even_grid_denominators': 64,
        'joint_grid_law': '(delta_0/3 + 2 delta_(1/2)/3) tensor uniform_grid',
        'equal_weight_boundary_survivors': equal_weight_survivors,
        'analytic_event_discrepancy': '2/3',
        'limit': 'Finite diagnostics do not prove covariance, measurability, or the universal allocation reduction.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
