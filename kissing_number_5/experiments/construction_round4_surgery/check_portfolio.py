#!/usr/bin/env python3
"""Recompute binary64 diagnostics for a contact-surgery portfolio."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import numpy as np

from . import contact_surgery


def graph_summary(n: int, edges: list[list[int]]):
    degrees = [0] * n
    parent = list(range(n))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(first, second):
        first = find(first)
        second = find(second)
        if first != second:
            parent[second] = first

    for first, second in edges:
        degrees[first] += 1
        degrees[second] += 1
        union(first, second)
    histogram = dict(sorted(collections.Counter(degrees).items()))
    components = collections.Counter(find(vertex) for vertex in range(n))
    return histogram, sorted(components.values(), reverse=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.portfolio.read_text())
    assert payload["status"] == contact_surgery.STATUS
    best = {}
    for run in payload["runs"]:
        points = np.asarray(run["coordinates"], dtype=float)
        recomputed = contact_surgery.diagnostics(points)
        stored = run["diagnostics"]
        assert recomputed["coordinate_sha256"] == stored["coordinate_sha256"]
        for key in (
            "maximum_inner_product",
            "minimum_inner_product",
            "norm_error",
        ):
            assert abs(recomputed[key] - stored[key]) <= 2e-14
        assert (
            recomputed["pairs_below_minus_one_half"]
            == stored["pairs_below_minus_one_half"]
        )
        assert recomputed["active_edges_1e-8"] == stored["active_edges_1e-8"]
        n = int(run["n"])
        if (
            n not in best
            or stored["maximum_inner_product"]
            < best[n]["diagnostics"]["maximum_inner_product"]
        ):
            best[n] = run
    assert len(payload["runs"]) == 36
    for n in sorted(best):
        run = best[n]
        edges = run["diagnostics"]["active_edges_1e-8"]
        histogram, components = graph_summary(n, edges)
        print(
            f"N={n} seed={run['seed']} "
            f"max={run['diagnostics']['maximum_inner_product']:.16f} "
            f"active={len(edges)} degrees={histogram} "
            f"components={components}"
        )


if __name__ == "__main__":
    main()
