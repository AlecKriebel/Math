"""Exact AA identity for every feasible two-active remainder descriptor.

The 18,496 outside-mixed remainder was selected before looking at any
orientation, rate vector, population state, stochastic history, or
communicating class.  This module performs one further finite geometric
check: every affine-feasible descriptor with exactly two active coordinates
classifies both linkage supports as available (Q, U, or C) under the frozen
ordered Q/U/C/S classifier.

This is a support/descriptor identity only.  In particular, it does not
enumerate directed orientations or prove a stochastic recurrence theorem.
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

# Filled from the canonical streaming encodings after deterministic replay.
EXPECTED_FEASIBLE_INCIDENCE_SHA256 = (
    "a4c4aa42dadabe7e73d46a690f29fe1d457bf57c5bece422b8c0a3fafe72eb99"
)
EXPECTED_IDENTITY_SHA256 = (
    "bc9195d09dc8717381486ae114fcd59e22786c729d957fe209ceac432deaaac8"
)


def dependency_sha256() -> dict[str, str]:
    source_directory = Path(__file__).resolve().parent
    return {
        filename: sha256((source_directory / filename).read_bytes()).hexdigest()
        for filename in EXPECTED_DEPENDENCY_SHA256
    }


def _row_payload(pair, descriptor) -> dict[str, object]:
    kinds = remainder.linkage_kinds(pair, descriptor)
    return {
        "pair": remainder.closure.pair_payload(pair),
        "partition": descriptor.partition,
        "active_mask": descriptor.active_mask,
        "caps": descriptor.caps,
        "weight": descriptor.weight,
        "ordered_linkage_kinds": kinds,
        "corrected_cut_passes": (
            superlevel.universal_strong_orientation_condition(pair, descriptor)
        ),
    }


def _digest(payload: object) -> str:
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def feasible_two_active_incidences():
    """Yield the canonical feasible two-active incidence order."""

    pairs = sorted(
        remainder.remainder_pairs(),
        key=remainder.closure.pair_payload,
    )
    descriptors = sorted(
        (
            descriptor
            for descriptor in tier.tier_descriptors()
            if descriptor.active_mask.bit_count() == 2
        ),
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


def certificate(*, enforce_fingerprints: bool = True) -> dict[str, object]:
    dependencies = dependency_sha256()
    incidence_digest = sha256()
    incidence_digest.update(b"[")

    rows = 0
    unavailable_rows = 0
    pass_rows = 0
    failure_rows = 0
    active_masks: Counter[int] = Counter()
    kind_histogram: Counter[str] = Counter()
    ordered_kind_histogram: Counter[str] = Counter()
    pair_set = set()

    for pair, descriptor in feasible_two_active_incidences():
        if rows:
            incidence_digest.update(b",")
        incidence_digest.update(
            json.dumps(
                _row_payload(pair, descriptor),
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        )
        rows += 1
        pair_set.add(pair)
        active_masks[descriptor.active_mask] += 1
        kinds = remainder.linkage_kinds(pair, descriptor)
        kind_histogram["/".join(sorted(kinds))] += 1
        ordered_kind_histogram["/".join(kinds)] += 1
        unavailable_rows += int(any(kind not in {"Q", "U", "C"} for kind in kinds))
        if superlevel.universal_strong_orientation_condition(pair, descriptor):
            pass_rows += 1
        else:
            failure_rows += 1

    incidence_digest.update(b"]")
    feasible_incidence_sha256 = incidence_digest.hexdigest()

    identity_payload = {
        "remainder_pair_sha256": remainder.EXPECTED_REMAINDER_PAIR_SHA256,
        "pairs_with_feasible_two_active_descriptor": len(pair_set),
        "pair_sha256": remainder.closure.pair_fingerprint(pair_set),
        "feasible_two_active_incidences": rows,
        "corrected_cut_passes": pass_rows,
        "corrected_cut_failures": failure_rows,
        "unavailable_linkage_rows": unavailable_rows,
        "active_mask_histogram": dict(sorted(active_masks.items())),
        "unordered_kind_histogram": dict(sorted(kind_histogram.items())),
        "ordered_kind_histogram": dict(sorted(ordered_kind_histogram.items())),
    }
    identity_sha256 = _digest(identity_payload)

    assert dependencies == EXPECTED_DEPENDENCY_SHA256
    assert len(remainder.remainder_pairs()) == 18_496
    assert rows == pass_rows + failure_rows
    assert failure_rows == 3_084
    assert unavailable_rows == 0
    if enforce_fingerprints:
        assert feasible_incidence_sha256 == EXPECTED_FEASIBLE_INCIDENCE_SHA256
        assert identity_sha256 == EXPECTED_IDENTITY_SHA256

    return {
        "claim_scope": (
            "finite support/descriptor/affine identity only; no orientation, "
            "rate, population, history, class, or recurrence claim"
        ),
        "dependency_sha256": dependencies,
        **identity_payload,
        "feasible_incidence_sha256": feasible_incidence_sha256,
        "identity_sha256": identity_sha256,
        "orientation_rate_population_or_history_enumeration": False,
        "recurrence_claim": False,
    }


def main() -> None:
    print(json.dumps(certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
