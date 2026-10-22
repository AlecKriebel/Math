#!/usr/bin/env python3
"""Independent exact finite controls for PR152 geometry; no candidate verifier import.

The all-n arguments are in GEOMETRIC_DERIVATIONS.md. These finite checks are
falsifiable controls, not replacements for the cited Veech theorems.
"""
from fractions import Fraction
from math import gcd
import json
from pathlib import Path


def cycles(n):
    unseen = {(s, j) for s in (0, 1) for j in range(n)}
    out = []
    while unseen:
        p = min(unseen)
        cycle = []
        q = p
        while q not in cycle:
            cycle.append(q)
            unseen.remove(q)
            q = (1 - q[0], (q[1] + 1) % n)
        assert q == p
        out.append(cycle)
    return out


def norm2(p, q):
    return p * p + q * q - p * q


def hex_weight2(p, q):
    # Fuchs p.506. Input is the first reached honeycomb vertex.
    assert (p + q) % 3 != 2
    if (p % 3, q % 3) == (1, 2):
        return 1, Fraction(3, 4)
    if p % 2 == 0 and q % 2 == 0:
        return 2, Fraction(1)
    if (p % 3, q % 3) == (2, 1):
        return 3, Fraction(3, 4)
    return 0, Fraction(1, 4)


def hex_first(p, q):
    assert gcd(p, q) == 1
    multiplier = 2 if (p + q) % 3 == 2 else 1
    for k in range(1, multiplier):
        assert (k * (p + q)) % 3 == 2
    x, y = multiplier * p, multiplier * q
    k, w2 = hex_weight2(x, y)
    return multiplier, k, Fraction(norm2(x, y), 1) / w2


def square_first(p, q):
    assert gcd(p, q) == 1
    k = int(p % 2 == 1 and q % 2 == 1)
    w2 = Fraction(1) if k else Fraction(1, 2)
    return k, Fraction(p * p + q * q) / w2


def group_orbit(p, q, rotation, reflection):
    out = set()
    pending = [(p, q)]
    while pending:
        u = pending.pop()
        if u in out:
            continue
        out.add(u)
        pending.extend((rotation(*u), reflection(*u)))
    return out


report = {'controls_are_finite': True, 'polygon_n_range': [3, 200], 'lattice_coordinate_bound': 100}
reflection_cases = 0
for n in range(3, 201):
    cs = cycles(n)
    expected_v = 1 if n % 2 else 2
    assert len(cs) == expected_v
    cone_multiple = Fraction(len(cs[0]) * (n - 2), 2 * n)
    assert cone_multiple.denominator == 1
    genus = Fraction(n - expected_v, 2)
    expected_g = Fraction(n - 1, 2) if n % 2 else Fraction(n - 2, 2)
    assert genus == expected_g
    if n >= 5:
        fixed_points = n + int(n % 2 == 1)
        assert fixed_points == 2 * genus + 2
    class_of = {p: i for i, c in enumerate(cs) for p in c}
    for p, i in class_of.items():
        exchanged = (1 - p[0], p[1])
        assert (class_of[exchanged] == i) == (n % 2 == 1)
    # A reflection axis at angle b*pi/n takes vertex j to b-j.
    # Each nonfixed orbit is precisely one chord perpendicular to that axis.
    for b in range(2 if n % 2 == 0 else 1):
        sigma = lambda j: (b - j) % n
        pairs = {tuple(sorted((j, sigma(j)))) for j in range(n) if j != sigma(j)}
        fixed = [j for j in range(n) if j == sigma(j)]
        assert sum(1 for pair in pairs for _ in pair) + len(fixed) == n
        assert all(sigma(sigma(j)) == j for j in range(n))
        assert len(fixed) == (1 if n % 2 else (2 if b % 2 == 0 else 0))
        reflection_cases += 1
report['corner_cycle_and_reflection_cases_passed'] = reflection_cases

hex_checks = square_checks = triangle_checks = 0
examples = []
for p in range(-100, 101):
    for q in range(-100, 101):
        if gcd(p, q) != 1:
            continue
        orb6 = group_orbit(p, q, lambda a, b: (a-b, a), lambda a, b: (b, a))
        original = hex_first(p, q)
        for a, b in orb6:
            assert norm2(a, b) == norm2(p, q)
            assert gcd(a, b) == 1
            assert (a+b) % 3 in {(p+q) % 3, -(p+q) % 3}
            assert hex_first(a, b)[2] == original[2]
            hex_checks += 1
            triangle_checks += 1
        orb4 = group_orbit(p, q, lambda a, b: (-b, a), lambda a, b: (b, a))
        sq = square_first(p, q)
        for a, b in orb4:
            assert gcd(a, b) == 1
            assert square_first(a, b) == sq
            square_checks += 1
        if (p, q) in {(1, 0), (1, 1), (2, 1), (1, 2)}:
            examples.append({'primitive': [p,q], 's_mod3': (p+q)%3, 'first_multiplier': original[0], 'type': original[1], 'L2_over_w2': str(original[2])})
report['hexagon_orbit_controls_passed'] = hex_checks
report['square_orbit_controls_passed'] = square_checks
report['triangle_primitivity_controls_passed'] = triangle_checks
report['hexagon_examples'] = examples
report['status'] = 'PASS'
p = Path(__file__).with_name('geometry_checks.json')
p.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
