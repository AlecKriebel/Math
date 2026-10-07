#!/usr/bin/env python3
"""Exact, finite diagnostic controls for the authored 5300048 note.

Only Python's standard library is required. These controls do not prove
analytic continuation, an infinite limiting claim, any cited theorem, or the
original accessibility question. Run with --check-result to compare against
the frozen result, or --check-manifest to verify the packet's file hashes.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        pivot = a[r][c]
        a[r] = [x / pivot for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def cmul(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def derivative_row(degree, x, y, part):
    # Real and imaginary coefficient pairs for F(z)=sum c_k z^k.
    row = [Q(0)] * (2 * (degree + 1))
    power = (Q(1), Q(0))
    for k in range(1, degree + 1):
        u, v = (k * power[0], k * power[1])
        row[2 * k:2 * k + 2] = [u, -v] if part == "real" else [v, u]
        power = cmul(power, (x, y))
    return row


def floor_mechanical(t, n):
    # floor(t+n*(sqrt(2)-1)) for rational t=a/b and integer n>=0.
    a, b = t.numerator, t.denominator
    return (a + isqrt(2 * n * n * b * b)) // b - n


def in_comb(x, y):
    return (0 < x < 1 and 0 < y < 1 and
            not (y <= Q(1, 2) and x.numerator == 1 and x.denominator >= 2))


def run_controls():
    counts = Counter()

    def check(name, value):
        if not value:
            raise AssertionError(name)
        counts[name] += 1

    for j in range(1, 101):
        u = Q(100 + j, 100)  # u = exp(R), treated algebraically.
        t = (u - 1) / (u + 1)
        check("hyperbolic_ball_coefficient_identity", 4 * t / (1 - t)**2 == u**2 - 1)

    for D in range(2, 13):
        for d in range(1, D + 1):
            for m in range(1, 7):
                deficit = D**m - d**m
                factor = (D-d) * sum(D**(m-1-j)*d**j for j in range(m))
                check("rational_degree_deficit", deficit == factor and deficit >= 0 and
                      ((deficit == 0) == (D == d)))

    for rho in (Q(1, 4), Q(1, 2), Q(3, 4), Q(9, 10)):
        delta = (1-rho)/2
        for k in range(1, 21):
            check("good_time_containment_constants", rho**k < 1-delta and 0 < delta < 1)

    for d in range(2, 11):
        previous = Q(0)
        for n in range(1, 21):
            s = 1-Q(1, 2**n)
            r = s**d
            exp_step = (1+s)*(1-r)/((1-s)*(1+r))
            check("monomial_inverse_pair_order", 0 < r < s < 1 and r == s**d)
            check("monomial_hyperbolic_step_bounds", 1 < exp_step <= d and exp_step > previous)
            previous = exp_step
        check("monomial_step_limit_control", abs(previous-d) < Q(1, 10**6))

    for t in (Q(0), Q(1, 7), Q(1, 2), Q(6, 7)):
        values = [floor_mechanical(t, n) for n in range(161)]
        digits = [values[n+1]-values[n] for n in range(160)]
        for digit in digits:
            check("mechanical_binary_digits", digit in (0, 1))
        for start in (0, 1, 7, 31):
            for N in range(1, 129):
                S = sum(digits[start:start+N])
                check("mechanical_telescoping", S == values[start+N]-values[start])
                # |S-N*(sqrt(2)-1)|<1, verified by squaring positive bounds.
                center = S+N
                check("mechanical_irrational_discrepancy", (center-1)**2 < 2*N*N < (center+1)**2)

    for n in range(2, 66):
        x = Q(1, n)
        between = (Q(1, n)+Q(1, n+1))/2
        check("comb_slit_barrier", not in_comb(x, Q(1, 4)))
        check("comb_upper_corridor", in_comb(x, Q(3, 4)))
        check("comb_between_slits", in_comb(between, Q(1, 4)))

    polynomial_ranks = []
    for d in range(1, 7):
        for part in ("real", "imag"):
            rows = [derivative_row(d, Q(1, n), Q(1, 8)+Q(j, 4*(d+1)), part)
                    for n in range(2, d+3) for j in range(1, d+1)]
            r = rank(rows)
            check("finite_polynomial_slit_rigidity", r == 2*d-1)
            # Two intercept parameters and the allowed real/imaginary slope.
            check("finite_polynomial_affine_nullity", 2*(d+1)-r == 3)
            polynomial_ranks.append({"degree": d, "derivative_part_zero": part,
                                     "rank": r, "nullity": 3})

    return {"problem_id": 5300048, "status": "pass", "arithmetic": "exact integer and rational",
            "total_assertions": sum(counts.values()), "assertions_by_group": dict(sorted(counts.items())),
            "polynomial_rank_controls": polynomial_ranks,
            "limits": ["Finite controls only; not a formal proof of any universal analytic statement.",
                       "Polynomial rank controls are not substitutes for the holomorphic identity principle.",
                       "Finite mechanical words do not establish aperiodicity; the irrational-frequency proof does.",
                       "No original accessibility claim or source theorem is certified by these computations."]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check-result", action="store_true")
    p.add_argument("--check-manifest", action="store_true")
    args = p.parse_args()
    base = Path(__file__).resolve().parent
    result = run_controls()
    if args.check_result:
        frozen = json.loads((base/"CONTROL_RESULTS.json").read_text())
        if result != frozen:
            raise AssertionError("control result differs from frozen result")
    if args.check_manifest:
        manifest = json.loads((base/"AUTHOR_MANIFEST.json").read_text())
        for entry in manifest["files"]:
            data = (base/entry["path"]).read_bytes()
            if len(data) != entry["bytes"] or sha256(data).hexdigest() != entry["sha256"]:
                raise AssertionError("manifest mismatch: " + entry["path"])
        print("All manifest entries match.")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
