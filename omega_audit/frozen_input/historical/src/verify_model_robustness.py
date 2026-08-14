"""Independent exact verifier for the JC/K2P/K3P theta hierarchy.

Every equality is checked by exact rational or polynomial arithmetic.  The
script performs no floating-point comparisons.
"""

from __future__ import annotations

import json

import sympy as sp

from fourier_models import (
    EDGE_NAMES,
    inverse_fourier_transition_probabilities,
    source_parameterization,
    target_parameterization,
)
from model_robustness_invariants import (
    K2P_THETA_SOURCE_INVARIANT,
    K3P_THETA_SOURCE_INVARIANT,
    evaluate_invariant,
)


ORBIT_ASSIGNMENTS = (
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)

EXPECTED_ORBITS = (
    sp.Rational(277, 8000),
    sp.Rational(3, 40),
    sp.Rational(67, 2400),
    sp.Rational(127, 16000),
    sp.Rational(27, 5000),
    sp.Rational(81, 5000),
    sp.Rational(153, 160000),
    sp.Rational(9, 500),
    sp.Rational(27, 16000),
    sp.Rational(261, 320000),
    sp.Rational(27, 10000),
    sp.Rational(27, 20000),
    sp.Rational(153, 320000),
    sp.Rational(183, 80000),
)


def by_name(parameters):
    return {str(parameter): parameter for parameter in parameters}


def inherited_source_substitution(parameters):
    values = {
        "x_rA": sp.Rational(2, 3),
        "x_rC": sp.Rational(3, 4),
        "x_AB": sp.Rational(3, 5),
        "x_BC": sp.Rational(1, 2),
        "x_CD": sp.Rational(9, 20),
        "x_DE": sp.Rational(2, 5),
        "x_AF": sp.Rational(1, 2),
        "x_EF": sp.Rational(1, 3),
        "x_pB": sp.Rational(1, 5),
        "x_pD": sp.Rational(1, 2),
        "x_pF": sp.Rational(1, 2),
        "x_pE": sp.Rational(3, 8),
        "lambda_C": sp.Rational(1, 2),
        "lambda_F": sp.Rational(1, 2),
    }
    names = by_name(parameters)
    return {names[name]: value for name, value in values.items()}


def inherited_target_substitution(parameters, beta):
    values = {
        "x_rA": sp.Rational(2, 3),
        "x_rC": sp.Rational(3, 4),
        "x_AB": 24835 * beta / (20678 - 24835 * beta),
        "x_BC": sp.Rational(1, 2),
        "x_CD": sp.Rational(9934, 12215),
        "x_DE": sp.Rational(171, 775),
        "x_AF": sp.Rational(10339, 53010) / beta,
        "x_EF": sp.Rational(1, 2),
        "x_pB": sp.Rational(3, 20) / beta,
        "x_pD": sp.Rational(1, 2),
        "x_pF": sp.Rational(1767, 4832),
        "x_pE": sp.Rational(31, 190),
        "lambda_C": sp.Rational(1, 2),
        "lambda_F": sp.Rational(1, 2),
    }
    names = by_name(parameters)
    return {names[name]: value for name, value in values.items()}


def numerator_remainder(expression, beta, polynomial):
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    remainder = sp.rem(sp.Poly(numerator, beta), sp.Poly(polynomial, beta)).as_expr()
    return sp.factor(remainder), sp.factor(denominator)


def verify_jc_replay():
    source, source_parameters = source_parameterization("JC", "")
    target, target_parameters = target_parameterization("JC", "")
    source_sub = inherited_source_substitution(source_parameters)

    actual_orbits = tuple(sp.factor(source[g].subs(source_sub)) for g in ORBIT_ASSIGNMENTS)
    assert actual_orbits == EXPECTED_ORBITS

    beta = sp.Symbol("beta")
    minimal_polynomial = 43337075 * beta**2 - 36083110 * beta + 7336259
    target_sub = inherited_target_substitution(target_parameters, beta)
    for assignment in source:
        difference = source[assignment].subs(source_sub) - target[assignment].subs(target_sub)
        remainder, denominator = numerator_remainder(difference, beta, minimal_polynomial)
        assert remainder == 0
        assert denominator != 0

    lower = sp.Rational(441, 1250)
    upper = sp.Rational(3529, 10000)
    polynomial = sp.Poly(minimal_polynomial, beta)
    assert polynomial.count_roots(lower, upper) == 1
    assert polynomial.eval(lower) * polynomial.eval(upper) < 0
    assert sp.discriminant(polynomial) > 0

    # Interval proofs for every beta-dependent target multiplier.
    assert 0 < lower < upper < 1
    assert sp.Rational(10339, 53010) / lower < 1
    assert 2 * 24835 * upper < 20678  # implies 0 < z(beta) < 1
    assert sp.Rational(3, 20) / lower < 1
    for value in target_sub.values():
        if beta not in value.free_symbols:
            assert 0 < value < 1

    return {
        "orbit_coordinates": [str(value) for value in actual_orbits],
        "all_fourier_coordinates_equal_mod_minpoly": 64,
        "beta_minimal_polynomial": str(minimal_polynomial),
        "beta_isolating_interval": [str(lower), str(upper)],
    }


def rational_witness(model, parameters):
    result = {}
    for parameter in parameters:
        name = str(parameter)
        if name == "lambda_C" or name == "lambda_F":
            result[parameter] = sp.Rational(1, 2)
            continue
        edge = name.rsplit("_", 1)[-1]
        edge_index = EDGE_NAMES.index(edge)
        if model == "K2P":
            if name.startswith("s_"):
                result[parameter] = sp.Rational(2, 5) + sp.Rational(edge_index % 5, 100)
            else:
                result[parameter] = sp.Rational(1, 3) + sp.Rational(edge_index % 7, 120)
        elif model == "K3P":
            if name.startswith("x1_"):
                result[parameter] = sp.Rational(1, 2) + sp.Rational(edge_index % 5, 100)
            elif name.startswith("x2_"):
                result[parameter] = sp.Rational(2, 5) + sp.Rational(edge_index % 7, 120)
            else:
                result[parameter] = sp.Rational(1, 3) + sp.Rational(edge_index % 11, 150)
        else:
            raise ValueError(model)
    return result


def verify_transition_positivity(model, parameters, substitution):
    minima = []
    names = by_name(parameters)
    for edge in EDGE_NAMES:
        if model == "K2P":
            multiplier = (
                sp.Integer(1),
                substitution[names[f"s_{edge}"]],
                substitution[names[f"t_{edge}"]],
                substitution[names[f"t_{edge}"]],
            )
        else:
            multiplier = (
                sp.Integer(1),
                substitution[names[f"x1_{edge}"]],
                substitution[names[f"x2_{edge}"]],
                substitution[names[f"x3_{edge}"]],
            )
        probabilities = inverse_fourier_transition_probabilities(multiplier)
        assert all(probability > 0 for probability in probabilities)
        minima.extend(probabilities)
    return min(minima)


def verify_leaf_swap(model, source, target):
    for assignment in source:
        swapped = (assignment[3], assignment[1], assignment[2], assignment[0])
        assert sp.factor(target[assignment] - source[swapped]) == 0


def verify_separating_invariant(model, terms):
    source, source_parameters = source_parameterization(model, "")
    target, target_parameters = target_parameterization(model, "")
    verify_leaf_swap(model, source, target)

    source_pullback = evaluate_invariant(source, terms)
    assert source_pullback == 0
    target_pullback = evaluate_invariant(target, terms)
    assert target_pullback != 0

    witness = rational_witness(model, target_parameters)
    witness_value = sp.factor(target_pullback.subs(witness))
    assert witness_value != 0
    minimum_transition_probability = verify_transition_positivity(
        model, target_parameters, witness
    )
    assert witness[target_parameters[-2]] == sp.Rational(1, 2)
    assert witness[target_parameters[-1]] == sp.Rational(1, 2)

    return {
        "source_pullback": "0",
        "target_pullback_nonzero_witness": str(witness_value),
        "minimum_target_transition_probability": str(minimum_transition_probability),
        "leaf_swap_identity_count": 64,
    }


def main():
    certificate = {
        "status": "EXACTLY COMPUTED",
        "JC_replay": verify_jc_replay(),
        "K2P_separation": verify_separating_invariant(
            "K2P", K2P_THETA_SOURCE_INVARIANT
        ),
        "K3P_separation": verify_separating_invariant(
            "K3P", K3P_THETA_SOURCE_INVARIANT
        ),
    }
    print(json.dumps(certificate, indent=2, sort_keys=True))
    print("PASS: exact JC replay and exact K2P/K3P separation certificates")


if __name__ == "__main__":
    main()
