"""Claim-neutral selector for the prospective no-promotion 26-pair family.

This module is downstream of :mod:`one_active_prospective_composition`.
It assumes no analytic promotion: the prospective 795-pair remainder is
used only as a finite set.  Inside that set it selects the pairs which

* have feasible failed descriptors in active dimensions exactly ``{1, 3}``;
* have a fixed reversible two-node whole-top linkage in every all-active
  failed descriptor; and
* satisfy the certified curvature-cofactor premise of the all-active
  rate-adjusted-factorial theorem on every such descriptor.

The resulting 26 pairs have no two-active failure, hence no promotion
kernel is needed.  The existing all-active theorem is stated for the
unpowered corrected factorial potential, however, and the one-active graph
theorem was frozen on a different pair selector.  Consequently every
analytic, pair-recurrence, and global flag below remains false.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_phase_shape as one_active
import one_active_prospective_composition as prospective
import one_active_relative_debt_cegar as graph
import one_active_remaining_structure as structure
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as three_active
import three_active_gluing_gate as three_glue
import two_active_phase_gate as two_active


Pair = closure.Pair
Descriptor = tier.TierDescriptor

EXPECTED_PARENT_795_SHA256 = (
    "6a1327e6c38bfcab30d334691415ba457e84d45d1dfe53d81df4c02aad868123"
)
EXPECTED_PAIR_SHA256 = (
    "393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af"
)
EXPECTED_ALL_INCIDENCE_SHA256 = (
    "af666979be9e3b747375ce885d5feabbb01ed3053ccca786e27b12558a4e3f20"
)
EXPECTED_ONE_INCIDENCE_SHA256 = (
    "d5c045a19191ec841ec75a0c0014ab04b7f638451eec6eee514bfa910b6d7d8e"
)
EXPECTED_THREE_INCIDENCE_SHA256 = (
    "8c99d1994817920d3226b797dced3d863fb4bd86953f0f1bcb02c277f346aab5"
)
EXPECTED_NO_TWO_LINEAR_20_SHA256 = (
    "32e2d78e51f99d765eb76bbb8a2bcf490c4dfd0208f4b904a0475efea506b446"
)
EXPECTED_ALL_TWO_ACTIVE_749_SHA256 = (
    "71de0de1b266a0e75f309495d31eb2ba0c7f4c39590054ccc2fd38597b695945"
)
EXPECTED_PAYLOAD_SHA256 = (
    "3f5b40759cd490a532b7bc24893768bca50f59202182a8b72d04c1ebc497e947"
)


@lru_cache(maxsize=1)
def prospective_after_pairs() -> frozenset[Pair]:
    """Reconstruct the claim-neutral prospective 795-pair remainder."""

    _positive, _signed, residual = feasibility._residual_failures()
    current = frozenset().union(
        *prospective.certified_branch_sets().values()
    )
    candidate = frozenset(one_active.candidate_pairs())
    result = residual - current - (candidate - current)
    assert len(result) == 795
    assert closure.pair_fingerprint(result) == EXPECTED_PARENT_795_SHA256
    return result


@lru_cache(maxsize=None)
def failures(pair: Pair) -> tuple[Descriptor, ...]:
    return feasibility.feasible_failing_descriptors(pair)


def active_profile(pair: Pair) -> frozenset[int]:
    return frozenset(
        len(tier._active_coordinates(descriptor))
        for descriptor in failures(pair)
    )


@lru_cache(maxsize=1)
def _all_active_by_pair() -> dict[Pair, tuple[Descriptor, ...]]:
    return three_glue.incidences_by_pair()


def _safe_reversible_all_active(pair: Pair) -> bool:
    """The exact unpowered all-active base-potential premise."""

    descriptors = _all_active_by_pair().get(pair)
    if not descriptors:
        return False
    top_values = {
        three_active.whole_top_linkage(pair, descriptor)[1]
        for descriptor in descriptors
    }
    if len(top_values) != 1:
        return False
    top = next(iter(top_values))
    return top.bit_count() == 2 and all(
        three_glue.direct_entropy_safe(pair, descriptor)
        for descriptor in descriptors
    )


@lru_cache(maxsize=1)
def selected_pairs() -> frozenset[Pair]:
    result = frozenset(
        pair
        for pair in prospective_after_pairs()
        if active_profile(pair) == frozenset((1, 3))
        and _safe_reversible_all_active(pair)
    )
    assert len(result) == 26
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


def selected_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    return tuple(
        sorted(
            (
                (pair, descriptor)
                for pair in selected_pairs()
                for descriptor in failures(pair)
            ),
            key=lambda item: (
                closure.pair_payload(item[0]),
                item[1].weight,
                item[1].caps,
            ),
        )
    )


def one_active_graph_category(pair: Pair, descriptor: Descriptor) -> str:
    """Route a selected one-active row through the existing proof shapes.

    This is a finite structural routing statement.  It does not enlarge the
    certified scope of the graph theorem by itself.
    """

    if len(tier._active_coordinates(descriptor)) != 1:
        raise ValueError("descriptor is not one-active")
    normalized = structure._normalized(pair, descriptor)
    supports = tuple(normalized["supports"])
    phases = tuple(structure._linkage_phase(support) for support in supports)
    kinds = tuple(kind for kind, _stripped in phases)
    if any(
        kind == "mixed_killed" and "0" in stripped
        for kind, stripped in phases
    ):
        return "mixed_C_source_direct_down_0"
    if kinds != ("mixed_killed", "mixed_killed"):
        raise AssertionError((supports, phases))
    if {phases[0][1], phases[1][1]} != {("A",), ("B",)}:
        raise AssertionError((supports, phases))
    return graph._family_iii_category(supports, phases)


def _incidence_rows(active_count: int) -> tuple[tuple[Pair, Descriptor], ...]:
    return tuple(
        (pair, descriptor)
        for pair, descriptor in selected_incidences()
        if len(tier._active_coordinates(descriptor)) == active_count
    )


def _top_histograms(
    all_active_rows: tuple[tuple[Pair, Descriptor], ...],
) -> tuple[Counter[str], Counter[str]]:
    pair_histogram: Counter[str] = Counter()
    incidence_histogram: Counter[str] = Counter()
    for pair in selected_pairs():
        _side, top = three_glue.fixed_whole_top(pair)
        pair_histogram[",".join(closure.support(top))] += 1
    for pair, descriptor in all_active_rows:
        _side, top = three_active.whole_top_linkage(pair, descriptor)
        incidence_histogram[",".join(closure.support(top))] += 1
    return pair_histogram, incidence_histogram


def _no_two_active_split() -> tuple[frozenset[Pair], frozenset[Pair]]:
    no_two = frozenset(
        pair
        for pair in prospective_after_pairs()
        if 2 not in active_profile(pair)
    )
    linear = no_two - selected_pairs()
    assert len(no_two) == 46
    assert len(linear) == 20
    assert closure.pair_fingerprint(linear) == EXPECTED_NO_TWO_LINEAR_20_SHA256
    return no_two, linear


def _two_active_maximality_check() -> tuple[frozenset[Pair], frozenset[Pair]]:
    any_two = frozenset(
        pair
        for pair in prospective_after_pairs()
        if 2 in active_profile(pair)
    )
    promotion = frozenset(
        pair
        for pair in prospective_after_pairs()
        for descriptor in failures(pair)
        if len(tier._active_coordinates(descriptor)) == 2
        and two_active.incidence_category(pair, descriptor).startswith(
            "promotion_"
        )
    )
    assert any_two == promotion
    assert len(any_two) == 749
    assert closure.pair_fingerprint(any_two) == EXPECTED_ALL_TWO_ACTIVE_749_SHA256
    return any_two, promotion


def certificate() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    pairs = selected_pairs()
    rows = selected_incidences()
    one_rows = _incidence_rows(1)
    all_active_rows = _incidence_rows(3)
    assert not _incidence_rows(2)

    graph_histogram = Counter(
        one_active_graph_category(pair, descriptor)
        for pair, descriptor in one_rows
    )
    assert graph_histogram == {
        "mixed_C_source_direct_down_0": 20,
        "family_iii_origin_down_0": 8,
        "family_iii_origin_no_history": 2,
    }
    pair_top_histogram, incidence_top_histogram = _top_histograms(
        all_active_rows
    )
    assert pair_top_histogram == {"2A,BC": 8, "AC,BC": 18}
    assert incidence_top_histogram == {"2A,BC": 40, "AC,BC": 54}

    no_two, linear = _no_two_active_split()
    any_two, promotion = _two_active_maximality_check()
    del promotion

    all_hash = feasibility._incidence_fingerprint(rows)
    one_hash = feasibility._incidence_fingerprint(one_rows)
    all_active_hash = feasibility._incidence_fingerprint(all_active_rows)
    assert all_hash == EXPECTED_ALL_INCIDENCE_SHA256
    assert one_hash == EXPECTED_ONE_INCIDENCE_SHA256
    assert all_active_hash == EXPECTED_THREE_INCIDENCE_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "finite prospective selector and base-potential compatibility "
            "only; no powered all-active or recurrence claim"
        ),
        "prospective_parent_795": {
            "pairs": len(prospective_after_pairs()),
            "pair_sha256": closure.pair_fingerprint(
                prospective_after_pairs()
            ),
        },
        "selector_definition": {
            "feasible_failure_active_profile": [1, 3],
            "fixed_all_active_top_size": 2,
            "all_all_active_rows_direct_entropy_safe": True,
            "two_active_failure_absent": True,
        },
        "selected_pairs": {
            "total": len(pairs),
            "positive": len(pairs & positive),
            "signed": len(pairs & signed),
            "pair_sha256": closure.pair_fingerprint(pairs),
        },
        "selected_incidences": {
            "total": len(rows),
            "one_active": len(one_rows),
            "two_active": 0,
            "all_active": len(all_active_rows),
            "all_sha256": all_hash,
            "one_active_sha256": one_hash,
            "all_active_sha256": all_active_hash,
        },
        "one_active_structural_routing": dict(sorted(graph_histogram.items())),
        "all_active_top_pair_histogram": dict(
            sorted(pair_top_histogram.items())
        ),
        "all_active_top_incidence_histogram": dict(
            sorted(incidence_top_histogram.items())
        ),
        "maximal_no_two_active_split": {
            "no_two_active_pairs": len(no_two),
            "factorial_compatible_pairs": len(pairs),
            "linear_workload_switch_pairs": len(linear),
            "linear_workload_switch_pair_sha256": closure.pair_fingerprint(
                linear
            ),
        },
        "two_active_maximality": {
            "pairs_with_two_active_failure": len(any_two),
            "all_have_a_promotion_failure": True,
            "pair_sha256": closure.pair_fingerprint(any_two),
        },
        "common_base_potential": (
            "rate-adjusted corrected factorial F_l selected by the fixed "
            "reversible all-active top; the one-active analytic theorem "
            "allows the same arbitrary fixed l"
        ),
        "one_active_graph_scope_extension_certified": False,
        "powered_all_active_lift_certified": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
