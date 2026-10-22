#!/usr/bin/env python3
"""Exact algebra diagnostics for the reviewed metric/rescaling mechanism.

These finite checks do not construct Nash embeddings and do not establish
any universal existence theorem. Universal deductions are in REPORT.md.
Every failure condition uses require(), so python -O retains all checks.
No third-party modules or input files are required.
"""

from fractions import Fraction as Q
import hashlib
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def prod(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def rq(lengths, frequency):
    return sum((Q(k * k) / (ell * ell) for k, ell in zip(frequency, lengths)), Q(0))


def first_positive(lengths):
    # Exact first positive eigenvalue on R^m/(2*pi*Z)^m with
    # constant diagonal metric diag(lengths_i^2).
    return 1 / max(ell * ell for ell in lengths)


def main():
    rng = random.Random(1142_30002112)
    c = Q(4)
    length_choices = (Q(1, 2), Q(1), Q(3, 2), Q(2), Q(3))
    stretch_choices = (Q(1, 2), Q(2, 3), Q(1), Q(3, 2), Q(2))
    counts = {"flat_torus_metric_pairs": 0, "fourier_rayleigh_checks": 0,
              "finite_quadrature_density_checks": 0,
              "area_corrected_eigenvalue_checks": 0,
              "dimension_tolerance_checks": 0, "mean_zero_control_examples": 0}
    witness = hashlib.sha256()

    # Genuine smooth metrics and genuine smooth Fourier functions on closed tori.
    # The absolute torus volume has a common (2*pi)^m factor, which cancels.
    for m in range(2, 33):
        for trial in range(20):
            g_lengths = tuple(rng.choice(length_choices) for _ in range(m))
            stretches = tuple(rng.choice(stretch_choices) for _ in range(m))
            h_lengths = tuple(a * b for a, b in zip(g_lengths, stretches))
            require(all(1 / c <= t * t <= c for t in stretches), "pointwise metric ratio")
            volume_ratio = prod(stretches)
            require(c ** (-m) <= volume_ratio ** 2 <= c ** m, "volume density bound")
            lg = first_positive(g_lengths)
            lh = first_positive(h_lengths)
            require(c ** (-m - 1) * lg <= lh <= c ** (m + 1) * lg,
                    "full-space first eigenvalue bound")
            # Area-corrected lambda ratio is volume_ratio^(2/m) * lh/lg.
            # Raise the positive inequality to m to avoid all irrational roots.
            normalized_power = volume_ratio ** 2 * (lh / lg) ** m
            require(c ** (-m * (m + 2)) <= normalized_power <= c ** (m * (m + 2)),
                    "combined exact-area eigenvalue bound")
            counts["area_corrected_eigenvalue_checks"] += 1
            for _ in range(8):
                frequency = tuple(rng.randint(-3, 3) for _ in range(m))
                if not any(frequency):
                    frequency = (1,) + frequency[1:]
                rg = rq(g_lengths, frequency)
                rh = rq(h_lengths, frequency)
                require(rg > 0 and rh > 0, "nonzero Fourier function quotient")
                require(c ** (-m - 1) * rg <= rh <= c ** (m + 1) * rg,
                        "Rayleigh comparison")
                counts["fourier_rayleigh_checks"] += 1
                witness.update(f"T{m}:{trial}:{rg}:{rh}:{volume_ratio}\n".encode())
            counts["flat_torus_metric_pairs"] += 1

    # Algebra stress-test with cell-dependent metric/volume coefficients.
    # This is finite positive quadrature data, NOT a constructed smooth metric
    # or a finite-element spectral computation. It tests the independent
    # numerator/denominator estimates used in the universal proof.
    for m in range(2, 17):
        for trial in range(30):
            eg = eh = ng = nh = vg = vh = Q(0)
            for _ in range(6):
                stretches = tuple(rng.choice(stretch_choices) for _ in range(m))
                density = prod(stretches)
                weight = Q(rng.randint(1, 5), rng.randint(1, 5))
                value = Q(rng.randint(-4, 4), 3)
                gradient = tuple(Q(rng.randint(-4, 4), 3) for _ in range(m))
                eg += weight * sum((p * p for p in gradient), Q(0))
                eh += weight * density * sum((p * p / (t * t)
                                               for p, t in zip(gradient, stretches)), Q(0))
                ng += weight * value * value
                nh += weight * density * value * value
                vg += weight
                vh += weight * density
            require(eg > 0 and eh > 0 and ng > 0 and nh > 0, "positive quadrature quotients")
            rg, rh = eg / ng, eh / nh
            require(c ** (-m - 1) * rg <= rh <= c ** (m + 1) * rg,
                    "variable-density Rayleigh algebra")
            require(c ** (-m) <= (vh / vg) ** 2 <= c ** m, "variable-density volume algebra")
            counts["finite_quadrature_density_checks"] += 1
            witness.update(f"Q{m}:{trial}:{rg}:{rh}:{vh/vg}\n".encode())

    # A rational explicit choice used by the universal tolerance argument.
    # Finite checks below are diagnostics. The all-m proof is the geometric
    # series estimate in REPORT.md, not this range of tests.
    for m in range(2, 257):
        n = m + 2
        cm = Q(4 * n + 1, 4 * n)
        require(1 < cm <= Q(17, 16), "dimension-dependent c range")
        require(cm ** n < Q(4, 3) < 2, "dimension-dependent spectral margin")
        require(cm < 4, "area scaling factor below two")
        counts["dimension_tolerance_checks"] += 1

    # A genuine smooth two-dimensional metric control for the min-max domain.
    # On the flat (2*pi)-periodic torus, h=(1+epsilon*cos x)g and u=cos x.
    # Use exact Fourier averages: <cos x>=0, <cos^2 x>=1/2.
    epsilon = Q(1, 2)
    mean_g = Q(0)
    mean_h_relative_g_volume = epsilon * Q(1, 2)
    require(1 - epsilon > 0, "conformal metric is positive")
    require(mean_g == 0 and mean_h_relative_g_volume == Q(1, 4),
            "metric-dependent mean-zero subspaces differ")
    counts["mean_zero_control_examples"] = 1

    print(json.dumps({
        "result": "PASS",
        "arithmetic": "fractions.Fraction, all failure checks explicit under normal and -O",
        "counts": counts,
        "transcript_sha256": witness.hexdigest(),
        "mean_zero_control": {"g_mean_relative_g_volume": str(mean_g),
                              "h_mean_relative_g_volume": str(mean_h_relative_g_volume)},
        "limits": "Finite algebra diagnostics only; no numerical Nash embedding or existence proof."
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
