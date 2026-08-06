#!/usr/bin/env python3
"""Exact weak-reversibility cone certificates.

For each reaction r:y->y', a directed return path y'~>y writes -zeta_r as
a nonnegative integer sum of reaction vectors.  Consequently the nonnegative
reaction cone equals the stoichiometric span.
"""
from __future__ import annotations

from collections import deque, defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from src.generator import Reaction  # type: ignore  # noqa:E402
from src.class_analyzer import is_weakly_reversible  # type: ignore  # noqa:E402


@dataclass(frozen=True, slots=True)
class ReturnPathCertificate:
    reaction_index: int
    return_indices: tuple[int, ...]
    vector_sum: tuple[int, ...]


def _adjacency(reactions: Sequence[Reaction]) -> dict[tuple[int, ...], list[tuple[tuple[int, ...], int]]]:
    out: dict[tuple[int, ...], list[tuple[tuple[int, ...], int]]] = defaultdict(list)
    for idx, r in enumerate(reactions):
        out[r.source].append((r.target, idx))
        out.setdefault(r.target, [])
    for y in out:
        out[y].sort(key=lambda pair: (pair[0], pair[1]))
    return dict(out)


def directed_return_path(reactions: Sequence[Reaction], reaction_index: int) -> tuple[int, ...]:
    """Return deterministic shortest directed path from target to source."""
    if not (0 <= reaction_index < len(reactions)):
        raise IndexError("reaction_index out of range")
    r = reactions[reaction_index]
    start, goal = r.target, r.source
    graph = _adjacency(reactions)
    queue = deque([start])
    parent: dict[tuple[int, ...], tuple[tuple[int, ...], int] | None] = {start: None}
    while queue:
        y = queue.popleft()
        if y == goal:
            break
        for yp, idx in graph.get(y, []):
            if yp not in parent:
                parent[yp] = (y, idx)
                queue.append(yp)
    if goal not in parent:
        raise ValueError("no directed return path; network is not weakly reversible on this edge")
    path: list[int] = []
    y = goal
    while y != start:
        prev, idx = parent[y]  # type: ignore[misc]
        path.append(idx)
        y = prev
    path.reverse()
    return tuple(path)


def return_path_certificate(reactions: Sequence[Reaction], reaction_index: int) -> ReturnPathCertificate:
    path = directed_return_path(reactions, reaction_index)
    d = reactions[0].dimension
    total = [0] * d
    for idx in path:
        for i, v in enumerate(reactions[idx].vector):
            total[i] += v
    expected = tuple(-v for v in reactions[reaction_index].vector)
    if tuple(total) != expected:
        raise AssertionError("return path vectors do not sum to the negative reaction vector")
    return ReturnPathCertificate(reaction_index, path, tuple(total))


def all_return_path_certificates(reactions: Sequence[Reaction]) -> tuple[ReturnPathCertificate, ...]:
    if not reactions:
        raise ValueError("empty reaction list")
    if not is_weakly_reversible(reactions):
        raise ValueError("network is not weakly reversible")
    return tuple(return_path_certificate(reactions, i) for i in range(len(reactions)))


def verify_cone_representation(
    reactions: Sequence[Reaction], coefficients: Sequence[int]
) -> tuple[int, ...]:
    if len(coefficients) != len(reactions) or any(c < 0 for c in coefficients):
        raise ValueError("coefficients must be a nonnegative vector of reaction multiplicities")
    d = reactions[0].dimension
    total = [0] * d
    for c, r in zip(coefficients, reactions):
        for i, v in enumerate(r.vector):
            total[i] += c * v
    return tuple(total)


def self_test() -> None:
    rs = [
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    ]
    certs = all_return_path_certificates(rs)
    assert len(certs) == 3
    for cert in certs:
        assert cert.vector_sum == tuple(-v for v in rs[cert.reaction_index].vector)


if __name__ == "__main__":
    self_test()
    print("cone_lemma.py self-test: OK")
