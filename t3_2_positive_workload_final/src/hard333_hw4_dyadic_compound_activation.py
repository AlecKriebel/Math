"""Claim-neutral dyadic compound-activation target for the hard H_w four.

The one-level transverse-mass comparison in the preceding repair is false:
many pure-to-mixed reactions can occur before a carrier clock catches up.
The exact replacement uses a weighted transverse coordinate.  After
relabeling, the resistance-two rows use ``R=2Y+C`` and have minimum-height
complexes ``{2C,XY}``; the resistance-one rows use ``R=Y+2C`` and have
minimum-height complexes ``{2Y,XC}``.  The accumulated mass dips in the
sparse counterorientation preserve this ``R`` exactly.

This module freezes the four supports, the two height tables, every strong
four-node digraph's distance from the minimum class to a strict height cut,
and an unaudited dyadic ascent/service/endpoint contract.  All analytic,
recurrence, and global flags remain false pending independent replay.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import hard333_pair_composition as composition
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import two_active_dormant_407_certificate as hard


Pair = closure.Pair

EXPECTED_PAIR_SHA256 = composition.EXPECTED_HW_4_SHA256
EXPECTED_ROWS_SHA256 = (
    "e80426c2363dca89d51a7a7e7cf845f64c807a8df76971c35c15941311d1ec70"
)
EXPECTED_CUT_PROFILE_SHA256 = (
    "2f48ace8a269e1a8ab2c6eb7e770b7d69f9f20a8d396b9468368b1c1d3a5a54f"
)
EXPECTED_PAYLOAD_SHA256 = (
    "57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7"
)

CANONICAL_NODES = ("2Y", "2C", "YC", "XY")
ARCS = tuple(
    (source, target)
    for source in range(4)
    for target in range(4)
    if source != target
)
RESISTANCE_TWO_MINIMUM = frozenset((1, 3))
RESISTANCE_TWO_HIGH = frozenset((0, 2))


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


def _hard_rows() -> dict[str, dict[str, object]]:
    return {
        json.dumps(row["pair"], separators=(",", ":")): row
        for row in hard.normalized_rows()
    }


def geometry_rows() -> tuple[dict[str, object], ...]:
    hard_rows = _hard_rows()
    rows: list[dict[str, object]] = []
    for pair in sorted(selected_pairs(), key=closure.pair_payload):
        payload = [list(part) for part in closure.pair_payload(pair)]
        lower_sides = [
            side
            for side, linkage in enumerate(pair)
            if closure.support(linkage) == ("0", "C")
        ]
        lower_side, = lower_sides
        top = pair[1 - lower_side]
        support = closure.support(top)
        dormant, = (
            species for species in ("A", "B") if f"2{species}" not in support
        )
        transverse = "B" if dormant == "A" else "A"
        xy_name = "".join(sorted((dormant, transverse)))
        xc_name = f"{dormant}C"
        seed_resistance = 2 if xy_name in support else 1
        if seed_resistance == 2:
            relabelled = ["2Y", "2C", "YC", "XY"]
            weighted_coordinate = "R=2Y+C"
            heights = {"2Y": 4, "2C": 2, "YC": 3, "XY": 2}
            minimum = ["2C", "XY"]
            high = ["YC", "2Y"]
            minimum_propensity = "C*(C-1)+X*Y"
            high_propensity = "Y*(Y-1)+Y*C"
        else:
            relabelled = ["2Y", "2C", "YC", "XC"]
            weighted_coordinate = "R=Y+2C"
            heights = {"2Y": 2, "2C": 4, "YC": 3, "XC": 2}
            minimum = ["2Y", "XC"]
            high = ["YC", "2C"]
            minimum_propensity = "Y*(Y-1)+X*C"
            high_propensity = "Y*C+C*(C-1)"

        hard_row = hard_rows[json.dumps(payload, separators=(",", ":"))]
        all_active = tuple(
            descriptor
            for candidate, descriptor in flat.feasible_all_active_incidences()
            if candidate == pair
        )
        descriptor, = all_active
        assert descriptor.weight == (1, 1, 1)
        assert flat._support_rank(top) == 2
        assert hard._resistance_class(hard_row) == 0
        assert sorted(heights.values()) == [2, 2, 3, 4]

        rows.append(
            {
                "pair": payload,
                "top_support": list(support),
                "lower_support": ["0", "C"],
                "dormant_species_X": dormant,
                "other_nonservice_species_Y": transverse,
                "activation_seed_resistance": seed_resistance,
                "relabelled_top_support": sorted(relabelled),
                "weighted_transverse_coordinate": weighted_coordinate,
                "complex_heights": heights,
                "minimum_height_complexes": minimum,
                "strictly_higher_complexes": high,
                "minimum_source_propensity_shape": minimum_propensity,
                "high_source_propensity_shape": high_propensity,
                "comparison_with_total_transverse_mass": "M<=R<=2M",
                "top_preserves_total_population": True,
                "top_rank": 2,
                "all_active_workload": [1, 1, 1],
            }
        )
    assert len(rows) == 4
    return tuple(rows)


def _is_strong(mask: int) -> bool:
    adjacency = [[] for _ in range(4)]
    reverse = [[] for _ in range(4)]
    for bit, (source, target) in enumerate(ARCS):
        if mask & (1 << bit):
            adjacency[source].append(target)
            reverse[target].append(source)
    for graph in (adjacency, reverse):
        seen = {0}
        stack = [0]
        while stack:
            source = stack.pop()
            for target in graph[source]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        if len(seen) != 4:
            return False
    return True


def _minimum_cut_distance(mask: int, start: int) -> int:
    queue = deque(((start, 0),))
    seen = {start}
    while queue:
        source, distance = queue.popleft()
        for bit, (edge_source, target) in enumerate(ARCS):
            if not mask & (1 << bit) or edge_source != source:
                continue
            if target in RESISTANCE_TWO_HIGH:
                return distance + 1
            if target in RESISTANCE_TWO_MINIMUM and target not in seen:
                seen.add(target)
                queue.append((target, distance + 1))
    raise AssertionError("strong digraph has no cut from its minimum class")


def _has_direct_cut(mask: int, start: int) -> bool:
    return any(
        edge_source == start
        and target in RESISTANCE_TWO_HIGH
        and mask & (1 << bit)
        for bit, (edge_source, target) in enumerate(ARCS)
    )


def _has_arc(mask: int, source: int, target: int) -> bool:
    return any(
        edge_source == source
        and edge_target == target
        and mask & (1 << bit)
        for bit, (edge_source, edge_target) in enumerate(ARCS)
    )


@lru_cache(maxsize=1)
def strong_cut_profile() -> tuple[tuple[int, int, int], ...]:
    rows: list[tuple[int, int, int]] = []
    for mask in range(1 << len(ARCS)):
        if not _is_strong(mask):
            continue
        distances = sorted(
            _minimum_cut_distance(mask, start)
            for start in RESISTANCE_TWO_MINIMUM
        )
        rows.append((mask, distances[0], distances[1]))
    result = tuple(rows)
    assert len(result) == 1606
    assert Counter((left, right) for _mask, left, right in result) == {
        (1, 1): 1234,
        (1, 2): 372,
    }
    assert _encoded_sha256(result) == EXPECTED_CUT_PROFILE_SHA256
    return result


def sparse_mass_dip_regression() -> dict[str, object]:
    return {
        "support": ["2Y", "2C", "YC", "XY"],
        "edges": [
            "2Y->2C",
            "2Y->YC",
            "2C->XY",
            "YC->2Y",
            "XY->2Y",
        ],
        "initial_state": "all transverse mass in C",
        "raw_mass_effect": (
            "Theta(M^2/n) pure-to-mixed dips may accumulate before the "
            "carrier rate catches up"
        ),
        "old_one_level_mass_comparison_valid": False,
        "weighted_coordinate": "R=2Y+C",
        "problem_edge": "2C->XY",
        "exact_weighted_increment_on_problem_edge": 0,
        "minimum_cut_word": ["2C->XY", "XY->2Y"],
        "minimum_cut_weighted_reward": 2,
    }


def claim_neutral_arithmetic() -> dict[str, object]:
    positive, signed, _residual = feasibility._residual_failures()
    selected = selected_pairs()
    after = composition.hb_switch_pairs()
    assert (len(selected & positive), len(selected & signed)) == (4, 0)
    assert (len(after & positive), len(after & signed)) == (12, 0)
    return {
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
    rows_hash = _encoded_sha256(rows)
    if EXPECTED_ROWS_SHA256 != "TO_BE_FILLED":
        assert rows_hash == EXPECTED_ROWS_SHA256

    cut_profile = strong_cut_profile()
    cut_hash = _encoded_sha256(cut_profile)
    direct_source_histogram = Counter(
        (
            "both_direct"
            if _has_direct_cut(mask, 1) and _has_direct_cut(mask, 3)
            else "single_direct_A"
            if _has_direct_cut(mask, 1)
            else "single_direct_B"
        )
        for mask, _left, _right in cut_profile
    )
    assert direct_source_histogram == {
        "both_direct": 1234,
        "single_direct_A": 186,
        "single_direct_B": 186,
    }
    direct_zero_histogram = Counter()
    for mask, _left, _right in cut_profile:
        direct_a = _has_direct_cut(mask, 1)
        direct_b = _has_direct_cut(mask, 3)
        zero_a_to_b = _has_arc(mask, 1, 3)
        zero_b_to_a = _has_arc(mask, 3, 1)
        assert direct_a or direct_b
        assert direct_a or zero_a_to_b
        assert direct_b or zero_b_to_a
        direct_zero_histogram[
            (direct_a, direct_b, zero_a_to_b, zero_b_to_a)
        ] += 1
    assert direct_zero_histogram == {
        (False, True, True, False): 84,
        (False, True, True, True): 102,
        (True, False, False, True): 84,
        (True, False, True, True): 102,
        (True, True, False, False): 228,
        (True, True, False, True): 308,
        (True, True, True, False): 308,
        (True, True, True, True): 390,
    }
    resistance_histogram = Counter(
        row["activation_seed_resistance"] for row in rows
    )
    assert resistance_histogram == {1: 2, 2: 2}

    payload: dict[str, object] = {
        "claim_scope": (
            "finite weighted-minimum-cut premises and unaudited dyadic "
            "compound activation target for the exact hard H_w four"
        ),
        "selector": {
            "pairs": 4,
            "positive": 4,
            "signed": 0,
            "pair_sha256": closure.pair_fingerprint(selected_pairs()),
            "activation_resistance_histogram": {
                str(key): value
                for key, value in sorted(resistance_histogram.items())
            },
        },
        "finite_minimum_cut": {
            "status": (
                "exact finite weighted-height equality only; it does not "
                "certify any physical-clock or stochastic contraction claim"
            ),
            "strong_simple_digraphs": 1606,
            "distance_profile": {
                "both_minimum_nodes_cut_directly": 1234,
                "one_minimum_node_needs_one_zero_height_transfer": 372,
            },
            "direct_source_profile": dict(
                sorted(direct_source_histogram.items())
            ),
            "direct_zero_edge_profile": [
                {
                    "direct_A": direct_a,
                    "direct_B": direct_b,
                    "A_to_B_zero": zero_a_to_b,
                    "B_to_A_zero": zero_b_to_a,
                    "count": count,
                }
                for (
                    direct_a,
                    direct_b,
                    zero_a_to_b,
                    zero_b_to_a,
                ), count in sorted(direct_zero_histogram.items())
            ],
            "maximum_minimum_class_cut_length": 2,
            "profile_sha256": cut_hash,
        },
        "mass_dip_regression": sparse_mass_dip_regression(),
        "candidate_compound_quadratic_ascent": {
            "localization": "K<=R<=epsilon*n with epsilon rate-dependent",
            "minimum_propensity_bound": "Lambda_min>=c*R^2",
            "withdrawn_pointwise_cut_claim": (
                "a cut source need not initially have order-R^2 propensity, "
                "and a shortest graph word need not be a bounded physical block"
            ),
            "event_skeleton": (
                "A=2P, B=XU, H={PU,2U}; observe only A-source, "
                "B-source, and exceptional H/lower firings in a dyadic shell"
            ),
            "clock_comparison": (
                "lambda_A+lambda_B>=c*R^2 and "
                "lambda_exception/(lambda_A+lambda_B)"
                "<=C*(epsilon+1/R)"
            ),
            "source_balance": [
                "if B has no direct H edge then b<=U_0+2a+2e",
                "if A has no direct H edge then 2a<=P_0+2b+2e",
                "if both are direct then every minimum firing is a "
                "direct-source opportunity",
            ],
            "adaptive_chernoff": (
                "a direct-source firing has a fixed positive strict-cut "
                "chance; in a deterministic (L+2)*R total-event prefix, "
                "no exit and E<=R leave at least (L+1)*R minimum firings, "
                "while fewer "
                "than 4*R cuts or enough bad jumps for a lower exit has "
                "probability C*exp(-c*R)"
            ),
            "lower_death_bound": "Lambda_death<=C*R",
            "dyadic_block": (
                "from R in [r, r+O(1)], stop at R<=r/2 or R>=2r; "
                "the lower-exit probability is at most C*exp(-c*r)"
            ),
            "block_duration": (
                "E exp(c*r*S_r)<=C and hence all fixed moments at scale O(1/r)"
            ),
            "finite_establishment": (
                "one or two physical C seeds reach fixed K with positive "
                "probability uniformly in n; all high-source slow clocks are "
                "competitors, and the fast XU contraction has no closed "
                "unsuccessful class"
            ),
            "escape_target": (
                "summing dyadic lower-exit tails gives a uniform positive "
                "probability of reaching R>=epsilon*n"
            ),
            "full_attempt_restart": (
                "from each preactivated endpoint use finite establishment "
                "only if R<K, otherwise start at a scale comparable to the "
                "actual R; a lower-block failure restarts at its actual endpoint"
            ),
            "seed_and_time_target": (
                "compound-geometric exponential positive birth tail and "
                "uniform exponential activation-duration moment"
            ),
            "all_reactions_retained": True,
        },
        "candidate_service_and_return": {
            "all_start_partition": (
                "R<epsilon*n implies X>(1-epsilon)*n and uses activation; "
                "R>=epsilon*n skips activation and enters the same service block"
            ),
            "service_zero_invariant_set": (
                "on every positive-population simplex the largest invariant "
                "subset of C=0 is the dormant X vertex"
            ),
            "deterministic_service": (
                "single-linkage weakly-reversible permanence after entry "
                "from the compact R>=epsilon*n activation shell"
            ),
            "full_chain_window": (
                "run every clock for T/n and use density convergence plus "
                "counting-process compensator moments"
            ),
            "negative_increment_mgf": (
                "Z<=B-D_window; B and D_window have uniform two-sided "
                "exponential moments, E(B-D_window)<=-a, and conditional "
                "Taylor gives E exp(lambda Z)<=1-c*lambda"
            ),
            "fractional_stop": "n<=rho*n0 or n>=2*n0",
            "upper_exit": "exp(-c*n0)",
            "duration_and_endpoint_order": "one uniform integer p>8",
            "common_factorial_endpoint": (
                "fixed fractional population contraction gives "
                "Delta W_ell<=-c*(n0*log(n0))^4 for the common shifted "
                "G_ell and W_ell=G_ell^4"
            ),
        },
        "geometry_rows": list(rows),
        "claim_neutral_arithmetic": claim_neutral_arithmetic(),
        "hashes": {
            "rows_sha256": rows_hash,
            "cut_profile_sha256": cut_hash,
        },
        "weighted_minimum_class_contraction_certified": False,
        "event_skeleton_source_balance_certified": False,
        "dyadic_quadratic_ascent_certified": False,
        "deterministic_service_integral_certified": False,
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
