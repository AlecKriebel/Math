"""Claim-neutral structural certificate for the 1,227 one-active pairs.

The affine-first residual selector has 1,227 pairs whose nonempty feasible
failure set consists entirely of one-active descriptors (3,297 incidences).
This module relabels the active species to ``C`` and freezes the finite data
needed by a future reflected-level theorem:

* the stripped fast-phase shape in each linkage;
* the initially enabled source layer;
* inactive-coordinate promotion boundaries;
* a canonical Hamilton-cycle reflected-debt depth regression; and
* the absence of a full-network affine invariant with nonzero active
  coefficient (such an invariant would contradict affine feasibility).

The depth computation is deliberately only a regression for the canonical
obstruction cycles and a bounded word box.  It is not an arbitrary-strong-
orientation theorem and it makes no recurrence claim.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_phase_shape as phase_shape
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Descriptor = tier.TierDescriptor

POPULATION_BOUND = 7
DEBT_BOUND = 8
INFINITY = 10**6

EXPECTED_ROWS_SHA256 = (
    "a05082a912f7629d107d14609a2ee65cae7b8eb997d7a17a4ac9934c1b66986d"
)
EXPECTED_PAYLOAD_SHA256 = (
    "283c02163c6a57cb10e9c13a47ad84cb3457ce9d428276719cf9e69dd3343034"
)


@dataclass(frozen=True)
class ProjectedEdge:
    source: tuple[int, int]
    delta: tuple[int, int]
    active_delta: int
    active_source_degree: int


def incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    return phase_shape.candidate_incidences()


def _enabled(source: tuple[int, int], state: tuple[int, int]) -> bool:
    return source[0] <= state[0] and source[1] <= state[1]


def _has_fast_clock(
    state: tuple[int, int], edges: tuple[ProjectedEdge, ...]
) -> bool:
    return any(
        edge.active_source_degree == 1 and _enabled(edge.source, state)
        for edge in edges
    )


def _projected_edges(
    descriptor: Descriptor,
    orientation: tuple[tuple[int, int], ...],
) -> tuple[ProjectedEdge, ...]:
    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    result = []
    for source, target in orientation:
        y = closure.COMPLEXES[source]
        z = closure.COMPLEXES[target]
        result.append(
            ProjectedEdge(
                source=tuple(y[index] for index in inactive),
                delta=tuple(z[index] - y[index] for index in inactive),
                active_delta=z[active] - y[active],
                active_source_degree=y[active],
            )
        )
    return tuple(result)


def _canonical_orientation(
    pair: Pair, descriptor: Descriptor
) -> tuple[tuple[int, int], ...]:
    first, second = tier.obstruction_cycles(pair, descriptor)
    return first + second


def _depth_search(
    start: tuple[int, int],
    start_debt: int,
    edges: tuple[ProjectedEdge, ...],
    *,
    seek_positive_base: bool,
) -> dict[tuple[tuple[int, int], int], int]:
    """Zero-one BFS for unresolved debt or the first surplus exit.

    The debt update is the exact reflected update.  A slow-before-fast race
    costs one whenever a degree-zero source fires while a degree-one source
    is enabled.  Surplus is the transition ``D=0, active_delta=-1``.
    """

    queue = deque([(start, start_debt)])
    distance = {(start, start_debt): 0}
    hits: dict[tuple[tuple[int, int], int], int] = {}
    while queue:
        state, debt = queue.popleft()
        old = distance[(state, debt)]
        fast = _has_fast_clock(state, edges)
        for edge in edges:
            if not _enabled(edge.source, state):
                continue
            endpoint = tuple(
                state[index] + edge.delta[index] for index in range(2)
            )
            if not all(0 <= value <= POPULATION_BOUND for value in endpoint):
                continue
            surplus = debt == 0 and edge.active_delta < 0
            new_debt = max(0, min(DEBT_BOUND, debt + edge.active_delta))
            rare = int(edge.active_source_degree == 0 and fast)
            new_distance = old + rare
            if seek_positive_base:
                if new_debt > 0 and not _has_fast_clock(endpoint, edges):
                    key = endpoint, new_debt
                    hits[key] = min(hits.get(key, INFINITY), new_distance)
            elif surplus:
                key = endpoint, 0
                hits[key] = min(hits.get(key, INFINITY), new_distance)
                continue
            key = endpoint, new_debt
            if new_distance < distance.get(key, INFINITY):
                distance[key] = new_distance
                (queue.append if rare else queue.appendleft)(key)
    return hits


def canonical_depth_row(
    pair: Pair, descriptor: Descriptor
) -> dict[str, object]:
    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    start = tuple(descriptor.caps[index] for index in inactive)
    edges = _projected_edges(descriptor, _canonical_orientation(pair, descriptor))
    assert all(edge.active_source_degree <= 1 for edge in edges)

    direct = _depth_search(start, 0, edges, seek_positive_base=False)
    creations = _depth_search(start, 0, edges, seek_positive_base=True)
    debt_rows = []
    for (endpoint, debt), creation_depth in sorted(creations.items()):
        services = _depth_search(
            endpoint, debt, edges, seek_positive_base=False
        )
        debt_rows.append(
            {
                "endpoint": endpoint,
                "debt": debt,
                "creation_depth": creation_depth,
                "surplus_service_depth": min(
                    services.values(), default=INFINITY
                ),
            }
        )
    return {
        "direct_surplus_depth": min(direct.values(), default=INFINITY),
        "positive_debt_bases": debt_rows,
    }


def _relabel_candidates(
    pair: Pair, descriptor: Descriptor
) -> tuple[dict[str, object], ...]:
    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    result = []
    for first, second in (inactive, tuple(reversed(inactive))):
        old_for_new = (first, second, active)
        supports = []
        for mask in pair:
            names = []
            for node in tier._nodes(mask):
                old = closure.COMPLEXES[node]
                new = tuple(old[index] for index in old_for_new)
                names.append(closure.NAMES[closure.COMPLEXES.index(new)])
            supports.append(tuple(sorted(names, key=closure.NAMES.index)))
        result.append(
            {
                "supports": tuple(supports),
                "caps": (descriptor.caps[first], descriptor.caps[second]),
                "old_for_new": old_for_new,
            }
        )
    return tuple(result)


def _normalized(pair: Pair, descriptor: Descriptor) -> dict[str, object]:
    return min(
        _relabel_candidates(pair, descriptor),
        key=lambda row: (row["supports"], row["caps"]),
    )


TOP_MENU = frozenset(("C", "AC", "BC"))


def _linkage_phase(support: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    top = tuple(name for name in support if name in TOP_MENU)
    if not top:
        return "lower_only", ()
    if len(top) == len(support):
        stripped = []
        for name in top:
            vector = list(closure.COMPLEXES[closure.NAME_TO_INDEX[name]])
            vector[2] -= 1
            stripped.append(closure.NAMES[closure.COMPLEXES.index(tuple(vector))])
        return "whole_top", tuple(sorted(stripped, key=closure.NAMES.index))
    stripped = []
    for name in top:
        vector = list(closure.COMPLEXES[closure.NAME_TO_INDEX[name]])
        vector[2] -= 1
        stripped.append(closure.NAMES[closure.COMPLEXES.index(tuple(vector))])
    return "mixed_killed", tuple(sorted(stripped, key=closure.NAMES.index))


def _source_enabled(name: str, caps: tuple[int, int]) -> bool:
    vector = closure.COMPLEXES[closure.NAME_TO_INDEX[name]]
    return vector[0] <= caps[0] and vector[1] <= caps[1]


def _initial_access(
    supports: tuple[tuple[str, ...], tuple[str, ...]],
    caps: tuple[int, int],
) -> str:
    phases = tuple(_linkage_phase(support) for support in supports)
    if any(kind == "whole_top" for kind, _ in phases):
        return "whole_open_countable"
    enabled_top = tuple(
        name
        for support in supports
        for name in support
        if name in TOP_MENU and _source_enabled(name, caps)
    )
    if enabled_top:
        return "mixed_direct_enabled"
    enabled_lower = tuple(
        name
        for support in supports
        for name in support
        if name not in TOP_MENU and _source_enabled(name, caps)
    )
    if not enabled_lower:
        return "frozen_face"
    if set(enabled_lower) == {"0"}:
        return "zero_source_seed"
    return "nonzero_lower_seed"


def _promotion_signature(
    supports: tuple[tuple[str, ...], tuple[str, ...]]
) -> tuple[str, str]:
    full = []
    fast = []
    for coordinate, label in ((0, "A"), (1, "B")):
        if any(
            len(
                {
                    closure.COMPLEXES[closure.NAME_TO_INDEX[name]][coordinate]
                    for name in support
                }
            )
            > 1
            for support in supports
        ):
            full.append(label)
        if any(
            len(
                {
                    closure.COMPLEXES[closure.NAME_TO_INDEX[name]][coordinate]
                    for name in support
                    if name in TOP_MENU
                }
            )
            > 1
            for support in supports
            if any(name in TOP_MENU for name in support)
        ):
            fast.append(label)
    return "".join(fast) or "none", "".join(full) or "none"


def _has_active_coefficient_invariant(
    pair: Pair, descriptor: Descriptor
) -> bool:
    active, = tier._active_coordinates(descriptor)
    return any(vector[active] for vector in feasibility.invariant_basis(pair))


def incidence_row(pair: Pair, descriptor: Descriptor) -> dict[str, object]:
    normalized = _normalized(pair, descriptor)
    supports = normalized["supports"]
    caps = normalized["caps"]
    assert isinstance(supports, tuple) and isinstance(caps, tuple)
    phases = tuple(_linkage_phase(support) for support in supports)
    depth = canonical_depth_row(pair, descriptor)
    debt_rows = depth["positive_debt_bases"]
    assert isinstance(debt_rows, list)
    finite_depths = tuple(
        row["surplus_service_depth"]
        for row in debt_rows
        if row["surplus_service_depth"] < INFINITY
    )
    if not debt_rows:
        depth_class = "no_positive_debt_base"
    elif not finite_depths:
        depth_class = "canonical_no_service_word"
    elif max(finite_depths) == 0:
        depth_class = "zero_contest_from_every_debt_base"
    elif min(finite_depths) == 0:
        depth_class = "mixed_zero_and_nested_service"
    else:
        depth_class = "nested_slow_before_fast_service"
    if not debt_rows:
        depth_order_class = "no_positive_debt_base"
    elif any(row["surplus_service_depth"] >= INFINITY for row in debt_rows):
        depth_order_class = "some_service_word_outside_box"
    else:
        differences = tuple(
            row["creation_depth"] - row["surplus_service_depth"]
            for row in debt_rows
        )
        if min(differences) > 0:
            depth_order_class = "creation_strictly_deeper"
        elif min(differences) == 0:
            depth_order_class = "some_equal_none_shallower"
        else:
            depth_order_class = "some_creation_shallower"
    fast_promotion, full_promotion = _promotion_signature(supports)
    return {
        "pair": [list(part) for part in closure.pair_payload(pair)],
        "weight": list(descriptor.weight),
        "caps": list(descriptor.caps),
        "normalized_supports": [list(support) for support in supports],
        "normalized_caps": list(caps),
        "phase_signature": [
            [kind, list(stripped)] for kind, stripped in phases
        ],
        "initial_access": _initial_access(supports, caps),
        "fast_promotion_coordinates": fast_promotion,
        "full_promotion_coordinates": full_promotion,
        "full_active_coefficient_invariant": (
            _has_active_coefficient_invariant(pair, descriptor)
        ),
        "canonical_direct_surplus_depth": depth["direct_surplus_depth"],
        "canonical_depth_class": depth_class,
        "canonical_depth_order_class": depth_order_class,
        "canonical_positive_debt_bases": debt_rows,
    }


def _template_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple((phase[0], tuple(phase[1])) for phase in row["phase_signature"]),
        row["initial_access"],
        row["canonical_depth_class"],
        row["fast_promotion_coordinates"],
        tuple(row["normalized_caps"]),
    )


def _coarse_template_key(row: dict[str, object]) -> tuple[object, ...]:
    """Quotient linkage order and cap representatives for analytic routing."""

    phases = tuple(
        sorted(
            (phase[0], tuple(phase[1]))
            for phase in row["phase_signature"]
        )
    )
    return (
        phases,
        row["initial_access"],
        row["canonical_depth_class"],
        row["fast_promotion_coordinates"],
    )


def _pair_stats(
    annotated: tuple[tuple[Pair, dict[str, object]], ...], predicate
) -> dict[str, object]:
    pairs = frozenset(pair for pair, row in annotated if predicate(row))
    return {
        "pairs": len(pairs),
        "pair_sha256": closure.pair_fingerprint(pairs),
    }


def certificate() -> dict[str, object]:
    annotated = tuple(
        sorted(
            (
                (pair, incidence_row(pair, descriptor))
                for pair, descriptor in incidences()
            ),
            key=lambda item: (
                item[1]["pair"], item[1]["weight"], item[1]["caps"]
            ),
        )
    )
    rows = tuple(row for _, row in annotated)
    phase_histogram = Counter(
        "+".join(phase[0] for phase in row["phase_signature"])
        for row in rows
    )
    access_histogram = Counter(row["initial_access"] for row in rows)
    depth_histogram = Counter(row["canonical_depth_class"] for row in rows)
    depth_order_histogram = Counter(
        row["canonical_depth_order_class"] for row in rows
    )
    access_depth_histogram = Counter(
        f'{row["initial_access"]}|{row["canonical_depth_class"]}'
        for row in rows
    )
    promotion_histogram = Counter(
        f'{row["fast_promotion_coordinates"]}/{row["full_promotion_coordinates"]}'
        for row in rows
    )
    templates = Counter(_template_key(row) for row in rows)
    coarse_templates = Counter(_coarse_template_key(row) for row in rows)
    template_payload = tuple(
        {
            "phase_signature": [
                [kind, list(stripped)] for kind, stripped in key[0]
            ],
            "initial_access": key[1],
            "canonical_depth_class": key[2],
            "fast_promotion_coordinates": key[3],
            "normalized_caps": list(key[4]),
            "incidences": count,
        }
        for key, count in sorted(templates.items(), key=lambda item: item[0])
    )
    coarse_template_payload = tuple(
        {
            "phase_signature": [
                [kind, list(stripped)] for kind, stripped in key[0]
            ],
            "initial_access": key[1],
            "canonical_depth_class": key[2],
            "fast_promotion_coordinates": key[3],
            "incidences": count,
        }
        for key, count in sorted(
            coarse_templates.items(), key=lambda item: item[0]
        )
    )
    critical_rows = tuple(
        row
        for row in rows
        if row["canonical_depth_order_class"]
        == "some_equal_none_shallower"
    )
    critical_pairs = tuple(
        sorted(
            {
                pair
                for pair, row in annotated
                if row["canonical_depth_order_class"]
                == "some_equal_none_shallower"
            }
        )
    )
    critical_debt_histogram = Counter(
        (
            debt_row["debt"],
            debt_row["creation_depth"],
            debt_row["surplus_service_depth"],
        )
        for row in critical_rows
        for debt_row in row["canonical_positive_debt_bases"]
        if debt_row["creation_depth"]
        <= debt_row["surplus_service_depth"]
    )
    critical_supports = {
        tuple(tuple(support) for support in row["normalized_supports"])
        for row in critical_rows
    }
    critical_pair_set = frozenset(critical_pairs)
    critical_pair_failure_counts = Counter(
        pair for pair, _ in annotated if pair in critical_pair_set
    )
    critical_pair_noncritical_incidences = sum(
        pair in critical_pair_set
        and row["canonical_depth_order_class"]
        != "some_equal_none_shallower"
        for pair, row in annotated
    )
    critical_pair_noncritical_payload = tuple(
        {
            "pair": row["pair"],
            "weight": row["weight"],
            "caps": row["caps"],
            "normalized_supports": row["normalized_supports"],
            "normalized_caps": row["normalized_caps"],
            "phase_signature": row["phase_signature"],
            "initial_access": row["initial_access"],
            "canonical_depth_class": row["canonical_depth_class"],
            "canonical_depth_order_class": row[
                "canonical_depth_order_class"
            ],
            "fast_promotion_coordinates": row[
                "fast_promotion_coordinates"
            ],
        }
        for pair, row in annotated
        if pair in critical_pair_set
        and row["canonical_depth_order_class"]
        != "some_equal_none_shallower"
    )
    critical_pair_axis_payload = []
    for pair in critical_pairs:
        pair_rows = tuple(
            row
            for candidate, row in annotated
            if candidate == pair
            and row["canonical_depth_order_class"]
            == "some_equal_none_shallower"
        )
        active_coordinates = tuple(
            sorted(
                {
                    index
                    for row in pair_rows
                    for index, value in enumerate(row["weight"])
                    if value > 0
                }
            )
        )
        mixed_shells = set()
        for active in active_coordinates:
            inactive = tuple(index for index in range(3) if index != active)
            shell_nodes = {(0, 0, 0)}
            for coordinate in inactive:
                vector = [0, 0, 0]
                vector[active] = 1
                vector[coordinate] = 1
                shell_nodes.add(tuple(vector))
            shell_mask = sum(
                1 << closure.COMPLEXES.index(vector)
                for vector in shell_nodes
            )
            assert shell_mask in pair
            mixed_shells.add(shell_mask)
        critical_pair_axis_payload.append(
            {
                "pair": [list(part) for part in closure.pair_payload(pair)],
                "critical_incidences": len(pair_rows),
                "active_species": ["ABC"[index] for index in active_coordinates],
                "mixed_shell_linkages": [
                    list(closure.support(mask)) for mask in sorted(mixed_shells)
                ],
            }
        )
    critical_pair_axis_payload = tuple(critical_pair_axis_payload)
    assert critical_supports
    assert all(
        supports[0] == ("0", "AC", "BC")
        for supports in critical_supports
    )
    assert all(
        {
            sum(
                closure.COMPLEXES[closure.NAME_TO_INDEX[name]][index]
                for index in (0, 1)
            )
            for name in supports[1]
        }
        == {1, 2}
        for supports in critical_supports
    )
    rows_hash = sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert rows_hash == EXPECTED_ROWS_SHA256
    payload: dict[str, object] = {
        "claim_scope": (
            "finite support, phase, boundary, and canonical Hamilton-word "
            "classification only; no arbitrary-orientation kinetic theorem "
            "and no recurrence claim"
        ),
        "candidate_pairs": len(phase_shape.candidate_pairs()),
        "candidate_incidences": len(rows),
        "normalized_active_species": "C",
        "phase_histogram": dict(sorted(phase_histogram.items())),
        "initial_access_histogram": dict(sorted(access_histogram.items())),
        "canonical_depth_histogram": dict(sorted(depth_histogram.items())),
        "canonical_depth_order_histogram": dict(
            sorted(depth_order_histogram.items())
        ),
        "access_depth_histogram": dict(sorted(access_depth_histogram.items())),
        "promotion_histogram": dict(sorted(promotion_histogram.items())),
        "full_active_coefficient_invariant_incidences": sum(
            bool(row["full_active_coefficient_invariant"]) for row in rows
        ),
        "fine_templates_with_caps_and_linkage_order": len(template_payload),
        "fine_template_payload": template_payload,
        "canonical_analytic_templates": len(coarse_template_payload),
        "canonical_template_payload": coarse_template_payload,
        "critical_equal_depth_incidences": len(critical_rows),
        "critical_equal_depth": _pair_stats(
            annotated,
            lambda row: row["canonical_depth_order_class"]
            == "some_equal_none_shallower",
        ),
        "critical_equal_depth_pair_payload": tuple(
            [list(part) for part in closure.pair_payload(pair)]
            for pair in critical_pairs
        ),
        "critical_normalized_support_templates": tuple(
            [list(support) for support in supports]
            for supports in sorted(critical_supports)
        ),
        "critical_pair_failure_count_histogram": dict(
            sorted(Counter(critical_pair_failure_counts.values()).items())
        ),
        "critical_pair_noncritical_incidences": (
            critical_pair_noncritical_incidences
        ),
        "critical_pair_noncritical_payload": (
            critical_pair_noncritical_payload
        ),
        "critical_pair_noncritical_class_histogram": dict(
            sorted(
                Counter(
                    (
                        f'{row["initial_access"]}|'
                        f'{row["canonical_depth_class"]}|'
                        f'{row["canonical_depth_order_class"]}'
                    )
                    for row in critical_pair_noncritical_payload
                ).items()
            )
        ),
        "critical_pair_axis_payload": critical_pair_axis_payload,
        "critical_pair_active_coordinate_count_histogram": dict(
            sorted(
                Counter(
                    len(row["active_species"])
                    for row in critical_pair_axis_payload
                ).items()
            )
        ),
        "critical_pair_mixed_shell_count_histogram": dict(
            sorted(
                Counter(
                    len(row["mixed_shell_linkages"])
                    for row in critical_pair_axis_payload
                ).items()
            )
        ),
        "critical_shell_structure": {
            "mixed_linkage": ["0", "AC", "BC"],
            "mixed_linkage_invariant": "Q=C-A-B",
            "lower_source_total_degrees": [1, 2],
            "normalized_support_templates": len(critical_supports),
            "averaged_q_drift_formula": (
                "-a_minus*Z[N+1]/Z[N]"
                "+a_plus*Z[N+2]/Z[N], with a_minus>0"
            ),
        },
        "critical_equal_depth_word_histogram": {
            f"debt={debt},creation={creation},service={service}": count
            for (debt, creation, service), count in sorted(
                critical_debt_histogram.items()
            )
        },
        "depth_pair_subsets": {
            depth_class: _pair_stats(
                annotated,
                lambda row, selected=depth_class: (
                    row["canonical_depth_class"] == selected
                ),
            )
            for depth_class in sorted(depth_histogram)
        },
        "access_pair_subsets": {
            access: _pair_stats(
                annotated,
                lambda row, selected=access: row["initial_access"] == selected,
            )
            for access in sorted(access_histogram)
        },
        "population_bound": POPULATION_BOUND,
        "debt_bound": DEBT_BOUND,
        "rows_sha256": rows_hash,
        "analytic_one_active_theorem_certified": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    digest = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    payload["payload_sha256"] = digest
    return payload


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
