#!/usr/bin/env python3
"""Independent replay of the orbit-2 first lift and eighteen quadrics."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from random import Random
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_orbit2_digit2_sat as orbit2  # noqa: E402


EXPECTED = {
    "origin": "760792d304ea71d5a6d12ed4e60f45f2f2ef3441362d1696664a158b14ba1f3d",
    "basis": "4d7a1a942b31aeba0cb15fd24e74002cadd2b8b6fdaffbee33e22fec55bb9764",
    "constants": "bb206d433d4a403395e03557bd4fe29c2988b6a025834fc4df5960c9594e2ffa",
    "linears": "d620d9c6db27fa3aaf5f27e8635ee39bb76f546b73f793d6b812438d0aad1fef",
    "polars": "1da28b8b0acc8074650bb4cd83949a018c6931f8c682c29c52807338c814f239",
}


def digest(value: object) -> str:
    payload = json.dumps(
        value, separators=(",", ":"), sort_keys=True
    ).encode()
    return sha256(payload).hexdigest()


def rank_mod3(matrix) -> int:
    work = np.array(matrix, dtype=np.int16) % 3
    row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        work[row] = (
            work[row] * (1 if work[row, column] == 1 else 2)
        ) % 3
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] = (
                    work[other]
                    - work[other, column] * work[row]
                ) % 3
        row += 1
        if row == work.shape[0]:
            break
    return row


def evaluate(constant, linear, polar, point) -> int:
    return (
        int(constant)
        + sum(int(a) * int(b) for a, b in zip(linear, point))
        + 2
        * sum(
            int(point[left])
            * int(polar[left][right])
            * int(point[right])
            for left in range(36)
            for right in range(36)
        )
    ) % 3


def verify() -> dict:
    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = orbit2.exact_forms()
    assert digest(origin) == EXPECTED["origin"]
    assert digest(basis) == EXPECTED["basis"]
    assert digest(constants) == EXPECTED["constants"]
    assert digest(linears) == EXPECTED["linears"]
    assert digest(polars) == EXPECTED["polars"]
    assert constants == (2, 1, 2, 0, 1, 0, 1, 0, 2, 2, 1, 0, 2, 2, 0, 0, 2, 0)
    assert len(basis) == 36
    assert all(
        polars[equation][left][right]
        == polars[equation][right][left]
        for equation in range(18)
        for left in range(36)
        for right in range(36)
    )
    polar_ranks = tuple(rank_mod3(matrix) for matrix in polars)
    assert polar_ranks.count(35) == 7
    assert polar_ranks.count(36) == 11
    flattened = tuple(
        tuple(
            polars[equation][left][right]
            for left in range(36)
            for right in range(left, 36)
        )
        for equation in range(18)
    )
    assert rank_mod3(flattened) == 18

    rng = Random(668_202_018)
    for _ in range(64):
        point = tuple(rng.randrange(3) for _ in range(36))
        algebraic = tuple(
            evaluate(
                constants[equation],
                linears[equation],
                polars[equation],
                point,
            )
            for equation in range(18)
        )
        placement = orbit2.second.lift_affine_point(
            origin, basis, point
        )
        physical = orbit2.second.symbolic_second_digits(
            orbit2.second.second_digit_term_data(profiles), placement
        )
        assert physical[0] == physical[7] == 0
        assert algebraic == tuple(
            physical[index] for index in orbit2.ACTIVE_ROWS
        )

    certificate = json.loads(
        (HERE / "DEFECT1_CERTIFICATE.json").read_text()
    )
    point = tuple(map(int, certificate["affine_coordinates"]))
    placement = orbit2.second.lift_affine_point(origin, basis, point)
    assert list(placement) == certificate["placement_trits"]
    assert digest(placement) == certificate["placement_trits_sha256"]
    first = orbit2.second.symbolic_first_digits(
        orbit2.first_digit_equations(profiles), placement
    )
    symbolic = orbit2.second.symbolic_second_digits(
        orbit2.second.second_digit_term_data(profiles), placement
    )
    direct = orbit2.second.direct_second_digits(profiles, placement)
    assert first == (0,) * 20
    assert list(symbolic) == certificate["full_second_digit_residuals"]
    assert direct == symbolic

    active_values = np.array(
        [symbolic[index] for index in orbit2.ACTIVE_ROWS],
        dtype=np.int16,
    )
    jacobian = (
        np.array(linears, dtype=np.int16)
        + np.einsum(
            "eij,j->ei",
            np.array(polars, dtype=np.int16),
            np.array(point, dtype=np.int16),
        )
    ) % 3
    assert rank_mod3(jacobian) == 18
    assert rank_mod3(jacobian[active_values == 0]) == 17

    local = certificate["exact_local_ball"]
    assert sum(local["sphere_counts"]) == local["points_tested"]
    expected_spheres = [
        1,
        36 * 2,
        630 * 4,
        7140 * 8,
        58905 * 16,
        376992 * 32,
        1947792 * 64,
    ]
    assert local["sphere_counts"] == expected_spheres
    assert local["status"] == "UNSAT_IN_BALL"
    return {
        "first_layer_rank": 18,
        "first_layer_nullity": 36,
        "active_quadrics": 18,
        "polar_rank_histogram": {35: 7, 36: 11},
        "polar_span_rank": 18,
        "random_direct_replays": 64,
        "pinned_defect": 1,
        "failed_full_row": 10,
        "jacobian_rank": 18,
        "satisfied_row_jacobian_rank": 17,
        "exact_local_radius": local["radius"],
        "exact_local_points": local["points_tested"],
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
    print("PASS: orbit-2 quadrics and defect-one local exclusion replayed")
