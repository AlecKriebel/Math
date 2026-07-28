#!/usr/bin/env python3
"""Independent exact verification of the three-neutral SAT boundary control."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys


N = 13
S = (0, 1, 2)


def parse_model(path: Path) -> dict[int, bool]:
    values: dict[int, bool] = {}
    status_seen = False
    for line in path.read_text(encoding="ascii").splitlines():
        if line == "s SATISFIABLE":
            status_seen = True
        if not line.startswith("v "):
            continue
        for token in line.split()[1:]:
            literal = int(token)
            if literal:
                values[abs(literal)] = literal > 0
    if not status_seen:
        raise AssertionError("model lacks SAT status")
    return values


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = None
    clauses: list[tuple[int, ...]] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("p cnf "):
            _, _, raw_variables, raw_clauses = line.split()
            variables = int(raw_variables)
            expected_clauses = int(raw_clauses)
        elif line and not line.startswith("c"):
            values = tuple(map(int, line.split()))
            if values[-1] != 0:
                raise AssertionError("unterminated clause")
            clauses.append(values[:-1])
    if variables is None or len(clauses) != expected_clauses:
        raise AssertionError("bad DIMACS header")
    return variables, clauses


def dominates(mask: int, closed: list[int], full: int) -> bool:
    covered = 0
    rest = mask
    while rest:
        bit = rest & -rest
        vertex = bit.bit_length() - 1
        covered |= closed[vertex]
        rest ^= bit
    return covered == full


def independent(mask: int, adjacency: list[int]) -> bool:
    rest = mask
    while rest:
        bit = rest & -rest
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (rest ^ bit):
            return False
        rest ^= bit
    return True


def colorable(
    adjacency: list[int], color_count: int
) -> tuple[bool, list[int] | None]:
    colors = [-1] * N
    neighbor_colors = [set() for _ in range(N)]

    def visit(colored: int) -> bool:
        if colored == N:
            return True
        candidates = [v for v in range(N) if colors[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (len(neighbor_colors[v]), adjacency[v].bit_count(), -v),
        )
        blocked = neighbor_colors[vertex]
        for color in range(color_count):
            if color in blocked:
                continue
            colors[vertex] = color
            changed = []
            rest = adjacency[vertex]
            while rest:
                bit = rest & -rest
                w = bit.bit_length() - 1
                rest ^= bit
                if colors[w] < 0 and color not in neighbor_colors[w]:
                    neighbor_colors[w].add(color)
                    changed.append(w)
            if visit(colored + 1):
                return True
            for w in changed:
                neighbor_colors[w].remove(color)
            colors[vertex] = -1
        return False

    success = visit(0)
    return success, colors[:] if success else None


def eternal_kernel(
    k: int, adjacency: list[int], closed: list[int], full: int
) -> set[int]:
    current = {
        sum(1 << v for v in state)
        for state in itertools.combinations(range(N), k)
        if dominates(sum(1 << v for v in state), closed, full)
    }
    while True:
        retained: set[int] = set()
        for state in current:
            valid = True
            for attacked in range(N):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                response = False
                guards = state
                while guards:
                    guard_bit = guards & -guards
                    guard = guard_bit.bit_length() - 1
                    guards ^= guard_bit
                    if adjacency[guard] & attacked_bit:
                        successor = (state ^ guard_bit) | attacked_bit
                        if successor in current:
                            response = True
                            break
                if not response:
                    valid = False
                    break
            if valid:
                retained.add(state)
        if retained == current:
            return retained
        current = retained


def graph6(edges: set[tuple[int, int]]) -> str:
    bits = [
        int((i, j) in edges)
        for j in range(1, N)
        for i in range(j)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = "".join(
        chr(63 + sum(bits[offset + k] << (5 - k) for k in range(6)))
        for offset in range(0, len(bits), 6)
    )
    return chr(63 + N) + payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    instance = here / "q3-control-instance.cnf"
    model = here / "q3-control-model.out"

    variable_count, clauses = parse_cnf(instance)
    values = parse_model(model)
    if len(values) != variable_count:
        raise AssertionError("model is not total")
    if any(
        not any(values[abs(literal)] == (literal > 0) for literal in clause)
        for clause in clauses
    ):
        raise AssertionError("model does not satisfy the CNF")

    pairs = tuple(itertools.combinations(range(N), 2))
    triples = tuple(itertools.combinations(range(N), 3))
    edge_variable = {uv: index + 1 for index, uv in enumerate(pairs)}
    family_offset = len(pairs)
    family_variable = {
        state: family_offset + index + 1 for index, state in enumerate(triples)
    }

    adjacency_g = [0] * N
    edges_g: list[list[int]] = []
    edges_h: list[list[int]] = []
    for u, v in pairs:
        if values[edge_variable[(u, v)]]:
            edges_h.append([u, v])
        else:
            edges_g.append([u, v])
            adjacency_g[u] |= 1 << v
            adjacency_g[v] |= 1 << u
    full = (1 << N) - 1
    closed = [adjacency_g[v] | (1 << v) for v in range(N)]
    adjacency_h = [full ^ closed[v] for v in range(N)]

    gamma = next(
        size
        for size in range(1, N + 1)
        if any(
            dominates(sum(1 << v for v in subset), closed, full)
            for subset in itertools.combinations(range(N), size)
        )
    )
    alpha = max(
        size
        for size in range(1, N + 1)
        if any(
            independent(sum(1 << v for v in subset), adjacency_g)
            for subset in itertools.combinations(range(N), size)
        )
    )
    independent_domination = next(
        size
        for size in range(1, N + 1)
        if any(
            independent(sum(1 << v for v in subset), adjacency_g)
            and dominates(sum(1 << v for v in subset), closed, full)
            for subset in itertools.combinations(range(N), size)
        )
    )
    theta = None
    theta_coloring = None
    for count in range(1, N + 1):
        ok, coloring = colorable(adjacency_h, count)
        if ok:
            theta = count
            theta_coloring = coloring
            break

    kernels = {}
    gamma_infinity = None
    for size in range(gamma, N + 1):
        kernel = eternal_kernel(size, adjacency_g, closed, full)
        kernels[str(size)] = len(kernel)
        if kernel:
            gamma_infinity = size
            break

    selected_family = {
        sum(1 << v for v in state)
        for state in triples
        if values[family_variable[state]]
    }
    family_dominates = all(
        dominates(state, closed, full) for state in selected_family
    )
    obligations = 0
    family_closed = True
    for state in selected_family:
        for attacked in range(N):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            obligations += 1
            if not any(
                (adjacency_g[guard] & attacked_bit)
                and (((state ^ (1 << guard)) | attacked_bit) in selected_family)
                for guard in range(N)
                if state & (1 << guard)
            ):
                family_closed = False
                break

    def response_list(vertex: int) -> list[int]:
        return [
            anchor
            for anchor in S
            if values[
                family_variable[
                    tuple(sorted((set(S) - {anchor}) | {vertex}))
                ]
            ]
        ]

    adjacency_bytes = "\n".join(
        "".join("1" if adjacency_g[u] & (1 << v) else "0" for v in range(N))
        for u in range(N)
    ).encode("ascii")
    result = {
        "verdict": "PASS",
        "instance_sha256": hashlib.sha256(instance.read_bytes()).hexdigest(),
        "model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
        "adjacency_matrix_sha256": hashlib.sha256(adjacency_bytes).hexdigest(),
        "order": N,
        "size": len(edges_g),
        "labeled_graph6": graph6({tuple(edge) for edge in edges_g}),
        "edges_g": edges_g,
        "edges_h": edges_h,
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "theta_coloring_of_h": theta_coloring,
        "greatest_kernel_sizes": kernels,
        "selected_family_size": len(selected_family),
        "selected_family_dominates": family_dominates,
        "selected_family_closed": family_closed,
        "attack_obligations": obligations,
        "reference_state": list(S),
        "reference_independent": independent(
            sum(1 << v for v in S), adjacency_g
        ),
        "neutral_vertices": {
            str(q): all(adjacency_g[q] & (1 << anchor) for anchor in S)
            for q in (8, 9, 10)
        },
        "response_lists": {
            "3": response_list(3),
            "5": response_list(5),
        },
        "cnf_satisfied": True,
    }
    required = (
        result["parameters"]
        == {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        }
        and family_dominates
        and family_closed
        and result["reference_independent"]
        and all(result["neutral_vertices"].values())
        and {0, 2}.issubset(result["response_lists"]["3"])
        and {0, 1}.issubset(result["response_lists"]["5"])
    )
    if not required:
        result["verdict"] = "FAIL"
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result:
        args.result.write_text(output, encoding="utf-8")
    print(output, end="")
    sys.exit(0 if result["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
