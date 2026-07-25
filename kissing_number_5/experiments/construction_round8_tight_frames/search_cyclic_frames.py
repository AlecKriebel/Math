#!/usr/bin/env python3
"""Exhaust and interval-certify all cyclic 41-by-5 harmonic UNTFs."""

from __future__ import annotations

import json
from pathlib import Path

import checker


def main() -> None:
    settings = {
        "atan_1_over_5_terms": 20,
        "atan_1_over_239_terms": 6,
        "cosine_terms": 20,
    }
    pi_interval = checker.pi_bounds(
        settings["atan_1_over_5_terms"],
        settings["atan_1_over_239_terms"],
    )
    cosine_bounds = {
        residue: checker.cosine_residue_bounds(
            residue, pi_interval, settings["cosine_terms"]
        )
        for residue in range(21)
    }
    records = []
    results = {}
    for a in checker.FREQUENCIES:
        for b in checker.FREQUENCIES:
            if a >= b:
                continue
            lower, upper, maximizers = checker.minimax_interval(
                a, b, cosine_bounds
            )
            sign_switch_witness = checker.sign_switch_obstruction_difference(
                a, b, cosine_bounds
            )
            results[(a, b)] = lower, upper, maximizers
            records.append(
                {
                    "frequencies": [a, b],
                    "maximum_lower": str(lower),
                    "maximum_upper": str(upper),
                    "maximum_midpoint_decimal": float((lower + upper) / 2),
                    "possible_maximizing_differences": maximizers,
                    "sign_switch_obstruction_difference": (
                        sign_switch_witness
                    ),
                }
            )

    best_pairs = sorted(checker.orbit((1, 9)))
    best_lower, best_upper, _ = results[(1, 9)]
    data = {
        "schema": "cyclic-real-harmonic-untf-41x5-v2",
        "order": checker.ORDER,
        "dimension": checker.DIMENSION,
        "pi_method": "Machin directed alternating series",
        "interval_settings": settings,
        "number_of_frequency_pairs": len(records),
        "globally_best_frequency_pairs": [
            list(pair) for pair in best_pairs
        ],
        "global_optimum_lower": str(best_lower),
        "global_optimum_upper": str(best_upper),
        "global_optimum_midpoint_decimal": float(
            (best_lower + best_upper) / 2
        ),
        "kissing_threshold": "1/2",
        "feasible_frequency_pairs": 0,
        "arbitrary_row_sign_flips_feasible_frequency_pairs": 0,
        "pairs": records,
    }
    checker.RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    checker.RESULT_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {checker.RESULT_PATH}")
    print(f"pairs={len(records)} feasible=0")
    print(
        "global optimum interval:",
        float(best_lower),
        float(best_upper),
    )
    print("globally best pairs:", best_pairs)


if __name__ == "__main__":
    main()
