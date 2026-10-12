"""Reproducible exact-arithmetic checks for the probability-family audit.

These are algebraic sanity checks, not a simulation or a substitute for the
conditioning, measurability, and infinite-limit proofs in REPORT.md.
Run with Python 3. Uses only the standard library and writes only this folder.
"""

from fractions import Fraction
from pathlib import Path
import json
import math


def run_checks():
    checks = []

    source_stages = []
    for n in range(12):
        D = 2 ** (4 * n + 8)
        child_tail = Fraction(1, 2 ** (n + 3))
        scaled_window = Fraction(1, 2 ** (n + 2))
        arrow_lower = scaled_window / 2
        p_lower = child_tail * arrow_lower
        mean_lower = D * p_lower
        assert p_lower == Fraction(1, 2 ** (2 * n + 6))
        assert mean_lower == 4 ** (n + 1)
        assert 4 ** (n + 1) >= 4 * (n + 1)
        assert scaled_window - scaled_window**2 / 2 >= arrow_lower
        source_stages.append({
            "n": n,
            "D_n": D,
            "scaled_window": str(scaled_window),
            "eligible_mean_lower": int(mean_lower),
            "failure_bound": str(Fraction(1, 16 ** (n + 1))),
        })
    checks.append("Submission's stage algebra verified exactly for n=0..11; REPORT.md proves all n.")

    # The infinite geometric tail is exact, not a floating truncation.
    geometric_failure_sum = Fraction(1, 16) / (1 - Fraction(1, 16))
    annealed_prefactor = Fraction(1, 4) * (1 - geometric_failure_sum)
    assert geometric_failure_sum == Fraction(1, 15)
    assert annealed_prefactor == Fraction(7, 30)
    checks.append("Infinite first-failure sum = 1/15 and annealed prefactor = 7/30 exactly.")

    recovery_partials = []
    for N in range(1, 20):
        total = 1 + sum(Fraction(1, 2 ** (n - 1)) for n in range(1, N + 1))
        assert total == 3 - Fraction(2, 2 ** N)
        assert total < 3
        recovery_partials.append({"vertices_after_root": N, "total_exposure_over_T": str(total)})
    checks.append("Recovery exposure partial sum = (3 - 2^(1-N))T; its increasing limit is 3T.")

    independent_stage_means = []
    previous = None
    for n in range(1, 10):
        a_n = Fraction(3, 4) * 2 ** (4 * 2 ** (n - 1) - n - 1)
        assert a_n >= 3 * n
        if previous is not None:
            assert a_n / previous >= 8
        independent_stage_means.append({"n": n, "eligible_mean_lower": int(a_n)})
        previous = a_n
    e3_lower = sum(Fraction(3 ** j, math.factorial(j)) for j in range(5))
    assert e3_lower == Fraction(131, 8)
    assert e3_lower > 16
    checks.append("Independent threshold argument has a_1=3, growth ratio >=8, and exact e^3 lower bound 131/8 >16.")

    # Diagnostic actual first-stage failure, not used to justify an infinite product.
    p0 = (1 - math.exp(-0.25)) / 8
    diagnostic = {
        "actual_submission_stage_0_failure": math.exp(256 * math.log1p(-p0)),
        "source_stage_0_exponential_failure_bound": math.exp(-4),
        "source_stage_0_dyadic_failure_bound": 1 / 16,
        "total_source_geometric_failure_bound": float(geometric_failure_sum),
        "independent_prefactor_proven_lower": float(Fraction(1, 4) * (1 - 1 / (math.exp(3) - 1))),
        "target_prefactor": float(annealed_prefactor),
    }
    assert diagnostic["actual_submission_stage_0_failure"] < diagnostic["source_stage_0_exponential_failure_bound"]
    assert diagnostic["independent_prefactor_proven_lower"] > diagnostic["target_prefactor"]

    return {
        "status": "PASS",
        "checks": checks,
        "submission_stages": source_stages,
        "recovery_partial_exposures": recovery_partials,
        "independent_stages": independent_stage_means,
        "exact_failure_sum": str(geometric_failure_sum),
        "exact_annealed_prefactor": str(annealed_prefactor),
        "diagnostic_floating_values_not_proof": diagnostic,
        "limitations": [
            "No random simulation was used.",
            "Finite checks do not by themselves prove adaptive independence or the all-stage limit.",
            "Infinite-stage, quenched, and measurability arguments are analytic and documented separately.",
        ],
    }


if __name__ == "__main__":
    result = run_checks()
    destination = Path(__file__).resolve().parent / "CHECK_RESULTS.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"], "output": str(destination)}, indent=2))
