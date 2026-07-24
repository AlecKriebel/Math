#!/usr/bin/env python3
"""Independent exact/numerical checker for round-8 tight-frame artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

try:
    from . import checker
    from . import d5_basis_checker
    from . import optimize_untf
except ImportError:  # Support direct execution from this directory.
    import checker
    import d5_basis_checker
    import optimize_untf


RESULT_PATH = (
    Path(__file__).resolve().parent / "results" / "untf_optimization.json"
)
SEEDED_RESULT_PATH = (
    Path(__file__).resolve().parent
    / "results"
    / "seeded_untf_challenges.json"
)


def coordinate_hash(coordinates) -> str:
    encoded = json.dumps(
        coordinates, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def recompute_numerical_entry(entry: dict) -> tuple[np.ndarray, dict]:
    frame = np.asarray(entry["coordinates"], dtype=float)
    assert frame.shape == (41, 5)
    diagnostics = optimize_untf.frame_diagnostics(frame)
    assert abs(
        diagnostics["maximum_inner_product"]
        - entry["maximum_inner_product"]
    ) < 5e-15
    assert diagnostics["maximizing_pair"] == entry["maximizing_pair"]
    assert diagnostics["maximum_unit_norm_residual"] < 5e-13
    assert diagnostics["tight_frame_frobenius_residual"] < 5e-12
    return frame, diagnostics


def verify(result_path: Path = RESULT_PATH) -> dict[str, object]:
    cyclic = checker.verify()
    d5 = d5_basis_checker.verify()
    assert cyclic["feasible_pairs"] == 0
    assert cyclic["switchable_frequency_pairs"] == 0
    assert cyclic["odd_cycle_witnesses"] == 190
    assert d5["partition_into_eight_bases"] is False

    data = json.loads(result_path.read_text())
    assert data["schema"] == "numerical-untf-41x5-search-v1"
    assert data["status"] == "NUMERICAL EVIDENCE ONLY"
    assert data["seed"] == 528041
    assert len(data["union_starts"]) == 24
    assert len(data["general_starts"]) == 25
    assert len(data["polishing"]) == 3

    union, union_diagnostics = recompute_numerical_entry(data["best_union"])
    general, general_diagnostics = recompute_numerical_entry(
        data["best_general"]
    )
    assert 0.58 < union_diagnostics["maximum_inner_product"] < 0.61
    assert 0.52 < general_diagnostics["maximum_inner_product"] < 0.54
    assert general_diagnostics["maximum_inner_product"] < (
        union_diagnostics["maximum_inner_product"]
    )
    assert general_diagnostics["maximum_inner_product"] > 0.5

    # The structured result really is seven orthonormal bases followed by
    # one regular 5-simplex, to numerical roundoff.
    for group in range(7):
        basis = union[5 * group : 5 * (group + 1)]
        assert np.linalg.norm(basis @ basis.T - np.eye(5), ord="fro") < 2e-12
    simplex = union[35:]
    expected_simplex_gram = (
        np.eye(6) * 1.2 - np.ones((6, 6)) * 0.2
    )
    assert (
        np.linalg.norm(
            simplex @ simplex.T - expected_simplex_gram, ord="fro"
        )
        < 2e-12
    )

    seeded = json.loads(SEEDED_RESULT_PATH.read_text())
    assert seeded["schema"] == "seeded-untf-41x5-challenges-v1"
    assert seeded["status"] == "NUMERICAL EVIDENCE ONLY"
    assert seeded["seed"] == 528142
    assert len(seeded["records"]) == 19
    seeded_frame, seeded_diagnostics = recompute_numerical_entry(
        seeded["best"]
    )
    assert seeded_frame.shape == (41, 5)
    assert 0.52 < seeded_diagnostics["maximum_inner_product"] < 0.54
    assert seeded_diagnostics["maximum_inner_product"] > 0.5
    assert general_diagnostics["maximum_inner_product"] < (
        seeded_diagnostics["maximum_inner_product"]
    )

    return {
        "status": "PASS",
        "cyclic_pairs_checked": cyclic["pairs_checked"],
        "cyclic_feasible_pairs": cyclic["feasible_pairs"],
        "cyclic_switchable_pairs": cyclic["switchable_frequency_pairs"],
        "d5_partition_into_eight_bases": False,
        "best_union_maximum_inner_product": union_diagnostics[
            "maximum_inner_product"
        ],
        "best_general_maximum_inner_product": general_diagnostics[
            "maximum_inner_product"
        ],
        "best_general_unit_residual": general_diagnostics[
            "maximum_unit_norm_residual"
        ],
        "best_general_tight_residual": general_diagnostics[
            "tight_frame_frobenius_residual"
        ],
        "best_seeded_maximum_inner_product": seeded_diagnostics[
            "maximum_inner_product"
        ],
        "best_union_coordinate_sha256": coordinate_hash(
            data["best_union"]["coordinates"]
        ),
        "best_general_coordinate_sha256": coordinate_hash(
            data["best_general"]["coordinates"]
        ),
        "best_seeded_coordinate_sha256": coordinate_hash(
            seeded["best"]["coordinates"]
        ),
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
