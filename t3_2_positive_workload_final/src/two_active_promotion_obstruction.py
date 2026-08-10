"""Exact dormant-promotion regression and pair-level structural selector.

This module deliberately makes no recurrence claim.  It freezes two facts
needed by the analytic repair:

* four no-whole-top incidences contain the same suppressed two-clock
  carrier, up to the species relabellings present in the residual table;
* after the already certified disjoint branches are removed, exactly 36
  promotion pairs have no affine-feasible one-active failure.  Those 36 are
  only a selector until the promotion episode is proved and audited.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json

import all_active_only_recurrence as all_active_only
import global_atlas_interface_closure as closure
import global_tier_interface as tier
import rank_one_no_promotion_branch as rank_one
import rank_two_return_certificate as rank_two
import stoichiometric_gate_feasibility as feasibility
import two_active_phase_gate as phase


Pair = closure.Pair
Descriptor = tier.TierDescriptor


def _active_count(descriptor: Descriptor) -> int:
    return sum(value > 0 for value in descriptor.weight)


def _complex(*coordinates: int) -> int:
    return tier.COMPLEXES.index(tuple(coordinates))


def _carrier_orbits() -> dict[Pair, tuple[int, int, int]]:
    """Return table-realized copies of ``{U,I+V}/{0,I,2I,I+U}``.

    The value is the coordinate triple ``(I,U,V)``.  Only four of the six
    formal species permutations occur in the inherited ordered residual
    table.
    """

    result: dict[Pair, tuple[int, int, int]] = {}
    for inactive in range(3):
        active = tuple(index for index in range(3) if index != inactive)
        for u, v in (active, tuple(reversed(active))):
            unit_u = tuple(int(index == u) for index in range(3))
            unit_i = tuple(int(index == inactive) for index in range(3))
            unit_v = tuple(int(index == v) for index in range(3))
            i_plus_v = tuple(a + b for a, b in zip(unit_i, unit_v))
            i_plus_u = tuple(a + b for a, b in zip(unit_i, unit_u))
            two_i = tuple(2 * value for value in unit_i)
            carrier = closure.mask(
                (tier.NAMES[_complex(*unit_u)], tier.NAMES[_complex(*i_plus_v)])
            )
            lower = closure.mask(
                (
                    "0",
                    tier.NAMES[_complex(*unit_i)],
                    tier.NAMES[_complex(*two_i)],
                    tier.NAMES[_complex(*i_plus_u)],
                )
            )
            for pair in ((carrier, lower), (lower, carrier)):
                if pair in feasibility._residual_failures()[2]:
                    result[pair] = (inactive, u, v)
    return result


def suppressed_rows() -> tuple[tuple[Pair, Descriptor, tuple[int, int, int]], ...]:
    """The four no-whole rows with positive isolated-block log reward."""

    orbits = _carrier_orbits()
    selected = []
    for pair, descriptor, category in phase.incidences():
        if pair not in orbits or category != "promotion_dormant_top":
            continue
        if phase._whole_top_linkages(pair, descriptor):
            continue
        inactive, u, v = orbits[pair]
        if descriptor.weight[inactive] != 0:
            continue
        if 2 * descriptor.weight[u] > descriptor.weight[v]:
            selected.append((pair, descriptor, (inactive, u, v)))
    return tuple(selected)


def _prior_certified_pairs() -> frozenset[Pair]:
    positive, signed, residual = feasibility._residual_failures()
    del positive, signed
    affine = frozenset(
        pair
        for pair in residual
        if not feasibility.feasible_failing_descriptors(pair)
    )
    rank_two_pairs = frozenset(pair for pair, _ in rank_two._rank_two_rows())
    return frozenset(
        affine
        | rank_two_pairs
        | all_active_only.selected_pairs()
        | rank_one.candidate_pair_level_pairs()
    )


def pair_level_selector() -> frozenset[Pair]:
    """Promotion pairs with no one-active failure after prior branches.

    This is a structural candidate selector, not an analytic theorem.
    """

    _, _, residual = feasibility._residual_failures()
    promotion_pairs = frozenset(
        pair
        for pair, _, category in phase.incidences()
        if category.startswith("promotion_")
    )
    one_active = frozenset(
        pair
        for pair in residual
        if any(
            _active_count(descriptor) == 1
            for descriptor in feasibility.feasible_failing_descriptors(pair)
        )
    )
    return promotion_pairs - _prior_certified_pairs() - one_active


def _suppressed_payload() -> tuple[dict[str, object], ...]:
    payload = []
    for pair, descriptor, (inactive, u, v) in suppressed_rows():
        payload.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "weight": list(descriptor.weight),
                "inactive": tier.NAMES[1 + inactive],
                "u": tier.NAMES[1 + u],
                "v": tier.NAMES[1 + v],
                "isolated_block_weight_reward": (
                    2 * descriptor.weight[u] - descriptor.weight[v]
                ),
            }
        )
    return tuple(sorted(payload, key=lambda row: (row["pair"], row["weight"])))


EXPECTED_SUPPRESSED_SHA256 = (
    "53911b366b023cfdc4e76f3bf8df99cd5a502252fb9df552268ea03ee7fae465"
)
EXPECTED_SELECTOR_SHA256 = (
    "f2ad8cbe4b9ca7f36c39bed4bfe5aaafc6a9152eaf300390b5c25ba546519137"
)


def certificate() -> dict[str, object]:
    positive, signed, _ = feasibility._residual_failures()
    suppressed = suppressed_rows()
    suppressed_payload = _suppressed_payload()
    suppressed_hash = sha256(
        json.dumps(
            suppressed_payload, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()

    selector = pair_level_selector()
    selector_rows = tuple(
        row
        for row in phase.incidences()
        if row[0] in selector and row[2].startswith("promotion_")
    )
    category_histogram = Counter(category for _, _, category in selector_rows)
    whole_histogram = Counter(
        "with_whole_top" if phase._whole_top_linkages(pair, descriptor)
        else "no_whole_top"
        for pair, descriptor, _ in selector_rows
    )
    seeded_whole_supports = Counter()
    dormant_whole_supports = Counter()
    dormant_enabled_sources = Counter()
    dormant_disabled = 0
    for pair, descriptor, category in selector_rows:
        whole = phase._whole_top_linkages(pair, descriptor)
        if category == "promotion_enabled_top_seed":
            seeded_whole_supports[
                ",".join(closure.support(whole[0])) if whole else "none"
            ] += 1
            source_levels = {
                sum(
                    descriptor.weight[index] * tier.COMPLEXES[node][index]
                    for index in range(3)
                )
                for mask in pair
                for node in tier._nodes(mask)
            }
            assert source_levels == {0, 1}
            continue

        assert category == "promotion_dormant_top"
        assert len(whole) == 1
        dormant_whole_supports[",".join(closure.support(whole[0]))] += 1
        inactive = next(
            index for index, value in enumerate(descriptor.weight) if value == 0
        )
        assert inactive == 2
        partner = pair[1] if pair[0] == whole[0] else pair[0]
        assert "2C" in closure.support(partner)
        enabled = tuple(
            tier.NAMES[node]
            for node in sorted(tier._nodes(partner))
            if tier._enabled(node, descriptor.caps)
        )
        dormant_enabled_sources[",".join(enabled) if enabled else "none"] += 1
        dormant_disabled += int(not enabled)

    assert len(suppressed) == 4
    assert suppressed_hash == EXPECTED_SUPPRESSED_SHA256
    assert all(
        2 * descriptor.weight[u] - descriptor.weight[v] == 3
        for _, descriptor, (_, u, v) in suppressed
    )
    assert closure.pair_fingerprint(selector) == EXPECTED_SELECTOR_SHA256
    assert len(selector) == 36
    assert all(
        {
            _active_count(descriptor)
            for descriptor in feasibility.feasible_failing_descriptors(pair)
        }
        == {2}
        for pair in selector
    )
    assert all(
        len(feasibility.feasible_failing_descriptors(pair)) == 1
        for pair in selector
    )

    return {
        "claim_scope": (
            "exact regression and pair selector only; no promotion or "
            "recurrence theorem"
        ),
        "suppressed_no_whole_incidences": len(suppressed),
        "suppressed_no_whole_pairs": len({pair for pair, _, _ in suppressed}),
        "suppressed_rows_sha256": suppressed_hash,
        "selector_pairs": len(selector),
        "selector_positive_pairs": len(selector & positive),
        "selector_signed_pairs": len(selector & signed),
        "selector_category_histogram": dict(sorted(category_histogram.items())),
        "selector_whole_top_histogram": dict(sorted(whole_histogram.items())),
        "selector_seeded_whole_support_histogram": dict(
            sorted(seeded_whole_supports.items())
        ),
        "selector_dormant_whole_support_histogram": dict(
            sorted(dormant_whole_supports.items())
        ),
        "selector_dormant_enabled_source_histogram": dict(
            sorted(dormant_enabled_sources.items())
        ),
        "selector_dormant_disabled_finite_class_incidences": dormant_disabled,
        "selector_pair_sha256": closure.pair_fingerprint(selector),
        "all_selector_failures_are_two_active": True,
        "each_selector_pair_has_one_feasible_failure": True,
        "analytic_promotion_theorem_certified": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
        "suppressed_rows": suppressed_payload,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
