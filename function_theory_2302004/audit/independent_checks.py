#!/usr/bin/env python3
"""Independent finite diagnostics for the erf Julia-ray audit.

These are not a proof of infinitely many preimages or normality. The
analytic review is in AUDIT.md. Requires Python 3 and mpmath 1.3.0.
"""
import json
from fractions import Fraction

import mpmath as mp

mp.mp.dps = 70
checks = []
root_samples = []


def check(name, condition, kind):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "kind": kind, "passed": True})


# Evaluate the real-path integral directly, independently of erfc's
# implementation, at nonradial points in both halves of Re(z)>0.
for x, y in [(1, 2), (2, -3), (3, 1), (4, 5), (2, 0), (5, -1)]:
    z = mp.mpc(x, y)
    integral = mp.quad(lambda t: mp.exp(-t*t-2*z*t), [0, 1, mp.inf])
    delta = -2*mp.quad(lambda t: t*mp.exp(-t*t-2*z*t), [0, 1, mp.inf])
    erfc_from_integral = 2/mp.sqrt(mp.pi)*mp.exp(-z*z)*integral
    check(f"integral_identity_{x}_{y}",
          abs(erfc_from_integral-mp.erfc(z)) < mp.mpf("1e-60") *
          max(1, abs(mp.erfc(z))), "non-rigorous numerical diagnostic")
    check(f"integration_by_parts_{x}_{y}",
          abs(2*z*integral-1-delta) < mp.mpf("1e-60"),
          "non-rigorous numerical diagnostic")
    check(f"direct_integral_bound_{x}_{y}",
          abs(delta) < mp.mpf(1)/(2*x*x),
          "non-rigorous numerical diagnostic")

# Exact disk-to-tail inequalities, independently recomputed.
for d in [Fraction(1, 1000), Fraction(1, 23), Fraction(1, 3), Fraction(49, 100)]:
    check(f"disk_radial_margin_{d}", 1-d > Fraction(1, 2), "exact rational")
    check(f"disk_argument_majorant_{d}", d/(1-d) < 2*d, "exact rational")

# Inspect the spherical derivative that underlies the normality contradiction.
omega = mp.exp(mp.j*mp.pi/4)
for radius in (3, 7, 15, 31):
    z = radius*omega
    value = mp.erf(z)
    derivative = mp.diff(mp.erf, z)
    normalized_spherical = abs(derivative)/(1+abs(value)**2)
    error_bound = (1+mp.mpf(radius)**-2)/(mp.sqrt(mp.pi)*radius)
    lower = (2/mp.sqrt(mp.pi))/(1+(1+error_bound)**2)
    check(f"radial_limit_bound_{radius}", abs(value-1) <= error_bound,
          "non-rigorous numerical diagnostic")
    check(f"spherical_derivative_lower_bound_{radius}",
          normalized_spherical >= lower,
          "non-rigorous numerical diagnostic")
    check(f"negative_conjugation_{radius}",
          abs(mp.erf(-mp.conj(z))+mp.conj(value)) < mp.mpf("1e-60"),
          "non-rigorous numerical diagnostic")

# Find finite sample preimages with independently derived asymptotic seeds.
# Neither successful roots nor decreasing angles prove the infinite claim.
for label, target in [("zero", mp.mpc(0)), ("two", mp.mpc(2)), ("i", mp.j)]:
    offsets = []
    moduli = []
    for index in (4, 16, 64):
        logarithm = mp.log((1-target)*mp.sqrt(mp.pi))-2*mp.pi*mp.j*index
        seed = mp.sqrt(-logarithm-mp.log(-logarithm)/2)
        root = mp.findroot(lambda z: mp.erf(z)-target,
                           (seed, seed+mp.mpc(".001", ".001")),
                           tol=mp.mpf("1e-60"), maxsteps=100)
        residual = abs(mp.erf(root)-target)
        offset = abs(mp.arg(root)-mp.pi/4)
        check(f"sample_preimage_{label}_{index}",
              residual < mp.mpf("1e-60") and mp.re(root) > 0 and mp.im(root) > 0,
              "non-rigorous numerical diagnostic")
        root_samples.append({"target": label, "seed_index": index,
                             "root_real": mp.nstr(mp.re(root), 16),
                             "root_imaginary": mp.nstr(mp.im(root), 16),
                             "angle_offset": mp.nstr(offset, 12),
                             "residual_below": "1e-60"})
        offsets.append(offset)
        moduli.append(abs(root))
    check(f"sample_angles_decrease_{label}",
          all(a > b for a, b in zip(offsets, offsets[1:])),
          "non-rigorous numerical diagnostic")
    check(f"sample_moduli_increase_{label}",
          all(a < b for a, b in zip(moduli, moduli[1:])),
          "non-rigorous numerical diagnostic")

# Complex target pairs: the real-only author samples do not test this case.
for index, (a, b) in enumerate([(mp.mpc(2, 3), mp.mpc(-5, 7)),
                               (mp.j, -mp.j), (mp.mpc(0), mp.mpc(0, 5))]):
    center, scale = (a+b)/2, (a-b)/2
    check(f"complex_affine_pair_{index}",
          scale != 0 and center+scale == a and center-scale == b,
          "exact representable complex algebra")

# Negative controls make the most plausible substitutions explicit.
check("oddness_alone_goes_to_five_pi_over_four",
      abs(mp.arg(-omega)+3*mp.pi/4) < mp.mpf("1e-60"),
      "non-rigorous numerical diagnostic")
check("negative_conjugation_goes_to_three_pi_over_four",
      abs(mp.arg(-mp.conj(omega))-3*mp.pi/4) < mp.mpf("1e-60"),
      "non-rigorous numerical diagnostic")
check("equal_targets_destroy_bijectivity", (mp.j-mp.j)/2 == 0,
      "exact representable complex algebra")
check("finite_asymptotic_limit_does_not_force_derivative_growth",
      all(r*mp.exp(-r) < mp.mpf(".001") for r in (10, 20, 40)),
      "non-rigorous numerical diagnostic")

print(json.dumps({
    "problem_id": "2302004",
    "status": "PASS",
    "mpmath_version": mp.__version__,
    "decimal_precision": mp.mp.dps,
    "checks_passed": len(checks),
    "scope": "Finite diagnostics only; the analytic proof is audited separately.",
    "checks": checks,
    "preimage_samples": root_samples,
}, indent=2, sort_keys=True))
