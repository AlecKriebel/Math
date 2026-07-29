#!/usr/bin/env python3
"""Audit the frozen-H4 numerical search archive and gradient formulas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import d6_one_sided_fixed_h4_leakage_target_search as target_search
import d6_one_sided_fixed_h4_search as fixed_search
import d6_riemannian_search as old_search


BASE_HASH = "2efa4484dc0604347b153c92f9946ebd070b247a67a3896e4d130cb2b4968e57"
TARGET_HASH = "b4720ed3f2e007ad3e2f556f1aec501a0f193f95b506c9233748df140e49f92f"


def jsonl(path: str) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (ROOT / path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def starts_and_finals(
    path: str,
) -> tuple[dict[int, dict[str, object]], dict[str, dict[str, object]]]:
    records = jsonl(path)
    starts = {
        int(record["seed"]): record
        for record in records
        if record["event"] == "start"
    }
    finals = {
        str(record["run_id"]): record
        for record in records
        if record["event"] == "final"
    }
    return starts, finals


def verify_archive_group(
    path: str,
    seeds: set[int],
    script_hash: str,
) -> list[dict[str, object]]:
    starts, finals_by_id = starts_and_finals(path)
    assert set(starts) == seeds
    finals: list[dict[str, object]] = []
    for seed in sorted(seeds):
        start = starts[seed]
        assert start["script_sha256"] == script_hash
        run_id = str(start["run_id"])
        assert run_id in finals_by_id
        final = finals_by_id[run_id]
        assert final["fixed_h4_error"] == 0.0
        assert float(final["hermiticity_error"]) < 1e-12
        assert float(final["involution_error"]) < 1e-12
        assert float(final["residual_frobenius"]) > 1e-6
        finals.append(final)
    return finals


def verify_old_search_was_not_frozen() -> None:
    labels = old_search.pair_labels(6, "one_sided_4plus2")
    rng = np.random.default_rng(26073160)
    h = old_search.random_unitary_involution(
        6, labels, rng, "complex", "h4_block"
    )
    problem = old_search.ResidualProblem(6, labels, "complex", 0.0)

    direction = np.zeros((36, 36), dtype=np.complex128)
    fixed_indices = np.asarray(
        [6 * first + second for first in range(4) for second in range(4)]
    )
    diagonal = np.diag(np.arange(1.0, 17.0))
    direction[np.ix_(fixed_indices, fixed_indices)] = diagonal
    tangent = problem.tangent_projection(direction, h)
    fixed_tangent = tangent[np.ix_(fixed_indices, fixed_indices)]
    assert np.linalg.norm(fixed_tangent) > 1e-3


def central_gradient_error(
    complement: np.ndarray,
    analytic_gradient: np.ndarray,
    value_function,
    seed: int,
    field: str,
) -> float:
    rng = np.random.default_rng(seed)
    ambient = rng.normal(size=(36, 36))
    if field == "complex":
        ambient = ambient + 1j * rng.normal(size=(36, 36))
    direction = fixed_search.complement_tangent(
        ambient, complement, field
    )
    direction /= np.linalg.norm(direction)
    generator = (direction @ complement - complement @ direction) / 4.0
    epsilon = 1e-4
    plus_unitary = expm(epsilon * generator)
    minus_unitary = expm(-epsilon * generator)
    plus = plus_unitary @ complement @ plus_unitary.conj().T
    minus = minus_unitary @ complement @ minus_unitary.conj().T
    quotient = (value_function(plus) - value_function(minus)) / (
        2.0 * epsilon
    )
    analytic = float(np.vdot(analytic_gradient, direction).real)
    return abs(quotient - analytic)


def verify_gradients() -> tuple[float, float]:
    rng = np.random.default_rng(26073100)
    complement = fixed_search.random_complement(rng, "complex")
    _, gradient, _, _ = fixed_search.value_gradient(
        complement, "complex", 0.0
    )
    base_error = central_gradient_error(
        complement,
        gradient,
        lambda trial: fixed_search.value_gradient(
            trial, "complex", 0.0, need_gradient=False
        ),
        26073161,
        "complex",
    )

    target_complement = fixed_search.random_complement(
        np.random.default_rng(26073150), "complex"
    )
    _, target_gradient, _, _, _ = target_search.value_gradient(
        target_complement, "complex", 0.25, 1000.0
    )
    target_error = central_gradient_error(
        target_complement,
        target_gradient,
        lambda trial: target_search.value_gradient(
            trial,
            "complex",
            0.25,
            1000.0,
            need_gradient=False,
        ),
        26073162,
        "complex",
    )
    assert base_error < 1e-6
    assert target_error < 1e-6
    return base_error, target_error


def main() -> None:
    verify_old_search_was_not_frozen()
    print("PASS old one_sided_4plus2 tangent moved the published WW block")

    complex_finals = verify_archive_group(
        "results/d6_fixed_h4_complex_runs.jsonl",
        set(range(26073110, 26073116)),
        BASE_HASH,
    )
    leakage_finals = verify_archive_group(
        "results/d6_fixed_h4_leakage_start_runs.jsonl",
        {26073120},
        BASE_HASH,
    )
    penalty_finals = verify_archive_group(
        "results/d6_fixed_h4_pt10_runs.jsonl",
        {26073130, 26073131, 26073132},
        BASE_HASH,
    )
    real_finals = verify_archive_group(
        "results/d6_fixed_h4_real_runs.jsonl",
        {26073140, 26073141},
        BASE_HASH,
    )
    target_finals = verify_archive_group(
        "results/d6_fixed_h4_leakage_target_runs.jsonl",
        {26073151, 26073152, 26073153},
        TARGET_HASH,
    )

    assert max(float(final["delta_coupling"]) for final in complex_finals) < 1e-12
    assert min(float(final["delta_coupling"]) for final in target_finals) > 0.17
    assert min(float(final["residual_frobenius"]) for final in complex_finals) == (
        6.011210894660647
    )
    assert min(float(final["residual_frobenius"]) for final in target_finals) == (
        6.284217255318515
    )
    assert len(leakage_finals) == 1
    assert len(penalty_finals) == 3
    assert len(real_finals) == 2
    print("PASS 15 frozen-WW production runs and source hashes")
    print("PASS no residual below 6.011210894660647")
    print("PASS leakage-target runs retain delta>0.17 but residual>=6.284217255318515")

    base_error, target_error = verify_gradients()
    print(f"PASS base central-gradient error {base_error:.3e}")
    print(f"PASS target central-gradient error {target_error:.3e}")
    print("All frozen-H4 numerical archive checks passed.")


if __name__ == "__main__":
    main()
