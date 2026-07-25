#!/usr/bin/env python3
"""Exact pair-level Welch audit for the K4 flag witnesses."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def trace_square(alpha: list[Q], grid: list[Q], size: int) -> Q:
    # alpha_q is the ordered q-pair count divided by N.
    return size * (1 + sum(a * q * q for a, q in zip(alpha, grid)))


def main() -> None:
    root = Path(__file__).resolve().parents[5]
    folder = Path(__file__).resolve().parent
    source_path = (
        root / "certificates/centered_quarter_bv_pseudodistribution.json"
    )
    weak_path = (
        root
        / "experiments/centered_quarter_k4_flag_psd/audit/results"
        / "full_exact_linear_witness.json"
    )
    source = json.loads(source_path.read_text())
    weak = json.loads(weak_path.read_text())
    grid = [Q(value) for value in source["grid"]]
    size = 41
    welch = Q(size * size, 5)
    weak_trace = trace_square(
        [Q(value) for value in weak["alpha"]], grid, size
    )
    source_trace = trace_square(
        [Q(value) for value in source["alpha"]], grid, size
    )
    assert weak_trace == Q(
        40814417640725411085201109,
        143939250000000000000000,
    )
    assert weak_trace < welch
    assert source_trace > welch

    summary = {
        "schema": "kissing5.k4_flag_welch_audit.v1",
        "normalization": (
            "tr(G^2)=N*(1+sum_q alpha_q*q^2), because alpha_q is "
            "the ordered q-pair count divided by N"
        ),
        "rank_at_most": 5,
        "welch_lower_bound": str(welch),
        "weak_witness_trace_g2": str(weak_trace),
        "weak_witness_trace_g2_float": float(weak_trace),
        "weak_witness_deficit": str(welch - weak_trace),
        "weak_witness_deficit_float": float(welch - weak_trace),
        "weak_witness_passes": False,
        "c093_trace_g2": str(source_trace),
        "c093_trace_g2_float": float(source_trace),
        "c093_surplus": str(source_trace - welch),
        "c093_surplus_float": float(source_trace - welch),
        "c093_passes": True,
        "conclusion": (
            "The earlier free-marginal K4 flag witness is impossible at "
            "pair-level rank five.  Subsequent tests must fix or constrain "
            "the harmonic/rank-valid pair marginal."
        ),
    }
    output = folder / "welch_audit.json"
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded)
    print(encoded, end="")
    print("sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
