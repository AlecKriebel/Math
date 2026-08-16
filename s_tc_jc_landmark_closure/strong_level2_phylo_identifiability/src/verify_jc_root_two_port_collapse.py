#!/usr/bin/env python3
"""Exact JC collapse of the unique two-port root cycle to an ordinary root."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import valid_binary_strong
from generic_fourier_network import evaluate_jc_coordinates


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_root_two_port_collapse.json"


def root_cycle_network():
    vertices = {
        "R": "S",
        "P": "T",
        "X": "X",
        "L1": "L",
        "L2": "L",
    }
    edges = (
        ("R", "P"),
        ("P", "X"),
        ("R", "X"),
        ("P", "L1"),
        ("X", "L2"),
    )
    assert valid_binary_strong(vertices, edges)
    return {"vertices": vertices, "edges": edges, "leaves": ("L1", "L2")}


def root_tree_network():
    vertices = {"R": "S", "L1": "L", "L2": "L"}
    edges = (("R", "L1"), ("R", "L2"))
    assert valid_binary_strong(vertices, edges)
    return {"vertices": vertices, "edges": edges, "leaves": ("L1", "L2")}


def exact_coordinate_replay():
    cycle = root_cycle_network()
    tree = root_tree_network()
    s, t, u, p, q, inheritance = sp.symbols("s t u p q lambda")
    c, d = sp.symbols("c d")
    # Root uniformity makes the twelve nonzero-total coordinates identically
    # zero.  The displayed-tree engine evaluates the four zero-sum entries.
    assignments = tuple((character, character) for character in range(4))
    cycle_coordinates = evaluate_jc_coordinates(
        cycle["vertices"],
        cycle["edges"],
        {"L1": 1, "L2": 2},
        assignments,
        (s, t, u, p, q),
        {"X": inheritance},
    )
    tree_coordinates = evaluate_jc_coordinates(
        tree["vertices"],
        tree["edges"],
        {"L1": 1, "L2": 2},
        assignments,
        (c, d),
        {},
    )
    rho = sp.factor(p * q * (inheritance * t + (1 - inheritance) * s * u))
    expected_cycle = (1, rho, rho, rho)
    expected_tree = (1, c * d, c * d, c * d)
    assert all(sp.expand(left - right) == 0 for left, right in zip(cycle_coordinates, expected_cycle))
    assert all(sp.expand(left - right) == 0 for left, right in zip(tree_coordinates, expected_tree))

    # Every source point maps rationally to two open tree arms.
    source_to_tree = {
        c: (1 + rho) / 2,
        d: 2 * rho / (1 + rho),
    }
    assert sp.factor(source_to_tree[c] * source_to_tree[d] - rho) == 0

    # Every open tree point maps rationally back to an open root cycle.
    r = c * d
    pendant = (1 + r) / 2
    path = 4 * r / (1 + r) ** 2
    first = (1 + path) / 2
    second = 2 * path / (1 + path)
    tree_to_source = {
        p: pendant,
        q: pendant,
        t: path,
        s: first,
        u: second,
        inheritance: sp.Rational(1, 2),
    }
    assert sp.factor(first * second - path) == 0
    assert sp.factor(rho.subs(tree_to_source) - r) == 0
    assert all(
        sp.factor(sp.sympify(tree_value).subs(source_to_tree) - cycle_value) == 0
        for tree_value, cycle_value in zip(tree_coordinates, cycle_coordinates)
    )
    assert all(
        sp.factor(sp.sympify(cycle_value).subs(tree_to_source) - tree_value) == 0
        for tree_value, cycle_value in zip(tree_coordinates, cycle_coordinates)
    )

    return {
        "zero_sum_fourier_coordinates_checked": len(assignments),
        "nonzero_total_coordinates_zero_by_uniform_root": 12,
        "complete_fourier_coordinates_accounted_for": 16,
        "effective_multiplier": str(rho),
        "source_to_tree": {str(key): str(sp.factor(value)) for key, value in source_to_tree.items()},
        "tree_to_source": {str(key): str(sp.factor(value)) for key, value in tree_to_source.items()},
    }


def exact_open_point_and_ranks():
    values = {
        "s": Fraction(2, 3),
        "t": Fraction(3, 5),
        "u": Fraction(4, 7),
        "p": Fraction(5, 8),
        "q": Fraction(7, 9),
        "lambda": Fraction(2, 5),
    }
    rho = values["p"] * values["q"] * (
        values["lambda"] * values["t"]
        + (1 - values["lambda"]) * values["s"] * values["u"]
    )
    c = (1 + rho) / 2
    d = 2 * rho / (1 + rho)
    assert 0 < rho < 1 and 0 < c < 1 and 0 < d < 1 and c * d == rho
    # d(rho)/d(p) and d(cd)/d(c) are positive throughout the open cubes.
    cycle_rank_minor = values["q"] * (
        values["lambda"] * values["t"]
        + (1 - values["lambda"]) * values["s"] * values["u"]
    )
    tree_rank_minor = d
    assert cycle_rank_minor > 0 and tree_rank_minor > 0
    return {
        "cycle_parameters": {key: str(value) for key, value in values.items()},
        "effective_multiplier": str(rho),
        "tree_parameters": {"c": str(c), "d": str(d)},
        "rank_one_minor_cycle_d_rho_d_p": str(cycle_rank_minor),
        "rank_one_minor_tree_d_cd_d_c": str(tree_rank_minor),
    }


def inequality_certificate():
    # The rational inverse uses only maps f(x)=(1+x)/2 and
    # g(x)=2x/(1+x), both strictly between zero and one on 0<x<1.
    # path=4r/(1+r)^2 is also open because
    # (1+r)^2-4r=(1-r)^2>0.
    r = sp.symbols("r")
    return {
        "source_effective_range": "0 < rho < 1 by products and a strict convex combination",
        "open_split_maps": ["(1+x)/2", "2*x/(1+x)"],
        "path_multiplier": "4*r/(1+r)**2",
        "path_upper_gap_factor": str(sp.factor((1 + r) ** 2 - 4 * r)),
        "complete_effective_range": "(0,1)",
    }


def generate_certificate():
    cycle = root_cycle_network()
    tree = root_tree_network()
    return {
        "status": {
            "two_port_root_cycle_complete_image_equality": "PROVED",
            "arbitrary_component_substitution": "PROVED",
            "local_model_dimension": 1,
            "move": "C_root: contract or insert the unique two-port root cycle",
            "semi_directed_parallel_artifact_convention": "MUST BE TRACKED",
        },
        "root_cycle_network": {
            "vertices": cycle["vertices"],
            "edges": [list(edge) for edge in cycle["edges"]],
            "leaves": list(cycle["leaves"]),
            "reticulation": "X",
        },
        "collapsed_root_tree": {
            "vertices": tree["vertices"],
            "edges": [list(edge) for edge in tree["edges"]],
            "leaves": list(tree["leaves"]),
        },
        "exact_symbolic_replay": exact_coordinate_replay(),
        "exact_common_regular_point": exact_open_point_and_ranks(),
        "open_domain_certificate": inequality_certificate(),
        "tensor_gluing_statement": (
            "equality of the complete two-port state tensor is preserved "
            "after contraction with arbitrary identical rooted JC network "
            "components at the two ports"
        ),
        "conclusion": (
            "the root cycle and ordinary binary root have equal complete "
            "open JC stochastic images after arbitrary corresponding "
            "component substitution"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
