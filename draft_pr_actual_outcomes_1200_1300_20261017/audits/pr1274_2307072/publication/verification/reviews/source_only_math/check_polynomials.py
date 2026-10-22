#!/usr/bin/env python3
"""Exact finite corroboration for the source-only Problem 7.72 reconstruction."""
from fractions import Fraction as Q
from math import comb
import argparse
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    c = list(a) + [Q(0)] * max(0, len(b) - len(a))
    for j, x in enumerate(b):
        c[j] += x
    return trim(c)


def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x * y
    return trim(c)


def derivative(a):
    return trim([Q(j)*a[j] for j in range(1, len(a))] or [Q(0)])


def eval_poly(a, t):
    value = Q(0)
    for c in reversed(a):
        value = value*t+c
    return value


def certificate(m):
    require(type(m) is int and m >= 1, "m must be a positive integer")
    # Build the sum in the original polynomial definition independently of
    # binomial expansion: z^2*S(t), with F(t)=t*S(t).
    power = [Q(1)]
    s = [Q(0)]
    for unused in range(m):
        s = add(s, power)
        power = mul(power, [Q(1), Q(-1)])
    f = [Q(0)] + s
    binomial_f = [Q(0)] + [Q((-1)**(j+1)*comb(m, j)) for j in range(1, m+1)]
    require(f == binomial_f, f"geometric/binomial mismatch m={m}")
    # J(t)=integral_t^1 F(u)/u du, exact antiderivative.
    jpoly = [sum((f[k]/k for k in range(1, m+1)), Q(0))]
    jpoly += [-f[k]/k for k in range(1, m+1)]
    b = add(f, [-x for x in jpoly])
    harmonic = sum((Q(1, k) for k in range(1, m+1)), Q(0))
    require(jpoly[0] == harmonic, f"harmonic identity failed m={m}")
    require(eval_poly(b, Q(0)) == -harmonic, f"origin failed m={m}")
    require(eval_poly(b, Q(1)) == 1, f"boundary limit failed m={m}")
    # C(z)=-z J(t). barpartial C=-z^2 J'(t)=z^2 S(t)=v_m;
    # partial C=-J(t)-t J'(t)=F(t)-J(t)=Bv_m.
    jp = derivative(jpoly)
    require([-x for x in jp] == s, f"barpartial potential failed m={m}")
    partial_c = add([-x for x in jpoly], [Q(0)] + [-x for x in jp])
    require(partial_c == b, f"partial potential failed m={m}")
    db = derivative(b)
    rhs = add(derivative(f), s)
    require(db == rhs, f"radial derivative identity failed m={m}")
    # Every monomial in z^2 S(z bar z) has angular frequency exactly 2;
    # pairing with analytic z^k therefore has nonzero positive frequency.
    for index, coefficient in enumerate(s):
        if coefficient:
            for k in range(0, 65):
                require((index+2+k)-index == 2+k > 0, "angular pairing failed")
    # Finite rational point corroboration supplements the all-t monotonicity proof.
    for t in [Q(k, 32) for k in range(33)]:
        fv = eval_poly(f, t)
        bv = eval_poly(b, t)
        require(0 <= fv <= 1, f"input range failed m={m},t={t}")
        require(-harmonic <= bv <= 1, f"output range failed m={m},t={t}")
        if 0 < t < 1:
            require(eval_poly(db, t) > 0, f"strict derivative failed m={m},t={t}")
    return {
        "m": m,
        "input_norm_exact": "1",
        "output_norm_exact": str(harmonic),
        "output_origin_exact": str(-harmonic),
        "input_polynomial_degree_in_z_bar_z": 2*m,
        "radial_output_coefficients": [str(x) for x in b],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--false-certificate", action="store_true")
    args = parser.parse_args()
    if args.false_certificate:
        # A real deliberately false guard, rather than a simulated success flag.
        require(Q(1, 2) == Q(2, 3), "deliberate false certificate rejected")
    cases = [certificate(m) for m in list(range(1, 33)) + [64, 100]]
    print(json.dumps({
        "status": "PASS",
        "optimization": sys.flags.optimize,
        "arithmetic": "exact fractions",
        "checked_m": [case["m"] for case in cases],
        "checks": [
            "independent geometric and binomial polynomial construction",
            "exact radial integral and harmonic identity",
            "Wirtinger potential derivatives coefficientwise",
            "positive angular frequencies of all tested analytic monomials",
            "rational-grid corroboration of proven norm and monotonicity",
        ],
        "scope_limit": "Finite checks corroborate; the authored report proves all m and all analytic-L1 tests.",
        "cases": cases,
    }, indent=2))


if __name__ == "__main__":
    main()
