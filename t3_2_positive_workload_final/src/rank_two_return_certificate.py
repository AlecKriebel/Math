"""Exact support partition used by the certified rank-two return theorem.

The executable checks finite support geometry and records the independently
audited theorem status.  It does not itself prove the analytic stopping-time
estimates in the accompanying note.
"""

from __future__ import annotations

from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import two_active_phase_gate as phase


def _rank_two_rows():
    return tuple(
        (pair, descriptor)
        for pair, descriptor, category in phase.incidences()
        if category == "coupled_rank_two_top_phase"
    )


def _lower_mask(pair, descriptor):
    top = phase._whole_top_linkages(pair, descriptor)[0]
    return pair[1] if pair[0] == top else pair[0]


def certificate() -> dict[str, object]:
    rows = _rank_two_rows()
    pairs = frozenset(pair for pair, _ in rows)
    lower_masks = frozenset(_lower_mask(pair, descriptor) for pair, descriptor in rows)
    names = {name: tier.NAMES.index(name) for name in ("0", "A", "C", "2C", "AC")}
    with_2c = frozenset(mask for mask in lower_masks if names["2C"] in tier._nodes(mask))
    ac_only = lower_masks - with_2c
    c_present = frozenset(mask for mask in ac_only if names["C"] in tier._nodes(mask))
    dormant = ac_only - c_present

    expected_ac_only = {
        frozenset(("0", "A", "AC")),
        frozenset(("0", "C", "AC")),
        frozenset(("A", "C", "AC")),
        frozenset(("0", "A", "C", "AC")),
    }
    actual_ac_only = {
        frozenset(closure.support(mask))
        for mask in ac_only
    }
    assert actual_ac_only == expected_ac_only
    assert {
        tuple(closure.support(mask)) for mask in dormant
    } == {("0", "A", "AC")}
    assert all(names["AC"] in tier._nodes(mask) for mask in ac_only)
    assert all(
        tier._nodes(mask)
        <= {names[name] for name in ("0", "A", "C", "2C", "AC")}
        for mask in lower_masks
    )
    positive_table = closure.unique_pairs(closure.POSITIVE_SHIELDED_MASKS)
    signed_table = closure.unique_pairs(closure.SIGNED_SHIELDED_MASKS)
    assert pairs <= positive_table
    assert not (pairs & signed_table)
    residual_overlap = frozenset(
        pair for pair in pairs if closure.is_exact_residual_pair(pair)
    )
    # The phase classifier starts after the exact residual branch has already
    # been removed.  The fourteen-partner family therefore does not contain
    # the earlier {0,A,C} theorem, despite sharing the same top support.
    assert not residual_overlap

    supports = [
        list(closure.support(mask))
        for mask in sorted(
            lower_masks,
            key=lambda value: (value.bit_count(), closure.support(value)),
        )
    ]
    fingerprint = sha256(
        json.dumps(supports, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "rank_two_incidences": len(rows),
        "support_pairs": len(pairs),
        "lower_supports": len(lower_masks),
        "with_2c_supports": len(with_2c),
        "ac_only_vertical_supports": len(ac_only),
        "c_present_linear_phase_supports": len(c_present),
        "dormant_activation_supports": len(dormant),
        "supports": supports,
        "support_sha256": fingerprint,
        "previous_exact_residual_overlap": 0,
        "new_positive_table_pairs": len(pairs),
        "new_signed_table_pairs": 0,
        "positive_remainder_before": 2169,
        "positive_remainder_after": 2169 - len(pairs),
        "signed_remainder_before": 191,
        "signed_remainder_after": 191,
        "analytic_theorem_certified": True,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
