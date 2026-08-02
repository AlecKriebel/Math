#!/usr/bin/env python3
"""Exact verifier for the arbitrary-chain JC root move Omega_chain.

The finite symbolic checks are accompanied by a length-independent five-case
Fourier identity and an effective-coordinate rank certificate.  The latter
are the machine-checkable algebra behind the all-k proof in the milestone
note; finite k=2,3,4 contractions are independent replays of the complete
displayed-tree formula.
"""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path

import sympy as sp

from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from enumerate_four_leaf_root_theta import valid_binary_strong


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "jc_omega_chain.json"


def zero_sum_assignments(count):
    assignments = []
    for prefix in product(range(4), repeat=count - 1):
        total = 0
        for character in prefix:
            total ^= character
        assignments.append(prefix + (total,))
    return tuple(assignments)


def omega_network(k):
    assert k >= 2
    vertices = {"S": "S", "U": "T", "V": "R", "X": "X", "Q": "T"}
    vertices.update({f"P{i}": "T" for i in range(1, k + 1)})
    vertices.update({f"L{i}": "L" for i in range(1, k + 3)})
    edges = [("U", "V")]
    path = ["U"] + [f"P{i}" for i in range(1, k + 1)] + ["V"]
    edges.extend(zip(path, path[1:]))
    edges.extend((("S", "U"), ("S", "X"), ("V", "Q"), ("Q", "X")))
    edges.extend((f"P{i}", f"L{i}") for i in range(1, k + 1))
    edges.extend((("Q", f"L{k + 1}"), ("X", f"L{k + 2}")))
    network = {
        "vertices": vertices,
        "edges": tuple(edges),
        "leaves": tuple(f"L{i}" for i in range(1, k + 3)),
    }
    assert valid_binary_strong(vertices, tuple(edges))
    return network


def model(k, labels, prefix):
    network = omega_network(k)
    edges = network["edges"]
    reticulations = reticulation_vertices(network["vertices"])
    edge_parameters = sp.symbols(f"{prefix}e0:{len(edges)}")
    inheritance_parameters = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], labels)),
        zero_sum_assignments(k + 2),
        edge_parameters,
        dict(zip(reticulations, inheritance_parameters)),
    )
    return edge_parameters, inheritance_parameters, coordinates


def index_data(k):
    return {
        "long_start": 1,
        "long_end": k + 1,
        "root_u": k + 2,
        "root_x": k + 3,
        "short_vq": k + 4,
        "short_qx": k + 5,
        "pendant_start": k + 6,
        "q_pendant": 2 * k + 6,
        "x_pendant": 2 * k + 7,
    }


def omega_substitutions(k, source, target):
    ae, al = source
    be, bl = target
    indices = index_data(k)
    A = ae[0]
    B = ae[indices["long_start"]]
    D = ae[indices["long_end"]]
    E = ae[indices["root_u"]]
    F = ae[indices["short_qx"]]
    R = ae[indices["q_pendant"]]
    G = E + 2 * F
    H = A * F + 2 * E
    source_substitution = {
        ae[indices["root_x"]]: sp.Rational(1, 2),
        ae[indices["short_vq"]]: sp.Rational(1, 2),
        ae[indices["x_pendant"]]: sp.Rational(1, 2),
        al[0]: sp.Rational(1, 2),
        al[1]: sp.Rational(1, 2),
    }
    target_substitution = {
        be[0]: 2 * F * (4 - A) / G,
        be[indices["long_start"]]: D / (4 - A),
        be[indices["long_end"]]: 2 * B * H / G,
        be[indices["root_u"]]: 4 * E * R * (4 - A) / H,
        be[indices["root_x"]]: sp.Rational(1, 2),
        be[indices["short_vq"]]: sp.Rational(1, 2),
        be[indices["short_qx"]]: 2 * A * R * G / H,
        be[indices["q_pendant"]]: G / 8,
        be[indices["x_pendant"]]: sp.Rational(1, 2),
        bl[0]: sp.Rational(1, 2),
        bl[1]: sp.Rational(1, 2),
    }
    for offset in range(1, k):
        target_substitution[be[indices["long_start"] + offset]] = ae[
            indices["long_end"] - offset
        ]
    for offset in range(k):
        target_substitution[be[indices["pendant_start"] + offset]] = ae[
            indices["pendant_start"] + k - 1 - offset
        ]
    return (G, H), source_substitution, target_substitution


def verify_complete_coordinate_maps():
    checks = {}
    for k in (2, 3, 4):
        source_labels = tuple(range(1, k + 3))
        target_labels = tuple(range(k, 0, -1)) + (k + 2, k + 1)
        ae, al, source_coordinates = model(k, source_labels, f"mapA{k}_")
        be, bl, target_coordinates = model(k, target_labels, f"mapB{k}_")
        _denominators, source_substitution, target_substitution = omega_substitutions(
            k, (ae, al), (be, bl)
        )
        differences = tuple(
            sp.factor(left.subs(source_substitution) - right.subs(target_substitution))
            for left, right in zip(source_coordinates, target_coordinates)
        )
        assert all(difference == 0 for difference in differences)
        checks[str(k)] = len(differences)
    return checks


def gauge_core(a, b, d, e, f, iq, ix, il, path_d, path_0, path_1):
    """Core coordinate with s=t=lambda=mu=1/2 and no pendant factors."""
    half = sp.Rational(1, 2)
    return sp.factor(
        half * (e * half) ** ix * half**iq
        * (half * path_d * a**iq + half * path_0)
        + half * f**ix * half**il
        * (half * path_d * a**il + half * path_1)
    )


def verify_universal_five_case_identity():
    A, B, D, E, F, R = sp.symbols("A B D E F R", nonzero=True)
    path_d, path_0, path_1 = sp.symbols("path_d path_0 path_1")
    G = E + 2 * F
    H = A * F + 2 * E
    target_values = {
        "a": 2 * F * (4 - A) / G,
        "b": D / (4 - A),
        "d": 2 * B * H / G,
        "e": 4 * E * R * (4 - A) / H,
        "f": 2 * A * R * G / H,
    }
    cases = (
        ("zero", 0, 0, 0, (path_d, path_d, path_d)),
        ("x_zero", 1, 0, 1, (path_d, path_0, path_0)),
        ("q_zero", 0, 1, 1, (path_d, path_d, path_1)),
        ("sum_zero", 1, 1, 0, (path_d, path_0, path_d)),
        ("all_nonzero", 1, 1, 1, (path_d, path_0, path_1)),
    )
    source_forms = {}
    for name, iq, ix, il, (xd, x0, x1) in cases:
        source_path_d = B**il * xd
        source_path_0 = B**ix * D**iq * x0
        source_path_1 = D**il * x1
        source = sp.factor(
            R**iq * sp.Rational(1, 2) ** ix
            * gauge_core(
                A, B, D, E, F, iq, ix, il,
                source_path_d, source_path_0, source_path_1,
            )
        )

        # Reversal sends (q,x) to (x,q), fixes the middle monomial path_0,
        # and exchanges path_d with path_1.
        target_iq, target_ix = ix, iq
        target_path_d = target_values["b"] ** il * x1
        target_path_0 = (
            target_values["b"] ** iq * target_values["d"] ** ix * x0
        )
        target_path_1 = target_values["d"] ** il * xd
        target = sp.factor(
            (G / 8) ** ix * sp.Rational(1, 2) ** iq
            * gauge_core(
                target_values["a"], target_values["b"], target_values["d"],
                target_values["e"], target_values["f"],
                target_iq, target_ix, il,
                target_path_d, target_path_0, target_path_1,
            )
        )
        assert sp.factor(source - target) == 0
        source_forms[name] = str(source)
    return source_forms


def arbitrary_core(a, b, d, e, s, t, f, inheritance_v, inheritance_x,
                   iq, ix, il, path_d, path_0, path_1):
    return sp.factor(
        inheritance_x * (e * s) ** ix * t**iq
        * (
            inheritance_v * path_d * a**iq
            + (1 - inheritance_v) * path_0
        )
        + (1 - inheritance_x) * f**ix * t**il
        * (
            inheritance_v * path_d * a**il
            + (1 - inheritance_v) * path_1
        )
    )


def verify_effective_core_factorization():
    a, b, d, e, s, t, f, lv, lx = sp.symbols("a b d e s t f lv lx")
    xd, x0, x1 = sp.symbols("Xd X0 X1")
    alpha = t * lv * b * a
    beta = t * (1 - lv) * d
    gamma = lx * e * s * b
    delta = (1 - lx) * f
    cases = (
        ("zero", 0, 0, 0, (xd, xd, xd), xd),
        ("x_zero", 1, 0, 1, (xd, x0, x0), alpha * xd + beta * x0),
        (
            "q_zero", 0, 1, 1, (xd, xd, x1),
            (gamma + delta * alpha) * xd + delta * beta * x1,
        ),
        (
            "sum_zero", 1, 1, 0, (xd, x0, xd),
            (delta + alpha * gamma / b**2) * xd + gamma * beta * x0,
        ),
        (
            "all_nonzero", 1, 1, 1, (xd, x0, x1),
            alpha * (delta + gamma / b) * xd
            + gamma * beta * x0 + delta * beta * x1,
        ),
    )
    for _name, iq, ix, il, (middle_d, middle_0, middle_1), expected in cases:
        path_d = b**il * middle_d
        path_0 = b**ix * d**iq * middle_0
        path_1 = d**il * middle_1
        actual = arbitrary_core(
            a, b, d, e, s, t, f, lv, lx, iq, ix, il,
            path_d, path_0, path_1,
        )
        assert sp.factor(actual - expected) == 0
    return {
        "effective_parameters": ["b", "alpha", "beta", "gamma", "delta"],
        "definitions": {
            "alpha": "t*lambdaV*b*a",
            "beta": "t*(1-lambdaV)*d",
            "gamma": "lambdaX*e*s*b",
            "delta": "(1-lambdaX)*f",
        },
        "middle_path_parameters": "k-1",
        "core_dimension_upper_bound": "(k-1)+5=k+4",
    }


def effective_base_expression(assignment, b, alpha, beta, gamma, delta, c):
    _g1, g2, q, x = assignment
    total_long = q ^ x
    indicator = lambda character: int(character != 0)
    xd = c ** indicator(g2)
    x0 = c ** indicator(g2 ^ q)
    x1 = c ** indicator(g2 ^ total_long)
    if q == 0 and x == 0:
        return xd
    if x == 0:
        return alpha * xd + beta * x0
    if q == 0:
        return (gamma + delta * alpha) * xd + delta * beta * x1
    if total_long == 0:
        return (delta + alpha * gamma / b**2) * xd + gamma * beta * x0
    return (
        alpha * (delta + gamma / b) * xd
        + gamma * beta * x0 + delta * beta * x1
    )


def verify_effective_rank_certificate():
    b, alpha, beta, gamma, delta, c = sp.symbols(
        "b alpha beta gamma delta c", nonzero=True
    )
    assignments = (
        (0, 0, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (0, 1, 2, 3),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
    )
    parameters = (b, alpha, beta, gamma, delta, c)
    outputs = tuple(
        sp.factor(effective_base_expression(item, *parameters))
        for item in assignments
    )
    determinant = sp.factor(sp.Matrix(outputs).jacobian(parameters).det())
    inner = (
        -alpha**2 * c + 2 * alpha * b * c - 2 * alpha * beta
        + b**2 * beta**2 * c**3 + b**2 * beta**2 * c - b**2 * c
        - 2 * b * beta**2 * c**2 - 2 * b * beta**2
        + 2 * b * beta + beta**2 * c
    )
    expected = sp.factor(
        alpha * gamma**2 * (c - 1) * (c + 1) * inner / b**4
    )
    assert sp.factor(determinant - expected) == 0

    # At the all-k rational witness, an adjacent quartet at position i has
    # L=2^{-(i-1)} and R=2^{-(k-1-i)}.  Clearing powers of two from the only
    # nontrivial factor gives this odd integer, hence it can never vanish.
    L, R = sp.symbols("L R", positive=True)
    witness_inner = sp.factor(
        inner.subs(
            {
                b: L / 4,
                alpha: L / 32,
                beta: R / 8,
                gamma: L / 32,
                delta: sp.Rational(1, 40),
                c: sp.Rational(1, 2),
            }
        )
    )
    cleared = sp.factor(8192 * witness_inner)
    expected_cleared = (
        5 * L**2 * R**2 - 196 * L**2 - 80 * L * R**2
        + 448 * L * R + 64 * R**2
    )
    assert sp.factor(cleared - expected_cleared) == 0
    return {
        "assignments": [list(item) for item in assignments],
        "jacobian_determinant": str(determinant),
        "dyadic_cleared_factor": (
            "5-196*2^(2r)-80*2^l+448*2^(l+r)+64*2^(2l)"
        ),
        "dyadic_nonzero_reason": "odd: constant 5 plus even terms",
    }


def exact_common_values(k):
    indices = index_data(k)
    source = [sp.Rational(1, 2)] * (2 * k + 8)
    source[indices["long_start"]] = sp.Rational(1, 4)
    source[indices["short_qx"]] = sp.Rational(1, 20)
    source[indices["q_pendant"]] = sp.Rational(1, 10)
    target = [sp.Rational(1, 2)] * (2 * k + 8)
    target[0] = sp.Rational(7, 12)
    target[indices["long_start"]] = sp.Rational(1, 7)
    target[indices["long_end"]] = sp.Rational(41, 48)
    target[indices["root_u"]] = sp.Rational(28, 41)
    target[indices["short_qx"]] = sp.Rational(12, 205)
    target[indices["q_pendant"]] = sp.Rational(3, 40)
    return source, target


def exact_derivative_columns(k, edge_values, inheritance_values, variable_edges):
    network = omega_network(k)
    assignments = zero_sum_assignments(k + 2)[1:]
    labels = dict(zip(network["leaves"], range(1, k + 3)))
    base = evaluate_jc_coordinates(
        network["vertices"], network["edges"], labels, assignments,
        edge_values, inheritance_values,
    )
    columns = []
    for edge_index in variable_edges:
        changed = list(edge_values)
        changed[edge_index] += 1
        output = evaluate_jc_coordinates(
            network["vertices"], network["edges"], labels, assignments,
            changed, inheritance_values,
        )
        columns.append(tuple(left - right for left, right in zip(output, base)))
    return assignments, columns


def verify_five_leaf_common_rank():
    k = 3
    indices = index_data(k)
    source_edges, target_edges = exact_common_values(k)
    half = sp.Rational(1, 2)
    reticulations = reticulation_vertices(omega_network(k)["vertices"])
    inheritance = {vertex: half for vertex in reticulations}
    variable_edges = tuple(
        index for index in range(len(source_edges))
        if index not in {
            indices["root_x"], indices["short_vq"], indices["x_pendant"]
        }
    )
    row_indices = (0, 3, 4, 5, 15, 16, 17, 19, 21, 63, 64)
    assignments, source_columns = exact_derivative_columns(
        k, source_edges, inheritance, variable_edges
    )
    source_minor = sp.factor(
        sp.Matrix(
            [
                [source_columns[column][row] for column in range(len(variable_edges))]
                for row in row_indices
            ]
        ).det()
    )
    expected = -sp.Rational(81, 755578637259143234191360000000)
    assert source_minor == expected

    # Equality at the exact point is independently contracted on all 256
    # coordinates, using the reversed target labels.
    source_labels = tuple(range(1, k + 3))
    target_labels = tuple(range(k, 0, -1)) + (k + 2, k + 1)
    network = omega_network(k)
    source_coordinates = evaluate_jc_coordinates(
        network["vertices"], network["edges"],
        dict(zip(network["leaves"], source_labels)),
        zero_sum_assignments(k + 2), source_edges, inheritance,
    )
    target_coordinates = evaluate_jc_coordinates(
        network["vertices"], network["edges"],
        dict(zip(network["leaves"], target_labels)),
        zero_sum_assignments(k + 2), target_edges, inheritance,
    )
    assert source_coordinates == target_coordinates
    assert all(0 < value < 1 for value in source_edges + target_edges)
    return {
        "k": k,
        "leaves": k + 2,
        "zero_sum_coordinates": len(source_coordinates),
        "gauge_columns": list(variable_edges),
        "minor_rows_after_constant": list(row_indices),
        "minor_assignments": [list(assignments[row]) for row in row_indices],
        "source_rank_minor": str(source_minor),
        "source_edges": [str(value) for value in source_edges],
        "target_edges": [str(value) for value in target_edges],
        "inheritances": ["1/2", "1/2"],
    }


def main():
    for k in range(2, 9):
        network = omega_network(k)
        assert len(network["leaves"]) == k + 2
        assert len(network["edges"]) == 2 * k + 8

    certificate = {
        "status": {
            "all_k_fourier_identity": "PROVED",
            "all_k_model_dimension": "PROVED",
            "full_dimensional_regular_stochastic_overlap": "PROVED",
            "finite_complete_contractions": "EXACTLY COMPUTED",
        },
        "scope": "JC Omega_chain for every integer k>=2",
        "network_schema": {
            "root_edges": ["S->U", "S->X"],
            "reticulations": ["V", "X"],
            "three_UV_paths_after_root_suppression": [
                "U-V", "U-P1-...-Pk-V", "U-X-Q-V"
            ],
            "source_port_order": "P1,...,Pk,Q,X",
            "target_port_order": "Pk,...,P1,X,Q",
            "leaf_count": "k+2",
            "edge_count": "2k+8",
            "cycle_lengths": [4, "k+2", "k+4"],
        },
        "complete_coordinate_replays": verify_complete_coordinate_maps(),
        "universal_five_case_source_forms": verify_universal_five_case_identity(),
        "effective_core_factorization": verify_effective_core_factorization(),
        "effective_rank_certificate": verify_effective_rank_certificate(),
        "exact_five_leaf_certificate": verify_five_leaf_common_rank(),
        "dimension": {
            "core": "k+4",
            "pendant_directions_added": "k+1",
            "complete": "2k+5=2n+1",
        },
        "parameter_map": {
            "fixed_source_and_target": [
                "root edge S->X=1/2",
                "edge V->Q=1/2",
                "pendant X->L_(k+2)=1/2",
                "lambda_V=lambda_X=1/2",
            ],
            "denominators": ["G=E+2F", "H=AF+2E", "4-A"],
            "reversed": ["all middle long-path edges", "all long-path pendants"],
        },
        "conclusion": (
            "For every k>=2 the two nonisomorphic, non-triangle-equivalent "
            "root semi-directed topologies have equal irreducible JC model "
            "closures and a common regular stochastic neighborhood of full "
            "dimension 2k+5."
        ),
    }
    CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
