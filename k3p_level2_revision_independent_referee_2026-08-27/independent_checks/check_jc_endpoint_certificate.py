#!/usr/bin/env python3
"""Independent exact replay of the corrected JC endpoint certificate.

The checker reads only the corrected JSON certificate.  It imports no package
producer, verifier, graph compiler, or prior referee module.  From each raw
switching-signature row it independently expands the JC inheritance mixture
as a sparse rational polynomial, removes the stored central incidence class,
reconstructs a,b,c,t and Delta/Gamma, and proves the claimed strict sign or
exact zero case.  It also rebuilds the two-active matrices and identities.

Independence boundary: this file does not regenerate the primitive graph
classification or completion grammar, and it does not perform the separately
claimed 808,642-case unreduced binary-word census.  It treats the 77 supplied
signature records as the finite input whose endpoint algebra is being checked.
Stored factor strings and Bernstein min/max/count summaries are deliberately
not replayed: their claimed sign is rederived from the reconstructed target.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys

import sympy as sp


if not __debug__ or sys.flags.optimize:
    raise RuntimeError("run without -O/-OO so every fail-closed check remains active")


EXPECTED_CASES = {
    "Delta_positive": 67,
    "Delta_zero_Gamma_positive": 2,
    "Delta_zero_Gamma_zero": 7,
    "Delta_zero_Gamma_zero_ordinary": 1,
}
THREE_COORDINATES = {
    "a": (1, 1, 0),
    "b": (1, 0, 1),
    "c": (0, 1, 1),
    "t": (1, 2, 3),
}
GROUP = (0, 1, 2, 3)


class CheckFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def locate_proof_root(package_root):
    relative = Path("cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json")
    for candidate in (package_root / "proof_package", package_root):
        if (candidate / relative).is_file():
            return candidate
    raise FileNotFoundError("could not locate proof_package beneath --package-root")


def clean(polynomial):
    return {power: coefficient for power, coefficient in polynomial.items() if coefficient}


def constant(width, value=1):
    coefficient = Q(value)
    return {} if coefficient == 0 else {(0,) * width: coefficient}


def variable(width, index):
    power = [0] * width
    power[index] = 1
    return {tuple(power): Q(1)}


def add(left, right):
    answer = defaultdict(Q)
    for power, coefficient in left.items():
        answer[power] += coefficient
    for power, coefficient in right.items():
        answer[power] += coefficient
    return clean(answer)


def scale(polynomial, multiplier):
    multiplier = Q(multiplier)
    return clean({power: multiplier * coefficient for power, coefficient in polynomial.items()})


def multiply(left, right):
    answer = defaultdict(Q)
    for left_power, left_coefficient in left.items():
        for right_power, right_coefficient in right.items():
            answer[tuple(a + b for a, b in zip(left_power, right_power))] += (
                left_coefficient * right_coefficient
            )
    return clean(answer)


def substitute_one(polynomial, variable_index):
    answer = defaultdict(Q)
    for power, coefficient in polynomial.items():
        changed = list(power)
        changed[variable_index] = 0
        answer[tuple(changed)] += coefficient
    return clean(answer)


def sparse_payload(polynomial):
    return [
        {
            "power": list(power),
            "numerator": coefficient.numerator,
            "denominator": coefficient.denominator,
        }
        for power, coefficient in sorted(polynomial.items())
    ]


def sparse_digest(polynomial):
    payload = json.dumps(sparse_payload(polynomial), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def sparse_expression(polynomial, symbols):
    expression = sp.Integer(0)
    for power, coefficient in polynomial.items():
        term = sp.Rational(coefficient.numerator, coefficient.denominator)
        for symbol, exponent in zip(symbols, power):
            if exponent:
                term *= symbol ** exponent
        expression += term
    return sp.expand(expression)


def selected_character(mask, assignment):
    character = 0
    for position, value in enumerate(assignment):
        if mask & (1 << position):
            character ^= value
    return character


def inheritance_weight(choice, edge_count):
    width = edge_count + len(choice)
    answer = constant(width)
    for index, bit in enumerate(choice):
        inheritance = variable(width, edge_count + index)
        factor = inheritance if bit == 0 else add(constant(width), scale(inheritance, -1))
        answer = multiply(answer, factor)
    return answer


def jc_coordinate(signatures, reticulation_count, assignment):
    require(len(assignment) == 3 and assignment[0] ^ assignment[1] ^ assignment[2] == 0,
            ("invalid three-port assignment", assignment))
    edge_count = len(signatures)
    width = edge_count + reticulation_count
    answer = {}
    choices = tuple(product((0, 1), repeat=reticulation_count))
    for switch_index, choice in enumerate(choices):
        term = inheritance_weight(choice, edge_count)
        edge_power = [0] * width
        for edge_index, signature in enumerate(signatures):
            if selected_character(signature[switch_index], assignment):
                edge_power[edge_index] = 1
        term = multiply(term, {tuple(edge_power): Q(1)})
        answer = add(answer, term)
    return answer


def rational(value):
    value = sp.Rational(value)
    return Q(int(value.p), int(value.q))


def bernstein_sign(expression, symbols):
    """Return a strict open-cube sign from the full Bernstein coefficients."""

    require(set(expression.free_symbols) <= set(symbols),
            ("unexpected symbols in Bernstein input", expression.free_symbols, symbols))
    active = tuple(symbol for symbol in symbols if sp.degree(expression, symbol) > 0)
    if not active:
        value = rational(expression)
        direction = 1 if value > 0 else -1 if value < 0 else 0
        return direction, {
            "coefficient_count": 1,
            "minimum": str(value),
            "maximum": str(value),
        }

    polynomial = sp.Poly(expression, *active, domain=sp.QQ)
    degrees = tuple(int(polynomial.degree(symbol)) for symbol in active)
    power_coefficients = {power: rational(coefficient) for power, coefficient in polynomial.terms()}
    values = []
    for beta in product(*(range(degree + 1) for degree in degrees)):
        value = Q(0)
        for alpha, coefficient in power_coefficients.items():
            if any(left > right for left, right in zip(alpha, beta)):
                continue
            multiplier = Q(1)
            for left, right, degree in zip(alpha, beta, degrees):
                multiplier *= Q(comb(right, left), comb(degree, left))
            value += coefficient * multiplier
        values.append(value)

    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        direction = 1
    elif all(value <= 0 for value in values) and any(value < 0 for value in values):
        direction = -1
    elif not any(values):
        direction = 0
    else:
        direction = None
    return direction, {
        "active_variables": [str(symbol) for symbol in active],
        "degrees": list(degrees),
        "coefficient_count": len(values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
    }


def factor_strict_sign(expression, symbols):
    """Prove every irreducible factor nonzero on the open cube, then combine signs."""

    if sp.expand(expression) == 0:
        return 0, {"method": "exact_zero"}
    coefficient, factors = sp.factor_list(sp.expand(expression), *symbols)
    coefficient = rational(coefficient)
    direction = 1 if coefficient > 0 else -1
    rows = []
    for factor, exponent in factors:
        factor_direction, detail = bernstein_sign(factor, symbols)
        if factor_direction not in (-1, 1):
            return None, {
                "method": "factor_bernstein",
                "failed_factor": str(factor),
                "exponent": int(exponent),
                "factor_bernstein": detail,
            }
        if exponent % 2:
            direction *= factor_direction
        rows.append({
            "factor": str(factor),
            "exponent": int(exponent),
            "sign": factor_direction,
            "bernstein": detail,
        })
    return direction, {
        "method": "factor_bernstein",
        "constant": str(coefficient),
        "factor_count": len(rows),
        "factors": rows,
    }


def nonnegative_factor_expression(expression, symbols):
    """Certify nonnegativity; also report whether positivity is uniform inside."""

    if sp.expand(expression) == 0:
        return True, False, {"zero": True}
    coefficient, factors = sp.factor_list(sp.expand(expression), *symbols)
    coefficient = rational(coefficient)
    direction = 1 if coefficient > 0 else -1
    strict = True
    rows = []
    for factor, exponent in factors:
        factor_direction, detail = bernstein_sign(factor, symbols)
        if exponent % 2:
            if factor_direction not in (-1, 1):
                return False, False, {
                    "failed_odd_factor": str(factor),
                    "exponent": int(exponent),
                    "factor_bernstein": detail,
                }
            direction *= factor_direction
        elif factor_direction not in (-1, 1):
            # The even power remains nonnegative, but may vanish in the interior.
            strict = False
        rows.append({
            "factor": str(factor),
            "exponent": int(exponent),
            "sign": factor_direction,
        })
    return direction == 1, strict and direction == 1, {
        "constant": str(coefficient),
        "factor_count": len(rows),
        "factors": rows,
    }


def inheritance_bernstein_positive(expression, all_symbols, inheritance_symbols):
    """Use Bernstein in inheritance variables with factored edge-polynomial coefficients."""

    if not inheritance_symbols:
        return False, {"method": "inheritance_bernstein", "reason": "no inheritance variables"}
    polynomial = sp.Poly(sp.expand(expression), *all_symbols, domain=sp.QQ)
    inheritance_positions = tuple(all_symbols.index(symbol) for symbol in inheritance_symbols)
    edge_symbols = tuple(symbol for symbol in all_symbols if symbol not in inheritance_symbols)
    edge_positions = tuple(all_symbols.index(symbol) for symbol in edge_symbols)
    degrees = tuple(int(polynomial.degree(symbol)) for symbol in inheritance_symbols)
    coefficient_rows = []
    strict_count = 0

    for beta in product(*(range(degree + 1) for degree in degrees)):
        residual = defaultdict(Q)
        for monomial, coefficient in polynomial.terms():
            alpha = tuple(monomial[position] for position in inheritance_positions)
            if any(left > right for left, right in zip(alpha, beta)):
                continue
            multiplier = Q(1)
            for left, right, degree in zip(alpha, beta, degrees):
                multiplier *= Q(comb(right, left), comb(degree, left))
            edge_power = tuple(monomial[position] for position in edge_positions)
            residual[edge_power] += rational(coefficient) * multiplier
        residual = clean(residual)
        residual_expression = sparse_expression(residual, edge_symbols)
        nonnegative, strict, detail = nonnegative_factor_expression(
            residual_expression, edge_symbols
        )
        if not nonnegative:
            return False, {
                "method": "inheritance_bernstein",
                "failed_index": list(beta),
                "detail": detail,
            }
        strict_count += int(strict)
        coefficient_rows.append({"index": list(beta), "strict": strict})

    return strict_count > 0, {
        "method": "inheritance_bernstein",
        "degrees": list(degrees),
        "coefficient_count": len(coefficient_rows),
        "strict_coefficient_count": strict_count,
        "coefficients": coefficient_rows,
    }


def certify_strict_positive(expression, all_symbols, inheritance_symbols):
    direction, factor_detail = factor_strict_sign(expression, all_symbols)
    if direction == 1:
        return factor_detail

    success, inheritance_detail = inheritance_bernstein_positive(
        expression, all_symbols, inheritance_symbols
    )
    if success:
        return inheritance_detail

    direct_direction, direct_detail = bernstein_sign(expression, all_symbols)
    if direct_direction == 1:
        return {"method": "full_bernstein", **direct_detail}

    raise CheckFailure({
        "message": "could not independently certify strict positivity",
        "factor_attempt": factor_detail,
        "inheritance_attempt": inheritance_detail,
        "full_bernstein_attempt": direct_detail,
    })


def compact_proof(proof):
    retained = (
        "method", "constant", "factor_count", "degrees", "coefficient_count",
        "strict_coefficient_count", "minimum", "maximum",
    )
    return {key: proof[key] for key in retained if key in proof}


def verify_endpoint_record(record, expected_id):
    require(record.get("id") == expected_id, ("endpoint id order", expected_id, record.get("id")))
    reticulation_count = int(record["reticulation_count"])
    signatures = tuple(tuple(int(mask) for mask in row) for row in record["signatures"])
    require(reticulation_count in (0, 1, 2), ("reticulation count", expected_id, reticulation_count))
    require(len(signatures) == len(set(signatures)), ("duplicate effective signature", expected_id))
    require(signatures == tuple(sorted(signatures)), ("signature ordering", expected_id))
    require(all(len(row) == 2 ** reticulation_count for row in signatures),
            ("switch width", expected_id))
    require(all(0 <= mask < 8 for row in signatures for mask in row),
            ("three-port mask range", expected_id))
    require(all(any(row) for row in signatures), ("inert all-zero signature", expected_id))
    require(all(mask != 7 for row in signatures for mask in row),
            ("unnormalized full three-port mask", expected_id))
    signature_hash = hashlib.sha256(repr((reticulation_count, signatures)).encode()).hexdigest()
    require(record.get("tensor_sha256") == signature_hash,
            ("signature tensor hash", expected_id, record.get("tensor_sha256"), signature_hash))

    dichotomy = record["dichotomy"]
    case = dichotomy["case"]
    require(case in EXPECTED_CASES, ("unknown endpoint case", expected_id, case))

    if case == "Delta_zero_Gamma_zero_ordinary":
        require(expected_id == 0 and reticulation_count == 0 and signatures == (),
                ("ordinary endpoint encoding", expected_id))
        require("normalization" not in dichotomy, ("ordinary normalization", expected_id))
        require(dichotomy["certificate"] == {
            "Delta": "0",
            "Gamma": "0",
            "method": "exact_constant_ordinary_component",
        }, ("ordinary stored certificate", expected_id))
        ordinary_coordinates = {
            name: jc_coordinate(signatures, reticulation_count, assignment)
            for name, assignment in THREE_COORDINATES.items()
        }
        require(all(value == constant(0) for value in ordinary_coordinates.values()),
                ("ordinary constant-chart coordinates", ordinary_coordinates))
        ordinary_delta = add(
            multiply(
                multiply(ordinary_coordinates["a"], ordinary_coordinates["b"]),
                ordinary_coordinates["c"],
            ),
            scale(multiply(ordinary_coordinates["t"], ordinary_coordinates["t"]), -1),
        )
        ordinary_gamma = add(
            ordinary_coordinates["a"],
            scale(multiply(ordinary_coordinates["b"], ordinary_coordinates["c"]), -1),
        )
        require(not ordinary_delta and not ordinary_gamma,
                ("ordinary Delta/Gamma reconstruction", ordinary_delta, ordinary_gamma))
        return {
            "id": expected_id,
            "case": case,
            "edge_classes": 0,
            "reticulation_count": 0,
            "Delta_terms": 0,
            "Gamma_terms": 0,
            "tensor_sha256_recomputed": signature_hash,
            "independent_method": "exact_constant_ordinary_component",
        }

    require(signatures, ("nonordinary endpoint has no signatures", expected_id))
    central = [
        index
        for index, row in enumerate(signatures)
        if len(set(row)) == 1 and row[0] in (3, 4)
    ]
    require(len(central) == 1, ("central incidence class", expected_id, central))
    central_index = central[0]
    expected_normalization = {
        "central_effective_edge_index": central_index,
        "central_effective_signature": list(signatures[central_index]),
        "substitution": f"x{central_index}=1",
    }
    require(dichotomy.get("normalization") == expected_normalization,
            ("stored central normalization", expected_id, dichotomy.get("normalization"),
             expected_normalization))

    edge_count = len(signatures)
    width = edge_count + reticulation_count
    edge_symbols = tuple(sp.symbols(f"x0:{edge_count}"))
    inheritance_symbols = tuple(sp.symbols(f"l0:{reticulation_count}"))
    all_symbols = edge_symbols + inheritance_symbols

    zero_coordinate = substitute_one(
        jc_coordinate(signatures, reticulation_count, (0, 0, 0)), central_index
    )
    require(zero_coordinate == constant(width), ("q000 normalization", expected_id, zero_coordinate))
    coordinates = {
        name: substitute_one(
            jc_coordinate(signatures, reticulation_count, assignment), central_index
        )
        for name, assignment in THREE_COORDINATES.items()
    }
    delta = add(
        multiply(multiply(coordinates["a"], coordinates["b"]), coordinates["c"]),
        scale(multiply(coordinates["t"], coordinates["t"]), -1),
    )
    gamma = add(coordinates["a"], scale(multiply(coordinates["b"], coordinates["c"]), -1))
    delta_expression = sparse_expression(delta, all_symbols)
    gamma_expression = sparse_expression(gamma, all_symbols)

    if case == "Delta_positive":
        require(delta, ("stored Delta-positive case is identically zero", expected_id))
        require(dichotomy["certificate"].get("method") in {
            "factor_bernstein", "inheritance_bernstein",
        }, ("stored Delta-positive method", expected_id, dichotomy["certificate"]))
        proof = certify_strict_positive(delta_expression, all_symbols, inheritance_symbols)
    elif case == "Delta_zero_Gamma_positive":
        require(not delta, ("stored Delta-zero case is nonzero", expected_id, sparse_digest(delta)))
        require(gamma, ("stored Gamma-positive case is identically zero", expected_id))
        require(dichotomy["certificate"].get("method") in {
            "factor_bernstein", "inheritance_bernstein",
        }, ("stored Gamma-positive method", expected_id, dichotomy["certificate"]))
        proof = certify_strict_positive(gamma_expression, all_symbols, inheritance_symbols)
    else:
        require(case == "Delta_zero_Gamma_zero", ("unhandled endpoint case", expected_id, case))
        require(not delta and not gamma,
                ("stored Delta/Gamma-zero case is nonzero", expected_id,
                 sparse_digest(delta), sparse_digest(gamma)))
        require(dichotomy["certificate"].get("method") == "zero",
                ("stored zero method", expected_id, dichotomy["certificate"]))
        proof = {"method": "exact_sparse_zero"}

    return {
        "id": expected_id,
        "case": case,
        "edge_classes": edge_count,
        "reticulation_count": reticulation_count,
        "central_effective_edge_index": central_index,
        "central_effective_signature": list(signatures[central_index]),
        "Delta_terms": len(delta),
        "Gamma_terms": len(gamma),
        "Delta_sha256": sparse_digest(delta),
        "Gamma_sha256": sparse_digest(gamma),
        "tensor_sha256_recomputed": signature_hash,
        "stored_method": dichotomy["certificate"].get("method"),
        "independent_method": proof["method"],
        "independent_proof": compact_proof(proof),
    }


def polynomial_terms(expression, symbols):
    polynomial = sp.Poly(sp.expand(expression), *symbols, domain=sp.QQ)
    return tuple(
        (tuple(int(value) for value in power), int(coefficient.p), int(coefficient.q))
        for power, coefficient in polynomial.terms()
    )


def up_to_sign_key(expression, symbols):
    positive = polynomial_terms(expression, symbols)
    negative = polynomial_terms(-sp.expand(expression), symbols)
    return min(positive, negative)


def endpoint_orbit(assignment, coordinates):
    require(assignment[0] ^ assignment[1] ^ assignment[2] == 0,
            ("two-active endpoint assignment", assignment))
    a, b, c, t = coordinates
    nonzero = [index for index, value in enumerate(assignment) if value]
    if not nonzero:
        return sp.Integer(1)
    if len(nonzero) == 2:
        zero = next(index for index, value in enumerate(assignment) if not value)
        return (c, b, a)[zero]
    require(len(nonzero) == 3 and len(set(assignment)) == 3,
            ("unexpected three-port JC orbit", assignment))
    return t


def verify_two_active(stored):
    a, b, c, t, upper_a, upper_b, upper_c, upper_t, z = sp.symbols(
        "a b c t A B C T z"
    )
    symbols = (a, b, c, t, upper_a, upper_b, upper_c, upper_t, z)
    lower = (a, b, c, t)
    upper = (upper_a, upper_b, upper_c, upper_t)
    minor_keys = set()
    blocks = {}

    for total in GROUP:
        pairs = tuple(pair for pair in product(GROUP, repeat=2) if pair[0] ^ pair[1] == total)
        matrix = []
        for g1, g3 in pairs:
            row = []
            for g2, g4 in pairs:
                separator = g1 ^ g2
                entry = endpoint_orbit((g1, g2, separator), lower)
                entry *= endpoint_orbit((g3, g4, separator), upper)
                if separator:
                    entry *= z
                row.append(sp.expand(entry))
            matrix.append(row)
        blocks[total] = {"pairs": pairs, "matrix": matrix}
        for rows in combinations(range(4), 2):
            for columns in combinations(range(4), 2):
                determinant = sp.expand(
                    matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
                    - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
                )
                if determinant != 0:
                    minor_keys.add(up_to_sign_key(determinant, symbols))

    required = {
        "f1": a * upper_a - z ** 2 * b * c * upper_b * upper_c,
        "f2": z * upper_t * t - z ** 2 * b * c * upper_b * upper_c,
        "f3": z * upper_c * (upper_a * t - z * upper_t * b * c),
        "f4": z * c * (z * upper_b * upper_c * t - upper_t * a),
    }

    def selected_ordered_minor(total, row_pairs, column_pairs):
        pairs = blocks[total]["pairs"]
        matrix = blocks[total]["matrix"]
        rows = tuple(pairs.index(pair) for pair in row_pairs)
        columns = tuple(pairs.index(pair) for pair in column_pairs)
        return sp.expand(
            matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
            - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
        )

    ordered = {
        "f1": selected_ordered_minor(0, ((0, 0), (1, 1)), ((0, 0), (1, 1))),
        "f2": selected_ordered_minor(0, ((0, 0), (1, 1)), ((0, 0), (2, 2))),
        "f3": selected_ordered_minor(1, ((0, 1), (1, 0)), ((0, 1), (2, 3))),
        "f4": selected_ordered_minor(1, ((0, 1), (1, 0)), ((1, 0), (2, 3))),
    }
    require(all(sp.expand(ordered[name] - required[name]) == 0 for name in required),
            ("ordered two-active minors", ordered, required))
    membership = {
        name: up_to_sign_key(expression, symbols) in minor_keys
        for name, expression in required.items()
    }
    require(all(membership.values()), ("two-active minor membership", membership))

    f1, f2, f3, f4 = (required[name] for name in ("f1", "f2", "f3", "f4"))
    identities = {
        "Aa_equals_zTt": sp.expand(a * upper_a - z * upper_t * t - (f1 - f2)),
        "left_F": sp.expand(
            z ** 2 * upper_c * upper_t * (a * b * c - t ** 2)
            - (z * upper_c * t * (f1 - f2) - a * f3)
        ),
        "right_F": sp.expand(
            z ** 2 * c * t * (upper_a * upper_b * upper_c - upper_t ** 2)
            - (upper_a * f4 + z * c * upper_t * (f1 - f2))
        ),
    }
    require(all(value == 0 for value in identities.values()), ("two-active identities", identities))

    lower_product, upper_product = sp.symbols("p P", positive=True)
    gamma, upper_gamma = sp.symbols("gamma Gamma", nonnegative=True)
    strict_expression = sp.expand(
        (lower_product + gamma) * (upper_product + upper_gamma)
        - z ** 2 * lower_product * upper_product
    )
    positive_decomposition = sp.expand(
        lower_product * upper_product * (1 - z ** 2)
        + lower_product * upper_gamma
        + upper_product * gamma
        + gamma * upper_gamma
    )
    require(sp.expand(strict_expression - positive_decomposition) == 0,
            "two-active strict-inequality decomposition")
    bound_to_f1 = sp.expand(strict_expression.subs({
        lower_product: b * c,
        upper_product: upper_b * upper_c,
        gamma: a - b * c,
        upper_gamma: upper_a - upper_b * upper_c,
    }) - f1)
    require(bound_to_f1 == 0, "two-active strict decomposition is not bound to f1")

    require(stored.get("status") == "EXACTLY COMPUTED", "stored two-active status")
    require(stored.get("minor_count_up_to_sign") == len(minor_keys),
            ("stored two-active minor count", stored.get("minor_count_up_to_sign"), len(minor_keys)))
    require(stored.get("required_minor_membership") == membership,
            ("stored two-active membership", stored.get("required_minor_membership"), membership))
    require(stored.get("identity_remainders") == {name: "0" for name in identities},
            ("stored two-active remainders", stored.get("identity_remainders")))

    return {
        "minor_count_up_to_sign": len(minor_keys),
        "four_ordered_manuscript_minors_checked": True,
        "required_minor_membership": membership,
        "identity_remainders": {name: str(value) for name, value in identities.items()},
        "strict_f1_decomposition": str(positive_decomposition),
        "strict_f1_conditions": ["p>0", "P>0", "gamma>=0", "Gamma>=0", "0<z<1"],
        "strict_f1_decomposition_checked": True,
        "strict_sign_from_listed_conditions": "elementary handwritten inference",
    }


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    args = arguments()
    proof_root = locate_proof_root(args.package_root.resolve())
    relative = Path("cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json")
    certificate_path = proof_root / relative
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    require(certificate.get("status") == "EXACTLY COMPUTED", "corrected certificate status")

    endpoint = certificate.get("three_port_endpoint_dichotomy", {})
    records = endpoint.get("records", [])
    require(endpoint.get("status") == "EXACTLY COMPUTED", "stored endpoint section status")
    require(endpoint.get("failures") == [], "stored endpoint failures")
    require(endpoint.get("tensor_count") == 77 and len(records) == 77,
            ("endpoint record count", endpoint.get("tensor_count"), len(records)))

    summaries = [verify_endpoint_record(record, index) for index, record in enumerate(records)]
    record_keys = [
        (int(record["reticulation_count"]), tuple(tuple(row) for row in record["signatures"]))
        for record in records
    ]
    require(len(record_keys) == len(set(record_keys)) == 77, "unique endpoint signature records")
    cases = Counter(summary["case"] for summary in summaries)
    methods = Counter(summary["independent_method"] for summary in summaries)
    reticulation_counts = Counter(summary["reticulation_count"] for summary in summaries)
    require(dict(cases) == EXPECTED_CASES, ("independent endpoint case census", dict(cases)))
    require(dict(reticulation_counts) == {0: 1, 1: 7, 2: 69},
            ("endpoint reticulation census", dict(reticulation_counts)))
    require([row["id"] for row in summaries if row["case"] == "Delta_zero_Gamma_zero"]
            == [6, 7, 56, 58, 74, 75, 76], "Delta/Gamma-zero endpoint IDs")
    require([row["id"] for row in summaries if row["case"] == "Delta_zero_Gamma_positive"]
            == [67, 72], "Gamma-positive endpoint IDs")
    require(endpoint.get("dichotomy_counts") == EXPECTED_CASES,
            ("stored endpoint case census", endpoint.get("dichotomy_counts")))

    two_active = verify_two_active(certificate.get("two_active_crossing", {}))
    report = {
        "schema": "independent-jc-endpoint-certificate-check-v1",
        "status": "PASS",
        "input": {
            "path_within_proof_package": relative.as_posix(),
            "bytes": certificate_path.stat().st_size,
            "sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        },
        "endpoint": {
            "records_checked": len(summaries),
            "normalizations_checked": sum("central_effective_edge_index" in row for row in summaries),
            "case_counts": dict(sorted(cases.items())),
            "reticulation_counts": {str(key): value for key, value in sorted(reticulation_counts.items())},
            "independent_proof_methods": dict(sorted(methods.items())),
            "records": summaries,
        },
        "two_active": two_active,
        "independence": {
            "package_modules_imported": False,
            "stored_endpoint_sign_certificates_trusted": False,
            "stored_factor_and_bernstein_detail_payloads_replayed": False,
            "stored_case_labels_retained_and_checked": True,
            "stored_normalizations_retained_and_checked": True,
            "raw_signatures_and_inheritance_counts_retained": True,
            "jc_tensor_reconstructed_as_sparse_rational_polynomials": True,
            "exact_symbolic_and_bernstein_sign_checks": True,
            "witness_graphs_reconstructed": False,
            "primitive_graph_completeness_regenerated": False,
            "unreduced_808642_word_census_regenerated": False,
            "boundary": (
                "This check independently validates the endpoint and two-active algebra for all 77 "
                "supplied corrected signature records. It does not regenerate the primitive graph "
                "classification/completion grammar, witness graphs, or the 808,642 unreduced word "
                "census. Stored factor/Bernstein detail summaries are ignored because every target "
                "sign is rederived independently."
            ),
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    atomic_json(args.output_dir / "jc_endpoint_certificate.json", report)
    print(rendered, end="")


if __name__ == "__main__":
    main()
