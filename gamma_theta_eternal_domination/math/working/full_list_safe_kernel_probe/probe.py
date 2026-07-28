#!/usr/bin/env python3
"""Bounded falsifier for the color-restricted full-list safe-kernel lemma.

This is an ordinary-set implementation.  It imports no campaign evaluator
or transition core.  The only external executable is the pinned nauty
``geng`` used as a stream of connected unlabeled graphs.

For an independent triple S, a target x, and u in S, define

    B_u(S,x) = {S-u+y : y is a complement-neighbor of x}.

The u-restricted kernel is the greatest one-guard-safe family among all
dominating triples outside B_u(S,x).  The candidate lemma asks whether, in a
graph with gamma=alpha=gamma-infinity=3, whenever x has a full response list
in the unrestricted greatest family, there is a u for which both S and
S-u+x survive in this restricted kernel.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
MMV_CATALOG = CAMPAIGN / "instances" / "mmv2022_table9.csv"

VertexSet = frozenset[int]
Graph = tuple[VertexSet, ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> Graph:
    text = record.strip()
    if not text or text.startswith("~"):
        raise ValueError("only short ordinary graph6 records are supported")
    order = ord(text[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("invalid graph6 order")
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) != ((needed + 5) // 6) * 6 or any(bits[needed:]):
        raise ValueError(f"noncanonical graph6 padding in {record!r}")
    rows = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low].add(high)
                rows[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def subsets(order: int, size: int):
    yield from (
        frozenset(group)
        for group in itertools.combinations(range(order), size)
    )


def independent(graph: Graph, state: VertexSet) -> bool:
    return all(graph[v].isdisjoint(state - {v}) for v in state)


def dominates(graph: Graph, state: VertexSet) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def exact_gamma(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in subsets(len(graph), size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def exact_alpha(graph: Graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(
            independent(graph, state)
            for state in subsets(len(graph), size)
        ):
            return size
    return 0


def alpha_at_most_three(graph: Graph) -> bool:
    return not any(
        independent(graph, state)
        for state in subsets(len(graph), 4)
    )


def gamma_at_least_three(graph: Graph) -> bool:
    return not any(
        dominates(graph, state)
        for size in (1, 2)
        for state in subsets(len(graph), size)
    )


def greatest_safe_family(
    graph: Graph,
    size: int,
    *,
    banned: frozenset[VertexSet] = frozenset(),
) -> tuple[frozenset[VertexSet], tuple[int, ...]]:
    active = {
        state
        for state in subsets(len(graph), size)
        if state not in banned and dominates(graph, state)
    }
    deletion_rounds: list[int] = []
    while True:
        delete: set[VertexSet] = set()
        for state in active:
            for attack in range(len(graph)):
                if attack in state:
                    continue
                if not any(
                    attack in graph[guard]
                    and (state - {guard}) | {attack} in active
                    for guard in state
                ):
                    delete.add(state)
                    break
        if not delete:
            return frozenset(active), tuple(deletion_rounds)
        deletion_rounds.append(len(delete))
        active.difference_update(delete)


def literal_family_audit(
    graph: Graph,
    family: frozenset[VertexSet],
) -> dict[str, int | bool]:
    obligations = 0
    for state in family:
        if not dominates(graph, state):
            raise AssertionError(f"nondominating state {sorted(state)}")
        for attack in range(len(graph)):
            if attack in state:
                continue
            obligations += 1
            if not any(
                attack in graph[guard]
                and (state - {guard}) | {attack} in family
                for guard in state
            ):
                raise AssertionError(
                    f"missing response at {sorted(state)}, attack {attack}"
                )
    return {
        "states": len(family),
        "unoccupied_attack_obligations": obligations,
        "valid": True,
    }


def response_list(
    graph: Graph,
    family: frozenset[VertexSet],
    reference: VertexSet,
    target: int,
) -> VertexSet:
    return frozenset(
        guard
        for guard in reference
        if target in graph[guard]
        and (reference - {guard}) | {target} in family
    )


def static_response_list(
    graph: Graph,
    reference: VertexSet,
    target: int,
) -> VertexSet:
    return frozenset(
        guard
        for guard in reference
        if target in graph[guard]
        and dominates(graph, (reference - {guard}) | {target})
    )


def complement_neighbors(graph: Graph, vertex: int) -> VertexSet:
    return frozenset(
        other
        for other in range(len(graph))
        if other != vertex and other not in graph[vertex]
    )


def family_lists(
    graph: Graph,
    family: frozenset[VertexSet],
    reference: VertexSet,
) -> dict[int, VertexSet]:
    return {
        target: response_list(graph, family, reference, target)
        for target in range(len(graph))
        if target not in reference
    }


def compatible_anchored_colorings(
    graph: Graph,
    reference: VertexSet,
    lists: dict[int, VertexSet],
    *,
    limit: int = 10000,
) -> tuple[dict[int, int], ...]:
    coloring = {anchor: anchor for anchor in reference}
    targets = sorted(
        lists,
        key=lambda vertex: (
            len(lists[vertex]),
            -len(complement_neighbors(graph, vertex)),
            vertex,
        ),
    )
    answers: list[dict[int, int]] = []

    def search(index: int) -> None:
        if len(answers) >= limit:
            return
        if index == len(targets):
            answers.append(dict(sorted(coloring.items())))
            return
        vertex = targets[index]
        for color in sorted(lists[vertex]):
            if any(
                other in coloring
                and coloring[other] == color
                and other not in graph[vertex]
                for other in range(len(graph))
                if other != vertex
            ):
                continue
            coloring[vertex] = color
            search(index + 1)
            del coloring[vertex]

    if all(lists[target] for target in targets):
        search(0)
    return tuple(answers)


def exact_chromatic_number(graph: Graph) -> int:
    """Exact chromatic number of the supplied graph by DSATUR backtracking."""

    order = len(graph)
    degrees = tuple(len(row) for row in graph)

    def colorable(color_count: int) -> bool:
        colors = [-1] * order
        neighbor_colors = [set() for _ in range(order)]

        def search(colored: int) -> bool:
            if colored == order:
                return True
            uncolored = [v for v in range(order) if colors[v] < 0]
            vertex = max(
                uncolored,
                key=lambda v: (
                    len(neighbor_colors[v]),
                    degrees[v],
                    -v,
                ),
            )
            forbidden = neighbor_colors[vertex]
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                changed: list[int] = []
                for neighbor in graph[vertex]:
                    if colors[neighbor] < 0 and color not in neighbor_colors[neighbor]:
                        neighbor_colors[neighbor].add(color)
                        changed.append(neighbor)
                if search(colored + 1):
                    return True
                for neighbor in changed:
                    neighbor_colors[neighbor].remove(color)
                colors[vertex] = -1
            return False

        return search(0)

    for count in range(1, order + 1):
        if colorable(count):
            return count
    raise AssertionError("finite graph is not colorable")


def complement_graph(graph: Graph) -> Graph:
    return tuple(complement_neighbors(graph, vertex) for vertex in range(len(graph)))


def exact_parameters(graph: Graph) -> dict[str, int]:
    gamma = exact_gamma(graph)
    alpha = exact_alpha(graph)
    eternal = None
    for size in range(alpha, len(graph) + 1):
        family, _ = greatest_safe_family(graph, size)
        if family:
            eternal = size
            break
    if eternal is None:
        raise AssertionError("all-occupied state must be eternal")
    theta = exact_chromatic_number(complement_graph(graph))
    return {
        "gamma": gamma,
        "alpha": alpha,
        "gamma_infinity": eternal,
        "theta": theta,
    }


def safe_kernel_report(
    graph: Graph,
    reference: VertexSet,
    target: int,
) -> dict[str, object]:
    greatest, greatest_rounds = greatest_safe_family(graph, 3)
    greatest_lists = family_lists(graph, greatest, reference)
    h_neighbors = complement_neighbors(graph, target)
    colors: dict[str, object] = {}
    successes: list[int] = []

    for color in sorted(reference):
        banned = frozenset(
            (reference - {color}) | {neighbor}
            for neighbor in h_neighbors
        )
        restricted, rounds = greatest_safe_family(
            graph,
            3,
            banned=banned,
        )
        selected = (reference - {color}) | {target}
        survives = reference in restricted and selected in restricted
        if survives:
            successes.append(color)
        restricted_lists = (
            family_lists(graph, restricted, reference)
            if reference in restricted
            else {}
        )
        colorings = (
            compatible_anchored_colorings(
                graph,
                reference,
                restricted_lists,
            )
            if restricted_lists
            else ()
        )
        colors[str(color)] = {
            "banned_states": len(banned),
            "banned_dominating_states": sum(
                dominates(graph, state) for state in banned
            ),
            "kernel_states": len(restricted),
            "deletion_rounds": list(rounds),
            "reference_survives": reference in restricted,
            "selected_target_state": sorted(selected),
            "selected_target_state_survives": selected in restricted,
            "candidate_survives": survives,
            "forbidden_swap_survivors": sum(
                state in restricted for state in banned
            ),
            "restricted_response_lists": {
                str(vertex): sorted(values)
                for vertex, values in restricted_lists.items()
            },
            "compatible_anchored_coloring_count": len(colorings),
            "compatible_anchored_colorings": [
                {str(vertex): value for vertex, value in coloring.items()}
                for coloring in colorings[:20]
            ],
        }

    return {
        "reference": sorted(reference),
        "target": target,
        "target_complement_neighbors": sorted(h_neighbors),
        "static_target_list": sorted(
            static_response_list(graph, reference, target)
        ),
        "reference_in_greatest_family": reference in greatest,
        "greatest_family_target_list": sorted(
            greatest_lists.get(target, frozenset())
        ),
        "target_full_in_greatest_family": (
            reference in greatest
            and greatest_lists.get(target, frozenset()) == reference
        ),
        "unrestricted_greatest_family_states": len(greatest),
        "unrestricted_deletion_rounds": list(greatest_rounds),
        "successful_colors": successes,
        "candidate_lemma_holds_at_incidence": bool(successes),
        "colors": colors,
    }


def parse_family(text: str) -> frozenset[VertexSet]:
    return frozenset(
        frozenset(int(char) for char in token)
        for token in text.split()
    )


FDZRO_FAMILY_17 = parse_family(
    """
    012 014 024 026 046 123 124 125 134 145 234 236 245 246 256 346 456
    """
)

GFZNC_FAMILY_35 = parse_family(
    """
    012 015 016 024 026 036 045 046 056
    123 124 125 127 135 136 145 146 156 157 167
    234 236 245 246 247 256 267
    345 346 356 367 456 457 467 567
    """
)


def named_control(
    name: str,
    graph6: str,
    incidences: tuple[tuple[VertexSet, int], ...],
    *,
    specified_families: tuple[
        tuple[str, frozenset[VertexSet], VertexSet], ...
    ] = (),
    canonical_expected: str | None = None,
) -> dict[str, object]:
    graph = decode_graph6(graph6)
    greatest, _ = greatest_safe_family(graph, 3)
    record: dict[str, object] = {
        "name": name,
        "graph6_labeled": graph6,
        "order": len(graph),
        "size": sum(map(len, graph)) // 2,
        "parameters": exact_parameters(graph),
        "greatest_eternal_three_family": literal_family_audit(graph, greatest),
        "incidences": [
            safe_kernel_report(graph, reference, target)
            for reference, target in incidences
        ],
        "specified_families": {},
    }
    if canonical_expected is not None:
        process = subprocess.run(
            (str(LABELG), "-q"),
            input=graph6 + "\n",
            text=True,
            capture_output=True,
            check=True,
        )
        canonical = process.stdout.strip()
        if process.stderr or canonical != canonical_expected:
            raise AssertionError(
                f"canonicalization mismatch: {canonical!r}, {process.stderr!r}"
            )
        record["graph6_canonical"] = canonical

    specified_records: dict[str, object] = {}
    for family_name, family, reference in specified_families:
        audit = literal_family_audit(graph, family)
        lists = family_lists(graph, family, reference)
        specified_records[family_name] = {
            **audit,
            "reference": sorted(reference),
            "response_lists": {
                str(target): sorted(values)
                for target, values in lists.items()
            },
            "full_targets": [
                target
                for target, values in lists.items()
                if values == reference
            ],
            "strict_subfamily_of_greatest": family < greatest,
        }
    record["specified_families"] = specified_records
    return record


def scan_connected_equality_graphs(
    maximum_order: int,
    deadline: float,
) -> dict[str, object]:
    orders: list[dict[str, object]] = []
    countermodels: list[dict[str, object]] = []

    for order in range(1, maximum_order + 1):
        stream_digest = hashlib.sha256()
        connected = 0
        static_candidate_graphs = 0
        static_full_incidences = 0
        equality_graphs = 0
        equality_static_full_incidences = 0
        family_full_incidences = 0
        candidate_successes = 0
        with subprocess.Popen(
            (str(GENG), "-cq", str(order)),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:
            if process.stdout is None or process.stderr is None:
                raise AssertionError("failed to capture geng streams")
            for raw in process.stdout:
                if time.monotonic() > deadline:
                    process.terminate()
                    raise TimeoutError("bounded scan exceeded its time budget")
                record = raw.strip()
                if not record:
                    continue
                connected += 1
                stream_digest.update(record.encode("ascii") + b"\n")
                graph = decode_graph6(record)
                possible: list[tuple[VertexSet, int]] = []
                for reference in subsets(order, 3):
                    if not independent(graph, reference):
                        continue
                    for target in range(order):
                        if target in reference:
                            continue
                        if static_response_list(graph, reference, target) == reference:
                            possible.append((reference, target))
                if not possible:
                    continue
                static_candidate_graphs += 1
                static_full_incidences += len(possible)

                # ``possible`` supplies an independent triple.  If there is
                # no independent four-set, that triple is maximum and hence
                # maximal, so it dominates.  The pair test then gives the
                # exact equality gamma=alpha=3 without general subset scans.
                if not alpha_at_most_three(graph) or not gamma_at_least_three(graph):
                    continue
                greatest, _ = greatest_safe_family(graph, 3)
                if not greatest:
                    continue
                equality_graphs += 1
                equality_static_full_incidences += len(possible)

                for reference, target in possible:
                    if reference not in greatest:
                        continue
                    if (
                        response_list(graph, greatest, reference, target)
                        != reference
                    ):
                        continue
                    family_full_incidences += 1
                    report = safe_kernel_report(graph, reference, target)
                    if report["candidate_lemma_holds_at_incidence"]:
                        candidate_successes += 1
                    else:
                        countermodels.append(
                            {
                                "graph6": record,
                                "order": order,
                                "reference": sorted(reference),
                                "target": target,
                                "report": report,
                            }
                        )
            stderr = process.stderr.read()
            return_code = process.wait()
        if return_code or stderr:
            raise RuntimeError(
                f"geng order {order} failed: return={return_code}, stderr={stderr!r}"
            )
        orders.append(
            {
                "order": order,
                "connected_graphs": connected,
                "graph6_stream_sha256": stream_digest.hexdigest(),
                "graphs_with_static_full_incidence": static_candidate_graphs,
                "static_full_incidences": static_full_incidences,
                "equality_graphs_among_static_candidates": equality_graphs,
                "equality_static_full_incidences": (
                    equality_static_full_incidences
                ),
                "greatest_family_full_incidences": family_full_incidences,
                "candidate_successes": candidate_successes,
                "candidate_failures": (
                    family_full_incidences - candidate_successes
                ),
            }
        )

    return {
        "orders": orders,
        "totals": {
            key: sum(int(row[key]) for row in orders)
            for key in (
                "connected_graphs",
                "graphs_with_static_full_incidence",
                "static_full_incidences",
                "equality_graphs_among_static_candidates",
                "equality_static_full_incidences",
                "greatest_family_full_incidences",
                "candidate_successes",
                "candidate_failures",
            )
        },
        "countermodels": countermodels,
    }


def compact_incidence(report: dict[str, object]) -> dict[str, object]:
    return {
        "reference": report["reference"],
        "target": report["target"],
        "successful_colors": report["successful_colors"],
        "candidate_lemma_holds_at_incidence": report[
            "candidate_lemma_holds_at_incidence"
        ],
        "kernel_state_counts": {
            color: data["kernel_states"]
            for color, data in report["colors"].items()
        },
        "compatible_coloring_counts": {
            color: data["compatible_anchored_coloring_count"]
            for color, data in report["colors"].items()
        },
    }


def scan_mmv_catalog(deadline: float) -> dict[str, object]:
    """Inspect the fixed published 56-graph near-miss catalog only."""

    records: list[dict[str, object]] = []
    graph_count = 0
    eligible_graphs = 0
    full_incidence_count = 0
    successful_incidence_count = 0
    failed_incidence_count = 0
    safe_success_with_theta_gap = 0

    with MMV_CATALOG.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if time.monotonic() > deadline:
                raise TimeoutError("catalog scan exceeded its time budget")
            graph_count += 1
            graph = decode_graph6(row["graph6"])
            parameters = exact_parameters(graph)
            greatest, _ = greatest_safe_family(graph, 3)
            if parameters["alpha"] != 3 or parameters["gamma_infinity"] != 3:
                continue
            eligible_graphs += 1
            incidences: list[dict[str, object]] = []
            for reference in subsets(len(graph), 3):
                if not independent(graph, reference) or reference not in greatest:
                    continue
                for target in range(len(graph)):
                    if target in reference:
                        continue
                    if response_list(graph, greatest, reference, target) != reference:
                        continue
                    full_incidence_count += 1
                    report = safe_kernel_report(graph, reference, target)
                    compact = compact_incidence(report)
                    incidences.append(compact)
                    if report["candidate_lemma_holds_at_incidence"]:
                        successful_incidence_count += 1
                        if parameters["theta"] > 3:
                            safe_success_with_theta_gap += 1
                    else:
                        failed_incidence_count += 1
            if incidences:
                records.append(
                    {
                        "catalog_id": row["catalog_id"],
                        "graph6": row["graph6"],
                        "parameters": parameters,
                        "incidences": incidences,
                    }
                )

    return {
        "scope": (
            "the fixed local copy of the 56 published MMV 2022 Table 9 "
            "near-miss graphs; no new order-10-or-11 graph enumeration"
        ),
        "catalog_path": str(MMV_CATALOG.relative_to(CAMPAIGN)),
        "catalog_sha256": sha256(MMV_CATALOG),
        "graphs": graph_count,
        "eligible_alpha_equals_eternal_three_graphs": eligible_graphs,
        "graphs_with_full_greatest_family_incidence": len(records),
        "full_greatest_family_incidences": full_incidence_count,
        "successful_incidences": successful_incidence_count,
        "failed_incidences": failed_incidence_count,
        "safe_successes_with_theta_gap": safe_success_with_theta_gap,
        "records": records,
    }


def build_result(maximum_order: int, max_seconds: float) -> dict[str, object]:
    started = time.monotonic()
    deadline = started + max_seconds

    controls = {
        "K_full_equality_order12": named_control(
            "K full-list equality control",
            "Ksv`f\\knJVis",
            ((frozenset({1, 2, 3}), 0),),
            canonical_expected="K{eYptMJynEn",
        ),
        "HCQebjw_static_not_family": named_control(
            "HCQebjw static-full but family-singleton control",
            "HCQebjw",
            ((frozenset({0, 1, 2}), 8),),
        ),
        "FDzro_gamma2_full": named_control(
            "FDzro gamma-two full-list control",
            "FDzro",
            (
                (frozenset({0, 1, 2}), 4),
                (frozenset({0, 1, 2}), 5),
            ),
            specified_families=(
                ("proper_family_17", FDZRO_FAMILY_17, frozenset({0, 1, 2})),
            ),
        ),
        "GFznc_ridge_control": named_control(
            "GFznc ridge-covariant no-full-list control",
            "GFznc{",
            (
                (frozenset({0, 1, 2}), 3),
                (frozenset({1, 2, 7}), 0),
            ),
            specified_families=(
                ("specified_family_35", GFZNC_FAMILY_35, frozenset({0, 1, 2})),
                ("specified_family_35_at_127", GFZNC_FAMILY_35, frozenset({1, 2, 7})),
            ),
            canonical_expected="G@~~fc",
        ),
        "IFjLBXiow_order10_static_only": named_control(
            "existing order-10 static-full non-eternal-three control",
            "IFjLBXiow",
            ((frozenset({0, 1, 2}), 3),),
        ),
    }

    scan = scan_connected_equality_graphs(maximum_order, deadline)
    catalog = scan_mmv_catalog(deadline)
    return {
        "schema": "full-list-color-restricted-safe-kernel-probe-v1",
        "status": "COMPLETE",
        "definition": {
            "candidate_hypotheses": (
                "gamma=alpha=gamma-infinity=3, S is an independent triple "
                "in the unrestricted greatest eternal three-family"
            ),
            "reference": "an independent triple S",
            "full_target": (
                "x outside S with L_S(x)=S in the unrestricted greatest "
                "eternal three-family"
            ),
            "color_restricted_bans": (
                "for u in S, ban every triple S-u+y with "
                "y in N_H(x)"
            ),
            "restricted_kernel": (
                "the greatest one-guard-safe subfamily of all dominating "
                "triples not banned"
            ),
            "success": (
                "both S and S-u+x survive for at least one u"
            ),
        },
        "claim_boundary": {
            "candidate_lemma_proved": False,
            "candidate_lemma_refuted": bool(scan["countermodels"]),
            "candidate_lemma_test_vacuous_through_order9": (
                scan["totals"]["greatest_family_full_incidences"] == 0
            ),
            "gamma_two_catalog_shows_hypotheses_are_essential": (
                catalog["successful_incidences"] > 0
                and catalog["failed_incidences"] > 0
            ),
            "safe_kernel_is_strictly_weaker_than_theta3_outside_gamma3": (
                catalog["safe_successes_with_theta_gap"] > 0
            ),
            "bounded_scan_only": True,
            "universal_conjecture_resolved": False,
            "finite_frontier_raised": False,
            "order14_used": False,
        },
        "logical_relation": {
            "theta3_implies_safe_kernel_success": (
                "PROVED IN NOTE: a three-clique partition supplies the "
                "eternal family of configurations with one guard per clique; "
                "for the color of x this family contains S and S-u+x and "
                "avoids every banned swap"
            ),
            "safe_kernel_success_implies_theta3": (
                "FALSE WITHOUT THE GAMMA=3 HYPOTHESIS: MMV-021 has theta=4 "
                "and exact safe-kernel successes with zero compatible "
                "anchored colorings. Under gamma=3 no converse is proved."
            ),
            "iteration_warning": (
                "recomputing a greatest restricted kernel can reintroduce "
                "states banned in earlier choices, so the lemma as stated "
                "does not provide a monotone elimination of all full targets"
            ),
        },
        "controls": controls,
        "connected_equality_scan": scan,
        "fixed_published_near_miss_catalog": catalog,
        "scope": {
            "orders": [1, maximum_order],
            "connected_unlabeled_only": True,
            "higher_order_inputs": [
                "the fixed 56-graph MMV 2022 Table 9 near-miss catalog",
                "IFjLBXiow (existing named order-10 static-only control)",
                "K{eYptMJynEn (existing named order-12 equality control)",
            ],
            "broad_order10_plus_enumeration": False,
            "max_seconds": max_seconds,
            "elapsed_seconds": time.monotonic() - started,
            "peak_memory_design": (
                "one graph and at most a few hundred triple states at a time"
            ),
        },
        "source": {
            "python": "standard library ordinary frozensets",
            "geng": str(GENG.relative_to(CAMPAIGN)),
            "geng_sha256": sha256(GENG),
            "labelg_sha256": sha256(LABELG),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=9)
    parser.add_argument("--max-seconds", type=float, default=240.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("result.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.max_order <= 9:
        raise SystemExit("--max-order must lie in 1..9")
    result = build_result(args.max_order, args.max_seconds)
    source_path = Path(__file__).resolve()
    result["source"]["probe_sha256_before_result_write"] = sha256(source_path)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "elapsed_seconds": result["scope"]["elapsed_seconds"],
                "scan_totals": result["connected_equality_scan"]["totals"],
                "countermodels": len(
                    result["connected_equality_scan"]["countermodels"]
                ),
                "output": str(args.output),
                "output_sha256": sha256(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
