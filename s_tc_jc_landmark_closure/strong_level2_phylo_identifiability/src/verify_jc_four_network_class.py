"""Exact certificate for the first nontrivial class in the four-leaf JC atlas.

Four entries in the root-spanning theta census have the inherited eight-
dimensional JC closure.  This verifier proves that they are not a new local
ambiguity: they are exactly two Theta-related semi-directed topologies, each
with two reversible root placements.  It also constructs one quadratic-
algebraic interior distribution common to all four models and certifies rank
eight at that same point.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations, product
import json

import sympy as sp

from enumerate_four_leaf_root_theta import canonical_code, enumerate_networks
from fourier_models import (
    source_parameterization,
    target_parameterization,
    zero_sum_assignments,
)
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES, ORBIT_INDEX
from verify_model_robustness import (
    inherited_source_substitution,
    inherited_target_substitution,
    numerator_remainder,
    verify_jc_replay,
)


CANDIDATES = {
    0: (1, 2, 3, 4),
    4: (1, 2, 4, 3),
    13: (2, 1, 3, 4),
    22: (2, 1, 3, 4),
}

# The common distribution is the inherited source point after globally
# relabelling old taxa by (1 2)(3 4).  If q_old[i] denotes the i-th coordinate
# in JC_REPRESENTATIVES, then q_old[i] = q_new[OLD_TO_NEW[i]].
OLD_TO_NEW = (0, 1, 6, 5, 7, 3, 2, 4, 8, 9, 10, 14, 12, 13, 11)

MINOR_COLUMNS = {
    0: (0, 1, 3, 4, 6, 7, 8, 9),
    4: (0, 1, 3, 4, 5, 6, 8, 9),
    13: (0, 1, 2, 3, 6, 7, 9, 10),
    22: (0, 1, 2, 4, 6, 7, 9, 10),
}


def parameterization(network, labels, prefix, assignments=zero_sum_assignments()):
    edges = tuple(tuple(edge) for edge in network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    edge_parameters = sp.symbols(f"{prefix}e0:{len(edges)}")
    inheritance_parameters = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], labels)),
        assignments,
        edge_parameters,
        dict(zip(reticulations, inheritance_parameters)),
    )
    return {
        "edge_parameters": edge_parameters,
        "inheritance_parameters": inheritance_parameters,
        "reticulations": reticulations,
        "coordinates": coordinates,
    }


def inherited_relations_in_new_labels(coordinates):
    """Return the inherited six equations after the global relabelling."""
    old = [coordinates[OLD_TO_NEW[index] - 1] for index in range(1, 15)]
    A, B, C, D, E, F, G, H, J, K, L, M, N, O = old
    return (
        J - K - M + N,
        J - A * H - B * F + C * E,
        G * L - E * N,
        L**2 - B * E * H,
        B * M - D * L - B**2 * F + B * C * E,
        B * E * O - B * G * H - C * E * L + D * E * H,
    )


def semi_directed_graph(network, labels):
    """Forget tree-edge directions and suppress the degree-two root artifact."""
    leaf_labels = dict(zip(network["leaves"], labels))
    colors = {}
    for vertex, color in network["vertices"].items():
        if color == "S":
            continue
        if color == "L":
            colors[vertex] = f"L{leaf_labels[vertex]}"
        elif color in {"R", "X"}:
            colors[vertex] = "R"
        else:
            colors[vertex] = "T"

    edges = []
    root_children = []
    for tail, head in (tuple(edge) for edge in network["edges"]):
        if tail == "S":
            root_children.append(head)
            continue
        assert head != "S"
        if network["vertices"][head] in {"R", "X"}:
            edges.append(("D", tail, head))
        else:
            edges.append(("U",) + tuple(sorted((tail, head))))

    assert len(root_children) == 2
    left, right = root_children
    left_reticulation = network["vertices"][left] in {"R", "X"}
    right_reticulation = network["vertices"][right] in {"R", "X"}
    assert not (left_reticulation and right_reticulation)
    if left_reticulation:
        edges.append(("D", right, left))
    elif right_reticulation:
        edges.append(("D", left, right))
    else:
        edges.append(("U",) + tuple(sorted((left, right))))
    return colors, tuple(sorted(edges))


def colored_graph_isomorphisms(first, second):
    first_colors, first_edges = first
    second_colors, second_edges = second
    first_groups = defaultdict(list)
    second_groups = defaultdict(list)
    for vertex, color in first_colors.items():
        first_groups[color].append(vertex)
    for vertex, color in second_colors.items():
        second_groups[color].append(vertex)
    if {key: len(value) for key, value in first_groups.items()} != {
        key: len(value) for key, value in second_groups.items()
    }:
        return ()

    keys = sorted(first_groups)
    answers = []
    for choices in product(*(permutations(second_groups[key]) for key in keys)):
        mapping = {
            old: new
            for key, choice in zip(keys, choices)
            for old, new in zip(first_groups[key], choice)
        }
        transported = []
        for edge_type, left, right in first_edges:
            left, right = mapping[left], mapping[right]
            if edge_type == "U":
                left, right = sorted((left, right))
            transported.append((edge_type, left, right))
        if tuple(sorted(transported)) == second_edges:
            answers.append(mapping)
    return tuple(answers)


def verify_topologies(networks):
    rooted_codes = []
    semi_directed = {}
    for index, labels in CANDIDATES.items():
        network = networks[index]
        leaf_label_map = dict(zip(network["leaves"], labels))
        rooted_codes.append(
            canonical_code(network["vertices"], tuple(map(tuple, network["edges"])), leaf_label_map)
        )
        semi_directed[index] = semi_directed_graph(network, labels)
    assert len(set(rooted_codes)) == 4

    equivalent_pairs = set()
    for left in CANDIDATES:
        for right in CANDIDATES:
            if colored_graph_isomorphisms(semi_directed[left], semi_directed[right]):
                equivalent_pairs.add((left, right))
    expected = {
        (left, right)
        for block in ((0, 4), (13, 22))
        for left in block
        for right in block
    }
    assert equivalent_pairs == expected
    return ((0, 4), (13, 22))


def inherited_values():
    _source_coordinates, source_parameters = source_parameterization("JC", "")
    _target_coordinates, target_parameters = target_parameterization("JC", "")
    beta = sp.Symbol("beta")
    source = {
        str(parameter): value
        for parameter, value in inherited_source_substitution(source_parameters).items()
    }
    target = {
        str(parameter): value
        for parameter, value in inherited_target_substitution(target_parameters, beta).items()
    }
    return beta, source, target


def common_substitutions(models, beta, source, target):
    """Construct the all-four common point from Theta, T, and root moves."""
    answer = {}

    # Network 22, source side of Theta.  Its generic edge ordering is
    # AB,BC,rA,rC,AF,CD,DE,EF,pB,pD,pE,pF.  The generic inheritance variable
    # at V selects BC first, whereas lambda_C selects rC in the inherited file.
    model = models[22]
    edge_values = [
        source[f"x_{name}"]
        for name in ("AB", "BC", "rA", "rC", "AF", "CD", "DE", "EF", "pB", "pD", "pE", "pF")
    ]
    substitution = dict(zip(model["edge_parameters"], edge_values))
    substitution.update(
        dict(
            zip(
                model["inheritance_parameters"],
                (1 - source["lambda_C"], source["lambda_F"]),
            )
        )
    )
    answer[22] = substitution

    # Network 13 is the same source semi-directed topology rooted on AF.
    model = models[13]
    edge_values = (
        source["x_rA"] * source["x_rC"],
        source["x_AB"],
        source["x_BC"],
        source["x_rA"],
        source["x_AF"] / source["x_rA"],
        source["x_CD"],
        source["x_DE"],
        source["x_EF"],
        source["x_pB"],
        source["x_pD"],
        source["x_pE"],
        source["x_pF"],
    )
    substitution = dict(zip(model["edge_parameters"], edge_values))
    substitution.update(
        dict(zip(model["inheritance_parameters"], (source["lambda_C"], source["lambda_F"])))
    )
    answer[13] = substitution

    # Apply the following exact triangle redirection to the target side of
    # Theta.  For old reticulation C in triangle A-B-C, put
    #   X=x_AB,
    #   Y=lambda*x_AC+(1-lambda)*x_AB*x_BC.
    # Redirect to B, retain the three values in the new roles AC,AB,CB, and
    # rescale the B,C arms by X/Y,Y/X.  The four effective triangle Fourier
    # factors, including the three-character factor, are then unchanged.
    x = target["x_AB"]
    x_ac = target["x_rA"] * target["x_rC"]
    x_bc = target["x_BC"]
    inheritance = target["lambda_C"]
    X = x
    Y = sp.factor(inheritance * x_ac + (1 - inheritance) * x * x_bc)

    model = models[0]
    edge_values = (
        x,
        target["x_rA"],
        target["x_rC"],
        x_bc,
        target["x_AF"],
        sp.factor(target["x_CD"] * Y / X),
        target["x_DE"],
        target["x_EF"],
        target["x_pD"],
        target["x_pE"],
        sp.factor(target["x_pB"] * X / Y),
        target["x_pF"],
    )
    substitution = dict(zip(model["edge_parameters"], edge_values))
    substitution.update(
        dict(zip(model["inheritance_parameters"], (inheritance, target["lambda_F"])))
    )
    answer[0] = substitution

    # Network 4 is the same target semi-directed topology rooted on AF.  Split
    # its effective AF multiplier z as (3/4)*(4z/3).
    model = models[4]
    source_model = models[0]
    source_substitution = answer[0]
    source_edges = source_model["edge_parameters"]
    z = source_substitution[source_edges[4]]
    edge_values = (
        source_substitution[source_edges[0]],
        sp.Rational(3, 4),
        sp.factor(sp.Rational(4, 3) * z),
        source_substitution[source_edges[5]],
        source_substitution[source_edges[6]],
        source_substitution[source_edges[7]],
        source_substitution[source_edges[1]] * source_substitution[source_edges[2]],
        source_substitution[source_edges[3]],
        source_substitution[source_edges[8]],
        source_substitution[source_edges[9]],
        source_substitution[source_edges[11]],
        source_substitution[source_edges[10]],
    )
    substitution = dict(zip(model["edge_parameters"], edge_values))
    source_inheritance = source_model["inheritance_parameters"]
    substitution.update(
        dict(
            zip(
                model["inheritance_parameters"],
                (
                    source_substitution[source_inheritance[1]],
                    source_substitution[source_inheritance[0]],
                ),
            )
        )
    )
    answer[4] = substitution
    return answer


def theta_target_model(network):
    """The inherited target after (1 2)(3 4), on census network 22."""
    return parameterization(network, (3, 1, 2, 4), "theta_target_")


def verify_common_point(models, substitutions, virtual_target, beta, target):
    minimal_polynomial = 43337075 * beta**2 - 36083110 * beta + 7336259
    assert sp.Poly(minimal_polynomial, beta).is_irreducible

    # First replay the inherited certificate, including its exact isolating
    # interval and all target-parameter inequalities.
    verify_jc_replay()

    target_edge_values = [
        target[f"x_{name}"]
        for name in ("AB", "BC", "rA", "rC", "AF", "CD", "DE", "EF", "pB", "pD", "pE", "pF")
    ]
    virtual_substitution = dict(zip(virtual_target["edge_parameters"], target_edge_values))
    virtual_substitution.update(
        dict(
            zip(
                virtual_target["inheritance_parameters"],
                (1 - target["lambda_C"], target["lambda_F"]),
            )
        )
    )

    base = models[22]["coordinates"]
    base_substitution = substitutions[22]
    compared = 0
    for coordinate_index in range(64):
        base_value = base[coordinate_index].subs(base_substitution)
        virtual_value = virtual_target["coordinates"][coordinate_index].subs(virtual_substitution)
        remainder, denominator = numerator_remainder(
            base_value - virtual_value, beta, minimal_polynomial
        )
        assert remainder == 0 and denominator != 0
        for network_index in (0, 4):
            candidate_value = models[network_index]["coordinates"][coordinate_index].subs(
                substitutions[network_index]
            )
            remainder, denominator = numerator_remainder(
                base_value - candidate_value, beta, minimal_polynomial
            )
            assert remainder == 0 and denominator != 0
        assert sp.factor(
            base_value - models[13]["coordinates"][coordinate_index].subs(substitutions[13])
        ) == 0
        compared += 1
    assert compared == 64

    # Exact normal forms for the two beta-dependent candidate points.
    values_0 = tuple(substitutions[0][parameter] for parameter in (
        models[0]["edge_parameters"] + models[0]["inheritance_parameters"]
    ))
    expected_0 = (
        24835 * beta / (20678 - 24835 * beta),
        sp.Rational(2, 3),
        sp.Rational(3, 4),
        sp.Rational(1, 2),
        sp.Rational(10339, 53010) / beta,
        sp.Rational(1477, 8725) / beta,
        sp.Rational(171, 775),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(31, 190),
        sp.Rational(14901, 20678),
        sp.Rational(1767, 4832),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
    )
    values_4 = tuple(substitutions[4][parameter] for parameter in (
        models[4]["edge_parameters"] + models[4]["inheritance_parameters"]
    ))
    expected_4 = (
        24835 * beta / (20678 - 24835 * beta),
        sp.Rational(3, 4),
        sp.Rational(20678, 79515) / beta,
        sp.Rational(1477, 8725) / beta,
        sp.Rational(171, 775),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(31, 190),
        sp.Rational(1767, 4832),
        sp.Rational(14901, 20678),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
    )
    assert all(sp.factor(actual - expected) == 0 for actual, expected in zip(values_0, expected_0))
    assert all(sp.factor(actual - expected) == 0 for actual, expected in zip(values_4, expected_4))

    # Extra inequalities introduced by redirection and the second root split.
    # Together with the inherited interval proof, these establish 0<p<1 for
    # every multiplier and inheritance parameter without floating point.
    lower = sp.Rational(441, 1250)
    upper = sp.Rational(3529, 10000)
    assert 0 < lower < upper
    assert 2 * 24835 * upper < 20678
    assert lower > sp.Rational(10339, 53010)
    assert lower > sp.Rational(1477, 8725)
    assert lower > sp.Rational(20678, 79515)
    assert 0 < sp.Rational(14901, 20678) < 1
    for value in expected_0 + expected_4:
        if beta not in value.free_symbols:
            assert 0 < value < 1

    # Rational source-side points are immediate.
    for network_index in (13, 22):
        assert all(0 < value < 1 for value in substitutions[network_index].values())
    return minimal_polynomial


def verify_invariant_pullbacks(models):
    for network_index, model in models.items():
        coordinate_lookup = dict(zip(zero_sum_assignments(), model["coordinates"]))
        representatives = tuple(coordinate_lookup[g] for g in JC_REPRESENTATIVES[1:])
        assert all(sp.factor(relation) == 0 for relation in inherited_relations_in_new_labels(representatives))


def verify_common_ranks(models, substitutions, beta, minimal_polynomial):
    certificates = {}
    for network_index, model in models.items():
        parameters = model["edge_parameters"] + model["inheritance_parameters"]
        chosen = [parameters[index] for index in MINOR_COLUMNS[network_index]]
        coordinate_lookup = dict(zip(zero_sum_assignments(), model["coordinates"]))
        outputs = [coordinate_lookup[g] for g in JC_REPRESENTATIVES[1:9]]
        jacobian = sp.Matrix(
            [
                [
                    sp.factor(sp.diff(output, parameter).subs(substitutions[network_index]))
                    for parameter in chosen
                ]
                for output in outputs
            ]
        )
        determinant = sp.factor(jacobian.det(method="domain-ge"))
        if beta in determinant.free_symbols:
            remainder, denominator = numerator_remainder(
                determinant, beta, minimal_polynomial
            )
            assert remainder != 0 and denominator != 0
            certificates[network_index] = {
                "minimal_polynomial_numerator_remainder": str(remainder),
                "denominator": str(denominator),
            }
        else:
            assert determinant != 0
            certificates[network_index] = {"determinant": str(determinant)}
    return certificates


def main():
    _raw, networks = enumerate_networks()
    topology_classes = verify_topologies(networks)

    models = {
        index: parameterization(networks[index], labels, f"n{index}_")
        for index, labels in CANDIDATES.items()
    }
    verify_invariant_pullbacks(models)

    beta, source, target = inherited_values()
    substitutions = common_substitutions(models, beta, source, target)
    virtual_target = theta_target_model(networks[22])
    minimal_polynomial = verify_common_point(
        models, substitutions, virtual_target, beta, target
    )
    rank_certificates = verify_common_ranks(
        models, substitutions, beta, minimal_polynomial
    )

    output = {
        "status": "EXACTLY COMPUTED",
        "candidate_network_indices": sorted(CANDIDATES),
        "candidate_leaf_labels_by_port_order": {
            str(index): list(labels) for index, labels in CANDIDATES.items()
        },
        "rooted_isomorphism_classes": 4,
        "semi_directed_isomorphism_classes": [list(block) for block in topology_classes],
        "six_invariant_pullbacks_zero_for_every_candidate": True,
        "common_zero_sum_fourier_coordinates_checked": 64,
        "common_point_number_field": {
            "minimal_polynomial": str(minimal_polynomial),
            "isolating_interval": ["441/1250", "3529/10000"],
        },
        "rank_eight_minor_columns": {
            str(index): list(columns) for index, columns in MINOR_COLUMNS.items()
        },
        "rank_certificates": {
            str(index): value for index, value in rank_certificates.items()
        },
        "conclusion": (
            "four equal eight-dimensional JC closures and one common regular "
            "open stochastic region; exactly two Theta-related semi-directed "
            "topologies, with two root placements each"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
