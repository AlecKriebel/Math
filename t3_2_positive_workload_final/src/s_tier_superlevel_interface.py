"""Corrected symbolic S-tier-superlevel interface certificate.

This derivative module deliberately does not enumerate reaction orientations
or stochastic trajectories.  It checks only finite support, tier, and affine
stoichiometric identities.  The universal quantifier over arbitrary strongly
connected reaction graphs is discharged by the cut theorem proved in
``research_notes/s_tier_superlevel_cut_and_affine151_corrected.md``.

The legacy global-top-D cut is sufficient but is not necessary when the
global top D-tier is wholly disabled.  The exact cut uses, in each linkage,
the D-superlevel at the (unique) D-level occupied by the global top S-tier.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as legacy
import stoichiometric_gate_feasibility as affine


Pair = closure.Pair
TierDescriptor = legacy.TierDescriptor


def d_level_map(descriptor: TierDescriptor) -> dict[int, int]:
    """Map each complex to its D-tier index, with zero the highest tier."""

    return {
        node: level
        for level, block in enumerate(descriptor.partition)
        for node in block
    }


def s_tier_superlevel(
    pair: Pair,
    descriptor: TierDescriptor,
) -> tuple[frozenset[int], tuple[frozenset[int], frozenset[int]]]:
    """Return the top S-tier and its linkagewise D-superlevel sets.

    If the top S-tier is empty, both superlevel sets are empty.  Otherwise all
    top-S complexes occupy one D-tier.  The superlevel in a linkage consists
    of its complexes in that tier or any higher D-tier.
    """

    _, top_s = legacy.tier_sets(pair, descriptor)
    if not top_s:
        return top_s, (frozenset(), frozenset())
    levels = d_level_map(descriptor)
    s_level = levels[next(iter(top_s))]
    if any(levels[node] != s_level for node in top_s):
        raise AssertionError("the top S-tier must occupy one D-tier")
    superlevels = tuple(
        frozenset(
            node
            for node in legacy._nodes(mask)
            if levels[node] <= s_level
        )
        for mask in pair
    )
    return top_s, (superlevels[0], superlevels[1])


def universal_strong_orientation_condition(
    pair: Pair,
    descriptor: TierDescriptor,
) -> bool:
    """Exact symbolic cut test, with no orientation enumeration.

    Every strongly connected directed graph on both linkage supports has a
    D-descending reaction sourced in the global top S-tier exactly when some
    linkage has a nonempty proper S-level superlevel contained in that top
    S-tier.
    """

    top_s, superlevels = s_tier_superlevel(pair, descriptor)
    if not top_s:
        return False
    return any(
        upper and upper != nodes and upper <= top_s
        for mask, upper in zip(pair, superlevels)
        for nodes in (legacy._nodes(mask),)
    )


def tier_split(
    shielded_masks: frozenset[int],
) -> tuple[frozenset[Pair], frozenset[Pair]]:
    """Split residual pairs using the corrected universal cut criterion."""

    passed: set[Pair] = set()
    failed: set[Pair] = set()
    descriptors = legacy.tier_descriptors()
    for pair in closure.residual_pairs(shielded_masks):
        target = (
            passed
            if all(
                universal_strong_orientation_condition(pair, descriptor)
                for descriptor in descriptors
            )
            else failed
        )
        target.add(pair)
    return frozenset(passed), frozenset(failed)


def _incidence_fingerprint(
    incidences: list[tuple[Pair, TierDescriptor]],
) -> str:
    """Fingerprint pair/weight/cap incidences in the established encoding."""

    ordered = sorted(
        incidences,
        key=lambda item: (
            closure.pair_payload(item[0]),
            item[1].weight,
            item[1].caps,
        ),
    )
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": list(descriptor.weight),
            "caps": list(descriptor.caps),
        }
        for pair, descriptor in ordered
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _family_certificate(
    label: str,
    shielded_masks: frozenset[int],
) -> tuple[dict[str, object], frozenset[Pair], frozenset[Pair]]:
    """Finite set certificate for one shielded-support family."""

    passed, failed = tier_split(shielded_masks)
    legacy_passed, legacy_failed = legacy.tier_split(shielded_masks)
    if passed != legacy_passed or failed != legacy_failed:
        raise AssertionError("the corrected and legacy pair splits changed")

    corrected_failures: list[tuple[Pair, TierDescriptor]] = []
    feasible_failures: list[tuple[Pair, TierDescriptor]] = []
    legacy_only_failures: list[tuple[Pair, TierDescriptor]] = []
    pairs_with_feasible_failure: set[Pair] = set()

    for pair in failed:
        for descriptor in legacy.tier_descriptors():
            corrected = universal_strong_orientation_condition(pair, descriptor)
            old = legacy.universal_orientation_tier_condition(pair, descriptor)
            if old and not corrected:
                raise AssertionError("legacy sufficient cut failed the exact cut")
            if not old and corrected:
                legacy_only_failures.append((pair, descriptor))
            if corrected:
                continue
            incidence = (pair, descriptor)
            corrected_failures.append(incidence)
            if affine.descriptor_feasible(pair, descriptor):
                feasible_failures.append(incidence)
                pairs_with_feasible_failure.add(pair)

    with_feasible = frozenset(pairs_with_feasible_failure)
    without_feasible = failed - with_feasible
    payload: dict[str, object] = {
        "label": label,
        "input_pre_tier_pairs": len(passed) + len(failed),
        "tier_certified_pairs": len(passed),
        "residual_pairs": len(failed),
        "tier_certified_sha256": closure.pair_fingerprint(passed),
        "residual_sha256": closure.pair_fingerprint(failed),
        "corrected_failing_incidences": len(corrected_failures),
        "corrected_feasible_failing_incidences": len(feasible_failures),
        "corrected_infeasible_failing_incidences": (
            len(corrected_failures) - len(feasible_failures)
        ),
        "corrected_failing_incidence_sha256": _incidence_fingerprint(
            corrected_failures
        ),
        "corrected_feasible_incidence_sha256": _incidence_fingerprint(
            feasible_failures
        ),
        "legacy_false_failure_incidences": len(legacy_only_failures),
        "legacy_false_failure_affected_pairs": len(
            {pair for pair, _ in legacy_only_failures}
        ),
        "legacy_false_failure_feasible": sum(
            affine.descriptor_feasible(pair, descriptor)
            for pair, descriptor in legacy_only_failures
        ),
        "legacy_false_failure_infeasible": sum(
            not affine.descriptor_feasible(pair, descriptor)
            for pair, descriptor in legacy_only_failures
        ),
        "legacy_false_failure_incidence_sha256": _incidence_fingerprint(
            legacy_only_failures
        ),
        "pairs_with_feasible_corrected_failure": len(with_feasible),
        "pairs_without_feasible_corrected_failure": len(without_feasible),
        "with_feasible_sha256": closure.pair_fingerprint(with_feasible),
        "without_feasible_sha256": closure.pair_fingerprint(without_feasible),
    }
    return payload, passed, failed


def counterexample_to_legacy_necessity() -> dict[str, object]:
    """A finite tier identity refuting necessity of the global-top-D cut."""

    pair = (
        closure.mask(("C", "2C")),
        closure.mask(("A", "2A", "AB", "AC")),
    )
    descriptor = legacy._descriptor_with_key(((0, 3, 1), (0, 2, 2)))
    if pair not in closure.residual_pairs(closure.POSITIVE_SHIELDED_MASKS):
        raise AssertionError("the witness must be a positive residual pair")
    top_d, top_s = legacy.tier_sets(pair, descriptor)
    _, superlevels = s_tier_superlevel(pair, descriptor)
    if legacy.universal_orientation_tier_condition(pair, descriptor):
        raise AssertionError("legacy cut unexpectedly passes its counterexample")
    if not universal_strong_orientation_condition(pair, descriptor):
        raise AssertionError("corrected cut unexpectedly fails its witness")
    return {
        "pair": closure.pair_payload(pair),
        "weight": list(descriptor.weight),
        "caps": list(descriptor.caps),
        "global_top_d": [legacy.NAMES[node] for node in sorted(top_d)],
        "global_top_s": [legacy.NAMES[node] for node in sorted(top_s)],
        "s_level_superlevels": [
            [legacy.NAMES[node] for node in sorted(upper)]
            for upper in superlevels
        ],
        "legacy_global_top_d_cut": False,
        "corrected_s_level_superlevel_cut": True,
    }


def certificate() -> dict[str, object]:
    """Complete deterministic certificate for the corrected dependency."""

    positive, positive_passed, positive_failed = _family_certificate(
        "positive-active-invariant",
        closure.POSITIVE_SHIELDED_MASKS,
    )
    signed, signed_passed, signed_failed = _family_certificate(
        "signed",
        closure.SIGNED_SHIELDED_MASKS,
    )
    without_feasible = frozenset(
        pair
        for pair in positive_failed | signed_failed
        if not any(
            not universal_strong_orientation_condition(pair, descriptor)
            and affine.descriptor_feasible(pair, descriptor)
            for descriptor in legacy.tier_descriptors()
        )
    )
    with_feasible = (positive_failed | signed_failed) - without_feasible

    pre = closure.certificate()
    payload: dict[str, object] = {
        "claim_scope": (
            "symbolic S-tier-superlevel cut and finite support/tier/affine "
            "identities; no orientation or stochastic enumeration"
        ),
        "pre_tier_branch_counts": {
            "positive": pre["positive"]["branch_counts"],
            "signed": pre["signed"]["branch_counts"],
        },
        "tier_descriptors": len(legacy.tier_descriptors()),
        "positive": positive,
        "signed": signed,
        "total_tier_certified_pairs": len(positive_passed | signed_passed),
        "total_residual_pairs": len(positive_failed | signed_failed),
        "total_corrected_failing_incidences": (
            positive["corrected_failing_incidences"]
            + signed["corrected_failing_incidences"]
        ),
        "total_corrected_feasible_failing_incidences": (
            positive["corrected_feasible_failing_incidences"]
            + signed["corrected_feasible_failing_incidences"]
        ),
        "total_corrected_infeasible_failing_incidences": (
            positive["corrected_infeasible_failing_incidences"]
            + signed["corrected_infeasible_failing_incidences"]
        ),
        "total_legacy_false_failure_incidences": (
            positive["legacy_false_failure_incidences"]
            + signed["legacy_false_failure_incidences"]
        ),
        "pairs_without_feasible_corrected_failure": len(without_feasible),
        "pairs_with_feasible_corrected_failure": len(with_feasible),
        "without_feasible_sha256": closure.pair_fingerprint(without_feasible),
        "with_feasible_sha256": closure.pair_fingerprint(with_feasible),
        "counterexample_to_legacy_necessity": counterexample_to_legacy_necessity(),
    }
    digest_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    payload["certificate_sha256"] = sha256(digest_payload).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    assert result["positive"]["input_pre_tier_pairs"] == 3531
    assert result["positive"]["tier_certified_pairs"] == 1219
    assert result["positive"]["residual_pairs"] == 2312
    assert result["signed"]["input_pre_tier_pairs"] == 358
    assert result["signed"]["tier_certified_pairs"] == 159
    assert result["signed"]["residual_pairs"] == 199
    assert result["total_residual_pairs"] == 2511
    assert result["total_corrected_failing_incidences"] == 12678
    assert result["total_corrected_feasible_failing_incidences"] == 9709
    assert result["total_corrected_infeasible_failing_incidences"] == 2969
    assert result["total_legacy_false_failure_incidences"] == 208
    assert result["pairs_without_feasible_corrected_failure"] == 151
    assert result["pairs_with_feasible_corrected_failure"] == 2360


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
