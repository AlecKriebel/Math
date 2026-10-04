"""Original finite probability controls; analytic conclusions remain in the proofs.

This program uses exact rational arithmetic and no candidate modules. It does not
construct a SIRSN or verify an infinite/continuum theorem by enumeration.
"""
from fractions import Fraction as F
from itertools import product
import json

checks = 0


def check(statement):
    global checks
    assert statement
    checks += 1


laws = 0
for weights in product(range(3), repeat=4):
    if not sum(weights):
        continue
    weights = [F(w, sum(weights)) for w in weights]
    qs = [F(0), F(1, 2**40), F(1, 3), F(1)]
    multipliers = [F(1), F(7), F(2), F(3)]
    mass_mean = sum(w * q for w, q in zip(weights, qs))
    mass_square = sum(w * q * q for w, q in zip(weights, qs))
    support_probability = sum(w for w, q in zip(weights, qs) if q > 0)
    check(mass_mean <= support_probability)
    check(mass_mean**2 <= support_probability * mass_square)
    # V is strongly coupled to the environment. Direct conditional Bernoulli
    # integration verifies the invariant multiplier identity without independence.
    conditional_integral = sum(w * q * v for w, q, v in zip(weights, qs, multipliers))
    full_bernoulli_integral = sum(
        w * (q * v * 1 + (1 - q) * v * 0)
        for w, q, v in zip(weights, qs, multipliers)
    )
    check(conditional_integral == full_bernoulli_integral)
    previous = F(0)
    for n in [1, 2, 4, 9, 31]:
        hit = sum(w * (1 - (1 - q)**n) for w, q in zip(weights, qs))
        check(previous <= hit <= support_probability)
        check(hit <= n * mass_mean)
        if mass_mean + (n - 1) * mass_square:
            check(F(n) * mass_mean**2 / (mass_mean + (n - 1) * mass_square) <= hit)
        previous = hit
    laws += 1

# An endpoint set of vanishingly small but positive mass: finite-sample average
# control and the infinite-sample support event are different quantities.
small_mass_controls = 0
for exponent in range(1, 81):
    q = F(1, 2**exponent)
    check(q > 0)
    for n in [1, 3, 10, 100]:
        check(1 - (1 - q)**n <= n * q)
        small_mass_controls += 1

# Heavy random environments with exceedingly rare high sampled values.
heavy_environment_controls = 0
for cutoff in range(1, 41):
    check(sum(F(1, 2**j) * 2**j for j in range(1, cutoff + 1)) == cutoff)
    check(sum(F(1, 2**j) for j in range(1, cutoff + 1)) == 1 - F(1, 2**cutoff))
    for s in [1, 2, 5, 10]:
        for j in range(max(1, 2 * s), max(1, 2 * s) + cutoff):
            check(-j * j + (s - 1) * j <= F(-j * j, 2))
            heavy_environment_controls += 1

# Layer-cake visibility integral for finite distributions, computed directly on
# intervals, independently of the closed-form expectation formula.
visibility_controls = 0
lengths = [F(0), F(1, 2), F(2), F(7)]
weights = [F(1, 8), F(3, 8), F(1, 4), F(1, 4)]
for alpha in range(8):
    integral = F(0)
    for lo, hi in zip(lengths[:-1], lengths[1:]):
        tail = sum(w for w, length in zip(weights, lengths) if length > lo)
        integral += tail * ((1 + hi)**(alpha + 1) - (1 + lo)**(alpha + 1)) / (alpha + 1)
    closed = sum(w * ((1 + length)**(alpha + 1) - 1) / (alpha + 1) for w, length in zip(weights, lengths))
    check(integral == closed)
    visibility_controls += 1

print(json.dumps({
    "status": "PASS",
    "exact_assertions": checks,
    "directing_laws": laws,
    "small_mass_controls": small_mass_controls,
    "heavy_environment_controls": heavy_environment_controls,
    "visibility_integrals": visibility_controls,
    "scope": "Original exact finite probability controls; no SIRSN realization, continuum proof or novelty certification.",
}, indent=2, sort_keys=True))
