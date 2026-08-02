#!/usr/bin/env python3
"""Exact K2P/K3P separation certificates for the Omega root reversal.

The source has port labels (1,2,3,4) at (P1,P2,Q,X); the target has
(2,1,4,3).  Thus this is the four-port member Omega_2 of Omega_chain.
All polynomial arithmetic and all stochastic witness checks are exact.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import sympy as sp
from flint import fmpq, fmpq_mat, fmpq_mpoly_ctx

from generic_fourier_network import precompute_displayed_trees
from omega_k2p_quintic_terms import TERMS as K2P_TERMS
from omega_k3p_sextic_terms import TERMS as K3P_TERMS
from verify_jc_omega_chain import omega_network, zero_sum_assignments


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "omega_model_hierarchy.json"

SOURCE_EDGE_POINT = (
    sp.Rational(1, 2), sp.Rational(1, 4),
    sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(1, 20),
    sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(1, 10), sp.Rational(1, 2),
)
TARGET_EDGE_POINT = (
    sp.Rational(7, 12), sp.Rational(1, 7),
    sp.Rational(1, 2), sp.Rational(41, 48),
    sp.Rational(28, 41), sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(12, 205),
    sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(3, 40), sp.Rational(1, 2),
)

TANGENT_MINOR_CERTIFICATES = {
    "K2P": {
        "source": (
            (1,2,4,5,6,8,9,10,11,16,17,18,20,22,24,25,32,33),
            (0,1,2,3,4,5,6,7,8,9,14,15,16,17,18,19,20,21),
            "-1640457/1088903574147003083082798743781658276659200000000000000",
        ),
        "target": (
            (1,2,4,5,6,8,9,10,11,16,17,18,20,22,24,25,32,33),
            (0,1,2,3,4,5,6,7,8,9,14,15,16,17,18,19,20,21),
            "-238739319/714320744640434022502315975920767829488435200000000000000",
        ),
        "combined": (
            (1,2,4,5,6,8,9,10,11,16,17,18,20,22,24,25,26,32,33),
            (0,1,2,3,4,5,6,7,8,9,14,15,16,17,18,19,20,21,26),
            "3916107/228582638284938887200741112294645705436299264000000000000000",
        ),
    },
    "K3P": {
        "source": (
            (1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,22,23,24,25,26,32,33,48),
            (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,26,27,28,29,30,31,32),
            "-669849209757/26328072917139296674479506920917608079723773850137277813577744384000000000000000000000",
        ),
        "target": (
            (1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,22,23,24,25,26,32,33,48),
            (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,26,27,28,29,30,31,32),
            "-946805259741003/88514981147422315419600102268124998364031327684161528009248376619008000000000000000000000",
        ),
        "combined": (
            (1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,22,23,24,25,26,27,28,32,33,48),
            (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,26,27,28,29,30,31,32,38,39),
            "-2842117551/141623969835875704671360163628999997382450124294658444814797402590412800000000000000000000000",
        ),
    },
}


def parameterization(model, labels, prefix):
    network = omega_network(2)
    edges = network["edges"]
    reticulations, displayed_trees = precompute_displayed_trees(
        network["vertices"], edges, dict(zip(network["leaves"], labels))
    )
    parameters = []
    multipliers = []
    for edge_index in range(len(edges)):
        if model == "K2P":
            singleton, doubleton = sp.symbols(
                f"{prefix}s{edge_index} {prefix}t{edge_index}"
            )
            parameters.extend((singleton, doubleton))
            multipliers.append((1, singleton, doubleton, doubleton))
        elif model == "K3P":
            x, y, z = sp.symbols(
                f"{prefix}x{edge_index} {prefix}y{edge_index} {prefix}z{edge_index}"
            )
            parameters.extend((x, y, z))
            multipliers.append((1, x, y, z))
        else:
            raise ValueError(model)
    inheritances = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    parameters.extend(inheritances)
    inheritance = dict(zip(reticulations, inheritances))

    outputs = {}
    for assignment in zero_sum_assignments(4):
        by_leaf = {index + 1: character for index, character in enumerate(assignment)}
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


def invariant_value(outputs, terms):
    return sp.factor(
        sum(
            coefficient * sp.prod(outputs[assignment] for assignment in monomial)
            for coefficient, monomial in terms
        )
    )


def flint_polynomial(expression, parameters, context):
    polynomial = sp.Poly(sp.expand(expression), *parameters)
    return context.from_dict(
        {
            monomial: fmpq(int(coefficient.p), int(coefficient.q))
            for monomial, coefficient in polynomial.terms()
        }
    )


def exact_pullback(outputs, parameters, terms):
    context = fmpq_mpoly_ctx.get(tuple(map(str, parameters)), "degrevlex")
    needed = {assignment for _, monomial in terms for assignment in monomial}
    converted = {
        assignment: flint_polynomial(outputs[assignment], parameters, context)
        for assignment in needed
    }
    result = context.constant(0)
    for coefficient, monomial in terms:
        term = context.constant(coefficient)
        for assignment in monomial:
            term *= converted[assignment]
        result += term
    return result


def character_class(model, character):
    if character == 0:
        return None
    if model == "K2P":
        return 0 if character == 1 else 1
    return character - 1


def invariant_multidegree(model, terms):
    classes = 2 if model == "K2P" else 3
    degrees = set()
    for _, monomial in terms:
        degree = [0] * (4 * classes)
        for assignment in monomial:
            for leaf, character in enumerate(assignment):
                cls = character_class(model, character)
                if cls is not None:
                    degree[leaf * classes + cls] += 1
        degrees.add(tuple(degree))
    assert len(degrees) == 1
    return next(iter(degrees))


def witness_substitution(model, parameters):
    if model == "K2P":
        substitution = {parameter: sp.Rational(1, 2) for parameter in parameters}
        substitution[parameters[0]] = sp.Rational(1, 3)
    else:
        substitution = {parameter: sp.Rational(1, 3) for parameter in parameters}
        substitution[parameters[0]] = sp.Rational(1, 4)
        substitution[parameters[3]] = sp.Rational(2, 5)
        substitution[parameters[-2]] = sp.Rational(1, 2)
        substitution[parameters[-1]] = sp.Rational(1, 2)
    return substitution


def transition_probabilities(model, edge_values):
    if model == "K2P":
        singleton, doubleton = edge_values
        return (
            (1 + singleton + 2 * doubleton) / 4,
            (1 + singleton - 2 * doubleton) / 4,
            (1 - singleton) / 4,
            (1 - singleton) / 4,
        )
    x, y, z = edge_values
    return (
        (1 + x + y + z) / 4,
        (1 + x - y - z) / 4,
        (1 - x + y - z) / 4,
        (1 - x - y + z) / 4,
    )


def verify_positive_witness(model, outputs, parameters, terms):
    width = 2 if model == "K2P" else 3
    substitution = witness_substitution(model, parameters)
    probabilities = []
    for edge_index in range(12):
        values = tuple(
            substitution[parameters[width * edge_index + offset]]
            for offset in range(width)
        )
        edge_probabilities = transition_probabilities(model, values)
        assert all(value > 0 for value in edge_probabilities)
        probabilities.extend(edge_probabilities)
    assert 0 < substitution[parameters[-2]] < 1
    assert 0 < substitution[parameters[-1]] < 1
    specialized = {
        assignment: sp.cancel(expression.subs(substitution))
        for _, monomial in terms
        for assignment in monomial
        for expression in (outputs[assignment],)
    }
    value = invariant_value(specialized, terms)
    expected = {
        "K2P": sp.Rational(1, 824633720832),
        "K3P": sp.Rational(1, 60037854118799648400),
    }[model]
    assert value == expected
    return {
        "invariant_value": str(value),
        "minimum_transition_probability": str(min(probabilities)),
        "inheritances": [
            str(substitution[parameters[-2]]),
            str(substitution[parameters[-1]]),
        ],
    }


def rational_to_fmpq(value):
    value = sp.cancel(value)
    return fmpq(int(value.p), int(value.q))


def exact_tangent_minors(model):
    width = 2 if model == "K2P" else 3
    source, source_parameters = parameterization(model, (1, 2, 3, 4), f"{model}a")
    target, target_parameters = parameterization(model, (2, 1, 4, 3), f"{model}b")
    source_substitution = {
        parameter: value
        for edge_index, value in enumerate(SOURCE_EDGE_POINT)
        for parameter in source_parameters[width * edge_index : width * edge_index + width]
    }
    target_substitution = {
        parameter: value
        for edge_index, value in enumerate(TARGET_EDGE_POINT)
        for parameter in target_parameters[width * edge_index : width * edge_index + width]
    }
    for parameter in source_parameters[width * 12 :]:
        source_substitution[parameter] = sp.Rational(1, 2)
    for parameter in target_parameters[width * 12 :]:
        target_substitution[parameter] = sp.Rational(1, 2)
    assignments = tuple(source)
    result = {}
    for name, (row_indices, column_indices, expected) in TANGENT_MINOR_CERTIFICATES[model].items():
        entries = []
        for row_index in row_indices:
            row = []
            for column_index in column_indices:
                if name == "source":
                    expression = source[assignments[row_index]]
                    parameter = source_parameters[column_index]
                    substitution = source_substitution
                elif name == "target":
                    expression = target[assignments[row_index]]
                    parameter = target_parameters[column_index]
                    substitution = target_substitution
                elif column_index < len(source_parameters):
                    expression = source[assignments[row_index]]
                    parameter = source_parameters[column_index]
                    substitution = source_substitution
                else:
                    expression = target[assignments[row_index]]
                    parameter = target_parameters[column_index - len(source_parameters)]
                    substitution = target_substitution
                row.append(
                    rational_to_fmpq(sp.diff(expression, parameter).subs(substitution))
                )
            entries.append(row)
        determinant = fmpq_mat(entries).det()
        assert str(determinant) == expected
        result[name] = {
            "order": len(row_indices),
            "row_assignments": [list(assignments[index]) for index in row_indices],
            "parameter_columns": list(column_indices),
            "determinant": str(determinant),
        }
    return result


def verify_model(model, terms, expected_degree):
    source, source_parameters = parameterization(model, (1, 2, 3, 4), f"{model}S")
    target, target_parameters = parameterization(model, (2, 1, 4, 3), f"{model}T")
    assert invariant_multidegree(model, terms) == expected_degree
    source_pullback = exact_pullback(source, source_parameters, terms)
    assert source_pullback == 0
    target_pullback = exact_pullback(target, target_parameters, terms)
    assert target_pullback != 0
    factor_constant, factors = target_pullback.factor()
    reconstructed = target_pullback.context().constant(factor_constant)
    for factor, exponent in factors:
        reconstructed *= factor**exponent
    assert reconstructed == target_pullback
    factor_strings = [(str(factor), exponent) for factor, exponent in factors]
    factor_digest = sha256(repr(factor_strings).encode()).hexdigest()
    return {
        "coordinate_degree": len(terms[0][1]),
        "term_count": len(terms),
        "invariant_terms": [
            {
                "coefficient": coefficient,
                "factors": [list(assignment) for assignment in monomial],
            }
            for coefficient, monomial in terms
        ],
        "coefficient_set": sorted({coefficient for coefficient, _ in terms}),
        "multidegree": list(expected_degree),
        "source_pullback": "0",
        "target_pullback_term_count": sum(1 for _ in target_pullback.terms()),
        "target_factor_constant": str(factor_constant),
        "target_factorization": factor_strings,
        "target_factorization_sha256": factor_digest,
        "positive_target_witness": verify_positive_witness(
            model, target, target_parameters, terms
        ),
        "JC_common_point_nonzero_tangent_minors": exact_tangent_minors(model),
    }


def main():
    k2p = verify_model(
        "K2P", K2P_TERMS,
        (1, 3, 2, 2, 1, 2, 1, 1),
    )
    k3p = verify_model(
        "K3P", K3P_TERMS,
        (2, 1, 2, 2, 2, 0, 2, 1, 1, 1, 1, 0),
    )
    certificate = {
        "status": {
            "K2P_Omega_separation": "PROVED",
            "K3P_Omega_separation": "PROVED",
            "Omega_chain_all_k_propagation": "PROVED",
        },
        "scope": (
            "Omega_2 has source port order P1,P2,Q,X and target order "
            "P2,P1,X,Q; every Omega_chain k>=2 contains this endpoint marginal"
        ),
        "K2P": k2p,
        "K3P": k3p,
        "all_k_marginal_argument": {
            "selected_ports": ["P1", "Pk", "Q", "X"],
            "suppressed_path_multiplier": (
                "the character-h multiplier is the product of the edge "
                "multipliers on the marginalized degree-two path"
            ),
            "nonzero_pullback": (
                "specializing unused path multipliers to 1 recovers the "
                "certified Omega_2 pullback, so the all-k pullback is not "
                "the zero polynomial"
            ),
        },
        "conclusion": (
            "The JC ambiguity Omega_chain is generically separated under both "
            "K2P and K3P. Equal-dimensional irreducible model closures are "
            "distinct, hence their stochastic intersection cannot contain a "
            "full-dimensional regular neighborhood."
        ),
    }
    CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
