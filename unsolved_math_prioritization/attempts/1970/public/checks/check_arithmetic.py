#!/usr/bin/env python3
"""Reconstruction checks only; no historical hashes or global optimality claim.

Run without arguments to verify the supplied exact small-prefix values and the
rational arithmetic behind the recovered identities. This checker does not
certify those optimizer values: see the separate exact finite verifier.
All validation uses explicit exceptions, not Python assertions.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "fixtures" / "exact" / "tau_through_X192.json"
EXPECTED_X = [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81, 96, 108, 128, 144, 162, 192]
EXPECTED_TAU = [0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 7, 8]

def need(condition, message):
    if not condition:
        raise ValueError(message)

def floor_log(x, base):
    x = Q(x)
    need(x >= 1, "floor_log is only called on arguments at least one")
    exponent = 0
    while base ** (exponent + 1) <= x:
        exponent += 1
    return exponent

def integral_to(rows, limit):
    return sum((Q(left["tau"]) * (Q(1, left["X"]) - Q(1, min(right["X"], limit)))
                for left, right in zip(rows, rows[1:]) if left["X"] < limit), Q())

def corrected_colors(x):
    """Explicit candidate only. This function does not compute tau or q1."""
    x = Q(x)
    need(x >= 24, "candidate reconstruction used only for X >= 24")
    colors = [0, 0, 0]
    a = 0
    while 2 ** a <= x:
        b = 0
        while 2 ** a * 3 ** b <= x:
            colors[(a + 2 * b) % 3] += 1
            b += 1
        a += 1
    m = floor_log(x, 2)
    if 3 * 2 ** (m - 1) > x:
        colors[m % 3] -= 1
    e = 0
    while 24 * 2 ** e <= x:
        if x < 27 * 2 ** e:
            colors[(e + 2) % 3] -= 1
        e += 1
    return colors

def predicted_vector(x):
    h = floor_log(8 * x, 3)
    z = Q(8 * x, 3 ** h)
    v = [0, 0, 0]
    if z >= Q(4, 3):
        v[(2 * h) % 3] += 1
    if z >= 2:
        v[(2 * h + 1) % 3] += 1
    return h, v

def verify():
    raw = INPUT.read_bytes()
    rows = json.loads(raw)
    need([r["index"] for r in rows] == list(range(1, 26)), "indices changed")
    need([r["X"] for r in rows] == EXPECTED_X, "numeric smooth cutoffs changed")
    need([r["tau"] for r in rows] == EXPECTED_TAU, "tau reconstruction changed")
    t24, t192, j = integral_to(rows, 24), integral_to(rows, 192), Q(35, 162)
    need(t24 == Q(3, 8), "T24 mismatch")
    need(t192 == Q(2803, 5184), "T192 mismatch")
    need(Q(4, 24) + Q(8, 243) / (1 - Q(1, 3)) == j, "floor-log integral mismatch")
    correction = 8 * t192 - t24 + j
    need(correction == Q(25, 6), "constant combination mismatch")
    constant = 1 - correction / 21
    need(constant == Q(101, 126), "renormalized constant mismatch")

    breakpoints = [Q(9, 8), Q(3, 2), Q(9, 4), Q(27, 8), Q(9, 2), Q(27, 4), Q(81, 8), Q(27, 2), Q(81, 4)]
    boundaries = [Q(1)] + breakpoints + [Q(27)]
    vectors = [[1, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 1], [1, 0, 1]]
    checked = 0
    partition = []
    for left, right, expected in zip(boundaries, boundaries[1:], vectors):
        partition.append({"left": str(left), "right_exclusive": str(right), "v": expected})
        for t in (left, (left + right) / 2):
            for q in (1, 2):
                x = 27 ** q * t
                h, v = predicted_vector(x)
                need(v == expected, "nine-breakpoint vector mismatch")
                colors = corrected_colors(x)
                enlarged = corrected_colors(8 * x)
                need([new - old - h for old, new in zip(colors, enlarged)] == v,
                     "explicit candidate color increment mismatch")
                output = min(enlarged) - min(colors) - h
                need(output in (0, 1), "candidate output not binary at validation point")
                state = [c - min(colors) for c in colors]
                need(output == min(s + a for s, a in zip(state, v)), "candidate output/state mismatch")
                rotated_t = 8 * t if 8 * t < 27 else Q(8 * t, 27)
                need(1 <= rotated_t < 27, "multiplicative rotation normalization mismatch")
                checked += 1
    # Separately validate the correction discontinuities whose scale invariance
    # is proved for every X >= 24 in proofs/03_ARITHMETIC_RESULTS.md.
    for e in range(6):
        for x in (Q(24 * 2 ** e), Q(27 * 2 ** e)):
            h, v = predicted_vector(x)
            colors, enlarged = corrected_colors(x), corrected_colors(8 * x)
            need([b - a - h for a, b in zip(colors, enlarged)] == v, "correction endpoint mismatch")
            checked += 1
    return {
        "status": "PASS: exact rational arithmetic and explicit candidate cocycle reconstruction",
        "kind": "2026-10-15 reconstruction, not a recovered 2026-10-14 artifact",
        "tau_input": str(INPUT.relative_to(HERE.parent)),
        "tau_input_sha256": hashlib.sha256(raw).hexdigest(),
        "tau_input_certification": "See fixtures/exact/ certificates and independent verifier; not established by this arithmetic checker",
        "T24": str(t24), "T192": str(t192), "J": str(j),
        "constant_combination": str(correction), "alpha_constant": str(constant),
        "nine_breakpoints": [str(b) for b in breakpoints],
        "candidate_partition": partition,
        "algebra_validation_points": checked,
        "global_actual_binary_output": "UNPROVED",
        "candidate_equals_tau": "UNPROVED; no such identification is used",
        "unbounded_state_or_finite_state_claim": "No finite-state claim is made by this checker",
    }

if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
