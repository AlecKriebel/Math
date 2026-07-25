"""Command-line evaluator for verifier B."""

from __future__ import annotations

import argparse
import json

from .eternal import eternal_domination_number, make_eternal_certificate
from .graph import Graph
from .invariants import (
    clique_cover_number,
    domination_number,
    independence_number,
    independent_domination_number,
    minimum_clique_partition,
)


def _ordered(configuration: frozenset[int]) -> list[int]:
    return sorted(configuration)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="independent exact set-based graph evaluator"
    )
    parser.add_argument("graph6", help="one graph6 record")
    parser.add_argument(
        "--family",
        action="store_true",
        help="include an explicit eternal family and one response per attack",
    )
    arguments = parser.parse_args()

    graph = Graph.from_graph6(arguments.graph6)
    gamma_infinity = eternal_domination_number(graph)
    partition = minimum_clique_partition(graph)
    output: dict[str, object] = {
        "graph6": graph.to_graph6(),
        "n": graph.order,
        "m": graph.size,
        "gamma": domination_number(graph),
        "i": independent_domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity_one_guard": gamma_infinity,
        "theta": clique_cover_number(graph),
        "clique_partition": [_ordered(part) for part in partition],
    }

    if arguments.family:
        certificate = make_eternal_certificate(graph, gamma_infinity)
        if certificate is None:
            raise AssertionError("optimum must have an eternal certificate")
        output["eternal_family"] = [
            _ordered(configuration)
            for configuration in sorted(
                certificate.family, key=lambda item: tuple(sorted(item))
            )
        ]
        output["responses"] = [
            {
                "configuration": _ordered(move.source),
                "attack": move.attack,
                "guard": move.guard,
                "successor": _ordered(move.target),
            }
            for move in certificate.responses
        ]

    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
