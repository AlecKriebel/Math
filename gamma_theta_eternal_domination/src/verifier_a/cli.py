"""Command-line interface for verifier A."""

from __future__ import annotations

import argparse
import json

from .core import (
    BitGraph,
    alpha,
    clique_cover,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
)


def _vertices(mask: int) -> list[int]:
    return [vertex for vertex in range(mask.bit_length()) if mask & (1 << vertex)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", help="one graph6 record")
    parser.add_argument(
        "--family",
        action="store_true",
        help="include a greatest eternal family at the optimum",
    )
    args = parser.parse_args()

    graph = BitGraph.from_graph6(args.graph6)
    gamma = domination_number(graph)
    gamma_inf = eternal_domination_number(graph)
    cover = clique_cover(graph)
    output: dict[str, object] = {
        "graph6": graph.to_graph6(),
        "n": graph.n,
        "m": graph.size,
        "gamma": gamma,
        "i": independent_domination_number(graph),
        "alpha": alpha(graph),
        "gamma_infinity_one_guard": gamma_inf,
        "theta": cover.value,
        "clique_partition": [_vertices(part) for part in cover.parts],
    }
    if args.family:
        eternal = eternal_fixed_point(graph, gamma_inf)
        output["eternal_family"] = [
            _vertices(configuration) for configuration in eternal.family
        ]
        output["responses"] = [
            {
                "configuration": _vertices(configuration),
                "attack": attacked,
                "guard": guard,
                "successor": _vertices(successor),
            }
            for (configuration, attacked), (guard, successor) in sorted(
                eternal.responses.items()
            )
        ]
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
