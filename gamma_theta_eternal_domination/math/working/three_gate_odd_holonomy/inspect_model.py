#!/usr/bin/env python3
"""Inspect a SAT model emitted by the boundary-cycle probe."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


def load_probe(path: Path):
    spec = importlib.util.spec_from_file_location("boundary_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def graph6(order: int, g_edges: set[tuple[int, int]]) -> str:
    if order > 62:
        raise ValueError("short graph6 header only")
    bits = [
        int((i, j) in g_edges)
        for j in range(1, order)
        for i in range(j)
    ]
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(order + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def dominates(
    state: tuple[int, ...],
    order: int,
    g_edges: set[tuple[int, int]],
) -> bool:
    occupied = set(state)
    for vertex in range(order):
        if vertex in occupied:
            continue
        if not any(tuple(sorted((vertex, guard))) in g_edges for guard in state):
            return False
    return True


def independent(
    state: tuple[int, ...],
    g_edges: set[tuple[int, int]],
) -> bool:
    return all(tuple(sorted(uv)) not in g_edges for uv in combinations(state, 2))


def chromatic_number(
    order: int,
    edges: set[tuple[int, int]],
) -> tuple[int, list[int]]:
    adjacency = [set() for _ in range(order)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def colorable(colors: int) -> list[int] | None:
        assignment = [-1] * order

        def visit() -> bool:
            uncolored = [v for v in range(order) if assignment[v] < 0]
            if not uncolored:
                return True
            vertex = max(
                uncolored,
                key=lambda v: (
                    len({assignment[w] for w in adjacency[v] if assignment[w] >= 0}),
                    len(adjacency[v]),
                    -v,
                ),
            )
            blocked = {assignment[w] for w in adjacency[vertex] if assignment[w] >= 0}
            for color in range(colors):
                if color in blocked:
                    continue
                assignment[vertex] = color
                if visit():
                    return True
            assignment[vertex] = -1
            return False

        return assignment if visit() else None

    for colors in range(1, order + 1):
        assignment = colorable(colors)
        if assignment is not None:
            return colors, assignment
    raise AssertionError("unreachable")


def greatest_family(
    order: int,
    size: int,
    g_edges: set[tuple[int, int]],
) -> set[tuple[int, ...]]:
    family = {
        state
        for state in combinations(range(order), size)
        if dominates(state, order, g_edges)
    }
    while True:
        remove = set()
        for state in family:
            for attacked in range(order):
                if attacked in state:
                    continue
                legal = False
                for guard in state:
                    if tuple(sorted((guard, attacked))) not in g_edges:
                        continue
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    if successor in family:
                        legal = True
                        break
                if not legal:
                    remove.add(state)
                    break
        if not remove:
            return family
        family -= remove


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    probe = load_probe(Path(__file__).with_name("probe_boundary_cycle.py"))
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=0,
    )
    literals = [
        int(piece)
        for line in args.model.read_text(encoding="ascii").splitlines()
        if line.startswith("v ")
        for piece in line.split()[1:]
        if piece != "0"
    ]
    assignment = {abs(literal): literal > 0 for literal in literals}
    if len(assignment) != len(cnf.names) - 1:
        raise RuntimeError("incomplete model")

    edge = metadata["edge"]
    family_variables = metadata["family"]
    assert isinstance(edge, dict)
    assert isinstance(family_variables, dict)
    order = int(metadata["order"])
    h_edges = {uv for uv, variable in edge.items() if assignment[variable]}
    all_edges = set(combinations(range(order), 2))
    g_edges = all_edges - h_edges
    selected = {
        state
        for state, variable in family_variables.items()
        if assignment[variable]
    }
    if not all(dominates(state, order, g_edges) for state in selected):
        raise RuntimeError("selected nondominating state")
    kernels = {
        size: greatest_family(order, size, g_edges)
        for size in range(1, 4)
    }
    kernel3 = kernels[3]

    gamma = min(
        size
        for size in range(1, order + 1)
        if any(
            dominates(state, order, g_edges)
            for state in combinations(range(order), size)
        )
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(
            independent(state, g_edges)
            for state in combinations(range(order), size)
        )
    )
    independent_dominating = [
        len(state)
        for size in range(1, order + 1)
        for state in combinations(range(order), size)
        if independent(state, g_edges) and dominates(state, order, g_edges)
    ]
    theta, coloring = chromatic_number(order, h_edges)
    serialization = "\n".join(
        ",".join(map(str, state)) for state in sorted(kernel3)
    ).encode("ascii")
    result = {
        "graph6": graph6(order, g_edges),
        "order": order,
        "size": len(g_edges),
        "parameters": {
            "gamma": gamma,
            "i": min(independent_dominating),
            "alpha": alpha,
            "gamma_infinity": min(size for size, kernel in kernels.items() if kernel),
            "theta": theta,
        },
        "selected_family_size": len(selected),
        "greatest_family_sizes_1_to_3": {
            str(size): len(kernel) for size, kernel in kernels.items()
        },
        "greatest_triple_family_size": len(kernel3),
        "greatest_triple_family_sha256": sha256(serialization).hexdigest(),
        "theta_coloring_of_H": coloring,
        "h_edges": [list(uv) for uv in sorted(h_edges)],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["parameters"], sort_keys=True))
    print(result["graph6"])


if __name__ == "__main__":
    main()
