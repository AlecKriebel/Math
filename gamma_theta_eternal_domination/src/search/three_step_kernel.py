#!/usr/bin/env python3
"""Recursive online-kernel certificates and the K3 survivor measurement.

This module uses only the Python standard library.  In particular, it imports
neither eternal-domination evaluator nor the earlier two-step search code.
The certificate verifier checks a finite alternating attack/response tree
directly from adjacency, occupancy, and domination.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import platform
import resource
import tempfile
import time
from typing import Iterable, Iterator, Mapping


CAMPAIGN_ROOT = Path(__file__).resolve().parents[2]
FORMAT = "gamma-theta-online-kernel-depth-measurement-v1"
CERTIFICATE_FORMAT = "gamma-theta-k3-recursive-failure-certificates-v1"
STRICTNESS_FORMAT = "gamma-theta-c15-k2-not-k3-v1"


@dataclass(frozen=True, slots=True)
class KernelGraph:
    """A finite simple graph with independent adjacency bit rows."""

    order: int
    neighbors: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.order) is not int or not 0 <= self.order <= 62:
            raise ValueError("order must be an integer in [0,62]")
        if (
            type(self.neighbors) is not tuple
            or len(self.neighbors) != self.order
        ):
            raise ValueError("one adjacency row is required per vertex")
        full = (1 << self.order) - 1
        for vertex, row in enumerate(self.neighbors):
            if type(row) is not int or row < 0 or row & ~full:
                raise ValueError("adjacency row contains an invalid vertex")
            if row & (1 << vertex):
                raise ValueError("loops are forbidden")
        for first in range(self.order):
            for second in range(first + 1, self.order):
                if bool(self.neighbors[first] & (1 << second)) != bool(
                    self.neighbors[second] & (1 << first)
                ):
                    raise ValueError("adjacency must be symmetric")

    @property
    def full(self) -> int:
        return (1 << self.order) - 1

    @property
    def size(self) -> int:
        return sum(row.bit_count() for row in self.neighbors) // 2

    @classmethod
    def from_edges(
        cls, order: int, edges: Iterable[tuple[int, int]]
    ) -> "KernelGraph":
        rows = [0] * order
        seen: set[tuple[int, int]] = set()
        for edge in edges:
            if type(edge) not in (tuple, list) or len(edge) != 2:
                raise ValueError("each edge must contain two endpoints")
            first, second = edge
            if (
                type(first) is not int
                or type(second) is not int
                or not 0 <= first < order
                or not 0 <= second < order
                or first == second
            ):
                raise ValueError("invalid edge")
            normalized = (
                (first, second) if first < second else (second, first)
            )
            if normalized in seen:
                raise ValueError("duplicate edge")
            seen.add(normalized)
            rows[first] |= 1 << second
            rows[second] |= 1 << first
        return cls(order, tuple(rows))

    @classmethod
    def cycle(cls, order: int) -> "KernelGraph":
        if order < 3:
            raise ValueError("a simple cycle has order at least three")
        return cls.from_edges(
            order, ((vertex, (vertex + 1) % order) for vertex in range(order))
        )

    @classmethod
    def from_graph6(cls, record: str | bytes) -> "KernelGraph":
        if isinstance(record, str):
            try:
                raw = record.encode("ascii")
            except UnicodeEncodeError as error:
                raise ValueError("graph6 must be ASCII") from error
        elif isinstance(record, bytes):
            raw = record
        else:
            raise ValueError("graph6 must be text or bytes")
        header = b">>graph6<<"
        if raw.startswith(header):
            raw = raw[len(header) :]
        if not raw or raw[0] == 126 or not 63 <= raw[0] <= 125:
            raise ValueError("only ordinary graph6 orders are accepted")
        order = raw[0] - 63
        if order > 62:
            raise ValueError("graph6 order exceeds this checker's limit")
        edge_bits = order * (order - 1) // 2
        payload_length = (edge_bits + 5) // 6
        if len(raw) != 1 + payload_length:
            raise ValueError("wrong graph6 payload length")
        if any(not 63 <= byte <= 126 for byte in raw[1:]):
            raise ValueError("invalid graph6 payload")
        padding = payload_length * 6 - edge_bits
        if padding and (raw[-1] - 63) & ((1 << padding) - 1):
            raise ValueError("nonzero graph6 padding")
        rows = [0] * order
        position = 0
        for second in range(1, order):
            for first in range(second):
                value = raw[1 + position // 6] - 63
                if value >> (5 - position % 6) & 1:
                    rows[first] |= 1 << second
                    rows[second] |= 1 << first
                position += 1
        return cls(order, tuple(rows))

    def to_graph6(self) -> str:
        bits: list[int] = []
        for second in range(1, self.order):
            for first in range(second):
                bits.append(
                    int(bool(self.neighbors[first] & (1 << second)))
                )
        while len(bits) % 6:
            bits.append(0)
        output = bytearray((self.order + 63,))
        for start in range(0, len(bits), 6):
            value = 0
            for bit in bits[start : start + 6]:
                value = value << 1 | bit
            output.append(value + 63)
        return output.decode("ascii")


def combination_masks(order: int, cardinality: int) -> Iterator[int]:
    if (
        type(order) is not int
        or type(cardinality) is not int
        or order < 0
        or not 0 <= cardinality <= order
    ):
        raise ValueError("invalid subset cardinality")
    for vertices in combinations(range(order), cardinality):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


def is_dominating(graph: KernelGraph, state: int) -> bool:
    if type(state) is not int or state < 0 or state & ~graph.full:
        return False
    covered = state
    remaining = state
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        covered |= graph.neighbors[bit.bit_length() - 1]
    return covered == graph.full


def first_undominated(graph: KernelGraph, state: int) -> int | None:
    for vertex in range(graph.order):
        if state & (1 << vertex) or graph.neighbors[vertex] & state:
            continue
        return vertex
    return None


def is_independent(graph: KernelGraph, state: int) -> bool:
    if type(state) is not int or state < 0 or state & ~graph.full:
        return False
    remaining = state
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        vertex = bit.bit_length() - 1
        if graph.neighbors[vertex] & remaining:
            return False
    return True


def independence_number(graph: KernelGraph) -> int:
    for cardinality in range(graph.order, -1, -1):
        if any(
            is_independent(graph, state)
            for state in combination_masks(graph.order, cardinality)
        ):
            return cardinality
    raise AssertionError("the empty set is independent")


def maximum_independent_states(
    graph: KernelGraph, guard_count: int
) -> tuple[int, ...]:
    if independence_number(graph) != guard_count:
        return ()
    return tuple(
        state
        for state in combination_masks(graph.order, guard_count)
        if is_independent(graph, state)
    )


def dominating_configurations(
    graph: KernelGraph, guard_count: int
) -> frozenset[int]:
    return frozenset(
        state
        for state in combination_masks(graph.order, guard_count)
        if is_dominating(graph, state)
    )


def adjacent_guards(
    graph: KernelGraph, state: int, attacked: int
) -> tuple[int, ...]:
    if (
        type(attacked) is not int
        or not 0 <= attacked < graph.order
        or state & (1 << attacked)
    ):
        raise ValueError("attack must be a valid unoccupied vertex")
    movable = state & graph.neighbors[attacked]
    result: list[int] = []
    while movable:
        bit = movable & -movable
        movable ^= bit
        result.append(bit.bit_length() - 1)
    return tuple(result)


def successor(state: int, guard: int, attacked: int) -> int:
    return state ^ (1 << guard) ^ (1 << attacked)


def predecessor_kernel(
    graph: KernelGraph,
    configurations: frozenset[int],
    active: frozenset[int],
) -> frozenset[int]:
    """Apply one online attack/response predecessor operator."""

    survivors: set[int] = set()
    for state in configurations:
        for attacked in range(graph.order):
            if state & (1 << attacked):
                continue
            if not any(
                successor(state, guard, attacked) in active
                for guard in adjacent_guards(graph, state, attacked)
            ):
                break
        else:
            survivors.add(state)
    return frozenset(survivors)


@dataclass(frozen=True, slots=True)
class KernelProfile:
    guard_count: int
    levels: tuple[frozenset[int], ...]
    deletion_rank: Mapping[int, int]
    stable_family: frozenset[int]

    @property
    def full_deletion_depth(self) -> int | None:
        return len(self.levels) - 1 if not self.stable_family else None

    def level(self, horizon: int) -> frozenset[int]:
        if type(horizon) is not int or horizon < 0:
            raise ValueError("horizon must be a nonnegative integer")
        if horizon < len(self.levels):
            return self.levels[horizon]
        return self.stable_family


def kernel_profile(graph: KernelGraph, guard_count: int) -> KernelProfile:
    configurations = dominating_configurations(graph, guard_count)
    levels = [configurations]
    deletion_rank: dict[int, int] = {}
    active = configurations
    while active:
        following = predecessor_kernel(graph, configurations, active)
        round_index = len(levels)
        for state in active - following:
            deletion_rank[state] = round_index
        levels.append(following)
        if following == active:
            return KernelProfile(
                guard_count,
                tuple(levels),
                deletion_rank,
                active,
            )
        active = following
    return KernelProfile(
        guard_count,
        tuple(levels),
        deletion_rank,
        frozenset(),
    )


@dataclass(frozen=True, slots=True)
class FailureBranch:
    guard: int
    child: "FailureNode"


@dataclass(frozen=True, slots=True)
class FailureNode:
    """A recursive proof that ``configuration`` is not in ``K_horizon``."""

    configuration: int
    horizon: int
    undominated: int | None
    attack: int | None
    branches: tuple[FailureBranch, ...]


@dataclass(frozen=True, slots=True)
class SurvivalResponse:
    attack: int
    guard: int
    child: "SurvivalNode"


@dataclass(frozen=True, slots=True)
class SurvivalNode:
    """An explicit online response tree proving membership in ``K_horizon``."""

    configuration: int
    horizon: int
    responses: tuple[SurvivalResponse, ...]


@dataclass(frozen=True, slots=True)
class ForcedFailureCertificate:
    guard_count: int
    horizon: int
    independent_state: int
    root: FailureNode


def build_failure_node(
    graph: KernelGraph,
    profile: KernelProfile,
    state: int,
    horizon: int,
    memo: dict[tuple[int, int], FailureNode | None] | None = None,
) -> FailureNode | None:
    """Construct a recursive nonmembership certificate from frozen levels."""

    if memo is None:
        memo = {}
    key = (state, horizon)
    if key in memo:
        return memo[key]
    if state not in profile.level(0):
        witness = first_undominated(graph, state)
        if witness is None:
            raise AssertionError("state outside K0 unexpectedly dominates")
        node = FailureNode(state, horizon, witness, None, ())
        memo[key] = node
        return node
    if state in profile.level(horizon):
        memo[key] = None
        return None
    if horizon == 0:
        raise AssertionError("a dominating state belongs to K0")

    for attacked in range(graph.order):
        if state & (1 << attacked):
            continue
        branches: list[FailureBranch] = []
        for guard in adjacent_guards(graph, state, attacked):
            child_state = successor(state, guard, attacked)
            child = build_failure_node(
                graph, profile, child_state, horizon - 1, memo
            )
            if child is None:
                break
            branches.append(FailureBranch(guard, child))
        else:
            node = FailureNode(
                state,
                horizon,
                None,
                attacked,
                tuple(branches),
            )
            memo[key] = node
            return node
    raise AssertionError("kernel nonmembership has no failing attack")


def build_survival_node(
    graph: KernelGraph,
    profile: KernelProfile,
    state: int,
    horizon: int,
    memo: dict[tuple[int, int], SurvivalNode] | None = None,
) -> SurvivalNode:
    """Construct one explicit adaptive response tree from frozen levels."""

    if state not in profile.level(horizon):
        raise ValueError("state does not survive the requested horizon")
    if memo is None:
        memo = {}
    key = (state, horizon)
    if key in memo:
        return memo[key]
    if horizon == 0:
        node = SurvivalNode(state, 0, ())
        memo[key] = node
        return node
    responses: list[SurvivalResponse] = []
    target_level = profile.level(horizon - 1)
    for attacked in range(graph.order):
        if state & (1 << attacked):
            continue
        for guard in adjacent_guards(graph, state, attacked):
            child_state = successor(state, guard, attacked)
            if child_state in target_level:
                child = build_survival_node(
                    graph,
                    profile,
                    child_state,
                    horizon - 1,
                    memo,
                )
                responses.append(
                    SurvivalResponse(attacked, guard, child)
                )
                break
        else:
            raise AssertionError("surviving state lacks a response")
    node = SurvivalNode(state, horizon, tuple(responses))
    memo[key] = node
    return node


def verify_failure_node(
    graph: KernelGraph,
    guard_count: int,
    node: FailureNode,
    *,
    expected_state: int | None = None,
    expected_horizon: int | None = None,
) -> bool:
    """Verify a recursive failure tree without computing any kernel."""

    try:
        if not isinstance(node, FailureNode):
            return False
        state = node.configuration
        horizon = node.horizon
        if (
            type(state) is not int
            or state < 0
            or state & ~graph.full
            or state.bit_count() != guard_count
            or type(horizon) is not int
            or horizon < 0
            or expected_state is not None
            and state != expected_state
            or expected_horizon is not None
            and horizon != expected_horizon
            or not isinstance(node.branches, tuple)
        ):
            return False
        if node.undominated is not None:
            witness = node.undominated
            return (
                type(witness) is int
                and 0 <= witness < graph.order
                and node.attack is None
                and node.branches == ()
                and not (
                    state & (1 << witness)
                    or graph.neighbors[witness] & state
                )
                and not is_dominating(graph, state)
            )
        if (
            horizon == 0
            or not is_dominating(graph, state)
            or type(node.attack) is not int
            or not 0 <= node.attack < graph.order
            or state & (1 << node.attack)
        ):
            return False
        expected_guards = adjacent_guards(graph, state, node.attack)
        if len(node.branches) != len(expected_guards):
            return False
        records: dict[int, FailureBranch] = {}
        for branch in node.branches:
            if (
                not isinstance(branch, FailureBranch)
                or type(branch.guard) is not int
                or branch.guard in records
            ):
                return False
            records[branch.guard] = branch
        if set(records) != set(expected_guards):
            return False
        for guard, branch in records.items():
            child_state = successor(state, guard, node.attack)
            if not verify_failure_node(
                graph,
                guard_count,
                branch.child,
                expected_state=child_state,
                expected_horizon=horizon - 1,
            ):
                return False
        return True
    except (IndexError, TypeError, ValueError, OverflowError, RecursionError):
        return False


def verify_survival_node(
    graph: KernelGraph,
    guard_count: int,
    node: SurvivalNode,
    *,
    expected_state: int | None = None,
    expected_horizon: int | None = None,
) -> bool:
    """Verify an explicit finite online strategy without kernel iteration."""

    try:
        if not isinstance(node, SurvivalNode):
            return False
        state = node.configuration
        horizon = node.horizon
        if (
            type(state) is not int
            or state < 0
            or state & ~graph.full
            or state.bit_count() != guard_count
            or type(horizon) is not int
            or horizon < 0
            or expected_state is not None
            and state != expected_state
            or expected_horizon is not None
            and horizon != expected_horizon
            or not isinstance(node.responses, tuple)
            or not is_dominating(graph, state)
        ):
            return False
        if horizon == 0:
            return node.responses == ()
        expected_attacks = {
            vertex
            for vertex in range(graph.order)
            if not state & (1 << vertex)
        }
        if len(node.responses) != len(expected_attacks):
            return False
        records: dict[int, SurvivalResponse] = {}
        for response in node.responses:
            if (
                not isinstance(response, SurvivalResponse)
                or type(response.attack) is not int
                or response.attack in records
            ):
                return False
            records[response.attack] = response
        if set(records) != expected_attacks:
            return False
        for attacked, response in records.items():
            guard = response.guard
            if (
                type(guard) is not int
                or not state & (1 << guard)
                or not graph.neighbors[attacked] & (1 << guard)
            ):
                return False
            child_state = successor(state, guard, attacked)
            if not verify_survival_node(
                graph,
                guard_count,
                response.child,
                expected_state=child_state,
                expected_horizon=horizon - 1,
            ):
                return False
        return True
    except (IndexError, TypeError, ValueError, OverflowError, RecursionError):
        return False


def verify_forced_failure(
    graph: KernelGraph, certificate: ForcedFailureCertificate
) -> bool:
    try:
        if not isinstance(certificate, ForcedFailureCertificate):
            return False
        guard_count = certificate.guard_count
        horizon = certificate.horizon
        independent = certificate.independent_state
        if (
            type(guard_count) is not int
            or not 0 <= guard_count <= graph.order
            or independence_number(graph) != guard_count
            or type(horizon) is not int
            or horizon < 1
            or type(independent) is not int
            or independent.bit_count() != guard_count
            or not is_independent(graph, independent)
        ):
            return False
        return verify_failure_node(
            graph,
            guard_count,
            certificate.root,
            expected_state=independent,
            expected_horizon=horizon,
        )
    except (TypeError, ValueError, OverflowError, RecursionError):
        return False


def failure_to_json(node: FailureNode) -> dict[str, object]:
    if node.undominated is not None:
        return {
            "kind": "nondominating",
            "configuration": node.configuration,
            "horizon": node.horizon,
            "undominated": node.undominated,
        }
    return {
        "kind": "attack",
        "configuration": node.configuration,
        "horizon": node.horizon,
        "attack": node.attack,
        "branches": [
            {"guard": branch.guard, "child": failure_to_json(branch.child)}
            for branch in node.branches
        ],
    }


def failure_from_json(value: object) -> FailureNode:
    if not isinstance(value, dict):
        raise ValueError("failure node must be an object")
    kind = value.get("kind")
    if kind == "nondominating":
        if set(value) != {
            "kind",
            "configuration",
            "horizon",
            "undominated",
        }:
            raise ValueError("unexpected nondominating-node fields")
        return FailureNode(
            value["configuration"],
            value["horizon"],
            value["undominated"],
            None,
            (),
        )
    if kind == "attack":
        if set(value) != {
            "kind",
            "configuration",
            "horizon",
            "attack",
            "branches",
        } or not isinstance(value["branches"], list):
            raise ValueError("unexpected attack-node fields")
        branches: list[FailureBranch] = []
        for item in value["branches"]:
            if (
                not isinstance(item, dict)
                or set(item) != {"guard", "child"}
            ):
                raise ValueError("malformed failure branch")
            branches.append(
                FailureBranch(
                    item["guard"], failure_from_json(item["child"])
                )
            )
        return FailureNode(
            value["configuration"],
            value["horizon"],
            None,
            value["attack"],
            tuple(branches),
        )
    raise ValueError("unknown failure-node kind")


def survival_to_json(node: SurvivalNode) -> dict[str, object]:
    return {
        "configuration": node.configuration,
        "horizon": node.horizon,
        "responses": [
            {
                "attack": response.attack,
                "guard": response.guard,
                "child": survival_to_json(response.child),
            }
            for response in node.responses
        ],
    }


def survival_from_json(value: object) -> SurvivalNode:
    if (
        not isinstance(value, dict)
        or set(value) != {"configuration", "horizon", "responses"}
        or not isinstance(value["responses"], list)
    ):
        raise ValueError("malformed survival node")
    responses: list[SurvivalResponse] = []
    for item in value["responses"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"attack", "guard", "child"}
        ):
            raise ValueError("malformed survival response")
        responses.append(
            SurvivalResponse(
                item["attack"],
                item["guard"],
                survival_from_json(item["child"]),
            )
        )
    return SurvivalNode(
        value["configuration"], value["horizon"], tuple(responses)
    )


def forced_failure_to_json(
    certificate: ForcedFailureCertificate,
) -> dict[str, object]:
    return {
        "guard_count": certificate.guard_count,
        "horizon": certificate.horizon,
        "independent_state": certificate.independent_state,
        "root": failure_to_json(certificate.root),
    }


def forced_failure_from_json(value: object) -> ForcedFailureCertificate:
    if (
        not isinstance(value, dict)
        or set(value)
        != {"guard_count", "horizon", "independent_state", "root"}
    ):
        raise ValueError("malformed forced-failure certificate")
    return ForcedFailureCertificate(
        value["guard_count"],
        value["horizon"],
        value["independent_state"],
        failure_from_json(value["root"]),
    )


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ValueError("duplicate or non-text JSON key")
        result[key] = value
    return result


def _strict_json_loads(text: str) -> object:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON constant: {value}")
            ),
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise ValueError(f"invalid JSON: {error}") from error


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _atomic_json(path: Path, value: object) -> None:
    _atomic_bytes(path, json.dumps(value, indent=2, sort_keys=True).encode() + b"\n")


@dataclass(frozen=True, slots=True)
class SelectedRow:
    row_index: int
    graph6: str
    graph: KernelGraph
    profile: KernelProfile
    independent_states: tuple[int, ...]
    earliest_forced_rank: int
    latest_forced_rank: int


def _selected_rows(ledger: Path) -> tuple[SelectedRow, ...]:
    selected: list[SelectedRow] = []
    target_rows = 0
    with ledger.open(newline="", encoding="ascii") as handle:
        reader = csv.DictReader(handle)
        required = {
            "canonical_graph6",
            "gamma_a",
            "gamma_b",
            "alpha_a",
            "alpha_b",
            "gamma_infinity_a",
            "gamma_infinity_b",
            "theta_a",
            "theta_b",
        }
        if reader.fieldnames is None or not required <= set(reader.fieldnames):
            raise ValueError("edge-toggle ledger schema differs")
        for row_index, row in enumerate(reader):
            parameters = tuple(
                int(row[field])
                for field in (
                    "gamma_a",
                    "gamma_b",
                    "alpha_a",
                    "alpha_b",
                    "gamma_infinity_a",
                    "gamma_infinity_b",
                    "theta_a",
                    "theta_b",
                )
            )
            if parameters != (3, 3, 3, 3, 4, 4, 4, 4):
                continue
            target_rows += 1
            graph = KernelGraph.from_graph6(row["canonical_graph6"])
            profile = kernel_profile(graph, 3)
            independent = maximum_independent_states(graph, 3)
            if not independent:
                raise AssertionError("stored alpha=3 row lacks forced triples")
            ranks = tuple(profile.deletion_rank[state] for state in independent)
            if min(ranks) <= 2:
                continue
            selected.append(
                SelectedRow(
                    row_index,
                    row["canonical_graph6"],
                    graph,
                    profile,
                    independent,
                    min(ranks),
                    max(ranks),
                )
            )
    if target_rows != 8_587 or len(selected) != 526:
        raise RuntimeError(
            f"unexpected target/survivor counts: {target_rows}/{len(selected)}"
        )
    return tuple(selected)


def _load_trace_rows(
    certificate_path: Path, needed: set[int]
) -> dict[int, dict[str, object]]:
    records: dict[int, dict[str, object]] = {}
    with certificate_path.open(encoding="ascii") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"invalid trace JSON on line {line_number}"
                ) from error
            if not isinstance(value, dict) or value.get("type") != "row":
                continue
            row_index = value.get("row_index")
            if row_index in needed:
                if row_index in records:
                    raise ValueError("duplicate trace row index")
                records[row_index] = value
    if set(records) != needed:
        raise ValueError("third-audit trace omits selected rows")
    return records


def _trace_rank_map(value: object) -> dict[int, int]:
    if not isinstance(value, list):
        raise ValueError("deletion rounds must be an array")
    ranks: dict[int, int] = {}
    for round_index, round_value in enumerate(value, 1):
        if not isinstance(round_value, list) or not round_value:
            raise ValueError("deletion rounds must be nonempty arrays")
        for record in round_value:
            if (
                not isinstance(record, list)
                or len(record) != 2
                or type(record[0]) is not int
                or type(record[1]) is not int
                or record[0] in ranks
            ):
                raise ValueError("malformed or duplicate deletion record")
            ranks[record[0]] = round_index
    return ranks


def _node_counts(node: FailureNode) -> tuple[int, int]:
    nodes = 1
    leaves = int(node.undominated is not None)
    for branch in node.branches:
        child_nodes, child_leaves = _node_counts(branch.child)
        nodes += child_nodes
        leaves += child_leaves
    return nodes, leaves


def _survival_counts(node: SurvivalNode) -> tuple[int, int]:
    nodes = 1
    leaves = int(node.horizon == 0)
    for response in node.responses:
        child_nodes, child_leaves = _survival_counts(response.child)
        nodes += child_nodes
        leaves += child_leaves
    return nodes, leaves


def _build_c15_strictness() -> tuple[dict[str, object], dict[str, int]]:
    graph = KernelGraph.cycle(15)
    profile = kernel_profile(graph, 7)
    expected_sizes = (765, 120, 15, 0)
    sizes = tuple(len(profile.level(index)) for index in range(4))
    if sizes != expected_sizes:
        raise AssertionError(f"unexpected C15 kernel sizes: {sizes}")
    independent_states = maximum_independent_states(graph, 7)
    if len(independent_states) != 15 or not all(
        state in profile.level(2) and state not in profile.level(3)
        for state in independent_states
    ):
        raise AssertionError("C15 forced-state strictness differs")
    state = sum(1 << vertex for vertex in (0, 2, 4, 6, 8, 10, 12))
    survival = build_survival_node(graph, profile, state, 2)
    failure = build_failure_node(graph, profile, state, 3)
    if failure is None:
        raise AssertionError("C15 failure certificate was not built")
    if not verify_survival_node(graph, 7, survival):
        raise AssertionError("C15 K2 survival certificate failed")
    forced = ForcedFailureCertificate(7, 3, state, failure)
    if not verify_forced_failure(graph, forced):
        raise AssertionError("C15 K3 failure certificate failed")
    payload = {
        "format": STRICTNESS_FORMAT,
        "graph6": graph.to_graph6(),
        "order": graph.order,
        "size": graph.size,
        "guard_count": 7,
        "kernel_sizes_K0_through_K3": list(sizes),
        "maximum_independent_states": len(independent_states),
        "independent_state": state,
        "survival_horizon": 2,
        "survival_certificate": survival_to_json(survival),
        "failure_horizon": 3,
        "failure_certificate": forced_failure_to_json(forced),
    }
    survival_nodes, survival_leaves = _survival_counts(survival)
    failure_nodes, failure_leaves = _node_counts(failure)
    return payload, {
        "survival_nodes": survival_nodes,
        "survival_leaves": survival_leaves,
        "failure_nodes": failure_nodes,
        "failure_leaves": failure_leaves,
    }


def _verify_recursive_file(
    path: Path,
    *,
    source_sha: str,
    ledger_sha: str,
    expected_rows: int,
) -> tuple[int, int, str]:
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) != expected_rows + 2:
        raise AssertionError("recursive certificate line count differs")
    header = _strict_json_loads(lines[0])
    if header != {
        "type": "header",
        "format": CERTIFICATE_FORMAT,
        "horizon": 3,
        "guard_count": 3,
        "source_sha256": source_sha,
        "ledger_sha256": ledger_sha,
    }:
        raise AssertionError("recursive certificate header differs")
    digest = sha256()
    seen_graphs: set[str] = set()
    nodes = 0
    leaves = 0
    for line in lines[1:-1]:
        value = _strict_json_loads(line)
        if (
            not isinstance(value, dict)
            or set(value)
            != {
                "type",
                "ledger_row_index",
                "graph6",
                "certificate",
                "nodes",
                "leaves",
            }
            or value.get("type") != "row"
            or type(value.get("ledger_row_index")) is not int
            or not isinstance(value.get("graph6"), str)
            or value["graph6"] in seen_graphs
            or type(value.get("nodes")) is not int
            or type(value.get("leaves")) is not int
        ):
            raise AssertionError("malformed recursive certificate row")
        graph = KernelGraph.from_graph6(value["graph6"])
        certificate = forced_failure_from_json(value["certificate"])
        if not verify_forced_failure(graph, certificate):
            raise AssertionError("serialized recursive certificate failed")
        counted_nodes, counted_leaves = _node_counts(certificate.root)
        if (
            value["nodes"] != counted_nodes
            or value["leaves"] != counted_leaves
        ):
            raise AssertionError("serialized certificate counts differ")
        seen_graphs.add(value["graph6"])
        nodes += counted_nodes
        leaves += counted_leaves
        digest.update(line.encode("ascii") + b"\n")
    trailer = _strict_json_loads(lines[-1])
    expected_digest = digest.hexdigest()
    if trailer != {
        "type": "trailer",
        "format": CERTIFICATE_FORMAT,
        "rows": expected_rows,
        "row_stream_sha256": expected_digest,
    }:
        raise AssertionError("recursive certificate trailer differs")
    return nodes, leaves, expected_digest


def _verify_c15_file(path: Path, source_sha: str) -> None:
    value = _strict_json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("format") != STRICTNESS_FORMAT:
        raise AssertionError("C15 strictness artifact format differs")
    if value.get("source_sha256") != source_sha:
        raise AssertionError("C15 source binding differs")
    graph6 = value.get("graph6")
    if not isinstance(graph6, str):
        raise AssertionError("C15 graph6 is missing")
    graph = KernelGraph.from_graph6(graph6)
    if graph != KernelGraph.cycle(15):
        raise AssertionError("strictness graph is not labeled C15")
    if (
        value.get("order") != 15
        or value.get("size") != 15
        or value.get("guard_count") != 7
        or value.get("kernel_sizes_K0_through_K3") != [765, 120, 15, 0]
        or value.get("maximum_independent_states") != 15
        or value.get("survival_horizon") != 2
        or value.get("failure_horizon") != 3
    ):
        raise AssertionError("C15 strictness metadata differs")
    state = value.get("independent_state")
    if type(state) is not int:
        raise AssertionError("C15 independent state is malformed")
    survival = survival_from_json(value.get("survival_certificate"))
    failure = forced_failure_from_json(value.get("failure_certificate"))
    if (
        not verify_survival_node(
            graph,
            7,
            survival,
            expected_state=state,
            expected_horizon=2,
        )
        or not verify_forced_failure(graph, failure)
        or failure.independent_state != state
        or failure.horizon != 3
    ):
        raise AssertionError("serialized C15 strictness certificate failed")


def run_measurement(
    *,
    ledger: Path,
    third_certificates: Path,
    output: Path,
    recursive_certificates: Path,
    strictness_certificate: Path,
) -> dict[str, object]:
    started = time.perf_counter()
    source_path = Path(__file__).resolve()
    source_sha = _sha256_file(source_path)
    selected = _selected_rows(ledger)
    trace_rows = _load_trace_rows(
        third_certificates, {row.row_index for row in selected}
    )

    earliest: Counter[int] = Counter()
    latest: Counter[int] = Counter()
    full_depth: Counter[int] = Counter()
    forced_triples: Counter[int] = Counter()
    joint: Counter[tuple[int, int, int]] = Counter()
    certificate_rows: list[dict[str, object]] = []
    certificate_node_count = 0
    certificate_leaf_count = 0
    maximum_certificate_nodes = 0
    deep_rows: list[dict[str, object]] = []

    for row in selected:
        trace = trace_rows[row.row_index]
        if trace.get("graph6") != row.graph6:
            raise AssertionError("trace graph6 differs from ledger")
        rounds = trace.get("deletion_rounds")
        trace_ranks = _trace_rank_map(rounds)
        if (
            trace.get("initial_dominating_configurations")
            != len(row.profile.level(0))
            or trace_ranks != dict(row.profile.deletion_rank)
            or not isinstance(rounds, list)
            or len(rounds) != row.profile.full_deletion_depth
        ):
            raise AssertionError("independent kernel profile differs from trace")

        depth = row.profile.full_deletion_depth
        if depth is None:
            raise AssertionError("selected noneternal row has a stable family")
        earliest[row.earliest_forced_rank] += 1
        latest[row.latest_forced_rank] += 1
        full_depth[depth] += 1
        joint[
            (row.earliest_forced_rank, row.latest_forced_rank, depth)
        ] += 1
        forced_triples.update(
            row.profile.deletion_rank[state]
            for state in row.independent_states
        )

        if row.earliest_forced_rank == 3:
            independent = next(
                state
                for state in row.independent_states
                if row.profile.deletion_rank[state] == 3
            )
            root = build_failure_node(
                row.graph, row.profile, independent, 3
            )
            if root is None:
                raise AssertionError("K3 failure tree was not constructed")
            certificate = ForcedFailureCertificate(3, 3, independent, root)
            if not verify_forced_failure(row.graph, certificate):
                raise AssertionError("generated K3 certificate failed")
            if independent not in row.profile.level(2):
                raise AssertionError("K3 witness did not survive K2")
            nodes, leaves = _node_counts(root)
            certificate_node_count += nodes
            certificate_leaf_count += leaves
            maximum_certificate_nodes = max(
                maximum_certificate_nodes, nodes
            )
            certificate_rows.append(
                {
                    "type": "row",
                    "ledger_row_index": row.row_index,
                    "graph6": row.graph6,
                    "certificate": forced_failure_to_json(certificate),
                    "nodes": nodes,
                    "leaves": leaves,
                }
            )
        else:
            deep_rows.append(
                {
                    "ledger_row_index": row.row_index,
                    "graph6": row.graph6,
                    "order": row.graph.order,
                    "size": row.graph.size,
                    "earliest_forced_rank": row.earliest_forced_rank,
                    "latest_forced_rank": row.latest_forced_rank,
                    "full_deletion_depth": depth,
                    "kernel_sizes": [
                        len(level) for level in row.profile.levels
                    ],
                }
            )

    if len(certificate_rows) != 518 or len(deep_rows) != 8:
        raise AssertionError("unexpected K3/deep split")

    header = {
        "type": "header",
        "format": CERTIFICATE_FORMAT,
        "horizon": 3,
        "guard_count": 3,
        "source_sha256": source_sha,
        "ledger_sha256": _sha256_file(ledger),
    }
    row_digest = sha256()
    encoded_rows: list[bytes] = []
    for record in certificate_rows:
        encoded = _canonical_json(record)
        encoded_rows.append(encoded)
        row_digest.update(encoded + b"\n")
    trailer = {
        "type": "trailer",
        "format": CERTIFICATE_FORMAT,
        "rows": len(certificate_rows),
        "row_stream_sha256": row_digest.hexdigest(),
    }
    certificate_content = (
        _canonical_json(header)
        + b"\n"
        + b"\n".join(encoded_rows)
        + b"\n"
        + _canonical_json(trailer)
        + b"\n"
    )
    _atomic_bytes(recursive_certificates, certificate_content)
    replay_nodes, replay_leaves, replay_digest = _verify_recursive_file(
        recursive_certificates,
        source_sha=source_sha,
        ledger_sha=_sha256_file(ledger),
        expected_rows=518,
    )
    if (
        replay_nodes != certificate_node_count
        or replay_leaves != certificate_leaf_count
        or replay_digest != row_digest.hexdigest()
    ):
        raise AssertionError("serialized recursive replay counts differ")

    c15_payload, c15_counts = _build_c15_strictness()
    c15_payload["source_sha256"] = source_sha
    _atomic_json(strictness_certificate, c15_payload)
    _verify_c15_file(strictness_certificate, source_sha)

    usage = resource.getrusage(resource.RUSAGE_SELF)
    result: dict[str, object] = {
        "format": FORMAT,
        "status": "complete",
        "scope": (
            "The 526 canonical gamma=alpha=3, gamma_infinity=theta=4 "
            "edge-toggle rows that survive K2; not all graphs of orders "
            "11 or 12."
        ),
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one edge",
            "kernel": "simultaneous online predecessor rounds",
        },
        "population": {
            "stored_parameter_target": 8_587,
            "survives_K2": len(selected),
            "eliminated_at_K3": len(certificate_rows),
            "survives_K3": len(deep_rows),
            "survives_K4": sum(
                row.earliest_forced_rank > 4 for row in selected
            ),
            "earliest_forced_deletion_rank": {
                str(key): earliest[key] for key in sorted(earliest)
            },
            "latest_forced_deletion_rank": {
                str(key): latest[key] for key in sorted(latest)
            },
            "individual_forced_triple_deletion_rank": {
                str(key): forced_triples[key]
                for key in sorted(forced_triples)
            },
            "full_kernel_deletion_depth": {
                str(key): full_depth[key] for key in sorted(full_depth)
            },
            "joint_earliest_latest_full": {
                ",".join(map(str, key)): joint[key]
                for key in sorted(joint)
            },
            "deep_rows": deep_rows,
        },
        "recursive_certificates": {
            "path": str(recursive_certificates),
            "sha256": _sha256_file(recursive_certificates),
            "rows": len(certificate_rows),
            "nodes": certificate_node_count,
            "leaves": certificate_leaf_count,
            "maximum_nodes_per_certificate": maximum_certificate_nodes,
            "row_stream_sha256": row_digest.hexdigest(),
        },
        "strictness_witness": {
            "path": str(strictness_certificate),
            "sha256": _sha256_file(strictness_certificate),
            **c15_counts,
        },
        "cross_check": {
            "method": (
                "fresh kernel implementation compared exact deletion rank "
                "of every dominating triple with the third-audit traces"
            ),
            "rows": len(selected),
            "configurations": sum(
                len(row.profile.level(0)) for row in selected
            ),
            "passed": True,
        },
        "inputs": {
            "ledger": str(ledger),
            "ledger_sha256": _sha256_file(ledger),
            "third_certificates": str(third_certificates),
            "third_certificates_sha256": _sha256_file(third_certificates),
        },
        "implementation": {
            "source": str(source_path),
            "source_sha256": source_sha,
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "resources": {
            "wall_seconds": time.perf_counter() - started,
            "user_cpu_seconds": usage.ru_utime,
            "system_cpu_seconds": usage.ru_stime,
            "maximum_resident_set_size_raw": usage.ru_maxrss,
        },
        "limitations": [
            "K3 eliminates 518 of 526 K2 survivors, not all 526.",
            "Eight rows first lose a forced state only at K5 or K6.",
            "The finite measurement does not resolve the gamma-theta conjecture.",
        ],
    }
    _atomic_json(output, result)
    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        type=Path,
        default=CAMPAIGN_ROOT / "results" / "edge_toggles_unique.csv",
    )
    parser.add_argument(
        "--third-certificates",
        type=Path,
        default=(
            CAMPAIGN_ROOT
            / "results"
            / "edge_toggle_third_evaluation_certificates.ndjson"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            CAMPAIGN_ROOT / "results" / "three_step_kernel_measurement.json"
        ),
    )
    parser.add_argument(
        "--recursive-certificates",
        type=Path,
        default=(
            CAMPAIGN_ROOT
            / "certificates"
            / "k3_three_step_edge_toggle.ndjson"
        ),
    )
    parser.add_argument(
        "--strictness-certificate",
        type=Path,
        default=(
            CAMPAIGN_ROOT / "certificates" / "c15_k2_not_k3.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    paths = {
        "ledger": arguments.ledger.resolve(),
        "third_certificates": arguments.third_certificates.resolve(),
        "output": arguments.output.resolve(),
        "recursive_certificates": arguments.recursive_certificates.resolve(),
        "strictness_certificate": arguments.strictness_certificate.resolve(),
    }
    for label in ("ledger", "third_certificates"):
        if not paths[label].is_file():
            raise SystemExit(f"{label} does not exist: {paths[label]}")
    if len(set(paths.values())) != len(paths):
        raise SystemExit("input and output paths must be distinct")
    result = run_measurement(**paths)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
