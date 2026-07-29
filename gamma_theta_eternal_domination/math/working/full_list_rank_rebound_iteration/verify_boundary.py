#!/usr/bin/env python3
"""Replay the exact boundary facts used in NOTE.md.

The underlying graph/game implementation is the pinned provisional
completion-fan verifier.  This wrapper adds the new cross-state and
minimum-exit assertions.  A decisive review must still reconstruct the
facts independently.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "full_list_escape_completion_fan" / "verify_control.py"
PINNED_BASE_SHA256 = (
    "4367a4f45504ff34974879f9b97e7e6acd8f09ac3ef5db7f0da45a78c493ff46"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_base():
    actual = hashlib.sha256(BASE.read_bytes()).hexdigest()
    require(actual == PINNED_BASE_SHA256, ("base verifier SHA-256", actual))
    spec = importlib.util.spec_from_file_location("completion_fan_base", BASE)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    m = load_base()
    graph = m.decode_graph6(m.GRAPH6)
    greatest, _, _ = m.greatest_kernel(graph, 3)
    ban = m.color_ban(graph, m.S, m.X, m.U)
    kernel, ranks, _ = m.greatest_kernel(graph, 3, ban)

    first_cross = m.state(m.X, m.Q, m.W)
    second_cross = m.state(m.X, m.R, m.Y)
    first_completion = m.state(m.Q, m.W, m.D)
    second_completion = m.state(m.R, m.Y, m.E)

    first_fan = m.pair_missed_set(graph, m.Q, m.W)
    second_fan = m.pair_missed_set(graph, m.R, m.Y)
    require(first_fan == (m.D,), ("first fan", first_fan))
    require(second_fan == (m.E,), ("second fan", second_fan))
    require(m.X in graph[m.D], "first fan not across target")
    require(m.X in graph[m.E], "second fan not across target")

    for cross, expected_rank in (
        (first_cross, 3),
        (second_cross, 2),
    ):
        require(m.dominates(graph, cross), ("cross nondominating", cross))
        require(cross in greatest, ("cross omitted", cross))
        require(ranks.get(cross) == expected_rank, ("cross rank", cross))

    require(not kernel, "source restricted kernel nonempty")
    require(ranks.get(first_completion) == 2, "first completion rank")
    require(ranks.get(second_completion) == 2, "second completion rank")
    witnesses = m.deletion_witnesses(
        graph, second_completion, ban, ranks
    )
    require(witnesses == (m.V, m.W, m.T), ("second witnesses", witnesses))
    require(m.W not in (m.V, m.T), "nonanchor witness collision")

    responses = tuple(
        endpoint
        for _, endpoint in m.successors(graph, second_completion, m.W)
        if endpoint in greatest
    )
    require(
        responses == (
            m.state(m.W, m.R, m.E),
            m.state(m.Y, m.W, m.R),
        ),
        ("nonanchor responses", responses),
    )
    require(
        all(ranks.get(endpoint) == 1 for endpoint in responses),
        ("nonanchor response ranks", responses),
    )

    result = {
        "schema": "full-list-rank-rebound-boundary-v1",
        "graph6": m.GRAPH6,
        "parameters": {
            "gamma": m.exact_gamma(graph),
            "i": m.exact_i(graph),
            "alpha": m.exact_alpha(graph),
            "gamma_infinity": m.exact_eternal_number(graph),
            "theta": m.exact_theta(graph),
        },
        "greatest_family_size": len(greatest),
        "source_kernel_size": len(kernel),
        "completion_fans": {
            "first": list(first_fan),
            "second": list(second_fan),
        },
        "crosses": {
            "first": {
                "state": list(first_cross),
                "dominates": True,
                "retained": True,
                "rank": ranks[first_cross],
            },
            "second": {
                "state": list(second_cross),
                "dominates": True,
                "retained": True,
                "rank": ranks[second_cross],
            },
        },
        "second_completion": {
            "state": list(second_completion),
            "rank": ranks[second_completion],
            "deletion_witnesses": list(witnesses),
            "nonanchor_witness": m.W,
            "nonanchor_responses": [
                {"state": list(endpoint), "rank": ranks[endpoint]}
                for endpoint in responses
            ],
        },
        "scope": (
            "exact gamma-two boundary; not an equality graph and not a "
            "gamma-theta counterexample"
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
