#!/usr/bin/env python3
"""Exact SAT/CEGAR probe for the static complement-link gate at k=3.

The unknown graph H is required to have:

* a fixed triangle 0,1,2 and no K4;
* a common neighbor for every pair of vertices;
* a bipartite link H[N_H(w)] for every vertex w.

The last condition is encoded by an explicit link two-coloring for every
root.  Non-three-colorability is imposed by CEGAR: whenever the SAT model
is three-colorable, its coloring gives the sound cut saying that at least
one same-colored pair must become an edge.  Thus every reported SAT graph
is checked independently against all four static conditions and against
an exact DSATUR coloring search.

This is a discovery probe.  A SAT witness is independently and exhaustively
checked by ``verify_witness.py`` before it is used as a mathematical control.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


Pair = tuple[int, int]


class CNF:
    def __init__(self) -> None:
        self.next_var = 1
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        answer = self.next_var
        self.next_var += 1
        return answer

    def add(self, *literals: int) -> None:
        if not literals:
            raise ValueError("empty clause")
        self.clauses.append(list(literals))

    @property
    def variable_count(self) -> int:
        return self.next_var - 1

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}\n"]
        lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in self.clauses)
        return "".join(lines).encode("ascii")


@dataclass(frozen=True)
class Encoding:
    cnf: CNF
    edge_vars: dict[Pair, int]


def edge_key(u: int, v: int) -> Pair:
    if u == v:
        raise ValueError("loops are not graph edges")
    return (u, v) if u < v else (v, u)


def build_base(order: int, coloring_cuts: Iterable[tuple[int, ...]]) -> Encoding:
    if order < 3:
        raise ValueError("order must be at least three")
    cnf = CNF()
    edge_vars = {
        pair: cnf.var() for pair in itertools.combinations(range(order), 2)
    }

    def edge(u: int, v: int) -> int:
        return edge_vars[edge_key(u, v)]

    # A triangle exists in every possible countermodel; fix one by relabeling.
    cnf.add(edge(0, 1))
    cnf.add(edge(0, 2))
    cnf.add(edge(1, 2))

    # K4-free.
    for four in itertools.combinations(range(order), 4):
        cnf.add(*(-edge(u, v) for u, v in itertools.combinations(four, 2)))

    # Every pair has a common neighbor.  Witness variables are one-way:
    # selected witness => the two incident graph edges.
    for u, v in itertools.combinations(range(order), 2):
        witnesses: list[int] = []
        for w in range(order):
            if w in (u, v):
                continue
            witness = cnf.var()
            witnesses.append(witness)
            cnf.add(-witness, edge(u, w))
            cnf.add(-witness, edge(v, w))
        cnf.add(*witnesses)

    # An existential two-coloring of every vertex link.  A triangle wuv
    # makes uv an edge of L_w, so its endpoints receive different colors.
    link_color = {
        (w, v): cnf.var()
        for w in range(order)
        for v in range(order)
        if w != v
    }
    for w in range(order):
        for u, v in itertools.combinations(
            (x for x in range(order) if x != w), 2
        ):
            guard = (-edge(w, u), -edge(w, v), -edge(u, v))
            cnf.add(*guard, link_color[w, u], link_color[w, v])
            cnf.add(*guard, -link_color[w, u], -link_color[w, v])

    # Each exact 3-coloring of a previous model is blocked soundly: some pair
    # in one of its color classes must be made adjacent.
    for colors in coloring_cuts:
        if len(colors) != order:
            raise ValueError("coloring cut has the wrong order")
        literals = [
            edge(u, v)
            for u, v in itertools.combinations(range(order), 2)
            if colors[u] == colors[v]
        ]
        cnf.add(*literals)

    return Encoding(cnf=cnf, edge_vars=edge_vars)


def adjacency_from_model(
    order: int, edge_vars: dict[Pair, int], positive: set[int]
) -> tuple[int, ...]:
    adjacency = [0] * order
    for (u, v), variable in edge_vars.items():
        if variable in positive:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return tuple(adjacency)


def exact_coloring(adjacency: tuple[int, ...], limit: int) -> tuple[int, ...] | None:
    """Return a proper coloring using at most ``limit`` colors, or None."""

    order = len(adjacency)
    colors = [-1] * order
    saturation = [0] * order
    degrees = [mask.bit_count() for mask in adjacency]

    def recurse(colored: int) -> bool:
        if colored == order:
            return True
        best = max(
            (v for v in range(order) if colors[v] < 0),
            key=lambda v: (saturation[v].bit_count(), degrees[v], -v),
        )
        forbidden = saturation[best]
        for color in range(limit):
            bit = 1 << color
            if forbidden & bit:
                continue
            colors[best] = color
            changed: list[tuple[int, int]] = []
            remaining = adjacency[best]
            while remaining:
                lsb = remaining & -remaining
                neighbor = lsb.bit_length() - 1
                remaining ^= lsb
                if colors[neighbor] < 0 and not saturation[neighbor] & bit:
                    changed.append((neighbor, saturation[neighbor]))
                    saturation[neighbor] |= bit
            if recurse(colored + 1):
                return True
            for neighbor, previous in changed:
                saturation[neighbor] = previous
            colors[best] = -1
        return False

    return tuple(colors) if recurse(0) else None


def solve(cadical: Path, cnf_bytes: bytes, timeout_seconds: float) -> tuple[str, set[int], str]:
    with tempfile.TemporaryDirectory(prefix="static_gate_") as temporary:
        cnf_path = Path(temporary) / "instance.cnf"
        cnf_path.write_bytes(cnf_bytes)
        try:
            completed = subprocess.run(
                [str(cadical.resolve()), str(cnf_path)],
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            return "TIMEOUT", set(), (error.stdout or "") + (error.stderr or "")
        output = completed.stdout + completed.stderr
        if completed.returncode == 20:
            return "UNSAT", set(), output
        if completed.returncode != 10:
            return f"ERROR-{completed.returncode}", set(), output
        positive = {
            int(token)
            for line in completed.stdout.splitlines()
            if line.startswith("v ")
            for token in line[2:].split()
            if token.lstrip("-").isdigit() and int(token) > 0
        }
        return "SAT", positive, output


def edges(adjacency: tuple[int, ...]) -> list[list[int]]:
    return [
        [u, v]
        for u in range(len(adjacency))
        for v in range(u + 1, len(adjacency))
        if adjacency[u] >> v & 1
    ]


def graph6(adjacency: tuple[int, ...]) -> str:
    order = len(adjacency)
    if order > 62:
        raise ValueError("compact graph6 only")
    bits: list[int] = []
    # graph6 orders upper-triangle bits by increasing second endpoint.
    for v in range(1, order):
        for u in range(v):
            bits.append((adjacency[u] >> v) & 1)
    while len(bits) % 6:
        bits.append(0)
    return chr(order + 63) + "".join(
        chr(63 + sum(bits[start + offset] << (5 - offset) for offset in range(6)))
        for start in range(0, len(bits), 6)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--max-iterations", type=int, default=10000)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    started = time.monotonic()
    cuts: list[tuple[int, ...]] = []
    transcript: list[dict[str, object]] = []
    final: dict[str, object] | None = None
    for iteration in range(arguments.max_iterations):
        encoding = build_base(arguments.order, cuts)
        data = encoding.cnf.dimacs()
        status, positive, solver_output = solve(arguments.cadical, data, arguments.timeout)
        record: dict[str, object] = {
            "iteration": iteration,
            "status": status,
            "variables": encoding.cnf.variable_count,
            "clauses": len(encoding.cnf.clauses),
            "cnf_sha256": hashlib.sha256(data).hexdigest(),
            "solver_tail": solver_output.splitlines()[-8:],
        }
        transcript.append(record)
        if status != "SAT":
            final = {"status": status}
            break
        adjacency = adjacency_from_model(
            arguments.order, encoding.edge_vars, positive
        )
        coloring = exact_coloring(adjacency, 3)
        if coloring is None:
            final = {
                "status": "WITNESS",
                "graph6": graph6(adjacency),
                "edges": edges(adjacency),
                "edge_count": sum(mask.bit_count() for mask in adjacency) // 2,
            }
            break
        cuts.append(coloring)
        record["three_coloring"] = list(coloring)
    else:
        final = {"status": "ITERATION_LIMIT"}

    payload = {
        "schema": "gamma-theta-static-gate-discovery-v1",
        "order": arguments.order,
        "fixed_triangle": [0, 1, 2],
        "elapsed_seconds": time.monotonic() - started,
        "cut_count": len(cuts),
        "final": final,
        "transcript": transcript,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: payload[k] for k in ("order", "elapsed_seconds", "cut_count", "final")}, indent=2))


if __name__ == "__main__":
    main()
