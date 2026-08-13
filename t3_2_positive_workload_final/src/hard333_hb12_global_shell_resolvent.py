"""Claim-neutral guard-free shell-resolvent target for the H_b twelve.

The earlier killed-shell target used a logarithmic pathwise guard.  That
guard is false on exact-tier sequences whose smallest center coordinate is
much smaller than the logarithm of the largest coordinate.  This repair
stops only at the first lower-linkage reaction and uses exact polynomial
size bias of the reversible top-shell factorial law plus same-state Kac
regeneration.  Boundary visits are allowed and every physical clock is
retained.

The module freezes finite D-tier exponents, dominant lower source sets, the
countersequence to the old guard, and the analytic resolvent contract.  It
does not certify the Kac moment bounds, common-factorial endpoint, pair
recurrence, or global theorem; all such flags remain false.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import hard333_pair_composition as composition
import prospective_no_promotion_26 as atlas
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import three_active_gluing_gate as all_active
import two_active_dormant_407_certificate as hard
import two_active_phase_gate as two_active


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = composition.EXPECTED_HB_12_SHA256
EXPECTED_ROWS_SHA256 = (
    "3999b185f5626b0999d72e9c10d3cdf082054f70cd84af8cd43a52aa6f286c7a"
)
EXPECTED_PAYLOAD_SHA256 = (
    "f750d01ff8c0ea884df27cf8e4625f6d6ef020f8d335c6086f6c1147c0934417"
)


def _encoded_sha256(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _pair_payload(pair: Pair) -> list[list[str]]:
    return [list(part) for part in closure.pair_payload(pair)]


def _vector(name: str) -> tuple[int, int, int]:
    return closure.COMPLEXES[closure.NAME_TO_INDEX[name]]


def _weight(name: str, descriptor_weight: tuple[int, int, int]) -> int:
    return sum(
        value * exponent
        for value, exponent in zip(_vector(name), descriptor_weight)
    )


@lru_cache(maxsize=1)
def selected_pairs() -> frozenset[Pair]:
    result = composition.hb_switch_pairs()
    assert len(result) == 12
    assert closure.pair_fingerprint(result) == EXPECTED_PAIR_SHA256
    return result


@lru_cache(maxsize=1)
def resolvent_rows() -> tuple[dict[str, object], ...]:
    """Freeze all sixteen gap/hazard comparisons and polynomial tilts."""

    selected = selected_pairs()
    rows: list[dict[str, object]] = []
    for pair, descriptor, recorded_excess in all_active.curvature_obstructions():
        if pair not in selected:
            continue
        top_side, top = flat.whole_top_linkage(pair, descriptor)
        assert closure.support(top) == ("2A", "BC")
        lower = pair[1 - top_side]
        lower_support = closure.support(lower)
        weights = {
            name: _weight(name, descriptor.weight) for name in lower_support
        }
        lower_exponent = max(weights.values())
        dominant_sources = tuple(
            name for name in lower_support if weights[name] == lower_exponent
        )
        top_exponents = {
            _weight(name, descriptor.weight) for name in closure.support(top)
        }
        top_exponent, = top_exponents
        smallest_index = min(
            range(3), key=lambda index: descriptor.weight[index]
        )
        gap_exponent = top_exponent - descriptor.weight[smallest_index]
        computed_excess = gap_exponent - lower_exponent
        assert computed_excess == recorded_excess
        assert computed_excess in (1, 2)

        rows.append(
            {
                "pair": _pair_payload(pair),
                "weight": list(descriptor.weight),
                "caps": list(descriptor.caps),
                "top_support": ["2A", "BC"],
                "lower_support": list(lower_support),
                "smallest_center_coordinate": ("A", "B", "C")[
                    smallest_index
                ],
                "top_source_exponent": top_exponent,
                "top_relaxation_gap_exponent": gap_exponent,
                "lower_hazard_exponent": lower_exponent,
                "relaxation_over_killing_excess": computed_excess,
                "dominant_lower_sources": list(dominant_sources),
                "dominant_source_max_degree": max(
                    sum(_vector(name)) for name in dominant_sources
                ),
                "lower_hazard_is_finite_factorial_tilt_sum": True,
                "top_balance_identity": (
                    2 * descriptor.weight[0]
                    == descriptor.weight[1] + descriptor.weight[2]
                ),
            }
        )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    assert len(rows) == 16
    return tuple(rows)


def lower_dimensional_routing() -> dict[str, object]:
    selected = selected_pairs()
    failure_histogram = Counter(
        len(tier._active_coordinates(descriptor))
        for pair in selected
        for descriptor in atlas.failures(pair)
    )
    two_histogram = Counter(
        category
        for pair, _descriptor, category in two_active.incidences()
        if pair in selected
    )
    selected_payloads = {closure.pair_payload(pair) for pair in selected}
    one_histogram = Counter(
        row["structural_family"]
        for row in hard.one_active_rows()
        if tuple(tuple(part) for part in row["pair"]) in selected_payloads
    )
    assert failure_histogram == {1: 38, 2: 48, 3: 60}
    assert two_histogram == {
        "closed_rank_one_top_phase": 36,
        "promotion_dormant_top": 12,
    }
    assert one_histogram == {
        "generalized_family_ii": 36,
        "direct_physical_C": 2,
    }
    return {
        "failure_incidence_histogram": {
            str(key): value for key, value in sorted(failure_histogram.items())
        },
        "two_active_48": dict(sorted(two_histogram.items())),
        "one_active_38": dict(sorted(one_histogram.items())),
    }


def false_guard_countersequence() -> dict[str, object]:
    return {
        "descriptor_weight": [3, 1, 5],
        "center_sequence": (
            "B=m, C=ceil(exp(m^2)), A adjusted so A^2/(B*C)->1"
        ),
        "same_D_tier_order": (
            "2C>AC>{2A,BC}>C>AB>A>2B>B>0"
        ),
        "smallest_center_scale": "B is asymptotic to m",
        "log_largest_scale": "log(C) is asymptotic to m^2",
        "old_log_largest_guard_reaches_B_zero": True,
        "old_q_ratio_uniform_on_guard": False,
        "pathwise_boundary_avoidance_required_by_repair": False,
    }


def claim_neutral_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    selected = selected_pairs()
    assert (len(selected & positive), len(selected & signed)) == (12, 0)
    return {
        "candidate_H_b_12": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected),
        },
        "claim_neutral_after": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "unchanged": True,
        },
    }


def certificate() -> dict[str, object]:
    rows = resolvent_rows()
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    excess_histogram = Counter(
        row["relaxation_over_killing_excess"] for row in rows
    )
    dominant_histogram = Counter(
        tuple(row["dominant_lower_sources"]) for row in rows
    )
    assert excess_histogram == {1: 12, 2: 4}
    assert dominant_histogram == {
        ("AB",): 5,
        ("AC",): 5,
        ("A",): 2,
        ("A", "2B"): 1,
        ("A", "2C"): 1,
        ("2B",): 1,
        ("2C",): 1,
    }

    payload: dict[str, object] = {
        "claim_scope": (
            "finite premises and unaudited guard-free Kac-resolvent "
            "common-factorial target for the exact hard H_b twelve"
        ),
        "selector": {
            "pairs": 12,
            "positive": 12,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "curvature_incidences": 16,
            "relaxation_over_killing_excess_histogram": {
                str(key): value for key, value in sorted(excess_histogram.items())
            },
        },
        "exact_stationary_size_bias": {
            "top_stationary_law": (
                "pi_q(x)=Z_q^-1*theta^x/prod_i(x_i!) on each finite "
                "2A<->BC shell"
            ),
            "single_source_identity": (
                "(x)_u*pi_q(x) is a constant times the law of Z+u, "
                "where Z has the stationary law on the invariant shell "
                "shifted by u"
            ),
            "product_identity": (
                "(x)_u*(x)_v is a finite nonnegative combination of "
                "falling factorials (x)_(u+v-r), of total degree at most 4"
            ),
            "target_consequences": (
                "uniform fixed moments of q/(pi q), bounded q-size-biased "
                "factorial energy, and bounded coefficient of variation"
            ),
        },
        "candidate_same_state_regeneration": {
            "stopping_rule": "the first lower-linkage reaction; no guard",
            "cycle": (
                "from a bounded-energy core state x, let T be the first "
                "positive return time of the top birth-death chain to x"
            ),
            "common_shifted_potential": (
                "G_ell=K_ell+sum_i log(x_i!)+ell dot x>=1, with one "
                "rate-dependent K_ell independent of the top shell; "
                "W_ell=G_ell^4"
            ),
            "cycle_integrals": [
                "H=int_0^T q_R(X_t)dt",
                "R=int_0^T L_R G_ell(X_t)dt",
            ],
            "Kac_identities": [
                "E H=E T*pi(q_R)",
                "E R=E T*pi(L_R G_ell)",
            ],
            "small_parameter": (
                "epsilon=pi(q_R)/gap(Q), which tends to zero with exact "
                "D-tier excess 1 or 2"
            ),
            "moment_targets": [
                "E H^2<=C*epsilon*E H",
                "sqrt(pi((L_R G_ell)^2))<=C*pi(q_R)*g",
                "E[H*int_0^T abs(L_R G_ell)dt]"
                "<=C*epsilon*E H*g",
            ],
            "renewal_target": (
                "the killed payoff equals pi(L_R G_ell)/pi(q_R)+o(g) "
                "uniformly on the bounded-energy core"
            ),
            "terminal_jump_moment_target": {
                "definition": (
                    "h_j=sum_e q_e*abs(Delta_e G_ell)^j over lower edges"
                ),
                "stationary_bound": (
                    "pi(h_j)/pi(q_R)<=C_j*(1+L_Q)^j for 1<=j<=p, "
                    "where L_Q=max_i log(1+x_i^*) and p>8"
                ),
                "renewal_consequence": (
                    "the actual terminal lower jump and total stopped "
                    "G_ell increment have moments <=C_j*(1+L_Q)^j"
                ),
            },
            "duration_moment_target": (
                "E_x[tau_R^j]<=C_j/pi(q_R)^j for every fixed 1<=j<=p"
            ),
            "all_reactions_retained": True,
        },
        "terminal_reward_target": {
            "mixed_quadratic_rows": 10,
            "double_only_rows": 6,
            "stationary_ratio": (
                "pi(L_R G_ell)/pi(q_R)<=-g with g tending to infinity"
            ),
            "fourth_power_remainder_condition": (
                "L_Q^2/(G_ell*g)->0 and L_Q/G_ell->0 along every "
                "escaping all-active curvature sequence"
            ),
            "core_complement_target": (
                "the top-shell flux branch and lower factorial high-cut "
                "branch are separately pointwise negative; no condition "
                "gamma/(pi(q_R)*g)->infinity is used"
            ),
            "candidate_common_W_drift": (
                "E[W_ell(X_tau)-W_ell(x)+tau]"
                "<=-c*G_ell(x)^3*g"
            ),
        },
        "withdrawn_guard": false_guard_countersequence(),
        "lower_dimensional_routing": lower_dimensional_routing(),
        "resolvent_rows": list(rows),
        "claim_neutral_arithmetic": claim_neutral_arithmetic(),
        "hashes": {"rows_sha256": rows_hash},
        "stationary_size_bias_moment_lemma_certified": False,
        "same_state_kac_moment_lemma_certified": False,
        "guard_free_killed_resolvent_certified": False,
        "terminal_lower_jump_moments_certified": False,
        "duration_moments_certified": False,
        "uniform_terminal_reward_certified": False,
        "pointwise_core_complement_certified": False,
        "common_W_endpoint_certified": False,
        "H_b_12_pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = _encoded_sha256(payload)
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    return {**payload, "payload_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
