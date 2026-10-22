#!/usr/bin/env python3
"""Exact finite checks ancillary to the all-parameter PDE proof in REPORT.md.

No assertions, third-party modules, source downloads, or floating-point tests.
Variables are formal z and w=bar(z); area integrals are divided by pi.
"""
from fractions import Fraction as Q
from math import comb
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def tidy(p):
    return {k: v for k, v in p.items() if v}


def add(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, Q(0)) + v
    return tidy(out)


def scale(p, c):
    return tidy({k: c * v for k, v in p.items()})


def multiply(p, q):
    out = {}
    for (a, b), c in p.items():
        for (d, e), f in q.items():
            k = (a + d, b + e)
            out[k] = out.get(k, Q(0)) + c * f
    return tidy(out)


def derivative(p, variable):
    out = {}
    for (a, b), c in p.items():
        powers = [a, b]
        n = powers[variable]
        if n:
            powers[variable] -= 1
            k = tuple(powers)
            out[k] = out.get(k, Q(0)) + n * c
    return tidy(out)


def moment(p):
    return sum((c / (a + 1) for (a, b), c in p.items() if a == b), Q(0))


def radial_value(p, t):
    require(all(a == b for a, b in p), "requested value of nonradial polynomial")
    return sum((c * t**a for (a, _), c in p.items()), Q(0))


def construction(m):
    if not isinstance(m, int) or isinstance(m, bool) or m < 1:
        raise ValueError("m must be a positive integer")
    # Construct u directly from the zero-trace primitive, not from a transform.
    u = {}
    for k in range(1, m + 1):
        for j in range(k + 1):
            key = (j + 1, j)
            u[key] = u.get(key, Q(0)) - Q((-1)**j * comb(k, j), k)
    # Construct the alleged input independently from its finite geometric sum.
    v = {}
    for k in range(m):
        for j in range(k + 1):
            key = (j + 2, j)
            v[key] = v.get(key, Q(0)) + (-1)**j * comb(k, j)
    return tidy(u), tidy(v), derivative(tidy(u), 0)


def logarithmic_u_moment(p, q):
    # Integral_D z log(|z|^2) z^p bar(z)^q / pi.
    return -Q(1, (q + 1)**2) if q == p + 1 else Q(0)


def angular_v_moment(p, q):
    # Integral_D (z/bar(z)) z^p bar(z)^q / pi.
    return Q(1, q) if q == p + 2 else Q(0)


def logarithmic_g_moment(p, q):
    # Integral_D (1+log(|z|^2)) z^p bar(z)^q / pi.
    return Q(p, (p + 1)**2) if p == q else Q(0)


def main():
    counts = {"polynomial_parameters": 0, "polynomial_stokes_identities": 0,
              "polynomial_analytic_moments": 0, "polynomial_l2_identities": 0,
              "positive_area_thresholds": 0, "logarithmic_stokes_identities": 0,
              "negative_controls": 0}
    parameters = list(range(1, 33))
    endpoint_data = []
    for m in parameters:
        u, v, g = construction(m)
        h = sum((Q(1, k) for k in range(1, m + 1)), Q(0))
        require(derivative(u, 1) == v, f"barpartial u != v at m={m}")
        require(derivative(g, 1) == derivative(v, 0), f"interior compatibility m={m}")
        # Trace u=0 is equivalent to sum of its radial coefficients being zero.
        require(sum(u.values(), Q(0)) == 0, f"nonzero outer trace m={m}")
        require(radial_value(g, Q(0)) == -h, f"wrong negative endpoint m={m}")
        require(radial_value(g, Q(1)) == 1, f"wrong positive endpoint m={m}")
        for p in range(9):
            for q in range(9):
                test = {(p, q): Q(1)}
                for variable, d in ((0, g), (1, v)):
                    lhs = moment(multiply(d, test))
                    rhs = -moment(multiply(u, derivative(test, variable)))
                    require(lhs == rhs, f"weak Stokes failure m,p,q,var={m,p,q,variable}")
                    counts["polynomial_stokes_identities"] += 1
        for n in range(129):
            require(moment(multiply(v, {(n, 0): Q(1)})) == 0,
                    f"analytic moment failure m,n={m,n}")
            counts["polynomial_analytic_moments"] += 1
        # Conjugating a polynomial with real coefficients swaps the exponents.
        v_conjugate = {(b, a): c for (a, b), c in v.items()}
        nv2 = moment(multiply(v, v_conjugate))
        ng2 = moment(multiply(g, g))
        expected = 1 - Q(2, m + 1) + Q(1, 2 * m + 1)
        require(nv2 == ng2 == expected, f"full-plane L2 isometry m={m}")
        counts["polynomial_l2_identities"] += 1
        eta = Q(1, 16)
        delta = min(eta / (4 * m), Q(1, 2))
        require(radial_value(g, delta) < -h + eta,
                f"positive-area lower bound m={m}")
        counts["positive_area_thresholds"] += 1
        counts["polynomial_parameters"] += 1
        if m in (1, 2, 4, 8, 16, 32):
            endpoint_data.append({"m": m, "H_m": str(h), "area_over_pi": str(delta)})
    for p in range(129):
        for q in range(129):
            rhs_bar = -q * logarithmic_u_moment(p, q - 1) if q else Q(0)
            rhs_partial = -p * logarithmic_u_moment(p - 1, q) if p else Q(0)
            require(angular_v_moment(p, q) == rhs_bar,
                    f"logarithmic barpartial weak identity p,q={p,q}")
            require(logarithmic_g_moment(p, q) == rhs_partial,
                    f"logarithmic partial weak identity p,q={p,q}")
            counts["logarithmic_stokes_identities"] += 2
    for k in range(8):
        m = 2**k
        h = sum((Q(1, j) for j in range(1, m + 1)), Q(0))
        require(h >= 1 + Q(k, 2), f"harmonic block divergence k={k}")
    for bad in (0, -1, True, Q(1, 2)):
        try:
            construction(bad)
        except ValueError:
            counts["negative_controls"] += 1
        else:
            raise RuntimeError("invalid parameter was not rejected")
    for defect in (Q(1), Q(-1)):
        u, v, _ = construction(3)
        wrong_v = add(v, {(0, 0): defect})
        require(moment(wrong_v) != -moment(multiply(u, derivative({(0, 0): Q(1)}, 1))),
                "deliberate input constant perturbation was undetected by weak test")
        counts["negative_controls"] += 1
    print(json.dumps({"status": "PASS", "optimization": sys.flags.optimize,
                      "method": "formal Wirtinger derivatives and exact weak test moments",
                      "counts": counts, "endpoint_examples": endpoint_data,
                      "single_input_l2_norm_squared_over_pi": "1",
                      "warning": "Finite checks supplement, and do not replace, REPORT.md's all-parameter proof."},
                     indent=2))


if __name__ == "__main__":
    main()
