#!/usr/bin/env python3
"""Construct and verify a finite enabling buffer for a reaction multiset."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from src.generator import Reaction  # type: ignore  # noqa:E402


@dataclass(frozen=True, slots=True)
class BufferedWordCertificate:
    order: tuple[int, ...]
    initial_buffer: tuple[int, ...]
    states: tuple[tuple[int, ...], ...]
    final_state: tuple[int, ...]
    net_vector: tuple[int, ...]


def expand_multiset(counts: Sequence[int]) -> tuple[int, ...]:
    if any(c < 0 for c in counts):
        raise ValueError("counts must be nonnegative")
    return tuple(idx for idx, c in enumerate(counts) for _ in range(c))


def enabling_buffer(reactions: Sequence[Reaction], order: Sequence[int]) -> tuple[int, ...]:
    if not reactions:
        raise ValueError("empty reaction list")
    d = reactions[0].dimension
    prefix = [0] * d
    need = [0] * d
    for idx in order:
        r = reactions[idx]
        for i in range(d):
            need[i] = max(need[i], r.source[i] - prefix[i])
        for i, v in enumerate(r.vector):
            prefix[i] += v
    return tuple(max(0, v) for v in need)


def construct_buffered_word(
    reactions: Sequence[Reaction], counts: Sequence[int], order: Sequence[int] | None = None
) -> BufferedWordCertificate:
    if len(counts) != len(reactions):
        raise ValueError("count vector length mismatch")
    if order is None:
        order = expand_multiset(counts)
    else:
        seen = [0] * len(reactions)
        for idx in order:
            seen[idx] += 1
        if tuple(seen) != tuple(counts):
            raise ValueError("order does not realize the supplied multiset")
    order = tuple(order)
    x = enabling_buffer(reactions, order)
    states = [x]
    for idx in order:
        r = reactions[idx]
        if not r.enabled(x):
            raise AssertionError("prefix-deficit buffer failed to enable the word")
        x = r.fire(x)
        states.append(x)
    net = tuple(states[-1][i] - states[0][i] for i in range(len(states[0])))
    return BufferedWordCertificate(order, states[0], tuple(states), states[-1], net)


def self_test() -> None:
    rs = [
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    ]
    cert = construct_buffered_word(rs, (0, 1, 0), order=(1,))
    assert cert.initial_buffer == (1, 1)
    assert cert.final_state == (0, 1)
    assert cert.net_vector == (-1, 0)


if __name__ == "__main__":
    self_test()
    print("buffered_word.py self-test: OK")
