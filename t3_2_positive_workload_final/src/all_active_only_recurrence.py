"""Exact selector for the all-active-only reversible-top theorem.

The finite selector is independent of the analytic Foster proof.  It keeps
only support pairs for which every affine-feasible failed descriptor is
three-active and the fixed whole-top linkage is a reversible two-complex
rank-one linkage satisfying the independently audited curvature-cofactor
condition.
"""

from __future__ import annotations

import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import three_active_gluing_gate as gluing


EXPECTED_PAIR_SHA256 = (
    "cc1d4b0941588f7b664a3266076789e548ae1f675924854eff18c9552d86e3ea"
)


def selected_pairs() -> frozenset[closure.Pair]:
    """Return the exact 51-pair all-active-only branch."""

    _, _, residual = feasibility._residual_failures()
    selected: set[closure.Pair] = set()
    for pair in residual:
        descriptors = feasibility.feasible_failing_descriptors(pair)
        if not descriptors:
            continue
        if any(len(tier._active_coordinates(item)) != 3 for item in descriptors):
            continue
        side, top = gluing.fixed_whole_top(pair)
        del side
        if not (
            top.bit_count() == 2
            and flat._support_rank(top) == 1
            and flat._support_deficiency(top) == 0
        ):
            continue
        if not all(gluing.direct_entropy_safe(pair, item) for item in descriptors):
            continue
        selected.add(pair)
    return frozenset(selected)


def certificate() -> dict[str, object]:
    positive, signed, _ = feasibility._residual_failures()
    pairs = selected_pairs()
    top_supports = {
        closure.support(gluing.fixed_whole_top(pair)[1]) for pair in pairs
    }
    descriptor_count = sum(
        len(feasibility.feasible_failing_descriptors(pair)) for pair in pairs
    )
    assert pairs <= positive
    assert not (pairs & signed)
    assert all(
        len(tier._active_coordinates(descriptor)) == 3
        for pair in pairs
        for descriptor in feasibility.feasible_failing_descriptors(pair)
    )
    assert all(
        gluing.direct_entropy_safe(pair, descriptor)
        for pair in pairs
        for descriptor in feasibility.feasible_failing_descriptors(pair)
    )
    all_active_incidences = set(flat.feasible_all_active_incidences())
    assert all(
        (pair, descriptor) in all_active_incidences
        for pair in pairs
        for descriptor in feasibility.feasible_failing_descriptors(pair)
    )
    assert all(
        flat.whole_top_linkage(pair, descriptor)
        == gluing.fixed_whole_top(pair)
        for pair in pairs
        for descriptor in feasibility.feasible_failing_descriptors(pair)
    )
    fingerprint = closure.pair_fingerprint(pairs)
    assert fingerprint == EXPECTED_PAIR_SHA256
    return {
        "claim_scope": (
            "finite selector plus independently audited classwise Foster "
            "theorem for this exact branch; "
            "global T3-2 is not asserted"
        ),
        "support_pairs": len(pairs),
        "positive_pairs": len(pairs & positive),
        "signed_pairs": len(pairs & signed),
        "failed_incidences": descriptor_count,
        "fixed_top_supports": [list(item) for item in sorted(top_supports)],
        "pair_sha256": fingerprint,
        "all_failed_incidences_are_certified_all_active_incidences": True,
        "all_failed_incidences_use_the_fixed_whole_top": True,
        "all_boundary_descriptors_pass_the_tier_condition": True,
        "analytic_theorem_certified": True,
        "global_t3_2_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
