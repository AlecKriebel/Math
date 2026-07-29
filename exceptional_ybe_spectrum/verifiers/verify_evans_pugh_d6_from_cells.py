#!/usr/bin/env python3
"""Independent exact reconstruction of the D^(6) connection from cells.

Unlike scripts/audit_evans_pugh_d6_connection.py, this verifier does not
enter the printed U-block matrices.  It specializes the printed Ocneanu
cells at k=1 and applies Evans--Pugh equation (HeckeRep) directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Sequence, Tuple

import sympy as sp


@dataclass(frozen=True)
class Edge:
    name: str
    source: str
    target: str


I = sp.I
SQRT3 = sp.sqrt(3)
OMEGA = (-1 + I * SQRT3) / 2
Q0 = (SQRT3 + I) / 2
Q = (1 + I * SQRT3) / 2

EDGES = (
    Edge("a", "0", "1"),
    Edge("g", "1", "2"),
    Edge("gp", "1", "2"),
    Edge("b", "2", "0"),
    Edge("c0", "2", "30"),
    Edge("c1", "2", "31"),
    Edge("c2", "2", "32"),
    Edge("d0", "30", "1"),
    Edge("d1", "31", "1"),
    Edge("d2", "32", "1"),
)
BY_NAME = {edge.name: edge for edge in EDGES}
PF = {"0": 1, "1": 2, "2": 2, "30": 1, "31": 1, "32": 1}


def paths(length: int) -> List[Tuple[str, ...]]:
    answer = [(edge.name,) for edge in EDGES]
    for _ in range(length - 1):
        answer = [
            path + (edge.name,)
            for path in answer
            for edge in EDGES
            if BY_NAME[path[-1]].target == edge.source
        ]
    return answer


def cyclic_rotations(word: Tuple[str, str, str]):
    return (word, word[1:] + word[:1], word[2:] + word[:2])


def cell_system() -> Dict[Tuple[str, str, str], sp.Expr]:
    cells: Dict[Tuple[str, str, str], sp.Expr] = {}

    def add_cycle(word: Tuple[str, str, str], value: sp.Expr) -> None:
        for rotation in cyclic_rotations(word):
            cells[rotation] = value

    add_cycle(("a", "g", "b"), sp.sqrt(2 * SQRT3))
    add_cycle(("a", "gp", "b"), sp.Integer(0))

    magnitude_g = sp.sqrt(6 * SQRT3) / 3
    magnitude_gp = 2 * sp.sqrt(3 * SQRT3) / 3
    for r in range(3):
        epsilon = OMEGA**r
        add_cycle((f"c{r}", f"d{r}", "g"), epsilon * magnitude_g)
        add_cycle(
            (f"c{r}", f"d{r}", "gp"),
            sp.conjugate(epsilon) * magnitude_gp,
        )
    return cells


def build_u2(paths2: Sequence[Tuple[str, str]]) -> sp.Matrix:
    cells = cell_system()
    index = {path: i for i, path in enumerate(paths2)}
    result = sp.zeros(len(paths2))
    for input_path, output_path in product(paths2, repeat=2):
        input_start = BY_NAME[input_path[0]].source
        input_end = BY_NAME[input_path[-1]].target
        output_start = BY_NAME[output_path[0]].source
        output_end = BY_NAME[output_path[-1]].target
        if (input_start, input_end) != (output_start, output_end):
            continue
        coefficient = 0
        for closing in EDGES:
            if closing.source != input_end or closing.target != input_start:
                continue
            output_cell = cells.get(
                (closing.name, output_path[0], output_path[1]), 0
            )
            input_cell = cells.get(
                (closing.name, input_path[0], input_path[1]), 0
            )
            coefficient += output_cell * sp.conjugate(input_cell)
        coefficient /= PF[input_start] * PF[input_end]
        result[index[output_path], index[input_path]] = sp.simplify(coefficient)
    return result


def insert_on_paths3(
    paths3: Sequence[Tuple[str, str, str]],
    paths2: Sequence[Tuple[str, str]],
    u2: sp.Matrix,
    position: int,
) -> sp.Matrix:
    index2 = {path: i for i, path in enumerate(paths2)}
    index3 = {path: i for i, path in enumerate(paths3)}
    result = sp.zeros(len(paths3))
    for input_index, path in enumerate(paths3):
        local_input = path[position : position + 2]
        for local_output in paths2:
            value = u2[index2[local_output], index2[local_input]]
            if value == 0:
                continue
            output = list(path)
            output[position : position + 2] = local_output
            output = tuple(output)
            if output in index3:
                result[index3[output], input_index] += value
    return result


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def main() -> None:
    vertices = ("0", "1", "2", "30", "31", "32")
    adjacency = sp.zeros(6)
    vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
    for edge in EDGES:
        adjacency[vertex_index[edge.source], vertex_index[edge.target]] += 1
    pf_vector = sp.Matrix([PF[vertex] for vertex in vertices])
    assert adjacency * pf_vector == 2 * pf_vector

    p2 = paths(2)
    p3 = paths(3)
    u = build_u2(p2)
    assert len(p2) == 20
    assert len(p3) == 48
    assert zero(u - u.conjugate().T)
    assert zero(u * u - SQRT3 * u)
    assert u.rank() == 10

    p = u / SQRT3
    f = Q * sp.eye(20) - Q0 * u
    assert zero(p * p - p)
    assert zero(f.conjugate().T * f - sp.eye(20))
    assert zero((f + sp.eye(20)) * (f - Q * sp.eye(20)))

    u1 = insert_on_paths3(p3, p2, u, 0)
    u2 = insert_on_paths3(p3, p2, u, 1)
    p1, p2_shift = u1 / SQRT3, u2 / SQRT3
    assert zero(
        p1 * p2_shift * p1
        - p2_shift * p1 * p2_shift
        - (p1 - p2_shift) / 3
    )
    r1 = Q * sp.eye(48) - Q0 * u1
    r2 = Q * sp.eye(48) - Q0 * u2
    assert zero(r1 * r2 * r1 - r2 * r1 * r2)

    print("Independent D^(6) cell-to-connection verifier: PASS")
    print("source data: specialized Ocneanu cells, not printed U blocks")
    print("integer Perron--Frobenius vector (1,2,2,1,1,1), eigenvalue 2: PASS")
    print("dim K2 = 20, rank P = 10, dim K3 = 48")
    print("Hermitian projection, unitarity, Hecke polynomial, cubic, braid: PASS")


if __name__ == "__main__":
    main()
