#!/usr/bin/env python3
"""Finite checks for an audit of a previously published identity.

These checks are not an all-orders proof or a novelty certificate.
Run: python code/verify.py --order 10 --output evidence/verification.json
"""
import argparse
import json
import math
import platform
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.polys.fields import field


def product(x, y, size, zero):
    z = [zero for _ in range(size)]
    for i in range(min(len(x), size)):
        for j in range(min(len(y), size - i)):
            z[i + j] += x[i] * y[j]
    return z


def exact_checks(order):
    # L is an indeterminate representing log(1+a); no numeric samples here.
    F, a, L = field("a,L", sp.QQ)
    zero = F.zero

    def derivative(f):
        return f.diff(a) + f.diff(L) / (1 + a)

    k = [zero] * (order + 1)
    k[1] = -L
    # Independent coefficient recursion from K = -lambda log(1+a+K).
    for n in range(2, order + 1):
        power = [F.one] + [zero] * (n - 1)
        for r in range(1, n):
            power = product(power, k, n, zero)
            k[n] -= (-1) ** (r + 1) * power[n - 1] / (r * (1 + a) ** r)

    ell = [zero] * (order + 1)
    power = [F.one] + [zero] * order
    for r in range(1, order + 1):
        power = product(power, k, order + 1, zero)
        for n in range(1, order + 1):
            ell[n] += (-1) ** (r + 1) * power[n] / (r * a ** r)

    checks, coefficients = [], []
    for n in range(1, order + 1):
        first, second = (-L) ** n, (-L) ** n / a
        for _ in range(n - 1):
            first, second = derivative(first), derivative(second)
        first /= math.factorial(n)
        second /= math.factorial(n)
        assert first == k[n], ("K mismatch", n)
        assert second == ell[n], ("L mismatch", n)
        checks.append({"order": n, "K_recursion_equals_derivative": True,
                       "log_composition_equals_derivative": True})
        if n <= 4:
            coefficients.append({"order": n, "I_coefficient": str(k[n] - ell[n - 1])})

    # Check a=0 by jets of -log(1+a). The apparent quotient is removable.
    log_jet = [sp.Rational(0)] + [sp.Rational((-1) ** j, j) for j in range(1, order + 2)]
    power = [sp.Rational(1)] + [sp.Rational(0)] * (order + 1)
    for n in range(1, order + 1):
        power = product(power, log_jet, order + 2, sp.Rational(0))
        assert power[n - 1] / n == 0
        assert power[n] / n == sp.Rational((-1) ** n, n)
    return checks, coefficients


def model_coefficient_checks():
    """Integrate coefficients of the actual v2 equation (21), orders 1--4.

    The coefficients of the arctangent are written independently below.
    This tests the model identification to finite order, not just inversion.
    Floating-point quadrature is evidence, not a rigorous error enclosure.
    """
    mp.mp.dps = 50

    def c1(x):
        return -mp.log1p(x)

    def c2(x):
        h = mp.log1p(x)
        return h / (1 + x) + h / x

    def c3(x):
        h = mp.log1p(x)
        return (h*h/2 - h)/(1+x)**2 - h/(x*(1+x)) + h*h/(2*x*x)

    # The derivative side is generated afresh, rather than using c1,c2,c3.
    x = sp.Symbol("x", positive=True)
    f = -sp.log(1+x)
    expected = []
    for n in range(1, 5):
        c = sp.diff(f**n, x, n-1) / sp.factorial(n)
        if n >= 2:
            c -= sp.diff(f**(n-1)/x, x, n-2) / sp.factorial(n-1)
        expected.append(sp.lambdify(x, c, "mpmath"))

    rows = []
    for av in [mp.mpf("0.2"), mp.mpf("1"), mp.mpf("3")]:
        def integrand(p, n):
            s = 1 + av + p
            if n == 1:
                return -av / (s*(1+p))
            q = -mp.log(p) + c1(p)
            if n == 2:
                return -q/s**2
            if n == 3:
                return q*q/s**3 - c2(p)/s**2 - mp.pi**2/(3*s**3)
            return -c3(p)/s**2 + 2*q*c2(p)/s**3 - q**3/s**4 + mp.pi**2*q/s**4

        for n in range(1, 5):
            observed = mp.quad(lambda p: integrand(p, n), [0, 1, mp.inf])
            target = expected[n-1](av)
            error = abs(observed-target)
            assert error < mp.mpf("1e-35"), (str(av), n, str(error))
            rows.append({"a": str(av), "order": n,
                         "integral": mp.nstr(observed, 42),
                         "target": mp.nstr(target, 42),
                         "absolute_discrepancy": mp.nstr(error, 6)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.order < 4:
        parser.error("--order must be at least 4")
    checks, coefficients = exact_checks(args.order)
    numeric = model_coefficient_checks()
    result = {
        "status": "PASS",
        "scope": "Finite verification of a known identity; not an all-orders proof or novelty claim.",
        "environment": {"python": platform.python_version(), "sympy": sp.__version__,
                        "mpmath": mp.__version__},
        "exact_coefficient_checks": checks,
        "first_four_coefficients_L_equals_log1p_a": coefficients,
        "endpoint_a_zero": "K=0; L=-log(1+lambda); I=lambda*log(1+lambda)",
        "endpoint_jet_checks_through_order": args.order,
        "model_integral_coefficient_checks": numeric,
        "numeric_precision_digits": 50,
        "numeric_discrepancy_threshold": "1e-35; not a rigorous quadrature error bound"
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS: exact K/L coefficients through order {args.order}, endpoint jets, "
          f"and {len(numeric)} model-integral coefficient checks.")
    print("Finite checks only. All-orders and priority conclusions require the cited proof.")


if __name__ == "__main__":
    main()
