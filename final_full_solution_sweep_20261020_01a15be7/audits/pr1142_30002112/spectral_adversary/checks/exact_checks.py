#!/usr/bin/env python3
"""New, independent finite diagnostics; no candidate executable is imported.

All correctness checks survive Python -O and -OO. These diagnostics do not
construct any cavity or certify its spectrum. See REPORT.md for the proof.
"""
from fractions import Fraction
from math import comb
import hashlib
import json
from pathlib import Path
import sys


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def choose(n, r):
    return comb(n, r) if n >= r >= 0 else 0


def multiplicity(m, degree):
    return choose(degree + m, m) - choose(degree + m - 2, m)


def monomials(variables, degree):
    """Actually enumerate exponent tuples, avoiding a binomial-formula oracle."""
    if variables == 1:
        yield (degree,)
    else:
        for first in range(degree + 1):
            for tail in monomials(variables - 1, degree - first):
                yield (first,) + tail


def threshold(m, q):
    return q * (q + m - 1)


def rank(m, q):
    return choose(q + m - 1, m) + choose(q + m - 2, m) + 2


def explicit_spectrum(m, q, inner_gap):
    spectrum = [0, inner_gap]
    for degree in range(q + 2):
        spectrum.extend([threshold(m, degree)] * multiplicity(m, degree))
    return sorted(spectrum)


counts = {"monomial_dimension_cases": 0, "counting_identity_cases": 0,
          "explicit_multiset_cases": 0, "large_index_bound_cases": 0,
          "exact_escape_certificates": 0, "circle_union_cases": 0}

for m in range(2, 7):
    for degree in range(9):
        dim = sum(1 for _ in monomials(m + 1, degree))
        prior = sum(1 for _ in monomials(m + 1, degree - 2)) if degree >= 2 else 0
        require(dim - prior == multiplicity(m, degree), "monomial count")
        counts["monomial_dimension_cases"] += 1

for m in range(2, 33):
    for q in range(1, 97):
        N = sum(multiplicity(m, degree) for degree in range(q))
        require(N + 2 == rank(m, q), "telescoping count")
        require(multiplicity(m, q) > 0, "positive block multiplicity")
        require(threshold(m, q) > threshold(m, q - 1), "strict levels")
        counts["counting_identity_cases"] += 1
        if q >= m:
            k = rank(m, q)
            require(k <= 2 * (q + m) ** m + 2, "first index bound")
            require(2 * (q + m) ** m + 2 <= 2 ** (m + 2) * q ** m,
                    "second index bound")
            # Equivalent to k^(2/m) <= 16 q^2, with no floating powers.
            require(k ** 2 <= 16 ** m * q ** (2 * m), "rational index bound")
            counts["large_index_bound_cases"] += 1

for m in range(2, 6):
    for q in range(1, 17):
        T = threshold(m, q)
        k = rank(m, q)
        spectrum = explicit_spectrum(m, q, T + 1)
        require(spectrum[0] == spectrum[1] == 0, "two zero modes")
        require(spectrum[k - 2] < T == spectrum[k - 1], "exact first rank")
        d = multiplicity(m, q)
        require(spectrum[k + d - 2] == T, "last repeated mode")
        require(spectrum[k + d - 1] > T, "end of repeated block")
        counts["explicit_multiset_cases"] += 1

negative_controls = {}
m, q = 3, 4
T, k = threshold(m, q), rank(m, q)
spectrum = explicit_spectrum(m, q, T + 1)
negative_controls["omit_extra_zero_or_shift_rank_down"] = spectrum[k - 2] != T
negative_controls["gap_below_threshold_breaks_identity"] = (
    explicit_spectrum(m, q, T - 1)[k - 1] != T)
negative_controls["gap_equal_threshold_extends_repeated_block"] = (
    explicit_spectrum(m, q, T)[k + multiplicity(m, q) - 1] == T)
negative_controls["ignore_sphere_multiplicities_breaks_rank"] = k != q + 2
negative_controls["rank_plus_one_equality_is_insufficient"] = (
    spectrum[k] == T and spectrum[k - 2] < T)
for label, detected in negative_controls.items():
    require(detected, "negative control failed: " + label)

escape_samples = []
for m in range(2, 17):
    n = m + 1
    # Unit ball contains [-1/n,1/n]^n and is contained in [-1,1]^n.
    lower_v = Fraction(2, n) ** n * (1 - Fraction(1, 2 ** n))
    D = max(Fraction(1), lower_v ** -2)
    upper_rho = n * 2 ** n
    for M in [1, 2, 10, 1000, 10 ** 12]:
        ceil_four_DM = (4 * D * M).__ceil__()
        q = (32 * M) ** m + ceil_four_DM + m + upper_rho
        require(q >= m and q >= upper_rho, "escape minimum q")
        require(Fraction(2) * D / q <= Fraction(1, 2 * M), "isoperimetric term")
        require(q ** 2 >= (32 * M) ** m, "index term root-free certificate")
        require(rank(m, q) ** 2 <= 16 ** m * q ** (2 * m), "large exact index")
        counts["exact_escape_certificates"] += 1
        if M == 1000 and m in [2, 3, 8, 16]:
            escape_samples.append({"m": m, "M": M, "q": str(q),
                                   "k": str(rank(m, q)), "D": str(D)})

for components in range(1, 13):
    for seed in range(1, 9):
        lengths = [Fraction(seed + j * j + 1, seed + j + 1)
                   for j in range(1, components + 1)]
        L = sum(lengths)
        for k in range(1, 33):
            xs = [Fraction(k) * ell / L for ell in lengths]
            counted = sum(1 + 2 * (x.numerator // x.denominator) for x in xs)
            require(sum(xs) == k, "circle scale normalization")
            require(counted >= k, "circle union bound")
            counts["circle_union_cases"] += 1

payload = {
    "status": "PASS",
    "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python_optimization": sys.flags.optimize,
    "checks": counts,
    "negative_controls": negative_controls,
    "escape_samples": escape_samples,
    "limitations": ["Finite arithmetic diagnostics only; not a formal proof.",
                    "Does not establish geometric existence or any numerical cavity spectrum."]}
print(json.dumps(payload, indent=2, sort_keys=True))
