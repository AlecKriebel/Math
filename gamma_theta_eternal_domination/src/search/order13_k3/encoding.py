"""Deterministic exact CNF for the order-13, parameter-three frontier.

The graph represented by edge variables is ``H = complement(G)``.  The four
instances are an overlapping, exhaustive template cover *conditional on* the
mathematical order-13 reduction recorded in ``math/lemmas/order13_strategy.md``.

There are deliberately no heuristic symmetry breakers in this module.  In
particular, it contains no signature sorting, rim reflection, or DoubleLex
clauses.  The only fixed labels are those justified by the odd-hole template
and the external common neighbor of rim edge 01.
"""

from __future__ import annotations

import hashlib
from collections import OrderedDict
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations


N = 13
TEMPLATES = ("hole5", "hole7", "hole9", "hole11")
Pair = tuple[int, int]
Triple = tuple[int, int, int]

# Full-formula values reconstructed from the frozen exploratory bytes.  These
# constants are a fail-closed regression gate, not an assumption in generation.
EXPECTED_FORMULAS: Mapping[str, Mapping[str, int | str]] = {
    "hole5": {
        "variables": 9_802,
        "base_clauses": 29_791,
        "base_literals": 227_006,
        "coloring_rows": 10_935,
        "clauses": 40_726,
        "literals": 493_820,
        "size_bytes": 1_805_539,
        "sha256": "8df56270f1abf3a9a8e5d088a78680dcde0198292eaa51da78a7fce9179d2fb5",
    },
    "hole7": {
        "variables": 9_802,
        "base_clauses": 29_800,
        "base_literals": 227_019,
        "coloring_rows": 5_103,
        "clauses": 34_903,
        "literals": 349_248,
        "size_bytes": 1_372_338,
        "sha256": "3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340",
    },
    "hole9": {
        "variables": 9_802,
        "base_clauses": 29_813,
        "base_literals": 227_028,
        "coloring_rows": 2_295,
        "clauses": 32_108,
        "literals": 281_028,
        "size_bytes": 1_168_197,
        "sha256": "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
    },
    "hole11": {
        "variables": 9_802,
        "base_clauses": 29_830,
        "base_literals": 227_033,
        "coloring_rows": 1_023,
        "clauses": 30_853,
        "literals": 250_664,
        "size_bytes": 1_076_723,
        "sha256": "1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901",
    },
}


def _pair(first: int, second: int) -> Pair:
    if type(first) is not int or type(second) is not int:
        raise ValueError("edge endpoints must be exact integers")
    if first == second:
        raise ValueError("an edge needs distinct endpoints")
    if not (0 <= first < N and 0 <= second < N):
        raise ValueError("edge endpoint is outside the vertex set")
    return (first, second) if first < second else (second, first)


class CNF:
    """Deterministic DIMACS builder with clause-family accounting."""

    def __init__(self) -> None:
        self.variable_names: list[str] = [""]
        self.clauses: list[tuple[int, ...]] = []
        self._family_counts: OrderedDict[str, list[int]] = OrderedDict()
        self._family_hashes: OrderedDict[str, object] = OrderedDict()

    @property
    def variable_count(self) -> int:
        return len(self.variable_names) - 1

    @property
    def literal_count(self) -> int:
        return sum(map(len, self.clauses))

    @property
    def family_counts(self) -> Mapping[str, tuple[int, int]]:
        return OrderedDict(
            (name, (counts[0], counts[1]))
            for name, counts in self._family_counts.items()
        )

    @property
    def family_sha256(self) -> Mapping[str, str]:
        return OrderedDict(
            (name, digest.hexdigest())
            for name, digest in self._family_hashes.items()
        )

    def new_variable(self, name: str) -> int:
        if not name or "\n" in name:
            raise ValueError("invalid variable name")
        self.variable_names.append(name)
        return self.variable_count

    def add_clause(self, family: str, literals: Iterable[int]) -> None:
        if not family or "\n" in family:
            raise ValueError("invalid clause-family name")
        clause = tuple(int(literal) for literal in literals)
        if any(literal == 0 for literal in clause):
            raise ValueError("zero is not a literal inside a clause")
        if any(abs(literal) > self.variable_count for literal in clause):
            raise ValueError("clause refers to an unallocated variable")
        if len(set(clause)) != len(clause):
            raise ValueError("duplicate literal in clause")
        if any(-literal in clause for literal in clause):
            raise ValueError("tautological clause")
        self.clauses.append(clause)
        counts = self._family_counts.setdefault(family, [0, 0])
        counts[0] += 1
        counts[1] += len(clause)
        digest = self._family_hashes.setdefault(family, hashlib.sha256())
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))

    def dimacs_bytes(self) -> bytes:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return ("\n".join(lines) + "\n").encode("ascii")


@dataclass(frozen=True)
class K3Encoding:
    template: str
    cnf: CNF
    edge_variables: Mapping[Pair, int]
    witness_variables: Mapping[tuple[int, int, int], int]
    family_variables: Mapping[Triple, int]
    move_variables: Mapping[tuple[Triple, int, int], int]
    coloring_bank: tuple[tuple[int, ...], ...] = ()

    def edge(self, first: int, second: int) -> int:
        return self.edge_variables[_pair(first, second)]

    def decode_edges(self, model: Mapping[int, bool]) -> tuple[Pair, ...]:
        return tuple(
            pair
            for pair, variable in self.edge_variables.items()
            if model.get(variable, False)
        )

    def decode_family(self, model: Mapping[int, bool]) -> tuple[Triple, ...]:
        return tuple(
            state
            for state, variable in self.family_variables.items()
            if model.get(variable, False)
        )


def template_length(template: str) -> int:
    if template not in TEMPLATES:
        raise ValueError(f"unknown order-13 k=3 template {template!r}")
    return int(template.removeprefix("hole"))


def positive_template_edges(template: str) -> tuple[Pair, ...]:
    """Forced-true H-edges relevant to a proper coloring."""

    length = template_length(template)
    edges = {
        _pair(vertex, (vertex + 1) % length)
        for vertex in range(length)
    }
    # Vertex `length` is the named common neighbor of rim edge 01.
    edges.add((0, length))
    edges.add((1, length))
    return tuple(sorted(edges))


def first_use_canonical(row: Sequence[int]) -> tuple[int, ...]:
    """Validate a restricted-growth representation of a <=3-coloring."""

    if len(row) != N:
        raise ValueError(f"expected a {N}-vertex coloring")
    result: list[int] = []
    maximum = -1
    for index, color in enumerate(row):
        if type(color) is not int or color not in (0, 1, 2):
            raise ValueError(f"color {index} is not an exact integer in 0..2")
        if color > maximum + 1:
            raise ValueError("color row is not first-use canonical")
        result.append(color)
        maximum = max(maximum, color)
    return tuple(result)


def canonicalize_color_names(row: Sequence[int]) -> tuple[int, ...]:
    if len(row) != N or any(
        type(color) is not int or color not in (0, 1, 2)
        for color in row
    ):
        raise ValueError("malformed labeled three-color row")
    names: dict[int, int] = {}
    result: list[int] = []
    for color in row:
        if color not in names:
            names[color] = len(names)
        result.append(names[color])
    return tuple(result)


def row_is_template_proper(template: str, row: Sequence[int]) -> bool:
    if len(row) != N or any(
        type(color) is not int or color not in (0, 1, 2)
        for color in row
    ):
        raise ValueError("malformed three-color row")
    return all(
        row[first] != row[second]
        for first, second in positive_template_edges(template)
    )


def enumerate_coloring_bank(template: str) -> tuple[tuple[int, ...], ...]:
    """All template-compatible color partitions, in lexical order."""

    neighbors_before: list[list[int]] = [[] for _ in range(N)]
    for first, second in positive_template_edges(template):
        neighbors_before[second].append(first)
    rows: list[tuple[int, ...]] = []
    partial: list[int] = []

    def visit(vertex: int, maximum: int) -> None:
        if vertex == N:
            rows.append(tuple(partial))
            return
        upper = min(2, maximum + 1)
        for color in range(upper + 1):
            if any(
                partial[neighbor] == color
                for neighbor in neighbors_before[vertex]
            ):
                continue
            partial.append(color)
            visit(vertex + 1, max(maximum, color))
            partial.pop()

    visit(0, -1)
    return tuple(rows)


def same_color_cut(
    encoding: K3Encoding, coloring: Sequence[int]
) -> tuple[int, ...]:
    """Clause saying that ``coloring`` is not proper for H."""

    row = first_use_canonical(coloring)
    clause = tuple(
        encoding.edge(first, second)
        for first, second in combinations(range(N), 2)
        if row[first] == row[second]
    )
    if not clause:
        raise AssertionError("thirteen vertices in three classes have an equal pair")
    return clause


def build_base_encoding(template: str) -> K3Encoding:
    """Construct the audited graph and one-guard clauses, without color cuts."""

    template_length(template)
    cnf = CNF()
    vertices = range(N)
    triples = tuple(combinations(vertices, 3))

    edge_variables = {
        pair: cnf.new_variable(f"e_{pair[0]}_{pair[1]}")
        for pair in combinations(vertices, 2)
    }
    witness_variables = {
        (first, second, witness): cnf.new_variable(
            f"w_{first}_{second}_{witness}"
        )
        for first, second in combinations(vertices, 2)
        for witness in vertices
        if witness not in (first, second)
    }
    family_variables = {
        triple: cnf.new_variable("f_" + "_".join(map(str, triple)))
        for triple in triples
    }
    move_variables = {
        (triple, attacked, guard): cnf.new_variable(
            "m_"
            + "_".join(map(str, triple))
            + f"__{attacked}_{guard}"
        )
        for triple in triples
        for attacked in vertices
        if attacked not in triple
        for guard in triple
    }
    encoding = K3Encoding(
        template=template,
        cnf=cnf,
        edge_variables=edge_variables,
        witness_variables=witness_variables,
        family_variables=family_variables,
        move_variables=move_variables,
    )

    # alpha(G) <= 3, equivalently omega(H) <= 3.
    for four_set in combinations(vertices, 4):
        cnf.add_clause(
            "no_h_k4",
            (
                -encoding.edge(first, second)
                for first, second in combinations(four_set, 2)
            ),
        )

    # gamma(G) >= 3: every pair has a vertex nonadjacent in G to both.
    for first, second in combinations(vertices, 2):
        witnesses = tuple(
            witness
            for witness in vertices
            if witness not in (first, second)
        )
        cnf.add_clause(
            "pair_common_neighbor_choice",
            (
                witness_variables[(first, second, witness)]
                for witness in witnesses
            ),
        )
        for witness in witnesses:
            variable = witness_variables[(first, second, witness)]
            cnf.add_clause(
                "pair_common_neighbor_implication",
                (-variable, encoding.edge(first, witness)),
            )
            cnf.add_clause(
                "pair_common_neighbor_implication",
                (-variable, encoding.edge(second, witness)),
            )

    _add_template_clauses(encoding)

    # G connected: each proper cut with 0 on its named side has a G-edge.
    full = (1 << N) - 1
    for mask in range(1, full):
        if not mask & 1:
            continue
        cnf.add_clause(
            "g_connected_cut",
            (
                -encoding.edge(first, second)
                for first in vertices
                if mask >> first & 1
                for second in vertices
                if not (mask >> second & 1)
            ),
        )

    # Every selected family state dominates G.
    for triple in triples:
        selected = family_variables[triple]
        for outside in vertices:
            if outside in triple:
                continue
            cnf.add_clause(
                "selected_state_dominates",
                (
                    -selected,
                    -encoding.edge(outside, triple[0]),
                    -encoding.edge(outside, triple[1]),
                    -encoding.edge(outside, triple[2]),
                ),
            )

    # A nonempty family supplies gamma(G) <= 3 and is closed under every
    # unoccupied attack.  A response variable names one guard; multiple legal
    # replies may coexist, which is existentially harmless.
    cnf.add_clause("eternal_family_nonempty", family_variables.values())
    for triple in triples:
        selected = family_variables[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                move = move_variables[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(move)
                # A G-edge is an H-nonedge.
                cnf.add_clause(
                    "move_guard_adjacent_in_g",
                    (-move, -encoding.edge(guard, attacked)),
                )
                cnf.add_clause(
                    "move_successor_in_family",
                    (-move, family_variables[successor]),
                )
            cnf.add_clause(
                "selected_attack_has_response",
                (-selected, *responses),
            )

    # Redundant maximum-independent-state lemma: every H-triangle belongs to
    # any eternal 3-family.  This does not alter graph coverage.
    for triple in triples:
        cnf.add_clause(
            "h_triangle_forced_into_family",
            (
                -encoding.edge(triple[0], triple[1]),
                -encoding.edge(triple[0], triple[2]),
                -encoding.edge(triple[1], triple[2]),
                family_variables[triple],
            ),
        )
    return encoding


def _add_template_clauses(encoding: K3Encoding) -> None:
    length = template_length(encoding.template)
    rim = tuple(range(length))
    rim_edges = {
        _pair(vertex, (vertex + 1) % length)
        for vertex in rim
    }
    for first, second in combinations(rim, 2):
        variable = encoding.edge(first, second)
        encoding.cnf.add_clause(
            "induced_hole",
            (variable if (first, second) in rim_edges else -variable,),
        )

    # C-051 forbids a hub of this odd hole.
    for outside in range(length, N):
        encoding.cnf.add_clause(
            "hole_hub_free",
            (-encoding.edge(outside, rim_vertex) for rim_vertex in rim),
        )

    # Relabel an external common neighbor of rim edge 01 as vertex `length`.
    # Together with forced e_01, this fixes an H-triangle / independent
    # 3-set of G without an unrelated anchor.
    encoding.cnf.add_clause(
        "named_rim_edge_common_neighbor",
        (encoding.edge(0, length),),
    )
    encoding.cnf.add_clause(
        "named_rim_edge_common_neighbor",
        (encoding.edge(1, length),),
    )


def build_full_encoding(template: str) -> K3Encoding:
    """Append the complete coloring obstruction bank to the base formula."""

    base = build_base_encoding(template)
    bank = enumerate_coloring_bank(template)
    for row in bank:
        base.cnf.add_clause("complete_coloring_obstruction", same_color_cut(base, row))
    return K3Encoding(
        template=base.template,
        cnf=base.cnf,
        edge_variables=base.edge_variables,
        witness_variables=base.witness_variables,
        family_variables=base.family_variables,
        move_variables=base.move_variables,
        coloring_bank=bank,
    )


def _normalize_edges(edges: Iterable[Pair]) -> set[Pair]:
    result: set[Pair] = set()
    try:
        records = tuple(edges)
    except TypeError as error:
        raise ValueError("edges must be iterable") from error
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 2:
            raise ValueError("each edge must be a pair")
        normalized = _pair(record[0], record[1])
        if normalized in result:
            raise ValueError("duplicate edge")
        result.add(normalized)
    return result


def _normalize_family(family: Iterable[Triple]) -> set[Triple]:
    result: set[Triple] = set()
    try:
        records = tuple(family)
    except TypeError as error:
        raise ValueError("family must be iterable") from error
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 3:
            raise ValueError("each family state must be a triple")
        if any(type(vertex) is not int for vertex in record):
            raise ValueError("family vertices must be exact integers")
        normalized = tuple(sorted(record))
        if (
            len(set(normalized)) != 3
            or normalized[0] < 0
            or normalized[-1] >= N
        ):
            raise ValueError("malformed family triple")
        if normalized in result:
            raise ValueError("duplicate family state")
        result.add(normalized)
    return result


def _is_three_colorable(edge: Callable[[int, int], bool]) -> bool:
    """Independent direct backtracking check used only for decoded candidates."""

    degrees = [
        sum(edge(vertex, other) for other in range(N) if other != vertex)
        for vertex in range(N)
    ]
    colors = [-1] * N

    def visit(colored: int) -> bool:
        if colored == N:
            return True
        uncolored = [vertex for vertex in range(N) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in range(N)
                        if (
                            neighbor != item
                            and edge(item, neighbor)
                            and colors[neighbor] >= 0
                        )
                    }
                ),
                degrees[item],
                -item,
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in range(N)
            if (
                neighbor != vertex
                and edge(vertex, neighbor)
                and colors[neighbor] >= 0
            )
        }
        for color in range(3):
            if color in forbidden:
                continue
            colors[vertex] = color
            if visit(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return visit(0)


def validate_decoded_candidate(
    template: str,
    edges: Iterable[Pair],
    family: Iterable[Triple],
) -> None:
    """Validate graph/family semantics directly rather than by CNF replay.

    Success proves the full encoded target for the supplied H-edge set and
    family.  It does not prove that the four-template cover is exhaustive.
    """

    length = template_length(template)
    edge_set = _normalize_edges(edges)
    family_set = _normalize_family(family)
    if not family_set:
        raise ValueError("eternal family is empty")

    def h_edge(first: int, second: int) -> bool:
        return _pair(first, second) in edge_set

    if any(
        all(
            h_edge(first, second)
            for first, second in combinations(four_set, 2)
        )
        for four_set in combinations(range(N), 4)
    ):
        raise ValueError("H contains a four-clique")
    for first, second in combinations(range(N), 2):
        if not any(
            h_edge(first, witness) and h_edge(second, witness)
            for witness in range(N)
            if witness not in (first, second)
        ):
            raise ValueError("a pair has no external common H-neighbor")

    reached = {0}
    frontier = [0]
    while frontier:
        first = frontier.pop()
        for second in range(N):
            if second == first or second in reached:
                continue
            if not h_edge(first, second):
                reached.add(second)
                frontier.append(second)
    if len(reached) != N:
        raise ValueError("G is disconnected")

    rim_edges = {
        _pair(vertex, (vertex + 1) % length)
        for vertex in range(length)
    }
    for first, second in combinations(range(length), 2):
        if h_edge(first, second) != ((first, second) in rim_edges):
            raise ValueError("required induced H-hole is absent")
    for outside in range(length, N):
        if all(h_edge(outside, rim) for rim in range(length)):
            raise ValueError("required H-hole has an external hub")
    if not h_edge(0, length) or not h_edge(1, length):
        raise ValueError("named rim-edge common neighbor is absent")
    if _is_three_colorable(h_edge):
        raise ValueError("H is three-colorable")

    for state in family_set:
        for outside in range(N):
            if outside not in state and all(
                h_edge(outside, guard) for guard in state
            ):
                raise ValueError("selected state does not dominate G")
        for attacked in range(N):
            if attacked in state:
                continue
            if not any(
                not h_edge(guard, attacked)
                and tuple(sorted((set(state) - {guard}) | {attacked}))
                in family_set
                for guard in state
            ):
                raise ValueError("selected state has an undefended attack")
