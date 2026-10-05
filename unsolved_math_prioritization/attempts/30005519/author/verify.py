#!/usr/bin/env python3
"""Exact, finite controls for an analytic proof; no network or source inputs.

The universal theorem is proved in PROOF.md. These checks exercise algebra,
boundary cases and counterexamples to stronger statements. They do not search
all real subspaces. Explicit exceptions keep every check active under python -O.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import factorial, prod
import json
import sympy as sp


counts = Counter()


def check(test, category):
    counts[category] += 1
    if not bool(test):
        raise RuntimeError("Exact check failed: " + category)


def elementary(values):
    out = [1] + [0] * len(values)
    for i, x in enumerate(values):
        for j in range(i + 1, 0, -1):
            out[j] += x * out[j - 1]
    return out


def linear_product_coefficients(roots):
    # Ascending coefficients of product(t+x), independently of elementary().
    out = [1]
    for x in roots:
        nxt = [0] * (len(out) + 1)
        for i, a in enumerate(out):
            nxt[i] += x * a
            nxt[i + 1] += a
        out = nxt
    return out


def derivative(coefficients):
    return [i * coefficients[i] for i in range(1, len(coefficients))]


def sign_variations(coefficients):
    signs = [1 if c > 0 else -1 for c in coefficients if c]
    return sum(a != b for a, b in zip(signs, signs[1:]))


vector_count = 0
adjacent_zero_instances = 0
for n in range(1, 8):
    for x in product(range(-2, 3), repeat=n):
        vector_count += 1
        es = elementary(x)
        support = sum(t != 0 for t in x)
        for r in range(2, n + 2):
            a = es[r - 1]
            b = es[r] if r <= n else 0
            if a == b == 0:
                adjacent_zero_instances += 1
            check(a != 0 or b != 0 or support <= r - 2,
                  "consecutive_coefficient_implication")
        if n <= 4:
            for r in range(n + 1):
                brute = sum(prod(z) for z in combinations(x, r))
                check(es[r] == brute, "elementary_recurrence_vs_subsets")
        if n <= 5:
            polynomial = linear_product_coefficients(x)
            for r in range(2, n + 1):
                q = polynomial[:]
                for _ in range(n - r):
                    q = derivative(q)
                check(q[0] == factorial(n-r) * es[r],
                      "derivative_constant_coefficient")
                check(q[1] == factorial(n-r+1) * es[r-1],
                      "derivative_linear_coefficient")

# Finite exhaustive check of the exact sign-gap combinatorics used in the
# deposited paper. Descartes' theorem and all real inputs remain analytic facts.
gap_patterns = 0
for degree in range(1, 9):
    for first, last in product((-1, 1), repeat=2):
        for middle in product((-1, 0, 1), repeat=degree-1):
            coefficients = (first,) + middle + (last,)
            total = sign_variations(coefficients) + sign_variations(
                [(-1)**i*c for i, c in enumerate(coefficients)])
            check(total <= degree, "descartes_gap_upper_bound")
            if any(coefficients[i] == coefficients[i+1] == 0
                   for i in range(1, degree-1)):
                gap_patterns += 1
                check(total <= degree-1, "descartes_two_missing_strictness")

# Sharp coordinate-space lower bounds including the identically-zero r>n case.
for n in range(1, 11):
    for r in range(2, 13, 2):
        d = min(n, r-1)
        variables = sp.symbols("t0:" + str(d))
        forms = list(variables) + [0] * (n-d)
        es = elementary(forms)
        check(sp.expand(es[r] if r <= n else 0) == 0,
              "sharp_coordinate_spaces")
        check(d == len(variables), "sharp_space_dimension")

# Genuine odd-degree counterspaces, with an injective parameterization.
for r in (1, 3, 5, 7):
    variables = sp.symbols("t0:" + str(r))
    forms = [entry for t in variables for entry in (t, -t)]
    check(sp.expand(elementary(forms)[r]) == 0, "odd_degree_counterspace")
    check(sp.Matrix([[sp.diff(f, t) for t in variables] for f in forms]).rank() == r,
          "odd_degree_dimension")

# Non-coordinate extremal line in the quadratic case.
check(elementary((Fraction(1), Fraction(1), Fraction(-1, 2)))[2] == 0,
      "quadratic_noncoordinate_line")

# The false support heuristic, with a symbolic identity for each even r<=12.
for r in range(4, 13, 2):
    k = r//2
    variables = sp.symbols("t0:" + str(k))
    forms = [entry for t in variables[:-1] for entry in (t, -t)]
    t = variables[-1]
    forms += [t, t, -t/2]
    check(sp.expand(elementary(forms)[r]) == 0, "stronger_heuristic_counterspace")
    matrix = sp.Matrix([[sp.diff(f, t) for t in variables] for f in forms])
    check(matrix.rank() == k, "stronger_heuristic_dimension")
    check(all(f.subs(dict.fromkeys(variables, 1)) != 0 for f in forms),
          "stronger_heuristic_full_support")

# Complex-field counterexample, handled exactly modulo omega^2+omega+1.
s, t, omega = sp.symbols("s t omega")
complex_e2 = sp.expand(elementary([s, t, omega*t, omega**2*t])[2])
remainder = sp.rem(complex_e2, omega**2+omega+1, omega)
check(sp.expand(remainder) == 0, "complex_dimension_two_counterspace")
check(sp.Matrix([[1, 0], [0, 1], [0, omega], [0, omega**2]]).rank() == 2,
      "complex_space_dimension")
complex_adjacent = elementary([1, -1, sp.I, -sp.I])
check(sp.expand(complex_adjacent[1]) == sp.expand(complex_adjacent[2]) == 0,
      "complex_coefficient_lemma_negative_control")

# Homogeneous leading term, the affine-space reduction, checked symbolically
# for several degrees/dimensions. The proof handles every n,r.
tau = sp.symbols("tau")
for n, r in ((2, 2), (3, 2), (4, 4), (5, 4), (6, 6)):
    aa, ww = sp.symbols("a0:"+str(n)), sp.symbols("w0:"+str(n))
    p = sp.Poly(sp.expand(elementary([a+tau*w for a, w in zip(aa, ww)])[r]), tau)
    check(sp.expand(p.coeff_monomial(tau**r)-elementary(ww)[r]) == 0,
          "affine_leading_term_identity")

result = {
    "status": "PASS",
    "scope": "Exact finite/symbolic controls only; the universal theorem is proved in PROOF.md.",
    "sympy_version": sp.__version__,
    "enumerated_real_vectors": vector_count,
    "enumerated_vector_alphabet": [-2, -1, 0, 1, 2],
    "enumerated_dimensions": [1, 2, 3, 4, 5, 6, 7],
    "adjacent_zero_instances": adjacent_zero_instances,
    "two_missing_sign_patterns": gap_patterns,
    "check_counts": dict(sorted(counts.items())),
    "total_checks": sum(counts.values()),
    "universal_claim_from_finite_tests": False,
    "optimization_safe": "Checks use explicit RuntimeError, not assert statements.",
}
print(json.dumps(result, indent=2, sort_keys=True))
