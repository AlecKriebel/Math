#!/usr/bin/env python3
"""Small numerical probe for three direct theta containment records.

This deliberately reconstructs only the three relevant graphs.  It never
loads the 77 MB atlas pickle (whose object graph has a much larger peak RSS).
"""

from __future__ import annotations

import importlib.util
import sys
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
SPEC = importlib.util.spec_from_file_location("k2p_theta_probe_core", CORE)
assert SPEC is not None and SPEC.loader is not None
atlas = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = atlas
SPEC.loader.exec_module(atlas)


def internal_edges(graph):
    arms = atlas.selected_arm_edges(graph)
    return tuple(edge for edge in graph.edges() if edge not in arms)


def switching_data(graph):
    edges = internal_edges(graph)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    retics = atlas.reticulation_nodes(graph)
    parents = tuple(tuple(sorted(graph.predecessors(node), key=repr)) for node in retics)
    rows = []
    for bits in product((0, 1), repeat=len(retics)):
        removed = set()
        for node, choices, bit in zip(retics, parents, bits):
            keep_parent = choices[bit]
            removed.update((parent, node) for parent in choices if parent != keep_parent)
        kept = tuple(edge for edge in graph.edges() if edge not in removed)
        masks = atlas.descendant_masks_for_switch(graph, kept)
        rows.append((bits, tuple((edge_index[edge], masks[edge]) for edge in edges if edge in masks)))
    return edges, tuple(rows)


def map_function(graph):
    edges, switches = switching_data(graph)
    characters = atlas.orbit_assignments(4)

    def evaluate(parameters):
        pairs = np.asarray(parameters[: 2 * len(edges)], dtype=float).reshape(len(edges), 2)
        lambdas = np.asarray(parameters[2 * len(edges) :], dtype=float)
        outputs = []
        for chars in characters:
            total = 0.0
            for bits, visible in switches:
                weight = 1.0
                for bit, inheritance in zip(bits, lambdas):
                    weight *= inheritance if bit else (1.0 - inheritance)
                monomial = 1.0
                for edge_index, mask in visible:
                    sector = atlas.sector_for_mask(mask, chars)
                    if sector:
                        monomial *= pairs[edge_index, sector - 1]
                total += weight * monomial
            outputs.append(total)
        return np.asarray(outputs)

    return edges, evaluate


def source_point(seed):
    rng = np.random.default_rng(seed)
    # Stay well inside D_+ while retaining enough heterogeneity to reveal maps.
    pairs = []
    for _ in range(8):
        s = rng.uniform(0.48, 0.82)
        g = rng.uniform(max(0.42, 2.0 * s - 0.96), 0.91)
        pairs.extend((s, g))
    pairs.extend(rng.uniform(0.22, 0.78, size=2))
    return np.asarray(pairs)


def solve_case(source_graph, target_graph, seed, algebraic=False):
    source_edges, source_map = map_function(source_graph)
    target_edges, target_map = map_function(target_graph)
    source_parameters = source_point(seed)
    observed = source_map(source_parameters)
    # Graph-aligned warm start.  Multiple deterministic perturbations protect
    # against a poor local chart while keeping the solve tiny.
    rng = np.random.default_rng(seed + 1000)
    starts = [source_parameters.copy()]
    starts.extend(np.clip(source_parameters + rng.normal(0.0, 0.08, 18), 0.08, 0.94) for _ in range(7))
    best = None
    lower = np.r_[np.full(16, -3.0 if algebraic else 0.001), np.full(2, 0.001)]
    upper = np.r_[np.full(16, 3.0 if algebraic else 1.4), np.full(2, 0.999)]
    for start in starts:
        result = least_squares(
            lambda candidate: target_map(candidate)[1:] - observed[1:],
            start,
            bounds=(lower, upper),
            xtol=1e-13,
            ftol=1e-13,
            gtol=1e-13,
            max_nfev=5000,
            x_scale="jac",
        )
        if best is None or np.linalg.norm(result.fun, ord=np.inf) < np.linalg.norm(best.fun, ord=np.inf):
            best = result
    assert best is not None
    print("source edges", source_edges)
    print("target edges", target_edges)
    print("source", np.array2string(source_parameters, precision=10, separator=","))
    print("target", np.array2string(best.x, precision=10, separator=","))
    print("residual_inf", np.linalg.norm(best.fun, ord=np.inf), "cost", best.cost, "nfev", best.nfev)
    print("target_Dplus", [
        bool(0 < best.x[2*i] < 1 and 0 < best.x[2*i+1] < 1 and best.x[2*i+1] > 2*best.x[2*i]-1)
        for i in range(8)
    ])


def main():
    sources = atlas.source_supports()
    target = atlas.target_completions(4, True)[822]
    cases = (
        ("source2-class112", sources[2].graph, target.graph, 112),
        ("source2-class113", sources[2].graph, atlas.relabel_record(target, (0, 1, 3, 2)).graph, 113),
        ("source4-class8", sources[4].graph, target.graph, 408),
    )
    for name, source_graph, target_graph, seed in cases:
        print("\n===", name, "===")
        solve_case(source_graph, target_graph, seed, algebraic=True)


if __name__ == "__main__":
    main()
