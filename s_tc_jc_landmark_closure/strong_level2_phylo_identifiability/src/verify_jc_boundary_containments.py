#!/usr/bin/env python3
"""Exact boundary-containment and strict-interior certificates.

This verifier resolves the 168 unequal-dimensional directions whose lifted
models have the same root marginal and were not directionally separated by
the compact Milestone 3E signature.  Seven S4 pair orbits occur.  A cubic
incoming-quartet invariant (and one quartic relabelling in the final orbit)
is identically zero on each smaller model and strictly nonzero throughout the
larger model's open stochastic cube.  Two of the seven directions also admit
explicit dominant rational maps into a zero-length-edge boundary sheet.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

from enumerate_four_leaf_root_theta import enumerate_networks
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices
from jc_root_spanning_atlas_data import INVARIANT_TEMPLATES
from verify_jc_incoming_port_atlas import (
    JC5_REPRESENTATIVES,
    coordinate_permutation5,
    lift_network,
    quartet_coordinate_indices,
)
from verify_jc_root_spanning_atlas import invariant_orbit


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "jc_boundary_containments.json"
INCOMING_CERTIFICATE = HERE / "certificates" / "jc_incoming_port_atlas.json"
ROOT_CERTIFICATE = HERE / "certificates" / "jc_root_spanning_atlas.json"

PAIR_ORBITS = (
    (96, 1, 4, (1, 2, 3, 4), 0, (1, 2, 4, 3), 0),
    (96, 414, 4, (1, 2, 3, 4), 22, (4, 1, 2, 3), 0),
    (144, 25, 6, (1, 2, 3, 4), 1, (1, 2, 4, 3), 0),
    (144, 265, 6, (1, 2, 3, 4), 11, (1, 2, 4, 3), 0),
    (144, 366, 6, (1, 2, 3, 4), 20, (4, 1, 2, 3), 0),
    (144, 438, 6, (1, 2, 3, 4), 23, (4, 1, 2, 3), 0),
    (144, 440, 6, (1, 2, 3, 4), 23, (4, 2, 1, 3), 6),
)


def model(networks, network_index, labels, prefix):
    parameters = sp.symbols(f"{prefix}0:15")
    network = lift_network(networks[network_index])
    reticulations = reticulation_vertices(network["vertices"])
    base = evaluate_jc_coordinates(
        network["vertices"],
        network["edges"],
        dict(zip(network["leaves"], range(1, 6))),
        JC5_REPRESENTATIVES,
        parameters[:12] + (sp.Integer(1), parameters[12]),
        dict(zip(reticulations, parameters[13:])),
    )
    permutation = coordinate_permutation5(tuple(labels) + (5,))
    return parameters, tuple(base[index] for index in permutation)


SELECTED_INVARIANTS = (
    invariant_orbit(INVARIANT_TEMPLATES[2])
    + invariant_orbit(INVARIANT_TEMPLATES[4])
)
OMIT_ONE_INDICES = quartet_coordinate_indices(1)


def feature_pullback(coordinates, feature_index):
    quartet = tuple(coordinates[index] for index in OMIT_ONE_INDICES)
    invariant = SELECTED_INVARIANTS[feature_index]
    answer = 0
    for monomial, coefficient in invariant:
        term = sp.Integer(coefficient)
        for coordinate in monomial:
            term *= quartet[coordinate]
        answer += term
    return sp.factor(answer)


def expected_strict_factors(parameters, orbit_index):
    b = parameters
    # Write the actual expected factors explicitly.  This is intentionally
    # redundant with symbolic contraction, so a changed edge ordering cannot
    # silently pass.
    if orbit_index == 0:
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]*b[6]*b[7]*b[9]**2
            *(b[1]-1)*(b[13]-1)*(b[14]-1)*(b[0]*b[1]-1)
            *(b[5]*b[6]-1)*(b[0]*b[5]*b[6]-1)
        )
    if orbit_index == 1:
        bracket = b[5]*b[6]*(b[13]*b[1] + (1-b[13])*b[3]) - 1
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]**2*b[6]**2*b[7]*b[8]**2
            *(b[0]-1)*(b[13]-1)*(b[14]-1)*(b[2]-1)
            *(b[0]*b[2]-1)*bracket
        )
    if orbit_index == 2:
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]*b[6]*b[7]*b[9]**2
            *(b[1]-1)*(b[13]-1)*(b[14]-1)*(b[6]-1)
            *(b[0]*b[1]-1)*(b[0]*b[6]-1)
        )
    if orbit_index == 3:
        return (
            -2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]*b[6]*b[7]*b[9]**2
            *(b[0]-1)*(b[1]-1)*(b[13]-1)*(b[14]-1)
            *(b[6]-1)*(b[1]*b[6]-1)
        )
    if orbit_index == 4:
        bracket = b[6]*(b[13]*b[0] + (1-b[13])*b[3]) - 1
        return (
            -2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]*b[6]**2*b[7]*b[8]**2
            *(b[1]-1)*(b[13]-1)*(b[14]-1)*(b[2]-1)**2*bracket
        )
    if orbit_index == 5:
        bracket = b[6]*(b[13]*b[1] + (1-b[13])*b[3]) - 1
        return (
            2*b[0]*b[1]*b[10]**2*b[11]**2*b[12]**2*b[13]*b[14]
            *b[2]*b[3]*b[4]*b[5]*b[6]**2*b[7]*b[8]**2
            *(b[0]-1)*(b[13]-1)*(b[14]-1)*(b[2]-1)
            *(b[0]*b[2]-1)*bracket
        )
    assert orbit_index == 6
    return (
        4*b[0]**2*b[1]*b[11]**2*b[12]**3*b[13]*b[2]**2*b[3]
        *b[4]**3*b[6]**2*b[7]**2*b[8]**3*b[9]**3
        *(b[0]-1)*(b[13]-1)*(b[14]-1)**2*(b[2]-1)*(b[0]*b[2]-1)
    )


def strict_reason(orbit_index):
    if orbit_index in {1, 4, 5}:
        return (
            "the final bracket is multiplier times a strict convex combination "
            "of open-cube multipliers minus one, hence is strictly negative; "
            "every other factor is also nonzero"
        )
    return (
        "every non-monomial factor is x-1 or a product of open-cube "
        "multipliers minus one, hence is strictly negative and nonzero"
    )


def map_case_zero(source):
    a = source
    half = sp.Rational(1, 2)
    denominator = a[0] + 1 - 2*a[0]*a[1]
    numerator = 2 - a[1]*(a[0] + 1)
    b0 = sp.factor(a[0]*a[1]*numerator/denominator)
    b5 = sp.factor(a[3]*denominator/numerator)
    inheritance0 = sp.factor(
        a[1]*(a[0]-1)**2
        /
        (2*(a[0]**2*a[1]**2 + a[0]*a[1]**2 - 4*a[0]*a[1] + a[0] + 1))
    )
    inheritance1 = sp.factor(a[2]/(a[2]+a[5]))
    edges = (
        b0, 1, half, half, half, b5, a[4], half,
        a[8], a[9], a[11], (a[2]+a[5])/2, a[12],
    )
    return edges + (inheritance0, inheritance1)


def map_case_one(source):
    a = source
    half = sp.Rational(1, 2)
    denominator = a[0] + 1 - 2*a[0]*a[1]
    numerator = 2 - a[1]*(a[0] + 1)
    delta = a[0]**2*a[1]**2 + a[0]*a[1]**2 - 4*a[0]*a[1] + a[0] + 1
    b0 = sp.factor(a[0]*a[1]*numerator/denominator)
    b2 = sp.factor(a[1]*a[11]*(a[0]-1)**2/delta)
    b3 = sp.factor(a[11]*denominator*numerator/delta)
    b6 = sp.factor(a[4]*denominator/numerator)
    inheritance1 = sp.factor(a[3]/(a[3]+a[5]))
    edges = (
        b0, 1, b2, b3, a[2], half, b6, half,
        a[8], a[9], half, (a[3]+a[5])/2, a[12],
    )
    return edges + (half, inheritance1)


def verify_boundary_map(networks, case):
    half = sp.Rational(1, 2)
    if case == 0:
        low_index, low_labels = 4, (1, 2, 3, 4)
        high_index, high_labels = 0, (1, 2, 4, 3)
        map_function = map_case_zero
    else:
        low_index, low_labels = 6, (1, 2, 3, 4)
        high_index, high_labels = 1, (1, 2, 4, 3)
        map_function = map_case_one

    source, low_coordinates = model(networks, low_index, low_labels, f"map{case}a_")
    target, high_coordinates = model(networks, high_index, high_labels, f"map{case}b_")
    low_gauge = {source[index]: half for index in (6, 7, 10, 13, 14)}
    mapped = map_function(source)
    substitution = {
        parameter: sp.sympify(value).subs(low_gauge)
        for parameter, value in zip(target, mapped)
    }
    for left, right in zip(low_coordinates, high_coordinates):
        assert sp.factor(sp.cancel(left.subs(low_gauge) - right.subs(substitution))) == 0

    free_indices = (0, 1, 2, 3, 4, 5, 8, 9, 11, 12)
    free = [source[index] for index in free_indices]
    rows = (1, 2, 3, 4, 5, 6, 7, 8, 15, 18)
    jacobian = sp.Matrix([low_coordinates[index].subs(low_gauge) for index in rows]).jacobian(free)
    determinant = sp.factor(jacobian.subs({parameter: half for parameter in free}).det())
    expected = (
        sp.Rational(99, 18014398509481984)
        if case == 0
        else -sp.Rational(99, 562949953421312)
    )
    assert determinant == expected

    source_half = tuple(half for _ in source)
    mapped_half = tuple(
        sp.factor(value.subs(dict(zip(source, source_half))))
        if hasattr(value, "subs") else sp.Rational(value)
        for value in mapped
    )
    assert mapped_half[1] == 1
    assert all(0 < value < 1 for index, value in enumerate(mapped_half) if index != 1)
    return {
        "source_network": low_index,
        "target_network": high_index,
        "source_labels": list(low_labels),
        "target_labels": list(high_labels),
        "coordinates_checked": len(low_coordinates),
        "source_gauge_fixed_parameter_indices": [6, 7, 10, 13, 14],
        "source_gauge_rank_minor_rows": list(rows),
        "source_gauge_rank_minor_at_half": str(determinant),
        "target_boundary_parameter_index": 1,
        "target_parameters_at_source_half": [str(value) for value in mapped_half],
        "map": [str(sp.factor(value)) for value in mapped],
    }


def generate_certificate():
    incoming = json.loads(INCOMING_CERTIFICATE.read_text())
    root = json.loads(ROOT_CERTIFICATE.read_text())
    components = incoming["components"]
    same_root_unresolved = []
    for lower in components:
        if lower["dimension"] != 10:
            continue
        for higher in components:
            if higher["dimension"] != 11:
                continue
            if lower["root_marginal_component"] != higher["root_marginal_component"]:
                continue
            if any(
                low == "1" and high == "0"
                for low, high in zip(lower["signature"], higher["signature"])
            ):
                continue
            same_root_unresolved.append((lower["id"], higher["id"]))
    assert len(same_root_unresolved) == 168
    assert len(PAIR_ORBITS) * 24 == len(same_root_unresolved)
    assert {pair[:2] for pair in PAIR_ORBITS} <= set(same_root_unresolved)

    _raw, networks = enumerate_networks()
    strict_certificates = []
    for orbit_index, (
        lower_component,
        higher_component,
        low_index,
        low_labels,
        high_index,
        high_labels,
        feature_index,
    ) in enumerate(PAIR_ORBITS):
        _low_parameters, low_coordinates = model(
            networks, low_index, low_labels, f"strict{orbit_index}a_"
        )
        high_parameters, high_coordinates = model(
            networks, high_index, high_labels, f"strict{orbit_index}b_"
        )
        low_pullback = feature_pullback(low_coordinates, feature_index)
        high_pullback = feature_pullback(high_coordinates, feature_index)
        assert low_pullback == 0
        expected = sp.factor(expected_strict_factors(high_parameters, orbit_index))
        assert sp.factor(high_pullback - expected) == 0
        strict_certificates.append(
            {
                "orbit_index": orbit_index,
                "S4_orbit_size": 24,
                "lower_component_representative": lower_component,
                "higher_component_representative": higher_component,
                "source_network": low_index,
                "source_labels": list(low_labels),
                "target_network": high_index,
                "target_labels": list(high_labels),
                "feature_index": feature_index,
                "source_pullback": "0",
                "target_pullback": str(high_pullback),
                "strict_nonzero_reason": strict_reason(orbit_index),
            }
        )

    boundary_maps = [
        verify_boundary_map(networks, 0),
        verify_boundary_map(networks, 1),
    ]

    root_unresolved = {
        tuple(pair) for pair in root["unresolved_directed_component_pairs"]
    }
    root_components = root["components"]
    compact_rejected = 0
    root_marginal_rejected = 0
    cross_root_unresolved = []
    for lower in components:
        if lower["dimension"] != 10:
            continue
        for higher in components:
            if higher["dimension"] != 11:
                continue
            if any(
                low == "1" and high == "0"
                for low, high in zip(lower["signature"], higher["signature"])
            ):
                compact_rejected += 1
                continue
            lower_root = lower["root_marginal_component"]
            higher_root = higher["root_marginal_component"]
            if lower_root == higher_root:
                continue  # settled by the strict certificates above
            lower_dimension = root_components[lower_root]["dimension"]
            higher_dimension = root_components[higher_root]["dimension"]
            rejected = False
            if lower_dimension >= higher_dimension:
                # Equal dimensions have distinct irreducible root closures;
                # a larger-dimensional root marginal also cannot be contained
                # in a smaller-dimensional one.
                rejected = True
            elif (lower_root, higher_root) not in root_unresolved:
                rejected = True
            if rejected:
                root_marginal_rejected += 1
            else:
                cross_root_unresolved.append((lower["id"], higher["id"]))
    assert (compact_rejected, root_marginal_rejected, len(cross_root_unresolved)) == (
        39168,
        384,
        600,
    )
    return {
        "status": {
            "same_root_unequal_dimension_stochastic_containment": "PROVED ABSENT",
            "two_algebraic_boundary_containment_orbits": "PROVED",
            "other_five_boundary_containment_orbits": "UNRESOLVED",
        },
        "same_root_directions_audited": len(same_root_unresolved),
        "pair_orbits_under_outgoing_S4": len(PAIR_ORBITS),
        "directions_per_pair_orbit": 24,
        "strict_open_cube_separation_certificates": strict_certificates,
        "dominant_boundary_maps": boundary_maps,
        "algebraic_boundary_containment_directions_proved": 48,
        "all_lower_to_higher_directions": 40320,
        "directions_rejected_by_compact_incoming_signatures": compact_rejected,
        "directions_rejected_by_root_marginal_certificates": root_marginal_rejected,
        "directions_rejected_by_same_root_strict_factors": 168,
        "combined_stochastic_containment_directions_rejected": (
            compact_rejected + root_marginal_rejected + 168
        ),
        "cross_root_directions_unresolved": len(cross_root_unresolved),
        "unresolved_cross_root_component_pairs": [
            list(pair) for pair in cross_root_unresolved
        ],
        "conclusion": (
            "all 168 same-root dimension-10 to dimension-11 directions have "
            "disjoint open stochastic images; two 24-direction orbits are "
            "nevertheless proper algebraic boundary containments"
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
                "same_root_directions_audited": certificate[
                    "same_root_directions_audited"
                ],
                "pair_orbits_under_outgoing_S4": certificate[
                    "pair_orbits_under_outgoing_S4"
                ],
                "algebraic_boundary_containment_directions_proved": certificate[
                    "algebraic_boundary_containment_directions_proved"
                ],
                "combined_stochastic_containment_directions_rejected": certificate[
                    "combined_stochastic_containment_directions_rejected"
                ],
                "cross_root_directions_unresolved": certificate[
                    "cross_root_directions_unresolved"
                ],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
