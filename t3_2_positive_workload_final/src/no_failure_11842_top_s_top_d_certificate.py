"""Exact top-S/top-D identity for the 11,842 no-failure pairs.

The corrected S-tier superlevel cut may in general live below a wholly
disabled global top D-tier.  The elementary global-top-D domination
argument used by the accompanying population fourth-power proof therefore
needs the stronger statement that its source is in the literal global top
D-tier.  (The full Anderson--Kim theorem itself has a broader hypothesis.)
This module certifies that stronger finite identity for the exact
11,842-pair family only.

No orientation, rate vector, population state, stochastic history, or
communicating class is enumerated here, and this module makes no recurrence
claim.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import global_tier_interface as tier
import outside_mixed_remaining_18496_certificate as remainder
import s_tier_superlevel_interface as superlevel
import stoichiometric_gate_feasibility as feasibility


EXPECTED_DEPENDENCY_SHA256 = {
    "outside_mixed_remaining_18496_certificate.py": (
        "314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63"
    ),
    "global_tier_interface.py": (
        "b8feae08c2eecf21b6e4e387eeaa6f5b15f32d862fca5324d4523c38872494ab"
    ),
    "s_tier_superlevel_interface.py": (
        "1a4e27fcf40af76cac6281f8830b7644bf086b3c05d97a963ce9f5bac736ad57"
    ),
    "stoichiometric_gate_feasibility.py": (
        "4602e7d31af02c26cc9785ed056c876e3e571e428ad974e861e4940b9edba9a1"
    ),
}

# Filled from the canonical payload after the first deterministic replay.
EXPECTED_FEASIBLE_INCIDENCE_SHA256 = (
    "a965d56c3b116a603ae147ad9bf22450c5cec9fb81477a3f99366920a0482ec8"
)
EXPECTED_TOP_IDENTITY_SHA256 = (
    "8f83a44a578f45597ea968c551d5dcdbba5a529833ba9eea01e14f1179af6bf5"
)


def dependency_sha256() -> dict[str, str]:
    source_directory = Path(__file__).resolve().parent
    return {
        filename: sha256((source_directory / filename).read_bytes()).hexdigest()
        for filename in EXPECTED_DEPENDENCY_SHA256
    }


def _incidence_payload(
    pair: remainder.Pair,
    descriptor: remainder.Descriptor,
) -> dict[str, object]:
    top_d, top_s = tier.tier_sets(pair, descriptor)
    return {
        "pair": remainder.closure.pair_payload(pair),
        "partition": descriptor.partition,
        "active_mask": descriptor.active_mask,
        "caps": descriptor.caps,
        "weight": descriptor.weight,
        "top_d": sorted(top_d),
        "top_s": sorted(top_s),
    }


def _digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def feasible_incidences():
    """Yield the canonical incidence order without materializing 3M rows."""

    pairs = sorted(
        remainder.no_failure_pairs(),
        key=remainder.closure.pair_payload,
    )
    descriptors = sorted(
        tier.tier_descriptors(),
        key=lambda descriptor: (
            descriptor.weight,
            descriptor.caps,
            descriptor.active_mask,
            descriptor.partition,
        ),
    )
    for pair in pairs:
        for descriptor in descriptors:
            if feasibility.descriptor_feasible(pair, descriptor):
                yield pair, descriptor


def certificate() -> dict[str, object]:
    dependencies = dependency_sha256()
    feasible_digest = sha256()
    feasible_digest.update(b"[")
    row_count = 0
    corrected_failure_count = 0
    empty_top_s_count = 0
    below_top_d_count = 0
    active_counts: Counter[int] = Counter()
    top_s_sizes: Counter[int] = Counter()

    for pair, descriptor in feasible_incidences():
        if row_count:
            feasible_digest.update(b",")
        feasible_digest.update(
            json.dumps(
                _incidence_payload(pair, descriptor),
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        )
        row_count += 1
        top_d, top_s = tier.tier_sets(pair, descriptor)
        active_counts[descriptor.active_mask.bit_count()] += 1
        top_s_sizes[len(top_s)] += 1
        if not superlevel.universal_strong_orientation_condition(pair, descriptor):
            corrected_failure_count += 1
        if not top_s:
            empty_top_s_count += 1
        if not top_s <= top_d:
            below_top_d_count += 1
    feasible_digest.update(b"]")
    feasible_incidence_sha256 = feasible_digest.hexdigest()

    identity_payload = {
        "pair_sha256": remainder.closure.pair_fingerprint(
            remainder.no_failure_pairs()
        ),
        "feasible_incidences": row_count,
        "corrected_failures": corrected_failure_count,
        "empty_top_s": empty_top_s_count,
        "top_s_not_subset_top_d": below_top_d_count,
        "active_count_histogram": dict(sorted(active_counts.items())),
        "top_s_size_histogram": dict(sorted(top_s_sizes.items())),
    }

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(remainder.no_failure_pairs()) == 11_842
    assert not corrected_failure_count
    assert not empty_top_s_count
    assert not below_top_d_count
    assert feasible_incidence_sha256 == EXPECTED_FEASIBLE_INCIDENCE_SHA256
    assert _digest(identity_payload) == EXPECTED_TOP_IDENTITY_SHA256

    return {
        "claim_scope": (
            "finite pair/descriptor/affine identity only; no orientation, "
            "rate, population, history, class, or recurrence claim"
        ),
        "dependency_sha256": dependencies,
        "pairs": len(remainder.no_failure_pairs()),
        "pair_sha256": remainder.closure.pair_fingerprint(
            remainder.no_failure_pairs()
        ),
        "feasible_incidences": row_count,
        "feasible_incidence_sha256": feasible_incidence_sha256,
        "corrected_cut_failures": corrected_failure_count,
        "empty_top_s": empty_top_s_count,
        "top_s_not_subset_global_top_d": below_top_d_count,
        "active_count_histogram": dict(sorted(active_counts.items())),
        "top_s_size_histogram": dict(sorted(top_s_sizes.items())),
        "top_identity_sha256": _digest(identity_payload),
        "orientation_rate_population_or_history_enumeration": False,
        "recurrence_claim": False,
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
