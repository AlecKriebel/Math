#!/usr/bin/env python3
"""Fail-closed mutations for the two-step obstruction certificate verifier."""

from __future__ import annotations

from dataclasses import replace
from itertools import combinations
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from search.two_step_obstruction import (  # noqa: E402
    FailedFirstMove,
    FailedSecondMove,
    find_two_step_obstruction,
    legal_dominating_successors,
    verify_two_step_obstruction,
)
from verifier_a.core import BitGraph  # noqa: E402


def require_rejected(label: str, graph: BitGraph, value: object) -> None:
    if verify_two_step_obstruction(graph, value):  # type: ignore[arg-type]
        raise AssertionError(f"mutation accepted: {label}")


def main() -> None:
    started = time.monotonic()
    graph = BitGraph.cycle(7)
    original = find_two_step_obstruction(graph)
    assert original is not None
    assert verify_two_step_obstruction(graph, original)
    immediate, second = original.failed_first_moves
    assert immediate.first_undominated is not None
    assert second.second_attack is not None
    assert second.second_failures

    mutations: list[tuple[str, object]] = [
        ("wrong certificate class", object()),
        ("negative independent mask", replace(original, independent_set=-1)),
        ("outside independent bit", replace(original, independent_set=1 << graph.n)),
        ("Boolean independent mask", replace(original, independent_set=True)),
        ("nonmaximum independent mask", replace(original, independent_set=5)),
        ("nonindependent three-set", replace(original, independent_set=7)),
        ("occupied first attack", replace(original, attack=0)),
        ("Boolean first attack", replace(original, attack=True)),
        ("out-of-range first attack", replace(original, attack=graph.n)),
        (
            "first records stored as list",
            replace(original, failed_first_moves=list(original.failed_first_moves)),
        ),
        (
            "missing first guard",
            replace(original, failed_first_moves=(immediate,)),
        ),
        (
            "duplicate first guard",
            replace(original, failed_first_moves=(immediate, immediate)),
        ),
        (
            "nonrecord first entry",
            replace(original, failed_first_moves=(object(), second)),
        ),
        (
            "wrong first guard",
            replace(
                original,
                failed_first_moves=(replace(immediate, guard=4), second),
            ),
        ),
        (
            "Boolean first guard",
            replace(
                original,
                failed_first_moves=(replace(immediate, guard=True), second),
            ),
        ),
        (
            "false immediate witness",
            replace(
                original,
                failed_first_moves=(
                    replace(immediate, first_undominated=0),
                    second,
                ),
            ),
        ),
        (
            "both first-record modes populated",
            replace(
                original,
                failed_first_moves=(
                    replace(
                        immediate,
                        second_attack=3,
                        second_failures=(FailedSecondMove(4, 5),),
                    ),
                    second,
                ),
            ),
        ),
        (
            "neither first-record mode populated",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_attack=None,
                        second_failures=(),
                    ),
                ),
            ),
        ),
        (
            "occupied second attack",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(second, second_attack=0),
                ),
            ),
        ),
        (
            "Boolean second attack",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(second, second_attack=True),
                ),
            ),
        ),
        (
            "out-of-range second attack",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(second, second_attack=graph.n),
                ),
            ),
        ),
        (
            "second failures stored as list",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=list(second.second_failures),
                    ),
                ),
            ),
        ),
        (
            "missing second guard",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(second, second_failures=()),
                ),
            ),
        ),
        (
            "duplicate second guard",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=second.second_failures * 2,
                    ),
                ),
            ),
        ),
        (
            "wrong second guard",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=(FailedSecondMove(0, 5),),
                    ),
                ),
            ),
        ),
        (
            "Boolean second guard",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=(FailedSecondMove(True, 5),),
                    ),
                ),
            ),
        ),
        (
            "false second witness",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=(FailedSecondMove(4, 0),),
                    ),
                ),
            ),
        ),
        (
            "out-of-range second witness",
            replace(
                original,
                failed_first_moves=(
                    immediate,
                    replace(
                        second,
                        second_failures=(FailedSecondMove(4, graph.n),),
                    ),
                ),
            ),
        ),
    ]
    for label, value in mutations:
        require_rejected(label, graph, value)

    complete = BitGraph.from_edges(4, combinations(range(4), 2))
    occupied_state = sum(1 << vertex for vertex in (0, 1, 2))
    helper_rejections = 0
    for configuration, attacked in (
        (occupied_state, 0),
        (occupied_state, -1),
        (occupied_state, complete.n),
        (occupied_state, True),
        (-1, 3),
        (1 << complete.n, 3),
        (True, 3),
    ):
        try:
            tuple(
                legal_dominating_successors(
                    complete, configuration, attacked
                )
            )
        except ValueError:
            helper_rejections += 1
        else:
            raise AssertionError("successor helper accepted malformed input")

    print(
        json.dumps(
            {
                "status": "all decisive certificate mutations rejected",
                "decisive_mutations": len(mutations),
                "successor_helper_malformed_inputs_rejected": helper_rejections,
                "wall_seconds": time.monotonic() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
