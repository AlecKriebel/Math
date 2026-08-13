"""Exact finite certificate for the raw shielded/shielded 446 branch.

This module proves only a support--workload incidence identity.  It does not
enumerate reaction orientations, rates, population states, or histories, and
it proves no stochastic estimate.  The analytic invariant, deficiency-zero,
and signed-service arguments are recorded separately in
``research_notes/proof_first_raw_ss446_invariant_dz_service_composition.md``.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import exact_shielded_seam as seam
import global_atlas_interface_closure as closure


Vector = seam.Vector
Pair = closure.Pair
Incidence = tuple[Vector, int, int]

FULL_MASK = (1 << len(seam.NAMES)) - 1


def _incidence_sort_key(row: Incidence) -> tuple[object, ...]:
    weight, first, second = row
    return weight, closure.support(first), closure.support(second)


@lru_cache(maxsize=1)
def raw_ss_incidences() -> tuple[Incidence, ...]:
    """All ordered SS incidences for the four frozen workload cells."""

    rows: list[Incidence] = []
    for weight in seam.WORKLOADS:
        for first in range(1, FULL_MASK + 1):
            if first.bit_count() < 2:
                continue
            if not seam.classify_shielded(first, weight):
                continue
            available = FULL_MASK ^ first
            second = available
            while second:
                if (
                    second.bit_count() >= 2
                    and seam.classify_shielded(second, weight)
                ):
                    rows.append((weight, first, second))
                second = (second - 1) & available
    return tuple(sorted(rows, key=_incidence_sort_key))


def branch(pair: Pair) -> str:
    """The disjoint analytic branch priority for one raw SS support pair."""

    first, second = pair
    if closure.has_strictly_positive_invariant(first, second):
        return "strict_positive_invariant"
    if closure.has_positive_active_invariant(first, second):
        return "active_chart_invariant"
    if closure.full_deficiency(first, second) == 0:
        return "full_deficiency_zero"
    if closure.is_signed_service_seam(pair):
        return "exact_signed_service"
    return "residual"


def incidence_fingerprint(*, annotated: bool) -> str:
    """Hash the sorted rows with an explicit canonical JSON schema."""

    payload: list[dict[str, object]] = []
    for weight, first, second in raw_ss_incidences():
        item: dict[str, object] = {
            "weight": weight,
            "first": closure.support(first),
            "second": closure.support(second),
        }
        if annotated:
            item["branch"] = branch((first, second))
        payload.append(item)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


@lru_cache(maxsize=1)
def certificate() -> dict[str, object]:
    """Return and internally verify the complete raw SS composition split."""

    rows = raw_ss_incidences()
    counts = Counter(branch((first, second)) for _, first, second in rows)
    assert counts == Counter(
        {
            "strict_positive_invariant": 18,
            "active_chart_invariant": 364,
            "full_deficiency_zero": 60,
            "exact_signed_service": 4,
        }
    )
    assert len(rows) == 446
    assert counts["residual"] == 0

    pairs = {(first, second) for _, first, second in rows}
    unique_counts = Counter(branch(pair) for pair in pairs)
    assert len(pairs) == 322
    assert unique_counts == Counter(
        {
            "strict_positive_invariant": 18,
            "active_chart_invariant": 268,
            "full_deficiency_zero": 32,
            "exact_signed_service": 4,
        }
    )

    per_weight = {
        weight: Counter(
            branch((first, second))
            for row_weight, first, second in rows
            if row_weight == weight
        )
        for weight in seam.WORKLOADS
    }
    assert per_weight == {
        (1, 1, 0): Counter(
            {
                "strict_positive_invariant": 18,
                "active_chart_invariant": 230,
                "full_deficiency_zero": 14,
            }
        ),
        (2, 3, 0): Counter(
            {
                "active_chart_invariant": 28,
                "full_deficiency_zero": 10,
            }
        ),
        (1, 2, 0): Counter(
            {
                "active_chart_invariant": 66,
                "full_deficiency_zero": 14,
            }
        ),
        (1, 3, 0): Counter(
            {
                "active_chart_invariant": 40,
                "full_deficiency_zero": 22,
                "exact_signed_service": 4,
            }
        ),
    }

    service_rows = tuple(
        row
        for row in rows
        if branch((row[1], row[2])) == "exact_signed_service"
    )
    expected_service_payload = (
        ((1, 3, 0), ("C", "2C"), ("0", "A", "2A", "BC")),
        ((1, 3, 0), ("0", "C", "2C"), ("A", "2A", "BC")),
        ((1, 3, 0), ("A", "2A", "BC"), ("0", "C", "2C")),
        ((1, 3, 0), ("0", "A", "2A", "BC"), ("C", "2C")),
    )
    service_payload = tuple(
        (weight, closure.support(first), closure.support(second))
        for weight, first, second in service_rows
    )
    assert set(service_payload) == set(expected_service_payload)
    assert all(
        closure.full_deficiency(first, second) == 1
        for _, first, second in service_rows
    )

    raw_hash = incidence_fingerprint(annotated=False)
    annotated_hash = incidence_fingerprint(annotated=True)
    assert raw_hash == (
        "842920b5280d96c96e49e0b0b959d548acb2ac43a5dfee4ab110346958acc45f"
    )
    assert annotated_hash == (
        "8870e74f85a50608b2f5586c87a3dc73cf825ae292df41063b77ebae7e1924e3"
    )

    return {
        "claim_scope": (
            "finite raw SS support-workload set identity only; analytic "
            "branches are proved separately"
        ),
        "raw_ss_incidences": len(rows),
        "distinct_ordered_support_pairs": len(pairs),
        "incidence_branch_counts": dict(sorted(counts.items())),
        "unique_pair_branch_counts": dict(sorted(unique_counts.items())),
        "per_weight_branch_counts": {
            ",".join(map(str, weight)): dict(sorted(weight_counts.items()))
            for weight, weight_counts in per_weight.items()
        },
        "service_rows": [
            {
                "weight": list(weight),
                "first": list(closure.support(first)),
                "second": list(closure.support(second)),
            }
            for weight, first, second in service_rows
        ],
        "raw_incidence_sha256": raw_hash,
        "branch_annotated_incidence_sha256": annotated_hash,
        "residual_incidences": counts["residual"],
    }


def self_test() -> None:
    certificate()


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
