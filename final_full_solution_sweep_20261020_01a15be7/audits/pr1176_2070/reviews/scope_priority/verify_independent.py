#!/usr/bin/env python3
"""Independent exact arithmetic checks; the all-future argument is in REPORT.md.

No candidate verifier or external algebra package is imported. All checks remain
active under Python optimization. Output is deterministic JSON.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def polynomial(x):
    return x**4 - x**3 - x**2 - x - 1


def derivative(x):
    return 4*x**3 - 3*x**2 - 2*x - 1


def multiply(a, b):
    """Q[X]/(X^4-X^3-X^2-X-1), coefficients in ascending order."""
    v = [F(0)] * 7
    for i in range(4):
        for j in range(4):
            v[i+j] += a[i] * b[j]
    for j in range(6, 3, -1):
        for t in range(4):
            v[j-4+t] += v[j]
    return v[:4]


one = [F(1), F(0), F(0), F(0)]
x = [F(0), F(1), F(0), F(0)]
den = [F(5), F(5), F(5), F(-3)]
basis = [[F(i == j) for i in range(4)] for j in range(4)]
columns = [multiply(den, v) for v in basis]
matrix = [[columns[j][i] for j in range(4)] + [one[i]] for i in range(4)]
for j in range(4):
    pivot = next(i for i in range(j, 4) if matrix[i][j])
    matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
    factor = matrix[j][j]
    matrix[j] = [v/factor for v in matrix[j]]
    for i in range(4):
        if i != j:
            factor = matrix[i][j]
            matrix[i] = [u-factor*v for u,v in zip(matrix[i], matrix[j])]
c = [matrix[i][-1] for i in range(4)]
require(multiply(den, c) == one, "field inverse")


def trace(v):
    return sum(multiply(v, basis[i])[i] for i in range(4))


k = [0, 0, 0, 0]
for m in range(272):
    k.append(sum(k[-4:]) + 1)
v = c
for m in range(276):
    require(trace(v) == k[m] + F(1, 3), "trace residue at " + str(m))
    v = multiply(v, x)

endpoints = {
    "positive_low": (F(48,25), F(-37009,390625)),
    "positive_high": (F(193,100), F(3092301,100000000)),
    "negative_low": (-F(77,100), F(-1483659,100000000)),
    "negative_high": (-F(39,50), F(101891,6250000)),
}
for label, (point, expected) in endpoints.items():
    require(polynomial(point) == expected, label)
require((1-F(193,100)+F(77,100))/2 == -F(2,25), "x lower bound")
require((1-F(48,25)+F(39,50))/2 == -F(7,100), "x upper bound")
require(1/(F(193,100)*F(39,50)) == F(5000,7527), "modulus lower")
require(1/(F(48,25)*F(77,100)) == F(2500,3696), "modulus upper")
require(F(2500,3696) < F(25,36), "modulus cutoff")
require(F(5000,7527)-F(4,625) > F(16,25), "imaginary lower")
require(F(39,50) < F(5,6), "negative root cutoff")
require(18*5**20 < 6**20, "uniform shift 20")
require(F(32,25)>1, "coefficient reciprocal bound")

# Modulo 2: no roots, and remainder upon division by X^2+X+1 is X+1.
f2 = [1,1,1,1,1]
require(f2[0] == 1 and sum(f2)%2 == 1, "no F2 linear factors")
for j in range(4,1,-1):
    if f2[j]:
        for t in range(3):
            f2[j-2+t] ^= 1
require(f2[:2] == [1,1], "no F2 quadratic factor")

left, right = F(48,25), F(193,100)
for unused in range(600):
    middle = (left+right)/2
    if polynomial(middle) < 0:
        left = middle
    else:
        right = middle
require(polynomial(left)<0<polynomial(right), "root isolating bracket")
require(derivative(left)>0, "positive derivative bracket")
# P''=12x^2-6x-2 is positive at 48/25 and increasing above it;
# hence (x-1)P'(x) increases throughout this interval.
require(12*F(48,25)**2-6*F(48,25)-2>0, "denominator monotonicity")


def floor_interval(m, multiplier=2):
    low = multiplier * left**m / ((right-1)*derivative(right))
    high = multiplier * right**m / ((left-1)*derivative(left))
    lo = low.numerator//low.denominator
    hi = high.numerator//high.denominator
    require(lo == hi, "unique floor at " + str(m))
    return lo


floors = []
for m in range(20,276):
    value = floor_interval(m)
    require(value == 2*k[m], "floor recurrence at " + str(m))
    floors.append(value)
require(floor_interval(3) == 1, "unshifted failure control")
require(floor_interval(24, 1) % 2 == 1, "missing factor 2 failure control")
require(floor_interval(20, 4) % 2 == 1, "doubled multiplier failure control")
# Exact all-future argument gives nonintegrality, so negating an eventual
# positive all-even-floor parameter gives odd floors, not another solution.
require((-floors[0]-1) % 2 == 1, "wrong-sign failure control")
expected_pairs = [[85488,164784], [164784,317632], [317632,612256],
                  [612256,1180162], [1180162,2274836], [2274836,4384888]]
pairs = [[floors[n],floors[n+1]] for n in range(6)]
require(pairs == expected_pairs, "displayed pairs")
proof = Path(__file__).parent / "inputs" / "PROOF.md"
require(len(proof.read_bytes()) == 9813, "input byte pin")
require(hashlib.sha256(proof.read_bytes()).hexdigest() ==
        "d1763e7b4b40f59f69c00f18e75f283a0692db29fb9835f1af66ab5197554207",
        "input SHA pin")
print(json.dumps({"status":"PASS", "checks": checks,
    "arithmetic":"Python standard-library Fraction and integers",
    "root_bisections":600, "trace_indices":[0,275],
    "isolated_floor_indices":[20,275], "first_six_pairs":pairs,
    "inverse_denominator_coefficients_ascending":[str(a) for a in c],
    "failure_controls":{"unshifted_m3_floor":1,
                        "missing_factor2_m24":"odd",
                        "doubled_multiplier_m20":"odd",
                        "negated_positive_multiplier_m20":"odd"},
    "logical_limit":"Finite checks supplement, not replace, the all-future proof."
},sort_keys=True,indent=2))
