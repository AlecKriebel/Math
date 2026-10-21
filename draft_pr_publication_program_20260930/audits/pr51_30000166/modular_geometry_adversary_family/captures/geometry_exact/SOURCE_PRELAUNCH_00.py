#!/usr/bin/env python3
"""Fresh standard-library diagnostics; imports no submitted checker or receipts.

The proof is in ANALYTIC_PROOF.md. Counts below describe finite diagnostics only.
The theta cutoff follows a completed-square bound rather than an observed box.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
import json

counts = Counter()

def require(condition, family):
    if not condition:
        raise AssertionError(family)
    counts[family] += 1

def primes(n):
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out

def phi(n):
    result = n
    for p in primes(n):
        result = result // p * (p - 1)
    return result

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def mobius(n):
    for p in primes(n):
        if n % (p * p) == 0:
            return 0
    return (-1) ** len(primes(n))

def quadratic(n):
    a = len(n)
    # Uses the integer triangular expression valid when sum(n)=0.
    return sum(a * x * (x - 1) // 2 + i * x for i, x in enumerate(n))

def rotate_translate(n, j):
    value = list(n[1:] + n[:1])
    if j:
        value[j - 1] += 1
        value[-1] -= 1
    return tuple(value)

def inverse_rotate_translate(n, j):
    value = list(n)
    if j:
        value[j - 1] -= 1
        value[-1] += 1
    return tuple(value[-1:] + value[:-1])

def product_series(powers, degree):
    # Each individual factor is a binomial series, then convolved. This is
    # independent of the submitted in-place positive/negative recurrence.
    result = [1] + [0] * degree
    for step, power in sorted(powers.items()):
        if power == 0 or step > degree:
            continue
        factor = [1] + [0] * degree
        coefficient = 1
        for k in range(1, degree // step + 1):
            coefficient = coefficient * (k - 1 - power) // k
            factor[k * step] = coefficient
        result = [sum(result[i-j] * factor[j] for j in range(i+1))
                  for i in range(degree+1)]
    return result

def theta_series(a, M, r, degree):
    coefficients = [0] * (degree + 1)
    bounds = []
    for j in range(a):
        linear = [M * i + (r * a if i == j else 0) for i in range(a)]
        squared_projection = sum(Fraction(x*x) for x in linear) - Fraction(sum(linear)**2, a)
        # e >= M*a*||n||^2/4 - ||projection(linear)||^2/(M*a).
        norm_bound = Fraction(4*degree, M*a) + 4*squared_projection/Fraction((M*a)**2)
        coordinate_bound = isqrt(norm_bound.numerator // norm_bound.denominator)
        bounds.append(coordinate_bound)
        for leading in product(range(-coordinate_bound, coordinate_bound+1), repeat=a-1):
            n = tuple(leading) + (-sum(leading),)
            if abs(n[-1]) > coordinate_bound:
                continue
            e = M * quadratic(n) + r * (a*n[j]+j)
            require(e >= 0, "theta_enumerated_exponents_nonnegative")
            require(Fraction(e) >= Fraction(M*a, 4)*sum(x*x for x in n) - squared_projection/Fraction(M*a),
                    "completed_square_bound")
            if e <= degree:
                coefficients[e] += 1
    return coefficients, bounds

# Charged beta-set energy gives precisely Q, including negative runners.
for a in range(2, 7):
    for leading in product(range(-2, 3), repeat=a-1):
        n = tuple(leading) + (-sum(leading),)
        direct = 0
        for i, charge in enumerate(n):
            if charge >= 0:
                direct += sum(i+a*k for k in range(charge))
            else:
                direct -= sum(i+a*k for k in range(charge, 0))
        require(direct == quadratic(n), "charged_beta_set_energy")
        require(quadratic(n) >= 0, "core_energy_nonnegative")
        require((quadratic(n) == 0) == all(x == 0 for x in n), "unique_zero_core")
        for j in range(a):
            t = rotate_translate(n, j)
            require(sum(t) == 0 and inverse_rotate_translate(t, j) == n, "lattice_bijection")
            require(quadratic(t)-quadratic(n) == a*n[j]+j, "theta_functional_transform")
            for M,r in ((3,1),(5,4),(11,3)):
                exponent = M*quadratic(n)+r*(a*n[j]+j)
                require(exponent == (M-r)*quadratic(n)+r*quadratic(t) and exponent >= 0,
                        "convex_specialization_energy")

theta_cases = []
for a,M,r,H in ((2,3,1,48),(2,5,4,48),(3,5,1,48),(3,5,4,48),(5,9,4,36),(5,9,8,36)):
    actual,bounds = theta_series(a,M,r,H)
    powers = Counter()
    for k in range(1,H+1):
        powers[k] += int(k % M == 0) + (a-2)*int(k % (a*M) == 0)
        powers[k] += int(k % (a*M) in (a*r,a*(M-r)))
        powers[k] -= int(k % M in (r,M-r))
    expected = product_series(powers,H)
    require(actual == expected, "theta_product_exact_coefficients")
    require(actual[0] == 1, "interior_specialization_constant")
    theta_cases.append({"a":a,"M":M,"r":r,"degree":H,"complete_coordinate_bounds_by_j":bounds})

normalizations = []
for N in range(1,301):
    exponents = {d: -mobius(d) for d in divisors(N)}
    exponents[N] += phi(N)
    leading = Fraction(sum(d*e for d,e in exponents.items()),24)
    require(leading >= 0, "eta_infinity_leading_exponent")
    require(Fraction(sum(exponents.values()),2) == (0 if N == 1 else Fraction(phi(N),2)),
            "eta_weight")
    require(sum((N//d)*e for d,e in exponents.items()) == 0, "eta_second_congruence")
    if N > 1:
        t = Fraction(phi(N),N)
        for c in divisors(N):
            direct = sum(Fraction(gcd(c,d)**2 * e, d) for d,e in exponents.items())
            rad = 1
            for p in primes(c):
                rad *= p
            closed = t*(c*c - (-1)**len(primes(c))*rad)
            require(direct == closed, "cusp_exponent_mobius_factorization")
            require(direct >= 0 and (direct == 0) == (c == 1), "cusp_exponent_sign_diagnostic")
    if N in (1,2,3,4,5,6,10,12,15,30,35,49,105):
        normalizations.append({"N":N,"leading_exponent":str(leading),
                               "integer_T_multiplier":leading.denominator == 1})

# Negative controls reject extending the specialization range or strict positivity.
for M in (1,3,10):
    n = (1,-1)
    require(M*quadratic(n)+(M+1)*(2*n[1]+1) == -1, "outside_range_negative_control")
    require(-1*(2*0+1) == -1, "negative_r_negative_control")
two_core = product_series({k: 2*int(k%2==0)-1 for k in range(1,13)},12)
require(two_core[2] == 0 and two_core[0] == 1, "strict_positivity_negative_control")
require(Fraction(2*phi(2)-sum(d*mobius(d) for d in divisors(2)),24) == Fraction(1,8),
        "fractional_primetwo_boundary")
require(Fraction(6*phi(6)-sum(d*mobius(d) for d in divisors(6)),24) == Fraction(5,12),
        "fractional_two_distinct_primes_boundary")

print(json.dumps({"schema":"pr51-independent-modular-geometry-diagnostics/v1",
                  "status":"PASS","assertions":sum(counts.values()),
                  "assertions_by_family":dict(sorted(counts.items())),
                  "theta_cases":theta_cases,"eta_normalizations":normalizations,
                  "limitations":["Finite exact diagnostics do not prove the universal theorem.",
                                  "Cusp expression checks are algebraic diagnostics; no blanket Dirichlet-character modularity is inferred.",
                                  "The universal reasoning, its classical foundations and source credit are set out separately."]},
                 sort_keys=True,indent=2))
