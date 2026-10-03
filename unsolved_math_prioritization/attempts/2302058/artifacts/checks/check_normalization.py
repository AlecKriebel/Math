#!/usr/bin/env python3
"""Finite transcription/algebra controls, not an analytic-existence certificate."""
from fractions import Fraction as Q
from math import asin, cos, exp, hypot, log, pi, sin, sqrt
from pathlib import Path
import json

checks = []
def require(condition, label):
    assert condition, label
    checks.append(label)

# |q+1|^2 - |q|^2 = 2 Re q + 1, exactly over Q(i).
for m in range(-20, 21):
    for n in range(-10, 11):
        x, y = Q(m, 7), Q(n, 11)
        require((x + 1)**2 + y*y - (x*x + y*y) == 2*x + 1,
                f"circle numerator {m},{n}")
for n in range(-100, 101):
    x, y = Q(-1, 2), Q(n, 13)
    norm = x*x + y*y
    # Real and imaginary parts of 1 + 1/q.
    fr, fi = 1 + x/norm, -y/norm
    require(fr*fr + fi*fi == 1, f"unit circle {n}")

def a(x):
    return pi/6 if x <= 0 else asin(exp(-x)/2)
def ap(x):
    return 0.0 if x < 0 else -exp(-x)/sqrt(4 - exp(-2*x))
def psi(x, y):
    return x, y + a(x)*sin(y)

require(abs(a(0)-pi/6) < 1e-15, "continuous at zero")
require(1-pi/6 > 0, "positive global Jacobian lower bound")
for x in [0, .01, .1, .5, 1, 2, 4, 8, 12]:
    require(abs(ap(x)) <= 1/sqrt(3) + 1e-15, f"a derivative {x}")
    for k in range(-8, 9):
        b = pi/2 + k*pi
        xp, yp = psi(x, b)
        # Relative-scale control avoids treating huge cancellation as exact.
        require(abs(cos(yp) + exp(-x)/2) < 8e-15,
                f"logarithmic vertical line {x},{k}")
        require(abs(yp - b - (-1)**k*a(x)) < 8e-15,
                f"parity of ray deformation {x},{k}")
for x in [-100, -2, 0, .1, 1, 10]:
    for j in range(-100, 101):
        y = j*pi/50
        det = 1 + a(x)*cos(y)
        require(det >= 1-pi/6-1e-15, f"Jacobian sample {x},{j}")

# Finite-order comparison witness with P(z)=z, plus a nonzero-alpha scaling.
for t in [1, .1, .01, .001]:
    u, v = log(2*sin(t/2)), pi/2+t/2
    fr, fi = 1+exp(u)*cos(v), exp(u)*sin(v)
    require(abs(fr-cos(t)) < 2e-15 and abs(fi-sin(t)) < 2e-15,
            f"finite order natural curve {t}")
    ar, ai = 2.0, -3.0
    gr, gi = ar*fr-ai*fi, ar*fi+ai*fr
    require(abs(hypot(gr,gi)-hypot(ar,ai)) < 2e-14,
            f"nonzero alpha scaling {t}")

result = {
    "status": "PASS",
    "checks_passed": len(checks),
    "scope": "Exact rational circle identities and finite floating-point transcription controls",
    "not_proved_by_script": ["published surface existence", "quasiconformal uniformization", "absence of every asymptotic path", "infinite order"],
    "analytic_proof": "PROOF_VERIFICATION.md"
}
output = Path(__file__).with_name("check_results.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
