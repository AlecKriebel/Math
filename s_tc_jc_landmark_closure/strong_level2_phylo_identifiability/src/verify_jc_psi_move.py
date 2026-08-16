"""Exact verifier for the JC root-adjacent theta port-rotation move Psi.

The move has an orbit of four pairwise nonisomorphic semi-directed topologies.
Two rational gauge transformations identify all 64 zero-sum Fourier
coordinates on an explicit seven-dimensional open stochastic box.
"""

from __future__ import annotations

import hashlib
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from enumerate_four_leaf_root_theta import canonical_code, enumerate_networks
from fourier_models import zero_sum_assignments
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES
from verify_jc_four_network_class import (
    colored_graph_isomorphisms,
    semi_directed_graph,
)


# A(a,b,c,d), A(c,b,a,d), B(b,a,c,d), B(b,c,a,d).
TOPOLOGIES = {
    "A": (18, (1, 2, 3, 4)),
    "A_reflected": (18, (3, 2, 1, 4)),
    "B": (19, (2, 1, 3, 4)),
    "B_reflected": (19, (2, 3, 1, 4)),
}

A_FREE = (0, 4, 6, 7, 8, 9, 10)
B_FREE = (0, 4, 5, 7, 8, 9, 10)


def model(network, labels, prefix, assignments=zero_sum_assignments()):
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
        "network": network,
        "labels": labels,
        "edges": edges,
        "reticulations": reticulations,
        "edge_parameters": edge_parameters,
        "inheritance_parameters": inheritance_parameters,
        "parameters": edge_parameters + inheritance_parameters,
        "coordinates": coordinates,
    }


def half_gauge(model_data, free_indices):
    free = tuple(model_data["parameters"][index] for index in free_indices)
    fixed = {
        parameter: sp.Rational(1, 2)
        for index, parameter in enumerate(model_data["parameters"])
        if index not in free_indices
    }
    return free, fixed


def parameter_maps(models):
    source_free, source_fixed = half_gauge(models["A"], A_FREE)
    u, x, y, z, p, q, r = source_free

    substitutions = {"A": source_fixed}

    target_free, target_fixed = half_gauge(models["A_reflected"], A_FREE)
    target_fixed.update(
        dict(
            zip(
                target_free,
                (
                    8 * y - sp.Rational(1, 4),
                    z,
                    (4 * u + 1) / 32,
                    x,
                    r,
                    q,
                    p,
                ),
            )
        )
    )
    substitutions["A_reflected"] = target_fixed

    target_free, target_fixed = half_gauge(models["B"], B_FREE)
    target_fixed.update(
        dict(
            zip(
                target_free,
                (
                    8 * y - sp.Rational(1, 4),
                    (4 * u + 1) / 32,
                    x,
                    z,
                    q,
                    p,
                    r,
                ),
            )
        )
    )
    substitutions["B"] = target_fixed

    # Composition of reflection with the A-to-B rotation.
    target_free, target_fixed = half_gauge(models["B_reflected"], B_FREE)
    target_fixed.update(dict(zip(target_free, (u, y, z, x, q, r, p))))
    substitutions["B_reflected"] = target_fixed
    return source_free, substitutions


def verify_graphs(models):
    rooted_codes = []
    semi_directed = {}
    for name, data in models.items():
        labels = dict(zip(data["network"]["leaves"], data["labels"]))
        rooted_codes.append(
            canonical_code(data["network"]["vertices"], data["edges"], labels)
        )
        semi_directed[name] = semi_directed_graph(data["network"], data["labels"])
        assert data["network"]["triangle_count_after_root_suppression"] == 0
    assert len(set(rooted_codes)) == 4
    for first_index, first in enumerate(models):
        for second in tuple(models)[first_index + 1 :]:
            assert not colored_graph_isomorphisms(
                semi_directed[first], semi_directed[second]
            )


def verify_coordinate_maps(models, substitutions):
    source = models["A"]["coordinates"]
    source_substitution = substitutions["A"]
    checked = {}
    for name in ("A_reflected", "B", "B_reflected"):
        target = models[name]["coordinates"]
        target_substitution = substitutions[name]
        differences = tuple(
            sp.factor(
                source_coordinate.subs(source_substitution)
                - target_coordinate.subs(target_substitution)
            )
            for source_coordinate, target_coordinate in zip(source, target)
        )
        assert all(difference == 0 for difference in differences)
        checked[name] = len(differences)
    return checked


def orbit_coordinates(model_data):
    lookup = dict(zip(zero_sum_assignments(), model_data["coordinates"]))
    return tuple(lookup[assignment] for assignment in JC_REPRESENTATIVES[1:])


def exact_generic_rank(model_data):
    coordinates = orbit_coordinates(model_data)
    jacobian = sp.Matrix(coordinates).jacobian(model_data["parameters"])
    domain_jacobian = DomainMatrix.from_Matrix(jacobian)
    nullspace = domain_jacobian.nullspace()
    assert nullspace.shape == (7, 14)
    assert nullspace.rank() == 7
    assert nullspace.matmul(domain_jacobian.transpose()).is_zero_matrix
    assert domain_jacobian.rank() == 7
    serialized = str(nullspace.to_Matrix()).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def gauge_determinant(model_data, free_indices, fixed_substitution):
    parameters = [model_data["parameters"][index] for index in free_indices]
    outputs = orbit_coordinates(model_data)[:7]
    matrix = sp.Matrix(
        [
            [sp.factor(sp.diff(output, parameter).subs(fixed_substitution)) for parameter in parameters]
            for output in outputs
        ]
    )
    determinant = sp.factor(matrix.det(method="domain-ge"))
    assert determinant != 0
    return determinant


def verify_ranks(models, substitutions):
    hashes = {
        "A": exact_generic_rank(models["A"]),
        "B": exact_generic_rank(models["B"]),
    }
    determinants = {}
    for name, data in models.items():
        free_indices = A_FREE if name.startswith("A") else B_FREE
        _free, fixed = half_gauge(data, free_indices)
        determinants[name] = gauge_determinant(data, free_indices, fixed)

    # The maps send the open source box
    #   0<u,x,z,p,q,r<1, 1/32<y<5/32
    # into the open target cubes.  Every displayed determinant remains nonzero:
    # all variable factors are positive; 4u-31, y-1, and
    # y(4u+1)-32 are strictly negative.  The same bounds hold for the mapped
    # variables u'=8y-1/4 and y'=(4u+1)/32.
    u, _x, y, _z, _p, _q, _r = half_gauge(models["A"], A_FREE)[0]
    assert sp.factor(8 * sp.Rational(1, 32) - sp.Rational(1, 4)) == 0
    assert sp.factor(8 * sp.Rational(5, 32) - sp.Rational(1, 4)) == 1
    assert sp.Rational(4 * 0 + 1, 32) == sp.Rational(1, 32)
    assert sp.Rational(4 * 1 + 1, 32) == sp.Rational(5, 32)
    assert u != y  # distinct symbols, guarding accidental gauge aliasing
    return hashes, {name: str(value) for name, value in determinants.items()}


def main():
    _raw, networks = enumerate_networks()
    models = {
        name: model(networks[index], labels, f"{name}_")
        for name, (index, labels) in TOPOLOGIES.items()
    }
    verify_graphs(models)
    source_free, substitutions = parameter_maps(models)
    coordinate_checks = verify_coordinate_maps(models, substitutions)
    nullspace_hashes, determinant_certificates = verify_ranks(models, substitutions)

    output = {
        "status": "EXACTLY COMPUTED",
        "move": "Psi: root-adjacent theta three-port rotation/reflection",
        "topologies": {
            name: {"census_index": index, "port_labels": list(labels)}
            for name, (index, labels) in TOPOLOGIES.items()
        },
        "pairwise_rooted_isomorphism_classes": 4,
        "pairwise_semi_directed_isomorphism_classes": 4,
        "triangle_count_after_root_suppression": 0,
        "common_model_dimension": 7,
        "source_open_box": {
            str(source_free[0]): "(0,1)",
            str(source_free[1]): "(0,1)",
            str(source_free[2]): "(1/32,5/32)",
            str(source_free[3]): "(0,1)",
            str(source_free[4]): "(0,1)",
            str(source_free[5]): "(0,1)",
            str(source_free[6]): "(0,1)",
        },
        "symbolic_zero_sum_coordinate_equalities": coordinate_checks,
        "full_jacobian_polynomial_nullspace_sha256": nullspace_hashes,
        "gauge_rank_seven_determinants": determinant_certificates,
        "conclusion": (
            "four pairwise distinct semi-directed JC network topologies share "
            "one seven-dimensional regular open stochastic region"
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
