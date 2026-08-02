#!/usr/bin/env python3
"""Exact K2P saturation of every reticulate three-port root blob.

The seven unlabelled reticulate root blobs from the exhaustive R3 census are
evaluated at the common JC algebraic point.  A prescribed 9 by 9 K2P
Jacobian minor factors into terms that are nonzero throughout the isolating
interval of that point.  Since nine is the full normalized K2P three-leaf
ambient dimension, every map is a submersion onto a neighborhood of the same
strictly positive distribution.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import sympy as sp

from generic_fourier_network import precompute_displayed_trees
from verify_jc_omega_chain import zero_sum_assignments
from verify_jc_root_three_port_saturation import (
    DELTA,
    ROOT_INTERVAL,
    TARGET_KAPPA,
    enumerate_unlabelled,
    equal_internal_subfamily,
    topology_counts,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "k2p_root_three_port_saturation.json"

# One representative from each nonconstant K2P character orbit.  K2P fixes
# character 1 and exchanges characters 2 and 3.
ORBIT_REPRESENTATIVES = (
    (0, 1, 1),
    (0, 2, 2),
    (1, 0, 1),
    (1, 1, 0),
    (1, 2, 3),
    (2, 0, 2),
    (2, 1, 3),
    (2, 2, 0),
    (2, 3, 1),
)

# Parameter columns yielding the compact exact minors below.  Each edge has
# columns (singleton multiplier, doubleton multiplier), followed by the
# inheritance columns.
MINOR_COLUMNS = {
    1: (0, 1, 2, 3, 6, 7, 8, 9, 10),
    2: (0, 1, 4, 5, 6, 7, 8, 9, 10),
    3: (0, 1, 2, 3, 4, 5, 6, 7, 12),
    4: (0, 1, 8, 9, 12, 13, 14, 15, 16),
    5: (0, 1, 2, 3, 4, 5, 8, 9, 12),
    6: (0, 1, 2, 3, 6, 7, 8, 9, 10),
    7: (0, 1, 2, 3, 6, 7, 8, 9, 10),
}


def k2p_parameterization(network, prefix):
    edges = tuple(network["edges"])
    reticulations, displayed_trees = precompute_displayed_trees(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], (1, 2, 3))),
    )
    parameters = []
    multipliers = []
    for edge_index in range(len(edges)):
        singleton, doubleton = sp.symbols(
            f"{prefix}s{edge_index} {prefix}t{edge_index}"
        )
        parameters.extend((singleton, doubleton))
        multipliers.append((1, singleton, doubleton, doubleton))
    inheritances = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    parameters.extend(inheritances)
    inheritance = dict(zip(reticulations, inheritances))

    outputs = {}
    for assignment in zero_sum_assignments(3):
        by_leaf = {
            leaf_index + 1: character
            for leaf_index, character in enumerate(assignment)
        }
        total = 0
        for choices, selected, descendants in displayed_trees:
            term = 1
            for reticulation, choice in zip(reticulations, choices):
                value = inheritance[reticulation]
                term *= value if choice == 0 else 1 - value
            for edge_index in selected:
                character = 0
                for leaf in descendants[edge_index]:
                    character ^= by_leaf[leaf]
                term *= multipliers[edge_index][character]
            total += term
        outputs[assignment] = sp.expand(total)
    return outputs, tuple(parameters)


def equal_jc_substitution(network, parameters):
    h = sp.Symbol("h")
    arms = sp.symbols("a0:3", positive=True)
    leaf_index = {leaf: index for index, leaf in enumerate(network["leaves"])}
    substitution = {}
    for edge_index, (_tail, head) in enumerate(network["edges"]):
        value = arms[leaf_index[head]] if head in leaf_index else h
        substitution[parameters[2 * edge_index]] = value
        substitution[parameters[2 * edge_index + 1]] = value
    first_inheritance = 2 * len(network["edges"])
    for parameter in parameters[first_inheritance:]:
        substitution[parameter] = sp.Rational(1, 2)
    return h, arms, substitution


def expected_minor(index, h, arms):
    a0, a1, a2 = arms
    if index == 1:
        return a0**5 * a1**6 * a2**7 * h**11 * (h - 1) ** 4 * (h + 1) ** 4 / 32
    if index == 2:
        return a0**5 * a1**6 * a2**7 * h**10 * (h - 1) ** 4 / 32
    if index == 3:
        return (
            a0**7 * a1**7 * a2**7 * h**21 * (h - 1) ** 4
            * (3 * h**4 + 7 * h**3 + 6 * h**2 + 4 * h + 4)
            / 16384
        )
    if index == 4:
        return (
            a0**5 * a1**6 * a2**7 * h**16 * (h - 1) ** 4 * (h + 1) ** 3
            * (h**3 + 2 * h**2 + 2 * h + 2) ** 4
            / 16384
        )
    if index == 5:
        return (
            a0**7 * a1**7 * a2**7 * h**19 * (h - 1) ** 4
            * (h**6 + 4 * h**5 + 5 * h**4 + 6 * h**3 + 6 * h**2 + 4 * h + 4)
            / 16384
        )
    if index == 6:
        return a0**7 * a1**7 * a2**7 * h**21 * (h - 1) ** 4 / 4096
    if index == 7:
        return (
            a0**7 * a1**7 * a2**7 * h**18 * (h - 1) ** 4
            * (h + 1) * (h + 2) * (h**3 + h**2 + 1)
            / 8192
        )
    raise ValueError(index)


def root_data(network, h):
    jc_h, _jc_arms, _coordinates, internal, kappa = equal_internal_subfamily(network)
    internal = tuple(sp.factor(value.subs(jc_h, h)) for value in internal)
    kappa = sp.factor(kappa.subs(jc_h, h))
    equation = sp.factor(sp.together(kappa - TARGET_KAPPA).as_numer_denom()[0])
    polynomial = sp.Poly(equation, h, domain=sp.QQ)
    left, right = ROOT_INTERVAL
    assert polynomial.count_roots(left, right) == 1
    assert sp.gcd(polynomial, polynomial.diff()).degree() == 0
    return internal, kappa, polynomial


def verify_common_coordinate_identities(internal, polynomial, h):
    c12, c13, c23, triple = internal
    arm_squares = (
        sp.factor(DELTA**2 * c23 / (c12 * c13)),
        sp.factor(DELTA**2 * c13 / (c12 * c23)),
        sp.factor(DELTA**2 * c12 / (c13 * c23)),
    )
    assert sp.factor(arm_squares[0] * arm_squares[1] * c12**2 - DELTA**4) == 0
    assert sp.factor(arm_squares[0] * arm_squares[2] * c13**2 - DELTA**4) == 0
    assert sp.factor(arm_squares[1] * arm_squares[2] * c23**2 - DELTA**4) == 0
    triple_square_difference = sp.together(
        sp.prod(arm_squares) * triple**2
        - (sp.Rational(4, 5) * DELTA**3) ** 2
    ).as_numer_denom()[0]
    _quotient, remainder = sp.div(
        sp.Poly(sp.expand(triple_square_difference), h, domain=sp.QQ),
        polynomial,
    )
    assert remainder.is_zero
    return arm_squares


def verify_record(index, record):
    network = record["network"]
    outputs, parameters = k2p_parameterization(network, f"n{index}_")
    h, arms, substitution = equal_jc_substitution(network, parameters)
    orbit_outputs = sp.Matrix([outputs[item] for item in ORBIT_REPRESENTATIVES])
    jacobian = orbit_outputs.jacobian(parameters).subs(substitution)
    columns = MINOR_COLUMNS[index]
    determinant = sp.factor(jacobian[:, columns].det())
    expected = sp.factor(expected_minor(index, h, arms))
    assert sp.factor(determinant - expected) == 0

    internal, kappa, polynomial = root_data(network, h)
    arm_squares = verify_common_coordinate_identities(internal, polynomial, h)

    # Exact Sturm exclusion proves that the univariate part of the minor has
    # no zero anywhere in the full root-isolating interval.  The omitted arm
    # factor is nonzero because the positive square roots are used.
    univariate = sp.factor(expected.subs({arm: 1 for arm in arms}))
    numerator = sp.Poly(
        sp.expand(sp.together(univariate).as_numer_denom()[0]), h, domain=sp.QQ
    )
    left, right = ROOT_INTERVAL
    assert numerator.count_roots(left, right) == 0
    assert sp.gcd(polynomial, numerator).degree() == 0

    first_inheritance = 2 * len(network["edges"])
    selected_names = [str(parameters[column]) for column in columns]
    assert all(column < first_inheritance for column in columns)
    return {
        "id": index,
        "kind": record["kind"],
        "core_index": record.get("core_index"),
        "subdivision_counts": list(record.get("counts", ())),
        "root_equation": str(polynomial.as_expr()),
        "root_isolating_interval": [str(left), str(right)],
        "root_count_in_interval": 1,
        "kappa": str(kappa),
        "minor_columns": list(columns),
        "minor_parameters": selected_names,
        "jacobian_minor": str(determinant),
        "minor_roots_in_isolating_interval": 0,
        "common_pendant_arm_squares": [str(value) for value in arm_squares],
        "generic_K2P_rank": 9,
    }


def generate_certificate():
    records = enumerate_unlabelled()
    assert Counter(record["kind"] for record in records) == {
        "tree": 1,
        "cycle": 2,
        "theta": 5,
    }
    reticulate_records = [
        verify_record(index, record)
        for index, record in enumerate(records)
        if record["kind"] != "tree"
    ]
    assert [record["id"] for record in reticulate_records] == list(range(1, 8))

    counts = topology_counts(records)
    assert counts["rooted_reticulate"] == 39
    assert counts["semi_directed_reticulate"] == 21
    assert counts["semi_directed_triangle_reticulate"] == 15

    common_pair = DELTA**2
    common_triple = sp.Rational(4, 5) * DELTA**3
    certificate = {
        "status": {
            "all_reticulate_root_three_port_models_one_K2P_bowtie_class": "PROVED",
            "common_full_dimensional_regular_stochastic_region": "PROVED",
            "common_K2P_Zariski_closure_is_affine_9_space": "PROVED",
            "complete_open_stochastic_image_equality": "UNRESOLVED",
            "ordinary_tree_relations": "UNRESOLVED IN THIS MILESTONE",
            "move": "R3_K2P: arbitrary replacement of a reticulate three-port root blob",
        },
        "model": "K2P",
        "convention": {
            "nonzero_Fourier_multipliers": "(s,t,t) on characters (1,2,3)",
            "transition_probabilities": [
                "(1+s+2*t)/4",
                "(1+s-2*t)/4",
                "(1-s)/4",
                "(1-s)/4",
            ],
            "strict_domain": "all four displayed probabilities positive",
        },
        "character_orbit_representatives": [
            list(assignment) for assignment in ORBIT_REPRESENTATIVES
        ],
        "normalized_three_leaf_ambient_dimension": 9,
        "unlabelled_reticulate_models": 7,
        "topology_counts": counts,
        "common_target": {
            "delta": str(DELTA),
            "six_pair_orbit_coordinates": str(common_pair),
            "three_triple_orbit_coordinates": str(common_triple),
            "kappa": str(TARGET_KAPPA),
        },
        "common_witness_domain": {
            "every_edge_has_s=t": True,
            "internal_multiplier": "unique h in (1/8,7/8) for each model",
            "inheritance_probabilities": "1/2",
            "pendant_multipliers": "positive square roots recorded per model, all <2^-9",
            "minimum_transition_probability_is_strictly_positive": True,
        },
        "rank_certificate": {
            "minor_order": 9,
            "all_seven_nonzero_at_common_point": True,
            "records": reticulate_records,
        },
        "conclusion": (
            "All 39 labelled rooted reticulate three-port root blobs, "
            "representing 21 semi-directed topologies, are K2P-dominant and "
            "share one regular nine-dimensional open stochastic neighborhood."
        ),
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate["deterministic_sha256"] = sha256(payload.encode()).hexdigest()
    return certificate


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
                "deterministic_sha256": certificate["deterministic_sha256"],
                "normalized_three_leaf_ambient_dimension": certificate[
                    "normalized_three_leaf_ambient_dimension"
                ],
                "topology_counts": certificate["topology_counts"],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
