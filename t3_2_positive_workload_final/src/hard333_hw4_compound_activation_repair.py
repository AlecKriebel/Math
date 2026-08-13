"""Claim-neutral compound-activation repair target for the hard H_w four.

The first fractional-return candidate incorrectly applied a linear
Perron--Frobenius/logistic bound at a resistance-two seed state.  This file
freezes the exact counterexample and replaces that step by a finite
pure/mixed-complex contraction.  The top support, after relabeling, always
contains the three pure-transverse complexes ``2Y, YC, 2C`` and exactly one
mixed carrier, ``XY`` in the resistance-two rows or ``XC`` in the
resistance-one rows; ``2X`` is absent.

The graph enumeration below covers every simple strongly connected
reaction digraph on the four labeled complexes.  It is a topological
premise only.  The rate-uniform trace comparison, deterministic service
lemma, stopped endpoint theorem, and recurrence statement remain false
pending independent analytic replay.
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
State = tuple[int, int, int]

EXPECTED_PAIR_SHA256 = composition.EXPECTED_HW_4_SHA256
EXPECTED_ROWS_SHA256 = (
    "47b6fae4896567c500f52bf82adc0fbce9923e91cb4c4fae2a22733928d275ed"
)
EXPECTED_DIGRAPH_PROFILE_SHA256 = (
    "2a136e64a12be64577c5852ed30e027d057b529ffefa5dc82abd67a8a39f1230"
)
EXPECTED_PAYLOAD_SHA256 = (
    "d62253d0663d7df818feebf9e2afa2e287c22490b1d1bda700ddf80352b30064"
)

RELABELLED_NODES = ("2Y", "2C", "YC", "XY")
NODE_VECTORS: tuple[State, ...] = (
    (0, 2, 0),
    (0, 0, 2),
    (0, 1, 1),
    (1, 1, 0),
)
ARCS = tuple((source, target) for source in range(4) for target in range(4)
             if source != target)


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
        dormant_vertices = [
            species for species in ("A", "B") if f"2{species}" not in support
        ]
        dormant, = dormant_vertices
        transverse = "B" if dormant == "A" else "A"
        resistance_two_carrier = "".join(sorted((dormant, transverse)))
        resistance_one_carrier = f"{dormant}C"
        seed_resistance = 2 if resistance_two_carrier in support else 1
        carrier = (
            resistance_two_carrier
            if seed_resistance == 2
            else resistance_one_carrier
        )
        relabelled_support = {"2Y", "YC", "2C"}
        relabelled_support.add("XY" if seed_resistance == 2 else "XC")
        hard_row = hard_rows[json.dumps(payload, separators=(",", ":"))]

        all_active = tuple(
            descriptor
            for candidate, descriptor in flat.feasible_all_active_incidences()
            if candidate == pair
        )
        descriptor, = all_active
        assert descriptor.weight == (1, 1, 1)
        assert flat._support_rank(top) == 2
        assert seed_resistance in (1, 2)
        assert hard._resistance_class(hard_row) == 0
        assert relabelled_support in (
            {"2Y", "YC", "2C", "XY"},
            {"2Y", "YC", "2C", "XC"},
        )

        rows.append(
            {
                "pair": payload,
                "top_support": list(support),
                "lower_support": ["0", "C"],
                "dormant_species_X": dormant,
                "other_nonservice_species_Y": transverse,
                "transverse_mass": "M=Y+C",
                "relabelled_top_support": sorted(relabelled_support),
                "pure_transverse_complexes": ["2Y", "YC", "2C"],
                "unique_mixed_carrier": (
                    "XY" if seed_resistance == 2 else "XC"
                ),
                "physical_carrier": carrier,
                "activation_seed_resistance": seed_resistance,
                "top_preserves_total_population": True,
                "top_rank": 2,
                "all_active_workload": [1, 1, 1],
                "hard_dormant_resistance": hard._resistance_class(hard_row),
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


def _enabled(state: State, source: State) -> bool:
    return all(value >= needed for value, needed in zip(state, source))


def _move(state: State, source: State, target: State) -> State:
    return tuple(
        value - consumed + produced
        for value, consumed, produced in zip(state, source, target)
    )


def _shortest_ignition(mask: int, allowed_loss: int) -> int | None:
    """Shortest top word from two C seeds to transverse mass three."""

    start: State = (4, 0, 2)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, distance = queue.popleft()
        if state[1] + state[2] >= 3:
            return distance
        for bit, (source_index, target_index) in enumerate(ARCS):
            if not mask & (1 << bit):
                continue
            source = NODE_VECTORS[source_index]
            target = NODE_VECTORS[target_index]
            if not _enabled(state, source):
                continue
            endpoint = _move(state, source, target)
            if endpoint[1] + endpoint[2] < 2 - allowed_loss:
                continue
            if endpoint not in seen:
                seen.add(endpoint)
                queue.append((endpoint, distance + 1))
    return None


@lru_cache(maxsize=1)
def strong_digraph_profile() -> tuple[tuple[int, int, int], ...]:
    """Return ``(mask, minimum loss, shortest word length)`` for all graphs."""

    rows: list[tuple[int, int, int]] = []
    for mask in range(1 << len(ARCS)):
        if not _is_strong(mask):
            continue
        no_loss = _shortest_ignition(mask, allowed_loss=0)
        if no_loss is not None:
            rows.append((mask, 0, no_loss))
            continue
        one_loss = _shortest_ignition(mask, allowed_loss=1)
        assert one_loss is not None
        rows.append((mask, 1, one_loss))
    result = tuple(rows)
    assert len(result) == 1606
    assert Counter((loss, length) for _mask, loss, length in result) == {
        (0, 2): 1420,
        (1, 3): 186,
    }
    return result


def sparse_dip_witness() -> dict[str, object]:
    mask = 611
    edges = [
        [RELABELLED_NODES[source], RELABELLED_NODES[target]]
        for bit, (source, target) in enumerate(ARCS)
        if mask & (1 << bit)
    ]
    assert edges == [
        ["2Y", "2C"],
        ["2Y", "YC"],
        ["2C", "XY"],
        ["YC", "2Y"],
        ["XY", "2Y"],
    ]
    return {
        "mask": mask,
        "edges": edges,
        "seed_state": "(X,Y,C)=(n-2,0,2)",
        "ignition_word": ["2C->XY", "XY->2Y", "XY->2Y"],
        "transverse_mass_path": [2, 1, 2, 3],
        "one_unit_dip_is_necessary": True,
    }


def false_linear_pf_regression() -> dict[str, object]:
    return {
        "support": ["2Y", "2C", "YC", "XY"],
        "strong_cycle": "2C->YC->2Y->XY->2C",
        "rates": "all one",
        "state": "(X,Y,C)=(n-2,0,2)",
        "only_enabled_top_source": "2C",
        "linear_form": "R=v_Y*Y+v_C*C, v_Y,v_C>0",
        "exact_top_drift": "L_T R=2*(v_Y-v_C)=O(1)",
        "claimed_logistic_rhs": "c*X*R-K*R^2=Theta(n)",
        "old_pointwise_pf_bound_valid": False,
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

    digraph_profile = strong_digraph_profile()
    digraph_hash = _encoded_sha256(digraph_profile)
    if EXPECTED_DIGRAPH_PROFILE_SHA256 != "TO_BE_FILLED":
        assert digraph_hash == EXPECTED_DIGRAPH_PROFILE_SHA256

    resistance_histogram = Counter(
        row["activation_seed_resistance"] for row in rows
    )
    assert resistance_histogram == {1: 2, 2: 2}
    path_histogram = Counter(
        (loss, length) for _mask, loss, length in digraph_profile
    )

    payload: dict[str, object] = {
        "claim_scope": (
            "finite compound-activation premises and unaudited repaired "
            "fractional-return target for the exact hard H_w four"
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
        "linear_pf_regression": false_linear_pf_regression(),
        "finite_cut_contraction": {
            "labeled_nodes": list(RELABELLED_NODES),
            "strong_simple_digraphs": len(digraph_profile),
            "ignition_profile": {
                "no_mass_loss_length_2": path_histogram[(0, 2)],
                "one_mass_loss_length_3": path_histogram[(1, 3)],
            },
            "profile_sha256": digraph_hash,
            "sparse_dip_witness": sparse_dip_witness(),
        },
        "candidate_compound_activation": {
            "transverse_mass": "M=Y+C",
            "resistance_one": (
                "one C seed enables XC; its mixed-to-pure exit raises M"
            ),
            "resistance_two": (
                "two C seeds enter a length-at-most-three ignition word, "
                "with at most one temporary unit of M loss"
            ),
            "contracted_trace_target": (
                "for K<=M<=epsilon*n, p_up is at least "
                "1-C/M-C*M/n after pure/mixed finite-state contraction"
            ),
            "escape_target": (
                "choose K large and epsilon small for a uniformly biased "
                "embedded walk from K to epsilon*n"
            ),
            "seed_and_time_target": (
                "geometric localized trials, an exponential positive birth "
                "tail, and all fixed activation-duration moments"
            ),
            "all_reactions_retained": True,
        },
        "candidate_service_and_return": {
            "deterministic_service": (
                "use the one-linkage strongly-endotactic rank-two top "
                "permanence lemma, or prove its finite-cut analogue, to "
                "obtain divergent integrated C from the activation shell"
            ),
            "full_chain_window": (
                "run every clock for T/n and use density convergence plus "
                "counting-process compensator moments"
            ),
            "fractional_stop": "n<=rho*n0 or n>=2*n0",
            "upper_exit": "exp(-c*n0)",
            "duration_and_endpoint_order": "one uniform integer p>8",
            "common_factorial_endpoint": (
                "fixed fractional population contraction gives "
                "Delta W_ell<=-c*(n0*log(n0))^4"
            ),
        },
        "geometry_rows": list(rows),
        "claim_neutral_arithmetic": claim_neutral_arithmetic(),
        "hashes": {
            "rows_sha256": rows_hash,
            "digraph_profile_sha256": digraph_hash,
        },
        "compound_trace_comparison_certified": False,
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
