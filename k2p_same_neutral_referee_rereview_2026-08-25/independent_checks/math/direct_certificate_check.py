#!/usr/bin/env python3
"""Independent symbolic replay of printed direct certificate R4Q-03.

The two rooted graph literals are transcribed from the source-0 and target-77
descriptor records bound to raw row 1849.  This script imports no submitted
model-map, classifier, certificate, graph builder, or canonicalizer.
"""

from __future__ import annotations

import hashlib
import itertools
import json

import sympy as sp


def edge_value(character, s, g):
    if character == 0:
        return 1
    return g if character == 2 else s


def network_coordinate(name, arcs, retic_parents, leaf_labels, pattern):
    edge_parameters = {
        edge: sp.symbols(f"s_{name}_{i} g_{name}_{i}")
        for i, edge in enumerate(arcs)
    }
    lambdas = {
        retic: sp.symbols(f"lambda_{name}_{retic}")
        for retic in retic_parents
    }
    total = 0
    retics = tuple(retic_parents)
    for choices in itertools.product((0, 1), repeat=len(retics)):
        selected = set(arcs)
        weight = 1
        for retic, choice in zip(retics, choices):
            parent0, parent1 = retic_parents[retic]
            chosen = parent0 if choice == 0 else parent1
            omitted = parent1 if choice == 0 else parent0
            selected.remove((omitted, retic))
            lam = lambdas[retic]
            weight *= lam if choice == 0 else (1 - lam)

        children = {}
        for u, v in selected:
            children.setdefault(u, []).append(v)
        memo = {}

        def descendant_character(node):
            if node in memo:
                return memo[node]
            value = pattern[leaf_labels[node]] if node in leaf_labels else 0
            for child in children.get(node, ()):
                value ^= descendant_character(child)
            memo[node] = value
            return value

        term = weight
        for edge in arcs:
            if edge not in selected:
                continue
            s, g = edge_parameters[edge]
            term *= edge_value(descendant_character(edge[1]), s, g)
        total += term
    return sp.expand(total)


def certificate_pullback(name, arcs, retic_parents, leaf_labels):
    # Printed four-port coordinate dictionary:
    # q10=C00C, q20=CGGC, q12=C0GT, q18=CG0T.
    patterns = {
        10: (1, 0, 0, 1),
        20: (1, 2, 2, 1),
        12: (1, 0, 2, 3),
        18: (1, 2, 0, 3),
    }
    q = {
        index: network_coordinate(name, arcs, retic_parents, leaf_labels, word)
        for index, word in patterns.items()
    }
    return sp.expand(q[10] * q[20] - q[12] * q[18])


def main():
    source_arcs = (
        ("r", "S"), ("r", "L0"),
        ("S", "U"), ("S", "V"), ("U", "V"),
        ("U", "A2"), ("A2", "X"), ("A2", "L1"),
        ("V", "A3"), ("A3", "X"), ("A3", "L2"),
        ("X", "L3"),
    )
    source_retics = {"V": ("S", "U"), "X": ("A2", "A3")}
    source_labels = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}

    # Target labels already include raw row 1849's port permutation
    # (0,1,3,2). D2 and D3 are zero-character completion leaves.
    target_arcs = (
        ("r", "S"), ("r", "L0"),
        ("S", "U"), ("S", "V"),
        ("U", "A2"), ("A2", "X"), ("A2", "D2"),
        ("V", "A3"), ("A3", "X"), ("A3", "D3"),
        ("U", "A40"), ("A40", "L1"), ("A40", "A41"),
        ("A41", "V"), ("A41", "L3"),
        ("X", "L2"),
    )
    target_retics = {"V": ("S", "A41"), "X": ("A2", "A3")}
    target_labels = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}

    source_pullback = certificate_pullback(
        "src", source_arcs, source_retics, source_labels
    )
    target_pullback = certificate_pullback(
        "tgt", target_arcs, target_retics, target_labels
    )
    assert target_pullback == 0
    assert source_pullback != 0
    source_terms = len(sp.Poly(source_pullback).terms())
    assert source_terms == 44

    payload = {
        "certificate": "R4Q-03: q10*q20-q12*q18",
        "bound_raw_row": 1849,
        "source_descriptor_sha256":
            "ffa19a908a552bb362e0c840df91c95a7db974f700f8ebc7fcce4ac2e5f55cd0",
        "target_descriptor_sha256":
            "7d9d43468513d406e3ea0bbea704f91b9f5c1a8dc58e2651aa8af96079478325",
        "port_permutation": [0, 1, 3, 2],
        "target_pullback_zero": True,
        "source_pullback_nonzero": True,
        "source_pullback_term_count": source_terms,
        "source_pullback_sha256": hashlib.sha256(
            sp.srepr(source_pullback).encode()
        ).hexdigest(),
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    print(encoded, end="")
    print("payload_sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
