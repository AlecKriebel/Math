#!/usr/bin/env python3
"""Supplement the written local-resolution derivation; standard library only.
No source fetching, original-package imports, or write side effects.
"""
from fractions import Fraction
import json


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def times(z, w):
    return (z[0]*w[0] - z[1]*w[1],
            z[0]*w[1] + z[1]*w[0] - z[1]*w[1])


def reciprocal(z):
    norm = z[0]*z[0] - z[0]*z[1] + z[1]*z[1]
    return ((z[0] - z[1])/norm, -z[1]/norm)


def integer(n):
    return (Fraction(n), Fraction(0))


roots = [integer(1), (Fraction(0), Fraction(1)), (Fraction(-1), Fraction(-1))]
# Spatial coefficients a,b of a*x+b*y+c*t; blow up y=u,x=u*v.
tangents = [(integer(1), times(integer(-1), q)) for q in roots]
tangents += [(q, add(integer(4), times(integer(2), q))) for q in roots]
tangents += [(times(integer(-1), add(integer(1), times(integer(4), q))), integer(-2)) for q in roots]
strict_transform_points = [times(times(integer(-1), b), reciprocal(a)) for a,b in tangents]
check(len(set(strict_transform_points)) == 9, "Nine distinct strict-transform intersection points required")


def local_ordinary(r):
    check(r >= 2, "Formula only applies to singular ordinary points")
    delta = r*(r-1)//2
    if r == 2:
        # Identity is already a normal-crossings resolution.
        return dict(r=r, delta=delta, rough_M=0, negative_square=0, fine_M=0)
    E2 = -1
    # Adjunction: (aE+E).E=-2. Solve, rather than assume canonical sign.
    canonical_coefficient = Fraction(-2, E2) - 1
    check(canonical_coefficient == 1, "Canonical sign")
    Cprime_E = r
    nef_test = canonical_coefficient*E2 + Cprime_E + E2
    check(nef_test >= 0, "K+D is relatively nef, allowing N=0")
    rough = canonical_coefficient*nef_test
    check(rough == r-2, "Resolution formula")
    return dict(r=r, delta=delta, rough_M=int(rough), negative_square=0, fine_M=int(rough))


nine = local_ordinary(9)
triple = local_ordinary(3)
check(nine['delta'] == 12*triple['delta'] == 36, "delta constant")
check(nine['rough_M'] == 7 < 12*triple['rough_M'] == 12, "strict summed inequality")
check(triple['rough_M'] <= nine['rough_M'], "Marked-section convention is not contradicted")

rows = []
for n in range(2,101):
    central = local_ordinary(3*n)
    vertex = local_ordinary(n)
    near_delta = 3*vertex['delta'] + n*n*triple['delta']
    near_m = 3*vertex['rough_M'] + n*n*triple['rough_M']
    check(near_delta == central['delta'], "Fermat delta identity")
    check(near_m-central['rough_M'] == n*n-4, "Fermat excess identity")
    # Orevkov's alternative adds the local branch count minus one.
    shifted_central = central['rough_M'] + (3*n-1)
    shifted_near = 3*(vertex['rough_M']+n-1) + n*n*(triple['rough_M']+2)
    check(shifted_near-shifted_central == 3*n*n-6, "Alternative multibranch normalization")
    rows.append(dict(n=n, delta=central['delta'], central_rough_M=central['rough_M'],
                     nearby_rough_M=near_m, excess=near_m-central['rough_M'],
                     alternative_excess=shifted_near-shifted_central))
check(rows[0]['excess'] == 0, "n=2 must not be advertised as strict")
check(rows[1]['excess'] == 5, "n=3 starts the stated extension")

# Deliberate competing conventions must not reproduce the claimed invariant.
wrong_canonical = -1
wrong_K_M9 = wrong_canonical*(wrong_canonical*(-1)+9-1)
check(wrong_K_M9 == -9 and wrong_K_M9 != 7, "Reject K=-E")
wrong_unreduced_D_M9 = -1 + 9 - 9
check(wrong_unreduced_D_M9 == -1 and wrong_unreduced_D_M9 != 7, "Reject total-transform D")

result = dict(status='PASS', proof_role='supplementary arithmetic and tangent checks; universal derivations are in AUDIT.md',
              independent_of_original_checker=True, strict_transform_points=9,
              central=nine, nearby_singularities=12, nearby_type=triple,
              nearby_delta=12*triple['delta'], nearby_rough_M=12*triple['rough_M'],
              marked_section_failure=False, ordinary_negative_part_zero=True,
              finite_extension_range=[2,100], finite_extension_first_rows=rows[:3],
              canonical_sign_negative_control=True, unreduced_D_negative_control=True,
              limitations=['No finite range proves all n.', 'Does not certify source scope, flatness or boundary topology.'])
print(json.dumps(result, indent=2, sort_keys=True))
