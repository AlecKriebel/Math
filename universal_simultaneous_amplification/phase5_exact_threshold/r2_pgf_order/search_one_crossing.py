#!/usr/bin/env python3
"""Hostile screen for one-crossing and integrated PGF weakenings."""

from __future__ import annotations

import argparse
import importlib.util
from math import comb
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("pgf_search", HERE / "search_uniform_pgf.py")
SEARCH = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SEARCH)


def quotient_from_eta(eta):
    n = len(eta)
    delta = eta - np.array([comb(n - 1, k) / 2 ** (n - 1) for k in range(n)])
    quotient = np.zeros(n - 2)
    quotient[: min(2, n - 2)] = delta[: min(2, n - 2)]
    for k in range(2, n - 2):
        quotient[k] = delta[k] + quotient[k - 2]
    division_error = max(abs(delta[n - 2] + quotient[n - 4]),
                         abs(delta[n - 1] + quotient[n - 3]))
    return quotient, division_error


def positive_roots(coefficients):
    roots = np.roots(np.trim_zeros(coefficients[::-1], "f"))
    real = sorted(float(z.real) for z in roots if abs(z.imag) < 2e-6 and 1e-7 < z.real < 1 - 1e-7)
    return real, roots


def integrated_gap(coefficients):
    return 2 * sum(value / ((k + 1) * (k + 2)) for k, value in enumerate(coefficients))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=981723)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--sparsity", type=float, default=.25)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    most_roots = (-1, None)
    min_integral = (float("inf"), None)
    max_variations = (-1, None)
    max_derivative_variations = (-1, None)
    min_unweighted_derivative = (float("inf"), None)

    for trial in range(args.trials):
        raw = (SEARCH.random_directed(args.n, rng, args.sparsity) if args.directed
               else SEARCH.random_reversible(args.n, rng, args.sparsity))
        P = SEARCH.kernel_from_weights(raw)
        eta, residual = SEARCH.stationary_rank_law(P)
        quotient, error = quotient_from_eta(eta)
        if error > 2e-8:
            continue
        roots, all_roots = positive_roots(quotient)
        nonzero = [x for x in quotient if abs(x) > 2e-8]
        variations = sum(a * b < 0 for a, b in zip(nonzero, nonzero[1:]))
        integral = integrated_gap(quotient)
        # A(t)=E[t^(K-1)(N x-K)] is the negative logarithmic derivative
        # numerator of the complete-normalized PGF ratio.  Express it from
        # Q via D=(1-t^2)Q.
        polynomial = np.polynomial.Polynomial(quotient)
        N = args.n - 1
        derivative_coefficients = (
            np.polynomial.Polynomial([N, 2 - N]) * polynomial
            - np.polynomial.Polynomial([1, 0, -1]) * polynomial.deriv()
        ).coef
        derivative_nonzero = [x for x in derivative_coefficients if abs(x) > 2e-8]
        derivative_variations = sum(
            a * b < 0 for a, b in zip(derivative_nonzero, derivative_nonzero[1:])
        )
        unweighted_derivative = sum(
            value / (j + 1) for j, value in enumerate(derivative_coefficients)
        )
        payload = (trial, raw, eta, quotient, roots, all_roots, residual)
        if len(roots) > most_roots[0]:
            most_roots = (len(roots), payload)
            print("most roots", len(roots), "trial", trial, "roots", roots)
        if variations > max_variations[0]:
            max_variations = (variations, payload)
            print("most coefficient variations", variations, "trial", trial,
                  "q", quotient.tolist())
        if derivative_variations > max_derivative_variations[0]:
            max_derivative_variations = (derivative_variations, payload)
            print("most derivative variations", derivative_variations,
                  "trial", trial, "A", derivative_coefficients.tolist())
        if unweighted_derivative < min_unweighted_derivative[0]:
            min_unweighted_derivative = (unweighted_derivative, payload)
        if integral < min_integral[0]:
            min_integral = (integral, payload)
        if len(roots) >= 2 or integral < -1e-8:
            print("WITNESS trial", trial, "roots", roots, "integral", integral)
            print("raw=", repr(raw.tolist()))
            print("eta=", repr(eta.tolist()))
            print("q=", repr(quotient.tolist()))
            break

    print("maximum roots", most_roots[0])
    print("maximum coefficient variations", max_variations[0])
    print("maximum derivative variations", max_derivative_variations[0])
    print("minimum unweighted derivative integral", min_unweighted_derivative[0])
    print("minimum integrated gap", min_integral[0])
    if most_roots[1] is not None:
        print("root-witness raw=", repr(most_roots[1][1].tolist()))
        print("root-witness q=", repr(most_roots[1][3].tolist()))


if __name__ == "__main__":
    main()
