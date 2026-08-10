"""Exact selector for the audited rank-one branch without promotion.

The 233-pair flag is a dimension-at-least-two common-potential theorem.
The 141-pair subset without an affine-feasible one-active failure has passed
an independent pair-level common-potential audit. The other 92 pairs retain
an open one-active interface.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import all_active_only_recurrence as all_active_only
import rank_two_return_certificate as rank_two
import stoichiometric_gate_feasibility as feasibility
import three_active_gluing_gate as all_active
import two_active_phase_gate as two_active


Pair = closure.Pair
Descriptor = tier.TierDescriptor


def _active_count(descriptor: Descriptor) -> int:
    return sum(value > 0 for value in descriptor.weight)


def _rank_one_rows() -> tuple[tuple[Pair, Descriptor], ...]:
    return tuple(
        (pair, descriptor)
        for pair, descriptor, category in two_active.incidences()
        if category == "closed_rank_one_top_phase"
    )


def _promotion_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair, _, category in two_active.incidences()
        if category.startswith("promotion_")
    )


def rank_one_pairs() -> frozenset[Pair]:
    return frozenset(pair for pair, _ in _rank_one_rows())


def no_promotion_pairs() -> frozenset[Pair]:
    return rank_one_pairs() - _promotion_pairs()


def one_active_obstruction_pairs() -> frozenset[Pair]:
    return frozenset(
        pair
        for pair in no_promotion_pairs()
        if any(
            _active_count(descriptor) == 1
            for descriptor in feasibility.feasible_failing_descriptors(pair)
        )
    )


def candidate_pair_level_pairs() -> frozenset[Pair]:
    return no_promotion_pairs() - one_active_obstruction_pairs()


def _top_masks() -> dict[Pair, int]:
    result: dict[Pair, set[int]] = defaultdict(set)
    for pair, descriptor in _rank_one_rows():
        top, = two_active._whole_top_linkages(pair, descriptor)
        result[pair].add(top)
    assert all(len(masks) == 1 for masks in result.values())
    return {pair: next(iter(masks)) for pair, masks in result.items()}


def _all_active_branch(pair: Pair, top: int) -> str:
    grouped = all_active.incidences_by_pair()
    if pair not in grouped:
        return "no_all_active_failure"
    _, all_top = all_active.fixed_whole_top(pair)
    assert all_top == top
    if top.bit_count() == 3:
        return "directed_triple_factorial_linear"
    obstruction_pairs = {
        obstruction_pair
        for obstruction_pair, _, _ in all_active.curvature_obstructions()
    }
    assert pair not in obstruction_pairs
    return "safe_reversible_rate_adjusted"


def _row_payload() -> tuple[dict[str, object], ...]:
    top_masks = _top_masks()
    one_active = one_active_obstruction_pairs()
    rows = []
    for pair in sorted(no_promotion_pairs(), key=closure.pair_payload):
        failures = feasibility.feasible_failing_descriptors(pair)
        top = top_masks[pair]
        rows.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "common_rank_one_top": list(closure.support(top)),
                "all_active_branch": _all_active_branch(pair, top),
                "feasible_failure_active_counts": sorted(
                    {_active_count(descriptor) for descriptor in failures}
                ),
                "has_one_active_obstruction": pair in one_active,
                "candidate_pair_level_composable": pair not in one_active,
            }
        )
    return tuple(rows)


EXPECTED_LOCAL_PAIR_SHA256 = (
    "afc4f8e121cdd6893f31edfdc5461f4d5f4d5b8340e37b64a222adcd7994114c"
)
EXPECTED_CANDIDATE_PAIR_SHA256 = (
    "bc3540674c5ec8eef96fe4272e15c1f3d220a06fe7ad890189d2f745e6c22e67"
)
EXPECTED_ROWS_SHA256 = (
    "6b3bc0cfb7dfae535f40d90a6d8faa6e7056902f75e3a578567652397a008809"
)


def certificate() -> dict[str, object]:
    flat = rank_one_pairs()
    promotions = _promotion_pairs()
    local = no_promotion_pairs()
    one_active = one_active_obstruction_pairs()
    candidate = candidate_pair_level_pairs()
    rows = _row_payload()

    positive_residual, signed_residual = tier.tier_split(
        closure.POSITIVE_SHIELDED_MASKS
    )[1], tier.tier_split(closure.SIGNED_SHIELDED_MASKS)[1]
    assert local <= positive_residual
    assert not (local & signed_residual)

    _, _, residual = feasibility._residual_failures()
    affine_branch = frozenset(
        pair
        for pair in residual
        if not feasibility.feasible_failing_descriptors(pair)
    )
    rank_two_branch = frozenset(
        pair for pair, _ in rank_two._rank_two_rows()
    )
    all_active_only_branch = all_active_only.selected_pairs()
    h_b_seams = frozenset(
        pair for pair, _, _ in all_active.curvature_obstructions()
    )
    assert not (local & affine_branch)
    assert not (local & rank_two_branch)
    assert not (local & all_active_only_branch)
    assert not (local & h_b_seams)
    assert not (candidate & affine_branch)
    assert not (candidate & rank_two_branch)
    assert not (candidate & all_active_only_branch)

    branch_histogram = Counter(row["all_active_branch"] for row in rows)
    candidate_histogram = Counter(
        row["all_active_branch"]
        for row in rows
        if row["candidate_pair_level_composable"]
    )
    active_count_histogram = Counter(
        ",".join(map(str, row["feasible_failure_active_counts"]))
        for row in rows
    )

    encoded_rows = json.dumps(
        rows, sort_keys=True, separators=(",", ":")
    ).encode()
    rows_hash = sha256(encoded_rows).hexdigest()
    assert rows_hash == EXPECTED_ROWS_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "audited common-potential closure for feasible failures with "
            "at least two active coordinates, plus independently audited "
            "pair-level recurrence for the exact 141-pair subset without "
            "a one-active obstruction"
        ),
        "rank_one_pairs": len(flat),
        "rank_one_pairs_with_promotion": len(flat & promotions),
        "no_promotion_local_pairs": len(local),
        "local_all_active_branch_histogram": dict(
            sorted(branch_histogram.items())
        ),
        "feasible_failure_active_count_histogram": dict(
            sorted(active_count_histogram.items())
        ),
        "pairs_with_one_active_obstruction": len(one_active),
        "pair_level_recurrent_pairs": len(candidate),
        "candidate_pair_level_composable_pairs": len(candidate),
        "candidate_all_active_branch_histogram": dict(
            sorted(candidate_histogram.items())
        ),
        "all_local_pairs_are_positive_residual": True,
        "dimension_at_least_two_common_potential_certified": True,
        "pair_level_recurrence_certified": True,
        "global_t3_2_certified": False,
        "ordered_prior_overlap": {
            "affine_151": len(candidate & affine_branch),
            "rank_two_14": len(candidate & rank_two_branch),
            "all_active_only_51": len(candidate & all_active_only_branch),
            "h_b_seam_12": len(candidate & h_b_seams),
        },
        "positive_remainder_before": 2104,
        "positive_remainder_after": 1963,
        "signed_remainder_before": 191,
        "signed_remainder_after": 191,
        "local_pair_sha256": closure.pair_fingerprint(local),
        "candidate_pair_sha256": closure.pair_fingerprint(candidate),
        "rows_sha256": rows_hash,
        "rows": rows,
    }
    assert payload["local_pair_sha256"] == EXPECTED_LOCAL_PAIR_SHA256
    assert (
        payload["candidate_pair_sha256"]
        == EXPECTED_CANDIDATE_PAIR_SHA256
    )
    return payload


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
