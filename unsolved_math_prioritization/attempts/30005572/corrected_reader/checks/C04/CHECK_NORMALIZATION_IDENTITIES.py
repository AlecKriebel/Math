#!/usr/bin/env python3
"""Exact finite-module sanity checks for the scalar-five normalization.

These checks do not prove the geometric theorem. The proof is in
SCALAR_FIVE_NORMALIZATION.md. No data or third-party sources are embedded.
"""
import json
from fractions import Fraction
from pathlib import Path

# Operators are represented here by their augmentation and constant eigenvalue.
B = (Fraction(5), Fraction(0))
A5 = (Fraction(1), Fraction(625))
P = tuple(125 * B[i] + A5[i] - 625 for i in range(2))
assert P == (Fraction(1), Fraction(0))
short_P = ((Fraction(1)-42+47)/6, (Fraction(625)-42*16+47)/6)
assert short_P == P

# These exhaust scalar defects satisfying the identities used in Sections 2-3.
# Over C=Z/nZ, 'a' is the fivefold defect; 'b' is the T5 defect.
# The test also runs modules with genuine 5-, 25-, and 125-torsion.
moduli = [1, 5, 7, 11, 13, 25, 35, 65, 125]
first_checks = second_checks = 0
records = []
for n in moduli:
    first_count = second_count = 0
    for a in range(n):
        for b in range(n):
            if (624*a-5*b) % n:
                continue
            correction = (b-125*a) % n
            assert (a+5*correction) % n == 0
            assert (b+624*correction) % n == 0
            first_checks += 1
            first_count += 1
            for d in [1, 16, 81, 256, 625, 2401]:
                for ba in range(n):
                    if (5*ba-(d-1)*a) % n or (624*ba-(d-1)*b) % n:
                        continue
                    assert (ba+(d-1)*correction) % n == 0
                    second_checks += 1
                    second_count += 1
    records.append({'modulus': n, 'first_stage_cases': first_count,
                    'second_stage_cases': second_count})

result = {
    'status': 'PASS',
    'scope': 'Exact operator and finite-constant-module checks; not a replacement for the proof',
    'P_augmentation': str(P[0]),
    'P_constant_eigenvalue': str(P[1]),
    'first_stage_cases': first_checks,
    'second_stage_cases': second_checks,
    'module_results': records,
}
print(json.dumps(result, indent=2))
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
