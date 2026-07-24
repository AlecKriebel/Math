#!/usr/bin/env python3
"""Exact countermodel to code-axis count/mass/individual-weight constraints.

This is only a graph-and-weight relaxation, not a Gram matrix or code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json


class VerificationError(Exception):
    """Raised when the exact graph-and-weight countermodel check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify() -> dict[str, object]:
    number = 41
    weights = [Q(1, number)] * number
    deep_neighbors = [
        {
            (vertex - 2) % number,
            (vertex - 1) % number,
            (vertex + 1) % number,
            (vertex + 2) % number,
        }
        for vertex in range(number)
    ]
    require(sum(weights) == 1, "weights do not sum to one")
    require(
        all(weight <= Q(1, 6) for weight in weights),
        "individual weight bound failed",
    )
    for vertex, neighbors in enumerate(deep_neighbors):
        require(
            len(neighbors) == 4 and len(neighbors) >= 2,
            f"wrong deep degree at vertex {vertex}",
        )
        require(
            all(vertex in deep_neighbors[neighbor] for neighbor in neighbors),
            f"deep adjacency is not symmetric at vertex {vertex}",
        )
        require(
            sum(weights[neighbor] for neighbor in neighbors) == Q(4, 41),
            f"wrong deep mass at vertex {vertex}",
        )
        require(Q(4, 41) >= Q(9, 98), "universal deep-mass bound failed")
        required_one_fifth_mass = (1 - 6 * weights[vertex]) / 12
        require(
            required_one_fifth_mass == Q(35, 492),
            f"wrong one-fifth threshold at vertex {vertex}",
        )
        require(
            Q(4, 41) == Q(48, 492)
            and Q(48, 492) >= required_one_fifth_mass,
            f"one-fifth deep-mass bound failed at vertex {vertex}",
        )
    return {
        "status": "PASS",
        "scope": (
            "exact code-axis deep-graph/weight relaxation; not a Gram matrix"
        ),
        "vertices": number,
        "weight": "1/41",
        "deep_degree": 4,
        "deep_weight_mass": "4/41",
        "required_deep_weight_mass": "9/98",
        "required_one_fifth_deep_mass": "35/492",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
