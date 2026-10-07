#!/usr/bin/env python3
"""Explicit matrix-liveness source and block pullback, with finite-run semantics.

This is a finite-instance test artifact for the uniform proofs in
agent_notes/binary_compiler.md; it does not certify upstream lower bounds.
Only the Python standard library is required.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from random import Random
from typing import Callable, Hashable, Iterable
import argparse
import json
import platform

LEFT, RIGHT = "<", ">"
State = Hashable
Move = tuple[State, int]


@dataclass
class Machine:
    states: tuple[State, ...]
    initial: State
    accepting: frozenset[State]
    transition: Callable[[State, object], tuple[Move, ...]]

    def accepts(self, word: Iterable[object], positive: bool = False) -> bool:
        """Configuration reachability; repeated configurations need not be unrolled.

        A finite run accepts. Missing transitions and infinite nonaccepting runs
        reject. The extra flag implements positive-transition acceptance exactly.
        """
        tape = (LEFT, *tuple(word), RIGHT)
        start = (self.initial, 0, False)
        pending, seen = [start], {start}
        while pending:
            state, pos, moved = pending.pop()
            if state in self.accepting and (moved or not positive):
                return True
            for target, direction in self.transition(state, tape[pos]):
                assert target in self.states
                assert direction in (-1, 0, 1)
                new_pos = pos + direction
                assert 0 <= new_pos < len(tape), "endmarker crossed"
                config = (target, new_pos, True)
                if config not in seen:
                    seen.add(config)
                    pending.append(config)
        return False


def encode(h: int, relations: Iterable[int]) -> tuple[int, ...]:
    """Bit t=ph+q is the indicator of relation edge (p,q)."""
    width = h * h
    return tuple((relation >> t) & 1 for relation in relations for t in range(width))


def matrix_liveness(h: int, bits: Iterable[int]) -> bool:
    bits = tuple(bits)
    width = h * h
    if len(bits) % width:
        return False
    reachable = set(range(h))
    for start in range(0, len(bits), width):
        reachable = {
            q for p in reachable for q in range(h) if bits[start + p * h + q]
        }
    return bool(reachable)


def binary_liveness_source(h: int) -> Machine:
    """Exactly (3h^3-h)/2+2 states; interior transitions all move right.

    U(p,t): next bit is t, and the edge from p is not chosen yet.
    V(q,t): edge into q was chosen, and next bit is t.
    States are trimmed to the exact ranges justified in the written proof.
    """
    assert h >= 1
    width = h * h
    initial, accepting = ("initial",), ("accept",)
    before = tuple(("U", p, t) for p in range(h) for t in range((p + 1) * h))
    after = tuple(("V", q, t) for q in range(h) for t in range(q + 1, width))
    states = (initial, accepting, *before, *after)
    assert len(states) == (3 * h**3 - h) // 2 + 2

    def transition(state: State, symbol: object) -> tuple[Move, ...]:
        if state == initial:
            return tuple((("U", p, 0), 1) for p in range(h)) if symbol == LEFT else ()
        if state == accepting:
            return ()
        kind, vertex, offset = state
        if symbol == RIGHT:
            return ((accepting, 0),) if kind == "U" and offset == 0 else ()
        if symbol not in (0, 1):
            return ()
        if kind == "U":
            out = []
            if offset < (vertex + 1) * h - 1:
                out.append((("U", vertex, offset + 1), 1))
            if symbol == 1 and offset // h == vertex:
                next_vertex = offset % h
                destination = (
                    ("U", next_vertex, 0)
                    if offset == width - 1
                    else ("V", next_vertex, offset + 1)
                )
                out.append((destination, 1))
            return tuple(out)
        destination = (
            ("U", vertex, 0)
            if offset == width - 1
            else ("V", vertex, offset + 1)
        )
        return ((destination, 1),)

    return Machine(states, initial, frozenset({accepting}), transition)


def pullback(h: int, binary: Machine) -> Machine:
    """Compile an s-state binary 2FA into exactly sh^2 relation states.

    Marker transition rows ignore the stored phase. This removes any need for
    marker-specific copies or extra normalization transitions.
    """
    width = h * h
    states = tuple((state, offset) for state in binary.states for offset in range(width))

    def transition(state: State, symbol: object) -> tuple[Move, ...]:
        original, offset = state
        if symbol == LEFT:
            out = []
            for target, direction in binary.transition(original, LEFT):
                assert direction in (0, 1)
                out.append(((target, 0 if direction == 1 else offset), direction))
            return tuple(out)
        if symbol == RIGHT:
            out = []
            for target, direction in binary.transition(original, RIGHT):
                assert direction in (-1, 0)
                out.append(((target, width - 1 if direction == -1 else offset), direction))
            return tuple(out)
        bit = (symbol >> offset) & 1
        out = []
        for target, direction in binary.transition(original, bit):
            if direction == 0:
                out.append(((target, offset), 0))
            elif direction == 1:
                out.append(((target, (offset + 1) % width), int(offset == width - 1)))
            else:
                assert direction == -1
                out.append(((target, (offset - 1) % width), -int(offset == 0)))
        return tuple(out)

    return Machine(
        states, (binary.initial, 0),
        frozenset((state, offset) for state in binary.accepting for offset in range(width)),
        transition,
    )


def words(alphabet: tuple[object, ...], max_length: int):
    for length in range(max_length + 1):
        yield from product(alphabet, repeat=length)


def table_machine(states: int, rows: tuple[tuple[Move, ...], ...], accept: int) -> Machine:
    symbols = (LEFT, 0, 1, RIGHT)
    table = {(state, symbol): rows[4 * state + index]
             for state in range(states) for index, symbol in enumerate(symbols)}
    return Machine(tuple(range(states)), 0,
                   frozenset(state for state in range(states) if accept >> state & 1),
                   lambda state, symbol: table[state, symbol])


def check_fooling_set(h: int) -> int:
    width = h * h
    identity = sum(1 << (p * h + p) for p in range(h))
    identity_bits = encode(h, (identity,))
    pairs = []
    for vertex in range(h):
        singleton = encode(h, (1 << (vertex * h + vertex),))
        for offset in range(width):
            pairs.append((singleton + identity_bits[:offset],
                          identity_bits[offset:] + singleton))
    for index, (prefix, suffix) in enumerate(pairs):
        assert matrix_liveness(h, prefix + suffix)
        for other, (_, other_suffix) in enumerate(pairs):
            if other != index:
                assert not matrix_liveness(h, prefix + other_suffix)
    return len(pairs)


def exhaustive_checks() -> dict[str, object]:
    counts = {"source_words": 0, "pullback_cases": 0, "fooling_pairs": 0,
              "deterministic_machines": 0, "sampled_machines": 0}
    for h, limit in ((1, 8), (2, 9)):
        source = binary_liveness_source(h)
        for word in words((0, 1), limit):
            truth = matrix_liveness(h, word)
            assert source.accepts(word) == truth
            assert source.accepts(word, positive=True) == truth
            counts["source_words"] += 1
    for h in (1, 2, 3, 4):
        counts["fooling_pairs"] += check_fooling_set(h)

    # All one-state partial deterministic machines with legal marker rows.
    choices = (
        ((), ((0, 0),), ((0, 1),)),
        ((), ((0, -1),), ((0, 0),), ((0, 1),)),
        ((), ((0, -1),), ((0, 0),), ((0, 1),)),
        ((), ((0, -1),), ((0, 0),)),
    )
    inputs = tuple(words(tuple(range(16)), 2))
    for rows in product(*choices):
        for accepting in range(2):
            binary = table_machine(1, rows, accepting)
            relation = pullback(2, binary)
            counts["deterministic_machines"] += 1
            for word in inputs:
                encoded = encode(2, word)
                for positive in (False, True):
                    assert relation.accepts(word, positive) == binary.accepts(encoded, positive)
                    counts["pullback_cases"] += 1

    # Reproducible two-/three-state samples with multiple successors, partial
    # rows, both directions, stays, marker loops, and interior cycles.
    random = Random(129)
    for states in (2, 3):
        for _ in range(64):
            rows = []
            for state in range(states):
                for directions in ((0, 1), (-1, 0, 1), (-1, 0, 1), (-1, 0)):
                    choices_here = tuple((target, d) for target in range(states) for d in directions)
                    rows.append(tuple(move for move in choices_here if random.randrange(4) == 0))
            binary = table_machine(states, tuple(rows), random.randrange(1 << states))
            relation = pullback(2, binary)
            counts["sampled_machines"] += 1
            for word in inputs:
                encoded = encode(2, word)
                for positive in (False, True):
                    assert relation.accepts(word, positive) == binary.accepts(encoded, positive)
                    counts["pullback_cases"] += 1
    return {"status": "passed", "python": platform.python_version(), **counts,
            "source_state_counts": {str(h): len(binary_liveness_source(h).states)
                                    for h in range(1, 9)},
            "scope": "Uniform encoding lemmas only; no upstream lower bound checked."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Optional JSON receipt path")
    arguments = parser.parse_args()
    result = exhaustive_checks()
    report = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        with open(arguments.output, "w", encoding="utf-8") as output:
            output.write(report)
    print(report, end="")
