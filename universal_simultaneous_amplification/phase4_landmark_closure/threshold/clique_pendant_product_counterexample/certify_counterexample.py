#!/usr/bin/env python3
"""Exact certificate for the K_32-with-four-pendants product counterexample.

The solve uses FLINT over QQ.  The returned vector is then converted to
stdlib Fractions and every harmonic equation is checked independently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from flint import fmpq, fmpq_mat

from model import absorbing_states, complete_baseline, moves, states


def fq(value: Fraction) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def fraction(value: fmpq) -> Fraction:
    return Fraction(int(value.p), int(value.q))


def exact_fixation(rule: str, c: int, m: int, r: Fraction):
    extinct, fixed = absorbing_states(c, m)
    transient = [s for s in states(c, m) if s not in (extinct, fixed)]
    index = {s: k for k, s in enumerate(transient)}
    size = len(transient)
    a = fmpq_mat(size, size)
    b = fmpq_mat(size, 1)

    # Removing the self-loop from h=Ph gives
    #   (sum changing probabilities) h_s - sum_{t transient} p_st h_t
    #       = p_{s,fix}.
    for row, state in enumerate(transient):
        outgoing = moves(rule, state, c, m, r)
        changing_mass = sum(outgoing.values(), Fraction())
        a[row, row] = fq(changing_mass)
        for target, probability in outgoing.items():
            if target == fixed:
                b[row, 0] += fq(probability)
            elif target != extinct:
                a[row, index[target]] -= fq(probability)

    answer = a.solve(b)
    h = {extinct: Fraction(0), fixed: Fraction(1)}
    h.update({state: fraction(answer[k, 0]) for k, state in enumerate(transient)})

    # Independent residual evaluation in Python's rational arithmetic.
    for state in transient:
        residual = sum(
            probability * (h[target] - h[state])
            for target, probability in moves(rule, state, c, m, r).items()
        )
        assert residual == 0, (rule, state, residual)
        assert 0 < h[state] < 1, (rule, state, h[state])

    n = c + m + 1
    rho = (h[(1, 0, 0)] + c * h[(0, 1, 0)] + m * h[(0, 0, 1)]) / n
    return rho, h, transient


def digest_solution(h, transient) -> str:
    payload = "\n".join(
        f"{state}:{h[state].numerator}/{h[state].denominator}" for state in transient
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-json", type=Path)
    parser.add_argument("--full", action="store_true", help="print the full exact JSON")
    args = parser.parse_args()

    c, m, r = 31, 4, Fraction(3, 2)
    n = c + m + 1
    results = {}
    solutions = {}
    transient = None
    for rule in ("Bd", "dB"):
        rho, h, transient = exact_fixation(rule, c, m, r)
        baseline = complete_baseline(rule, n, r)
        results[rule] = {
            "rho": rho,
            "baseline": baseline,
            "ratio": rho / baseline,
            "solution_sha256": digest_solution(h, transient),
        }
        solutions[rule] = h

    normalized_product = results["Bd"]["ratio"] * results["dB"]["ratio"]
    gap = normalized_product - 1
    x = results["Bd"]["ratio"]
    y = results["dB"]["ratio"]
    balanced_gap = (x + y) / 2 - 1
    lambda_zero = (1 - y) / (x - y)
    assert results["Bd"]["ratio"] > 1
    assert results["dB"]["ratio"] < 1
    assert gap > 0
    assert balanced_gap > 0
    assert 0 < lambda_zero < Fraction(1, 2)

    report = {
        "graph": {"c": c, "m": m, "n": n, "clique_size": c + 1},
        "fitness": str(r),
        "transient_states": len(transient),
        "rules": {
            rule: {
                key: str(value) for key, value in result.items()
            }
            for rule, result in results.items()
        },
        "normalized_product": str(normalized_product),
        "product_gap": str(gap),
        "product_gap_numerator": str(gap.numerator),
        "product_gap_denominator": str(gap.denominator),
        "balanced_arithmetic_gap": str(balanced_gap),
        "balanced_arithmetic_gap_numerator": str(balanced_gap.numerator),
        "balanced_arithmetic_gap_denominator": str(balanced_gap.denominator),
        "arithmetic_crossing_lambda": str(lambda_zero),
        "decimal": {
            "Bd_ratio": f"{float(results['Bd']['ratio']):.15f}",
            "dB_ratio": f"{float(results['dB']['ratio']):.15f}",
            "normalized_product": f"{float(normalized_product):.15f}",
            "balanced_arithmetic_mean": f"{float((x + y) / 2):.15f}",
            "arithmetic_crossing_lambda": f"{float(lambda_zero):.15f}",
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.write_json:
        args.write_json.write_text(rendered + "\n")
    else:
        committed = Path(__file__).resolve().with_name("certificate.json")
        assert json.loads(committed.read_text()) == report
    if args.full:
        print(rendered)
    else:
        print(
            f"PASS: exact {len(transient)}-state solves; "
            f"Bd ratio={report['decimal']['Bd_ratio']}, "
            f"dB ratio={report['decimal']['dB_ratio']}, "
            f"product={report['decimal']['normalized_product']}"
        )
        print(
            "PASS: product-gap and balanced-arithmetic-gap numerators are "
            f"positive ({len(str(gap.numerator))} and "
            f"{len(str(balanced_gap.numerator))} decimal digits)"
        )
        print(
            "Exact arithmetic crossing lambda_0 has decimal value "
            f"{report['decimal']['arithmetic_crossing_lambda']}"
        )


if __name__ == "__main__":
    main()
