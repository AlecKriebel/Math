#!/usr/bin/env python3
"""Finite controls for the exact proof, Python 3.10+, standard library.

This is NOT a formal proof checker or an exhaustive univalence test.
The analytic strip lemma and the infinite nonnormality sequence are proved
in PROOF.md. Exact rational controls verify its constants and coefficients.
Floating-point diagnostics are secondary and not interval-certified.
"""
from fractions import Fraction as Q
from pathlib import Path
import cmath
import json
import math
import sys


def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def neg(z):
    return (-z[0], -z[1])


def mul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def main():
    b, c = Q(1, 100), Q(1, 10)
    a, real_b, one = (b, c), (b, Q(0)), (Q(1), Q(0))
    a_squared_norm = b*b+c*c
    assert a_squared_norm == Q(101, 10000)
    assert Q(1, 10)**2 < a_squared_norm < Q(11, 100)**2

    # Mathematical inputs: pi<4, and exp(s)<1/(1-s) for 0<s<1.
    # These are proved/explained in PROOF.md, not inferred from floats.
    phase_upper = Q(4, 20)
    exp_upper = 1/(1-phase_upper)
    u_upper = Q(1, 10)*exp_upper
    assert exp_upper == Q(5, 4) and u_upper == Q(1, 8)
    perturbation_upper = c*u_upper/(1-u_upper)
    q = Q(11, 100)+perturbation_upper
    assert perturbation_upper == Q(1, 70)
    assert q == Q(87, 700) and q < 1

    # Exact derivative-at-origin and normalization coefficients.
    f0 = add(a, neg(real_b))
    d = add(mul(a, add(one, a)), neg(mul(real_b, add(one, real_b))))
    assert f0 == (Q(0), c)
    assert d == (Q(-1, 100), Q(51, 500))
    assert d != (Q(0), Q(0))
    assert c*20 == 2      # c*(20*pi*n) is an integer multiple of 2*pi
    assert b*20 == Q(1, 5)  # exact exponent in exp(pi*n/5)

    exact = {
        "a_norm_squared": str(a_squared_norm),
        "exponential_upper": str(exp_upper),
        "u_upper": str(u_upper),
        "log_derivative_perturbation_upper": str(perturbation_upper),
        "strip_lemma_q": str(q),
        "margin_one_minus_q": str(1-q),
        "f_at_zero": [str(v) for v in f0],
        "f_prime_at_zero": [str(v) for v in d],
        "zero_sequence_phase_multiplier_of_pi_n": str(c*20),
        "divergence_exponent_multiplier_of_pi_n": str(b*20),
    }

    # Repeated phases of u have x period 20*pi. Sample two periods on
    # a deterministic grid inside Omega, including near-strip edges.
    yvals = [-math.pi/2 + 1e-8, math.pi/2 - 1e-8]
    yvals += [-math.pi/2 + math.pi*j/400 for j in range(1, 400)]
    maximum = 0.0
    maximum_u = 0.0
    ac = complex(float(b), float(c))
    sample_count = 0
    for y in yvals:
        xmin = -math.log(2*math.cos(y))
        for j in range(401):
            w = complex(xmin + 1e-6 + 40*math.pi*j/400, y)
            u = float(b)/ac*cmath.exp(-1j*float(c)*w)
            displacement = ac + 1j*float(c)*u/(1-u)
            maximum = max(maximum, abs(displacement))
            maximum_u = max(maximum_u, abs(u))
            sample_count += 1
    assert maximum < float(q)
    assert maximum_u < float(u_upper)

    # Never form z_n=1-t_n numerically: even n=1 rounds to 1 in binary64.
    # Evaluate the exact closed form from the proof in stable coordinates.
    values = []
    for n in (1, 2, 5, 10):
        t = math.exp(-20*math.pi*n)
        normality_quantity = 0.1*(2-t)*math.exp(math.pi*n/5)
        values.append({"n": n, "t_n": format(t, ".8e"),
                       "normality_quantity": format(normality_quantity, ".8e")})
    diagnostics = {
        "certification": "binary64 finite diagnostics only",
        "samples": sample_count,
        "max_sampled_abs_u": format(maximum_u, ".8e"),
        "max_sampled_abs_L_prime_minus_one": format(maximum, ".8e"),
        "radial_closed_form": values,
        "warning": "No direct evaluation of z_n; it rounds to the boundary in binary64.",
    }
    result = {"exact": exact, "diagnostics": diagnostics,
              "all_controls_pass": True,
              "limits": "No interval arithmetic, formal theorem prover, exhaustive search, or novelty test."}
    target = Path(__file__).with_name("CHECKS.json")
    if "--write" in sys.argv:
        target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    else:
        stored = json.loads(target.read_text(encoding="utf-8"))
        # Exact controls are portable; diagnostics are printed but need not
        # have identical last-place rounding across platform math libraries.
        assert result["exact"] == stored["exact"]
        assert stored["all_controls_pass"] is True
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
