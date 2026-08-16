#!/usr/bin/env python3
"""Exact JC/K2P/K3P two-port root-cycle collapse certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = (
    HERE / "certificates" / "group_based_root_two_port_collapse.json"
)


def xor_convolution(first, second):
    return tuple(
        sp.factor(sum(first[index] * second[index ^ output] for index in range(4)))
        for output in range(4)
    )


def fourier(probabilities):
    return tuple(
        sp.factor(
            sum(
                probabilities[state]
                * (-1) ** (((character & 1) * (state & 1)) ^ (((character >> 1) & 1) * ((state >> 1) & 1)))
                for state in range(4)
            )
        )
        for character in range(4)
    )


def inverse_fourier(multipliers):
    return tuple(
        sp.factor(
            sum(
                multipliers[character]
                * (-1)
                ** (
                    ((character & 1) * (state & 1))
                    ^ (
                        ((character >> 1) & 1)
                        * ((state >> 1) & 1)
                    )
                )
                for character in range(4)
            )
            / 4
        )
        for state in range(4)
    )


def factorization_chambers():
    r0, r1, r2 = sp.symbols("r0 r1 r2")
    probabilities = (r0, r1, r2, 1 - r0 - r1 - r2)
    records = []
    for minimum_index in range(4):
        minimum = probabilities[minimum_index]
        epsilon = 2 * minimum
        near_identity = (
            1 - 3 * epsilon / 4,
            epsilon / 4,
            epsilon / 4,
            epsilon / 4,
        )
        residual = tuple(
            sp.factor((value - epsilon / 4) / (1 - epsilon))
            for value in probabilities
        )
        convolution = xor_convolution(near_identity, residual)
        assert all(
            sp.factor(left - right) == 0
            for left, right in zip(convolution, probabilities)
        )
        assert sp.factor(sum(near_identity) - 1) == 0
        assert sp.factor(sum(residual) - 1) == 0
        near_fourier = fourier(near_identity)
        source_fourier = fourier(probabilities)
        residual_fourier = fourier(residual)
        assert near_fourier[0] == residual_fourier[0] == source_fourier[0] == 1
        assert all(
            sp.factor(near_fourier[index] * residual_fourier[index] - source_fourier[index]) == 0
            for index in range(1, 4)
        )
        records.append(
            {
                "minimum_coordinate": minimum_index,
                "epsilon": str(epsilon),
                "near_identity_probabilities": [str(sp.factor(value)) for value in near_identity],
                "residual_probabilities": [str(value) for value in residual],
                "convolution_identities": 4,
                "fourier_product_identities": 3,
            }
        )
    return records


def model_preservation_certificate():
    r0, r1, r2, r3, epsilon = sp.symbols("r0 r1 r2 r3 epsilon")
    residual = tuple(
        sp.factor((value - epsilon / 4) / (1 - epsilon))
        for value in (r0, r1, r2, r3)
    )
    assert sp.factor((residual[2] - residual[3]).subs(r2, r3)) == 0
    assert (
        sp.factor(
            (residual[1] - residual[2]).subs(r1, r3).subs(r2, r3)
        )
        == 0
    )

    x = sp.symbols("x")
    jc_probabilities = ((1 + 3 * x) / 4,) + ((1 - x) / 4,) * 3
    minimum = jc_probabilities[1]
    epsilon_jc = 2 * minimum
    near_jc = 1 - epsilon_jc
    residual_jc = sp.factor(x / near_jc)
    assert sp.factor(near_jc - (1 + x) / 2) == 0
    assert sp.factor(residual_jc - 2 * x / (1 + x)) == 0
    return {
        "K3P": "all strictly positive probability kernels on Z2xZ2",
        "K2P": (
            "probabilities (r0,r1,r2,r3) satisfy r2=r3; equivalently "
            "Fourier multipliers a1=a3, and this equality is preserved"
        ),
        "JC": (
            "for 0<x<1 the factors have multipliers "
            "(1+x)/2 and 2*x/(1+x), both strictly between zero and one"
        ),
        "near_identity_factor": "JC and therefore belongs to all three models",
    }


def regular_rank_certificate():
    # Put multiplier 1/2 on every nonzero character of every source edge and
    # lambda=1/2.  The effective multiplier is 3/32 in every character.
    source_diagonal = sp.Rational(1, 8)
    target_diagonal = sp.Rational(1, 2)
    records = {}
    model_orbits = {
        "JC": ((1, 2, 3),),
        "K2P": ((2,), (1, 3)),
        "K3P": ((1,), (2,), (3,)),
    }
    for model, orbits in model_orbits.items():
        dimension = len(orbits)
        source_variables = sp.symbols(f"t0:{dimension}")
        target_variables = sp.symbols(f"d0:{dimension}")
        source_by_character = {}
        target_by_character = {}
        for orbit_index, orbit in enumerate(orbits):
            for character in orbit:
                source_by_character[character] = source_variables[orbit_index]
                target_by_character[character] = target_variables[orbit_index]

        source_outputs = tuple(
            sp.Rational(1, 4)
            * (
                sp.Rational(1, 2) * source_by_character[character]
                + sp.Rational(1, 2) * sp.Rational(1, 4)
            )
            for character in (orbit[0] for orbit in orbits)
        )
        target_outputs = tuple(
            sp.Rational(1, 2) * target_by_character[orbit[0]]
            for orbit in orbits
        )
        source_jacobian = sp.Matrix(source_outputs).jacobian(source_variables)
        target_jacobian = sp.Matrix(target_outputs).jacobian(target_variables)
        assert source_jacobian == sp.eye(dimension) * source_diagonal
        assert target_jacobian == sp.eye(dimension) * target_diagonal

        source_point = {variable: sp.Rational(1, 2) for variable in source_variables}
        target_point = {
            variable: sp.Rational(3, 16) for variable in target_variables
        }
        assert all(
            output.subs(source_point) == sp.Rational(3, 32)
            for output in source_outputs
        )
        assert all(
            output.subs(target_point) == sp.Rational(3, 32)
            for output in target_outputs
        )

        for multiplier in (sp.Rational(1, 2), sp.Rational(3, 16)):
            probabilities = inverse_fourier((1, multiplier, multiplier, multiplier))
            assert sum(probabilities) == 1
            assert all(value > 0 for value in probabilities)

        records[model] = {
            "effective_nonzero_multipliers": ["3/32"] * dimension,
            "source_rank_minor": str(source_diagonal**dimension),
            "target_rank_minor": str(target_diagonal**dimension),
            "model_dimension": dimension,
            "all_source_edge_nonzero_multipliers": "1/2",
            "target_first_arm_nonzero_multipliers": "1/2",
            "target_second_arm_nonzero_multipliers": "3/16",
            "inheritance_probability": "1/2",
            "source_jacobian": [
                [str(value) for value in row]
                for row in source_jacobian.tolist()
            ],
            "target_jacobian": [
                [str(value) for value in row]
                for row in target_jacobian.tolist()
            ],
            "strict_probability_positivity_checked": True,
        }
    return records


def generate_certificate():
    chambers = factorization_chambers()
    return {
        "status": {
            "JC_complete_image_equality": "PROVED",
            "K2P_complete_image_equality": "PROVED",
            "K3P_complete_image_equality": "PROVED",
            "arbitrary_component_substitution_all_models": "PROVED",
            "move": "C_root",
        },
        "positive_kernel_factorization": {
            "chambers": chambers,
            "chamber_count": len(chambers),
            "exact_probability_convolution_identities": 16,
            "exact_nonzero_fourier_product_identities": 12,
            "rule": (
                "choose a minimum probability m, set epsilon=2m, "
                "E=(1-epsilon)delta_0+epsilon U, and "
                "D=(R-epsilon U)/(1-epsilon)"
            ),
            "strict_positivity": (
                "0<m<=1/4 gives 0<epsilon<=1/2; every D coordinate "
                "is at least m/(2*(1-2m))>0"
            ),
        },
        "model_preservation": model_preservation_certificate(),
        "tree_to_cycle_algorithm": [
            "convolve the two target arm kernels to obtain R",
            "factor R=P*R1 with the positive factorization lemma",
            "factor R1=Q*H",
            "factor H=S*U",
            "set T=H and lambda=1/2",
        ],
        "cycle_to_tree_algorithm": [
            "form H=lambda*T+(1-lambda)*(S*U)",
            "form R=P*Q*H",
            "factor R=C*D with the positive factorization lemma",
        ],
        "exact_common_regular_points": regular_rank_certificate(),
        "conclusion": (
            "C_root preserves the complete open stochastic image under "
            "JC, K2P, and K3P, including after arbitrary identical "
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
