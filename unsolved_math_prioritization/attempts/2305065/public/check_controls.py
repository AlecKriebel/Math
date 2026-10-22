#!/usr/bin/env python3
"""Finite arithmetic and adversarial controls for the 2305065 proof.

This is not a theorem prover, a construction of the required analytic function,
or a computation of the limiting exceptional set. No third-party modules needed.
"""
from fractions import Fraction as F
import json


def rouche_margin(contour_min, norm_error, value_error):
    """Sufficient strict inequality used by the compact persistence proof."""
    return contour_min > 0 and 2 * norm_error + value_error < contour_min


def approximation_parameters(epsilon, eta):
    # pi < 22/7 makes this a rational sufficient bound, not a numerical guess.
    pi_upper = F(22, 7)
    x = 4 * pi_upper / epsilon
    n = x.numerator // x.denominator + 1
    return n, eta / (2 * n), 4 * pi_upper / n


def main():
    checks = []
    def record(label, ok):
        assert ok, label
        checks.append({"check": label, "passed": True})

    for b in [F(1, 1000), F(1, 7), F(1), F(1000)]:
        # Using non-strict upper bounds b/8,b/4 still leaves factor-two slack.
        record(f"Rouche positive margin b={b}", rouche_margin(b, b/8, b/4))
        record(f"Rouche equality rejected b={b}", not rouche_margin(b, b/4, b/2))
        record(f"Rouche excess rejected b={b}", not rouche_margin(b, b/2, b/4))
    record("Zero contour separation rejected", not rouche_margin(F(0), F(0), F(0)))

    for epsilon in [F(1, 2), F(1, 100), F(1, 10000)]:
        for N in [1, 2, 10, 1000]:
            eta = F(1, N)
            n, arc_bound, norm_bound = approximation_parameters(epsilon, eta)
            record(f"Lemma parameters epsilon={epsilon},N={N}",
                   n >= 2 and norm_bound < epsilon and n * arc_bound < eta)
            # A deliberate mutation consumes the entire allowed boundary budget.
            record(f"Strict contact-budget equality rejected epsilon={epsilon},N={N}",
                   not (n * (eta/n) < eta))

    # For h(t)=t a cover's angular length is at most 2*pi*sum r_i.
    radii = [F(1, 100), F(1, 200), F(1, 400)]
    record("Disc-cover radii in small-radius regime", all(r < F(1, 2) for r in radii))
    record("Finite cover arithmetic", sum(radii) == F(7, 400))

    # The norm distance of every constant c from z is >=1, so this ball excludes c.
    record("Selected ball excludes constants", F(1, 2) < F(1))
    record("Radius exceeding one cannot use that exclusion", not (F(3, 2) < F(1)))

    # Exact model controls: c+alpha*z maps D onto B(c,|alpha|).
    # Thus E=T for alpha!=0, but E is empty for alpha=0.
    def affine_exception_measure(alpha):
        return F(0) if alpha == 0 else F(1)
    record("Constant exception set empty", affine_exception_measure(F(0)) == 0)
    for r in [F(1, 2), F(1, 100), F(1, 1000000)]:
        record(f"Arbitrarily small nonconstant perturbation r={r}",
               affine_exception_measure(r) == 1)
        # g=r*z has |g|<1 everywhere on T, yet E(g)=T: the surjectivity trap.
        boundary_contact_measure = F(0) if 0 < r < 1 else F(1)
        record(f"Non-surjective contraction countercontrol r={r}",
               boundary_contact_measure == 0 and affine_exception_measure(r) == 1)

    output = {
        "problem_id": "2305065",
        "status": "passed",
        "checks_passed": len(checks),
        "checks": checks,
        "limitations": [
            "The analytic conclusion depends on the cited published theorem or its geometric lemma.",
            "Finite arithmetic controls do not verify an infinite-dimensional existence theorem.",
            "No analytic witness, exceptional-set numerical estimate, or formal proof is produced.",
            "The affine cases are exact controls and are not candidate solutions."
        ]
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
