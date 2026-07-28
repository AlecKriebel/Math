#!/usr/bin/env python3
"""Clean-room bounded falsifier for the adjacent true-twin reduction.

Only Python's standard library and the pinned nauty ``geng`` stream are
used.  No campaign evaluator, transition routine, or target-lemma code is
imported.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
TARGET = CAMPAIGN / "math" / "lemmas" / "adjacent_true_twin_reduction.md"
EXPECTED_CONNECTED = (0, 1, 1, 2, 6, 21, 112, 853, 11117)

Graph = tuple[int, ...]  # open-neighborhood bit masks


def file_sha256(path: Path) -> str:
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
        raise ValueError("noncanonical graph6 padding")
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def masks_of_size(order: int, size: int):
    for vertices in itertools.combinations(range(order), size):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


def dominates(graph: Graph, state: int) -> bool:
    covered = state
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        covered |= graph[vertex]
        remaining ^= bit
    return covered == (1 << len(graph)) - 1


def independent(graph: Graph, state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if graph[vertex] & (state ^ bit):
            return False
        remaining ^= bit
    return True


def clique(graph: Graph, state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if (state ^ bit) & ~graph[vertex]:
            return False
        remaining ^= bit
    return True


@functools.cache
def domination_number(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in masks_of_size(len(graph), size)):
            return size
    raise AssertionError("finite nonempty graph has no dominating set")


@functools.cache
def independence_number(graph: Graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(
            independent(graph, state)
            for state in masks_of_size(len(graph), size)
        ):
            return size
    return 0


@functools.cache
def clique_cover_number(graph: Graph) -> int:
    order = len(graph)

    @functools.cache
    def solve(remaining: int) -> int:
        if not remaining:
            return 0
        anchor_bit = remaining & -remaining
        anchor = anchor_bit.bit_length() - 1
        available = remaining & graph[anchor]
        best = 1 + solve(remaining ^ anchor_bit)
        subset = available
        while subset:
            candidate = subset | anchor_bit
            if clique(graph, candidate):
                best = min(best, 1 + solve(remaining & ~candidate))
            subset = (subset - 1) & available
        return best

    return solve((1 << order) - 1)


@functools.cache
def greatest_eternal_family(graph: Graph, size: int) -> frozenset[int]:
    active = {
        state
        for state in masks_of_size(len(graph), size)
        if dominates(graph, state)
    }
    while True:
        rejected: set[int] = set()
        for state in active:
            for target in range(len(graph)):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                legal = False
                guards = state & graph[target]
                while guards:
                    guard_bit = guards & -guards
                    successor = (state ^ guard_bit) | target_bit
                    if successor in active:
                        legal = True
                        break
                    guards ^= guard_bit
                if not legal:
                    rejected.add(state)
                    break
        if not rejected:
            return frozenset(active)
        active.difference_update(rejected)


@functools.cache
def eternal_number(graph: Graph) -> int:
    for size in range(domination_number(graph), len(graph) + 1):
        if greatest_eternal_family(graph, size):
            return size
    raise AssertionError("all-occupied configuration must survive")


def exact_parameters(graph: Graph) -> dict[str, int]:
    return {
        "gamma": domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": eternal_number(graph),
        "theta": clique_cover_number(graph),
    }


def adjacent_true_twin_pairs(graph: Graph) -> tuple[tuple[int, int], ...]:
    return tuple(
        (u, v)
        for u in range(len(graph))
        for v in range(u + 1, len(graph))
        if graph[u] & (1 << v)
        and (graph[u] | (1 << u)) == (graph[v] | (1 << v))
    )


def delete_vertex(graph: Graph, deleted: int) -> tuple[Graph, dict[int, int]]:
    old_vertices = [v for v in range(len(graph)) if v != deleted]
    relabel = {old: new for new, old in enumerate(old_vertices)}
    rows: list[int] = []
    for old in old_vertices:
        row = 0
        for neighbor in old_vertices:
            if graph[old] & (1 << neighbor):
                row |= 1 << relabel[neighbor]
        rows.append(row)
    return tuple(rows), relabel


def relabel_state(state: int, relabel: dict[int, int]) -> int:
    answer = 0
    for old, new in relabel.items():
        if state & (1 << old):
            answer |= 1 << new
    return answer


def audit_eternal_family(graph: Graph, family: frozenset[int]) -> dict[str, int | bool]:
    if not family:
        raise AssertionError("eternal family is empty")
    obligations = 0
    for state in family:
        if not dominates(graph, state):
            raise AssertionError("family contains a nondominating state")
        for target in range(len(graph)):
            target_bit = 1 << target
            if state & target_bit:
                continue
            obligations += 1
            guards = state & graph[target]
            if not any(
                ((state ^ guard_bit) | target_bit) in family
                for guard_bit in (
                    1 << guard
                    for guard in range(len(graph))
                    if guards & (1 << guard)
                )
            ):
                raise AssertionError("missing one-guard response")
    return {
        "nonempty": True,
        "states": len(family),
        "unoccupied_attack_obligations": obligations,
        "valid": True,
    }


def inspect_pair(
    graph6: str,
    graph: Graph,
    u: int,
    v: int,
) -> tuple[dict[str, object], list[str]]:
    failures: list[str] = []
    quotient, relabel = delete_vertex(graph, v)
    p_graph = exact_parameters(graph)
    p_quotient = exact_parameters(quotient)
    for parameter in ("gamma", "alpha", "theta"):
        if p_graph[parameter] != p_quotient[parameter]:
            failures.append(f"static {parameter} changed")

    record: dict[str, object] = {
        "graph6": graph6,
        "pair": [u, v],
        "graph_parameters": p_graph,
        "deleted_parameters": p_quotient,
        "equality_hypothesis": p_graph["gamma"] == p_graph["gamma_infinity"],
    }
    if not record["equality_hypothesis"]:
        return record, failures

    k = p_graph["gamma"]
    if not (
        p_quotient["gamma"]
        == p_quotient["alpha"]
        == p_quotient["gamma_infinity"]
        == k
        and p_quotient["theta"] == p_graph["theta"]
    ):
        failures.append("Theorem 3 parameter conclusion failed")

    greatest = greatest_eternal_family(graph, k)
    avoiding_v_old = frozenset(
        state for state in greatest if not state & (1 << v)
    )
    restricted = frozenset(
        relabel_state(state, relabel) for state in avoiding_v_old
    )
    if not restricted:
        failures.append("restricted family is empty")
        restriction_audit: dict[str, int | bool] = {
            "nonempty": False,
            "states": 0,
            "unoccupied_attack_obligations": 0,
            "valid": False,
        }
    else:
        try:
            restriction_audit = audit_eternal_family(quotient, restricted)
        except AssertionError as error:
            failures.append(f"restricted family audit failed: {error}")
            restriction_audit = {
                "nonempty": True,
                "states": len(restricted),
                "unoccupied_attack_obligations": 0,
                "valid": False,
            }

    independent_k_states = frozenset(
        state
        for state in masks_of_size(len(graph), k)
        if independent(graph, state)
    )
    missing_independent_states = independent_k_states - greatest
    if missing_independent_states:
        failures.append("Lemma 2 failed in the greatest family")

    record.update(
        {
            "greatest_family_states": len(greatest),
            "greatest_states_containing_both_twins": sum(
                bool(state & (1 << u)) and bool(state & (1 << v))
                for state in greatest
            ),
            "restricted_family_audit": restriction_audit,
            "independent_k_states": len(independent_k_states),
            "independent_k_states_missing_from_greatest": len(
                missing_independent_states
            ),
        }
    )
    return record, failures


def run(max_order: int, max_seconds: float) -> dict[str, object]:
    started = time.monotonic()
    deadline = started + max_seconds
    order_records: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    first_equality_pair: dict[str, object] | None = None
    first_both_twins_state: dict[str, object] | None = None
    k2_record: dict[str, object] | None = None

    for order in range(1, max_order + 1):
        stream_hash = hashlib.sha256()
        connected = 0
        graphs_with_twins = 0
        pair_count = 0
        equality_pair_count = 0
        with subprocess.Popen(
            (str(GENG), "-cq", str(order)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            if process.stdout is None or process.stderr is None:
                raise AssertionError("failed to capture geng")
            for raw in process.stdout:
                if time.monotonic() > deadline:
                    process.terminate()
                    raise TimeoutError("bounded falsifier exceeded time budget")
                graph6 = raw.strip()
                if not graph6:
                    continue
                connected += 1
                stream_hash.update(graph6.encode("ascii") + b"\n")
                graph = decode_graph6(graph6)
                pairs = adjacent_true_twin_pairs(graph)
                if not pairs:
                    continue
                graphs_with_twins += 1
                pair_count += len(pairs)
                for u, v in pairs:
                    record, pair_failures = inspect_pair(graph6, graph, u, v)
                    if record["equality_hypothesis"]:
                        equality_pair_count += 1
                        if first_equality_pair is None:
                            first_equality_pair = record
                        if (
                            first_both_twins_state is None
                            and record["greatest_states_containing_both_twins"]
                        ):
                            first_both_twins_state = record
                    if order == 2:
                        k2_record = record
                    if pair_failures:
                        failures.append(
                            {
                                "record": record,
                                "failures": pair_failures,
                            }
                        )
            stderr = process.stderr.read()
            return_code = process.wait()
        if return_code or stderr:
            raise RuntimeError(
                f"geng failed at order {order}: "
                f"return={return_code}, stderr={stderr!r}"
            )
        if connected != EXPECTED_CONNECTED[order]:
            raise AssertionError(
                f"coverage mismatch at order {order}: "
                f"{connected} != {EXPECTED_CONNECTED[order]}"
            )
        order_records.append(
            {
                "order": order,
                "connected_graphs": connected,
                "graph6_stream_sha256": stream_hash.hexdigest(),
                "graphs_with_adjacent_true_twins": graphs_with_twins,
                "adjacent_true_twin_pairs": pair_count,
                "equality_hypothesis_pairs": equality_pair_count,
            }
        )

    return {
        "schema": "adjacent-true-twin-clean-room-falsifier-v1",
        "status": "COMPLETE",
        "verdict": "NO_COUNTERMODEL_IN_BOUNDED_SCAN" if not failures else "COUNTERMODEL",
        "scope": {
            "connected_unlabeled_orders": [1, max_order],
            "max_seconds": max_seconds,
            "elapsed_seconds": time.monotonic() - started,
            "broad_order9_plus_enumeration": False,
        },
        "orders": order_records,
        "totals": {
            key: sum(int(row[key]) for row in order_records)
            for key in (
                "connected_graphs",
                "graphs_with_adjacent_true_twins",
                "adjacent_true_twin_pairs",
                "equality_hypothesis_pairs",
            )
        },
        "failures": failures,
        "edge_cases": {
            "K2": k2_record,
            "first_equality_pair": first_equality_pair,
            "first_greatest_family_with_both_twins_occupied": (
                first_both_twins_state
            ),
        },
        "checks_per_pair": [
            "gamma, alpha, and theta are unchanged by deleting the second twin",
            "under gamma=gamma-infinity, all Theorem 3 parameters match",
            "the greatest k-family restricted to states avoiding the deleted twin is nonempty",
            "every restricted state dominates the induced deletion graph",
            "every unoccupied attack has a one-guard response along an induced-graph edge",
            "every independent k-state occurs in the greatest k-family",
            "states containing both twins are counted rather than silently excluded from the source family",
        ],
        "implementation": {
            "target": str(TARGET.relative_to(CAMPAIGN)),
            "target_sha256": file_sha256(TARGET),
            "graph_representation": "ordinary integer adjacency masks",
            "eternal_algorithm": "literal greatest-fixed-point deletion",
            "static_algorithms": "exhaustive subsets and clique-partition recursion",
            "campaign_core_imported": False,
            "geng": str(GENG.relative_to(CAMPAIGN)),
            "geng_sha256": file_sha256(GENG),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=8)
    parser.add_argument("--max-seconds", type=float, default=180.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("result.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.max_order <= 8:
        raise SystemExit("--max-order must lie in 1..8")
    result = run(args.max_order, args.max_seconds)
    result["implementation"]["falsifier_sha256_before_result_write"] = (
        file_sha256(Path(__file__).resolve())
    )
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verdict": result["verdict"],
                "elapsed_seconds": result["scope"]["elapsed_seconds"],
                "totals": result["totals"],
                "failures": len(result["failures"]),
                "output_sha256": file_sha256(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
