#!/usr/bin/env python3
"""Symbolic audit for the signed-balance exact-two-list attack trees.

This checker does not search for a graph.  It verifies that every stated
one-guard forcing step uses only literal complement edges, exact response
lists, and previously retained states, and independently enumerates the
short residual type words.
"""

from __future__ import annotations

from itertools import permutations, product
import json


Anchor = str
Vertex = str
State = frozenset[Vertex]

ANCHORS = frozenset(("a", "b", "c"))


def edge(u: Vertex, v: Vertex) -> frozenset[Vertex]:
    if u == v:
        raise ValueError("loops are forbidden")
    return frozenset((u, v))


def canonical_word(word: tuple[int, ...]) -> tuple[int, ...]:
    images: list[tuple[int, ...]] = []
    size = len(word)
    for relabeling in permutations(range(3)):
        relabeled = tuple(relabeling[value] for value in word)
        for shift in range(size):
            rotated = relabeled[shift:] + relabeled[:shift]
            images.append(rotated)
            images.append(tuple(reversed(rotated)))
    return min(images)


def word_orbits() -> dict[int, list[str]]:
    output: dict[int, list[str]] = {}
    for size in range(3, 6):
        representatives = {
            canonical_word(word)
            for word in product(range(3), repeat=size)
            if sum(
                word[index] == word[(index + 1) % size]
                for index in range(size)
            )
            % 2
            == 1
        }
        output[size] = [
            "".join(map(str, word)) for word in sorted(representatives)
        ]
    expected = {
        3: ["000", "001"],
        4: ["0012"],
        5: ["00000", "00001", "00011", "00101", "00102", "00121"],
    }
    if output != expected:
        raise RuntimeError(f"unexpected type-word orbits: {output}")
    residual = {
        "0012",
        "00011",
        "00101",
        "00102",
        "00121",
    }
    removed = {
        "000": "one-type odd cycle in a bipartite projection",
        "001": "opposite-side neighbors of a same-type edge",
        "00000": "one-type odd cycle in a bipartite projection",
        "00001": "opposite-side neighbors of a length-three path",
    }
    if set(sum(output.values(), [])) - set(removed) != residual:
        raise RuntimeError("residual-word reduction differs")
    return output


class Audit:
    def __init__(
        self,
        name: str,
        types: dict[Vertex, Anchor],
        h_edges: set[frozenset[Vertex]],
    ) -> None:
        self.name = name
        self.types = dict(types)
        self.h_edges = set(h_edges)
        self.h_edges |= {
            edge(u, v)
            for index, u in enumerate(sorted(ANCHORS))
            for v in sorted(ANCHORS)[index + 1 :]
        }
        self.retained: set[State] = set()
        self.steps: list[dict[str, object]] = []
        for vertex, omitted in self.types.items():
            if omitted not in ANCHORS:
                raise RuntimeError(f"{name}: bad type for {vertex}")
            self.h_edges.add(edge(vertex, omitted))

    def is_h(self, u: Vertex, v: Vertex) -> bool:
        return edge(u, v) in self.h_edges

    def direct(self, vertex: Vertex, omitted: Anchor) -> State:
        return frozenset((ANCHORS - {omitted}) | {vertex})

    def retain_direct(self, vertex: Vertex, omitted: Anchor) -> State:
        if vertex not in self.types:
            raise RuntimeError(f"{self.name}: unknown outside vertex {vertex}")
        if self.types[vertex] == omitted:
            raise RuntimeError(
                f"{self.name}: omitted type {omitted} is not a response"
            )
        state = self.direct(vertex, omitted)
        self.retained.add(state)
        self.steps.append(
            {
                "kind": "direct-retained",
                "vertex": vertex,
                "omitted": omitted,
                "state": sorted(state),
            }
        )
        return state

    def check_invalid(
        self,
        state: State,
        reason: tuple[str, Vertex, Anchor | None],
    ) -> None:
        kind, vertex, omitted = reason
        if kind == "miss":
            if vertex in state:
                raise RuntimeError(
                    f"{self.name}: claimed missed vertex {vertex} occupied"
                )
            missing_edges = [
                guard
                for guard in state
                if not self.is_h(vertex, guard)
            ]
            if missing_edges:
                raise RuntimeError(
                    f"{self.name}: {sorted(state)} does not literally miss "
                    f"{vertex}; absent H edges to {missing_edges}"
                )
            return
        if kind == "direct-absent":
            if omitted is None:
                raise RuntimeError("missing omitted anchor")
            if vertex not in self.types:
                raise RuntimeError(f"{self.name}: unknown direct vertex")
            if self.types[vertex] != omitted:
                raise RuntimeError(
                    f"{self.name}: {vertex} has type {self.types[vertex]}, "
                    f"not absent response {omitted}"
                )
            if state != self.direct(vertex, omitted):
                raise RuntimeError(
                    f"{self.name}: {sorted(state)} is not the direct state"
                )
            return
        raise RuntimeError(f"{self.name}: unknown invalidity kind {kind}")

    def force(
        self,
        state: State,
        attacked: Vertex,
        expected: State,
        invalid: dict[State, tuple[str, Vertex, Anchor | None]],
    ) -> None:
        if state not in self.retained:
            raise RuntimeError(
                f"{self.name}: forcing from unproved state {sorted(state)}"
            )
        if attacked in state:
            raise RuntimeError(f"{self.name}: occupied attack at {attacked}")
        candidate_guards: list[Vertex] = []
        audited: list[dict[str, object]] = []
        for guard in sorted(state):
            successor = frozenset((state - {guard}) | {attacked})
            if self.is_h(guard, attacked):
                audited.append(
                    {
                        "guard": guard,
                        "outcome": "blocked-by-H",
                    }
                )
                continue
            if successor == expected:
                candidate_guards.append(guard)
                audited.append(
                    {
                        "guard": guard,
                        "outcome": "forced-successor",
                        "state": sorted(successor),
                    }
                )
                continue
            if successor not in invalid:
                raise RuntimeError(
                    f"{self.name}: unaudited successor {sorted(successor)} "
                    f"under attack {attacked}"
                )
            self.check_invalid(successor, invalid[successor])
            audited.append(
                {
                    "guard": guard,
                    "outcome": invalid[successor][0],
                    "state": sorted(successor),
                    "witness": invalid[successor][1],
                }
            )
        if len(candidate_guards) != 1:
            raise RuntimeError(
                f"{self.name}: expected one forced guard, got "
                f"{candidate_guards}"
            )
        self.retained.add(expected)
        self.steps.append(
            {
                "kind": "force",
                "from": sorted(state),
                "attack": attacked,
                "to": sorted(expected),
                "responses": audited,
            }
        )

    def contradict(
        self,
        state: State,
        attacked: Vertex,
        invalid: dict[State, tuple[str, Vertex, Anchor | None]],
    ) -> None:
        if state not in self.retained:
            raise RuntimeError(
                f"{self.name}: contradiction from unproved state"
            )
        if attacked in state:
            raise RuntimeError(f"{self.name}: occupied terminal attack")
        audited: list[dict[str, object]] = []
        for guard in sorted(state):
            successor = frozenset((state - {guard}) | {attacked})
            if self.is_h(guard, attacked):
                audited.append(
                    {
                        "guard": guard,
                        "outcome": "blocked-by-H",
                    }
                )
                continue
            if successor not in invalid:
                raise RuntimeError(
                    f"{self.name}: live terminal successor "
                    f"{sorted(successor)}"
                )
            self.check_invalid(successor, invalid[successor])
            audited.append(
                {
                    "guard": guard,
                    "outcome": invalid[successor][0],
                    "state": sorted(successor),
                    "witness": invalid[successor][1],
                }
            )
        self.steps.append(
            {
                "kind": "contradiction",
                "from": sorted(state),
                "attack": attacked,
                "responses": audited,
            }
        )

    def nondominating(self, state: State, missed: Vertex) -> None:
        self.check_invalid(state, ("miss", missed, None))
        self.steps.append(
            {
                "kind": "nondominating",
                "state": sorted(state),
                "missed": missed,
            }
        )


def miss(vertex: Vertex) -> tuple[str, Vertex, Anchor | None]:
    return ("miss", vertex, None)


def absent(
    vertex: Vertex,
    omitted: Anchor,
) -> tuple[str, Vertex, Anchor | None]:
    return ("direct-absent", vertex, omitted)


def cycle_edges(vertices: tuple[Vertex, ...]) -> set[frozenset[Vertex]]:
    return {
        edge(vertices[index], vertices[(index + 1) % len(vertices)])
        for index in range(len(vertices))
    }


def audit_0012() -> Audit:
    types = {"p": "a", "q": "a", "u": "b", "v": "c"}
    audit = Audit("0012", types, cycle_edges(("p", "q", "u", "v")))
    root = audit.retain_direct("p", "b")
    audit.contradict(
        root,
        "u",
        {
            frozenset(("c", "p", "u")): miss("v"),
            frozenset(("a", "p", "u")): miss("q"),
            frozenset(("a", "c", "u")): absent("u", "b"),
        },
    )
    return audit


def audit_00011() -> Audit:
    types = {
        "p": "a",
        "q": "a",
        "r": "a",
        "u": "b",
        "v": "b",
    }
    audit = Audit(
        "00011",
        types,
        cycle_edges(("p", "q", "r", "u", "v")),
    )
    root = audit.retain_direct("p", "c")
    first = frozenset(("b", "p", "v"))
    audit.force(root, "v", first, {})
    second = frozenset(("p", "r", "v"))
    audit.force(
        first,
        "r",
        second,
        {
            frozenset(("b", "r", "v")): miss("u"),
            frozenset(("b", "p", "r")): miss("a"),
        },
    )
    audit.contradict(
        second,
        "a",
        {frozenset(("a", "p", "r")): miss("q")},
    )
    return audit


def audit_00121() -> Audit:
    types = {
        "p": "a",
        "q": "a",
        "u": "b",
        "v": "c",
        "w": "b",
    }
    audit = Audit(
        "00121",
        types,
        cycle_edges(("p", "q", "u", "v", "w")),
    )
    root = audit.retain_direct("v", "a")
    first = frozenset(("c", "p", "v"))
    audit.force(
        root,
        "p",
        first,
        {
            frozenset(("b", "p", "v")): miss("w"),
            frozenset(("b", "c", "p")): absent("p", "a"),
        },
    )
    second = frozenset(("p", "q", "v"))
    audit.force(
        first,
        "q",
        second,
        {frozenset(("c", "p", "q")): miss("a")},
    )
    audit.contradict(
        second,
        "b",
        {
            frozenset(("b", "q", "v")): miss("u"),
            frozenset(("b", "p", "v")): miss("w"),
            frozenset(("b", "p", "q")): miss("a"),
        },
    )
    return audit


def audit_00102() -> Audit:
    types = {
        "x0": "a",
        "x1": "a",
        "y": "b",
        "x2": "a",
        "z": "c",
        "q": "c",
    }
    h_edges = cycle_edges(("x0", "x1", "y", "x2", "z"))
    h_edges |= {edge("q", "x1"), edge("q", "y")}
    audit = Audit("00102", types, h_edges)
    root = audit.retain_direct("z", "b")
    first = frozenset(("a", "x0", "z"))
    audit.force(root, "x0", first, {})
    second = frozenset(("x0", "y", "z"))
    audit.force(
        first,
        "y",
        second,
        {
            frozenset(("a", "y", "z")): miss("x2"),
            frozenset(("a", "x0", "y")): miss("x1"),
        },
    )
    third = frozenset(("y", "z", "q"))
    audit.force(
        second,
        "q",
        third,
        {frozenset(("x0", "y", "q")): miss("x1")},
    )
    audit.contradict(
        third,
        "a",
        {
            frozenset(("a", "z", "q")): miss("c"),
            frozenset(("a", "y", "q")): miss("x1"),
            frozenset(("a", "y", "z")): miss("x2"),
        },
    )
    return audit


def audit_00101(collide: bool) -> Audit:
    types = {
        "p": "a",
        "q": "a",
        "u": "b",
        "r": "a",
        "v": "b",
        "t": "c",
    }
    if not collide:
        types["s"] = "c"
    s = "t" if collide else "s"
    h_edges = cycle_edges(("p", "q", "u", "r", "v"))
    h_edges |= {
        edge("t", "q"),
        edge("t", "u"),
        edge(s, "u"),
        edge(s, "r"),
    }
    audit = Audit(
        "00101-collided" if collide else "00101-distinct",
        types,
        h_edges,
    )
    root = audit.retain_direct("v", "c")
    first = frozenset(("a", "r", "v"))
    audit.force(root, "r", first, {})
    second = frozenset(("a", "q", "r"))
    audit.force(
        first,
        "q",
        second,
        {frozenset(("a", "q", "v")): miss("p")},
    )
    third = frozenset(("q", "u", "r"))
    audit.force(second, "u", third, {})
    if collide:
        audit.nondominating(third, "t")
    else:
        audit.contradict(
            third,
            "c",
            {
                frozenset(("c", "u", "r")): miss("s"),
                frozenset(("c", "q", "r")): miss("a"),
                frozenset(("c", "q", "u")): miss("t"),
            },
        )
    return audit


def coloring_truth_table() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []

    def color(vertex_type: int, chirality: int) -> int:
        return (
            (vertex_type - 1) % 3
            if chirality == 0
            else (vertex_type + 1) % 3
        )

    for first_type in range(3):
        for second_type in range(3):
            if first_type == second_type:
                first_chirality, second_chirality = 0, 1
                sign = 1
            else:
                first_chirality = second_chirality = 0
                sign = 0
            first_color = color(first_type, first_chirality)
            second_color = color(second_type, second_chirality)
            if first_color == second_color:
                raise RuntimeError("signed coloring truth table failed")
            rows.append(
                {
                    "first_type": first_type,
                    "second_type": second_type,
                    "sign": sign,
                    "first_chirality": first_chirality,
                    "second_chirality": second_chirality,
                    "first_color": first_color,
                    "second_color": second_color,
                }
            )
    return rows


def main() -> None:
    audits = [
        audit_0012(),
        audit_00011(),
        audit_00121(),
        audit_00102(),
        audit_00101(True),
        audit_00101(False),
    ]
    output = {
        "schema": "signed-balance-symbolic-audit-v1",
        "status": "PASS",
        "unbalanced_type_word_orbits": word_orbits(),
        "attack_audits": {
            audit.name: {
                "types": audit.types,
                "literal_h_edges": [
                    sorted(item) for item in sorted(
                        audit.h_edges,
                        key=lambda item: tuple(sorted(item)),
                    )
                ],
                "steps": audit.steps,
            }
            for audit in audits
        },
        "coloring_truth_table": coloring_truth_table(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
