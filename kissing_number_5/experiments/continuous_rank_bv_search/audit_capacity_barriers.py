#!/usr/bin/env python3
"""Exact audit of the corrected stratified capacity cuts on prior barriers."""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path

from experiments.continuous_rank_bv_search.search import (
    N,
    feasible_orbits,
    qstr,
    stratified_capacity_rows,
    weighted_capacity_rows,
)


def load_source(path: Path):
    data = json.loads(path.read_text())
    if "grid" in data:
        nodes = tuple(Q(value) for value in data["grid"])
        alpha = tuple(Q(value) for value in data["alpha"])
        orbits = feasible_orbits(nodes)
        orbit_index = {orbit: index for index, orbit in enumerate(orbits)}
        nu = [Q(0) for _ in orbits]
        for orbit, weight in zip(data["triples"], data["nu"]):
            nu[orbit_index[tuple(orbit)]] = Q(weight)
    else:
        nodes = tuple(Q(value) for value in data["nodes"])
        alpha = tuple(Q(value, N) for value in data["ordered_pair_counts"])
        orbits = feasible_orbits(nodes)
        orbit_index = {orbit: index for index, orbit in enumerate(orbits)}
        nu = [Q(0) for _ in orbits]
        for item in data["triple_counts"]:
            nu[orbit_index[tuple(item["types"])]] = Q(
                6 * item["count"], N
            )
    return nodes, alpha, orbits, tuple(nu)


def row_slack(row, alpha, nu):
    left = sum(
        Q(coefficient) * weight
        for coefficient, weight in zip(row["nu_coefficients"], nu)
    )
    right = Q(3 * row["capacity"]) * sum(
        alpha[index] for index in row["alpha_indices"]
    )
    return right - left


def audit(path: Path) -> dict[str, object]:
    nodes, alpha, orbits, nu = load_source(path)
    stratified = stratified_capacity_rows(nodes, orbits)
    evaluated = [(row_slack(row, alpha, nu), row) for row in stratified]
    minimum, row = min(evaluated, key=lambda item: item[0])
    negative_singletons = [
        {
            "base": qstr(candidate["lower"]),
            "high": qstr(candidate["high"]),
            "p": None
            if candidate["p"] is None
            else qstr(candidate["p"]),
            "capacity": candidate["capacity"],
            "normalized_slack": qstr(slack),
            "unordered_count_scale_slack": qstr(Q(N, 6) * slack),
        }
        for slack, candidate in evaluated
        if slack < 0 and candidate["lower"] == candidate["upper"]
    ]

    weighted_results = []
    for weighted in weighted_capacity_rows(nodes, orbits):
        left = sum(
            Q(coefficient) * weight
            for coefficient, weight in zip(
                weighted["nu_coefficients"], nu
            )
        )
        right = Q(3) * sum(
            Q(capacity) * alpha[index]
            for index, capacity in weighted["capacities"].items()
        )
        weighted_results.append((right - left, weighted["high"]))
    weighted_minimum, weighted_high = min(weighted_results)
    return {
        "source": path.name,
        "stratified_row_count": len(stratified),
        "minimum_stratified_slack_normalized": qstr(minimum),
        "minimum_stratified_slack_unordered_count_scale": qstr(
            Q(N, 6) * minimum
        ),
        "minimum_stratified_row": {
            "lower": qstr(row["lower"]),
            "upper": qstr(row["upper"]),
            "high": qstr(row["high"]),
            "p": None if row["p"] is None else qstr(row["p"]),
            "capacity": row["capacity"],
        },
        "passes_all_stratified_rows": minimum >= 0,
        "negative_singleton_strata": negative_singletons,
        "minimum_weighted_slack_normalized": qstr(weighted_minimum),
        "minimum_weighted_high": qstr(weighted_high),
        "passes_all_weighted_rows": weighted_minimum >= 0,
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    sources = (
        project_root
        / "certificates"
        / "fixed41_bv_fullradial_k16_pseudodistribution.json",
        project_root
        / "certificates"
        / "common_pair_capacity_degree4_pseudodistribution.json",
    )
    result = {
        "schema": "corrected-stratified-capacity-barrier-audit-v1",
        "arithmetic": "fractions.Fraction only",
        "sources": [audit(path) for path in sources],
        "conclusion": (
            "Both imported pseudo-objects fail corrected universal capacity "
            "cuts; this does not preclude reoptimization of their pair data"
        ),
    }
    output = Path(__file__).resolve().parent / "results" / (
        "corrected_capacity_barrier_audit.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
