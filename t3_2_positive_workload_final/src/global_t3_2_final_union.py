"""Exact final union of the independently proved residual pair branches.

The baseline is the 2,511-pair residual left by the global support/tier and
exact physical branches.  This module checks set identities only.  It does
not turn any candidate analytic input into a theorem.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

import global_atlas_interface_closure as closure
import hard333_final_descriptor_coverage as hard_coverage
import one_active_phase_shape as one_active
import one_active_prospective_composition as prospective
import prospective_no_promotion_26 as exact26
import rank_two_linear_switch_13 as linear13
import rank_two_mixed_profile_7_stopped_service as final7
import stoichiometric_gate_feasibility as feasibility
import two_active_dormant_407_certificate as hard
import two_active_easy_common_w as easy416


Pair = closure.Pair

EXPECTED_ROWS_SHA256 = (
    "9e9c6be443216f3a6d05795fcf0dcf25170ce020371c6bffde25eb316e52ad27"
)
EXPECTED_PAYLOAD_SHA256 = (
    "4a1542367400376de42fec24ddabe328bd3489c91c246e8d70def32bcd78cb33"
)


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def disjoint_final_branches() -> dict[str, frozenset[Pair]]:
    prior = prospective.certified_branch_sets()
    prior_union = frozenset().union(*prior.values())
    universal = frozenset(one_active.candidate_pairs()) - prior_union
    branches = {
        **prior,
        "universal_one_active_net_1212": universal,
        "exact_common_w_26": exact26.selected_pairs(),
        "easy_common_w_416": easy416.fully_easy_promotion_pairs(),
        "rank_two_scalar_13": linear13.selected_pairs(),
        "rank_two_stopped_7": final7.branch.selected_pairs(),
        "hard_common_w_333": hard.selected_pairs(),
    }
    names = tuple(sorted(branches))
    assert all(
        not (branches[left] & branches[right])
        for left, right in combinations(names, 2)
    )
    return branches


def rows() -> tuple[dict[str, object], ...]:
    positive, signed, residual = feasibility._residual_failures()
    branches = disjoint_final_branches()
    owner: dict[Pair, str] = {}
    for name, branch in branches.items():
        for pair in branch:
            assert pair not in owner
            owner[pair] = name
    assert frozenset(owner) == residual
    result = tuple(
        {
            "pair": [list(part) for part in closure.pair_payload(pair)],
            "stratum": "positive" if pair in positive else "signed",
            "analytic_branch": owner[pair],
        }
        for pair in sorted(residual, key=closure.pair_payload)
    )
    assert len(result) == 2511
    assert sum(row["stratum"] == "positive" for row in result) == 2312
    assert sum(row["stratum"] == "signed" for row in result) == 199
    return result


def certificate() -> dict[str, object]:
    positive, signed, residual = feasibility._residual_failures()
    branches = disjoint_final_branches()
    data = rows()
    rows_hash = _digest(data)
    branch_payload = {
        name: {
            "pairs": len(branch),
            "positive": len(branch & positive),
            "signed": len(branch & signed),
            "pair_sha256": closure.pair_fingerprint(branch),
        }
        for name, branch in sorted(branches.items())
    }
    union = frozenset().union(*branches.values())
    assert union == residual
    assert len(hard_coverage.pair_rows()) == len(hard.selected_pairs()) == 333

    payload = {
        "claim_scope": (
            "exact disjoint exhaustion of the 2,511-pair post-interface "
            "residual by analytic theorem branches"
        ),
        "baseline": {
            "pairs": len(residual),
            "positive": len(positive),
            "signed": len(signed),
            "pair_sha256": closure.pair_fingerprint(residual),
        },
        "branches": branch_payload,
        "pairwise_disjoint": True,
        "union_equals_baseline": True,
        "remaining_pairs": 0,
        "rows_sha256": rows_hash,
        "finite_code_role": "set exhaustion only; no analytic proof",
        "hard333_pair_recurrence_input_certified": False,
        "global_t3_2_theorem_independently_audited": False,
        "global_t3_2_certified": False,
    }
    payload_hash = _digest(payload)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert payload_hash == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": payload_hash}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
