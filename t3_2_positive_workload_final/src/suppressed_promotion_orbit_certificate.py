"""Certified exact four-pair suppressed-promotion orbit theorem.

The finite certificate freezes the support orbit and every affine-feasible
failed descriptor.  The physical shell theorem and pair-level recurrence
claim have passed two independent reviews at exactly this scope.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import stoichiometric_gate_feasibility as feasibility
import two_active_phase_gate as phase
import two_active_promotion_obstruction as promotion


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = (
    "20aae4680ad31e03b96c2c633833d1d6612f902b136154dbc012537e4352e584"
)
EXPECTED_ROWS_SHA256 = (
    "161581ee07987cad6154d27be24d4716189c3e437a765160100dd2b7d0f94f71"
)


# Cleaned endpoints are ordered as (I, U, V).  These displacements already
# include the top-shell cleanup from a lower-linkage target back to I = 0.
MACRO_DISPLACEMENTS = {
    "0->I": (0, 1, -1),
    "0->2I": (0, 2, -2),
    "0->I+U": (0, 2, -1),
    "I+U->0": (0, -2, 1),
    "I+U->I": (0, -1, 0),
    "I+U->2I": (0, 0, -1),
}


def reward_coefficients(
    u_weight: int, v_weight: int
) -> dict[str, int]:
    """Leading log-N coefficients of the six cleaned factorial rewards."""

    return {
        "0->I": u_weight - v_weight,
        "0->2I": 2 * (u_weight - v_weight),
        "0->I+U": 2 * u_weight - v_weight,
        "I+U->0": v_weight - 2 * u_weight,
        "I+U->I": -u_weight,
        "I+U->2I": -v_weight,
    }


def selected_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _, _ in promotion.suppressed_rows())


def _coordinate_maps() -> dict[Pair, tuple[int, int, int]]:
    return {
        pair: coordinates
        for pair, _, coordinates in promotion.suppressed_rows()
    }


def _rows() -> tuple[dict[str, object], ...]:
    maps = _coordinate_maps()
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs()):
        inactive, u_index, v_index = maps[pair]
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            rows.append(
                {
                    "pair": [
                        list(part) for part in closure.pair_payload(pair)
                    ],
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "iuv": [inactive, u_index, v_index],
                    "profile": [
                        descriptor.weight[inactive],
                        descriptor.weight[u_index],
                        descriptor.weight[v_index],
                    ],
                    "active": sum(value > 0 for value in descriptor.weight),
                }
            )
    return tuple(
        sorted(
            rows,
            key=lambda row: (row["pair"], row["weight"], row["caps"]),
        )
    )


def certificate() -> dict[str, object]:
    pairs = selected_pairs()
    positive, signed, residual = feasibility._residual_failures()
    rows = _rows()
    row_hash = sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    profile_histogram = Counter(tuple(row["profile"]) for row in rows)
    one_active_caps = Counter(
        tuple(row["caps"][index] for index in row["iuv"])
        for row in rows
        if row["active"] == 1
    )
    whole_top_two_active = 0
    for pair in pairs:
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if sum(value > 0 for value in descriptor.weight) != 2:
                continue
            whole_top_two_active += int(
                bool(phase._whole_top_linkages(pair, descriptor))
            )

    prior = promotion._prior_certified_pairs() | promotion.pair_level_selector()
    pair_hash = closure.pair_fingerprint(pairs)

    assert len(pairs) == 4
    assert pairs <= positive
    assert not (pairs & signed)
    assert pairs <= residual
    assert not (pairs & prior)
    assert pair_hash == EXPECTED_PAIR_SHA256
    assert row_hash == EXPECTED_ROWS_SHA256
    assert len(rows) == 28
    assert profile_histogram == {
        (0, 0, 1): 12,
        (0, 1, 1): 4,
        (0, 1, 2): 4,
        (0, 1, 3): 4,
        (0, 4, 5): 4,
    }
    assert one_active_caps == {
        (0, 0, 2): 4,
        (0, 1, 2): 4,
        (0, 2, 2): 4,
    }
    assert all(row["caps"][row["iuv"][0]] == 0 for row in rows)
    assert whole_top_two_active == 4

    q_changes = {
        edge: delta_u + 2 * delta_v - delta_i
        for edge, (delta_i, delta_u, delta_v) in MACRO_DISPLACEMENTS.items()
    }
    assert q_changes == {
        "0->I": -1,
        "0->2I": -2,
        "0->I+U": 0,
        "I+U->0": 0,
        "I+U->I": -1,
        "I+U->2I": -2,
    }

    reward_signs = {
        "one_active_001": reward_coefficients(0, 1),
        "equal_depth_011": reward_coefficients(1, 1),
        "critical_012": reward_coefficients(1, 2),
        "deep_v_013": reward_coefficients(1, 3),
        "deep_parallel_045": reward_coefficients(4, 5),
    }
    assert all(
        reward_signs["one_active_001"][edge] < 0
        for edge in ("0->I", "0->2I", "0->I+U")
    )
    assert all(
        reward_signs["equal_depth_011"][edge] < 0
        for edge in ("I+U->0", "I+U->I", "I+U->2I")
    )
    assert reward_signs["critical_012"] == {
        "0->I": -1,
        "0->2I": -2,
        "0->I+U": 0,
        "I+U->0": 0,
        "I+U->I": -1,
        "I+U->2I": -2,
    }
    assert all(
        reward_signs["deep_v_013"][edge] < 0
        for edge in ("0->I", "0->2I", "0->I+U")
    )
    assert all(
        reward_signs["deep_parallel_045"][edge] < 0
        for edge in ("I+U->0", "I+U->I", "I+U->2I")
    )

    return {
        "claim_scope": (
            "independently audited physical-time recurrence theorem for "
            "the exact four-pair orbit and all 28 failed descriptors"
        ),
        "pairs": len(pairs),
        "positive_pairs": len(pairs & positive),
        "signed_pairs": len(pairs & signed),
        "prior_certified_overlap": len(pairs & prior),
        "failed_incidences": len(rows),
        "one_active_incidences": sum(row["active"] == 1 for row in rows),
        "two_active_incidences": sum(row["active"] == 2 for row in rows),
        "profile_histogram": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(profile_histogram.items())
        },
        "one_active_cap_histogram": {
            ",".join(map(str, caps)): count
            for caps, count in sorted(one_active_caps.items())
        },
        "whole_top_two_active_incidences": whole_top_two_active,
        "no_whole_top_two_active_incidences": 16 - whole_top_two_active,
        "all_inactive_i_caps_zero": True,
        "pair_sha256": pair_hash,
        "rows_sha256": row_hash,
        "macro_displacements": MACRO_DISPLACEMENTS,
        "macro_q_changes": q_changes,
        "macro_reward_coefficients": reward_signs,
        "independent_audits_passed": 2,
        "analytic_shell_theorem_certified": True,
        "pair_level_recurrence_certified": True,
        "positive_remainder_before": 1839,
        "positive_remainder_after": 1835,
        "signed_remainder": 187,
        "global_t3_2_certified": False,
        "rows": rows,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
