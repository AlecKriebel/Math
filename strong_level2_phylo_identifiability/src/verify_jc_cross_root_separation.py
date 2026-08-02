#!/usr/bin/env python3
"""Exact strict separation of every remaining cross-root JC direction.

Milestone 3F leaves 600 dimension-10-to-11 incoming-port pairs whose root
marginals lie in ten unresolved directed S4 orbits.  For each root orbit, an
existing root-atlas invariant vanishes on the smaller model and factors into
a strictly nonzero expression on the larger model's complete open cube.
Marginalization therefore proves that all 600 five-port image pairs are
disjoint, closing the one-sided stochastic-containment audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import enumerate_networks
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from jc_root_spanning_atlas_data import INVARIANT_TEMPLATES
from probe_four_leaf_jc_atlas import JC_REPRESENTATIVES, coordinate_permutation
from verify_jc_root_spanning_atlas import invariant_orbit, item_action, move_components


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_cross_root_separation.json"
ROOT_CERTIFICATE = HERE / "certificates" / "jc_root_spanning_atlas.json"
INCOMING_CERTIFICATE = HERE / "certificates" / "jc_incoming_port_atlas.json"
BOUNDARY_CERTIFICATE = HERE / "certificates" / "jc_boundary_containments.json"

# (lower root component, higher root component, selected feature index,
#  expected lower representative, expected higher representative)
ROOT_PAIR_ORBITS = (
    (0, 24, 2, (0, (1, 2, 3, 4)), (2, (1, 2, 3, 4))),
    (0, 48, 6, (0, (1, 2, 3, 4)), (9, (1, 2, 3, 4))),
    (0, 49, 10, (0, (1, 2, 3, 4)), (9, (1, 2, 4, 3))),
    (12, 36, 56, (1, (1, 2, 3, 4)), (3, (1, 2, 3, 4))),
    (12, 48, 8, (1, (1, 2, 3, 4)), (9, (1, 2, 3, 4))),
    (12, 74, 5, (1, (1, 2, 3, 4)), (16, (1, 3, 2, 4))),
    (12, 86, 8, (1, (1, 2, 3, 4)), (17, (1, 3, 2, 4))),
    (96, 3, 31, (18, (1, 2, 3, 4)), (0, (2, 1, 3, 4))),
    (96, 14, 2, (18, (1, 2, 3, 4)), (1, (1, 3, 2, 4))),
    (96, 84, 7, (18, (1, 2, 3, 4)), (17, (1, 2, 3, 4))),
)
EXPECTED_DIRECTION_COUNTS = (48, 48, 48, 144, 48, 48, 96, 24, 72, 24)

ALL_INVARIANTS = tuple(
    invariant
    for template in INVARIANT_TEMPLATES
    for invariant in invariant_orbit(template)
)
assert len(ALL_INVARIANTS) == 60


def root_item(root_certificate, component_index):
    member = root_certificate["components"][component_index]["members"][0]
    return member["network_index"], tuple(member["port_labels"])


def model(networks, item, prefix):
    network_index, labels = item
    network = networks[network_index]
    edges = tuple(map(tuple, network["edges"]))
    reticulations = reticulation_vertices(network["vertices"])
    parameters = sp.symbols(f"{prefix}0:{len(edges) + len(reticulations)}")
    coordinates = evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], range(1, 5))),
        JC_REPRESENTATIVES,
        parameters[: len(edges)],
        dict(zip(reticulations, parameters[len(edges) :])),
    )
    permutation = coordinate_permutation(labels)
    return parameters, tuple(coordinates[index] for index in permutation)


def pullback(coordinates, invariant):
    result = 0
    for monomial, coefficient in invariant:
        term = sp.Integer(coefficient)
        for coordinate in monomial:
            term *= coordinates[coordinate]
        result += term
    return sp.factor(result)


def expected_factor(parameters, pair_index):
    b = parameters
    if pair_index == 0:
        return (
            -2*b[0]*b[1]*b[10]**2*b[11]*b[12]*b[13]*b[2]*b[3]
            *b[4]*b[5]*b[6]**2*b[8]*b[9]**2
            *(b[0]-1)*(b[12]-1)*(b[3]-1)
        )
    if pair_index == 1:
        return (
            2*b[0]*b[10]*b[11]*b[13]*b[4]*b[5]*b[6]*b[8]*b[9]
            *(b[1]-1)*(b[1]+1)*(b[12]-1)
        )
    if pair_index == 2:
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]*b[13]*b[2]*b[3]
            *b[4]*b[5]*b[6]*b[7]*b[8]**2*b[9]**2
            *(b[0]-1)*(b[1]-1)*(b[12]-1)*(b[13]-1)
            *(b[6]-1)*(b[1]*b[6]-1)
        )
    if pair_index == 3:
        return (
            b[0]*b[1]**2*b[10]**3*b[11]**2*b[12]**2*b[2]**2*b[3]**2
            *b[4]*b[5]**2*b[7]**2*b[8]**3*b[9]**2
            *(b[0]-1)**2*(b[12]-1)*(b[13]-1)**2
            *(b[3]-1)*(b[0]*b[3]-1)
        )
    if pair_index == 4:
        return (
            -2*b[1]*b[10]*b[11]*b[12]*b[13]*b[2]*b[3]*b[5]*b[6]
            *b[8]*b[9]*(b[0]-1)*(b[0]+1)
        )
    if pair_index == 5:
        return (
            -2*b[0]*b[1]*b[10]**2*b[11]*b[12]*b[13]*b[2]*b[3]
            *b[4]*b[5]*b[6]**2*b[8]**2*b[9]
            *(b[1]-1)*(b[12]-1)*(b[2]-1)
        )
    if pair_index == 6:
        return (
            -2*b[1]*b[10]*b[11]*b[12]*b[13]*b[2]*b[4]*b[5]*b[6]
            *b[8]*b[9]*(b[0]-1)*(b[0]+1)
        )
    if pair_index == 7:
        positive_mixture = b[12]*b[0]*b[1]*b[2] + (1-b[12])*b[3]
        return (
            -2*b[0]*b[1]*b[10]**3*b[11]**3*b[12]*b[13]**2*b[2]*b[3]
            *b[4]**2*b[5]**3*b[6]**3*b[7]*b[8]**3*b[9]**4
            *(b[0]-1)**2*(b[12]-1)*(b[13]-1)*(b[6]-1)**2
            *positive_mixture
        )
    if pair_index == 8:
        return (
            2*b[0]*b[1]*b[10]**2*b[11]*b[12]*b[13]*b[2]*b[3]
            *b[4]**2*b[5]*b[6]**2*b[8]*b[9]**2
            *(b[0]-1)**2*(b[12]-1)
        )
    assert pair_index == 9
    return (
        -2*b[1]*b[10]*b[11]*b[12]*b[13]*b[2]*b[4]*b[5]*b[6]
        *b[8]*b[9]*(b[0]-1)*(b[0]+1)
    )


def strict_reason(pair_index):
    if pair_index == 7:
        return (
            "the final factor is the strictly positive convex combination "
            "lambda*x0*x1*x2 + (1-lambda)*x3; all remaining factors are "
            "nonzero on the open cube"
        )
    return (
        "all monomial factors are positive; every x-1 or product-minus-one "
        "factor is strictly negative, and every x+1 factor is positive"
    )


def root_pair_action_data(networks, root_topology):
    item_to_component = {
        item: component_index
        for component_index, component in enumerate(root_topology["components"])
        for item in component
    }

    def image(component_index, permutation):
        representative = root_topology["components"][component_index][0]
        transformed = item_action(
            networks,
            root_topology["rooted_code_to_item"],
            representative,
            permutation,
        )
        return item_to_component[transformed]

    pair_to_orbit = {}
    orbit_sizes = []
    for pair_index, (lower, higher, _feature, _low_item, _high_item) in enumerate(
        ROOT_PAIR_ORBITS
    ):
        orbit = {
            (image(lower, permutation), image(higher, permutation))
            for permutation in permutations((1, 2, 3, 4))
        }
        orbit_sizes.append(len(orbit))
        for pair in orbit:
            assert pair not in pair_to_orbit
            pair_to_orbit[pair] = pair_index
    return pair_to_orbit, tuple(orbit_sizes)


def generate_certificate():
    root_certificate = json.loads(ROOT_CERTIFICATE.read_text())
    incoming_certificate = json.loads(INCOMING_CERTIFICATE.read_text())
    boundary_certificate = json.loads(BOUNDARY_CERTIFICATE.read_text())
    _raw, networks = enumerate_networks()
    root_topology = move_components(networks)

    strict_certificates = []
    for pair_index, (
        lower_component,
        higher_component,
        feature_index,
        expected_low_item,
        expected_high_item,
    ) in enumerate(ROOT_PAIR_ORBITS):
        low_item = root_item(root_certificate, lower_component)
        high_item = root_item(root_certificate, higher_component)
        assert low_item == expected_low_item
        assert high_item == expected_high_item
        _low_parameters, low_coordinates = model(
            networks, low_item, f"cross{pair_index}a"
        )
        high_parameters, high_coordinates = model(
            networks, high_item, f"cross{pair_index}b"
        )
        invariant = ALL_INVARIANTS[feature_index]
        low_pullback = pullback(low_coordinates, invariant)
        high_pullback = pullback(high_coordinates, invariant)
        assert low_pullback == 0
        expected = sp.factor(expected_factor(high_parameters, pair_index))
        assert sp.factor(high_pullback - expected) == 0
        strict_certificates.append(
            {
                "orbit_index": pair_index,
                "lower_root_component": lower_component,
                "higher_root_component": higher_component,
                "lower_representative": [low_item[0], list(low_item[1])],
                "higher_representative": [high_item[0], list(high_item[1])],
                "feature_index": feature_index,
                "invariant_degree": len(invariant[0][0]),
                "invariant_support": len(invariant),
                "lower_pullback": "0",
                "higher_pullback": str(high_pullback),
                "strict_nonzero_reason": strict_reason(pair_index),
            }
        )

    pair_to_orbit, root_orbit_sizes = root_pair_action_data(networks, root_topology)
    incoming_components = incoming_certificate["components"]
    direction_counts = Counter()
    unresolved_pairs = boundary_certificate["unresolved_cross_root_component_pairs"]
    assert len(unresolved_pairs) == 600
    for lower, higher in unresolved_pairs:
        root_pair = (
            incoming_components[lower]["root_marginal_component"],
            incoming_components[higher]["root_marginal_component"],
        )
        direction_counts[pair_to_orbit[root_pair]] += 1
    assert tuple(direction_counts[index] for index in range(10)) == (
        EXPECTED_DIRECTION_COUNTS
    )
    assert sum(direction_counts.values()) == 600

    return {
        "status": {
            "cross_root_stochastic_containments": "PROVED ABSENT",
            "complete_incoming_atlas_one_sided_containment_classification": "PROVED",
        },
        "root_pair_orbits": len(ROOT_PAIR_ORBITS),
        "root_pair_orbit_sizes": list(root_orbit_sizes),
        "strict_root_marginal_certificates": strict_certificates,
        "incoming_directions_by_root_pair_orbit": [
            direction_counts[index] for index in range(10)
        ],
        "cross_root_directions_separated": sum(direction_counts.values()),
        "previously_separated_directions": 39720,
        "all_lower_to_higher_directions": 40320,
        "all_lower_to_higher_directions_with_disjoint_open_images": 40320,
        "one_sided_stochastic_containments": 0,
        "conclusion": (
            "every dimension-10 model and every dimension-11 model in the "
            "incoming-port atlas have disjoint complete open stochastic images"
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
                "root_pair_orbits": certificate["root_pair_orbits"],
                "cross_root_directions_separated": certificate[
                    "cross_root_directions_separated"
                ],
                "all_lower_to_higher_directions_with_disjoint_open_images": certificate[
                    "all_lower_to_higher_directions_with_disjoint_open_images"
                ],
                "one_sided_stochastic_containments": certificate[
                    "one_sided_stochastic_containments"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
