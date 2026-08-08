#!/usr/bin/env python3
"""Exact Green--Poisson identity for the balanced endpoint separator.

At r=3/2, write x=rho_Bd/rho_Bd(K_n) and
y=rho_dB/rho_dB(K_n).  This verifier constructs continuous-time
type-changing generators directly from the update rules, solves their exact
Green occupation measures from a uniform singleton, and checks

    x+y-2 = T_occ + C_cut - E_disp.

The three terms are defined in ``BALANCED_POISSON_REDUCTION.md``.  Exact
finite diagnostics then show why neither a statewise nor a rankwise sign
proof can close the inequality.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import sympy as sp
from flint import fmpq, fmpq_mat

from verify_endpoint_candidates import complete_baseline, graph, hostile_corpus


R = sp.Rational(3, 2)
Q = sp.Rational(2, 3)


def harmonics(n: int, rule: str):
    if rule == "Bd":
        return tuple(sp.cancel((1 - Q**k) / (1 - Q**n)) for k in range(n + 1))
    return tuple(
        sp.cancel(
            (n - (n + sp.Rational(k, 2)) * Q**k)
            / (n * (1 - Q ** (n - 1)))
        )
        for k in range(n + 1)
    )


def changing_rates(weights, state: int, rule: str):
    n = len(weights)
    degree = tuple(sum(row, sp.Integer(0)) for row in weights)
    answer = []
    for target in range(n):
        target_mutant = bool(state & (1 << target))
        if rule == "Bd":
            mutant_mass = sum(
                (
                    weights[parent][target] / degree[parent]
                    if state & (1 << parent)
                    else 0
                )
                for parent in range(n)
            )
            resident_mass = sum(
                (
                    weights[parent][target] / degree[parent]
                    if not state & (1 << parent)
                    else 0
                )
                for parent in range(n)
            )
            rate = resident_mass if target_mutant else R * mutant_mass
        elif rule == "dB":
            row_mass = sum(
                weights[target][parent]
                for parent in range(n)
                if state & (1 << parent)
            ) / degree[target]
            rate = (
                2 * (1 - row_mass) / (2 + row_mass)
                if target_mutant
                else 3 * row_mass / (2 + row_mass)
            )
        else:
            raise ValueError(rule)
        if rate:
            answer.append((state ^ (1 << target), sp.cancel(rate)))
    return answer


def green_occupation(weights, rule: str):
    """Expected continuous occupation before absorption, exactly over QQ."""
    n = len(weights)
    full = (1 << n) - 1
    size = full - 1
    # Build the transposed system directly in FLINT.  Some separated-scale
    # witnesses have benign forward solves but severe fraction swell in a
    # generic symbolic transpose solve.
    transposed = fmpq_mat(size, size)
    source = fmpq_mat(size, 1)
    for vertex in range(n):
        source[(1 << vertex) - 1, 0] = fmpq(1, n)

    def as_fmpq(value):
        value = sp.cancel(value)
        numerator, denominator = sp.fraction(value)
        return fmpq(int(numerator), int(denominator))

    for state in range(1, full):
        row = state - 1
        rates = changing_rates(weights, state, rule)
        transposed[row, row] = as_fmpq(sum(rate for _, rate in rates))
        for target, rate in rates:
            if target not in (0, full):
                transposed[target - 1, row] -= as_fmpq(rate)
    solution = transposed.solve(source)
    occupation = tuple(
        sp.Rational(int(solution[row, 0].p), int(solution[row, 0].q))
        for row in range(size)
    )
    return occupation


def harmonic_drift(weights, state: int, rule: str, phi):
    value = phi[state.bit_count()]
    return sp.cancel(
        sum(
            rate * (phi[target.bit_count()] - value)
            for target, rate in changing_rates(weights, state, rule)
        )
    )


def state_geometry(weights, state: int):
    n = len(weights)
    k = state.bit_count()
    degree = tuple(sum(row, sp.Integer(0)) for row in weights)
    kernel = tuple(
        tuple(sp.cancel(weights[i][j] / degree[i]) for j in range(n))
        for i in range(n)
    )
    row_mass = tuple(
        sum(
            kernel[i][j]
            for j in range(n)
            if state & (1 << j)
        )
        for i in range(n)
    )
    b_cut = sum(
        row_mass[i] for i in range(n) if not state & (1 << i)
    )
    a_cut = sum(
        1 - row_mass[i] for i in range(n) if state & (1 << i)
    )
    b_complete = sp.Rational(k * (n - k), n - 1)
    c_r = sp.Rational(2 * (n - 1) ** 2, 2 * n + k - 2)
    c_m = sp.Rational(3 * (n - 1) ** 2, 2 * n + k - 3)
    alpha = sp.Rational(k, n - 1)
    beta = sp.Rational(k - 1, n - 1)
    dispersion = c_r * sum(
        (row_mass[i] - alpha) ** 2 / (2 + row_mass[i])
        for i in range(n)
        if not state & (1 << i)
    ) + c_m * sum(
        (row_mass[i] - beta) ** 2 / (2 + row_mass[i])
        for i in range(n)
        if state & (1 << i)
    )
    d_math = (
        (n + sp.Rational(k, 2) - 1)
        * sum(
            row_mass[i] / (1 + row_mass[i] / 2)
            for i in range(n)
            if not state & (1 << i)
        )
        - (n + sp.Rational(k, 2) - sp.Rational(3, 2))
        * sum(
            (1 - row_mass[i]) / (1 + row_mass[i] / 2)
            for i in range(n)
            if state & (1 << i)
        )
    )
    bridge = sp.cancel(
        d_math
        + c_m * (a_cut - b_cut)
        + (c_m - c_r) * (b_cut - b_complete)
        + dispersion
    )
    assert bridge == 0
    return a_cut, b_cut, b_complete, c_r, c_m, dispersion, d_math


def analyze(weights):
    n = len(weights)
    full = (1 << n) - 1
    phi_b = harmonics(n, "Bd")
    phi_d = harmonics(n, "dB")
    z_b = green_occupation(weights, "Bd")
    z_d = green_occupation(weights, "dB")
    baseline_b = complete_baseline(n, "Bd")
    baseline_d = complete_baseline(n, "dB")

    excess_b = sp.Integer(0)
    excess_d = sp.Integer(0)
    occupation_mismatch = sp.Integer(0)
    signed_cut = sp.Integer(0)
    negative_dispersion = sp.Integer(0)
    ranks = defaultdict(lambda: [sp.Integer(0), sp.Integer(0), sp.Integer(0)])
    positive_mismatch_atoms = []
    positive_cut_dispersion_atoms = []
    up_flux_b = defaultdict(lambda: sp.Integer(0))
    down_flux_b = defaultdict(lambda: sp.Integer(0))
    up_flux_d = defaultdict(lambda: sp.Integer(0))
    down_flux_d = defaultdict(lambda: sp.Integer(0))

    for state in range(1, full):
        row = state - 1
        k = state.bit_count()
        drift_b = harmonic_drift(weights, state, "Bd", phi_b)
        drift_d = harmonic_drift(weights, state, "dB", phi_d)
        excess_b += z_b[row] * drift_b / baseline_b
        excess_d += z_d[row] * drift_d / baseline_d
        for target, rate in changing_rates(weights, state, "Bd"):
            if target.bit_count() == k + 1:
                up_flux_b[k] += z_b[row] * rate
            else:
                assert target.bit_count() == k - 1
                down_flux_b[k] += z_b[row] * rate
        for target, rate in changing_rates(weights, state, "dB"):
            if target.bit_count() == k + 1:
                up_flux_d[k] += z_d[row] * rate
            else:
                assert target.bit_count() == k - 1
                down_flux_d[k] += z_d[row] * rate

        a_cut, b_cut, b_complete, c_r, c_m, dispersion, d_math = (
            state_geometry(weights, state)
        )
        # These two normalizations are exact consequences of the complete
        # harmonic increments:
        #   drift_B / rho_B(K_n) = q^(k-1)(A-B),
        #   drift_D / rho_D(K_n) = q^(k-1) D_math/(n-1).
        assert sp.cancel(
            drift_b / baseline_b - Q ** (k - 1) * (a_cut - b_cut)
        ) == 0
        assert sp.cancel(
            drift_d / baseline_d
            - Q ** (k - 1) * d_math / (n - 1)
        ) == 0

        mismatch_atom = sp.cancel(
            Q ** (k - 1)
            * (z_b[row] - c_m * z_d[row] / (n - 1))
            * (a_cut - b_cut)
        )
        cut_atom = sp.cancel(
            -Q ** (k - 1)
            * z_d[row]
            / (n - 1)
            * (c_m - c_r)
            * (b_cut - b_complete)
        )
        dispersion_atom = sp.cancel(
            -Q ** (k - 1) * z_d[row] * dispersion / (n - 1)
        )
        occupation_mismatch += mismatch_atom
        signed_cut += cut_atom
        negative_dispersion += dispersion_atom
        ranks[k][0] += mismatch_atom
        ranks[k][1] += cut_atom
        ranks[k][2] += dispersion_atom
        if mismatch_atom > 0:
            positive_mismatch_atoms.append((state, mismatch_atom))
        if cut_atom + dispersion_atom > 0:
            positive_cut_dispersion_atoms.append(
                (state, sp.cancel(cut_atom + dispersion_atom))
            )

    excess_b = sp.cancel(excess_b)
    excess_d = sp.cancel(excess_d)
    occupation_mismatch = sp.cancel(occupation_mismatch)
    signed_cut = sp.cancel(signed_cut)
    negative_dispersion = sp.cancel(negative_dispersion)
    assert sp.cancel(
        excess_b
        + excess_d
        - occupation_mismatch
        - signed_cut
        - negative_dispersion
    ) == 0
    rho_b = sp.cancel(baseline_b * (1 + excess_b))
    rho_d = sp.cancel(baseline_d * (1 + excess_d))
    for k in range(1, n):
        assert sp.cancel(up_flux_b[k] - down_flux_b[k + 1] - rho_b) == 0
        assert sp.cancel(up_flux_d[k] - down_flux_d[k + 1] - rho_d) == 0
    return {
        "excess_b": excess_b,
        "excess_d": excess_d,
        "total": sp.cancel(excess_b + excess_d),
        "mismatch": occupation_mismatch,
        "cut": signed_cut,
        "dispersion": negative_dispersion,
        "ranks": {
            k: tuple(map(sp.cancel, values)) for k, values in ranks.items()
        },
        "positive_mismatch_atoms": positive_mismatch_atoms,
        "positive_cut_dispersion_atoms": positive_cut_dispersion_atoms,
    }


def exact_mismatch_counterexample():
    """A path whose aggregate occupation-mismatch term is positive."""
    # Vertex order along the path is 4--0--3--1--2, with consecutive
    # weights 1033,1,6,1269.
    return graph(
        5,
        [(0, 3, 1), (0, 4, 1033), (1, 2, 1269), (1, 3, 6)],
    )


def first_change_balancing_coefficient(weights):
    """Coefficient that exactly balances Bd/dB reach-two deviations."""
    n = len(weights)
    degree = tuple(sum(row, sp.Integer(0)) for row in weights)
    kernel = tuple(
        tuple(sp.cancel(weights[i][j] / degree[i]) for j in range(n))
        for i in range(n)
    )
    temperature = tuple(
        sum(kernel[j][i] for j in range(n)) for i in range(n)
    )
    q_b = sum(R / (R + value) for value in temperature) / n
    lambda_d = tuple(
        sum(
            R * kernel[j][i] / (1 + (R - 1) * kernel[j][i])
            for j in range(n)
        )
        for i in range(n)
    )
    q_d = sum(value / (1 + value) for value in lambda_d) / n
    q_b_complete = R / (R + 1)
    q_d_complete = sp.cancel(R * (n - 1) / ((R + 1) * n - 2))
    deviation_b = sp.cancel(q_b - q_b_complete)
    deviation_d = sp.cancel(q_d - q_d_complete)
    assert deviation_b > 0 > deviation_d
    return sp.cancel(-deviation_d / (deviation_b - deviation_d))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="run all ten witnesses rather than the three exact route obstructions",
    )
    parser.add_argument("--label", help="run one named hostile witness")
    args = parser.parse_args()
    labels = None
    if args.label:
        labels = {args.label}
    elif not args.all:
        labels = {
            "weighted-star",
            "separated-path",
            "rationalized-nearest-five-edge",
        }

    count = 0
    records = {}
    for label, weights in hostile_corpus():
        if labels is not None and label not in labels:
            continue
        result = analyze(weights)
        records[label] = result
        assert result["total"] <= 0
        print(
            f"PASS {label}: eB~{sp.N(result['excess_b'], 10)}, "
            f"eD~{sp.N(result['excess_d'], 10)}, "
            f"sum~{sp.N(result['total'], 10)}, "
            f"T~{sp.N(result['mismatch'], 10)}, "
            f"C~{sp.N(result['cut'], 10)}, "
            f"-E~{sp.N(result['dispersion'], 10)}",
            flush=True,
        )
        count += 1

    # Exact failures of stronger proof shortcuts.  They do not refute the
    # total inequality on the witness graphs.
    if labels is None or "weighted-star" in labels:
        star = records["weighted-star"]
        assert star["positive_mismatch_atoms"]
        assert star["positive_cut_dispersion_atoms"]
        assert sum(star["ranks"][1]) > 0
        assert star["total"] < 0
    if labels is None or "rationalized-nearest-five-edge" in labels:
        chord = records["rationalized-nearest-five-edge"]
        assert sum(chord["ranks"][2]) > 0
        assert chord["total"] < 0

        # A natural graph-sensitive coefficient balances the exact singleton
        # reach-two deviations of the two rules.  It is nevertheless too
        # Bd-heavy on this graph and gives an exact false separator.
        chord_weights = next(
            weights
            for label, weights in hostile_corpus()
            if label == "rationalized-nearest-five-edge"
        )
        local_lambda = first_change_balancing_coefficient(chord_weights)
        local_score = sp.cancel(
            local_lambda * (1 + chord["excess_b"])
            + (1 - local_lambda) * (1 + chord["excess_d"])
        )
        assert 0 < local_lambda < 1
        assert local_score > 1
        print(
            "PASS: exact first-change-balanced graph-sensitive coefficient "
            f"fails (lambda~{sp.N(local_lambda, 10)}, "
            f"score~{sp.N(local_score, 12)})"
        )

    if labels is None:
        mismatch = analyze(exact_mismatch_counterexample())
        assert mismatch["mismatch"] > 0
        assert mismatch["cut"] + mismatch["dispersion"] < 0
        assert mismatch["total"] < 0
        assert sum(mismatch["ranks"][2]) > 0
        print(
            "PASS: exact path refutes aggregate T<=0: "
            f"T~{sp.N(mismatch['mismatch'], 12)}, "
            f"C-E~{sp.N(mismatch['cut'] + mismatch['dispersion'], 12)}, "
            f"total~{sp.N(mismatch['total'], 12)}"
        )
    print(f"PASS: exact balanced Green--Poisson identity on {count} witnesses")
    print("PASS: statewise and fixed-rank sign strengthenings are exactly false")


if __name__ == "__main__":
    main()
