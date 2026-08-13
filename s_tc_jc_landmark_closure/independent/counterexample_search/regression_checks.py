#!/usr/bin/env python3
"""Independent convention/Fourier regressions, including the frozen pair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from clean_graph import MixedGraph, T_class_code, canonical_mixed_code, class_membership, edge_key, isomorphic, level
from fourier_engine import build_model, evaluate_fraction


def theta_graph(target: bool) -> MixedGraph:
    n = 4
    A, B, C, D, E, F = range(4, 10)
    edges = [(A, C), (A, B), (B, C), (C, D), (D, E), (A, F), (E, F)]
    pendants = [(E, 0), (D, 1), (F, 2), (B, 3)] if target else [(B, 0), (D, 1), (F, 2), (E, 3)]
    edges += pendants
    arrows = {
        edge_key(A, C): {C},
        edge_key(B, C): {C},
        edge_key(A, F): {F},
        edge_key(E, F): {F},
    }
    return MixedGraph.make(n, 6, {C, F}, edges, arrows)


def rooting_on(graph: MixedGraph, edge: tuple[int, int]):
    _, roots = class_membership(graph)
    wanted = edge_key(*edge)
    return next(r for r in roots if r.root_edge == wanted)


def parameter_vector(model, edge_values, lambdas):
    values = []
    for arc in model.arcs:
        if arc not in edge_values:
            raise KeyError(arc)
        values.append(edge_values[arc])
    values.extend(lambdas[r] for r in model.reticulations)
    return values


def main() -> None:
    source = theta_graph(False)
    target = theta_graph(True)
    A, B, C, D, E, F = range(4, 10)
    root = 10

    source_membership, source_roots = class_membership(source)
    target_membership, target_roots = class_membership(target)
    assert source_membership == target_membership == "W_TC_NOT_S_TC"
    assert len(source_roots) == len(target_roots) == 5
    assert sum(r.tree_child for r in source_roots) == sum(r.tree_child for r in target_roots) == 2
    assert level(source) == level(target) == 2
    assert not isomorphic(source, target)
    assert T_class_code(source) != T_class_code(target)

    source_model = build_model(source, rooting_on(source, (A, C)))
    target_model = build_model(target, rooting_on(target, (A, C)))

    beta = sp.Symbol("beta")
    minpoly = 43337075 * beta**2 - 36083110 * beta + 7336259
    half = sp.Rational(1, 2)
    source_edges = {
        (root, A): sp.Rational(2, 3),
        (root, C): sp.Rational(3, 4),
        (A, B): sp.Rational(3, 5),
        (B, C): half,
        (C, D): sp.Rational(9, 20),
        (D, E): sp.Rational(2, 5),
        (A, F): half,
        (E, F): sp.Rational(1, 3),
        (B, 0): sp.Rational(1, 5),
        (D, 1): half,
        (F, 2): half,
        (E, 3): sp.Rational(3, 8),
    }
    target_edges = {
        (root, A): sp.Rational(2, 3),
        (root, C): sp.Rational(3, 4),
        (A, B): 24835 * beta / (20678 - 24835 * beta),
        (B, C): half,
        (C, D): sp.Rational(9934, 12215),
        (D, E): sp.Rational(171, 775),
        (A, F): sp.Rational(10339, 53010) / beta,
        (E, F): half,
        (E, 0): sp.Rational(31, 190),
        (D, 1): half,
        (F, 2): sp.Rational(1767, 4832),
        (B, 3): sp.Rational(3, 20) / beta,
    }
    lambdas = {C: half, F: half}
    source_values = evaluate_fraction(source_model, parameter_vector(source_model, source_edges, lambdas))
    target_values = evaluate_fraction(target_model, parameter_vector(target_model, target_edges, lambdas))
    remainder_records = []
    for index, (left, right) in enumerate(zip(source_values, target_values)):
        numerator = sp.together(left - right).as_numer_denom()[0]
        remainder = sp.rem(sp.Poly(numerator, beta), sp.Poly(minpoly, beta)).as_expr()
        remainder = sp.factor(remainder)
        assert remainder == 0, (index, remainder)
        remainder_records.append({"coordinate": list(source_model.coordinates[index]), "remainder": "0"})

    report = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED",
        "source_membership": source_membership,
        "target_membership": target_membership,
        "admissible_rootings_each": len(source_roots),
        "tree_child_rootings_each": sum(r.tree_child for r in source_roots),
        "isomorphic": False,
        "ordinary_T_equivalent": False,
        "JC_orbit_coordinate_count": len(source_values),
        "quadratic_remainders": remainder_records,
        "interpretation": "The clean-room graph and Fourier engines reproduce the frozen four-leaf equality while excluding the pair from S_TC.",
    }
    path = Path("regression_certificate.json")
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

