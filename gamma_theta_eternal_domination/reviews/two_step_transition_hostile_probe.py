#!/usr/bin/env python3
"""Independent replay of the two-step transition-kernel measurements.

No campaign Python module is imported.  Graphs and guard configurations use
frozensets, and all predicates below are reconstructed from the definitions.
"""

from __future__ import annotations

from collections import Counter
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "results/edge_toggles_unique.csv"
GENG = ROOT / "tools/nauty2_9_3/geng"
MEASUREMENT = ROOT / "results/two_step_obstruction_measurement.json"

EXPECTED_LEDGER_SHA = (
    "a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319"
)
EXPECTED_GENG_SHA = (
    "588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1"
)
EXPECTED_MEASUREMENT_SHA = (
    "8cbbe566c10a390593ec56afa2d2a454804540083264835f9738fbe86081f591"
)
EXPECTED_EDGE = {
    "population": 8_587,
    "one_step_rejected": 4_169,
    "two_step_rejected": 8_061,
    "strict_two_step_additional": 3_892,
    "survives_two_step": 526,
}
EXPECTED_SMALL = {
    5: (21, 0, 0, 0, 0, 0, 0),
    6: (112, 0, 0, 0, 0, 0, 0),
    7: (853, 5, 0, 2, 5, 3, 0),
    8: (11_117, 78, 0, 51, 78, 27, 0),
    9: (261_080, 1_569, 0, 1_134, 1_569, 435, 0),
}


class ProbeError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeError(message)


def file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_graph6(record: str) -> tuple[frozenset[int], ...]:
    try:
        raw = record.strip().encode("ascii")
    except UnicodeEncodeError as error:
        raise ProbeError("non-ASCII graph6") from error
    require(raw and raw[0] != 126 and 63 <= raw[0] <= 125, "graph6 order")
    order = raw[0] - 63
    require(order <= 12, "graph6 order too large")
    edge_bits = order * (order - 1) // 2
    payload_length = (edge_bits + 5) // 6
    require(len(raw) == 1 + payload_length, "graph6 payload length")
    require(all(63 <= byte <= 126 for byte in raw[1:]), "graph6 payload")
    padding = payload_length * 6 - edge_bits
    if padding:
        require(
            ((raw[-1] - 63) & ((1 << padding) - 1)) == 0,
            "graph6 nonzero padding",
        )
    rows = [set() for _ in range(order)]
    position = 0
    for second in range(1, order):
        for first in range(second):
            value = raw[1 + position // 6] - 63
            if value >> (5 - position % 6) & 1:
                rows[first].add(second)
                rows[second].add(first)
            position += 1
    return tuple(frozenset(row) for row in rows)


def independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(not (graph[vertex] & state) for vertex in state)


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def independent_triples(
    graph: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    return tuple(
        state
        for values in combinations(range(len(graph)), 3)
        if independent(graph, state := frozenset(values))
    )


def alpha_is_three(
    graph: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...] | None:
    triples = independent_triples(graph)
    if not triples:
        return None
    if any(
        independent(graph, frozenset(values))
        for values in combinations(range(len(graph)), 4)
    ):
        return None
    return triples


def gamma_is_three(graph: tuple[frozenset[int], ...]) -> bool:
    vertices = range(len(graph))
    if any(
        dominates(graph, frozenset(values))
        for size in (1, 2)
        for values in combinations(vertices, size)
    ):
        return False
    return any(
        dominates(graph, frozenset(values))
        for values in combinations(vertices, 3)
    )


def clique_partition_at_most_three(
    graph: tuple[frozenset[int], ...],
) -> bool:
    """Backtrack over three unlabeled clique parts of G."""

    order = tuple(
        sorted(
            range(len(graph)),
            key=lambda vertex: (len(graph) - 1 - len(graph[vertex]), vertex),
            reverse=True,
        )
    )
    failed: set[tuple[int, tuple[frozenset[int], ...]]] = set()

    def visit(index: int, parts: tuple[frozenset[int], ...]) -> bool:
        if index == len(order):
            return True
        normalized = tuple(sorted(parts, key=lambda part: tuple(sorted(part))))
        key = (index, normalized)
        if key in failed:
            return False
        vertex = order[index]
        tried_empty = False
        for part_index, part in enumerate(parts):
            if not part:
                if tried_empty:
                    continue
                tried_empty = True
            if not part <= graph[vertex]:
                continue
            replacement = list(parts)
            replacement[part_index] = part | {vertex}
            if visit(index + 1, tuple(replacement)):
                return True
        failed.add(key)
        return False

    return visit(0, (frozenset(), frozenset(), frozenset()))


def responses(
    graph: tuple[frozenset[int], ...],
    state: frozenset[int],
    attacked: int,
) -> tuple[frozenset[int], ...]:
    require(attacked not in state, "response requested for occupied attack")
    result = []
    for guard in sorted(state & graph[attacked]):
        successor = frozenset((state - {guard}) | {attacked})
        require(len(successor) == len(state), "not exactly one guard")
        if dominates(graph, successor):
            result.append(successor)
    return tuple(result)


def secure(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    require(dominates(graph, state), "security called on nondominating state")
    return all(
        responses(graph, state, attacked)
        for attacked in range(len(graph))
        if attacked not in state
    )


def one_and_two_step_reject(
    graph: tuple[frozenset[int], ...],
    maximum_states: tuple[frozenset[int], ...],
) -> tuple[bool, bool]:
    one_step = False
    two_step = False
    for state in maximum_states:
        require(dominates(graph, state), "maximum independent set not dominating")
        for attacked in range(len(graph)):
            if attacked in state:
                continue
            first_successors = responses(graph, state, attacked)
            if not first_successors:
                one_step = True
                two_step = True
                continue
            if not any(secure(graph, successor) for successor in first_successors):
                two_step = True
    require(not one_step or two_step, "depth-two did not subsume depth-one")
    return one_step, two_step


def eternal_at_three(graph: tuple[frozenset[int], ...]) -> bool:
    active = {
        frozenset(values)
        for values in combinations(range(len(graph)), 3)
        if dominates(graph, frozenset(values))
    }
    while active:
        doomed = set()
        frozen = frozenset(active)
        for state in frozen:
            for attacked in range(len(graph)):
                if attacked in state:
                    continue
                if not any(
                    successor in frozen
                    for successor in responses(graph, state, attacked)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return True
        active.difference_update(doomed)
    return False


def edge_toggle_measurement() -> dict[str, int]:
    counts: Counter[str] = Counter()
    seen: set[str] = set()
    with LEDGER.open(newline="", encoding="ascii") as handle:
        reader = csv.DictReader(handle, strict=True)
        required = (
            "canonical_graph6",
            "gamma_a",
            "gamma_b",
            "alpha_a",
            "alpha_b",
            "gamma_infinity_a",
            "gamma_infinity_b",
            "theta_a",
            "theta_b",
        )
        require(
            reader.fieldnames is not None
            and all(name in reader.fieldnames for name in required),
            "edge-toggle CSV schema",
        )
        for row in reader:
            graph6 = row["canonical_graph6"]
            require(graph6 not in seen, "duplicate edge-toggle key")
            seen.add(graph6)
            stored = tuple(int(row[name]) for name in required[1:])
            if stored != (3, 3, 3, 3, 4, 4, 4, 4):
                continue
            graph = parse_graph6(graph6)
            maximum_states = alpha_is_three(graph)
            require(maximum_states is not None, "selected edge graph alpha != 3")
            require(gamma_is_three(graph), "selected edge graph gamma != 3")
            require(
                not clique_partition_at_most_three(graph),
                "selected edge graph theta <= 3",
            )
            one_step, two_step = one_and_two_step_reject(
                graph, maximum_states
            )
            counts["population"] += 1
            counts["one_step_rejected"] += one_step
            counts["two_step_rejected"] += two_step
            counts["strict_two_step_additional"] += two_step and not one_step
            counts["survives_two_step"] += not two_step
    require(len(seen) == 19_136, "edge-toggle unique universe")
    return {key: counts[key] for key in EXPECTED_EDGE}


def small_order_measurement(order: int) -> tuple[int, ...]:
    command = (str(GENG), "-qc", str(order))
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    assert process.stdout is not None
    assert process.stderr is not None
    counts: Counter[str] = Counter()
    for line in process.stdout:
        graph = parse_graph6(line)
        require(len(graph) == order, "geng order")
        counts["graphs"] += 1
        maximum_states = alpha_is_three(graph)
        if maximum_states is None or not gamma_is_three(graph):
            continue
        if clique_partition_at_most_three(graph):
            continue
        counts["targets"] += 1
        one_step, two_step = one_and_two_step_reject(graph, maximum_states)
        eternal = eternal_at_three(graph)
        require(not (eternal and two_step), "false two-step rejection")
        counts["eternal"] += eternal
        counts["one"] += one_step
        counts["two"] += two_step
        counts["strict"] += two_step and not one_step
        counts["survive"] += not two_step
    stderr = process.stderr.read()
    return_code = process.wait()
    require(return_code == 0, f"geng failed: {stderr}")
    return (
        counts["graphs"],
        counts["targets"],
        counts["eternal"],
        counts["one"],
        counts["two"],
        counts["strict"],
        counts["survive"],
    )


def c7_kernel_check() -> dict[str, object]:
    graph = tuple(
        frozenset({(vertex - 1) % 7, (vertex + 1) % 7})
        for vertex in range(7)
    )
    maximum_states = alpha_is_three(graph)
    require(maximum_states is not None and len(maximum_states) == 7, "C7 alpha")
    require(all(secure(graph, state) for state in maximum_states), "C7 K1")
    state = frozenset({0, 2, 4})
    first = responses(graph, state, 1)
    require(first == (frozenset({0, 1, 4}),), "C7 first responses")
    require(not secure(graph, first[0]), "C7 successor unexpectedly secure")
    require(
        not responses(graph, first[0], 3),
        "C7 second attack unexpectedly defendable",
    )
    return {
        "maximum_independent_triples": len(maximum_states),
        "all_maximum_states_secure": True,
        "specified_state_in_k2": False,
    }


def main() -> None:
    started = time.monotonic()
    require(file_sha(LEDGER) == EXPECTED_LEDGER_SHA, "ledger hash")
    require(file_sha(GENG) == EXPECTED_GENG_SHA, "geng hash")
    require(file_sha(MEASUREMENT) == EXPECTED_MEASUREMENT_SHA, "measurement hash")
    recorded = json.loads(MEASUREMENT.read_text(encoding="utf-8"))

    c7 = c7_kernel_check()
    edge = edge_toggle_measurement()
    require(edge == EXPECTED_EDGE, "edge-toggle count mismatch")
    small = {
        order: small_order_measurement(order)
        for order in sorted(EXPECTED_SMALL)
    }
    require(small == EXPECTED_SMALL, "small-order count mismatch")

    recorded_edge = dict(recorded["edge_toggle_population"])
    recorded_edge.pop("predicate")
    require(recorded_edge == edge, "recorded edge counts differ")
    recorded_small = {
        item["order"]: (
            item["connected_unlabeled_graphs"],
            item["static_gamma_alpha_3_theta_gt_3"],
            item["eternal_three"],
            item["one_step_rejected"],
            item["two_step_rejected"],
            item["strict_two_step_additional"],
            item["survives_two_step"],
        )
        for item in recorded["small_connected_unlabeled"]["orders"]
    }
    require(recorded_small == small, "recorded small counts differ")

    print(
        json.dumps(
            {
                "status": "accepted as independently reproduced observations",
                "c7": c7,
                "edge_toggle": edge,
                "small_orders": {str(key): value for key, value in small.items()},
                "wall_seconds": time.monotonic() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
