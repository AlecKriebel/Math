"""Independent irreducibility, support-profile, and certificate-total checks.

Run from any directory with Python 3.8 or newer. No third-party libraries.
This does not rerun the exhaustive C++ enumeration.
"""
import json
from pathlib import Path

P = 3
F = [2, 0, 1, 0, 0, 0, 0, 1]
HERE = Path(__file__).resolve().parent


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def remainder(a, b):
    a = a[:]
    while len(a) >= len(b):
        c = a[-1] * pow(b[-1], -1, P) % P
        offset = len(a) - len(b)
        for j, x in enumerate(b):
            a[offset + j] = (a[offset + j] - c * x) % P
        trim(a)
    return a


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return remainder(trim(out), F)


def power(a, n):
    out = [1]
    while n:
        if n % 2:
            out = multiply(out, a)
        a = multiply(a, a)
        n //= 2
    return out


def subtract(a, b):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0)
                  - (b[i] if i < len(b) else 0)) % P
    return trim(out)


def gcd(a, b):
    while b:
        a, b = b, remainder(a, b)
    return a


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


# Degree seven is prime, so these are precisely the Rabin conditions.
residue = power([0, 1], 3 ** 7)
g = gcd(F, subtract(power([0, 1], 3), [0, 1]))
require(residue == [0, 1], "Frobenius residue failed")
require(len(g) == 1, "Frobenius gcd failed")

profiles = json.loads((HERE / "PROFILES.json").read_text())
for s in range(1, 7):
    shifts = [{(a + j * s) % 7 for a in {0, 1, 3}} for j in range(8)]
    sums = [len(set.union(*shifts[:i + 1])) for i in range(8)]
    intersections = [len(set.intersection(*shifts[:i + 1])) for i in range(8)]
    require(profiles["monomial_013"][str(s)] == {
        "sums": sums, "intersections": intersections}, "Support profile failed")

finite = json.loads((HERE / "FINITE_TEST.json").read_text())
for code in finite["codes"]:
    hist = code["projective_rank_histogram"]
    require(sum(hist) == 2187 ** 2 + 2187 + 1, "Representative total failed")
    require(sum(hist[:5]) == 0 and hist[5] > 0, "Minimum rank failed")

print(json.dumps({
    "rabin_irreducibility": "passed",
    "x_to_3_power_7_residue": residue,
    "gcd_x_cubed_minus_x_degree": len(g) - 1,
    "independent_support_profiles_checked": 6,
    "projective_representatives_per_code": 2187 ** 2 + 2187 + 1,
    "certificate_minimum_rank": 5
}, indent=2))
