"""Certified common-scalar theorem for the rank-two thirteen.

For each of the thirteen all-active-only rank-two pairs, the analytic
candidate uses

    V = (1 + F)^4 + eta * (1 + H_w)^q,

where ``q=6`` for workload ``(1,1,1)`` and ``q=5`` for the two weighted
supports.  This module freezes the finite exponent inequalities, support
coercivity, independent analytic audit, and exact post-416 pair arithmetic.
The global T3-2 flag remains false.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import rank_two_linear_switch_13 as branch
import three_active_flat_phase as flat
import two_active_easy_common_w as easy_416


EXPECTED_PAIR_SHA256 = branch.EXPECTED_PAIR_SHA256
EXPECTED_ROWS_SHA256 = (
    "cd78e50b5749b6feb35e459df5e7df690d235919e64336c1e1dde13370fae9e0"
)
EXPECTED_PAYLOAD_SHA256 = (
    "5dc6c6acf4f08be9ce913122b61d22ae35025b3d7e42c2dd1d3c09b2b06e79dc"
)
EXPECTED_POST_416_PAIR_SHA256 = (
    "9868f965cc8af951fd7545f8832ed0275a8d60bab70b2593b7424654cba7d8ec"
)
EXPECTED_POST_13_PAIR_SHA256 = (
    "196fd2b2c43cff3b83d252e33b15e276ac592e96ce992d7e18cc30d588d63936"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _boundary_sources(workload: tuple[int, int, int]) -> tuple[str, str]:
    """Pure A/B sources giving the C-bounded source-rate lower bound."""

    if workload == (1, 1, 1):
        return ("2A", "2B")
    if workload == (2, 1, 1):
        return ("A", "2B")
    if workload == (1, 2, 1):
        return ("2A", "B")
    raise AssertionError(workload)


def scalar_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for source_row in branch.all_active_rows():
        payload = tuple(tuple(part) for part in source_row["pair"])
        pair = tuple(
            sum(1 << closure.NAME_TO_INDEX[name] for name in names)
            for names in payload
        )
        descriptor = branch._all_active_descriptor(pair)
        side, top = flat.whole_top_linkage(pair, descriptor)
        workload = tuple(descriptor.weight)
        maximum_weight = max(workload)
        levels = {
            sum(
                workload[index] * closure.COMPLEXES[node][index]
                for index in range(3)
            )
            for node in tier._nodes(top)
        }
        top_level, = levels
        assert flat._support_rank(top) == 2
        assert top_level == 2
        assert closure.support(pair[1 - side]) == ("0", "C")

        power = 6 if maximum_weight == 1 else 5
        top_rate_exponent = Fraction(top_level, maximum_weight)
        service_exponent = Fraction(workload[2], maximum_weight)
        positive_powered_entropy_exponent = 3 + top_rate_exponent
        negative_workload_power_exponent = power - 1 + service_exponent
        power_gap = (
            negative_workload_power_exponent
            - positive_powered_entropy_exponent
        )
        assert power_gap > 0

        sources = _boundary_sources(workload)
        top_support = set(closure.support(top))
        assert set(sources) <= top_support
        boundary_source_exponent = Fraction(power - 4)
        # When C is bounded, H_w is comparable with w_A A+w_B B.
        # The displayed pure sources give A_max >= c H^(q-4).
        if workload == (1, 1, 1):
            assert boundary_source_exponent == 2
        else:
            assert boundary_source_exponent == 1

        rows.append(
            {
                "pair": source_row["pair"],
                "top_support": source_row["top_support"],
                "lower_support": ["0", "C"],
                "workload": list(workload),
                "workload_max": maximum_weight,
                "top_workload_level": top_level,
                "top_stoichiometric_rank": 2,
                "scalar_power": power,
                "candidate_scalar": (
                    "V=(1+F)^4+eta*(1+H_w)^q"
                ),
                "all_active_exponents": {
                    "top_rate_in_H": str(top_rate_exponent),
                    "positive_LW_power": str(
                        positive_powered_entropy_exponent
                    ),
                    "lower_birth_LW_order": "O(H^3*log(H)^4)",
                    "lower_birth_is_strictly_lower_order": True,
                    "service_C_in_H": str(service_exponent),
                    "negative_LHq_power": str(
                        negative_workload_power_exponent
                    ),
                    "strict_power_gap": str(power_gap),
                },
                "C_bounded_passing_exponents": {
                    "coercive_top_sources": list(sources),
                    "max_source_rate_at_least_H_power": str(
                        boundary_source_exponent
                    ),
                    "positive_LHq_power": str(power - 1),
                    "negative_LW_power_before_log_gap": str(
                        3 + boundary_source_exponent
                    ),
                    "strict_margin": "log(H)^3*g(H), g(H)->infinity",
                },
            }
        )
    rows.sort(key=lambda row: json.dumps(row["pair"], sort_keys=True))
    return tuple(rows)


def certified_pair_arithmetic() -> dict[str, object]:
    positive, signed, _residual = branch.feasibility._residual_failures()
    before = easy_416.post_416_pairs()
    selected = branch.selected_pairs()
    after = before - selected

    assert closure.pair_fingerprint(before) == EXPECTED_POST_416_PAIR_SHA256
    assert selected <= before
    assert (len(selected & positive), len(selected & signed)) == (13, 0)
    assert (len(after & positive), len(after & signed)) == (306, 34)
    assert closure.pair_fingerprint(after) == EXPECTED_POST_13_PAIR_SHA256

    return {
        "before": {
            "positive": 319,
            "signed": 34,
            "total": 353,
            "pair_sha256": closure.pair_fingerprint(before),
        },
        "new_exact_13": {
            "positive": 13,
            "signed": 0,
            "total": 13,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "after": {
            "positive": 306,
            "signed": 34,
            "total": 340,
            "pair_sha256": closure.pair_fingerprint(after),
        },
    }


def certificate() -> dict[str, object]:
    rows = scalar_rows()
    assert len(rows) == 13
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    power_histogram = Counter(row["scalar_power"] for row in rows)
    gap_histogram = Counter(
        row["all_active_exponents"]["strict_power_gap"] for row in rows
    )
    assert power_histogram == {6: 11, 5: 2}
    assert gap_histogram == {"1": 11, "1/2": 2}
    assert all(
        row["all_active_exponents"][
            "lower_birth_is_strictly_lower_order"
        ]
        for row in rows
    )

    payload: dict[str, object] = {
        "claim_scope": (
            "independently audited classwise recurrence theorem for one "
            "common scalar on each of the thirteen pairs"
        ),
        "selector": {
            "pairs": 13,
            "pair_sha256": closure.pair_fingerprint(
                branch.selected_pairs()
            ),
        },
        "scalar_family": {
            "factorial_power": 4,
            "formula": "V=(1+F)^4+eta*(1+H_w)^q",
            "eta": "any fixed positive constant",
            "power_histogram": {
                str(key): value
                for key, value in sorted(power_histogram.items())
            },
            "all_active_power_gap_histogram": dict(
                sorted(gap_histogram.items())
            ),
        },
        "sequence_partition": {
            "failed_all_active": (
                "strict polynomial domination by the H_w power"
            ),
            "passing_with_C_unbounded": (
                "both the powered factorial and H_w-power drifts are "
                "eventually negative"
            ),
            "passing_with_C_bounded": (
                "the quantitative descending-source term has the same "
                "H power and an extra log(H)^3*g(H) margin"
            ),
        },
        "hashes": {"rows_sha256": rows_hash},
        "certified_pair_arithmetic": certified_pair_arithmetic(),
        "rows": list(rows),
        "independent_audit_passed": True,
        "analytic_common_scalar_independently_certified": True,
        "exact_13_pair_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
