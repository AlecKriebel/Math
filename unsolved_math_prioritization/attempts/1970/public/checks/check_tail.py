#!/usr/bin/env python3
"""Bounded reconstruction checks; the unbounded-remainder proof is analytical."""
from fractions import Fraction as Q
import json

def need(condition, message):
    if not condition:
        raise ValueError(message)

def floor_log(x, p):
    need(x >= 1, "argument below one")
    exponent = 0
    while p ** (exponent + 1) <= x:
        exponent += 1
    return exponent

def reciprocal_tail_by_complement(x):
    total = Q(3)
    a = 0
    while 2 ** a <= x:
        b = 0
        while 2 ** a * 3 ** b <= x:
            total -= Q(1, 2 ** a * 3 ** b)
            b += 1
        a += 1
    return total

def reciprocal_tail_closed_form(x):
    m = floor_log(x, 2)
    main = Q()
    for a in range(m + 1):
        b = floor_log(x / 2 ** a, 3) + 1
        need(x < 2 ** a * 3 ** b <= 3 * x, "strict-cutoff exponent mismatch")
        main += Q(1, 2 ** a * 3 ** b)
    return Q(3, 2) * main + Q(3, 2 ** (m + 1))

def verify():
    cutoffs = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81, 96, 108, 128, 144, 162, 192]
    points = sorted({Q(x) + offset for x in cutoffs for offset in (Q(-1, 2), Q(), Q(1, 2)) if Q(x) + offset >= 1})
    for x in points:
        a = reciprocal_tail_by_complement(x)
        b = reciprocal_tail_closed_form(x)
        need(a == b, "exact tail identity mismatch")
        m = floor_log(x, 2)
        need(0 < a < Q(3 * (m + 3), 2) / x, "weaker tail bound mismatch")
    return {
        "status": "PASS",
        "kind": "2026-10-15 reconstruction; no original artifact identity claim",
        "checked_exact_cutoffs_and_neighbors": len(points),
        "source": "https://arxiv.org/pdf/2604.15515v1",
        "source_pdf_sha256": "68e3b58de8d2bf8f4e5fb48560f2c43e489d7979e7e0f8c44ed2ddf1c7adbb14",
        "analytic_claim": "The proposed O(1/X) remainder for S={2,3} is false; see authored Abel/Bessel proof",
        "preserved_claims": ["exact reciprocal-tail identity", "O(log X/X) bound", "density series", "exact nested bounds"],
        "finite_checks_do_not_prove_unboundedness": True,
    }

if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
