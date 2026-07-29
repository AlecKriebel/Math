#!/usr/bin/env python3
"""Exact audit of the Evans--Pugh D^(6) Ocneanu-cell connection.

This reconstructs the critical Hecke operator from the block matrices printed
in Evans--Pugh, arXiv:0906.4307, specialized to n=6 (k=1).  It verifies that:

* the operator acts on the 20-dimensional space of composable two-edge paths;
* its normalized Hecke projection has rank 10;
* the corresponding two-eigenvalue unitary satisfies the braid relation on
  the 48-dimensional space of composable three-edge paths;
* the zero extension to the full tensor square of the 10-dimensional edge
  space is singular, and hence is not an ordinary unitary R-matrix.
* either scalar Hecke-compatible completion of the noncomposable edge-pair
  sector fails the ordinary braid relation on mixed-composability triples.

Only exact SymPy arithmetic is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp


@dataclass(frozen=True)
class Edge:
    name: str
    source: str
    target: str


SQRT2 = sp.sqrt(2)
SQRT3 = sp.sqrt(3)
I = sp.I
OMEGA = (-1 + I * SQRT3) / 2
Q0 = (SQRT3 + I) / 2  # exp(pi i/6), Evans--Pugh's q at n=6
Q = (1 + I * SQRT3) / 2  # q0^2 = exp(pi i/3)


EDGES: Tuple[Edge, ...] = (
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
EDGE_BY_NAME: Dict[str, Edge] = {edge.name: edge for edge in EDGES}


Path2 = Tuple[str, str]
Path3 = Tuple[str, str, str]


def composable(words: Sequence[str]) -> bool:
    return all(
        EDGE_BY_NAME[left].target == EDGE_BY_NAME[right].source
        for left, right in zip(words, words[1:])
    )


def all_paths(length: int) -> List[Tuple[str, ...]]:
    if length < 1:
        raise ValueError("length must be positive")
    paths: List[Tuple[str, ...]] = [(edge.name,) for edge in EDGES]
    for _ in range(length - 1):
        paths = [
            path + (edge.name,)
            for path in paths
            for edge in EDGES
            if EDGE_BY_NAME[path[-1]].target == edge.source
        ]
    return paths


def endpoint(path: Sequence[str]) -> Tuple[str, str]:
    return EDGE_BY_NAME[path[0]].source, EDGE_BY_NAME[path[-1]].target


def d6_blocks() -> Dict[Tuple[str, str], Tuple[List[Path2], sp.Matrix]]:
    """Return the nonzero U^(x,y) blocks in printed row order."""
    blocks: Dict[Tuple[str, str], Tuple[List[Path2], sp.Matrix]] = {}

    rank_one_diag = sp.diag(SQRT3, 0)
    blocks[("0", "2")] = ([("a", "g"), ("a", "gp")], rank_one_diag)
    blocks[("1", "0")] = ([("g", "b"), ("gp", "b")], rank_one_diag)

    for r in range(3):
        eps = OMEGA**r
        v = sp.Matrix(
            [
                [1 / SQRT3, sp.conjugate(eps) * SQRT2 / SQRT3],
                [eps * SQRT2 / SQRT3, 2 / SQRT3],
            ]
        )
        blocks[("1", f"3{r}")] = (
            [("g", f"c{r}"), ("gp", f"c{r}")],
            v,
        )
        blocks[(f"3{r}", "2")] = (
            [(f"d{r}", "g"), (f"d{r}", "gp")],
            v,
        )

    # Evans--Pugh use epsilon = omega + 2*conjugate(omega) when k=1.
    epsilon = OMEGA + 2 * sp.conjugate(OMEGA)
    a = 1 / (2 * SQRT3)
    b = sp.Rational(1, 2)
    w = sp.Matrix(
        [
            [SQRT3 / 2, sp.conjugate(epsilon) * a, epsilon * a, b],
            [epsilon * a, SQRT3 / 2, sp.conjugate(epsilon) * a, OMEGA * b],
            [
                sp.conjugate(epsilon) * a,
                epsilon * a,
                SQRT3 / 2,
                sp.conjugate(OMEGA) * b,
            ],
            [b, sp.conjugate(OMEGA) * b, OMEGA * b, SQRT3 / 2],
        ]
    )
    blocks[("2", "1")] = (
        [("c0", "d0"), ("c1", "d1"), ("c2", "d2"), ("b", "a")],
        w,
    )
    return blocks


def global_u_on_paths2(
    paths2: Sequence[Path2],
) -> Tuple[sp.Matrix, Dict[Path2, int]]:
    index = {path: j for j, path in enumerate(paths2)}
    matrix = sp.zeros(len(paths2))
    assigned: set[Path2] = set()
    for endpoints, (block_paths, block) in d6_blocks().items():
        assert all(endpoint(path) == endpoints for path in block_paths)
        assert block.shape == (len(block_paths), len(block_paths))
        for row, out_path in enumerate(block_paths):
            assigned.add(out_path)
            for col, in_path in enumerate(block_paths):
                matrix[index[out_path], index[in_path]] = block[row, col]
    assert assigned == set(paths2)
    return matrix, index


def local_operator_on_paths3(
    paths3: Sequence[Path3],
    u2: sp.Matrix,
    index2: Dict[Path2, int],
    position: int,
) -> sp.Matrix:
    """Insert U on edge positions (0,1) or (1,2) of a path of length 3."""
    if position not in (0, 1):
        raise ValueError("position must be 0 or 1")
    index3 = {path: j for j, path in enumerate(paths3)}
    result = sp.zeros(len(paths3))
    for col, path in enumerate(paths3):
        local_in = path[position : position + 2]
        local_col = index2[local_in]
        for local_out, local_row in index2.items():
            coefficient = u2[local_row, local_col]
            if coefficient == 0:
                continue
            candidate = list(path)
            candidate[position : position + 2] = local_out
            candidate_tuple = tuple(candidate)
            if candidate_tuple in index3:
                result[index3[candidate_tuple], col] += coefficient
    return result


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    paths2 = [tuple(path) for path in all_paths(2)]
    paths3 = [tuple(path) for path in all_paths(3)]
    u2, index2 = global_u_on_paths2(paths2)

    assert len(EDGES) == 10
    assert len(paths2) == 20
    assert len(paths3) == 48
    assert is_zero(u2 - u2.conjugate().T)
    assert is_zero(u2 * u2 - SQRT3 * u2)
    assert u2.rank() == 10

    projection = sp.simplify(u2 / SQRT3)
    face_r = sp.simplify(Q * sp.eye(len(paths2)) - Q0 * u2)
    assert is_zero(projection * projection - projection)
    assert is_zero(face_r.conjugate().T * face_r - sp.eye(len(paths2)))
    assert is_zero(
        (face_r + sp.eye(len(paths2)))
        * (face_r - Q * sp.eye(len(paths2)))
    )

    u1 = local_operator_on_paths3(paths3, u2, index2, 0)
    u2_shift = local_operator_on_paths3(paths3, u2, index2, 1)
    p1 = sp.simplify(u1 / SQRT3)
    p2 = sp.simplify(u2_shift / SQRT3)
    cubic_residual = p1 * p2 * p1 - p2 * p1 * p2 - (p1 - p2) / 3
    assert is_zero(cubic_residual)

    r1 = Q * sp.eye(len(paths3)) - Q0 * u1
    r2 = Q * sp.eye(len(paths3)) - Q0 * u2_shift
    assert is_zero(r1 * r2 * r1 - r2 * r1 * r2)

    # The literal extension by zero from composable edge pairs to E tensor E
    # has an 80-dimensional kernel and cannot be unitary.
    full_edge_tensor_dimension = len(EDGES) ** 2
    zero_extension_rank = face_r.rank()
    assert full_edge_tensor_dimension == 100
    assert zero_extension_rank == 20

    # On the endpoint block (0,2), face_r has eigenvalues -1 on (a,g) and Q
    # on (a,gp).  Appending the edge a gives mixed triples because g/a and
    # gp/a are noncomposable.  If the noncomposable pair sector is completed
    # by a scalar s, the two sides of the braid relation act by
    # s*lambda**2 and s**2*lambda.  Neither allowed Hecke scalar works for
    # both eigenvalues.
    scalar_completion_residuals = {
        "-1 completion on q eigenvector": sp.simplify(
            (-1) * Q**2 - (-1) ** 2 * Q
        ),
        "q completion on -1 eigenvector": sp.simplify(Q - Q**2 * (-1)),
    }
    assert all(value != 0 for value in scalar_completion_residuals.values())

    endpoint_dimensions: Dict[Tuple[str, str], int] = {}
    endpoint_ranks: Dict[Tuple[str, str], int] = {}
    for endpoints, (block_paths, block) in d6_blocks().items():
        endpoint_dimensions[endpoints] = len(block_paths)
        endpoint_ranks[endpoints] = block.rank()

    print("Evans--Pugh D^(6) exact connection audit")
    print(f"vertices: 6")
    print(f"directed edges (with multiplicity): {len(EDGES)}")
    print(f"composable two-edge paths: {len(paths2)}")
    print(f"composable three-edge paths: {len(paths3)}")
    print(f"U rank / dimension: {u2.rank()} / {len(paths2)}")
    print(f"scaled connection eigenvalue multiplicities: -1^{u2.rank()}, q^{len(paths2)-u2.rank()}")
    print("endpoint block dimensions:", endpoint_dimensions)
    print("endpoint block ranks:", endpoint_ranks)
    print("exact Hecke, unitarity, cubic projection, and braid checks: PASS")
    print(
        "zero extension to Edge tensor Edge: "
        f"rank {zero_extension_rank} in dimension {full_edge_tensor_dimension} (NOT UNITARY)"
    )
    print("scalar Hecke completions on noncomposable pairs: FAIL")
    for label, value in scalar_completion_residuals.items():
        print(f"  {label}: residual {value}")
    print("vertex tensor square dimension: 6^2 = 36 (not the connection space)")


if __name__ == "__main__":
    main()
