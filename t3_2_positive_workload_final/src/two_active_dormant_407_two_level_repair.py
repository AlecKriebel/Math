"""Claim-neutral finite certificate for the hard-333 two-level repair.

The frozen candidate in :mod:`two_active_dormant_407_certificate` attached a
global paid counter to successive no-fast base returns.  The exact witness in
:mod:`two_active_dormant_407_asymmetric_return_audit` shows that this cannot
work.  This module records the finite support facts used by the replacement:

* local opened-excursion marks are discarded at every physical ``I=0``
  return;
* exact physical self returns disappear from the outer trace generator;
* the unique degree-two/degree-zero exception has only an exact-self
  ``U**4/n`` term, while every nonself term is ``O(U**3/n)``;
* all other base-open templates have a fixed cut or a safer degree ledger.
* interrupted exact returns are a genuinely small second renewal after the
  pure nested diagonal class is summed; and
* the local theorem is needed only on historically reachable positive-debt
  bases, not on the frozen/no-history faces in the finite atlas.

The analytic statements are proved in
``research_notes/two_active_dormant_407_two_level_repair.md``.  This executable
does not certify that proof, any support pair, or T3-2.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import two_active_dormant_407_certificate as dormant
import two_active_dormant_407_asymmetric_return_audit as failed_audit


ROOT = Path(__file__).resolve().parents[1]

U_DEGREE = {
    "0": 0,
    "U": 1,
    "2U": 2,
    "I": 0,
    "2I": 0,
    "UI": 1,
    "VI": 0,
}
I_DEGREE = {
    "0": 0,
    "U": 0,
    "2U": 0,
    "I": 1,
    "2I": 2,
    "UI": 1,
    "VI": 1,
}
PHYSICAL_COMPLEX_VECTOR = {
    "0": (0, 0, 0),
    "U": (1, 0, 0),
    "2U": (2, 0, 0),
    "I": (0, 1, 0),
    "2I": (0, 2, 0),
    "UI": (1, 1, 0),
    "VI": (0, 1, 1),
}

FROZEN_FAILED_HASHES = dict(failed_audit.FROZEN_HASHES)


def _encoded_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _max_ifree_degree(support: list[str]) -> int:
    return max(
        U_DEGREE[name] for name in support if I_DEGREE[name] == 0
    )


def base_open_exact_templates() -> tuple[dict[str, object], ...]:
    """The exact proper pairs with an enabled ``I=0`` proper source."""

    rows = []
    for row in dormant.generalized_support_templates():
        proper = set(row["proper"])
        if len(proper) != 2 or "VI" not in proper:
            continue
        ifree = [name for name in proper if I_DEGREE[name] == 0]
        if len(ifree) != 1:
            continue
        source = ifree[0]
        rows.append(
            {
                "proper": list(row["proper"]),
                "lower": list(row["lower"]),
                "base_source": source,
                "base_source_degree": U_DEGREE[source],
                "lower_ifree_cut_degree": _max_ifree_degree(row["lower"]),
            }
        )
    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return tuple(rows)


def exact_menu_partition() -> dict[str, object]:
    templates = dormant.generalized_support_templates()
    base_open = base_open_exact_templates()
    all_exact = tuple(row for row in templates if len(row["proper"]) == 2)
    no_base_open = tuple(
        row
        for row in all_exact
        if not any(I_DEGREE[name] == 0 for name in row["proper"])
    )
    larger = tuple(row for row in templates if len(row["proper"]) > 2)

    source_histogram = Counter(row["base_source"] for row in base_open)
    cut_histogram = {
        source: Counter(
            row["lower_ifree_cut_degree"]
            for row in base_open
            if row["base_source"] == source
        )
        for source in ("0", "U", "2U")
    }
    assert source_histogram == {"0": 6, "U": 5, "2U": 6}
    assert cut_histogram == {
        "0": Counter({2: 5, 1: 1}),
        "U": Counter({2: 5}),
        "2U": Counter({1: 5, 0: 1}),
    }
    assert len(all_exact) == 37
    assert len(no_base_open) == 20
    assert len(larger) == 109
    assert len(base_open) + len(no_base_open) + len(larger) == 146

    return {
        "support_templates": len(templates),
        "base_open_exact": len(base_open),
        "base_open_source_histogram": dict(sorted(source_histogram.items())),
        "base_open_cut_histogram": {
            source: {
                str(degree): count
                for degree, count in sorted(histogram.items())
            }
            for source, histogram in cut_histogram.items()
        },
        "exact_without_ifree_proper_source": len(no_base_open),
        "larger_proper_support": len(larger),
        "base_open_rows_sha256": _encoded_sha256(base_open),
    }


def _complete_template_edges(
    row: dict[str, object],
) -> tuple[tuple[str, str, str], ...]:
    """All potential directed edges on a support template.

    Every strongly connected orientation is a subgraph of this complete
    directed menu, so a path property checked here is orientation-uniform.
    """

    return tuple(
        (linkage, source, target)
        for linkage in ("proper", "lower")
        for source in row[linkage]
        for target in row[linkage]
        if source != target
    )


def _fire_relative(
    state: tuple[int, int, int],
    edge: tuple[str, str, str],
) -> tuple[int, int, int] | None:
    """Fire an edge in coordinates ``(U,I,R=V-n)`` when enabled."""

    _linkage, source, target = edge
    source_vector = PHYSICAL_COMPLEX_VECTOR[source]
    target_vector = PHYSICAL_COMPLEX_VECTOR[target]
    if state[0] < source_vector[0] or state[1] < source_vector[1]:
        return None
    return tuple(
        state[index] - source_vector[index] + target_vector[index]
        for index in range(3)
    )


def _outer_base_degree(template: dict[str, object]) -> int:
    """Maximal cut/service degree after exact base diagonals are erased."""

    proper = set(template["proper"])
    proper_ifree = {
        name for name in proper if I_DEGREE[name] == 0
    }
    if len(proper) == 2 and "VI" in proper and len(proper_ifree) == 1:
        # The only proper macro is a physical diagonal.  Its source clock is
        # not an outer denominator; the strongly connected lower linkage
        # supplies the first genuine cut/service clock.
        candidates = {
            name for name in template["lower"] if I_DEGREE[name] == 0
        }
    else:
        candidates = {
            name
            for name in proper | set(template["lower"])
            if I_DEGREE[name] == 0
        }
    assert candidates
    return max(U_DEGREE[name] for name in candidates)


def positive_continuing_primitive_ledger() -> dict[str, object]:
    """Exhaust the one-defect positive continuing architectures.

    An opening is a slow edge from the ``I=0`` face to an ``I``-bearing
    target.  After it, the path contains exactly one further slow edge and
    otherwise only fast ``VI``-source edges.  The path stops at the first
    physical ``I=0`` endpoint or strict service.  Exact physical loops are
    erased before this ledger analytically; enumerating the complete path
    menu here is an overcount and therefore only strengthens the check.
    """

    start = (20, 0, 0)
    rows: list[dict[str, object]] = []
    for template_index, template in enumerate(
        dormant.generalized_support_templates()
    ):
        edges = _complete_template_edges(template)
        fast_edges = tuple(edge for edge in edges if edge[1] == "VI")
        slow_edges = tuple(edge for edge in edges if edge[1] != "VI")
        openings = tuple(
            edge
            for edge in slow_edges
            if I_DEGREE[edge[1]] == 0 and I_DEGREE[edge[2]] > 0
        )
        base_degree = _outer_base_degree(template)

        for opening in openings:
            opened_state = _fire_relative(start, opening)
            assert opened_state is not None and opened_state[1] > 0

            def visit(
                state: tuple[int, int, int],
                defect: tuple[str, str, str] | None,
                steps: tuple[tuple[str, tuple[str, str, str]], ...],
            ) -> None:
                if state[2] < 0:
                    return  # strict service
                if state[1] == 0:
                    if defect is None or state[2] != 0 or state[0] <= start[0]:
                        return
                    opening_degree = U_DEGREE[opening[1]]
                    defect_degree = U_DEGREE[defect[1]]
                    jump = state[0] - start[0]
                    relative_power = (
                        opening_degree + defect_degree - base_degree
                    )
                    rows.append(
                        {
                            "template_index": template_index,
                            "proper": list(template["proper"]),
                            "lower": list(template["lower"]),
                            "opening": list(opening),
                            "defect": list(defect),
                            "steps": [
                                [kind, list(edge)] for kind, edge in steps
                            ],
                            "opening_source_degree": opening_degree,
                            "defect_source_degree": defect_degree,
                            "base_degree": base_degree,
                            "relative_power": relative_power,
                            "positive_jump": jump,
                        }
                    )
                    return
                if len(steps) > 4:
                    raise AssertionError("primitive path failed to terminate")

                if defect is None:
                    for edge in slow_edges:
                        next_state = _fire_relative(state, edge)
                        if next_state is not None:
                            visit(
                                next_state,
                                edge,
                                steps + (("slow", edge),),
                            )
                for edge in fast_edges:
                    next_state = _fire_relative(state, edge)
                    if next_state is not None:
                        visit(
                            next_state,
                            defect,
                            steps + (("fast", edge),),
                        )

            visit(opened_state, None, ())

    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    relative_jump_histogram = Counter(
        (row["relative_power"], row["positive_jump"]) for row in rows
    )
    expected_histogram = Counter(
        {
            (-2, 1): 158,
            (-2, 2): 170,
            (-2, 3): 58,
            (-2, 4): 36,
            (-1, 1): 316,
            (-1, 2): 140,
            (-1, 3): 20,
            (0, 1): 238,
            (0, 2): 98,
            (1, 1): 73,
            (2, 1): 1,
        }
    )
    exact_pair_degree_histogram = Counter(
        ("|".join(template["proper"]), _outer_base_degree(template))
        for template in dormant.generalized_support_templates()
        if len(template["proper"]) == 2
    )
    expected_exact_pair_degree_histogram = Counter(
        {
            ("0|VI", 1): 1,
            ("0|VI", 2): 5,
            ("U|VI", 2): 5,
            ("2U|VI", 0): 1,
            ("2U|VI", 1): 5,
            ("I|VI", 1): 1,
            ("I|VI", 2): 6,
            ("2I|VI", 1): 1,
            ("2I|VI", 2): 5,
            ("UI|VI", 1): 1,
            ("UI|VI", 2): 6,
        }
    )
    assert len(rows) == 1308
    assert relative_jump_histogram == expected_histogram
    assert exact_pair_degree_histogram == expected_exact_pair_degree_histogram
    assert max(
        row["opening_source_degree"] + row["defect_source_degree"]
        for row in rows
    ) == 3
    assert all(
        not (
            row["opening_source_degree"] == 2
            and row["defect_source_degree"] == 2
        )
        for row in rows
    )
    assert max(row["positive_jump"] for row in rows) == 4
    # For 0 < theta < 1/2, the exact histogram gives
    # max(relative_power + theta*positive_jump) = 2 + theta < 5/2.
    assert max(2 * power + jump for power, jump in relative_jump_histogram) == 5

    return {
        "templates": len(dormant.generalized_support_templates()),
        "orientation_menu": "complete directed support supergraph",
        "actual_strong_orientation_relation": "subgraph",
        "outer_denominator": "post-diagonal cut/service degree",
        "primitive_positive_continuing_paths": len(rows),
        "relative_power_jump_histogram": {
            f"{power},{jump}": count
            for (power, jump), count in sorted(relative_jump_histogram.items())
        },
        "exact_pair_outer_degree_histogram": {
            f"{proper},{degree}": count
            for (proper, degree), count in sorted(
                exact_pair_degree_histogram.items()
            )
        },
        "maximum_opening_plus_defect_source_degree": 3,
        "degree_two_plus_degree_two_positive_path": False,
        "maximum_positive_jump": 4,
        "critical_twice_weighted_power": 5,
        "theta_bound": (
            "max(relative_power+theta*jump)=2+theta<5/2 for theta<1/2"
        ),
        "path_ledger_sha256": _encoded_sha256(rows),
    }


def interrupted_exact_return_ledger() -> dict[str, object]:
    """Exhaust one-defect exact returns after pure nested loops are removed.

    The whole pure class consists of repeated copies of one ``aU -> VI``
    opening and its matching ``VI -> aU`` cleanup.  Such histories are
    summed first.  This ledger retains exact physical returns containing a
    genuinely different post-opening slow edge.  It is the finite base case
    for the analytic all-order diagonal-renewal estimate.
    """

    start = (20, 0, 0)
    rows: list[dict[str, object]] = []
    for template_index, template in enumerate(
        dormant.generalized_support_templates()
    ):
        edges = _complete_template_edges(template)
        fast_edges = tuple(edge for edge in edges if edge[1] == "VI")
        slow_edges = tuple(edge for edge in edges if edge[1] != "VI")
        openings = tuple(
            edge
            for edge in slow_edges
            if I_DEGREE[edge[1]] == 0 and I_DEGREE[edge[2]] > 0
        )
        base_degree = _outer_base_degree(template)

        for opening in openings:
            opened_state = _fire_relative(start, opening)
            assert opened_state is not None and opened_state[1] > 0

            def visit(
                state: tuple[int, int, int],
                defect: tuple[str, str, str] | None,
                steps: tuple[tuple[str, tuple[str, str, str]], ...],
            ) -> None:
                if state[2] < 0:
                    return
                if state[1] == 0:
                    if defect is None or state != start:
                        return
                    pure_nested = (
                        opening[2] == "VI"
                        and defect == opening
                        and all(
                            edge[1] == "VI" and edge[2] == opening[1]
                            for kind, edge in steps
                            if kind == "fast"
                        )
                    )
                    if pure_nested:
                        return
                    opening_degree = U_DEGREE[opening[1]]
                    defect_degree = U_DEGREE[defect[1]]
                    rows.append(
                        {
                            "template_index": template_index,
                            "proper": list(template["proper"]),
                            "lower": list(template["lower"]),
                            "opening": list(opening),
                            "defect": list(defect),
                            "steps": [
                                [kind, list(edge)] for kind, edge in steps
                            ],
                            "opening_source_degree": opening_degree,
                            "defect_source_degree": defect_degree,
                            "base_degree": base_degree,
                            "relative_power": (
                                opening_degree
                                + defect_degree
                                - base_degree
                            ),
                        }
                    )
                    return
                if len(steps) > 4:
                    raise AssertionError("exact-return path failed to terminate")

                if defect is None:
                    for edge in slow_edges:
                        next_state = _fire_relative(state, edge)
                        if next_state is not None:
                            visit(
                                next_state,
                                edge,
                                steps + (("slow", edge),),
                            )
                for edge in fast_edges:
                    next_state = _fire_relative(state, edge)
                    if next_state is not None:
                        visit(
                            next_state,
                            defect,
                            steps + (("fast", edge),),
                        )

            visit(opened_state, None, ())

    rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    power_histogram = Counter(row["relative_power"] for row in rows)
    assert len(rows) == 1560
    assert power_histogram == Counter(
        {-2: 164, -1: 482, 0: 636, 1: 278}
    )
    assert max(power_histogram) == 1
    return {
        "templates": len(dormant.generalized_support_templates()),
        "pure_nested_class_removed_first": True,
        "one_defect_interrupted_exact_returns": len(rows),
        "relative_power_histogram": {
            str(power): count
            for power, count in sorted(power_histogram.items())
        },
        "maximum_relative_power": max(power_histogram),
        "rows_sha256": _encoded_sha256(rows),
    }


def historical_scope_certificate() -> dict[str, object]:
    """Freeze the no-history faces excluded by positive reflected debt."""

    no_history_templates = tuple(
        template
        for template in dormant.generalized_support_templates()
        if all(I_DEGREE[name] > 0 for name in template["proper"])
        and all(I_DEGREE[name] == 0 for name in template["lower"])
    )
    keys = {
        (tuple(template["proper"]), tuple(template["lower"]))
        for template in no_history_templates
    }
    rows = tuple(
        row
        for row in dormant.generalized_normalized_rows()
        if (tuple(row["proper"]), tuple(row["lower"])) in keys
    )
    pair_payloads = sorted(
        {
            json.dumps(
                row["pair"], sort_keys=True, separators=(",", ":")
            )
            for row in rows
        }
    )
    witness = {
        "proper": ["I", "VI"],
        "lower": ["0", "U", "2U"],
        "no_fast_face": "I=0",
        "face_invariant": True,
        "V_changes_on_face": False,
        "strict_service_possible_on_face": False,
    }
    assert witness["proper"] in [
        template["proper"] for template in no_history_templates
    ]
    assert len(no_history_templates) == 12
    assert len(rows) == 84
    assert len(pair_payloads) == 28
    return {
        "normalized_no_history_supports": len(no_history_templates),
        "physical_incidences": len(rows),
        "pairs": len(pair_payloads),
        "required_local_start": (
            "reachable marked no-fast base with selected reflected D_V>0"
        ),
        "D_V_zero_alternative": (
            "V=H_V<=x_V_reference, hence finite in a one-active tube"
        ),
        "witness": witness,
        "rows_sha256": _encoded_sha256(rows),
        "pair_payloads_sha256": _encoded_sha256(pair_payloads),
    }


def exceptional_template() -> dict[str, object]:
    matches = tuple(
        row
        for row in base_open_exact_templates()
        if row["base_source"] == "2U"
        and row["lower_ifree_cut_degree"] == 0
    )
    assert len(matches) == 1
    row = matches[0]
    assert set(row["proper"]) == {"2U", "VI"}
    assert set(row["lower"]) == {"0", "I", "2I", "UI"}

    lower_edges = tuple(
        (source, target)
        for source in row["lower"]
        for target in row["lower"]
        if source != target
    )
    degree_one = tuple(
        edge for edge in lower_edges if U_DEGREE[edge[0]] == 1
    )
    positive = tuple(
        edge
        for edge in lower_edges
        if U_DEGREE[edge[1]] > U_DEGREE[edge[0]]
    )
    assert degree_one
    assert all(
        U_DEGREE[target] <= U_DEGREE[source]
        for source, target in degree_one
    )
    assert all(U_DEGREE[source] == 0 for source, _target in positive)

    return {
        "proper": row["proper"],
        "lower": row["lower"],
        "base_source_degree": 2,
        "lower_cut_degree": 0,
        "dangerous_nested_edge": "2U->VI",
        "dangerous_nested_then_fast": "exact physical self return",
        "apparent_nested_effective_rate": "O(U^4/n)",
        "largest_nonself_defect_source_degree": 1,
        "nonself_effective_rate": "O(U^3/n)",
        "degree_one_first_defect_edges_are_U_nonincreasing": True,
        "positive_U_first_defect_edge_source_degree": 0,
        "positive_U_continuing_base_rate": "O(U^2/n)",
        "positive_U_terminal_service_rate_can_be": "O(U^3/n)",
        "degree_one_positive_terminal_service_states": (
            degree_one_positive_service_states()
        ),
        "terminal_factorial_method": "theta_minus<theta_zero<theta_plus gap",
        "degree_one_edges": [list(edge) for edge in degree_one],
        "positive_U_edges": [list(edge) for edge in positive],
    }


def exact_self_word_states(
    n: int = 10**6, u: int = 20, duplicates: int = 3
) -> tuple[list[int], ...]:
    """Open, nest ``duplicates`` times, and fast-clean to the exact base."""

    if duplicates < 0:
        raise ValueError("duplicates must be nonnegative")
    vectors = failed_audit.VECTORS
    state = (u, n, 0)
    states = [[u, 0, 0]]

    def fire(source: str, target: str) -> None:
        nonlocal state
        source_vector = vectors[source]
        target_vector = vectors[target]
        if any(state[index] < source_vector[index] for index in range(3)):
            raise AssertionError(f"disabled source {source} at {state}")
        state = tuple(
            state[index] + target_vector[index] - source_vector[index]
            for index in range(3)
        )
        states.append([state[0], state[2], state[1] - n])

    for _ in range(duplicates + 1):
        fire("2U", "VI")
    for _ in range(duplicates + 1):
        fire("VI", "2U")
    assert state == (u, n, 0)
    return tuple(states)


def degree_one_positive_service_states(
    n: int = 10**6, u: int = 20
) -> tuple[list[int], ...]:
    """A leading degree-one defect raises ``U`` only at strict service."""

    vectors = failed_audit.VECTORS
    state = (u, n, 0)
    states = [[u, 0, 0]]
    word = (
        ("2U", "VI"),
        ("UI", "2I"),
        ("VI", "2U"),
        ("VI", "2U"),
    )
    for source, target in word:
        source_vector = vectors[source]
        target_vector = vectors[target]
        if any(state[index] < source_vector[index] for index in range(3)):
            raise AssertionError(f"disabled source {source} at {state}")
        state = tuple(
            state[index] + target_vector[index] - source_vector[index]
            for index in range(3)
        )
        states.append([state[0], state[2], state[1] - n])
    assert states == [
        [u, 0, 0],
        [u - 2, 1, 1],
        [u - 3, 2, 1],
        [u - 1, 1, 0],
        [u + 1, 0, -1],
    ]
    return tuple(states)


def degree_ledger() -> dict[str, object]:
    """Record the powers used in the two outer insertion estimates."""

    # L_n = n^(1/3)/log(n+e).  Thus L_n^3/n = O(log(n)^-3).
    # The exceptional continuing primitive has post-diagonal relative power
    # two and jump one.  Further slow firings have the geometric factor
    # L_n^(2+2 theta)/n, which is negligible for theta < 1/2.
    return {
        "cutoff": "floor(n^(1/3)/log(n+e))",
        "cutoff_weight": "n^(1/3+o(1))",
        "generic_relative_insertion": "O((1+U)^2/n)",
        "generic_green_accumulation": "O((1+U)^3/n)",
        "exceptional_nonself_insertion": "O((1+U)^3/n)",
        "uniform_outer_neumann_norm": "O(log(n)^(-3))",
        "positive_U_continuing_rate_exceptional": "O((1+U)^2/n)",
        "positive_U_terminal_service_rate_exceptional": "O((1+U)^3/n)",
        "factorial_positive_power": "(1+U)^(2*k+theta)/n^k",
        "factorial_exponent_condition": "theta<1/2",
        "factorial_positive_bound_at_cutoff": (
            "n^(-(1-theta)/3+o(1))"
        ),
        "same_weight_continuation_green": True,
        "terminal_weight_gap_only": True,
        "multi_slow_prefix_bound": "subsumed by the all-k invariant",
        "extra_slow_geometric_ratio": (
            "O((1+U)^3/n)=o(1) after I occupation"
        ),
        "reserve_fast_count_for_k_slow": (
            "each VI-target slow firing pairs with one reserve-consuming fast firing"
        ),
        "factorial_terminal_method": (
            "theta_minus<theta_zero<theta_plus two-weight gap"
        ),
        "primitive_positive_weighted_power": "2+theta<5/2",
        "primitive_positive_bound_at_cutoff": (
            "n^(-(1-theta)/3+o(1)) <= n^(-1/6+o(1))"
        ),
        "all_k_coupled_invariant": (
            "r+j<=2*k+1 and r+theta*j<=2*k+theta"
        ),
        "r_le_2k_scope": "positive continuing or interrupted exact returns only",
        "negative_return_r_le_2k_claimed": False,
        "all_k_proof_method": (
            "pair each VI cleanup with its reserve-creating slow edge; "
            "the d=0 nonpure path has one strict lower-target saving"
        ),
        "all_orders_open_race": (
            "P(N>=m|opened)<=C*(C*L^2/n)^m/(1-C*L^2/n)"
        ),
        "all_orders_I_occupation_cost": "C^k*k^k",
        "factorial_continuation_geometric_ratio": "C*L^3/n=o(1)",
        "pure_renewal_amplification": {
            "proper_subset": "O(1)",
            "exact_pair_d_ge_1": "O(L)",
            "unique_exact_pair_d_0": "O(L^2) with N>=2",
        },
        "compact_nontrapping_basis": (
            "historical positive-debt killed transience; no closed pure-only class"
        ),
        "interrupted_diagonal_renewal": (
            "sum Z_pure first, then ||(I-Z_pure)^-1 Z_int||=o(1)"
        ),
        "interrupted_diagonal_norm": (
            "O((L^2/n)/(1-C*L^3/n)+L^2*(C*L^2/n)^L)=o(1)"
        ),
        "first_nonself_insertion_from_subpower_start": "n^(-1+o(1))",
    }


def repair_certificate() -> dict[str, object]:
    observed_frozen_hashes = {
        name: _file_sha256(path)
        for name, path in failed_audit.FROZEN_PATHS.items()
    }
    assert observed_frozen_hashes == FROZEN_FAILED_HASHES

    failed = failed_audit.audit()
    assert failed["verdict"] == "FAIL-as-written"
    dormant_certificate = dormant.certificate()
    flags = {
        name: dormant_certificate[name]
        for name in (
            "analytic_theorem_independently_audited",
            "pair_level_recurrence_certified",
            "global_t3_2_certified",
        )
    }
    assert not any(flags.values())

    menu = exact_menu_partition()
    exceptional = exceptional_template()
    primitive_ledger = positive_continuing_primitive_ledger()
    exact_return_ledger = interrupted_exact_return_ledger()
    historical_scope = historical_scope_certificate()
    ledger = degree_ledger()
    payload = {
        "frozen_failed_snapshot_sha256": observed_frozen_hashes,
        "frozen_failure_verdict": failed["verdict"],
        "frozen_failure_scope": failed["scope"],
        "two_level_state": {
            "inner": "physical (U,I,R) plus a local interruption mark",
            "inner_reserve": "R=V-n",
            "reset": "only at an included physical I=R=0 base return",
            "outer": "physical one-species base (U,n,0)",
            "upward_terminal": "an I=0 return with V>n",
            "outer_outcome_partition": [
                "exact physical self return",
                "nonexact continuing I=R=0 return",
                "strict service",
                "upward I=0,R>0 return",
                "physical boundary",
            ],
            "perturbed_terminal_kernel": "strict service plus upward return",
            "physical_reserve": "R=V-n before the first service",
            "terminal_and_boundary_marks": ["U", "I", "R"],
            "global_paid_counter_used": False,
            "finite_paid_cap_used": False,
        },
        "self_loop_erasure": {
            "criterion": "exact equality of the complete physical state",
            "trace_generator_identity": "q(x,x)*(f(x)-f(x))=0",
            "raw_diagonal_includes_opening_selection_probability": True,
            "raw_renewal_includes_no_interruption_base_exit": True,
            "boundary_hits_inside_a_loop_retained": True,
            "physical_loop_duration_retained": True,
            "performed_before_weighted_and_duration_norms": True,
            "projection_scope": "descriptor-local physical kernel only",
            "global_reflected_debt_mark_equality_asserted": False,
            "common_W_depends_only_on_physical_population": True,
            "fixed_population_global_mark_fiber": "finite",
            "mark_corrector_inserted": False,
            "fiber_finiteness_use": "properness only",
            "physical_law_incoming_mark_independent": True,
            "sample_nested_word": exact_self_word_states(),
        },
        "exact_menu_partition": menu,
        "exceptional_template": exceptional,
        "positive_continuing_primitive_ledger": primitive_ledger,
        "interrupted_exact_return_ledger": exact_return_ledger,
        "historical_scope": historical_scope,
        "outer_degree_ledger": ledger,
        "inner_open_excursion": {
            "state": ["U", "I", "R", "local_N"],
            "admissible_initial_data": (
                "base opening N=0,I+R<=2 or post-first-slow N=1,I+R<=5"
            ),
            "arbitrary_initial_I_R_polynomial_bound_claimed": False,
            "mark_order": "1<a_I<a_R",
            "terminal_reward": "(1+U+I+R)^q",
            "terminal_contains_local_N": False,
            "polynomial_endpoint_order": "q -> q",
            "all_local_interruption_orders_summed": True,
        },
        "boundary_and_duration": {
            "boundary": ["U", "I", "R"],
            "exact_handoff_boundary": "I=R=0 outer-base U boundary only",
            "open_phase_U_boundary": "auxiliary charged boundary",
            "unperturbed_terminal_partition": [
                "strict service",
                "outer-base promotion",
                "physical boundary",
            ],
            "no_interruption_upward_return": False,
            "paid_counter_boundary": False,
            "every_fixed_endpoint_order": True,
            "every_fixed_physical_duration_order": True,
            "rare_event_endpoint_weighted_entropy": True,
            "rare_event_includes_interrupted_terminals": True,
            "zero_slow_service_I_R_uniformly_bounded": True,
            "full_physical_G_entropy_split": True,
            "duration_method": "competing physical hazard after diagonal renewal",
            "hard_sections_3_to_6_log_refinement_uniform": True,
        },
        "independent_audit_obligations": [
            (
                "two-stage raw diagonal renewal: pure nested class then "
                "small interrupted exact-return kernel, including boundary "
                "hits and physical time"
            ),
            (
                "same-order inner Feynman-Kac endpoint from bounded "
                "opening/post-first-slow data for every reaction vector"
            ),
            "exceptional first-defect comparison with arbitrary fixed rates",
            (
                "146-support fixed-cut and contracted nonself operator "
                "placement with service/upward/boundary terminals"
            ),
            (
                "analytic all-k coupled source-endpoint invariant, with the "
                "finite one-defect ledger used only as regression, plus the "
                "three-weight terminal gap at all slow orders"
            ),
            (
                "historical positive-debt scope, duration, endpoint-weighted "
                "full-G entropy, exact no-fast promotion versus charged open "
                "boundaries, and hard-section uniformity"
            ),
        ],
        "analytic_claim": (
            "candidate proof written; independent adversarial audit required"
        ),
        "descriptor_local_recurrence_certified": False,
        "pair_counts_promoted": 0,
        "certification_flags": flags,
    }
    payload["payload_sha256"] = _encoded_sha256(payload)
    return payload


if __name__ == "__main__":
    print(json.dumps(repair_certificate(), indent=2, sort_keys=True))
