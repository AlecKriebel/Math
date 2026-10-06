#!/usr/bin/env python3
"""Reproducible diagnostics for the explicit lens obstruction, not a theorem prover."""
import cmath
from fractions import Fraction
import json
import math
from pathlib import Path

A = complex(0.5, math.sqrt(3) / 2)
B = A.conjugate()
ROT = cmath.exp(-2j * math.pi / 3)

def W(z):
    return ROT * (z - A) / (z - B)

def F(z):
    return W(z) ** 1.5

def inverse_F(w):
    t = (w ** (2 / 3)) / ROT
    return (t * B - A) / (t - 1)

def density(z):
    s, d = abs(z - A), abs(z - B)
    return (3 * math.sqrt(3) / (2 * math.pi)) * math.sqrt(s) / (d ** 2.5 * (1 + (s / d) ** 3))

def run():
    assert abs(F(0.5) - 1j) < 1e-13
    assert abs(F(1) + 1) < 1e-13
    # Exact arithmetic verifies the only integration thresholds used in the proof.
    p, beta = Fraction(5, 4), Fraction(1, 2)
    assert beta - p == Fraction(-3, 4) > -1
    assert -p == Fraction(-5, 4) < -1
    count, max_inverse_error = 0, 0.0
    for ix in range(1, 100):
        for iy in range(-99, 100):
            z = complex(ix / 100, iy / 100)
            if abs(z) < 1 - 1e-8 and abs(z - 1) < 1 - 1e-8:
                w = F(z)
                assert w.imag > 0
                arg = cmath.phase(W(z))
                assert 0 < arg < 2 * math.pi / 3
                max_inverse_error = max(max_inverse_error, abs(inverse_F(w) - z))
                count += 1
    assert max_inverse_error < 1e-12
    limit = 3 ** 0.25 / (2 * math.pi)
    checks = []
    for k in range(2, 8):
        gap = 10 ** (-k)
        z = cmath.exp(1j * (math.pi / 3 - gap))
        s = abs(z - A)
        assert abs(z - 1) < 1
        ratio = density(z) / math.sqrt(s)
        # Independent modulus-of-complex-derivative expression.
        w_prime = ROT * (A - B) / ((z - B) ** 2)
        f_prime = 1.5 * (W(z) ** 0.5) * w_prime
        via_derivative = abs(f_prime) / (math.pi * (1 + abs(F(z)) ** 2))
        assert abs(density(z) - via_derivative) < 1e-12
        checks.append({'angle_gap': gap, 'density_divided_by_sqrt_distance': ratio, 'relative_error_to_limit': abs(ratio / limit - 1)})
    assert checks[-1]['relative_error_to_limit'] < 1e-6
    status = json.loads((Path(__file__).parent / 'STATUS.json').read_text())
    assert status['turns_used'] == 2 and status['turn_limit'] == 5
    assert status['full_solution'] is False and status['novelty_claim'] is False
    assert status['current_literature_status'] == 'unverified'
    return {
        'result': 'pass',
        'scope': 'Exact exponent checks, numerical conformal-map and density diagnostics, status consistency. The proof is in PROOF.md; these checks do not prove the localization converse.',
        'interior_points_checked': count,
        'max_inverse_map_error': max_inverse_error,
        'cut_integrability_exponent': str(beta - p),
        'original_integrability_exponent': str(-p),
        'density_limit': limit,
        'asymptotic_diagnostics': checks,
        'independent_mathematical_audit': 'not performed by this script',
    }

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
