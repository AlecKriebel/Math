#!/usr/bin/env python3
"""Finite certificate: smallest-root field maps need not compose coherently.

The 25-element enumeration is a bounded verification, not an efficient
canonicalization algorithm or a new research theorem.
"""
import json
from finite_fields import FiniteField


def evaluate(field, coefficients, value):
    result = field.zero
    for coefficient in reversed(coefficients):
        result = field.add(field.mul(result, value), field.element(coefficient))
    return result


def encoding(element):
    return element[0] + 5 * element[1]


def roots(field, polynomial):
    return sorted((value for value in field.elements_for_testing()
                   if evaluate(field, polynomial, value) == field.zero),
                  key=encoding)


def certificate():
    A = FiniteField(5, (1, 1, 1))
    B = FiniteField(5, (2, 1, 1))
    roots_ab = roots(B, A.h)
    roots_ba = roots(A, B.h)
    roots_aa = roots(A, A.h)
    assert roots_ab == [(3, 2), (1, 3)]
    assert roots_ba == [(3, 2), (1, 3)]
    assert roots_aa == [(0, 1), (4, 4)]
    composite = evaluate(A, roots_ab[0], roots_ba[0])
    assert composite == (4, 4)
    assert composite != roots_aa[0]
    assert composite == A.pow(A.element((0, 1)), 5)
    return {
        "characteristic": 5,
        "A_modulus": A.h,
        "B_modulus": B.h,
        "ordering": "c0 + 5*c1",
        "roots_A_in_B": roots_ab,
        "roots_B_in_A": roots_ba,
        "roots_A_in_A": roots_aa,
        "composite_image_of_A_generator": composite,
        "direct_image_of_A_generator": roots_aa[0],
        "coherence_claim_falsified": True,
        "scope": "exact bounded counterexample; no novel canonicity claim",
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
