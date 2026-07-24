#!/usr/bin/env python3
"""Exact countermodel to code-axis count/mass/individual-weight constraints.

This is only a graph-and-weight relaxation, not a Gram matrix or code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json


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
    assert sum(weights) == 1
    assert all(weight <= Q(1, 6) for weight in weights)
    for vertex, neighbors in enumerate(deep_neighbors):
        assert len(neighbors) == 4 >= 2
        assert all(vertex in deep_neighbors[neighbor] for neighbor in neighbors)
        assert sum(weights[neighbor] for neighbor in neighbors) == Q(4, 41)
        assert Q(4, 41) >= Q(9, 98)
        required_one_fifth_mass = (1 - 6 * weights[vertex]) / 12
        assert required_one_fifth_mass == Q(35, 492)
        assert Q(4, 41) == Q(48, 492) >= required_one_fifth_mass
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
