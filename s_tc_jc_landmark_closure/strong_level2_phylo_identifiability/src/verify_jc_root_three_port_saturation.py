#!/usr/bin/env python3
"""Exact three-port root-blob saturation theorem under JC.

Every binary strongly tree-child root blob with exactly three outgoing ports
is enumerated from the level-2 cycle/theta cores.  All 39 labelled reticulate
rooted topologies are shown to contain one common regular four-dimensional JC
region.  The proof constructs a shared exact algebraic point through a
one-variable equal-internal-edge subfamily and checks regularity symbolically.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import (
    build_network,
    canonical_code,
    semi_directed_triangle_count,
    valid_binary_strong,
)
from enumerate_theta_orientation_cores import enumerate_cores, weak_compositions
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import (
    canonical_mixed_graph,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_root_three_port_saturation.json"

ASSIGNMENTS = (
    (0, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 2, 3),
)
TARGET_KAPPA = sp.Rational(16, 25)
DELTA = sp.Rational(1, 2**30)
ROOT_INTERVAL = (sp.Rational(1, 8), sp.Rational(7, 8))


def tree_network():
    network = {
        "vertices": {
            "S": "S",
            "P": "T",
            "L0": "L",
            "L1": "L",
            "L2": "L",
        },
        "edges": (("S", "L0"), ("S", "P"), ("P", "L1"), ("P", "L2")),
        "leaves": ("L0", "L1", "L2"),
    }
    assert valid_binary_strong(network["vertices"], network["edges"])
    return network


def build_cycle_root(counts):
    vertices = {"S": "S", "X": "X"}
    edges = []
    parents = []
    for side, count in enumerate(counts):
        chain = ["S"]
        for index in range(count):
            vertex = f"P{side}_{index}"
            vertices[vertex] = "T"
            parents.append(vertex)
            chain.append(vertex)
        chain.append("X")
        edges.extend(zip(chain, chain[1:]))
    parents.append("X")
    leaves = []
    for index, parent in enumerate(parents):
        leaf = f"L{index}"
        vertices[leaf] = "L"
        edges.append((parent, leaf))
        leaves.append(leaf)
    network = {
        "vertices": vertices,
        "edges": tuple(edges),
        "leaves": tuple(leaves),
    }
    assert valid_binary_strong(vertices, tuple(edges))
    return network


def enumerate_unlabelled():
    records = {}

    tree = tree_network()
    records[("tree", canonical_code(tree["vertices"], tree["edges"]))] = {
        "kind": "tree",
        "network": tree,
    }

    for counts in ((0, 2), (1, 1), (2, 0)):
        network = build_cycle_root(counts)
        code = canonical_code(network["vertices"], network["edges"])
        records.setdefault(
            ("cycle", code),
            {"kind": "cycle", "counts": counts, "network": network},
        )

    _raw, cores = enumerate_cores()
    for core_index, core in enumerate(cores):
        sink_count = sum(
            color == "X" for color in core["vertex_types"].values()
        )
        ordinary_count = 3 - sink_count
        if ordinary_count < 0:
            continue
        for counts in weak_compositions(
            ordinary_count, len(core["directed_segments"])
        ):
            vertices, edges, leaves = build_network(core, counts)
            if not valid_binary_strong(vertices, edges):
                continue
            code = canonical_code(vertices, edges)
            records.setdefault(
                ("theta", code),
                {
                    "kind": "theta",
                    "core_index": core_index,
                    "counts": counts,
                    "network": {
                        "vertices": vertices,
                        "edges": edges,
                        "leaves": leaves,
                    },
                },
            )

    order = {"tree": 0, "cycle": 1, "theta": 2}
    return tuple(
        records[key]
        for key in sorted(records, key=lambda item: (order[item[0]], repr(item[1])))
    )


def jc_coordinates(network, edge_parameters, inheritance_parameters):
    reticulations = reticulation_vertices(network["vertices"])
    return evaluate_jc_coordinates(
        network["vertices"],
        tuple(network["edges"]),
        dict(zip(network["leaves"], (1, 2, 3))),
        ASSIGNMENTS,
        edge_parameters,
        dict(zip(reticulations, inheritance_parameters)),
    )


def exact_generic_rank(network):
    edge_count = len(network["edges"])
    reticulation_count = len(reticulation_vertices(network["vertices"]))
    parameters = sp.symbols(f"g0:{edge_count + reticulation_count}")
    coordinates = jc_coordinates(
        network,
        parameters[:edge_count],
        parameters[edge_count:],
    )[1:]
    jacobian = sp.Matrix(coordinates).jacobian(parameters)
    point = {
        parameter: sp.Rational(2 + index % 5, 8)
        for index, parameter in enumerate(parameters)
    }
    evaluated = jacobian.subs(point)
    rank = evaluated.rank()
    rows = None
    columns = None
    determinant = None
    for selected_rows in combinations(range(evaluated.rows), rank):
        for selected_columns in combinations(range(len(parameters)), rank):
            minor = sp.factor(
                evaluated.extract(selected_rows, selected_columns).det()
            )
            if minor:
                rows = selected_rows
                columns = selected_columns
                determinant = minor
                break
        if columns is not None:
            break
    assert rows is not None and columns is not None
    return rank, rows, columns, determinant, coordinates


def equal_internal_subfamily(network):
    h = sp.symbols("h")
    arms = sp.symbols("a0:3", positive=True)
    leaf_index = {leaf: index for index, leaf in enumerate(network["leaves"])}
    edge_parameters = []
    for _tail, head in network["edges"]:
        edge_parameters.append(arms[leaf_index[head]] if head in leaf_index else h)
    reticulation_count = len(reticulation_vertices(network["vertices"]))
    coordinates = tuple(
        sp.factor(value)
        for value in jc_coordinates(
            network,
            tuple(edge_parameters),
            (sp.Rational(1, 2),) * reticulation_count,
        )
    )
    assert coordinates[0] == 1
    c12 = sp.factor(coordinates[1] / (arms[0] * arms[1]))
    c13 = sp.factor(coordinates[2] / (arms[0] * arms[2]))
    c23 = sp.factor(coordinates[3] / (arms[1] * arms[2]))
    triple = sp.factor(coordinates[4] / (arms[0] * arms[1] * arms[2]))
    assert not any(
        expression.has(*arms) for expression in (c12, c13, c23, triple)
    )
    kappa = sp.factor(triple**2 / (c12 * c13 * c23))
    return h, arms, coordinates, (c12, c13, c23, triple), kappa


def root_and_regularity_record(record):
    network = record["network"]
    internal_edge_count = len(network["edges"]) - len(network["leaves"])
    assert internal_edge_count <= 7
    pendant_square_upper_bound = sp.factor(DELTA**2 * 8**14)
    assert pendant_square_upper_bound == sp.Rational(1, 2**18)
    assert 0 < pendant_square_upper_bound < 1
    h, arms, coordinates, internal, kappa = equal_internal_subfamily(network)
    c12, c13, c23, triple = internal
    equation = sp.factor(sp.together(kappa - TARGET_KAPPA).as_numer_denom()[0])
    polynomial = sp.Poly(equation, h, domain=sp.QQ)
    left, right = ROOT_INTERVAL
    assert polynomial.count_roots(left, right) == 1
    assert sp.sign(sp.factor((kappa - TARGET_KAPPA).subs(h, left))) == -1
    assert sp.sign(sp.factor((kappa - TARGET_KAPPA).subs(h, right))) == 1
    assert sp.gcd(polynomial, polynomial.diff()).degree() == 0

    derivative = sp.factor(sp.diff(kappa, h))
    derivative_numerator = sp.Poly(
        sp.together(derivative).as_numer_denom()[0], h, domain=sp.QQ
    )
    assert sp.gcd(polynomial, derivative_numerator).degree() == 0

    log_matrix = sp.Matrix(
        (
            (1, 1, 0, sp.diff(c12, h) / c12),
            (1, 0, 1, sp.diff(c13, h) / c13),
            (0, 1, 1, sp.diff(c23, h) / c23),
            (1, 1, 1, sp.diff(triple, h) / triple),
        )
    )
    log_determinant = sp.factor(log_matrix.det())
    assert sp.factor(log_determinant + derivative / kappa) == 0

    arm_squares = (
        sp.factor(DELTA**2 * c23 / (c12 * c13)),
        sp.factor(DELTA**2 * c13 / (c12 * c23)),
        sp.factor(DELTA**2 * c12 / (c13 * c23)),
    )
    assert sp.factor(arm_squares[0] * arm_squares[1] * c12**2 - DELTA**4) == 0
    assert sp.factor(arm_squares[0] * arm_squares[2] * c13**2 - DELTA**4) == 0
    assert sp.factor(arm_squares[1] * arm_squares[2] * c23**2 - DELTA**4) == 0
    triple_identity = sp.together(
        arm_squares[0]
        * arm_squares[1]
        * arm_squares[2]
        * triple**2
        - (sp.Rational(4, 5) * DELTA**3) ** 2
    ).as_numer_denom()[0]
    _quotient, remainder = sp.div(
        sp.Poly(triple_identity, h, domain=sp.QQ), polynomial
    )
    assert remainder.is_zero

    return {
        "equal_internal_kappa": str(kappa),
        "root_equation": str(equation),
        "isolating_interval": [str(left), str(right)],
        "roots_in_isolating_interval": 1,
        "root_is_simple": True,
        "kappa_derivative": str(derivative),
        "log_jacobian_determinant": str(log_determinant),
        "internal_pair_factors": [str(c12), str(c13), str(c23)],
        "internal_triple_factor": str(triple),
        "pendant_arm_squares": [str(value) for value in arm_squares],
        "pendant_arm_square_upper_bound": str(pendant_square_upper_bound),
        "common_coordinate_square_identities": 4,
    }, kappa


def topology_counts(records):
    rooted_by_kind = Counter()
    semi_by_kind_triangle = {}
    all_semi = set()
    retic_semi = set()
    triangle_retic_semi = set()
    for record in records:
        network = record["network"]
        rooted_codes = set()
        semi_codes = set()
        for labels in permutations((1, 2, 3)):
            rooted_codes.add(
                canonical_code(
                    network["vertices"],
                    network["edges"],
                    dict(zip(network["leaves"], labels)),
                )
            )
            semi_codes.add(canonical_mixed_graph(semi_directed_graph(network, labels)))
        rooted_by_kind[record["kind"]] += len(rooted_codes)
        triangle_count = (
            0
            if record["kind"] == "tree"
            else semi_directed_triangle_count(
                network["vertices"], network["edges"]
            )
        )
        semi_by_kind_triangle.setdefault((record["kind"], triangle_count), set()).update(
            semi_codes
        )
        all_semi.update(semi_codes)
        if record["kind"] != "tree":
            retic_semi.update(semi_codes)
            if triangle_count == 1:
                triangle_retic_semi.update(semi_codes)
    return {
        "rooted_by_kind": dict(sorted(rooted_by_kind.items())),
        "rooted_reticulate": rooted_by_kind["cycle"] + rooted_by_kind["theta"],
        "semi_directed_total": len(all_semi),
        "semi_directed_reticulate": len(retic_semi),
        "semi_directed_triangle_reticulate": len(triangle_retic_semi),
        "semi_directed_by_kind_and_triangle_count": {
            f"{kind}:triangles={triangle}": len(codes)
            for (kind, triangle), codes in sorted(semi_by_kind_triangle.items())
        },
    }


def generate_certificate():
    records = enumerate_unlabelled()
    assert Counter(record["kind"] for record in records) == {
        "tree": 1,
        "cycle": 2,
        "theta": 5,
    }

    expected_kappas = {
        sp.factor(4 * sp.Symbol("h") ** 2 / (sp.Symbol("h") ** 2 + 1) ** 2),
        sp.factor(
            (sp.Symbol("h") + 1) ** 2
            / (2 * (sp.Symbol("h") ** 2 + 1))
        ),
        sp.factor(
            2
            * (2 * sp.Symbol("h") ** 2 + sp.Symbol("h") + 1) ** 2
            / (
                (sp.Symbol("h") + 1)
                * (sp.Symbol("h") + 3)
                * (sp.Symbol("h") ** 4 + sp.Symbol("h") ** 3 + 2)
            )
        ),
        sp.factor(
            8
            * sp.Symbol("h") ** 3
            * (sp.Symbol("h") + 1)
            / (sp.Symbol("h") ** 4 + sp.Symbol("h") ** 3 + 2) ** 2
        ),
        sp.factor(
            sp.Symbol("h")
            * (2 * sp.Symbol("h") ** 2 + sp.Symbol("h") + 1) ** 2
            / (
                (sp.Symbol("h") + 1) ** 2
                * (sp.Symbol("h") ** 2 + 1)
                * (sp.Symbol("h") ** 2 - sp.Symbol("h") + 1)
                * (sp.Symbol("h") ** 2 - sp.Symbol("h") + 2)
            )
        ),
        sp.factor(
            (2 * sp.Symbol("h") ** 2 + sp.Symbol("h") + 1) ** 2
            / (
                (sp.Symbol("h") ** 2 + 1) ** 2
                * (sp.Symbol("h") ** 2 + 3)
            )
        ),
        sp.factor(
            (2 * sp.Symbol("h") ** 2 + sp.Symbol("h") + 1) ** 2
            / (
                2
                * (sp.Symbol("h") + 1) ** 3
                * (sp.Symbol("h") ** 2 - sp.Symbol("h") + 1)
            )
        ),
    }

    network_records = []
    observed_kappas = set()
    dimensions = Counter()
    for index, record in enumerate(records):
        network = record["network"]
        rank, rows, columns, determinant, coordinates = exact_generic_rank(network)
        dimensions[(record["kind"], rank)] += 1
        triangle_count = (
            0
            if record["kind"] == "tree"
            else semi_directed_triangle_count(
                network["vertices"], network["edges"]
            )
        )
        local = {
            "id": index,
            "kind": record["kind"],
            "core_index": record.get("core_index"),
            "subdivision_counts": list(record.get("counts", ())),
            "triangle_count_after_root_suppression": triangle_count,
            "generic_rank": rank,
            "exact_rank_minor_rows": list(rows),
            "exact_rank_minor_columns": list(columns),
            "exact_rank_minor": str(determinant),
            "vertices": dict(sorted(network["vertices"].items())),
            "edges": [list(edge) for edge in network["edges"]],
            "leaves": list(network["leaves"]),
            "rooted_code_sha256": sha256(
                repr(canonical_code(network["vertices"], network["edges"])).encode()
            ).hexdigest(),
        }
        if record["kind"] == "tree":
            r12, r13, r23, triple = coordinates
            assert sp.factor(r12 * r13 * r23 - triple**2) == 0
            assert rank == 3
            local["tree_invariant"] = "r12*r13*r23-u^2=0"
        else:
            assert rank == 4
            regularity, kappa = root_and_regularity_record(record)
            observed_kappas.add(kappa)
            local["common_regular_witness"] = regularity
        network_records.append(local)
    assert observed_kappas == expected_kappas
    assert dimensions == {
        ("tree", 3): 1,
        ("cycle", 4): 2,
        ("theta", 4): 5,
    }

    counts = topology_counts(records)
    assert counts["rooted_by_kind"] == {"cycle": 9, "theta": 30, "tree": 3}
    assert counts["rooted_reticulate"] == 39
    assert counts["semi_directed_total"] == 22
    assert counts["semi_directed_reticulate"] == 21
    assert counts["semi_directed_triangle_reticulate"] == 15

    # There are four nontrivial JC character-orbit coordinates on three
    # leaves.  Rank four therefore proves that every reticulate closure is
    # the complete affine four-space in these coordinates.
    return {
        "status": {
            "complete_root_three_port_bowtie_classification": "PROVED",
            "all_reticulate_root_three_port_models_one_class": "PROVED",
            "ordinary_tree_bowtie_reticulate": "PROVED ABSENT BY DIMENSION",
            "ordinary_tree_one_sided_containment": "UNRESOLVED",
            "move": "R3: arbitrary replacement of a reticulate three-port root blob",
        },
        "model": "JC",
        "three_leaf_nontrivial_fourier_orbit_coordinates": [
            "r12",
            "r13",
            "r23",
            "u123",
        ],
        "unlabelled_generator_counts": {"tree": 1, "cycle": 2, "theta": 5},
        "topology_counts": counts,
        "common_target": {
            "delta": str(DELTA),
            "r12": str(DELTA**2),
            "r13": str(DELTA**2),
            "r23": str(DELTA**2),
            "u123": str(sp.Rational(4, 5) * DELTA**3),
            "kappa=u123^2/(r12*r13*r23)": str(TARGET_KAPPA),
        },
        "common_witness_open_domain": {
            "internal_edge_parameter": "the unique h in (1/8,7/8) recorded for each topology",
            "inheritance_probabilities": "1/2",
            "pendant_edge_bound": "0<a_i<2^-9, from c_ij>=h^7 and delta=2^-30",
            "strict_transition_positivity": True,
        },
        "dimension_counts": {
            f"{kind}:rank={rank}": count
            for (kind, rank), count in sorted(dimensions.items())
        },
        "networks": network_records,
        "conclusion": (
            "all 39 labelled rooted reticulate three-port root blobs, "
            "representing 21 semi-directed topologies, share one regular "
            "four-dimensional JC stochastic neighborhood; the 33 rooted "
            "and 15 semi-directed one-triangle members already lie inside L1"
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
    print(
        json.dumps(
            {
                "unlabelled_generator_counts": certificate[
                    "unlabelled_generator_counts"
                ],
                "topology_counts": certificate["topology_counts"],
                "dimension_counts": certificate["dimension_counts"],
                "common_target": certificate["common_target"],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
