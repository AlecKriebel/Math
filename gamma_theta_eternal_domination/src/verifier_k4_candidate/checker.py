"""Fail-closed checker for a decoded ``(n, k) = (12, 4)`` candidate.

The implementation is intentionally small and independent.  It uses ordinary
``frozenset`` neighborhoods, direct subset enumeration, and a complete
anchor-normalized enumeration of all ``4**8`` color rows.  It imports no
campaign search or verifier core.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Iterator, Mapping, Sequence


SCHEMA = "gamma-theta-order12-k4-candidate-v1"
VERIFIER = "independent-k4-candidate-verifier-v1"
N = 12
K = 4
ANCHOR = (0, 1, 2, 3)
OUTER = tuple(range(4, N))
MAX_CANDIDATE_BYTES = 2_000_000
MAX_RECORDED_FAILURES = 32
DEFINITION_LEVEL_CHECKS = (
    "graph_identity",
    "gamma_equals_4",
    "one_guard_eternal_family",
    "theta_at_least_5",
)
Pair = tuple[int, int]
State = tuple[int, int, int, int]


class CandidateFormatError(ValueError):
    """The JSON object is not in the strict candidate format."""


@dataclass(frozen=True, slots=True)
class Graph:
    """A simple labeled graph with ordinary set-valued neighborhoods."""

    adjacency: tuple[frozenset[int], ...]

    def __post_init__(self) -> None:
        order = len(self.adjacency)
        normalized = tuple(frozenset(row) for row in self.adjacency)
        object.__setattr__(self, "adjacency", normalized)
        for vertex, neighbors in enumerate(normalized):
            if vertex in neighbors:
                raise ValueError(f"loop at vertex {vertex}")
            for neighbor in neighbors:
                if type(neighbor) is not int or not 0 <= neighbor < order:
                    raise ValueError("adjacency has an invalid vertex")
                if vertex not in normalized[neighbor]:
                    raise ValueError("adjacency is not symmetric")

    @classmethod
    def from_edges(cls, order: int, edges: Iterable[Pair]) -> "Graph":
        if type(order) is not int or order < 0:
            raise ValueError("order must be a nonnegative integer")
        rows = [set() for _ in range(order)]
        seen: set[Pair] = set()
        for first, second in edges:
            if (
                type(first) is not int
                or type(second) is not int
                or not 0 <= first < order
                or not 0 <= second < order
                or first >= second
            ):
                raise ValueError("edges must be ordered pairs 0 <= u < v < n")
            pair = (first, second)
            if pair in seen:
                raise ValueError("duplicate edge")
            seen.add(pair)
            rows[first].add(second)
            rows[second].add(first)
        return cls(tuple(frozenset(row) for row in rows))

    @property
    def order(self) -> int:
        return len(self.adjacency)

    @property
    def vertices(self) -> range:
        return range(self.order)

    def edges(self) -> tuple[Pair, ...]:
        return tuple(
            (first, second)
            for first in self.vertices
            for second in sorted(self.adjacency[first])
            if first < second
        )

    def has_edge(self, first: int, second: int) -> bool:
        return second in self.adjacency[first]

    def complement_edges(self) -> tuple[Pair, ...]:
        return tuple(
            pair
            for pair in combinations(self.vertices, 2)
            if not self.has_edge(*pair)
        )

    def to_graph6(self) -> str:
        """Return the standard labeled graph6 record, without a header."""

        if self.order > 62:
            raise ValueError("this compact checker supports graph6 order <= 62")
        values = [self.order]
        bits: list[int] = []
        for higher in range(1, self.order):
            for lower in range(higher):
                bits.append(int(self.has_edge(lower, higher)))
        while len(bits) % 6:
            bits.append(0)
        for start in range(0, len(bits), 6):
            value = 0
            for bit in bits[start : start + 6]:
                value = (value << 1) | bit
            values.append(value)
        return "".join(chr(value + 63) for value in values)

    def is_connected(self, vertices: Iterable[int] | None = None) -> bool:
        selected = (
            frozenset(self.vertices)
            if vertices is None
            else frozenset(vertices)
        )
        if not selected:
            return False
        start = min(selected)
        reached = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in self.adjacency[vertex]:
                if neighbor in selected and neighbor not in reached:
                    reached.add(neighbor)
                    stack.append(neighbor)
        return reached == set(selected)

    def is_dominating(self, vertices: Iterable[int]) -> bool:
        selected = frozenset(vertices)
        covered = set(selected)
        for vertex in selected:
            covered.update(self.adjacency[vertex])
        return len(covered) == self.order

    def is_independent(self, vertices: Iterable[int]) -> bool:
        selected = tuple(vertices)
        return all(
            not self.has_edge(first, second)
            for first, second in combinations(selected, 2)
        )


@dataclass(frozen=True, slots=True)
class MinorCertificate:
    kind: str
    branch_sets: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class ImperfectionCertificate:
    kind: str
    vertices: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Candidate:
    order: int
    edges: tuple[Pair, ...]
    graph6: str
    graph6_sha256: str
    edges_sha256: str
    dominating_set: State
    independent_set: State
    eternal_family: tuple[State, ...]
    nonplanarity_minor: MinorCertificate
    imperfection_witness: ImperfectionCertificate

    @property
    def graph(self) -> Graph:
        return Graph.from_edges(self.order, self.edges)


@dataclass(frozen=True, slots=True)
class EternalCheck:
    passed: bool
    family_size: int
    states_checked: int
    unoccupied_attacks_checked: int
    occupied_attacks_excluded: int
    legal_responses_counted: int
    chosen_response_sha256: str
    independent_four_sets: int
    forced_independent_states_missing: tuple[State, ...]
    failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ColorSearch:
    performed: bool
    rows_checked: int
    proper_rows: int
    first_proper_coloring: tuple[int, ...] | None
    trace_sha256: str | None
    trace_format: str


def canonical_edges_bytes(edges: Sequence[Pair]) -> bytes:
    """Canonical compact JSON serialization used by ``edges_sha256``."""

    serializable = [[first, second] for first, second in edges]
    return json.dumps(
        serializable,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("ascii")


def graph6_sha256(record: str) -> str:
    return sha256(record.encode("ascii")).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CandidateFormatError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise CandidateFormatError(f"non-finite JSON number: {token}")


def _exact_keys(
    value: Any,
    expected: set[str],
    location: str,
) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise CandidateFormatError(f"{location} must be an object")
    observed = set(value)
    if observed != expected:
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        raise CandidateFormatError(
            f"{location} keys differ; missing={missing}, extra={extra}"
        )
    return value


def _integer(value: Any, location: str) -> int:
    if type(value) is not int:
        raise CandidateFormatError(f"{location} must be an integer")
    return value


def _string(value: Any, location: str) -> str:
    if not isinstance(value, str):
        raise CandidateFormatError(f"{location} must be a string")
    return value


def _vertex_tuple(
    value: Any,
    *,
    location: str,
    size: int | None = None,
    sorted_required: bool = True,
) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise CandidateFormatError(f"{location} must be an array")
    if size is not None and len(value) != size:
        raise CandidateFormatError(f"{location} must contain {size} vertices")
    vertices = tuple(
        _integer(vertex, f"{location}[{index}]")
        for index, vertex in enumerate(value)
    )
    if any(not 0 <= vertex < N for vertex in vertices):
        raise CandidateFormatError(f"{location} has a vertex outside 0..11")
    if len(set(vertices)) != len(vertices):
        raise CandidateFormatError(f"{location} repeats a vertex")
    if sorted_required and tuple(sorted(vertices)) != vertices:
        raise CandidateFormatError(f"{location} must be strictly increasing")
    return vertices


def parse_candidate(value: Any) -> Candidate:
    """Parse a decoded witness from an already-decoded JSON value."""

    root = _exact_keys(
        value,
        {
            "schema",
            "order",
            "edges",
            "graph6",
            "graph6_sha256",
            "edges_sha256",
            "claims",
            "dominating_set",
            "independent_set",
            "eternal_family",
            "nonplanarity_minor",
            "imperfection_witness",
        },
        "candidate",
    )
    if _string(root["schema"], "schema") != SCHEMA:
        raise CandidateFormatError(f"schema must equal {SCHEMA!r}")
    order = _integer(root["order"], "order")
    if order != N:
        raise CandidateFormatError(f"order must equal {N}")

    raw_edges = root["edges"]
    if not isinstance(raw_edges, list) or len(raw_edges) > N * (N - 1) // 2:
        raise CandidateFormatError("edges must be an array of at most 66 pairs")
    edges: list[Pair] = []
    for index, raw_pair in enumerate(raw_edges):
        if not isinstance(raw_pair, list) or len(raw_pair) != 2:
            raise CandidateFormatError(f"edges[{index}] must be a pair")
        first = _integer(raw_pair[0], f"edges[{index}][0]")
        second = _integer(raw_pair[1], f"edges[{index}][1]")
        if not 0 <= first < second < N:
            raise CandidateFormatError(
                f"edges[{index}] must satisfy 0 <= u < v < 12"
            )
        edges.append((first, second))
    if tuple(sorted(edges)) != tuple(edges) or len(set(edges)) != len(edges):
        raise CandidateFormatError("edges must be unique and lexicographically sorted")

    graph6 = _string(root["graph6"], "graph6")
    try:
        graph6.encode("ascii")
    except UnicodeEncodeError as error:
        raise CandidateFormatError("graph6 must be ASCII") from error
    if not graph6 or any(not 63 <= ord(character) <= 126 for character in graph6):
        raise CandidateFormatError("graph6 contains an invalid character")

    hexadecimal = set("0123456789abcdef")
    g6_hash = _string(root["graph6_sha256"], "graph6_sha256")
    edge_hash = _string(root["edges_sha256"], "edges_sha256")
    for location, digest in (
        ("graph6_sha256", g6_hash),
        ("edges_sha256", edge_hash),
    ):
        if len(digest) != 64 or any(character not in hexadecimal for character in digest):
            raise CandidateFormatError(f"{location} must be lowercase SHA-256")

    claims = _exact_keys(
        root["claims"],
        {
            "gamma",
            "independent_domination",
            "alpha",
            "eternal_domination",
            "theta_lower_bound",
        },
        "claims",
    )
    expected_claims = {
        "gamma": K,
        "independent_domination": K,
        "alpha": K,
        "eternal_domination": K,
        "theta_lower_bound": K + 1,
    }
    for name, expected in expected_claims.items():
        if _integer(claims[name], f"claims.{name}") != expected:
            raise CandidateFormatError(
                f"claims.{name} must equal {expected}"
            )

    dominating = _vertex_tuple(
        root["dominating_set"],
        location="dominating_set",
        size=K,
    )
    independent = _vertex_tuple(
        root["independent_set"],
        location="independent_set",
        size=K,
    )

    raw_family = root["eternal_family"]
    if (
        not isinstance(raw_family, list)
        or not 1 <= len(raw_family) <= 495
    ):
        raise CandidateFormatError(
            "eternal_family must have between 1 and 495 states"
        )
    family = tuple(
        _vertex_tuple(
            raw_state,
            location=f"eternal_family[{index}]",
            size=K,
        )
        for index, raw_state in enumerate(raw_family)
    )
    if tuple(sorted(family)) != family or len(set(family)) != len(family):
        raise CandidateFormatError(
            "eternal_family must be unique and lexicographically sorted"
        )

    raw_minor = _exact_keys(
        root["nonplanarity_minor"],
        {"kind", "branch_sets"},
        "nonplanarity_minor",
    )
    minor_kind = _string(raw_minor["kind"], "nonplanarity_minor.kind")
    expected_branches = {"K5": 5, "K3,3": 6}.get(minor_kind)
    if expected_branches is None:
        raise CandidateFormatError("minor kind must be 'K5' or 'K3,3'")
    raw_branches = raw_minor["branch_sets"]
    if not isinstance(raw_branches, list) or len(raw_branches) != expected_branches:
        raise CandidateFormatError(
            f"{minor_kind} needs exactly {expected_branches} branch sets"
        )
    branches = tuple(
        _vertex_tuple(
            branch,
            location=f"nonplanarity_minor.branch_sets[{index}]",
        )
        for index, branch in enumerate(raw_branches)
    )
    if any(not branch for branch in branches):
        raise CandidateFormatError("minor branch sets must be nonempty")
    flattened = tuple(vertex for branch in branches for vertex in branch)
    if len(set(flattened)) != len(flattened):
        raise CandidateFormatError("minor branch sets must be disjoint")

    raw_imperfection = _exact_keys(
        root["imperfection_witness"],
        {"kind", "vertices"},
        "imperfection_witness",
    )
    imperfection_kind = _string(
        raw_imperfection["kind"],
        "imperfection_witness.kind",
    )
    if imperfection_kind not in {"odd_hole", "odd_antihole"}:
        raise CandidateFormatError(
            "imperfection kind must be 'odd_hole' or 'odd_antihole'"
        )
    cycle = _vertex_tuple(
        raw_imperfection["vertices"],
        location="imperfection_witness.vertices",
        sorted_required=False,
    )
    if len(cycle) < 5 or len(cycle) % 2 == 0:
        raise CandidateFormatError(
            "imperfection witness must have odd length at least five"
        )
    if cycle[0] != min(cycle) or cycle[1] >= cycle[-1]:
        raise CandidateFormatError(
            "cycle order must start at its minimum vertex and use the "
            "lexicographically smaller orientation"
        )

    return Candidate(
        order=order,
        edges=tuple(edges),
        graph6=graph6,
        graph6_sha256=g6_hash,
        edges_sha256=edge_hash,
        dominating_set=dominating,  # type: ignore[arg-type]
        independent_set=independent,  # type: ignore[arg-type]
        eternal_family=family,  # type: ignore[arg-type]
        nonplanarity_minor=MinorCertificate(minor_kind, branches),
        imperfection_witness=ImperfectionCertificate(
            imperfection_kind,
            cycle,
        ),
    )


def load_candidate(path: str | Path) -> tuple[Candidate, str]:
    """Load a strict JSON file and return the parsed object and file hash."""

    source = Path(path)
    size = source.stat().st_size
    if size > MAX_CANDIDATE_BYTES:
        raise CandidateFormatError(
            f"candidate exceeds the {MAX_CANDIDATE_BYTES}-byte limit"
        )
    raw = source.read_bytes()
    if len(raw) != size:
        raise CandidateFormatError("candidate changed while it was read")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CandidateFormatError("candidate JSON must be UTF-8") from error
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise CandidateFormatError(f"invalid JSON: {error.msg}") from error
    except RecursionError as error:
        raise CandidateFormatError("candidate JSON nesting is too deep") from error
    return parse_candidate(decoded), sha256(raw).hexdigest()


def _first_dominating_set(graph: Graph) -> tuple[int, tuple[int, ...]]:
    for size in range(graph.order + 1):
        for vertices in combinations(graph.vertices, size):
            if graph.is_dominating(vertices):
                return size, vertices
    raise AssertionError("the full vertex set must dominate")


def _first_maximum_independent_set(
    graph: Graph,
) -> tuple[int, tuple[int, ...]]:
    for size in range(graph.order, -1, -1):
        for vertices in combinations(graph.vertices, size):
            if graph.is_independent(vertices):
                return size, vertices
    raise AssertionError("the empty set must be independent")


def _maximal_independent_profile(
    graph: Graph,
) -> tuple[tuple[int, ...], int]:
    sizes: list[int] = []
    count = 0
    for size in range(graph.order + 1):
        for vertices in combinations(graph.vertices, size):
            if not graph.is_independent(vertices):
                continue
            selected = frozenset(vertices)
            maximal = all(
                bool(graph.adjacency[outside] & selected)
                for outside in graph.vertices
                if outside not in selected
            )
            if maximal:
                sizes.append(size)
                count += 1
    return tuple(sorted(set(sizes))), count


def check_eternal_family(
    graph: Graph,
    family: Sequence[State],
) -> EternalCheck:
    """Check the one-guard definition literally for a supplied family."""

    failures: list[str] = []

    def fail(message: str) -> None:
        if len(failures) < MAX_RECORDED_FAILURES:
            failures.append(message)

    if not family:
        fail("eternal family is empty")
    valid_states: list[State] = []
    for index, raw_state in enumerate(family):
        try:
            state = tuple(raw_state)
        except TypeError:
            fail(f"state {index} is not iterable")
            continue
        if (
            len(state) != K
            or any(type(vertex) is not int for vertex in state)
            or any(not 0 <= vertex < graph.order for vertex in state)
            or len(set(state)) != K
            or tuple(sorted(state)) != state
        ):
            fail(f"state {index} is not a canonical four-set")
            continue
        valid_states.append(state)  # type: ignore[arg-type]
    if tuple(sorted(valid_states)) != tuple(valid_states):
        fail("eternal family is not lexicographically sorted")
    if len(set(valid_states)) != len(valid_states):
        fail("eternal family repeats a state")
    family_set = frozenset(valid_states)

    chosen = sha256()
    attacks = 0
    occupied_excluded = 0
    legal_count = 0
    for state in valid_states:
        if not graph.is_dominating(state):
            fail(f"selected state {state} does not dominate")
        selected = frozenset(state)
        occupied_excluded += len(state)
        for attacked in graph.vertices:
            if attacked in selected:
                continue
            attacks += 1
            legal: list[tuple[int, State]] = []
            for guard in state:
                if not graph.has_edge(guard, attacked):
                    continue
                successor = tuple(
                    sorted((selected - {guard}) | {attacked})
                )
                if successor in family_set:
                    legal.append((guard, successor))  # type: ignore[arg-type]
            legal_count += len(legal)
            if not legal:
                fail(
                    f"no one-edge, one-guard response from {state} "
                    f"to unoccupied attack {attacked}"
                )
                continue
            guard, successor = legal[0]
            chosen.update(
                (
                    ",".join(map(str, state))
                    + f"|{attacked}|{guard}|"
                    + ",".join(map(str, successor))
                    + "\n"
                ).encode("ascii")
            )

    independent_states = tuple(
        vertices
        for vertices in combinations(graph.vertices, K)
        if graph.is_independent(vertices)
    )
    missing = tuple(
        state for state in independent_states if state not in family_set
    )
    return EternalCheck(
        passed=not failures,
        family_size=len(family),
        states_checked=len(valid_states),
        unoccupied_attacks_checked=attacks,
        occupied_attacks_excluded=occupied_excluded,
        legal_responses_counted=legal_count,
        chosen_response_sha256=chosen.hexdigest(),
        independent_four_sets=len(independent_states),
        forced_independent_states_missing=missing,
        failures=tuple(failures),
    )


def anchored_four_color_search(
    graph: Graph,
    *,
    trace_path: str | Path | None = None,
) -> ColorSearch:
    """Enumerate all anchor-normalized four-colorings of ``complement(G)``.

    The anchor ``0,1,2,3`` must be independent in ``G``.  It is therefore a
    four-clique in the complement and receives colors ``0,1,2,3`` without
    loss of generality.  Every one of the remaining ``4**8`` rows is checked,
    even when a proper row is found.  If requested, the complete deterministic
    text trace is created with exclusive-create semantics.
    """

    if graph.order != N:
        raise ValueError("anchored search requires order 12")
    if not graph.is_independent(ANCHOR):
        raise ValueError("anchor is not a K4 in the complement")

    writer: BinaryIO | None = None
    output = Path(trace_path) if trace_path is not None else None
    created = False
    digest = sha256()

    def emit(line: str) -> None:
        raw = line.encode("ascii")
        digest.update(raw)
        if writer is not None:
            writer.write(raw)

    try:
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            writer = output.open("xb")
            created = True
        complement_edges = graph.complement_edges()
        emit("GT4TRACE 1\n")
        emit(f"graph6 {graph.to_graph6()}\n")
        emit("anchor 0:0 1:1 2:2 3:3\n")
        emit("outer 4 5 6 7 8 9 10 11\n")
        emit("rows 65536\n")

        proper = 0
        first_proper: tuple[int, ...] | None = None
        rows = 0
        for index, digits in enumerate(product(range(K), repeat=len(OUTER))):
            coloring = ANCHOR + digits
            conflict: Pair | None = None
            for first, second in complement_edges:
                if coloring[first] == coloring[second]:
                    conflict = (first, second)
                    break
            digit_text = "".join(map(str, digits))
            if conflict is None:
                proper += 1
                if first_proper is None:
                    first_proper = coloring
                emit(f"r {index:05d} {digit_text} proper\n")
            else:
                emit(
                    f"r {index:05d} {digit_text} conflict "
                    f"{conflict[0]} {conflict[1]}\n"
                )
            rows += 1
        emit(f"summary rows {rows} proper {proper}\n")
        if writer is not None:
            writer.flush()
        return ColorSearch(
            performed=True,
            rows_checked=rows,
            proper_rows=proper,
            first_proper_coloring=first_proper,
            trace_sha256=digest.hexdigest(),
            trace_format="GT4TRACE 1",
        )
    except BaseException:
        if writer is not None:
            writer.close()
            writer = None
        if created and output is not None:
            output.unlink(missing_ok=True)
        raise
    finally:
        if writer is not None:
            writer.close()


def _has_triangle(graph: Graph) -> tuple[int, int, int] | None:
    for vertices in combinations(graph.vertices, 3):
        if all(graph.has_edge(*pair) for pair in combinations(vertices, 2)):
            return vertices
    return None


def _has_four_cycle(graph: Graph) -> tuple[int, int, int, int] | None:
    for first, second, third, fourth in combinations(graph.vertices, 4):
        candidates = (
            (first, second, third, fourth),
            (first, second, fourth, third),
            (first, third, second, fourth),
        )
        for cycle in candidates:
            if all(
                graph.has_edge(cycle[index], cycle[(index + 1) % 4])
                for index in range(4)
            ):
                return cycle
    return None


def _cycle_certificate_is_valid(
    graph: Graph,
    certificate: ImperfectionCertificate,
) -> bool:
    vertices = certificate.vertices
    length = len(vertices)
    if length < 5 or length % 2 == 0:
        return False
    for left_index in range(length):
        for right_index in range(left_index + 1, length):
            consecutive = (
                right_index == left_index + 1
                or (left_index == 0 and right_index == length - 1)
            )
            edge = graph.has_edge(
                vertices[left_index],
                vertices[right_index],
            )
            expected = consecutive
            if certificate.kind == "odd_antihole":
                expected = not expected
            if edge != expected:
                return False
    return True


def _canonical_cycle_order(
    graph: Graph,
    subset: tuple[int, ...],
    *,
    complement: bool,
) -> tuple[int, ...] | None:
    selected = frozenset(subset)

    def adjacent(first: int, second: int) -> bool:
        edge = graph.has_edge(first, second)
        return not edge if complement else edge

    neighborhoods = {
        vertex: tuple(
            other
            for other in subset
            if other != vertex and adjacent(vertex, other)
        )
        for vertex in subset
    }
    if any(len(neighbors) != 2 for neighbors in neighborhoods.values()):
        return None
    start = min(subset)
    second = min(neighborhoods[start])
    order = [start, second]
    previous, current = start, second
    while len(order) < len(selected):
        candidates = [
            vertex
            for vertex in neighborhoods[current]
            if vertex != previous
        ]
        if len(candidates) != 1:
            return None
        following = candidates[0]
        if following in order:
            return None
        order.append(following)
        previous, current = current, following
    if start not in neighborhoods[current]:
        return None
    result = tuple(order)
    if result[1] > result[-1]:
        result = (result[0],) + tuple(reversed(result[1:]))
    return result


def _first_imperfection_witness(
    graph: Graph,
) -> tuple[ImperfectionCertificate | None, int]:
    checked = 0
    for length in range(5, graph.order + 1, 2):
        for subset in combinations(graph.vertices, length):
            checked += 1
            cycle = _canonical_cycle_order(graph, subset, complement=False)
            if cycle is not None:
                return ImperfectionCertificate("odd_hole", cycle), checked
            anticycle = _canonical_cycle_order(
                graph,
                subset,
                complement=True,
            )
            if anticycle is not None:
                return (
                    ImperfectionCertificate("odd_antihole", anticycle),
                    checked,
                )
    return None, checked


def _minor_certificate_is_valid(
    graph: Graph,
    certificate: MinorCertificate,
) -> tuple[bool, str]:
    branches = certificate.branch_sets
    for index, branch in enumerate(branches):
        if not graph.is_connected(branch):
            return False, f"branch set {index} is disconnected"

    required_pairs: Iterator[tuple[int, int]]
    if certificate.kind == "K5":
        required_pairs = combinations(range(5), 2)
    elif certificate.kind == "K3,3":
        required_pairs = (
            (left, right)
            for left in range(3)
            for right in range(3, 6)
        )
    else:
        return False, "unknown minor type"

    for left, right in required_pairs:
        if not any(
            graph.has_edge(first, second)
            for first in branches[left]
            for second in branches[right]
        ):
            return (
                False,
                f"no edge joins required branch sets {left} and {right}",
            )
    return True, (
        f"valid {certificate.kind} minor model; nonplanar by Wagner's theorem"
    )


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def _classify_checks(
    checks: Mapping[str, Mapping[str, Any]],
) -> tuple[bool, bool, str, tuple[str, ...]]:
    """Keep definition-level validity separate from ancillary restrictions."""

    mathematical_counterexample_verified = all(
        bool(checks[name]["passed"]) for name in DEFINITION_LEVEL_CHECKS
    )
    consistency_names = tuple(
        name for name in checks if name not in DEFINITION_LEVEL_CHECKS
    )
    campaign_consistency_complete = (
        mathematical_counterexample_verified
        and all(bool(checks[name]["passed"]) for name in consistency_names)
    )
    if mathematical_counterexample_verified:
        status = (
            "VERIFIED_COUNTEREXAMPLE_CANDIDATE"
            if campaign_consistency_complete
            else "VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS"
        )
    else:
        status = "REJECTED_NO_COUNTEREXAMPLE_VERIFIED"
    return (
        mathematical_counterexample_verified,
        campaign_consistency_complete,
        status,
        consistency_names,
    )


def verify_candidate(
    candidate: Candidate,
    *,
    source_sha256: str | None = None,
    color_trace_path: str | Path | None = None,
) -> dict[str, Any]:
    """Recompute every decisive property and return a deterministic report."""

    graph = candidate.graph
    failures: list[str] = []
    checks: dict[str, dict[str, Any]] = {}

    def record(name: str, passed: bool, **details: Any) -> None:
        checks[name] = {"passed": bool(passed), **_jsonable(details)}
        if not passed and len(failures) < MAX_RECORDED_FAILURES:
            failures.append(name)

    computed_graph6 = graph.to_graph6()
    computed_graph_hash = graph6_sha256(computed_graph6)
    computed_edge_hash = sha256(canonical_edges_bytes(candidate.edges)).hexdigest()
    record(
        "graph_identity",
        candidate.graph6 == computed_graph6
        and candidate.graph6_sha256 == computed_graph_hash
        and candidate.edges_sha256 == computed_edge_hash,
        order=graph.order,
        size=len(candidate.edges),
        labeled_graph6=computed_graph6,
        graph6_sha256=computed_graph_hash,
        edges_sha256=computed_edge_hash,
        canonicalization_claimed=False,
    )

    connected = graph.is_connected()
    record("connected", connected)

    graph_anchor_ok = graph.is_independent(ANCHOR)
    anchor_ok = (
        candidate.independent_set == ANCHOR
        and graph_anchor_ok
    )
    record(
        "anchored_complement_K4",
        anchor_ok,
        anchor=ANCHOR,
        declared_independent_set=candidate.independent_set,
    )

    gamma, minimum_dominating = _first_dominating_set(graph)
    triple_violations = tuple(
        triple
        for triple in combinations(graph.vertices, 3)
        if graph.is_dominating(triple)
    )
    dominating_witness_ok = graph.is_dominating(candidate.dominating_set)
    record(
        "gamma_equals_4",
        gamma == K and dominating_witness_ok and not triple_violations,
        computed_gamma=gamma,
        first_minimum_dominating_set=minimum_dominating,
        declared_dominating_set=candidate.dominating_set,
        declared_set_dominates=dominating_witness_ok,
        triples_exhausted=220,
        dominating_triples=triple_violations[:8],
    )

    alpha, maximum_independent = _first_maximum_independent_set(graph)
    independent_five_sets = tuple(
        vertices
        for vertices in combinations(graph.vertices, 5)
        if graph.is_independent(vertices)
    )
    independent_witness_ok = graph.is_independent(candidate.independent_set)
    record(
        "alpha_equals_4",
        alpha == K and independent_witness_ok and not independent_five_sets,
        computed_alpha=alpha,
        first_maximum_independent_set=maximum_independent,
        declared_set_is_independent=independent_witness_ok,
        five_sets_exhausted=792,
        independent_five_sets=independent_five_sets[:8],
    )

    eternal = check_eternal_family(graph, candidate.eternal_family)
    record(
        "one_guard_eternal_family",
        eternal.passed,
        family_size=eternal.family_size,
        selected_states_checked=eternal.states_checked,
        unoccupied_attacks_checked=eternal.unoccupied_attacks_checked,
        occupied_attacks_excluded=eternal.occupied_attacks_excluded,
        legal_responses_counted=eternal.legal_responses_counted,
        chosen_response_sha256=eternal.chosen_response_sha256,
        independent_four_sets=eternal.independent_four_sets,
        forced_independent_states_missing=(
            eternal.forced_independent_states_missing[:8]
        ),
        failures=eternal.failures,
    )
    record(
        "independent_four_sets_forced_into_family",
        not eternal.forced_independent_states_missing,
        independent_four_sets=eternal.independent_four_sets,
        missing=eternal.forced_independent_states_missing[:8],
    )

    if graph_anchor_ok:
        color_search = anchored_four_color_search(
            graph,
            trace_path=color_trace_path,
        )
        record(
            "theta_at_least_5",
            color_search.proper_rows == 0,
            complement_color_count=4,
            anchor_normalized_rows_checked=color_search.rows_checked,
            proper_rows=color_search.proper_rows,
            first_proper_coloring=color_search.first_proper_coloring,
            trace_format=color_search.trace_format,
            trace_sha256=color_search.trace_sha256,
            trace_path=(
                str(Path(color_trace_path).resolve())
                if color_trace_path is not None
                else None
            ),
        )
    else:
        color_search = ColorSearch(
            performed=False,
            rows_checked=0,
            proper_rows=0,
            first_proper_coloring=None,
            trace_sha256=None,
            trace_format="GT4TRACE 1",
        )
        record(
            "theta_at_least_5",
            False,
            reason="anchor normalization is unavailable",
            anchor_normalized_rows_checked=0,
            trace_sha256=None,
        )

    maximal_sizes, maximal_count = _maximal_independent_profile(graph)
    independent_domination = min(maximal_sizes) if maximal_sizes else None
    well_covered = len(maximal_sizes) == 1 and maximal_sizes == (K,)
    record(
        "independent_domination_and_well_covered",
        independent_domination == K and well_covered,
        independent_domination=independent_domination,
        maximal_independent_set_sizes=maximal_sizes,
        maximal_independent_set_count=maximal_count,
        well_covered=well_covered,
        subsets_exhausted=1 << N,
    )

    triangle = _has_triangle(graph)
    record("contains_triangle", triangle is not None, witness=triangle)
    four_cycle = _has_four_cycle(graph)
    record("contains_4_cycle", four_cycle is not None, witness=four_cycle)
    degrees = tuple(len(graph.adjacency[vertex]) for vertex in graph.vertices)
    record(
        "maximum_degree_at_least_4",
        max(degrees) >= 4,
        degree_sequence=tuple(sorted(degrees, reverse=True)),
        maximum_degree=max(degrees),
    )

    minor_ok, minor_reason = _minor_certificate_is_valid(
        graph,
        candidate.nonplanarity_minor,
    )
    record(
        "nonplanar",
        minor_ok,
        certificate_kind=candidate.nonplanarity_minor.kind,
        branch_sets=candidate.nonplanarity_minor.branch_sets,
        reason=minor_reason,
        method="explicit Wagner minor model",
    )

    declared_imperfection_ok = _cycle_certificate_is_valid(
        graph,
        candidate.imperfection_witness,
    )
    discovered_imperfection, imperfection_subsets_checked = (
        _first_imperfection_witness(graph)
    )
    record(
        "induced_odd_hole_or_antihole",
        declared_imperfection_ok and discovered_imperfection is not None,
        declared_kind=candidate.imperfection_witness.kind,
        declared_vertices=candidate.imperfection_witness.vertices,
        declared_witness_valid=declared_imperfection_ok,
        first_independently_found=(
            {
                "kind": discovered_imperfection.kind,
                "vertices": discovered_imperfection.vertices,
            }
            if discovered_imperfection is not None
            else None
        ),
        subsets_checked=imperfection_subsets_checked,
        subset_universe_size=sum(
            1
            for length in range(5, N + 1, 2)
            for _ in combinations(range(N), length)
        ),
    )

    (
        mathematical_counterexample_verified,
        campaign_consistency_complete,
        status,
        consistency_names,
    ) = _classify_checks(checks)
    derived = {
        "gamma": gamma,
        "independent_domination": independent_domination,
        "alpha": alpha,
        "eternal_domination": (
            K
            if gamma == K and eternal.passed
            else None
        ),
        "theta_lower_bound": (
            K + 1
            if color_search.performed and color_search.proper_rows == 0
            else None
        ),
        "well_covered": well_covered,
    }
    return {
        "verifier": VERIFIER,
        "schema": SCHEMA,
        "status": status,
        "accepted": mathematical_counterexample_verified,
        "mathematical_counterexample_verified": (
            mathematical_counterexample_verified
        ),
        "campaign_consistency_complete": campaign_consistency_complete,
        "definition_level_checks": DEFINITION_LEVEL_CHECKS,
        "consistency_checks": consistency_names,
        "source_sha256": source_sha256,
        "checks": checks,
        "derived": derived,
        "failed_checks": failures,
        "claim_boundary": (
            "mathematical_counterexample_verified=true proves the supplied "
            "labeled graph satisfies "
            "gamma(G)=gamma^infinity(G)=4<theta(G) in the one-guard-moves "
            "model. Ancillary consistency alerts never erase that result. "
            "A negative result makes no nonexistence claim."
        ),
    }
