"""Exact anchored CNF for the connected ``(n, k) = (12, 4)`` target.

The graph represented by the edge variables is ``H = complement(G)``.
The encoding is derived in
``math/lemmas/order12_k4_synthesis_target.md``.  It includes:

* ``gamma(G) = alpha(G) = 4`` through an anchored ``H``-clique, no
  ``H``-clique of order five, and an external common ``H``-neighbor for
  every triple;
* connectedness of ``G``;
* a nonempty one-guard-moves eternal family of four-sets;
* a complete anchor-normalized bank excluding every four-coloring of ``H``;
* an optional, proved outer-vertex signature ordering.

No SAT result is asserted by constructing this formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable, Iterable, Mapping, Sequence


N = 12
K = 4
ANCHOR = (0, 1, 2, 3)
OUTER = tuple(range(4, N))
Pair = tuple[int, int]
Triple = tuple[int, int, int]
Quadruple = tuple[int, int, int, int]


def _pair(first: int, second: int) -> Pair:
    if first == second:
        raise ValueError("an edge needs two distinct endpoints")
    return (first, second) if first < second else (second, first)


class CNF:
    """Deterministic DIMACS builder with a readable variable layout."""

    def __init__(self) -> None:
        self.variable_names: list[str] = [""]
        self.clauses: list[tuple[int, ...]] = []

    @property
    def variable_count(self) -> int:
        return len(self.variable_names) - 1

    @property
    def literal_count(self) -> int:
        return sum(len(clause) for clause in self.clauses)

    def new_variable(self, name: str) -> int:
        if not name or "\n" in name or "\r" in name:
            raise ValueError("invalid variable name")
        self.variable_names.append(name)
        return self.variable_count

    def add_clause(self, literals: Iterable[int]) -> None:
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

    def dimacs_bytes(self) -> bytes:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(
            " ".join(map(str, clause)) + " 0" for clause in self.clauses
        )
        return ("\n".join(lines) + "\n").encode("ascii")


@dataclass(frozen=True)
class ClauseFamily:
    name: str
    first_clause: int
    clause_count: int
    literal_count: int


@dataclass(frozen=True)
class K4Encoding:
    cnf: CNF
    edge_variables: Mapping[Pair, int]
    witness_variables: Mapping[tuple[Triple, int], int]
    family_variables: Mapping[Quadruple, int]
    move_variables: Mapping[tuple[Quadruple, int, int], int]
    clause_families: tuple[ClauseFamily, ...]
    include_coloring_bank: bool
    include_signature_breaker: bool

    def edge(self, first: int, second: int) -> int:
        return self.edge_variables[_pair(first, second)]

    def decode_edges(self, model: Mapping[int, bool]) -> tuple[Pair, ...]:
        return tuple(
            pair
            for pair, variable in self.edge_variables.items()
            if model.get(variable, False)
        )

    def decode_family(
        self, model: Mapping[int, bool]
    ) -> tuple[Quadruple, ...]:
        return tuple(
            state
            for state, variable in self.family_variables.items()
            if model.get(variable, False)
        )


class _FamilyRecorder:
    def __init__(self, cnf: CNF) -> None:
        self.cnf = cnf
        self.records: list[ClauseFamily] = []

    def add(self, name: str, action: Callable[[], None]) -> None:
        first = len(self.cnf.clauses)
        literals = self.cnf.literal_count
        action()
        self.records.append(
            ClauseFamily(
                name=name,
                first_clause=first,
                clause_count=len(self.cnf.clauses) - first,
                literal_count=self.cnf.literal_count - literals,
            )
        )


def build_k4_encoding(
    *,
    include_coloring_bank: bool = True,
    include_signature_breaker: bool = True,
) -> K4Encoding:
    """Build the exact connected, anchored order-12 parameter-four CNF."""

    if include_signature_breaker and not include_coloring_bank:
        # The breaker is also sound for the base formula, but this guard keeps
        # the three public formula modes unambiguous: base, bank, and full.
        raise ValueError("signature breaker requires the complete coloring bank")

    cnf = CNF()
    vertices = tuple(range(N))
    triples = tuple(combinations(vertices, 3))
    states = tuple(combinations(vertices, K))

    edge_variables = {
        pair: cnf.new_variable(f"e_{pair[0]}_{pair[1]}")
        for pair in combinations(vertices, 2)
    }
    witness_variables = {
        (triple, witness): cnf.new_variable(
            "w_" + "_".join(map(str, triple)) + f"__{witness}"
        )
        for triple in triples
        for witness in vertices
        if witness not in triple
    }
    family_variables = {
        state: cnf.new_variable("f_" + "_".join(map(str, state)))
        for state in states
    }
    move_variables = {
        (state, attacked, guard): cnf.new_variable(
            "m_"
            + "_".join(map(str, state))
            + f"__{attacked}_{guard}"
        )
        for state in states
        for attacked in vertices
        if attacked not in state
        for guard in state
    }

    shell = K4Encoding(
        cnf=cnf,
        edge_variables=edge_variables,
        witness_variables=witness_variables,
        family_variables=family_variables,
        move_variables=move_variables,
        clause_families=(),
        include_coloring_bank=include_coloring_bank,
        include_signature_breaker=include_signature_breaker,
    )
    recorder = _FamilyRecorder(cnf)

    def no_k5() -> None:
        for five_set in combinations(vertices, 5):
            cnf.add_clause(
                -shell.edge(first, second)
                for first, second in combinations(five_set, 2)
            )

    recorder.add("no_k5", no_k5)

    def witness_existence() -> None:
        for triple in triples:
            cnf.add_clause(
                witness_variables[(triple, witness)]
                for witness in vertices
                if witness not in triple
            )

    recorder.add("triple_witness_existence", witness_existence)

    def witness_implications() -> None:
        for triple in triples:
            for witness in vertices:
                if witness in triple:
                    continue
                variable = witness_variables[(triple, witness)]
                for vertex in triple:
                    cnf.add_clause((-variable, shell.edge(vertex, witness)))

    recorder.add("triple_witness_implications", witness_implications)

    def anchor_units() -> None:
        for first, second in combinations(ANCHOR, 2):
            cnf.add_clause((shell.edge(first, second),))

    recorder.add("anchored_k4", anchor_units)

    def connected_cuts() -> None:
        full = (1 << N) - 1
        for mask in range(1, full):
            if not mask & 1:
                continue
            cnf.add_clause(
                -shell.edge(first, second)
                for first in vertices
                if mask >> first & 1
                for second in vertices
                if not (mask >> second & 1)
            )

    recorder.add("connected_g_cuts", connected_cuts)

    def selected_state_domination() -> None:
        for state in states:
            selected = family_variables[state]
            for outside in vertices:
                if outside in state:
                    continue
                cnf.add_clause(
                    (-selected,)
                    + tuple(-shell.edge(guard, outside) for guard in state)
                )

    recorder.add("selected_state_domination", selected_state_domination)

    recorder.add(
        "family_nonempty",
        lambda: cnf.add_clause(family_variables.values()),
    )

    def move_implications() -> None:
        for state in states:
            for attacked in vertices:
                if attacked in state:
                    continue
                for guard in state:
                    move = move_variables[(state, attacked, guard)]
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    cnf.add_clause((-move, -shell.edge(guard, attacked)))
                    cnf.add_clause((-move, family_variables[successor]))

    recorder.add("move_edge_and_successor", move_implications)

    def attack_responses() -> None:
        for state in states:
            selected = family_variables[state]
            for attacked in vertices:
                if attacked in state:
                    continue
                cnf.add_clause(
                    (-selected,)
                    + tuple(
                        move_variables[(state, attacked, guard)]
                        for guard in state
                    )
                )

    recorder.add("attack_response_disjunctions", attack_responses)

    def force_independent_states() -> None:
        for state in states:
            cnf.add_clause(
                tuple(
                    -shell.edge(first, second)
                    for first, second in combinations(state, 2)
                )
                + (family_variables[state],)
            )

    recorder.add("h_k4_to_family", force_independent_states)

    if include_coloring_bank:
        def coloring_bank() -> None:
            for outer_colors in product(range(K), repeat=len(OUTER)):
                coloring = ANCHOR + outer_colors
                cnf.add_clause(normalized_four_color_clause(shell, coloring))

        recorder.add("complete_anchored_four_color_bank", coloring_bank)

    if include_signature_breaker:
        def signature_breaker() -> None:
            for left, right in zip(OUTER[:-1], OUTER[1:], strict=True):
                for clause in signature_comparator_clauses(shell, left, right):
                    cnf.add_clause(clause)

        recorder.add("outer_signature_order", signature_breaker)

    return K4Encoding(
        cnf=cnf,
        edge_variables=edge_variables,
        witness_variables=witness_variables,
        family_variables=family_variables,
        move_variables=move_variables,
        clause_families=tuple(recorder.records),
        include_coloring_bank=include_coloring_bank,
        include_signature_breaker=include_signature_breaker,
    )


def normalized_four_color_clause(
    encoding: K4Encoding, coloring: Sequence[int]
) -> tuple[int, ...]:
    """Exclude one four-color assignment with anchor colors ``0,1,2,3``."""

    if len(coloring) != N:
        raise ValueError(f"expected {N} colors")
    if tuple(coloring[:K]) != ANCHOR:
        raise ValueError("anchor colors must be exactly 0,1,2,3")
    if any(type(color) is not int or not 0 <= color < K for color in coloring):
        raise ValueError("colors must be exact integers in 0,1,2,3")
    clause = tuple(
        encoding.edge(first, second)
        for first, second in combinations(range(N), 2)
        if coloring[first] == coloring[second]
    )
    if not clause:
        raise ValueError("a 12-vertex four-coloring has no equal-color pair")
    return clause


def signature_comparator_clauses(
    encoding: K4Encoding, left: int, right: int
) -> tuple[tuple[int, ...], ...]:
    """Encode ``s(left) <=lex s(right)`` without auxiliary variables."""

    if left not in OUTER or right not in OUTER or left == right:
        raise ValueError("signature vertices must be distinct outer vertices")
    result: list[tuple[int, ...]] = []
    for first_difference in range(K):
        for prefix in product((0, 1), repeat=first_difference):
            literals: list[int] = []
            for coordinate, bit in enumerate(prefix):
                left_edge = encoding.edge(ANCHOR[coordinate], left)
                right_edge = encoding.edge(ANCHOR[coordinate], right)
                if bit == 0:
                    literals.extend((left_edge, right_edge))
                else:
                    literals.extend((-left_edge, -right_edge))
            literals.extend(
                (
                    -encoding.edge(ANCHOR[first_difference], left),
                    encoding.edge(ANCHOR[first_difference], right),
                )
            )
            result.append(tuple(literals))
    return tuple(result)


def clause_is_true(
    clause: Sequence[int], assignment: Mapping[int, bool]
) -> bool:
    """Evaluate a clause under a total assignment; useful for truth-table tests."""

    for literal in clause:
        if abs(literal) not in assignment:
            raise ValueError(f"missing variable {abs(literal)}")
        value = assignment[abs(literal)]
        if type(value) is not bool:
            raise ValueError("assignment values must be booleans")
        if value == (literal > 0):
            return True
    return False


def validate_decoded_candidate(
    encoding: K4Encoding,
    edges: Iterable[Pair],
    family: Iterable[Quadruple],
) -> None:
    """Check the decoded target semantics without replaying the CNF core."""

    edge_set: set[Pair] = set()
    for record in tuple(edges):
        if not isinstance(record, (tuple, list)) or len(record) != 2:
            raise ValueError("each edge must be a pair")
        first, second = record
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < N
            or not 0 <= second < N
            or first == second
        ):
            raise ValueError("malformed simple-graph edge")
        normalized = _pair(first, second)
        if normalized in edge_set:
            raise ValueError("duplicate edge")
        edge_set.add(normalized)

    family_set: set[Quadruple] = set()
    for record in tuple(family):
        if not isinstance(record, (tuple, list)) or len(record) != K:
            raise ValueError("each family state must be a four-set")
        if any(type(vertex) is not int for vertex in record):
            raise ValueError("family vertices must be exact integers")
        normalized = tuple(sorted(record))
        if (
            len(set(normalized)) != K
            or normalized[0] < 0
            or normalized[-1] >= N
        ):
            raise ValueError("malformed family four-set")
        if normalized in family_set:
            raise ValueError("duplicate family state")
        family_set.add(normalized)
    if not family_set:
        raise ValueError("the eternal family is empty")

    def h_edge(first: int, second: int) -> bool:
        return _pair(first, second) in edge_set

    if not all(h_edge(first, second) for first, second in combinations(ANCHOR, 2)):
        raise ValueError("the anchored H-K4 is absent")
    if any(
        all(h_edge(first, second) for first, second in combinations(group, 2))
        for group in combinations(range(N), 5)
    ):
        raise ValueError("H contains a five-clique")
    for triple in combinations(range(N), 3):
        if not any(
            all(h_edge(vertex, witness) for vertex in triple)
            for witness in range(N)
            if witness not in triple
        ):
            raise ValueError("an H-triple has no external common neighbor")

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

    for state in family_set:
        for outside in range(N):
            if outside not in state and all(
                h_edge(guard, outside) for guard in state
            ):
                raise ValueError("a selected state does not dominate G")
        for attacked in range(N):
            if attacked in state:
                continue
            if not any(
                not h_edge(guard, attacked)
                and tuple(sorted((set(state) - {guard}) | {attacked}))
                in family_set
                for guard in state
            ):
                raise ValueError("a selected state has an undefended attack")

    for state in combinations(range(N), K):
        if all(h_edge(first, second) for first, second in combinations(state, 2)):
            if state not in family_set:
                raise ValueError("an independent four-set is missing from the family")

    if has_anchor_normalized_four_coloring(edge_set):
        raise ValueError("H has an anchor-normalized proper four-coloring")


def has_anchor_normalized_four_coloring(edges: Iterable[Pair]) -> bool:
    """Return whether ``H`` has a proper coloring fixing the anchor colors."""

    edge_set = {_pair(first, second) for first, second in edges}
    colors = [-1] * N
    colors[:K] = ANCHOR

    def search(vertex: int) -> bool:
        if vertex == N:
            return True
        for color in range(K):
            if all(
                colors[neighbor] != color
                for neighbor in range(vertex)
                if _pair(vertex, neighbor) in edge_set
            ):
                colors[vertex] = color
                if search(vertex + 1):
                    return True
        colors[vertex] = -1
        return False

    return search(K)
