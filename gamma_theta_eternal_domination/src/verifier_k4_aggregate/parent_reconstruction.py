"""Clean-room reconstruction of the frozen order-12, parameter-four parent.

This module is deliberately independent of ``search``, ``synthesis_k3``, and
``synthesis_k4``.  It allocates every semantic variable and emits every clause
family directly from the mathematical specification.  The aggregate verifier
uses the resulting bytes rather than treating a retained parent hash as a
substitute for reconstruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product
from typing import Iterable, Sequence


N = 12
K = 4
VERTICES = tuple(range(N))
ANCHOR = (0, 1, 2, 3)
OUTER = tuple(range(4, N))

Pair = tuple[int, int]
Triple = tuple[int, int, int]
State = tuple[int, int, int, int]
Clause = tuple[int, ...]

EXPECTED_VARIABLE_COUNT = 18_381
EXPECTED_CLAUSE_COUNT = 114_742
EXPECTED_LITERAL_COUNT = 1_180_016
EXPECTED_SIZE_BYTES = 3_992_947
EXPECTED_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)

EXPECTED_FAMILIES = (
    ("no_k5", 0, 792, 7_920),
    ("triple_witness_existence", 792, 220, 1_980),
    ("triple_witness_implications", 1_012, 5_940, 11_880),
    ("anchored_k4", 6_952, 6, 6),
    ("connected_g_cuts", 6_958, 2_047, 67_584),
    ("selected_state_domination", 9_005, 3_960, 19_800),
    ("family_nonempty", 12_965, 1, 495),
    ("move_edge_and_successor", 12_966, 31_680, 63_360),
    ("attack_response_disjunctions", 44_646, 3_960, 19_800),
    ("h_k4_to_family", 48_606, 495, 3_465),
    ("complete_anchored_four_color_bank", 49_101, 65_536, 983_040),
    ("outer_signature_order", 114_637, 105, 686),
)


@dataclass(frozen=True, slots=True)
class ClauseFamily:
    name: str
    first_clause_zero_based: int
    clause_count: int
    literal_count: int


@dataclass(frozen=True, slots=True)
class ParentReconstruction:
    payload: bytes
    variable_count: int
    clause_count: int
    literal_count: int
    cube_variables: tuple[int, int, int, int]
    cube_labels: tuple[str, str, str, str]
    clause_families: tuple[ClauseFamily, ...]


def _pair(first: int, second: int) -> Pair:
    if first == second:
        raise AssertionError("loop in clean-room edge map")
    return (first, second) if first < second else (second, first)


class _VariableMap:
    """Independent deterministic allocation of the four semantic families."""

    def __init__(self) -> None:
        self.next_variable = 1
        self.edges = self._allocate(combinations(VERTICES, 2))
        self.triples = tuple(combinations(VERTICES, 3))
        self.states = tuple(combinations(VERTICES, 4))
        self.witnesses = self._allocate(
            (triple, witness)
            for triple in self.triples
            for witness in VERTICES
            if witness not in triple
        )
        self.family = self._allocate(self.states)
        self.moves = self._allocate(
            (state, attacked, guard)
            for state in self.states
            for attacked in VERTICES
            if attacked not in state
            for guard in state
        )
        if self.next_variable - 1 != EXPECTED_VARIABLE_COUNT:
            raise AssertionError("clean-room variable census changed")

    def _allocate(self, keys: Iterable[object]) -> dict[object, int]:
        result: dict[object, int] = {}
        for key in keys:
            if key in result:
                raise AssertionError("duplicate semantic variable key")
            result[key] = self.next_variable
            self.next_variable += 1
        return result

    def edge(self, first: int, second: int) -> int:
        return self.edges[_pair(first, second)]


class _Emitter:
    def __init__(self, variable_count: int, clause_count: int) -> None:
        self.payload = bytearray(
            f"p cnf {variable_count} {clause_count}\n".encode("ascii")
        )
        self.clause_count = 0
        self.literal_count = 0
        self.families: list[ClauseFamily] = []

    def family(self, name: str, clauses: Iterable[Sequence[int]]) -> None:
        first_clause = self.clause_count
        first_literal = self.literal_count
        for clause_like in clauses:
            clause = tuple(int(literal) for literal in clause_like)
            if not clause:
                raise AssertionError(f"empty generated clause in {name}")
            if 0 in clause:
                raise AssertionError(f"internal zero in {name}")
            if len(set(clause)) != len(clause):
                raise AssertionError(f"duplicate literal in {name}")
            if any(-literal in clause for literal in clause):
                raise AssertionError(f"tautology in {name}")
            self.payload.extend(" ".join(map(str, clause)).encode("ascii"))
            self.payload.extend(b" 0\n")
            self.clause_count += 1
            self.literal_count += len(clause)
        self.families.append(
            ClauseFamily(
                name=name,
                first_clause_zero_based=first_clause,
                clause_count=self.clause_count - first_clause,
                literal_count=self.literal_count - first_literal,
            )
        )


@lru_cache(maxsize=1)
def reconstruct_parent() -> ParentReconstruction:
    """Return the exact parent bytes from an independent semantic construction."""

    variables = _VariableMap()
    emitter = _Emitter(EXPECTED_VARIABLE_COUNT, EXPECTED_CLAUSE_COUNT)

    emitter.family(
        "no_k5",
        (
            tuple(-variables.edges[pair] for pair in combinations(five, 2))
            for five in combinations(VERTICES, 5)
        ),
    )
    emitter.family(
        "triple_witness_existence",
        (
            tuple(
                variables.witnesses[triple, witness]
                for witness in VERTICES
                if witness not in triple
            )
            for triple in variables.triples
        ),
    )

    def witness_implications() -> Iterable[Clause]:
        for triple in variables.triples:
            for witness in VERTICES:
                if witness in triple:
                    continue
                witness_variable = variables.witnesses[triple, witness]
                for vertex in triple:
                    yield (-witness_variable, variables.edge(vertex, witness))

    emitter.family("triple_witness_implications", witness_implications())
    emitter.family(
        "anchored_k4",
        ((variables.edges[pair],) for pair in combinations(ANCHOR, 2)),
    )

    def connected_cuts() -> Iterable[Clause]:
        full = (1 << N) - 1
        for mask in range(1, full):
            if not mask & 1:
                continue
            yield tuple(
                -variables.edge(first, second)
                for first in VERTICES
                if mask >> first & 1
                for second in VERTICES
                if not mask >> second & 1
            )

    emitter.family("connected_g_cuts", connected_cuts())

    def domination_clauses() -> Iterable[Clause]:
        for state in variables.states:
            for outside in VERTICES:
                if outside not in state:
                    yield (
                        -variables.family[state],
                        *(-variables.edge(guard, outside) for guard in state),
                    )

    emitter.family("selected_state_domination", domination_clauses())
    emitter.family("family_nonempty", (tuple(variables.family.values()),))

    def move_implications() -> Iterable[Clause]:
        for state in variables.states:
            for attacked in VERTICES:
                if attacked in state:
                    continue
                for guard in state:
                    move = variables.moves[state, attacked, guard]
                    successor = tuple(
                        sorted(
                            [vertex for vertex in state if vertex != guard]
                            + [attacked]
                        )
                    )
                    yield (-move, -variables.edge(guard, attacked))
                    yield (-move, variables.family[successor])

    emitter.family("move_edge_and_successor", move_implications())

    def attack_responses() -> Iterable[Clause]:
        for state in variables.states:
            for attacked in VERTICES:
                if attacked not in state:
                    yield (
                        -variables.family[state],
                        *(
                            variables.moves[state, attacked, guard]
                            for guard in state
                        ),
                    )

    emitter.family("attack_response_disjunctions", attack_responses())
    emitter.family(
        "h_k4_to_family",
        (
            (
                *(-variables.edges[pair] for pair in combinations(state, 2)),
                variables.family[state],
            )
            for state in variables.states
        ),
    )
    emitter.family(
        "complete_anchored_four_color_bank",
        (
            tuple(
                variables.edge(first, second)
                for first, second in combinations(VERTICES, 2)
                if coloring[first] == coloring[second]
            )
            for coloring in (
                ANCHOR + outer_colors
                for outer_colors in product(range(K), repeat=len(OUTER))
            )
        ),
    )

    def sorter_clauses() -> Iterable[Clause]:
        for left, right in zip(OUTER[:-1], OUTER[1:], strict=True):
            for first_difference in range(K):
                for prefix in product((0, 1), repeat=first_difference):
                    literals: list[int] = []
                    for coordinate, bit in enumerate(prefix):
                        left_edge = variables.edge(ANCHOR[coordinate], left)
                        right_edge = variables.edge(ANCHOR[coordinate], right)
                        if bit == 0:
                            literals.extend((left_edge, right_edge))
                        else:
                            literals.extend((-left_edge, -right_edge))
                    literals.extend(
                        (
                            -variables.edge(
                                ANCHOR[first_difference], left
                            ),
                            variables.edge(
                                ANCHOR[first_difference], right
                            ),
                        )
                    )
                    yield tuple(literals)

    emitter.family("outer_signature_order", sorter_clauses())

    families = tuple(emitter.families)
    observed = tuple(
        (
            family.name,
            family.first_clause_zero_based,
            family.clause_count,
            family.literal_count,
        )
        for family in families
    )
    if observed != EXPECTED_FAMILIES:
        raise AssertionError(f"clean-room clause-family census changed: {observed}")
    if (
        emitter.clause_count != EXPECTED_CLAUSE_COUNT
        or emitter.literal_count != EXPECTED_LITERAL_COUNT
    ):
        raise AssertionError("clean-room parent census changed")
    payload = bytes(emitter.payload)
    if len(payload) != EXPECTED_SIZE_BYTES:
        raise AssertionError("clean-room parent byte size changed")

    cube_variables = tuple(variables.edge(vertex, 4) for vertex in ANCHOR)
    if cube_variables != (4, 14, 23, 31):
        raise AssertionError("clean-room cube-variable allocation changed")
    return ParentReconstruction(
        payload=payload,
        variable_count=EXPECTED_VARIABLE_COUNT,
        clause_count=EXPECTED_CLAUSE_COUNT,
        literal_count=EXPECTED_LITERAL_COUNT,
        cube_variables=cube_variables,
        cube_labels=tuple(f"e_{vertex}_4" for vertex in ANCHOR),
        clause_families=families,
    )
