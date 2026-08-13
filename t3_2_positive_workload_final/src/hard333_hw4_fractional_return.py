"""Claim-neutral fractional-return candidate for the four hard H_w pairs.

Each selected pair has lower linkage ``0 <-> C`` and a homogeneous
rank-two top linkage.  The finite certificate identifies the unique
service-zero dormant vertex and whether one or two ``0 -> C`` seeds are
needed before a top clock is enabled there.  The analytic candidate repeats
an all-reactions-retained activation/service macroepisode until total
population contracts by a fixed fraction.  No analytic or recurrence flag
is set before independent audit.
"""

from __future__ import annotations

from hashlib import sha256
from functools import lru_cache
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard333_pair_composition as composition
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import two_active_dormant_407_certificate as hard


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = composition.EXPECTED_HW_4_SHA256
EXPECTED_AFTER_PAIR_SHA256 = composition.EXPECTED_HB_12_SHA256
EXPECTED_ROWS_SHA256 = (
    "f182123a34c92cf1e2477f3b2aabc0510554882d7a2eb74a3da7f46db0c703bb"
)
EXPECTED_PAYLOAD_SHA256 = (
    "1fcc914b9848e55defab0279670c79f64b69911aa19fc7233bd22d816218fc9b"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@lru_cache(maxsize=1)
def selected_pairs() -> frozenset[Pair]:
    result = composition.hw_switch_pairs()
    assert len(result) == 4
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


@lru_cache(maxsize=1)
def remaining_H_b_pairs() -> frozenset[Pair]:
    result = composition.hb_switch_pairs()
    assert len(result) == 12
    assert closure.pair_fingerprint(result) == EXPECTED_AFTER_PAIR_SHA256
    return result


def _top_linkage(pair: Pair) -> int:
    lower = tuple(
        side
        for side, linkage in enumerate(pair)
        if closure.support(linkage) == ("0", "C")
    )
    lower_side, = lower
    return pair[1 - lower_side]


def geometry_rows() -> tuple[dict[str, object], ...]:
    hard_lookup = {
        json.dumps(row["pair"], separators=(",", ":")): row
        for row in hard.normalized_rows()
    }
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        payload = [list(part) for part in closure.pair_payload(pair)]
        top = _top_linkage(pair)
        support = closure.support(top)
        service_free = tuple(name for name in support if "C" not in name)
        dormant = tuple(
            species for species in ("A", "B") if f"2{species}" not in support
        )
        dormant_vertex, = dormant
        carrier = f"{dormant_vertex}C"
        seed_resistance = 1 if carrier in support else 2
        hard_row = hard_lookup[json.dumps(payload, separators=(",", ":"))]

        all_active = tuple(
            descriptor
            for candidate, descriptor in flat.feasible_all_active_incidences()
            if candidate == pair
        )
        descriptor, = all_active
        side, certified_top = flat.whole_top_linkage(pair, descriptor)
        assert certified_top == top
        assert descriptor.weight == (1, 1, 1)
        assert flat._support_rank(top) == 2
        assert {
            sum(closure.COMPLEXES[node]) for node in tier._nodes(top)
        } == {2}
        assert "2C" in support
        assert seed_resistance in (1, 2)
        assert hard._resistance_class(hard_row) == 0

        rows.append(
            {
                "pair": payload,
                "top_support": list(support),
                "lower_support": ["0", "C"],
                "top_rank": 2,
                "top_preserves_total_population": True,
                "all_active_workload": [1, 1, 1],
                "service_zero_sources": list(service_free),
                "unique_service_zero_dormant_vertex": dormant_vertex,
                "dormant_service_carrier": carrier,
                "carrier_present": carrier in support,
                "activation_seed_resistance": seed_resistance,
                "two_seed_source_when_carrier_absent": (
                    None if seed_resistance == 1 else "2C"
                ),
                "hard_dormant_normalized_ratio": hard_row["normalized_ratio"],
                "hard_dormant_proper_support": hard_row["proper_support"],
            }
        )
    return tuple(rows)


def claim_neutral_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    selected = selected_pairs()
    before = selected | remaining_H_b_pairs()
    after = before - selected
    assert after == remaining_H_b_pairs()
    assert (len(selected & positive), len(selected & signed)) == (4, 0)
    assert (len(after & positive), len(after & signed)) == (12, 0)
    assert closure.pair_fingerprint(after) == EXPECTED_AFTER_PAIR_SHA256
    return {
        "candidate_before": {
            "pairs": 16,
            "positive": 16,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(before),
        },
        "candidate_H_w_4": {
            "pairs": 4,
            "positive": 4,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "claim_neutral_after": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(after),
            "equals_exact_H_b_12": True,
        },
    }


def certificate() -> dict[str, object]:
    rows = geometry_rows()
    assert len(rows) == 4
    assert sorted(row["activation_seed_resistance"] for row in rows) == [1, 1, 2, 2]
    assert {row["unique_service_zero_dormant_vertex"] for row in rows} == {
        "A",
        "B",
    }
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    payload: dict[str, object] = {
        "claim_scope": (
            "finite premises and unaudited fractional-population return "
            "contract for the four hard H_w switches"
        ),
        "selector": {
            "pairs": 4,
            "positive": 4,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "activation_resistance_histogram": {"1": 2, "2": 2},
        },
        "one_macroepisode_contract": {
            "activation": (
                "from the unique dormant vertex, obtain one carrier seed "
                "directly or obtain 2C first; repeat with exponential seed tails"
            ),
            "service": (
                "from a compact normalized shell away from the dormant "
                "vertex, use divergent deterministic integrated C and a "
                "full-chain T/N service window"
            ),
            "population_increment": (
                "uniform negative conditional mean and a uniform positive "
                "exponential moment"
            ),
            "all_reactions_retained": True,
        },
        "repeated_fractional_return_contract": {
            "stopping_shell": "n<=rho*n0 or n>=2*n0, with fixed 0<rho<1",
            "upper_exit_probability": "exp(-c*n0)",
            "episode_count_moments": "E J^m <= C_m*(1+n0)^m",
            "physical_duration_moments": "E tau^m <= C_m*(1+n0)^m",
            "required_endpoint_order": "choose integer m>8",
        },
        "common_W_endpoint": {
            "potential": "W_ell=(K_ell+sum log(x_i!)+ell dot x)^4",
            "contraction_envelope": (
                "n_tau<=rho*n0 implies F_ell(X_tau)-F_ell(x) "
                "<=-c*n0*log(n0) uniformly over redistribution"
            ),
            "candidate_stopped_drift": (
                "E[W_ell(X_tau)-W_ell(x)+tau] "
                "<=-c*(n0*log(n0))^4"
            ),
        },
        "geometry_rows": list(rows),
        "claim_neutral_arithmetic": claim_neutral_arithmetic(),
        "hashes": {"rows_sha256": rows_hash},
        "independent_analytic_audit_passed": False,
        "single_macroepisode_service_certified": False,
        "fractional_return_iteration_certified": False,
        "common_W_endpoint_certified": False,
        "H_w_4_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
