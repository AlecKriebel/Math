#!/usr/bin/env python3
"""Backward dead-state calculus for an all-distinct witnessed path.

A state is dead when a forced-H attack is undominated, or when one
unoccupied attack has every one-guard response either blocked by a forced
H-edge or leading to an already dead state.  Unknown graph edges are never
treated as nonedges, so every derived death is valid in every completion.
"""

from __future__ import annotations

import argparse
import itertools
import json


State = tuple[int, int, int]


def normalize(vertices) -> State:
    answer = tuple(sorted(vertices))
    if len(answer) != 3 or len(set(answer)) != 3:
        raise ValueError("not a triple")
    return answer


def derive(path_length: int) -> dict[str, object]:
    rim_order = path_length + 1
    witness_start = rim_order
    target = witness_start + path_length
    vertices = tuple(range(target + 1))
    states = tuple(itertools.combinations(vertices, 3))
    forced_h: set[tuple[int, int]] = set()

    def pair(first: int, second: int) -> tuple[int, int]:
        return tuple(sorted((first, second)))

    for index in range(path_length):
        forced_h.add(pair(index, index + 1))
        witness = witness_start + index
        forced_h.add(pair(index, witness))
        forced_h.add(pair(index + 1, witness))

    dead: dict[State, dict[str, object]] = {}
    for index in range(path_length):
        witness = witness_start + index
        for endpoint in (index, index + 1):
            state = normalize(
                {index, index + 1, witness} - {endpoint} | {target}
            )
            dead[state] = {
                "kind": "assumed-inactive-successor",
                "edge_index": index,
                "endpoint": endpoint,
            }
    endpoint_state = normalize((0, path_length, target))
    dead[endpoint_state] = {"kind": "assumed-endpoint-dead"}

    changed = True
    while changed:
        changed = False
        for state in states:
            if state in dead:
                continue
            for attacked in vertices:
                if attacked in state:
                    continue
                blocked_or_dead = []
                valid = True
                for guard in state:
                    if pair(guard, attacked) in forced_h:
                        blocked_or_dead.append(
                            {"guard": guard, "reason": "forced-H-edge"}
                        )
                        continue
                    successor = normalize(
                        (set(state) - {guard}) | {attacked}
                    )
                    if successor not in dead:
                        valid = False
                        break
                    blocked_or_dead.append(
                        {
                            "guard": guard,
                            "reason": "dead-successor",
                            "successor": successor,
                        }
                    )
                if valid:
                    dead[state] = {
                        "kind": "dead-under-attack",
                        "attacked": attacked,
                        "responses": blocked_or_dead,
                    }
                    changed = True
                    break

    named_states = [
        normalize((index, index + 1, witness_start + index))
        for index in range(path_length)
    ]
    dead_named = [state for state in named_states if state in dead]
    return {
        "schema": "inactive-path-dead-state-saturation-v1",
        "classification": "PROVED-FINITE-CALCULUS",
        "path_length": path_length,
        "order": len(vertices),
        "forced_h_edges": sorted(forced_h),
        "dead_state_count": len(dead),
        "state_count": len(states),
        "named_states": named_states,
        "dead_named_states": dead_named,
        "contradiction": bool(dead_named),
        "derivations": {
            ",".join(map(str, state)): reason
            for state, reason in sorted(dead.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path-length", required=True, type=int)
    arguments = parser.parse_args()
    print(json.dumps(derive(arguments.path_length), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
