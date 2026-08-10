"""Exact structural split of affine-feasible two-active tier failures.

This module makes no recurrence claim.  It separates the two-active
pair--descriptor incidences left by ``stoichiometric_gate_feasibility`` into
the support-level mechanisms that a later physical-time argument must treat:

* a proper top-D subset with or without an enabled top seed; and
* a flat, closed top linkage of stoichiometric rank one or two.

All counts concern descriptor incidences unless a field explicitly says
``pairs``.  A support pair may occur in more than one incidence category.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Descriptor = tier.TierDescriptor


def _linkage_rank(mask: int) -> int:
    nodes = tuple(sorted(tier._nodes(mask)))
    anchor = tier.COMPLEXES[nodes[0]]
    differences = tuple(
        tuple(
            tier.COMPLEXES[node][coordinate] - anchor[coordinate]
            for coordinate in range(3)
        )
        for node in nodes[1:]
    )
    return len(feasibility._rref(differences, 3)[0])


def _active_count(descriptor: Descriptor) -> int:
    return sum(value > 0 for value in descriptor.weight)


def _inactive_coordinate(descriptor: Descriptor) -> int:
    inactive = tuple(
        coordinate
        for coordinate, value in enumerate(descriptor.weight)
        if value == 0
    )
    if len(inactive) != 1:
        raise ValueError("descriptor is not two-active")
    return inactive[0]


def _proper_top_linkages(
    pair: Pair,
    descriptor: Descriptor,
) -> tuple[tuple[int, frozenset[int]], ...]:
    top_d, _ = tier.tier_sets(pair, descriptor)
    result = []
    for mask in pair:
        nodes = tier._nodes(mask)
        intersection = nodes & top_d
        if intersection and intersection != nodes:
            result.append((mask, intersection))
    return tuple(result)


def _whole_top_linkages(pair: Pair, descriptor: Descriptor) -> tuple[int, ...]:
    top_d, _ = tier.tier_sets(pair, descriptor)
    return tuple(mask for mask in pair if tier._nodes(mask) <= top_d)


def incidence_category(pair: Pair, descriptor: Descriptor) -> str:
    """Return the exact structural category of one feasible two-active failure."""

    if _active_count(descriptor) != 2:
        raise ValueError("descriptor is not two-active")
    if tier.universal_orientation_tier_condition(pair, descriptor):
        raise ValueError("descriptor is not a tier failure")
    if not feasibility.descriptor_feasible(pair, descriptor):
        raise ValueError("descriptor is not affine-stoichiometrically feasible")

    mode = tier._gate_mode(pair, descriptor)
    if mode == "disabled_source_promotion":
        proper = _proper_top_linkages(pair, descriptor)
        if not proper:
            raise AssertionError("promotion mode has no proper top linkage")
        seeded = any(
            tier._enabled(node, descriptor.caps)
            for _, top_nodes in proper
            for node in top_nodes
        )
        return "promotion_enabled_top_seed" if seeded else "promotion_dormant_top"

    if mode != "flat_top_linkage":
        raise AssertionError(f"unknown gate mode {mode}")
    whole = _whole_top_linkages(pair, descriptor)
    if len(whole) != 1:
        raise AssertionError("flat two-active failure lacks a unique top linkage")
    rank = _linkage_rank(whole[0])
    if rank == 1:
        return "closed_rank_one_top_phase"
    if rank == 2:
        return "coupled_rank_two_top_phase"
    raise AssertionError(f"unexpected flat top-linkage rank {rank}")


def rank_one_activation_category(pair: Pair, descriptor: Descriptor) -> str:
    """Refine a closed rank-one top phase by its first activation layer."""

    if incidence_category(pair, descriptor) != "closed_rank_one_top_phase":
        raise ValueError("incidence does not have a closed rank-one top phase")
    top_mask = _whole_top_linkages(pair, descriptor)[0]
    lower_mask = pair[1] if pair[0] == top_mask else pair[0]
    lower_nodes = tier._nodes(lower_mask)
    lower_orders = {
        node: sum(
            descriptor.weight[coordinate] * tier.COMPLEXES[node][coordinate]
            for coordinate in range(3)
        )
        for node in lower_nodes
    }
    lower_maximum = max(lower_orders.values())
    lower_top = {
        node for node, order in lower_orders.items() if order == lower_maximum
    }
    if any(tier._enabled(node, descriptor.caps) for node in lower_top):
        return "lower_top_seeded"

    inactive = _inactive_coordinate(descriptor)
    top_changes_inactive = len(
        {
            tier.COMPLEXES[node][inactive]
            for node in tier._nodes(top_mask)
        }
    ) > 1
    if top_changes_inactive:
        return "top_phase_activates"
    if any(tier._enabled(node, descriptor.caps) for node in lower_nodes):
        return "lower_layer_activation_needed"
    return "zero_boundary_phase_only"


@lru_cache(maxsize=1)
def incidences() -> tuple[tuple[Pair, Descriptor, str], ...]:
    _, _, residual = feasibility._residual_failures()
    result = []
    for pair in sorted(residual):
        for descriptor in feasibility.feasible_failing_descriptors(pair):
            if _active_count(descriptor) != 2:
                continue
            result.append((pair, descriptor, incidence_category(pair, descriptor)))
    return tuple(result)


def _incidence_fingerprint(rows: tuple[tuple[Pair, Descriptor, str], ...]) -> str:
    payload = [
        {
            "pair": closure.pair_payload(pair),
            "weight": list(descriptor.weight),
            "caps": list(descriptor.caps),
            "category": category,
        }
        for pair, descriptor, category in sorted(
            rows,
            key=lambda row: (
                closure.pair_payload(row[0]),
                row[1].weight,
                row[1].caps,
                row[2],
            ),
        )
    ]
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return sha256(encoded).hexdigest()


def certificate() -> dict[str, object]:
    positive, signed, _ = feasibility._residual_failures()
    rows = incidences()
    categories = (
        "promotion_enabled_top_seed",
        "promotion_dormant_top",
        "closed_rank_one_top_phase",
        "coupled_rank_two_top_phase",
    )
    by_category: dict[str, object] = {}
    for category in categories:
        selected = tuple(row for row in rows if row[2] == category)
        pairs = frozenset(pair for pair, _, _ in selected)
        top_supports = frozenset(
            mask
            for pair, descriptor, _ in selected
            for mask in _whole_top_linkages(pair, descriptor)
        ) if category.endswith("top_phase") else frozenset()
        by_category[category] = {
            "incidences": len(selected),
            "pairs": len(pairs),
            "positive_pairs": len(pairs & positive),
            "signed_pairs": len(pairs & signed),
            "pair_sha256": closure.pair_fingerprint(pairs),
            "top_supports": [
                list(closure.support(mask))
                for mask in sorted(
                    top_supports,
                    key=lambda value: (value.bit_count(), closure.support(value)),
                )
            ],
        }

    all_pairs = frozenset(pair for pair, _, _ in rows)
    flat_rows = tuple(
        row for row in rows if row[2].endswith("top_phase")
    )
    flat_pairs = frozenset(pair for pair, _, _ in flat_rows)
    promotion_rows = tuple(
        row for row in rows if row[2].startswith("promotion_")
    )
    promotion_pairs = frozenset(pair for pair, _, _ in promotion_rows)
    rank_two_supports = {
        tuple(closure.support(mask))
        for pair, descriptor, category in rows
        if category == "coupled_rank_two_top_phase"
        for mask in _whole_top_linkages(pair, descriptor)
    }
    assert rank_two_supports == {("B", "2A", "BC")}
    rank_two_lower_masks = frozenset(
        pair[1]
        if pair[0] == _whole_top_linkages(pair, descriptor)[0]
        else pair[0]
        for pair, descriptor, category in rows
        if category == "coupled_rank_two_top_phase"
    )
    rank_two_low_group = {
        tier.NAMES.index(name) for name in ("0", "C", "2C")
    }
    rank_two_high_group = {
        tier.NAMES.index(name) for name in ("A", "AC")
    }
    assert len(rank_two_lower_masks) == 14
    assert all(
        tier._nodes(mask) <= rank_two_low_group | rank_two_high_group
        and bool(tier._nodes(mask) & rank_two_low_group)
        and bool(tier._nodes(mask) & rank_two_high_group)
        for mask in rank_two_lower_masks
    )

    # Every rank-one flat shell is genuinely bounded by its positive active
    # workload: its line direction is not the inactive coordinate axis.
    for pair, descriptor, category in rows:
        if category != "closed_rank_one_top_phase":
            continue
        top_mask = _whole_top_linkages(pair, descriptor)[0]
        direction = feasibility.stoichiometric_basis((top_mask, top_mask))[0]
        inactive = _inactive_coordinate(descriptor)
        assert any(
            direction[coordinate]
            for coordinate in range(3)
            if coordinate != inactive
        )
        assert sum(
            descriptor.weight[coordinate] * direction[coordinate]
            for coordinate in range(3)
        ) == 0

    promotion_cap_histogram = Counter(
        descriptor.caps[_inactive_coordinate(descriptor)]
        for _, descriptor, category in rows
        if category.startswith("promotion_")
    )
    flat_cap_histogram = Counter(
        descriptor.caps[_inactive_coordinate(descriptor)]
        for _, descriptor, category in rows
        if category.endswith("top_phase")
    )
    assert promotion_cap_histogram == {0: 1416}
    assert flat_cap_histogram == {0: 324, 1: 324, 2: 324}

    rank_one_activation = Counter()
    rank_one_lower_maximum_weight = Counter()
    rank_one_activation_pairs: dict[str, set[Pair]] = {}
    for pair, descriptor, category in rows:
        if category != "closed_rank_one_top_phase":
            continue
        top_mask = _whole_top_linkages(pair, descriptor)[0]
        lower_mask = pair[1] if pair[0] == top_mask else pair[0]
        rank_one_lower_maximum_weight[
            max(
                sum(
                    descriptor.weight[coordinate]
                    * tier.COMPLEXES[node][coordinate]
                    for coordinate in range(3)
                )
                for node in tier._nodes(lower_mask)
            )
        ] += 1
        activation = rank_one_activation_category(pair, descriptor)
        rank_one_activation[activation] += 1
        rank_one_activation_pairs.setdefault(activation, set()).add(pair)

    assert rank_one_activation == {
        "lower_top_seeded": 893,
        "top_phase_activates": 2,
        "lower_layer_activation_needed": 25,
        "zero_boundary_phase_only": 10,
    }
    assert rank_one_lower_maximum_weight == {1: 930}

    zero_boundary_incidences = frozenset(
        (pair, descriptor.weight, descriptor.caps)
        for pair, descriptor, category in rows
        if category == "closed_rank_one_top_phase"
        and rank_one_activation_category(pair, descriptor)
        == "zero_boundary_phase_only"
    )
    assert len(zero_boundary_incidences) == 10

    affine_branch = frozenset(
        pair for pair in positive | signed
        if not feasibility.feasible_failing_descriptors(pair)
    )
    one_active_after_affine = frozenset(
        pair
        for pair in (positive | signed) - affine_branch
        if (failures := feasibility.feasible_failing_descriptors(pair))
        and all(_active_count(descriptor) == 1 for descriptor in failures)
    )
    assert not (affine_branch & one_active_after_affine)
    prior_union = affine_branch | one_active_after_affine
    composition_candidates: set[Pair] = set()
    for pair in (positive | signed) - prior_union:
        remaining_multi = tuple(
            descriptor
            for descriptor in feasibility.feasible_failing_descriptors(pair)
            if _active_count(descriptor) > 1
        )
        if remaining_multi and all(
            (pair, descriptor.weight, descriptor.caps) in zero_boundary_incidences
            for descriptor in remaining_multi
        ):
            composition_candidates.add(pair)
    assert not composition_candidates

    category_histogram = Counter(category for _, _, category in rows)
    assert sum(category_histogram.values()) == len(rows)
    return {
        "claim_scope": (
            "exact structural classification only; closed phase and promotion "
            "labels are not full-network recurrence claims"
        ),
        "feasible_two_active_incidences": len(rows),
        "pairs_with_a_feasible_two_active_failure": len(all_pairs),
        "positive_pairs": len(all_pairs & positive),
        "signed_pairs": len(all_pairs & signed),
        "flat_top_incidences": len(flat_rows),
        "flat_top_pairs": len(flat_pairs),
        "promotion_incidences": len(promotion_rows),
        "promotion_pairs": len(promotion_pairs),
        "flat_and_promotion_pair_overlap": len(flat_pairs & promotion_pairs),
        "promotion_inactive_cap_histogram": dict(
            sorted(promotion_cap_histogram.items())
        ),
        "flat_inactive_cap_histogram": dict(sorted(flat_cap_histogram.items())),
        "rank_two_lower_partners": {
            "count": len(rank_two_lower_masks),
            "supports": [
                list(closure.support(mask))
                for mask in sorted(
                    rank_two_lower_masks,
                    key=lambda value: (value.bit_count(), closure.support(value)),
                )
            ],
            "all_cross_q_partition": True,
        },
        "rank_one_activation_refinement": {
            category: {
                "incidences": rank_one_activation[category],
                "pairs": len(rank_one_activation_pairs[category]),
                "pair_sha256": closure.pair_fingerprint(
                    rank_one_activation_pairs[category]
                ),
            }
            for category in (
                "lower_top_seeded",
                "top_phase_activates",
                "lower_layer_activation_needed",
                "zero_boundary_phase_only",
            )
        },
        "rank_one_lower_maximum_weight_histogram": dict(
            sorted(rank_one_lower_maximum_weight.items())
        ),
        "reachability_aware_composition_selector": {
            "claim_scope": (
                "selector only; composition with the one-active theorem is "
                "not asserted here"
            ),
            "affine_branch_pairs": len(affine_branch),
            "one_active_after_affine_pairs": len(one_active_after_affine),
            "branch_overlap": len(affine_branch & one_active_after_affine),
            "prior_union_pairs": len(prior_union),
            "prior_union_positive": len(prior_union & positive),
            "prior_union_signed": len(prior_union & signed),
            "remaining_after_prior_union": len((positive | signed) - prior_union),
            "zero_boundary_incidences": len(zero_boundary_incidences),
            "zero_boundary_pairs": len(
                {pair for pair, _, _ in zero_boundary_incidences}
            ),
            "new_pairs_after_removing_one_active_failures": len(
                composition_candidates
            ),
            "new_pair_sha256": closure.pair_fingerprint(
                composition_candidates
            ),
        },
        "categories": by_category,
        "all_pair_sha256": closure.pair_fingerprint(all_pairs),
        "all_incidence_sha256": _incidence_fingerprint(rows),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
