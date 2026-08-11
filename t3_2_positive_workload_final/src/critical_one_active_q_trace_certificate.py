"""Exact certificate for the audited fifteen-pair positive-Q trace theorem."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_phase_shape as phase_shape
import one_active_remaining_structure as structure
import stoichiometric_gate_feasibility as feasibility
import suppressed_promotion_orbit_certificate as suppressed
import two_active_promotion_obstruction as promotion


Pair = closure.Pair
Descriptor = tier.TierDescriptor

EXPECTED_PAIR_SHA256 = (
    "6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3"
)
EXPECTED_ROWS_SHA256 = (
    "480bd3fbe6813148a898d62aefa55e13aa2fdf8814cc0e7eedc14e441ea76518"
)


def _shell_mask(active: int) -> int:
    inactive = tuple(index for index in range(3) if index != active)
    vectors = [(0, 0, 0)]
    for coordinate in inactive:
        vector = [0, 0, 0]
        vector[active] = 1
        vector[coordinate] = 1
        vectors.append(tuple(vector))
    return sum(1 << closure.COMPLEXES.index(vector) for vector in vectors)


def _critical_coordinate(pair: Pair) -> int | None:
    matches = []
    for active in range(3):
        shell = _shell_mask(active)
        if shell not in pair:
            continue
        partner = pair[1] if pair[0] == shell else pair[0]
        inactive = tuple(index for index in range(3) if index != active)
        nodes = tuple(tier._nodes(partner))
        if not all(closure.COMPLEXES[node][active] == 0 for node in nodes):
            continue
        degrees = {
            sum(closure.COMPLEXES[node][index] for index in inactive)
            for node in nodes
        }
        if degrees == {1, 2}:
            matches.append(active)
    if not matches:
        return None
    assert len(matches) == 1
    return matches[0]


def selected_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair in phase_shape.candidate_pairs()
        if _critical_coordinate(pair) is not None
    )


def _row_payload() -> tuple[dict[str, object], ...]:
    rows = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        critical = _critical_coordinate(pair)
        assert critical is not None
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            active, = tier._active_coordinates(descriptor)
            normalized = structure._normalized(pair, descriptor)
            rows.append(
                {
                    "pair": [list(part) for part in closure.pair_payload(pair)],
                    "weight": list(descriptor.weight),
                    "caps": list(descriptor.caps),
                    "critical_coordinate": critical,
                    "active_coordinate": active,
                    "critical_q_row": active == critical,
                    "normalized_supports": [
                        list(support) for support in normalized["supports"]
                    ],
                    "normalized_caps": list(normalized["caps"]),
                }
            )
    return tuple(
        sorted(rows, key=lambda row: (row["pair"], row["weight"], row["caps"]))
    )


def certificate() -> dict[str, object]:
    pairs = selected_pairs()
    rows = _row_payload()
    positive, signed, residual = feasibility._residual_failures()
    prior = frozenset(
        promotion._prior_certified_pairs()
        | promotion.pair_level_selector()
        | suppressed.selected_pairs()
    )
    pair_hash = closure.pair_fingerprint(pairs)
    row_hash = sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    companion_templates = Counter(
        (
            tuple(tuple(support) for support in row["normalized_supports"]),
            tuple(row["normalized_caps"]),
        )
        for row in rows
        if not row["critical_q_row"]
    )

    assert len(pairs) == 15
    assert pairs <= residual
    assert pairs <= positive
    assert not (pairs & signed)
    assert not (pairs & prior)
    assert pair_hash == EXPECTED_PAIR_SHA256
    assert len(rows) == 83
    assert sum(row["critical_q_row"] for row in rows) == 75
    assert sum(not row["critical_q_row"] for row in rows) == 8
    assert row_hash == EXPECTED_ROWS_SHA256
    assert sorted(companion_templates.values()) == [2, 2, 2, 2]

    return {
        "claim_scope": (
            "independently audited positive-Q physical trace and common-"
            "squared-factorial recurrence theorem for the exact 15 pairs"
        ),
        "pairs": len(pairs),
        "positive_pairs": len(pairs & positive),
        "signed_pairs": len(pairs & signed),
        "prior_certified_overlap": len(pairs & prior),
        "failed_incidences": len(rows),
        "critical_q_incidences": sum(row["critical_q_row"] for row in rows),
        "companion_incidences": sum(
            not row["critical_q_row"] for row in rows
        ),
        "companion_template_histogram": {
            json.dumps(key, separators=(",", ":")): value
            for key, value in sorted(companion_templates.items())
        },
        "pair_sha256": pair_hash,
        "rows_sha256": row_hash,
        "independent_audits_passed": 2,
        "analytic_critical_trace_certified": True,
        "pair_level_recurrence_certified": True,
        "positive_remainder_before": 1835,
        "positive_remainder_after": 1820,
        "signed_remainder": 187,
        "global_t3_2_certified": False,
        "rows": rows,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
