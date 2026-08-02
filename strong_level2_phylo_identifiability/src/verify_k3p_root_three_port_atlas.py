#!/usr/bin/env python3
"""Exact K3P atlas for all reticulate three-port root blobs.

The verifier proves that the seven unlabelled R3 models split into one
irreducible quartic hypersurface class and one ambient-dominant class.  Exact
rational interval-Newton boxes isolate preimages of one common rational K2P
tensor.  Rank blocks are interval-certified at those same algebraic roots,
which proves both full-dimensional stochastic overlap inside each class and
one-sided generic containment from the hypersurface class into the ambient
class.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

from flint import fmpq, fmpq_mpoly_ctx
import sympy as sp

from enumerate_four_leaf_root_theta import canonical_code, semi_directed_triangle_count
from generic_fourier_network import precompute_displayed_trees
from r3_k3p_common_point_data import (
    BOX_RADIUS,
    CENTERS,
    FIXED,
    RANK_COLUMNS,
    RANK_ROWS,
)
from r3_k3p_quartic_terms import TERMS
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import canonical_mixed_graph
from verify_jc_omega_chain import zero_sum_assignments
from verify_jc_root_three_port_saturation import enumerate_unlabelled
from verify_k2p_root_three_port_saturation import (
    MINOR_COLUMNS,
    ORBIT_REPRESENTATIVES,
    k2p_parameterization,
)


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "k3p_root_three_port_atlas.json"

ASSIGNMENTS = tuple(zero_sum_assignments(3))
NONCONSTANT_ASSIGNMENTS = tuple(
    assignment for assignment in ASSIGNMENTS if assignment != (0, 0, 0)
)
HYPERSURFACE_RECORDS = (1, 2, 4)
AMBIENT_RECORDS = (3, 5, 6, 7)

DELTA = sp.Rational(1, 100)
PAIR_SINGLETON = sp.Rational(101, 100) * DELTA**2
PAIR_DOUBLET = DELTA**2
TRIPLE = sp.Rational(4, 5) * DELTA**3
COMMON_TARGET_REPS = (
    PAIR_SINGLETON,
    PAIR_DOUBLET,
    PAIR_SINGLETON,
    PAIR_SINGLETON,
    TRIPLE,
    PAIR_DOUBLET,
    TRIPLE,
    PAIR_DOUBLET,
    TRIPLE,
)

GENERIC_ROWS = {
    1: tuple(range(14)),
    2: tuple(range(14)),
    3: tuple(range(15)),
    4: tuple(range(14)),
    5: tuple(range(15)),
    6: tuple(range(15)),
    7: tuple(range(15)),
}
GENERIC_COLUMNS = {
    1: (0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16),
    2: (0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
    3: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20),
    4: (0, 1, 2, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25),
    5: (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 18, 19, 20),
    6: (0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 18),
    7: (0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17),
}
GENERIC_DETERMINANTS = {
    1: sp.Rational(57618379, 7298231506347656250000000000000000),
    2: -sp.Rational(17946887, 1824557876586914062500000000000000),
    3: -sp.Rational(
        253804860429186336949,
        76255974849870000000000000000000000000000000000000000000000000,
    ),
    4: sp.Rational(
        3687696921468417942498877,
        423644304721500000000000000000000000000000000000000000000,
    ),
    5: -sp.Rational(
        148115971073684136523,
        317733228541125000000000000000000000000000000000000000000000,
    ),
    6: sp.Rational(
        399094256701,
        813397065065280000000000000000000000000000000000000000,
    ),
    7: sp.Rational(
        1843988903624959,
        1029455660473245000000000000000000000000000000000000000000,
    ),
}
GENERIC_INVARIANT_VALUES = {
    1: sp.Rational(0),
    2: sp.Rational(0),
    3: sp.Rational(3301407761, 12597120000000000000000),
    4: sp.Rational(0),
    5: sp.Rational(37454327, 3149280000000000000),
    6: sp.Rational(63917011, 94478400000000000000),
    7: -sp.Rational(914207, 787320000000000000),
}


def k3p_parameterization(network, prefix):
    edges = tuple(network["edges"])
    reticulations, displayed_trees = precompute_displayed_trees(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], (1, 2, 3))),
    )
    parameters = []
    multipliers = []
    for edge_index in range(len(edges)):
        x, y, z = sp.symbols(f"{prefix}x{edge_index} {prefix}y{edge_index} {prefix}z{edge_index}")
        parameters.extend((x, y, z))
        multipliers.append((1, x, y, z))
    inheritances = sp.symbols(f"{prefix}l0:{len(reticulations)}")
    parameters.extend(inheritances)
    inheritance = dict(zip(reticulations, inheritances))

    outputs = {}
    for assignment in ASSIGNMENTS:
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


def quartic_expression(coordinates):
    return sp.expand(
        sum(
            coefficient * sp.prod(coordinates[assignment] for assignment in monomial)
            for coefficient, monomial in TERMS
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


def exact_quartic_pullback(outputs, parameters):
    context = fmpq_mpoly_ctx.get(tuple(map(str, parameters)), "degrevlex")
    needed = {assignment for _, monomial in TERMS for assignment in monomial}
    converted = {
        assignment: flint_polynomial(outputs[assignment], parameters, context)
        for assignment in needed
    }
    result = context.constant(0)
    for coefficient, monomial in TERMS:
        term = context.constant(coefficient)
        for assignment in monomial:
            term *= converted[assignment]
        result += term
    return result


def generic_positive_substitution(parameters, edge_count):
    triples = (
        (sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(2, 5)),
        (sp.Rational(2, 5), sp.Rational(1, 4), sp.Rational(1, 3)),
        (sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(1, 4)),
    )
    substitution = {}
    for edge_index in range(edge_count):
        for offset, value in enumerate(triples[edge_index % 3]):
            substitution[parameters[3 * edge_index + offset]] = value
    for index, parameter in enumerate(parameters[3 * edge_count:]):
        substitution[parameter] = sp.Rational(2 + index, 5 + index)
    return substitution


def k3p_transition_probabilities(x, y, z):
    return (
        (1 + x + y + z) / 4,
        (1 + x - y - z) / 4,
        (1 - x + y - z) / 4,
        (1 - x - y + z) / 4,
    )


def swap_k2p_characters(assignment):
    swap = {0: 0, 1: 1, 2: 3, 3: 2}
    return tuple(swap[value] for value in assignment)


def common_target():
    values = {(0, 0, 0): sp.Rational(1)}
    for assignment, value in zip(ORBIT_REPRESENTATIVES, COMMON_TARGET_REPS):
        values[assignment] = value
        values[swap_k2p_characters(assignment)] = value
    assert set(values) == set(ASSIGNMENTS)
    for leaf_permutation in permutations(range(3)):
        for assignment, value in values.items():
            permuted = tuple(assignment[index] for index in leaf_permutation)
            assert values[permuted] == value
    return values


@dataclass(frozen=True)
class Interval:
    lo: sp.Rational
    hi: sp.Rational

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, denominator):
        denominator = sp.Rational(denominator)
        assert denominator > 0
        return Interval(self.lo / denominator, self.hi / denominator)

    def __pow__(self, exponent):
        assert exponent >= 0
        result = Interval(sp.Rational(1), sp.Rational(1))
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def abs_upper(self):
        return max(abs(self.lo), abs(self.hi))


def as_interval(value):
    if isinstance(value, Interval):
        return value
    value = sp.Rational(value)
    return Interval(value, value)


def evaluate_poly(polynomial, boxes):
    result = as_interval(0)
    for monomial, coefficient in polynomial.terms():
        term = as_interval(coefficient)
        for box, exponent in zip(boxes, monomial):
            if exponent:
                term *= box**exponent
        result += term
    return result


def krawczyk_certificate(equations, variables, centers, radius):
    polynomials = tuple(sp.Poly(eq, *variables, domain=sp.QQ) for eq in equations)
    jacobian = [
        [polynomial.diff(variable) for variable in variables]
        for polynomial in polynomials
    ]
    center_substitution = dict(zip(variables, centers))
    function_center = sp.Matrix(
        [polynomial.eval(center_substitution) for polynomial in polynomials]
    )
    jacobian_center = sp.Matrix(
        [
            [entry.eval(center_substitution) for entry in row]
            for row in jacobian
        ]
    )
    inverse = jacobian_center.inv()
    newton_center = sp.Matrix(centers) - inverse * function_center
    boxes = tuple(Interval(center - radius, center + radius) for center in centers)
    jacobian_box = [
        [evaluate_poly(entry, boxes) for entry in row] for row in jacobian
    ]
    identity_error = []
    for row in range(len(variables)):
        local = []
        for column in range(len(variables)):
            value = as_interval(1 if row == column else 0)
            for inner in range(len(variables)):
                value -= inverse[row, inner] * jacobian_box[inner][column]
            local.append(value)
        identity_error.append(local)

    delta = Interval(-radius, radius)
    image = []
    for row in range(len(variables)):
        value = as_interval(newton_center[row])
        for column in range(len(variables)):
            value += identity_error[row][column] * delta
        image.append(value)
    margins = []
    for center, value in zip(centers, image):
        assert center - radius < value.lo < value.hi < center + radius
        margins.append(
            min(value.lo - (center - radius), (center + radius) - value.hi)
        )
    contraction = max(
        sum(entry.abs_upper() for entry in row) for row in identity_error
    )
    assert contraction < sp.Rational(1, 10**20)
    assert min(margins) > sp.Rational(9, 10**31)
    return boxes


def interval_invertibility_certificate(matrix, variables, boxes):
    polynomials = [
        [sp.Poly(entry, *variables, domain=sp.QQ) for entry in row]
        for row in matrix.tolist()
    ]
    centers = tuple((box.lo + box.hi) / 2 for box in boxes)
    center_substitution = dict(zip(variables, centers))
    center_matrix = sp.Matrix(
        [
            [entry.eval(center_substitution) for entry in row]
            for row in polynomials
        ]
    )
    inverse = center_matrix.inv()
    interval_matrix = [
        [evaluate_poly(entry, boxes) for entry in row] for row in polynomials
    ]
    error = []
    for row in range(matrix.rows):
        local = []
        for column in range(matrix.cols):
            value = as_interval(1 if row == column else 0)
            for inner in range(matrix.rows):
                value -= inverse[row, inner] * interval_matrix[inner][column]
            local.append(value)
        error.append(local)
    bound = max(sum(entry.abs_upper() for entry in row) for row in error)
    assert bound < sp.Rational(1, 10**20)


def common_point_record(index, record):
    network = record["network"]
    outputs, parameters = k2p_parameterization(network, f"n{index}_")
    columns = MINOR_COLUMNS[index]
    variables = tuple(parameters[column] for column in columns)
    parameter_lookup = {str(parameter): parameter for parameter in parameters}
    fixed = {
        parameter_lookup[name]: sp.Rational(value)
        for name, value in FIXED[index].items()
    }
    equations = tuple(
        sp.expand(outputs[assignment].subs(fixed) - target)
        for assignment, target in zip(ORBIT_REPRESENTATIVES, COMMON_TARGET_REPS)
    )
    centers = tuple(sp.Rational(value) for value in CENTERS[index])
    radius = sp.Rational(BOX_RADIUS)
    boxes = krawczyk_certificate(equations, variables, centers, radius)

    variable_boxes = dict(zip(variables, boxes))
    parameter_boxes = {
        parameter: variable_boxes.get(parameter, as_interval(value))
        for parameter, value in {
            **fixed,
            **{variable: centers[position] for position, variable in enumerate(variables)},
        }.items()
    }
    minimum_transition_lower = sp.Rational(1)
    for edge_index in range(len(network["edges"])):
        singleton = parameter_boxes[parameters[2 * edge_index]]
        doubleton = parameter_boxes[parameters[2 * edge_index + 1]]
        probabilities = (
            (1 + singleton + 2 * doubleton) / 4,
            (1 + singleton - 2 * doubleton) / 4,
            (1 - singleton) / 4,
            (1 - singleton) / 4,
        )
        minimum_transition_lower = min(
            minimum_transition_lower, *(probability.lo for probability in probabilities)
        )
    assert minimum_transition_lower > sp.Rational(1, 20)
    for parameter in parameters[2 * len(network["edges"]):]:
        assert parameter in fixed and 0 < fixed[parameter] < 1

    k3_outputs, k3_parameters = k3p_parameterization(network, f"k{index}_")
    k2_values = dict(fixed)
    k2_values.update({variable: variable for variable in variables})
    diagonal_substitution = {}
    for edge_index in range(len(network["edges"])):
        singleton = k2_values[parameters[2 * edge_index]]
        doubleton = k2_values[parameters[2 * edge_index + 1]]
        diagonal_substitution[k3_parameters[3 * edge_index]] = singleton
        diagonal_substitution[k3_parameters[3 * edge_index + 1]] = doubleton
        diagonal_substitution[k3_parameters[3 * edge_index + 2]] = doubleton
    k2_inheritances = parameters[2 * len(network["edges"]):]
    k3_inheritances = k3_parameters[3 * len(network["edges"]):]
    for source, target in zip(k2_inheritances, k3_inheritances):
        diagonal_substitution[target] = k2_values[source]

    full_jacobian = sp.Matrix(
        [k3_outputs[assignment] for assignment in NONCONSTANT_ASSIGNMENTS]
    ).jacobian(k3_parameters)
    selected = full_jacobian.extract(
        RANK_ROWS[index], RANK_COLUMNS[index]
    ).subs(diagonal_substitution)
    interval_invertibility_certificate(selected, variables, boxes)

    return {
        "id": index,
        "kind": record["kind"],
        "core_index": record.get("core_index"),
        "subdivision_counts": list(record.get("counts", ())),
        "class": "H14" if index in HYPERSURFACE_RECORDS else "A15",
        "isolated_variable_names": [str(variable) for variable in variables],
        "box_centers": list(CENTERS[index]),
        "common_box_radius": BOX_RADIUS,
        "fixed_parameters": dict(sorted(FIXED[index].items())),
        "Krawczyk_contraction_strict_upper_bound": "1/10^20",
        "Krawczyk_inclusion_margin_strict_lower_bound": "9/10^31",
        "K3P_rank_block_order": selected.rows,
        "K3P_rank_block_rows": list(RANK_ROWS[index]),
        "K3P_rank_block_columns": list(RANK_COLUMNS[index]),
        "rank_inverse_error_strict_upper_bound": "1/10^20",
        "transition_probability_strict_lower_bound": "1/20",
        "unique_real_algebraic_preimage_in_box": True,
    }


def topology_class_counts(records):
    result = {}
    for name, indices in (("H14", HYPERSURFACE_RECORDS), ("A15", AMBIENT_RECORDS)):
        rooted = set()
        semi_directed = set()
        one_triangle_semi_directed = set()
        for index in indices:
            network = records[index]["network"]
            triangle_count = semi_directed_triangle_count(
                network["vertices"], network["edges"]
            )
            for labels in permutations((1, 2, 3)):
                rooted.add(
                    canonical_code(
                        network["vertices"],
                        network["edges"],
                        dict(zip(network["leaves"], labels)),
                    )
                )
                code = canonical_mixed_graph(semi_directed_graph(network, labels))
                semi_directed.add(code)
                if triangle_count == 1:
                    one_triangle_semi_directed.add(code)
        result[name] = {
            "record_ids": list(indices),
            "rooted_topologies": len(rooted),
            "semi_directed_topologies": len(semi_directed),
            "one_triangle_semi_directed_topologies": len(one_triangle_semi_directed),
        }
    assert result["H14"] == {
        "record_ids": [1, 2, 4],
        "rooted_topologies": 15,
        "semi_directed_topologies": 9,
        "one_triangle_semi_directed_topologies": 3,
    }
    assert result["A15"] == {
        "record_ids": [3, 5, 6, 7],
        "rooted_topologies": 24,
        "semi_directed_topologies": 12,
        "one_triangle_semi_directed_topologies": 12,
    }
    return result


def generate_certificate():
    records = enumerate_unlabelled()
    assert Counter(record["kind"] for record in records) == {
        "tree": 1,
        "cycle": 2,
        "theta": 5,
    }

    coordinate_symbols = {
        assignment: sp.Symbol("q" + "".join(map(str, assignment)))
        for assignment in ASSIGNMENTS
    }
    invariant = quartic_expression(coordinate_symbols)
    assert sp.factor(invariant) == invariant
    swapped = invariant.xreplace(
        {
            coordinate_symbols[assignment]: coordinate_symbols[
                swap_k2p_characters(assignment)
            ]
            for assignment in ASSIGNMENTS
        }
    )
    assert sp.expand(swapped + invariant) == 0
    leaf_permutation_signs = {}
    for leaf_permutation in permutations(range(3)):
        permuted = invariant.xreplace(
            {
                coordinate_symbols[assignment]: coordinate_symbols[
                    tuple(assignment[index] for index in leaf_permutation)
                ]
                for assignment in ASSIGNMENTS
            }
        )
        if sp.expand(permuted - invariant) == 0:
            leaf_permutation_signs[leaf_permutation] = 1
        else:
            assert sp.expand(permuted + invariant) == 0
            leaf_permutation_signs[leaf_permutation] = -1

    target = common_target()
    target_substitution = {
        coordinate_symbols[assignment]: value for assignment, value in target.items()
    }
    assert invariant.subs(target_substitution) == 0
    target_gradient = {
        assignment: sp.factor(
            sp.diff(invariant, coordinate_symbols[assignment]).subs(target_substitution)
        )
        for assignment in ASSIGNMENTS
    }
    nonzero_gradient = {
        assignment: value for assignment, value in target_gradient.items() if value
    }
    assert nonzero_gradient[(1, 2, 3)] == -sp.Rational(37, 10**14)

    generic_records = []
    common_records = []
    for index, record in enumerate(records):
        if index == 0:
            continue
        network = record["network"]
        outputs, parameters = k3p_parameterization(network, f"g{index}_")
        jacobian = sp.Matrix(
            [outputs[assignment] for assignment in NONCONSTANT_ASSIGNMENTS]
        ).jacobian(parameters)
        substitution = generic_positive_substitution(parameters, len(network["edges"]))
        selected = jacobian.extract(
            GENERIC_ROWS[index], GENERIC_COLUMNS[index]
        ).subs(substitution)
        determinant = sp.factor(selected.det())
        assert determinant == GENERIC_DETERMINANTS[index]

        transition_probabilities = []
        for edge_index in range(len(network["edges"])):
            values = tuple(
                substitution[parameters[3 * edge_index + offset]]
                for offset in range(3)
            )
            transition_probabilities.extend(k3p_transition_probabilities(*values))
        assert min(transition_probabilities) == sp.Rational(31, 240)
        for parameter in parameters[3 * len(network["edges"]):]:
            assert 0 < substitution[parameter] < 1

        invariant_value = sp.factor(
            quartic_expression(outputs).subs(substitution)
        )
        assert invariant_value == GENERIC_INVARIANT_VALUES[index]
        if index in HYPERSURFACE_RECORDS:
            pullback = exact_quartic_pullback(outputs, parameters)
            assert pullback == 0
            pullback_terms = 0
        else:
            pullback_terms = "nonzero_by_rank_15_and_exact_witness"

        generic_records.append(
            {
                "id": index,
                "kind": record["kind"],
                "core_index": record.get("core_index"),
                "subdivision_counts": list(record.get("counts", ())),
                "class": "H14" if index in HYPERSURFACE_RECORDS else "A15",
                "generic_rank": len(GENERIC_ROWS[index]),
                "rank_witness_transition_probability_minimum": "31/240",
                "rank_minor_rows": list(GENERIC_ROWS[index]),
                "rank_minor_columns": list(GENERIC_COLUMNS[index]),
                "rank_minor": str(determinant),
                "quartic_pullback_terms": pullback_terms,
                "quartic_at_rank_witness": str(invariant_value),
                "vertices": dict(sorted(network["vertices"].items())),
                "edges": [list(edge) for edge in network["edges"]],
                "leaves": list(network["leaves"]),
                "rooted_code_sha256": sha256(
                    repr(canonical_code(network["vertices"], network["edges"])).encode()
                ).hexdigest(),
            }
        )
        common_records.append(common_point_record(index, record))

    class_counts = topology_class_counts(records)
    certificate = {
        "status": {
            "complete_reticulate_three_port_K3P_bowtie_atlas": "PROVED",
            "H14_pairwise_full_dimensional_regular_overlap": "PROVED",
            "A15_pairwise_full_dimensional_regular_overlap": "PROVED",
            "H14_one_sided_generically_contained_in_A15": "PROVED",
            "A15_one_sided_contained_in_H14": "PROVED ABSENT BY DIMENSION",
            "H14_A15_bowtie": "PROVED ABSENT BY UNEQUAL DIMENSION",
            "complete_open_stochastic_image_equalities": "UNRESOLVED",
            "ordinary_tree_relations": "UNRESOLVED IN THIS MILESTONE",
        },
        "model": "K3P",
        "normalized_three_leaf_ambient_dimension": 15,
        "quartic": {
            "terms": [
                {
                    "coefficient": coefficient,
                    "monomial": [list(assignment) for assignment in monomial],
                }
                for coefficient, monomial in TERMS
            ],
            "term_count": 8,
            "coefficient_set": [-1, 1],
            "irreducible_over_Q": True,
            "anti_invariant_under_K2P_character_swap": True,
            "alternating_under_leaf_permutations": {
                "".join(map(str, permutation)): sign
                for permutation, sign in leaf_permutation_signs.items()
            },
            "H14_pullback_zero_record_ids": list(HYPERSURFACE_RECORDS),
            "A15_nonzero_pullback_record_ids": list(AMBIENT_RECORDS),
        },
        "model_varieties": {
            "H14": "the irreducible quartic hypersurface V(I), dimension 14",
            "A15": "the complete normalized affine K3P tensor space, dimension 15",
        },
        "class_counts": class_counts,
        "generic_rank_certificates": generic_records,
        "common_target": {
            "normal_coordinate": "1",
            "singleton_pair_coordinates": str(PAIR_SINGLETON),
            "doubleton_pair_coordinates": str(PAIR_DOUBLET),
            "all_distinct_triple_coordinates": str(TRIPLE),
            "all_16_coordinates": {
                "".join(map(str, assignment)): str(value)
                for assignment, value in sorted(target.items())
            },
            "leaf_permutation_invariant": True,
            "quartic_value": "0",
            "nonzero_quartic_gradient_entry_dI_dq123": str(
                nonzero_gradient[(1, 2, 3)]
            ),
        },
        "common_exact_algebraic_preimages": {
            "method": (
                "exact rational Krawczyk inclusion; each box contains one "
                "unique real algebraic solution of the nine K2P output equations"
            ),
            "all_parameters_on_K2P_diagonal_inside_K3P": True,
            "records": common_records,
        },
        "observational_relations": {
            "within_H14": "bowtie_K3P",
            "within_A15": "bowtie_K3P",
            "H14_to_A15": "preceq_K3P",
            "A15_to_H14": "no one-sided generic containment",
            "simultaneous_seven_model_intersection_local_dimension": 14,
        },
        "conclusion": (
            "K3P refines the JC/K2P R3 collapse into exactly two reticulate "
            "bowtie classes, of dimensions 14 and 15. Every H14 model is "
            "one-sided generically contained in every A15 model at the same "
            "strict regular algebraic distribution."
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
                "class_counts": certificate["class_counts"],
                "deterministic_sha256": certificate["deterministic_sha256"],
                "model_varieties": certificate["model_varieties"],
                "observational_relations": certificate["observational_relations"],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
