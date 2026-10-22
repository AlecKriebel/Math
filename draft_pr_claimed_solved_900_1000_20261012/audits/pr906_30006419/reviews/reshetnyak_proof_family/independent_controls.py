#!/usr/bin/env python3
"""Independent audit controls; these do not formally verify Sobolev analysis.

Only standard Python is used. Exact controls use rational polynomial algebra;
the cutoff quadrature is explicitly illustrative floating-point evidence.
No original audit or author check code is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import math

EXPECTED_CONTROL_RESULTS_SHA256 = "e022ef5834ae41f135a308818af975d612c59af0fc4e836ee397a4e451b02783"


class ControlFailure(ValueError):
    """A control fails independently of Python's optimization mode."""


def require(condition, message):
    if not condition:
        raise ControlFailure(message)


def add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0)) +
            (q[i] if i < len(q) else F(0)) for i in range(n)]


def scale(p, c):
    return [c * x for x in p]


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def deriv(p):
    return [i * p[i] for i in range(1, len(p))]


def integ(p, a, b):
    return sum(c * (b ** (i + 1) - a ** (i + 1)) / (i + 1)
               for i, c in enumerate(p))


def B(x):
    return math.exp(-1 / x) if x > 0 else 0.0


def H(x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    # Stable equivalent of B(x)/(B(x)+B(1-x)).
    log_ratio = 1 / x - 1 / (1 - x)
    if log_ratio >= 0:
        e = math.exp(-log_ratio)
        return e / (1 + e)
    e = math.exp(log_ratio)
    return 1 / (1 + e)


def a(t):
    eta = 1 - H((16 * t * t - 1) / 3)
    return eta * t * t + 1 - eta


def simpson(f, lo, hi, panels):
    step = (hi - lo) / panels
    value = f(lo) + f(hi)
    value += sum((4 if k % 2 else 2) * f(lo + k * step)
                 for k in range(1, panels))
    return step * value / 3


def run():
    checks = []

    def record(name, evidence, negative_control=None):
        checks.append({"name": name, "passed": True, "evidence": evidence,
                       "negative_control": negative_control})

    # Exact scalar calibration cross term and square on [-1,1]^2.
    p = [F(1), F(0), F(-1)]
    dp = deriv(p)
    cross = integ(p, F(-1), F(1)) * integ(dp, F(-1), F(1))
    grad_squared = 2 * integ(mul(dp, dp), F(-1), F(1)) * integ(
        mul(p, p), F(-1), F(1))
    require(cross == 0 and grad_squared == F(256, 45), "Independent control C01 failed")
    require(F(4) + F(1, 100) * grad_squared > F(4), "Independent control C02 failed")
    record("same-trace scalar calibration exact polynomial control",
           {"integral_partial_x_w": str(cross),
            "integral_grad_w_squared": str(grad_squared),
            "energy_formula": "4 + epsilon^2 * 256/45"},
           "Dropping the fixed trace permits f=0 with energy 0; the lower bound 4 fails.")

    # Boundary-invariant exact form requires zero sphere integral.
    for r in [F(1, 10), F(1, 4), F(49, 100)]:
        b = r / (1 - r)
        require(b < 1 and (1 + b) * r - b == 0, "Independent control C03 failed")
        require(-b >= -1 and 1 + b - b == 1, "Independent control C04 failed")
    bad_b = F(3, 5) / (1 - F(3, 5))
    require(bad_b > 1, "Independent control C05 failed")
    record("exact cutoff comass and zero-period algebra",
           {"tested_area_fractions": ["1/10", "1/4", "49/100"],
            "signed_period": "0 exactly", "coefficient_range": "[-b,1]"},
           "For m/A=3/5, b=3/2 violates comass <=1. The full sphere area form has nonzero period and cannot use the exact-form gluing proof.")

    # Smooth cutoff sample evidence is not an analytic proof of smoothness.
    ts = [-1 + k / 10000 for k in range(20001)]
    vals = [a(t) for t in ts]
    require(all((0 <= v <= 1 for v in vals)), "Independent control C06 failed")
    require(a(0) == 0, "Independent control C07 failed")
    require(a(F(1, 4)) == F(1, 16), "Independent control C08 failed")
    require(a(F(1, 2)) == 1, "Independent control C09 failed")
    require(all((a(t) == a(-t) for t in ts)), "Independent control C10 failed")
    cs = [simpson(lambda t: 1 - a(t), 0.0, 0.5, n)
          for n in (2000, 4000, 8000)]
    require(all((float(F(47, 192)) < c < float(F(11, 24)) for c in cs)), "Independent control C11 failed")
    record("cutoff and positive energy surplus floating control",
           {"status": "illustrative quadrature; no certified error bound",
            "sample_count": len(ts), "c_estimates": cs,
            "analytic_c_bounds": "47/192 <= c < 11/24",
            "energy_surplus_estimate_4pi_c": 4 * math.pi * cs[-1]},
           "Setting a=1 removes c and the entire distortion counterexample; keeping only the rank defect at a single point would not prove essential unboundedness.")

    # Exact ratios on nonzero points and exact cover boundary checks.
    ratios = []
    for n in range(1, 10):
        t = F(1, 2 ** (n + 2))
        ratio = 1 / (t * t)
        require(ratio == 2 ** (2 * n + 4), "Independent control C12 failed")
        ratios.append({"t": str(t), "distortion": str(ratio)})
    for t in [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]:
        require(abs(t) < 1 or abs(t) > F(1, 2), "Independent control C13 failed")
    for Q in [1, 4, 16, 256, 65536]:
        delta = min(F(1, 4), F(1, 2 * math.isqrt(Q)))
        require(delta > 0 and 1 / (delta * delta) > Q, "Independent control C14 failed")
        require(4 * math.pi * math.tanh(float(delta)) > 0, "Independent control C15 failed")
    record("positive-measure distortion and seam boundary controls",
           {"exact_point_ratios": ratios,
            "round_band_area": "4*pi*tanh(delta)>0 for every delta>0",
            "cover": "|t|<1 or |t|>1/2, plus both poles"},
           "The equator alone is a zero-area set and cannot establish failure of almost-everywhere quasiconformality.")

    # Nonconvex chart coordinate: wrapping makes a local gradient bound insufficient.
    eps = 0.1
    angular_gap = 2 * math.pi - 2 * eps
    wrap_path_length = 2 * eps
    require(angular_gap > wrap_path_length, "Independent control C16 failed")
    record("ambient angular-coordinate Lipschitz negative control",
           {"coordinate_gap": angular_gap,
            "ambient_path_upper_bound": wrap_path_length},
           "An angular branch on (-pi,pi) with gradient norm 1 is not ambient 1-Lipschitz across its seam. The strong convex ball restriction is essential.")

    # Rational first variation for a same-trace first-coordinate bump in a positive-t rectangle.
    lo, hi = F(1, 16), F(1, 8)
    bump_t = mul([-(lo), F(1)], [hi, F(-1)])
    bump_t = mul(bump_t, bump_t)
    edge = F(1, 4)
    bump_x = [edge * edge, F(0), F(-1)]
    bump_x = mul(bump_x, bump_x)
    int_t_psi = integ(mul([F(0), F(1)], bump_t), lo, hi) * integ(
        bump_x, -edge, edge)
    first_variation = -4 * int_t_psi
    require(int_t_psi > 0 and first_variation < 0, "Independent control C17 failed")
    # Off-diagonal perturbations can increase the op norm: avoid a false plateau claim.
    top_left, off_diagonal = 0.2, 0.01
    trace = top_left ** 2 + off_diagonal ** 2 + 1
    det = top_left ** 2
    largest_eigenvalue = (trace + math.sqrt(trace * trace - 4 * det)) / 2
    require(largest_eigenvalue > 1, "Independent control C18 failed")
    record("Dirichlet negative variation and operator-norm distinction",
           {"integral_t_psi_exact": str(int_t_psi),
            "Dirichlet_first_variation_exact": str(first_variation),
            "matrix_control_largest_eigenvalue": largest_eigenvalue,
            "bump_regularization": "Polynomial bump and its first derivative vanish at the boundary; smooth approximation retains the strict negative variation."},
           "Energy comparability cannot equate minimizers. A theta-dependent first-coordinate variation need not retain operator norm exactly 1, but scalar calibration still forbids lowering E_+.")

    return {"purpose": "independent finite and adversarial analytic controls",
            "formal_analytic_proof": False,
            "imports_original_check_code": False,
            "all_passed": True, "check_count": len(checks), "checks": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("CONTROL_RESULTS.json"))
    args = parser.parse_args()
    try:
        result = run()
        encoded = (json.dumps(result, indent=2) + "\n").encode()
        require(hashlib.sha256(encoded).hexdigest() == EXPECTED_CONTROL_RESULTS_SHA256,
                "Control result differs from the fixed initial-review result pin")
        args.output.write_bytes(encoded)
        print(json.dumps({"all_passed": result["all_passed"],
                          "check_count": result["check_count"],
                          "result_sha256": EXPECTED_CONTROL_RESULTS_SHA256}))
    except (ControlFailure, OSError) as exc:
        parser.exit(1, f"Control failure: {exc}\n")
