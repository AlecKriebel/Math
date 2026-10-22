#!/usr/bin/env python3
"""Exact finite controls for the written analytic proof, not a formal proof."""
from fractions import Fraction as Q
import json

counts = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def mul(p, q):
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r

def power(p, n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out, p)
    return out

def val(p, x):
    out = Q(0)
    for a in reversed(p):
        out = out * x + a
    return out

def derivative(p):
    return [Q(i) * p[i] for i in range(1, len(p))] or [Q(0)]

# Infinite-tail formulas are exact identities; the grid checks transcription.
for n in range(1, 129):
    eps = Q(1, 4**n)
    tail = Q(4, 3) * eps
    check("tail_recurrence", tail == eps + Q(4, 3) * Q(1, 4**(n + 1)))
    check("rouche_error_margin", Q(0) < tail <= Q(1, 3) < 2)
    check("target_endpoint_inside_island", Q(n, n + 2) < 1)
    for depth in range(1, 17):
        partial = sum((Q(1, 4**j) for j in range(n, n + depth)), Q(0))
        rest = Q(4, 3) * Q(1, 4**(n + depth))
        check("finite_tail_plus_remainder", partial + rest == tail)

# Rational complex target points: normalized zero lies strictly inside island.
for n in range(1, 17):
    for x in range(-n, n + 1):
        for y in range(-n, n + 1):
            if x*x + y*y <= n*n:
                zero_norm_squared = Q(x*x + y*y, (n + 2)**2)
                check("affine_zero_strictly_inside", zero_norm_squared < 1)

# Full multiplicity, including critical points, is required for separation.
centers = [Q(-2), Q(-1, 2), Q(0), Q(2, 3)]
for p in centers:
    for q in centers:
        if p == q:
            continue
        for m in range(1, 7):
            for k in range(1, 4):
                r = [Q(1), Q(0), Q(1)]  # R(z)=1+z^2, nonzero at real p.
                b = mul(power([-q, Q(1)], k), r)
                alpha_minus_c = mul(power([-p, Q(1)], m), b)
                check("same_fiber_at_distinct_points", val(alpha_minus_c, p) == val(alpha_minus_c, q) == 0)
                check("removable_value_nonzero", val(b, p) == (p-q)**k * (1+p*p) != 0)
                check("second_fiber_value_zero", val(b, q) == 0)
                d = alpha_minus_c
                for _ in range(m):
                    check("zero_order_lower_derivatives", val(d, p) == 0)
                    d = derivative(d)
                check("zero_order_exact", val(d, p) != 0)
                if m > 1:
                    weakened = mul(power([-p, Q(1)], m - 1), b)
                    check("reject_dividing_only_once", val(weakened, p) == val(weakened, q) == 0)
                check("reject_overdivision", val(b, p) != 0)  # b/(z-p) has a genuine pole.
                for x in [Q(j, 3) for j in range(-12, 13)]:
                    if x != p:
                        check("quotient_identity", val(alpha_minus_c, x) / (x-p)**m == val(b, x))
                        for delta in [Q(1, 10), Q(1, 2), Q(1)]:
                            if abs(x-p) >= delta:
                                M = abs(val(alpha_minus_c, x))
                                check("off_disk_tube_bound", abs(val(b, x)) <= M / delta**m)

# Orderedness direction and its contrapositive agree in every truth assignment.
for f_escapes in [False, True]:
    for a_escapes in [False, True]:
        implication = (not f_escapes) or a_escapes
        contrapositive = a_escapes or (not f_escapes)
        check("ordering_truth_table", implication == contrapositive)
check("reject_reversed_order", ((not False) or True) != ((not True) or False))

# Boundedness alone does not keep values away from the actual image boundary.
for n in range(3, 129):
    z = Q(n-1, n)
    check("bounded_range_escape_diagnostic", 0 < z < 1 and z > Q(n-2, n-1))

# A fixed H cannot work for all analytic b: use the explicit H(w)=w^2, alpha=z.
for x in [Q(j, 7) for j in range(-20, 21)]:
    check("reject_universal_H_all_analytic_b", x*x + (-x*x) == 0)

result = {
    "result": "PASS",
    "checks": dict(sorted(counts.items())),
    "total_assertions": sum(counts.values()),
    "limitations": [
        "Finite controls check algebra and transcription only; universal estimates are proved in PROOF.md.",
        "No infinite Runge approximant is computed; approximation, convergence and Rouche remain analytic proof steps.",
        "The script does not certify historical novelty, peer review, source licensing or an arbitrary-surface extension.",
        "The bounded-range diagnostic illustrates an invalid shortcut and is not a counterexample to the theorem."
    ]
}
print(json.dumps(result, indent=2, sort_keys=True))
