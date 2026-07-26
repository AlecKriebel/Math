#!/usr/bin/env python3
"""Independent hostile replay of the recursive K3 certificate lane.

This program deliberately imports no campaign Python module.  Graphs are
represented by tuples of frozenset neighborhoods and configurations by
frozensets, unlike the author's bit-row/bit-mask implementation.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTHOR_SOURCE = ROOT / "src/search/three_step_kernel.py"
AUTHOR_TESTS = ROOT / "tests/test_three_step_kernel.py"
MEASUREMENT = ROOT / "results/three_step_kernel_measurement.json"
RECURSIVE_CERTIFICATES = (
    ROOT / "certificates/k3_three_step_edge_toggle.ndjson"
)
C15_CERTIFICATE = ROOT / "certificates/c15_k2_not_k3.json"
LEMMA = ROOT / "math/lemmas/three_step_forced_obstruction.md"
LEDGER = ROOT / "results/edge_toggles_unique.csv"
THIRD_TRACE = (
    ROOT / "results/edge_toggle_third_evaluation_certificates.ndjson"
)

EXPECTED_HASHES = {
    "author_source": (
        "e65102358dbfb5a7ab4e5cfe55907e6c583def32c95ed10e50efa49c5271b6fd"
    ),
    "author_tests": (
        "76044cc09946098abd00467a5efc2f19c802836bea3511cd51587d798476205a"
    ),
    "measurement": (
        "1369c38a696b9d1d1c5c4c0aefdf823ae0bda143c25c30ebe7335ab263b41c12"
    ),
    "recursive_certificates": (
        "74d20dd736cf8b962b79e235b1fff77df1f065df8d698913c4811d1cd18b349b"
    ),
    "c15_certificate": (
        "e89df4aaf127f8f3069c40d6a7dc56830cb36c16fd0417e52a9e48162fdfba41"
    ),
    "lemma": (
        "a0fa3a28269a30a4cf8930d3c72ccb83b8d04890fa8695d45d56de59cec14fed"
    ),
    "ledger": (
        "a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319"
    ),
    "third_trace": (
        "b31eee468a8a45e0534fece7b54cb142ff126fb1f9155db5bbea98acaa948435"
    ),
}

EXPECTED_EARLIEST = {3: 518, 5: 7, 6: 1}
EXPECTED_LATEST = {3: 225, 4: 291, 5: 2, 6: 7, 7: 1}
EXPECTED_FORCED = {3: 5283, 4: 1012, 5: 19, 6: 55, 7: 6}
EXPECTED_FULL = {3: 185, 4: 331, 5: 2, 6: 7, 7: 1}
EXPECTED_JOINT = {
    (3, 3, 3): 185,
    (3, 3, 4): 40,
    (3, 4, 4): 291,
    (3, 5, 5): 2,
    (5, 6, 6): 7,
    (6, 7, 7): 1,
}
EXPECTED_ALL_TARGET_EARLIEST = {1: 4169, 2: 3892, 3: 518, 5: 7, 6: 1}
EXPECTED_DEEP = {
    79: ("J@l|bfNuVK_", 5, 6, 6),
    14025: ("K]?H[|]nj}\\k", 5, 6, 6),
    17003: ("KoDbMyz}@}ju", 5, 6, 6),
    17228: ("KoYu~_VMyzLf", 5, 6, 6),
    17453: ("Kp]e~_VDyZlf", 5, 6, 6),
    17957: ("Krqb}iw[W^`~", 5, 6, 6),
    17966: ("KrrDthx\\_^`~", 5, 6, 6),
    18404: ("Kun_w{vRrblV", 6, 7, 7),
}


Graph = tuple[frozenset[int], ...]
State = frozenset[int]


class ProbeFailure(RuntimeError):
    """Raised when any claimed property fails hostile replay."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeFailure(message)


def file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(text: str) -> object:
    try:
        return json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ProbeFailure(f"non-finite JSON value {value}")
            ),
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise ProbeFailure(f"invalid JSON: {error}") from error


def exact_keys(value: object, keys: Iterable[str], label: str) -> dict[str, object]:
    require(type(value) is dict, f"{label} is not an object")
    assert isinstance(value, dict)
    require(set(value) == set(keys), f"{label} fields differ")
    return value


def parse_graph6(record: object) -> Graph:
    require(type(record) is str, "graph6 is not text")
    assert isinstance(record, str)
    try:
        raw = record.encode("ascii")
    except UnicodeEncodeError as error:
        raise ProbeFailure("graph6 is not ASCII") from error
    header = b">>graph6<<"
    if raw.startswith(header):
        raw = raw[len(header) :]
    require(raw and raw[0] != 126 and 63 <= raw[0] <= 125, "graph6 order")
    order = raw[0] - 63
    edge_bits = order * (order - 1) // 2
    payload_length = (edge_bits + 5) // 6
    require(len(raw) == payload_length + 1, "graph6 payload length")
    require(all(63 <= byte <= 126 for byte in raw[1:]), "graph6 payload byte")
    padding = payload_length * 6 - edge_bits
    if padding:
        require(
            ((raw[-1] - 63) & ((1 << padding) - 1)) == 0,
            "graph6 nonzero padding",
        )
    neighborhoods = [set() for _ in range(order)]
    position = 0
    for high in range(1, order):
        for low in range(high):
            value = raw[1 + position // 6] - 63
            if value & (1 << (5 - position % 6)):
                neighborhoods[low].add(high)
                neighborhoods[high].add(low)
            position += 1
    return tuple(frozenset(row) for row in neighborhoods)


def graph_size(graph: Graph) -> int:
    return sum(map(len, graph)) // 2


def connected(graph: Graph) -> bool:
    if not graph:
        return False
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == len(graph)


def state_from_mask(value: object, order: int, cardinality: int) -> State:
    require(type(value) is int, "configuration is not an integer")
    assert isinstance(value, int)
    require(0 <= value < (1 << order), "configuration is out of range")
    state = frozenset(vertex for vertex in range(order) if value >> vertex & 1)
    require(len(state) == cardinality, "configuration cardinality differs")
    return state


def dominates(graph: Graph, state: State) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def independent(graph: Graph, state: State) -> bool:
    return all(not (graph[vertex] & state) for vertex in state)


def independent_states(graph: Graph, cardinality: int) -> tuple[State, ...]:
    return tuple(
        state
        for values in combinations(range(len(graph)), cardinality)
        if independent(graph, state := frozenset(values))
    )


def alpha_equals(graph: Graph, cardinality: int) -> tuple[State, ...]:
    states = independent_states(graph, cardinality)
    require(states, f"alpha is less than {cardinality}")
    if cardinality < len(graph):
        require(
            not independent_states(graph, cardinality + 1),
            f"alpha exceeds {cardinality}",
        )
    return states


def dominating_states(graph: Graph, cardinality: int) -> frozenset[State]:
    return frozenset(
        state
        for values in combinations(range(len(graph)), cardinality)
        if dominates(graph, state := frozenset(values))
    )


def predecessor(
    graph: Graph,
    configurations: frozenset[State],
    active: frozenset[State],
) -> frozenset[State]:
    survivors: set[State] = set()
    vertices = range(len(graph))
    for state in configurations:
        survives = True
        for attacked in vertices:
            if attacked in state:
                continue
            response_exists = False
            for guard in state & graph[attacked]:
                child = frozenset((state - {guard}) | {attacked})
                if child in active:
                    response_exists = True
                    break
            if not response_exists:
                survives = False
                break
        if survives:
            survivors.add(state)
    return frozenset(survivors)


def kernel_profile(
    graph: Graph, cardinality: int
) -> tuple[tuple[frozenset[State], ...], dict[State, int], bool]:
    configurations = dominating_states(graph, cardinality)
    levels = [configurations]
    ranks: dict[State, int] = {}
    active = configurations
    while active:
        following = predecessor(graph, configurations, active)
        rank = len(levels)
        for state in active - following:
            ranks[state] = rank
        levels.append(following)
        if following == active:
            return tuple(levels), ranks, True
        active = following
    return tuple(levels), ranks, False


def gamma_equals_three(graph: Graph, configurations: frozenset[State]) -> bool:
    if not configurations:
        return False
    return not any(
        dominates(graph, frozenset(values))
        for size in (1, 2)
        for values in combinations(range(len(graph)), size)
    )


def clique_partition_at_most(graph: Graph, part_count: int) -> bool:
    """Fresh exact backtracker for a partition of V(G) into <= part_count cliques."""

    order = tuple(
        sorted(
            range(len(graph)),
            key=lambda vertex: (len(graph) - 1 - len(graph[vertex]), vertex),
            reverse=True,
        )
    )
    failed: set[tuple[int, tuple[State, ...]]] = set()

    def visit(index: int, parts: tuple[State, ...]) -> bool:
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

    return visit(0, tuple(frozenset() for _ in range(part_count)))


def undominated(graph: Graph, state: State, witness: object) -> bool:
    return (
        type(witness) is int
        and 0 <= witness < len(graph)
        and witness not in state
        and not bool(graph[witness] & state)
    )


def verify_failure_node(
    graph: Graph,
    guard_count: int,
    value: object,
    expected_state: State,
    expected_horizon: int,
) -> tuple[int, int]:
    node = exact_keys(
        value,
        (
            ("kind", "configuration", "horizon", "undominated")
            if isinstance(value, dict) and value.get("kind") == "nondominating"
            else ("kind", "configuration", "horizon", "attack", "branches")
        ),
        "failure node",
    )
    require(node.get("kind") in {"nondominating", "attack"}, "failure kind")
    state = state_from_mask(node["configuration"], len(graph), guard_count)
    require(state == expected_state, "failure child configuration differs")
    require(
        type(node["horizon"]) is int
        and node["horizon"] == expected_horizon
        and expected_horizon >= 0,
        "failure horizon differs",
    )
    if node["kind"] == "nondominating":
        require(
            undominated(graph, state, node["undominated"]),
            "false undominated witness",
        )
        require(not dominates(graph, state), "terminal state dominates")
        return 1, 1

    require(expected_horizon >= 1, "attack node at horizon zero")
    require(dominates(graph, state), "attack node is nondominating")
    attacked = node["attack"]
    require(type(attacked) is int, "attack is not an integer")
    assert isinstance(attacked, int)
    require(0 <= attacked < len(graph), "attack is out of range")
    require(attacked not in state, "attack is occupied")
    branches = node["branches"]
    require(type(branches) is list, "branches is not an array")
    expected_guards = state & graph[attacked]
    records: dict[int, object] = {}
    for item in branches:
        branch = exact_keys(item, ("guard", "child"), "failure branch")
        guard = branch["guard"]
        require(type(guard) is int, "guard is not an integer")
        assert isinstance(guard, int)
        require(guard not in records, "duplicate response guard")
        records[guard] = branch["child"]
    require(set(records) == set(expected_guards), "response branches incomplete")
    nodes = 1
    leaves = 0
    for guard, child_value in records.items():
        child = frozenset((state - {guard}) | {attacked})
        child_nodes, child_leaves = verify_failure_node(
            graph,
            guard_count,
            child_value,
            child,
            expected_horizon - 1,
        )
        nodes += child_nodes
        leaves += child_leaves
    return nodes, leaves


def verify_forced_failure(
    graph: Graph, value: object, expected_horizon: int | None = None
) -> tuple[State, int, int]:
    certificate = exact_keys(
        value,
        ("guard_count", "horizon", "independent_state", "root"),
        "forced-failure certificate",
    )
    guard_count = certificate["guard_count"]
    horizon = certificate["horizon"]
    require(
        type(guard_count) is int and 0 <= guard_count <= len(graph),
        "guard count differs",
    )
    require(type(horizon) is int and horizon >= 1, "forced horizon invalid")
    assert isinstance(guard_count, int)
    assert isinstance(horizon, int)
    if expected_horizon is not None:
        require(horizon == expected_horizon, "forced horizon differs")
    state = state_from_mask(
        certificate["independent_state"], len(graph), guard_count
    )
    maxima = alpha_equals(graph, guard_count)
    require(state in maxima, "root is not maximum independent")
    nodes, leaves = verify_failure_node(
        graph, guard_count, certificate["root"], state, horizon
    )
    return state, nodes, leaves


def verify_survival_node(
    graph: Graph,
    guard_count: int,
    value: object,
    expected_state: State,
    expected_horizon: int,
) -> tuple[int, int]:
    node = exact_keys(
        value, ("configuration", "horizon", "responses"), "survival node"
    )
    state = state_from_mask(node["configuration"], len(graph), guard_count)
    require(state == expected_state, "survival child configuration differs")
    require(
        type(node["horizon"]) is int
        and node["horizon"] == expected_horizon
        and expected_horizon >= 0,
        "survival horizon differs",
    )
    require(dominates(graph, state), "survival state is nondominating")
    responses = node["responses"]
    require(type(responses) is list, "survival responses is not an array")
    if expected_horizon == 0:
        require(not responses, "horizon-zero survival has responses")
        return 1, 1
    expected_attacks = set(range(len(graph))) - set(state)
    records: dict[int, dict[str, object]] = {}
    for item in responses:
        response = exact_keys(
            item, ("attack", "guard", "child"), "survival response"
        )
        attacked = response["attack"]
        require(type(attacked) is int, "survival attack is not an integer")
        assert isinstance(attacked, int)
        require(attacked not in records, "duplicate survival attack")
        records[attacked] = response
    require(set(records) == expected_attacks, "survival attacks incomplete")
    nodes = 1
    leaves = 0
    for attacked, response in records.items():
        guard = response["guard"]
        require(type(guard) is int, "survival guard is not an integer")
        assert isinstance(guard, int)
        require(guard in state, "survival guard is unoccupied")
        require(guard in graph[attacked], "survival guard is nonadjacent")
        child = frozenset((state - {guard}) | {attacked})
        child_nodes, child_leaves = verify_survival_node(
            graph,
            guard_count,
            response["child"],
            child,
            expected_horizon - 1,
        )
        nodes += child_nodes
        leaves += child_leaves
    return nodes, leaves


def first_node(value: dict[str, object], kind: str) -> dict[str, object] | None:
    if value.get("kind") == kind:
        return value
    branches = value.get("branches")
    if type(branches) is list:
        for branch in branches:
            if type(branch) is dict and type(branch.get("child")) is dict:
                found = first_node(branch["child"], kind)
                if found is not None:
                    return found
    return None


def expect_rejected(operation, label: str) -> None:
    try:
        operation()
    except (ProbeFailure, KeyError, TypeError, ValueError, RecursionError):
        return
    raise ProbeFailure(f"tamper accepted: {label}")


def audit_hashes() -> dict[str, str]:
    paths = {
        "author_source": AUTHOR_SOURCE,
        "author_tests": AUTHOR_TESTS,
        "measurement": MEASUREMENT,
        "recursive_certificates": RECURSIVE_CERTIFICATES,
        "c15_certificate": C15_CERTIFICATE,
        "lemma": LEMMA,
        "ledger": LEDGER,
        "third_trace": THIRD_TRACE,
    }
    actual = {label: file_sha(path) for label, path in paths.items()}
    require(actual == EXPECTED_HASHES, "frozen or input hashes differ")
    return actual


def load_ledger() -> tuple[list[dict[str, str]], list[int]]:
    with LEDGER.open(newline="", encoding="ascii") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None, "ledger has no header")
        assert reader.fieldnames is not None
        require(len(reader.fieldnames) == len(set(reader.fieldnames)), "CSV keys")
        rows = list(reader)
    require(len(rows) == 19_136, "ledger row count differs")
    all_graphs = [row["canonical_graph6"] for row in rows]
    require(len(all_graphs) == len(set(all_graphs)), "ledger graph6 duplicates")
    fields = (
        "gamma_a",
        "gamma_b",
        "alpha_a",
        "alpha_b",
        "gamma_infinity_a",
        "gamma_infinity_b",
        "theta_a",
        "theta_b",
    )
    target = [
        index
        for index, row in enumerate(rows)
        if tuple(int(row[field]) for field in fields)
        == (3, 3, 3, 3, 4, 4, 4, 4)
    ]
    require(len(target) == 8_587, "stored target population differs")
    return rows, target


def replay_population(
    rows: list[dict[str, str]], target: list[int]
) -> tuple[
    dict[str, object],
    dict[int, tuple[str, dict[State, int], int, int]],
]:
    earliest = Counter()
    latest = Counter()
    forced = Counter()
    full = Counter()
    joint = Counter()
    all_earliest = Counter()
    selected: dict[int, tuple[str, dict[State, int], int, int]] = {}
    configurations_checked = 0
    static_parameter_checks = 0

    for row_index in target:
        row = rows[row_index]
        graph = parse_graph6(row["canonical_graph6"])
        require(len(graph) == int(row["n"]), "stored order differs")
        require(graph_size(graph) == int(row["m"]), "stored size differs")
        require(row["connected"] == "1" and connected(graph), "target disconnected")
        maxima = alpha_equals(graph, 3)
        levels, ranks, stable = kernel_profile(graph, 3)
        require(not stable and not levels[-1], "target has eternal triple family")
        require(gamma_equals_three(graph, levels[0]), "target gamma is not three")
        require(
            not clique_partition_at_most(graph, 3)
            and clique_partition_at_most(graph, 4),
            "target theta is not four",
        )
        static_parameter_checks += 1
        maximum_ranks = tuple(ranks[state] for state in maxima)
        first = min(maximum_ranks)
        all_earliest[first] += 1
        if first <= 2:
            continue
        last = max(maximum_ranks)
        depth = len(levels) - 1
        selected[row_index] = (
            row["canonical_graph6"],
            ranks,
            len(levels[0]),
            depth,
        )
        configurations_checked += len(levels[0])
        earliest[first] += 1
        latest[last] += 1
        forced.update(maximum_ranks)
        full[depth] += 1
        joint[(first, last, depth)] += 1

    require(dict(all_earliest) == EXPECTED_ALL_TARGET_EARLIEST, "all ranks differ")
    require(len(selected) == 526, "K2 survivor count differs")
    require(dict(earliest) == EXPECTED_EARLIEST, "earliest distribution differs")
    require(dict(latest) == EXPECTED_LATEST, "latest distribution differs")
    require(dict(forced) == EXPECTED_FORCED, "forced distribution differs")
    require(dict(full) == EXPECTED_FULL, "full-depth distribution differs")
    require(dict(joint) == EXPECTED_JOINT, "joint distribution differs")
    require(configurations_checked == 64_893, "configuration count differs")
    return (
        {
            "stored_target_rows": len(target),
            "static_gamma_alpha_theta_eternal_checks": static_parameter_checks,
            "all_target_earliest_forced_rank": dict(sorted(all_earliest.items())),
            "survives_K2": len(selected),
            "earliest_forced_rank": dict(sorted(earliest.items())),
            "latest_forced_rank": dict(sorted(latest.items())),
            "individual_forced_rank": dict(sorted(forced.items())),
            "full_kernel_empty_depth": dict(sorted(full.items())),
            "joint_earliest_latest_full": {
                ",".join(map(str, key)): joint[key] for key in sorted(joint)
            },
            "selected_dominating_configurations": configurations_checked,
        },
        selected,
    )


def replay_third_trace(
    rows: list[dict[str, str]],
    selected: dict[int, tuple[str, dict[State, int], int, int]],
) -> dict[str, object]:
    selected_seen: set[int] = set()
    row_digest = sha256()
    row_count = 0
    with THIRD_TRACE.open(encoding="ascii") as handle:
        header_line = handle.readline()
        header = exact_keys(
            strict_json(header_line),
            (
                "binding",
                "binding_sha256",
                "expected_rows",
                "format",
                "type",
            ),
            "third-trace header",
        )
        require(header["type"] == "header", "third-trace header type")
        require(header["expected_rows"] == 19_136, "third-trace expected rows")
        footer: dict[str, object] | None = None
        for line in handle:
            value = strict_json(line)
            require(type(value) is dict, "third-trace record is not an object")
            assert isinstance(value, dict)
            if value.get("type") == "footer":
                footer = value
                break
            require(value.get("type") == "row", "third-trace row type")
            require(value.get("row_index") == row_count, "trace row sequence")
            require(
                value.get("graph6") == rows[row_count]["canonical_graph6"],
                "trace graph differs from ledger",
            )
            row_digest.update(line.encode("ascii"))
            if row_count in selected:
                graph6, expected_ranks, initial_count, depth = selected[row_count]
                require(value.get("graph6") == graph6, "selected trace graph")
                require(
                    value.get("initial_dominating_configurations")
                    == initial_count,
                    "selected initial configuration count",
                )
                rounds = value.get("deletion_rounds")
                require(type(rounds) is list and len(rounds) == depth, "round count")
                trace_ranks: dict[State, int] = {}
                graph = parse_graph6(graph6)
                for rank, round_value in enumerate(rounds, 1):
                    require(type(round_value) is list and round_value, "empty round")
                    for record in round_value:
                        require(
                            type(record) is list
                            and len(record) == 2
                            and type(record[0]) is int
                            and type(record[1]) is int,
                            "malformed deletion record",
                        )
                        state = state_from_mask(record[0], len(graph), 3)
                        require(state not in trace_ranks, "duplicate trace state")
                        trace_ranks[state] = rank
                require(trace_ranks == expected_ranks, "trace ranks differ")
                selected_seen.add(row_count)
            row_count += 1
        require(footer is not None, "third-trace footer missing")
        require(not handle.read(), "data follows third-trace footer")
    require(row_count == 19_136, "third-trace row count")
    require(selected_seen == set(selected), "selected trace coverage differs")
    assert footer is not None
    summary = footer.get("summary")
    require(type(summary) is dict, "third-trace summary missing")
    assert isinstance(summary, dict)
    require(summary.get("rows") == row_count, "third-trace summary rows")
    require(
        summary.get("row_stream_sha256") == row_digest.hexdigest(),
        "third-trace row digest differs",
    )
    return {
        "rows": row_count,
        "selected_rows": len(selected_seen),
        "selected_configuration_ranks": sum(
            len(record[1]) for record in selected.values()
        ),
        "row_stream_sha256": row_digest.hexdigest(),
    }


def replay_recursive_certificates(
    rows: list[dict[str, str]],
    selected: dict[int, tuple[str, dict[State, int], int, int]],
) -> tuple[dict[str, object], dict[str, object]]:
    lines = RECURSIVE_CERTIFICATES.read_text(encoding="ascii").splitlines()
    require(len(lines) == 520, "recursive certificate line count")
    header = exact_keys(
        strict_json(lines[0]),
        (
            "type",
            "format",
            "horizon",
            "guard_count",
            "source_sha256",
            "ledger_sha256",
        ),
        "recursive header",
    )
    require(
        header
        == {
            "type": "header",
            "format": "gamma-theta-k3-recursive-failure-certificates-v1",
            "horizon": 3,
            "guard_count": 3,
            "source_sha256": EXPECTED_HASHES["author_source"],
            "ledger_sha256": EXPECTED_HASHES["ledger"],
        },
        "recursive header values",
    )
    seen_indices: set[int] = set()
    seen_graphs: set[str] = set()
    nodes = 0
    leaves = 0
    maximum_nodes = 0
    row_digest = sha256()
    first_payload: dict[str, object] | None = None
    for line in lines[1:-1]:
        value = exact_keys(
            strict_json(line),
            (
                "type",
                "ledger_row_index",
                "graph6",
                "certificate",
                "nodes",
                "leaves",
            ),
            "recursive row",
        )
        require(value["type"] == "row", "recursive row type")
        row_index = value["ledger_row_index"]
        require(type(row_index) is int, "recursive row index type")
        assert isinstance(row_index, int)
        require(row_index in selected, "recursive row is outside K2 survivors")
        require(row_index not in seen_indices, "duplicate recursive row index")
        graph6, ranks, _, _ = selected[row_index]
        require(value["graph6"] == graph6, "recursive graph differs from ledger")
        require(graph6 not in seen_graphs, "duplicate recursive graph")
        graph = parse_graph6(graph6)
        root, counted_nodes, counted_leaves = verify_forced_failure(
            graph, value["certificate"], 3
        )
        require(ranks[root] == 3, "recursive root did not first fail at K3")
        require(
            value["nodes"] == counted_nodes
            and value["leaves"] == counted_leaves,
            "recursive node counts differ",
        )
        seen_indices.add(row_index)
        seen_graphs.add(graph6)
        nodes += counted_nodes
        leaves += counted_leaves
        maximum_nodes = max(maximum_nodes, counted_nodes)
        row_digest.update(line.encode("ascii") + b"\n")
        if first_payload is None:
            first_payload = deepcopy(value)
    trailer = exact_keys(
        strict_json(lines[-1]),
        ("type", "format", "rows", "row_stream_sha256"),
        "recursive trailer",
    )
    require(
        trailer
        == {
            "type": "trailer",
            "format": "gamma-theta-k3-recursive-failure-certificates-v1",
            "rows": 518,
            "row_stream_sha256": row_digest.hexdigest(),
        },
        "recursive trailer values",
    )
    require(len(seen_indices) == 518, "recursive certificate row count")
    require(nodes == 5_540 and leaves == 3_174, "aggregate tree counts")
    require(maximum_nodes == 17, "maximum tree size")
    require(first_payload is not None, "no recursive row available")
    return (
        {
            "rows": len(seen_indices),
            "nodes": nodes,
            "leaves": leaves,
            "maximum_nodes": maximum_nodes,
            "row_stream_sha256": row_digest.hexdigest(),
            "ledger_indices": seen_indices,
        },
        first_payload,
    )


def replay_c15() -> tuple[dict[str, object], dict[str, object]]:
    payload = exact_keys(
        strict_json(C15_CERTIFICATE.read_text(encoding="utf-8")),
        (
            "failure_certificate",
            "failure_horizon",
            "format",
            "graph6",
            "guard_count",
            "independent_state",
            "kernel_sizes_K0_through_K3",
            "maximum_independent_states",
            "order",
            "size",
            "source_sha256",
            "survival_certificate",
            "survival_horizon",
        ),
        "C15 payload",
    )
    require(payload["format"] == "gamma-theta-c15-k2-not-k3-v1", "C15 format")
    require(payload["source_sha256"] == EXPECTED_HASHES["author_source"], "C15 source")
    graph = parse_graph6(payload["graph6"])
    cycle = tuple(
        frozenset({(vertex - 1) % 15, (vertex + 1) % 15})
        for vertex in range(15)
    )
    require(graph == cycle, "C15 graph6 is not the labeled cycle")
    require(len(graph) == payload["order"] == 15, "C15 order")
    require(graph_size(graph) == payload["size"] == 15, "C15 size")
    require(payload["guard_count"] == 7, "C15 guard count")
    state = state_from_mask(payload["independent_state"], 15, 7)
    maxima = alpha_equals(graph, 7)
    require(len(maxima) == payload["maximum_independent_states"] == 15, "C15 alpha")
    rotations = {
        frozenset((vertex + offset) % 15 for vertex in state)
        for offset in range(15)
    }
    require(set(maxima) == rotations, "C15 maxima are not the stated rotations")
    levels, ranks, stable = kernel_profile(graph, 7)
    sizes = [len(level) for level in levels[:4]]
    require(not stable, "C15 unexpectedly has stable seven-family")
    require(sizes == [765, 120, 15, 0], "C15 kernel sizes")
    require(payload["kernel_sizes_K0_through_K3"] == sizes, "C15 stored sizes")
    require(all(candidate in levels[2] for candidate in maxima), "C15 K2")
    require(all(candidate not in levels[3] for candidate in maxima), "C15 K3")
    require(set(ranks[candidate] for candidate in maxima) == {3}, "C15 ranks")
    require(payload["survival_horizon"] == 2, "C15 survival horizon")
    survival_nodes, survival_leaves = verify_survival_node(
        graph, 7, payload["survival_certificate"], state, 2
    )
    require(payload["failure_horizon"] == 3, "C15 failure horizon")
    failure_state, failure_nodes, failure_leaves = verify_forced_failure(
        graph, payload["failure_certificate"], 3
    )
    require(failure_state == state, "C15 certificate roots differ")
    require(
        (survival_nodes, survival_leaves, failure_nodes, failure_leaves)
        == (73, 64, 8, 4),
        "C15 tree counts differ",
    )
    return (
        {
            "kernel_sizes": sizes,
            "maximum_independent_states": len(maxima),
            "all_maximum_states_in_K2_not_K3": True,
            "survival_nodes": survival_nodes,
            "survival_leaves": survival_leaves,
            "failure_nodes": failure_nodes,
            "failure_leaves": failure_leaves,
        },
        payload,
    )


def audit_coverage(
    selected: dict[int, tuple[str, dict[State, int], int, int]],
    recursive: dict[str, object],
    measurement: dict[str, object],
) -> dict[str, object]:
    population = measurement.get("population")
    require(type(population) is dict, "measurement population missing")
    assert isinstance(population, dict)
    deep_rows = population.get("deep_rows")
    require(type(deep_rows) is list and len(deep_rows) == 8, "deep rows")
    deep_indices: set[int] = set()
    for item in deep_rows:
        require(type(item) is dict, "deep row is not an object")
        assert isinstance(item, dict)
        row_index = item.get("ledger_row_index")
        require(type(row_index) is int and row_index in selected, "deep row index")
        assert isinstance(row_index, int)
        require(row_index not in deep_indices, "duplicate deep row")
        expected = EXPECTED_DEEP.get(row_index)
        require(expected is not None, "unexpected deep row")
        graph6, earliest, latest, depth = expected
        require(
            (
                item.get("graph6"),
                item.get("earliest_forced_rank"),
                item.get("latest_forced_rank"),
                item.get("full_deletion_depth"),
            )
            == (graph6, earliest, latest, depth),
            "deep row metadata differs",
        )
        selected_graph, ranks, _, selected_depth = selected[row_index]
        maxima = alpha_equals(parse_graph6(selected_graph), 3)
        require(
            selected_graph == graph6
            and min(ranks[state] for state in maxima) == earliest
            and max(ranks[state] for state in maxima) == latest
            and selected_depth == depth,
            "deep row recomputation differs",
        )
        deep_indices.add(row_index)
    certificate_indices = recursive["ledger_indices"]
    require(type(certificate_indices) is set, "recursive index set")
    assert isinstance(certificate_indices, set)
    require(not (certificate_indices & deep_indices), "coverage sets overlap")
    require(
        certificate_indices | deep_indices == set(selected),
        "518 certificates and eight deep rows do not cover selected population",
    )
    return {
        "certificate_rows": len(certificate_indices),
        "deep_rows": len(deep_indices),
        "disjoint": True,
        "union_equals_all_K2_survivors": True,
    }


def audit_measurement(
    measurement: dict[str, object],
    population_result: dict[str, object],
    recursive_result: dict[str, object],
    c15_result: dict[str, object],
) -> None:
    require(measurement.get("status") == "complete", "measurement status")
    implementation = measurement.get("implementation")
    inputs = measurement.get("inputs")
    recursive = measurement.get("recursive_certificates")
    strictness = measurement.get("strictness_witness")
    population = measurement.get("population")
    cross_check = measurement.get("cross_check")
    for value, label in (
        (implementation, "implementation"),
        (inputs, "inputs"),
        (recursive, "recursive"),
        (strictness, "strictness"),
        (population, "population"),
        (cross_check, "cross check"),
    ):
        require(type(value) is dict, f"measurement {label} missing")
    assert isinstance(implementation, dict)
    assert isinstance(inputs, dict)
    assert isinstance(recursive, dict)
    assert isinstance(strictness, dict)
    assert isinstance(population, dict)
    assert isinstance(cross_check, dict)
    require(
        implementation.get("source_sha256") == EXPECTED_HASHES["author_source"],
        "measurement source binding",
    )
    require(inputs.get("ledger_sha256") == EXPECTED_HASHES["ledger"], "ledger binding")
    require(
        inputs.get("third_certificates_sha256") == EXPECTED_HASHES["third_trace"],
        "third-trace binding",
    )
    require(
        recursive.get("sha256") == EXPECTED_HASHES["recursive_certificates"],
        "recursive artifact binding",
    )
    require(
        strictness.get("sha256") == EXPECTED_HASHES["c15_certificate"],
        "C15 artifact binding",
    )
    require(
        (
            recursive.get("rows"),
            recursive.get("nodes"),
            recursive.get("leaves"),
            recursive.get("maximum_nodes_per_certificate"),
            recursive.get("row_stream_sha256"),
        )
        == (
            recursive_result["rows"],
            recursive_result["nodes"],
            recursive_result["leaves"],
            recursive_result["maximum_nodes"],
            recursive_result["row_stream_sha256"],
        ),
        "recursive measurement summary",
    )
    require(
        (
            strictness.get("survival_nodes"),
            strictness.get("survival_leaves"),
            strictness.get("failure_nodes"),
            strictness.get("failure_leaves"),
        )
        == (
            c15_result["survival_nodes"],
            c15_result["survival_leaves"],
            c15_result["failure_nodes"],
            c15_result["failure_leaves"],
        ),
        "strictness measurement summary",
    )
    require(
        population.get("stored_parameter_target")
        == population_result["stored_target_rows"],
        "stored population count",
    )
    require(
        population.get("survives_K2") == population_result["survives_K2"],
        "K2 survivor count",
    )
    require(population.get("eliminated_at_K3") == 518, "K3 eliminated count")
    require(population.get("survives_K3") == 8, "K3 survivor count")
    require(population.get("survives_K4") == 8, "K4 survivor count")
    expected_maps = {
        "earliest_forced_deletion_rank": EXPECTED_EARLIEST,
        "latest_forced_deletion_rank": EXPECTED_LATEST,
        "individual_forced_triple_deletion_rank": EXPECTED_FORCED,
        "full_kernel_deletion_depth": EXPECTED_FULL,
    }
    for field, expected in expected_maps.items():
        require(
            population.get(field) == {str(key): value for key, value in expected.items()},
            f"measurement {field}",
        )
    require(
        population.get("joint_earliest_latest_full")
        == {",".join(map(str, key)): value for key, value in EXPECTED_JOINT.items()},
        "measurement joint distribution",
    )
    require(
        cross_check.get("passed") is True
        and cross_check.get("rows") == 526
        and cross_check.get("configurations") == 64_893,
        "measurement cross-check summary",
    )


def mutation_suite(
    first_row: dict[str, object], c15_payload: dict[str, object]
) -> dict[str, int]:
    rejected = 0

    def reject_failure(tampered: dict[str, object], label: str) -> None:
        nonlocal rejected
        graph = parse_graph6(tampered["graph6"])
        expect_rejected(
            lambda: verify_forced_failure(graph, tampered["certificate"], 3),
            label,
        )
        rejected += 1

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    certificate["guard_count"] = True
    reject_failure(mutation, "Boolean guard count")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    certificate["independent_state"] = 0
    reject_failure(mutation, "nonmaximum root")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    root = certificate["root"]
    assert isinstance(root, dict)
    root["horizon"] = 2
    reject_failure(mutation, "wrong root horizon")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    root = certificate["root"]
    assert isinstance(root, dict)
    state = state_from_mask(root["configuration"], len(parse_graph6(mutation["graph6"])), 3)
    root["attack"] = min(state)
    reject_failure(mutation, "occupied attack")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    root = certificate["root"]
    assert isinstance(root, dict)
    branches = root["branches"]
    assert isinstance(branches, list)
    branches.pop()
    reject_failure(mutation, "missing response branch")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    root = certificate["root"]
    assert isinstance(root, dict)
    branches = root["branches"]
    assert isinstance(branches, list)
    branches[0]["guard"] = True
    reject_failure(mutation, "Boolean response guard")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    root = certificate["root"]
    assert isinstance(root, dict)
    branches = root["branches"]
    assert isinstance(branches, list)
    child = branches[0]["child"]
    assert isinstance(child, dict)
    child["configuration"] ^= 1
    reject_failure(mutation, "wrong one-guard successor")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    leaf = first_node(certificate["root"], "nondominating")
    assert leaf is not None
    leaf_state = state_from_mask(
        leaf["configuration"], len(parse_graph6(mutation["graph6"])), 3
    )
    leaf["undominated"] = min(leaf_state)
    reject_failure(mutation, "false terminal witness")

    mutation = deepcopy(first_row)
    certificate = mutation["certificate"]
    assert isinstance(certificate, dict)
    certificate["extra"] = 0
    reject_failure(mutation, "extra forced-certificate field")

    duplicate_key = '{"kind":"nondominating","kind":"attack"}'
    expect_rejected(lambda: strict_json(duplicate_key), "duplicate JSON key")
    rejected += 1

    survival = deepcopy(c15_payload["survival_certificate"])
    assert isinstance(survival, dict)
    responses = survival["responses"]
    assert isinstance(responses, list)
    responses.pop()
    c15_graph = parse_graph6(c15_payload["graph6"])
    c15_state = state_from_mask(c15_payload["independent_state"], 15, 7)
    expect_rejected(
        lambda: verify_survival_node(c15_graph, 7, survival, c15_state, 2),
        "missing survival attack",
    )
    rejected += 1

    survival = deepcopy(c15_payload["survival_certificate"])
    assert isinstance(survival, dict)
    responses = survival["responses"]
    assert isinstance(responses, list)
    responses[0]["attack"] = min(c15_state)
    expect_rejected(
        lambda: verify_survival_node(c15_graph, 7, survival, c15_state, 2),
        "occupied survival attack",
    )
    rejected += 1

    survival = deepcopy(c15_payload["survival_certificate"])
    assert isinstance(survival, dict)
    responses = survival["responses"]
    assert isinstance(responses, list)
    responses[0]["guard"] = True
    expect_rejected(
        lambda: verify_survival_node(c15_graph, 7, survival, c15_state, 2),
        "Boolean survival guard",
    )
    rejected += 1

    survival = deepcopy(c15_payload["survival_certificate"])
    assert isinstance(survival, dict)
    responses = survival["responses"]
    assert isinstance(responses, list)
    child = responses[0]["child"]
    assert isinstance(child, dict)
    child["configuration"] ^= 1
    expect_rejected(
        lambda: verify_survival_node(c15_graph, 7, survival, c15_state, 2),
        "wrong survival successor",
    )
    rejected += 1

    return {"decisive_mutations_rejected": rejected}


def main() -> None:
    started = time.perf_counter()
    hashes = audit_hashes()
    rows, target = load_ledger()
    population, selected = replay_population(rows, target)
    trace = replay_third_trace(rows, selected)
    recursive, first_row = replay_recursive_certificates(rows, selected)
    c15, c15_payload = replay_c15()
    measurement = strict_json(MEASUREMENT.read_text(encoding="utf-8"))
    require(type(measurement) is dict, "measurement is not an object")
    assert isinstance(measurement, dict)
    coverage = audit_coverage(selected, recursive, measurement)
    audit_measurement(measurement, population, recursive, c15)
    mutations = mutation_suite(first_row, c15_payload)
    recursive.pop("ledger_indices")
    output = {
        "status": "ACCEPT",
        "implementation_independence": (
            "No campaign Python module imported; frozenset graph/configuration "
            "model and fresh recursive replay/kernel implementation."
        ),
        "hashes": hashes,
        "population": population,
        "third_trace": trace,
        "recursive_certificates": recursive,
        "c15": c15,
        "coverage": coverage,
        "tamper_tests": mutations,
        "wall_seconds": time.perf_counter() - started,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
