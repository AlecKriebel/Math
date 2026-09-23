#!/usr/bin/env python3
"""Exact finite checks for the strict Dirichlet gap inequality.

Only Python's standard library is used.  These checks audit algebra and known
box spectra; they are not a proof for arbitrary domains or infinite spectra.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


class VerificationError(RuntimeError):
    pass


CHECK_COUNT = 0


def check(condition: bool, message: str) -> None:
    """A check that remains active when Python is run with -O."""
    global CHECK_COUNT
    CHECK_COUNT += 1
    if not condition:
        raise VerificationError(message)


def rational(value: F | int) -> str:
    return str(F(value))


def moments(values: list[F], n: int) -> tuple[F, F, F, F]:
    a = sum(values, F(0)) / len(values)
    b = sum((e * e for e in values), F(0)) / len(values)
    m1 = F(n + 2, n) * a
    d = m1 * m1 - F(n + 4, n) * b
    return a, b, m1, d


def q_direct(values: list[F], n: int, t: F) -> F:
    return sum(((t - e) ** 2 - F(4, n) * (t - e) * e
                for e in values), F(0)) / len(values)


def check_quadratic() -> dict:
    """Check coefficient identities, evaluations, and spectral homogeneity."""
    spectra = [
        [F(1)],
        [F(2), F(2), F(2)],
        [F(1, 3), F(7, 5), F(7, 5), F(19, 4)],
        [F(3), F(11), F(27), F(61), F(105)],
    ]
    scales = [F(1, 7), F(3, 2), F(11)]
    evaluations = 0
    for n in range(1, 7):
        for values in spectra:
            a, b, m1, d = moments(values, n)
            # Coefficients are computed independently from the summands.
            coefficients = (
                sum((F(1) for _ in values), F(0)) / len(values),
                sum((-2 * e - F(4, n) * e for e in values), F(0)) / len(values),
                sum((e * e + F(4, n) * e * e for e in values), F(0)) / len(values),
            )
            check(coefficients == (F(1), -2 * m1, m1 * m1 - d),
                  "Quadratic coefficient identity")
            check(coefficients[2] == F(n + 4, n) * b,
                  "Constant term uses mean squared energy")
            for t in [F(-3, 2), F(0), values[0], values[-1], F(17, 3)]:
                check(q_direct(values, n, t) == (t - m1) ** 2 - d,
                      "Completed-square evaluation")
                evaluations += 1
            for c in scales:
                ca, cb, cm1, cd = moments([c * e for e in values], n)
                check((ca, cb, cm1, cd) == (c * a, c * c * b, c * m1, c * c * d),
                      "Moment scaling under E -> c E")
                check(q_direct([c * e for e in values], n, c * F(7, 3))
                      == c * c * q_direct(values, n, F(7, 3)),
                      "Q scaling under (E,t) -> (c E,c t)")
    return {"status": "pass", "dimensions": [1, 2, 3, 4, 5, 6],
            "synthetic_spectra": len(spectra), "evaluations": evaluations,
            "energy_scale_factors": list(map(rational, scales))}


def synthetic_coefficient(alpha: int, j: int, k: int) -> F:
    """Explicit nonzero rational entries of a symmetric synthetic matrix."""
    p, q = sorted((j + 1, k + 1))
    sign = -1 if (p + q + alpha) % 2 else 1
    return F(sign * (p * q + alpha + 1), p + q + alpha + 2)


def check_remainder() -> dict:
    """Audit finite algebra WITHOUT imposing unrealizable finite sum rules."""
    energies = [F(1), F(1), F(5, 2), F(4), F(4), F(7), F(10)]
    thresholds = [F(0), F(1), F(7, 4), F(5, 2), F(3), F(4), F(11, 2), F(7), F(12)]
    dimension = 3
    rows = []
    for z in thresholds:
        low = [j for j, e in enumerate(energies) if e < z]
        high = [k for k, e in enumerate(energies) if e > z]
        internal = F(0)
        t_full = F(0)
        t_moments = F(0)
        positive_remainder = F(0)
        for alpha in range(dimension):
            for j in low:
                ej = energies[j]
                tj = z - ej
                s1 = F(0)
                s2 = F(0)
                for k, ek in enumerate(energies):
                    ajk = synthetic_coefficient(alpha, j, k)
                    check(ajk == synthetic_coefficient(alpha, k, j),
                          "Synthetic matrix symmetry")
                    weight = ajk * ajk
                    delta = ek - ej
                    term = tj * delta * (z - ek) * weight
                    t_full += term
                    s1 += delta * weight
                    s2 += delta * delta * weight
                    if k in low:
                        internal += term
                        opposite = (z - ek) * (-delta) * (z - ej) * weight
                        check(term + opposite == 0, "Internal ordered-pair cancellation")
                    if ek == z:
                        check(term == 0, "Threshold eigenspace contributes zero")
                    if k in high:
                        summand = tj * delta * (ek - z) * weight
                        check(summand > 0, "Every nonzero low-to-high summand is positive")
                        positive_remainder += summand
                t_moments += tj * tj * s1 - tj * s2
        check(internal == 0, "Full internal spectral block cancels")
        check(t_full == t_moments, "Full finite remainder moment expansion")
        check(-t_full == positive_remainder, "Full finite remainder sign and normalization")
        check(positive_remainder >= 0, "Finite positive remainder")
        rows.append({"z": rational(z), "low_count": len(low),
                     "threshold_count": energies.count(z), "high_count": len(high),
                     "T": rational(t_full), "positive_remainder": rational(positive_remainder)})

    # In finite dimension, the total first moment of a symmetric matrix is zero.
    # Therefore the Laplacian sum rule s1_j = 1 for EVERY j cannot hold here.
    all_first_moments = sum(
        ((ek - ej) * synthetic_coefficient(alpha, j, k) ** 2
         for alpha in range(dimension)
         for j, ej in enumerate(energies) for k, ek in enumerate(energies)), F(0))
    check(all_first_moments == 0, "Finite trace obstruction is explicit")
    check(all_first_moments != dimension * len(energies),
          "Synthetic matrices are not asserted to realize Laplacian sum rules")
    return {"status": "pass", "energies": list(map(rational, energies)),
            "coordinate_matrices": dimension, "threshold_cases": rows,
            "limitation": "Synthetic symmetric matrices check finite algebra only; they do not realize Dirichlet coordinate sum rules."}


def certified_box_spectrum(lengths: tuple[F, ...], count: int, copies: int) -> tuple[list[F], int, F]:
    """Enumerate until a rigorous omitted-mode bound certifies the prefix.

    If every index 1 <= m_i <= K is enumerated, any omitted mode has some
    m_i >= K+1 and every other index >= 1.  The minimum of the resulting
    coordinatewise bounds is a lower bound for EVERY omitted eigenvalue.
    Strict comparison also rules out missing multiplicity at the final level.
    """
    n = len(lengths)
    k_cut = 1
    while True:
        inverse_squares = [1 / (length * length) for length in lengths]
        one_box = sorted(sum((F(m * m) * weight for m, weight in zip(mode, inverse_squares)), F(0))
                         for mode in product(range(1, k_cut + 1), repeat=n))
        spectrum = [e for e in one_box for _ in range(copies)]
        omitted_bound = min(
            F((k_cut + 1) ** 2) * inverse_squares[i]
            + sum((inverse_squares[h] for h in range(n) if h != i), F(0))
            for i in range(n))
        if len(spectrum) >= count and spectrum[count - 1] < omitted_bound:
            check(all(spectrum[i] <= spectrum[i + 1] for i in range(count - 1)),
                  "Enumerated box spectrum is ordered with multiplicity")
            check(spectrum[count - 1] < omitted_bound,
                  "Omitted-mode lower bound certifies complete prefix")
            return spectrum[:count], k_cut, omitted_bound
        k_cut *= 2
        if k_cut > 512:
            raise VerificationError("Unexpectedly large box cutoff")


def check_boxes() -> dict:
    configs = [
        ("interval", (F(1),), 1, 128),
        ("rational_interval", (F(3, 2),), 1, 64),
        ("square", (F(1), F(1)), 1, 96),
        ("rectangle", (F(1), F(3, 2)), 1, 96),
        ("long_rectangle", (F(1), F(5)), 1, 96),
        ("cube", (F(1),) * 3, 1, 96),
        ("rectangular_box_3d", (F(1), F(3, 2), F(5, 3)), 1, 96),
        ("hypercube_4d", (F(1),) * 4, 1, 96),
        ("rectangular_box_4d", (F(1), F(3, 2), F(5, 3), F(2)), 1, 96),
        ("two_disjoint_intervals", (F(1),), 2, 64),
        ("five_disjoint_squares", (F(1), F(1)), 5, 96),
        ("three_disjoint_rectangles", (F(1), F(3, 2)), 3, 96),
        ("three_disjoint_cubes", (F(1),) * 3, 3, 96),
        ("four_disjoint_hypercubes", (F(1),) * 4, 4, 96),
    ]
    reports = []
    total_j = 0
    total_repeated = 0
    total_ground_multiplicity = 0
    geometric_scale = F(7, 3)
    energy_scale = 1 / (geometric_scale * geometric_scale)
    for name, lengths, copies, max_j in configs:
        n = len(lengths)
        spectrum, cutoff, omitted_bound = certified_box_spectrum(lengths, max_j + 1, copies)
        exact_ground = sum((1 / (length * length) for length in lengths), F(0))
        check(spectrum[:copies] == [exact_ground] * copies and spectrum[copies] > exact_ground,
              f"{name}: analytic ground energy and exact ground multiplicity")
        if name == "square":
            check(spectrum[:10] == list(map(F, [2, 5, 5, 8, 10, 10, 13, 13, 17, 17])),
                  "Square prefix agrees with direct enumeration by hand")
        if name == "hypercube_4d":
            check(spectrum[:11] == list(map(F, [4] + [7] * 4 + [10] * 6)),
                  "Hypercube prefix agrees with binomial multiplicities")
        scaled_spectrum, _, _ = certified_box_spectrum(
            tuple(geometric_scale * length for length in lengths), max_j + 1, copies)
        check(scaled_spectrum == [energy_scale * e for e in spectrum],
              f"{name}: independently enumerated geometric scaling")
        repeated = 0
        ground_multiplicity = 0
        min_relative = None
        min_row = None
        for j in range(1, max_j + 1):
            values = spectrum[:j]
            _, _, m1, d = moments(values, n)
            y, z = spectrum[j - 1], spectrum[j]
            gap_quarter = (z - y) ** 2 / 4
            margin = d - gap_quarter
            if n == 1 and copies == 1:
                # Independent closed forms from the sums of squares/fourth powers.
                interval_d = F((j + 1) * (2 * j + 1) * (3 * j + 5), 12) / lengths[0] ** 4
                interval_margin = F((2 * j + 1) * (3 * j * j + 2 * j + 2), 12) / lengths[0] ** 4
                check(d == interval_d and margin == interval_margin,
                      f"{name}, J={j}: independent closed-form interval result")
            check(margin > 0, f"{name}, J={j}: strict gap inequality")
            check(q_direct(values, n, y) <= 0, f"{name}, J={j}: lower endpoint Yang inequality")
            if z > spectrum[0]:
                check(q_direct(values, n, z) < 0,
                      f"{name}, J={j}: strict upper endpoint Yang inequality")
            else:
                ground_multiplicity += 1
                check(d == F(4, n * n) * spectrum[0] ** 2 and gap_quarter == 0,
                      f"{name}, J={j}: exceptional repeated ground state formula")
            if y == z:
                repeated += 1
            _, _, sm1, sd = moments(scaled_spectrum[:j], n)
            scaled_margin = sd - (scaled_spectrum[j] - scaled_spectrum[j - 1]) ** 2 / 4
            check(sm1 == energy_scale * m1 and sd == energy_scale ** 2 * d
                  and scaled_margin == energy_scale ** 2 * margin,
                  f"{name}, J={j}: length scaling gives inverse fourth-power margin")
            relative = margin / (z * z)
            if min_relative is None or relative < min_relative:
                min_relative = relative
                min_row = {"J": j, "E_J": rational(y), "E_next": rational(z),
                           "D": rational(d), "gap_squared_over_four": rational(gap_quarter),
                           "margin": rational(margin), "margin_over_E_next_squared": rational(relative)}
        total_j += max_j
        total_repeated += repeated
        total_ground_multiplicity += ground_multiplicity
        reports.append({"name": name, "dimension": n,
                        "lengths": list(map(rational, lengths)), "identical_disjoint_copies": copies,
                        "J_min": 1, "J_max": max_j, "coordinate_cutoff_K": cutoff,
                        "enumerated_modes_with_multiplicity": copies * cutoff ** n,
                        "last_needed_energy": rational(spectrum[-1]),
                        "omitted_energy_lower_bound": rational(omitted_bound),
                        "first_ten_energies": list(map(rational, spectrum[:10])),
                        "zero_gap_cases": repeated, "E_next_equals_ground_cases": ground_multiplicity,
                        "smallest_relative_margin_case": min_row, "status": "pass"})
    check(total_repeated > 0 and total_ground_multiplicity > 0,
          "Multiplicity boundary cases were actually exercised")
    check(set(row["dimension"] for row in reports) == {1, 2, 3, 4},
          "Box dimensions one through four were exercised")
    return {"status": "pass", "normalization": "E = lambda / pi^2 = sum_i (m_i/L_i)^2; m_i >= 1",
            "J_cases": total_j, "zero_gap_cases": total_repeated,
            "E_next_equals_ground_cases": total_ground_multiplicity,
            "geometric_scale_factor": rational(geometric_scale),
            "energy_scale_factor": rational(energy_scale),
            "cases": reports}


def check_negative_controls() -> dict:
    values = [F(1), F(4), F(9)]
    n, c, t = 2, F(3), F(7, 2)
    a, _, m1, _ = moments(values, n)
    wrong_d = m1 * m1 - F(n + 4, n) * a  # Deliberate mean(E) for mean(E^2) mutation.
    ca, _, cm1, _ = moments([c * e for e in values], n)
    wrong_scaled_d = cm1 * cm1 - F(n + 4, n) * ca
    quadratic_residual = q_direct(values, n, t) - ((t - m1) ** 2 - wrong_d)
    scaling_residual = wrong_scaled_d - c * c * wrong_d
    check(quadratic_residual != 0, "Negative control catches unsquared second moment")
    check(scaling_residual != 0, "Negative control catches dimensional inconsistency")
    # One low mode, one high mode, one coordinate, coefficient a_12 = 1.
    e_low, e_high, z = F(1), F(5), F(3)
    t_full = (z - e_low) * (e_high - e_low) * (z - e_high)
    remainder = (z - e_low) * (e_high - e_low) * (e_high - z)
    check(-t_full == remainder, "Sign negative-control baseline")
    check(t_full != remainder, "Negative control catches T = +remainder sign mutation")
    return {"status": "pass", "expected_failures_detected": 3,
            "unsquared_moment_quadratic_residual": rational(quadratic_residual),
            "unsquared_moment_scaling_residual": rational(scaling_residual),
            "wrong_sign_identity_residual": rational(t_full - remainder)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    results = {"schema_version": 1, "arithmetic": "exact fractions.Fraction throughout",
               "claim_checked_on_boxes": "D > (E_(J+1)-E_J)^2/4, D=((n+2)/n mean(E))^2-(n+4)/n mean(E^2)",
               "scope": "Finite algebra and certified exact spectra of specified boxes only; not an infinite-dimensional theorem proof.",
               "quadratic": check_quadratic(), "finite_remainder": check_remainder(),
               "boxes": check_boxes(), "negative_controls": check_negative_controls()}
    results["check_count"] = CHECK_COUNT
    results["status"] = "pass"
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {CHECK_COUNT} exact checks; {results['boxes']['J_cases']} certified box/J cases; "
          f"{results['negative_controls']['expected_failures_detected']} negative controls detected.")
    print(f"Results: {args.output}")


if __name__ == "__main__":
    main()
