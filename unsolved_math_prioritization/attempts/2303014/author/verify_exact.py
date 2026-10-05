#!/usr/bin/env python3
"""Fresh exact rational algebra controls, not a proof of analytic theorems."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
checks = {}

def record(name, n):
    checks[name] = {"checks": n, "arithmetic": "exact rational", "status": "PASS"}

def norm(x, y):
    return x*x+y*y

# Dipole evaluation at ±r: each grid value checks the identity and its sign.
n = 0
for den in range(2, 102):
    for num in range(1, den):
        r = Q(num, den)
        a = (1-r*r)/(1-r)**2
        b = (1-r*r)/(1+r)**2
        assert a-b == 4*r/(1-r*r) > 0
        assert b-a == -4*r/(1-r*r) < 0
        n += 2
record("poisson_dipole_axis_identities_and_signs", n)

# Rational unit-circle parametrization of ξ with Re ξ>0; w in right half-disk.
n = 0
for j in range(-9, 10):
    t = Q(j, 10)
    a, b = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    assert a*a+b*b == 1 and a > 0
    for ix in range(1, 10):
        for iy in range(-9, 10):
            x, y = Q(ix, 10), Q(iy, 10)
            if x*x+y*y >= 1:
                continue
            dp = norm(a-x, b-y)
            dm = norm(-a-x, b-y)
            assert dm-dp == 4*x*a > 0
            k = (1-x*x-y*y)*(1/dp-1/dm)
            assert k > 0
            n += 2
record("paired_slit_poisson_kernel_positivity", n)

# q_a=c(r²-a²)/(1-a²): exact sample pass, missed-radius fail, boundary and Laplacian.
n = 0
for den in range(2, 42):
    for num in range(1, den):
        a = Q(num, den)
        c = Q(den+num, den)
        def f(r):
            return c*(r*r-a*a)/(1-a*a)
        for j in range(11):
            r = a*Q(j, 10)
            assert f(r) <= 0
            n += 1
        missed = (1+a)/2
        assert a < missed < 1 and 0 < f(missed) < c
        assert f(Q(1)) == c
        assert 4*c/(1-a*a) > 0
        n += 3
record("finite_radius_false_positive_controls", n)

# For b(e^s), its derivative is 2t/(π(1+t²)), t=e^(s/2).
# Its second derivative, after multiplying by π, is t(1-t²)/(1+t²)^2>0.
# These tests check the rational factor, not transcendental evaluations.
n = 0
for den in range(2, 82):
    for num in range(1, den):
        t = Q(num, den)
        assert t*(1-t*t)/(1+t*t)**2 > 0
        n += 1
record("radial_envelope_log_convexity_factor", n)

out = {
    "problem_id": 2303014,
    "packet_generation": "new reconstruction, 2026-10-05",
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "status": "PASS",
    "exact_checks": sum(v["checks"] for v in checks.values()),
    "groups": checks,
    "limits": [
        "These finite exact controls validate only the encoded algebra.",
        "They do not verify all radii or arbitrary L1 data numerically.",
        "They do not replace the analytic proofs, source interpretation, or independent audit.",
        "The historical reported count of 33257 was not reproduced and is not inherited."
    ]
}
(HERE / "CHECKS.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
