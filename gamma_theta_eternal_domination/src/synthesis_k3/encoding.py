"""Exact CNF encoding for the order-12, parameter-three synthesis target.

The encoded graph is ``H = complement(G)``.  Edge variables come first so a
SAT model can be decoded without importing either eternal-domination
evaluator.  The clauses implement the mathematical design in
``math/synthesis_k3_cegar_design.md``.

Non-three-colorability is intentionally absent from the base formula.  It is
added by CEGAR through :func:`same_color_cut`; every such clause is a necessary
condition for a graph not to admit the recorded coloring.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from collections.abc import Callable
from typing import Iterable, Mapping, Sequence


N = 12
TEMPLATES = ("hole5", "hole7", "hole9", "antihole7")
Triple = tuple[int, int, int]
Pair = tuple[int, int]


def _pair(first: int, second: int) -> Pair:
    if first == second:
        raise ValueError("an edge needs two distinct endpoints")
    return (first, second) if first < second else (second, first)


class CNF:
    """Small deterministic DIMACS builder with a human-readable variable map."""

    def __init__(self) -> None:
        self.variable_names: list[str] = [""]
        self.clauses: list[tuple[int, ...]] = []

    @property
    def variable_count(self) -> int:
        return len(self.variable_names) - 1

    def new_variable(self, name: str) -> int:
        if not name or "\n" in name:
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

    def dimacs(self) -> str:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class K3Encoding:
    template: str
    cnf: CNF
    edge_variables: Mapping[Pair, int]
    witness_variables: Mapping[tuple[int, int, int], int]
    family_variables: Mapping[Triple, int]
    move_variables: Mapping[tuple[Triple, int, int], int]

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
            triple
            for triple, variable in self.family_variables.items()
            if model.get(variable, False)
        )


def build_k3_encoding(template: str) -> K3Encoding:
    """Build one of the four proved order-12 SPGT template instances."""

    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template!r}")

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

    # omega(H) <= 3.
    for four_set in combinations(vertices, 4):
        cnf.add_clause(
            -encoding.edge(first, second)
            for first, second in combinations(four_set, 2)
        )

    # Every pair has an external common neighbor in H, equivalently no
    # two-set dominates G.
    for first, second in combinations(vertices, 2):
        witnesses = [
            witness
            for witness in vertices
            if witness not in (first, second)
        ]
        cnf.add_clause(
            witness_variables[(first, second, witness)]
            for witness in witnesses
        )
        for witness in witnesses:
            variable = witness_variables[(first, second, witness)]
            cnf.add_clause((-variable, encoding.edge(first, witness)))
            cnf.add_clause((-variable, encoding.edge(second, witness)))

    _add_template_clauses(encoding)

    # G is connected: every proper cut containing vertex 0 has a G-edge,
    # which is a nonedge of H.
    full = (1 << N) - 1
    for mask in range(1, full):
        if not mask & 1:
            continue
        cnf.add_clause(
            -encoding.edge(first, second)
            for first in vertices
            if mask >> first & 1
            for second in vertices
            if not (mask >> second & 1)
        )

    # Selected family states dominate G.
    for triple in triples:
        family_variable = family_variables[triple]
        for outside in vertices:
            if outside in triple:
                continue
            cnf.add_clause(
                (
                    -family_variable,
                    -encoding.edge(outside, triple[0]),
                    -encoding.edge(outside, triple[1]),
                    -encoding.edge(outside, triple[2]),
                )
            )

    # The selected family is nonempty and is closed under every unoccupied
    # attack by exactly one legal guard move.
    cnf.add_clause(family_variables.values())
    for triple in triples:
        family_variable = family_variables[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            response_variables: list[int] = []
            for guard in triple:
                move_variable = move_variables[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                response_variables.append(move_variable)
                cnf.add_clause(
                    (-move_variable, -encoding.edge(guard, attacked))
                )
                cnf.add_clause(
                    (-move_variable, family_variables[successor])
                )
            cnf.add_clause((-family_variable, *response_variables))

    # Every maximum independent triple of G (triangle of H) must occur in
    # every eternal three-family. This is redundant but sound strengthening.
    for triple in triples:
        cnf.add_clause(
            (
                -encoding.edge(triple[0], triple[1]),
                -encoding.edge(triple[0], triple[2]),
                -encoding.edge(triple[1], triple[2]),
                family_variables[triple],
            )
        )

    return encoding


def _add_template_clauses(encoding: K3Encoding) -> None:
    cnf = encoding.cnf
    template = encoding.template

    if template.startswith("hole"):
        length = int(template[4:])
        rim = tuple(range(length))
        rim_edges = {
            _pair(vertex, (vertex + 1) % length) for vertex in rim
        }
        for first, second in combinations(rim, 2):
            variable = encoding.edge(first, second)
            cnf.add_clause((variable if (first, second) in rim_edges else -variable,))

        # No external vertex is a hub of the induced odd hole.
        for outside in range(length, N):
            cnf.add_clause(-encoding.edge(outside, rim_vertex) for rim_vertex in rim)

        # By the common-neighbor condition, rim edge 01 has a common neighbor
        # outside the induced cycle. Relabel one such vertex as `length`.
        common_neighbor = length
        cnf.add_clause((encoding.edge(0, common_neighbor),))
        cnf.add_clause((encoding.edge(1, common_neighbor),))
        return

    if template == "antihole7":
        rim = tuple(range(7))
        cycle_edges = {
            _pair(vertex, (vertex + 1) % 7) for vertex in rim
        }
        for first, second in combinations(rim, 2):
            variable = encoding.edge(first, second)
            # Force the complement of an induced C7.
            cnf.add_clause((-variable if (first, second) in cycle_edges else variable,))
        return

    raise AssertionError("template validation should make this unreachable")


def same_color_cut(
    encoding: K3Encoding, coloring: Sequence[int]
) -> tuple[int, ...]:
    """Return the valid CEGAR clause excluding one proposed 3-coloring."""

    if len(coloring) != N:
        raise ValueError(f"expected {N} colors")
    if any(type(color) is not int or color not in (0, 1, 2) for color in coloring):
        raise ValueError("colors must be the integers 0, 1, or 2")
    clause = tuple(
        encoding.edge(first, second)
        for first, second in combinations(range(N), 2)
        if coloring[first] == coloring[second]
    )
    if not clause:
        raise ValueError("a 12-vertex three-color assignment has no equal pair")
    return clause


def validate_decoded_candidate(
    encoding: K3Encoding,
    edges: Iterable[Pair],
    family: Iterable[Triple],
) -> None:
    """Check the graph/family semantics directly, without replaying CNF."""

    edge_set: set[Pair] = set()
    try:
        edge_records = tuple(edges)
    except TypeError as error:
        raise ValueError("edges must be iterable") from error
    for record in edge_records:
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

    family_set: set[Triple] = set()
    try:
        family_records = tuple(family)
    except TypeError as error:
        raise ValueError("family must be iterable") from error
    for record in family_records:
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
        if normalized in family_set:
            raise ValueError("duplicate family triple")
        family_set.add(normalized)

    if not family_set:
        raise ValueError("the eternal family is empty")

    def h_edge(first: int, second: int) -> bool:
        return _pair(first, second) in edge_set

    if any(
        all(h_edge(first, second) for first, second in combinations(four_set, 2))
        for four_set in combinations(range(N), 4)
    ):
        raise ValueError("H contains a four-clique")

    for first, second in combinations(range(N), 2):
        if not any(
            h_edge(first, witness) and h_edge(second, witness)
            for witness in range(N)
            if witness not in (first, second)
        ):
            raise ValueError("a pair of H has no external common neighbor")

    # Direct connectivity check in G.
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

    for triple in family_set:
        for outside in range(N):
            if outside in triple:
                continue
            if all(h_edge(outside, guard) for guard in triple):
                raise ValueError("a selected state does not dominate G")
        for attacked in range(N):
            if attacked in triple:
                continue
            if not any(
                not h_edge(guard, attacked)
                and tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                in family_set
                for guard in triple
            ):
                raise ValueError("a selected state has an undefended attack")

    _validate_template(encoding.template, h_edge)


def _validate_template(
    template: str, h_edge: Callable[[int, int], bool]
) -> None:
    edge = h_edge
    if template.startswith("hole"):
        length = int(template[4:])
        rim_edges = {
            _pair(vertex, (vertex + 1) % length) for vertex in range(length)
        }
        for first, second in combinations(range(length), 2):
            if bool(edge(first, second)) != ((first, second) in rim_edges):
                raise ValueError("the required induced odd hole is absent")
        for outside in range(length, N):
            if all(edge(outside, rim) for rim in range(length)):
                raise ValueError("the required hole has an external hub")
        if not edge(0, length) or not edge(1, length):
            raise ValueError("the labeled rim-edge common neighbor is absent")
        return

    if template == "antihole7":
        cycle_edges = {
            _pair(vertex, (vertex + 1) % 7) for vertex in range(7)
        }
        for first, second in combinations(range(7), 2):
            if bool(edge(first, second)) == ((first, second) in cycle_edges):
                raise ValueError("the required induced complement-C7 is absent")
        return

    raise ValueError(f"unknown template {template!r}")
