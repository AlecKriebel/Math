#!/usr/bin/env python3
"""Independent exact D3+ homogeneous-coefficient audit for cut minors.

This script only consumes the graph-derived target descriptors from the parent
cross-bridge exploration.  For every unresolved target direction, it rebuilds
all four Fourier blocks and their 2x2 minors, factors a strictly positive
monomial, and substitutes each K3P edge spectrum

    c = w_C + w_U,  g = w_G + w_U,  t = w_T + w_U,

where (w_O,w_C,w_G,w_T,w_U) is in the open four-simplex.  It homogenizes in
each edge's five weights independently.  Inheritance variables are treated as
open one-simplexes, lambda = l_1 and 1-lambda = l_0.

If every resulting homogeneous coefficient has one weak sign and at least one
is nonzero, the minor is strictly signed throughout the strict principal K3P
domain.  The condition is sufficient, not necessary.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PROJECT = HERE.parents[2]
UPSTREAM_REPORT = PARENT / "CUT_MINOR_SIGN_SEARCH.json"
RESULT_PATH = HERE / "SIMPLEX_HOMOGENEOUS_RESULTS.json"


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cross = import_path("audit_simplex_crossbridge", PARENT / "explore_crossbridge_atlas.py")
atlas = cross.atlas


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def sparse_mul(left, right):
    answer = collections.defaultdict(int)
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            answer[tuple(a + b for a, b in zip(left_exp, right_exp))] += (
                left_coefficient * right_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def sparse_subtract(left, right):
    answer = collections.defaultdict(int)
    for exponent, coefficient in left.items():
        answer[exponent] += int(coefficient)
    for exponent, coefficient in right.items():
        answer[exponent] -= int(coefficient)
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def minor_polynomial(outputs, coordinate_index, character_sum, rows, columns):
    row0, row1 = rows
    column0, column1 = columns
    a = coordinate_index[(row0, character_sum ^ row0, column0, character_sum ^ column0)]
    b = coordinate_index[(row1, character_sum ^ row1, column1, character_sum ^ column1)]
    c = coordinate_index[(row0, character_sum ^ row0, column1, character_sum ^ column1)]
    d = coordinate_index[(row1, character_sum ^ row1, column0, character_sum ^ column0)]
    return sparse_subtract(sparse_mul(outputs[a], outputs[b]), sparse_mul(outputs[c], outputs[d])), (a, b, c, d)


def factor_positive_monomial(polynomial):
    width = len(next(iter(polynomial)))
    common = tuple(min(exponent[axis] for exponent in polynomial) for axis in range(width))
    answer = collections.defaultdict(int)
    for exponent, coefficient in polynomial.items():
        answer[tuple(exponent[axis] - common[axis] for axis in range(width))] += coefficient
    return common, {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def multinomial_expansion(variable_count: int, degree: int):
    """Return exact coefficients of (z_0+...+z_{m-1})**degree."""
    if degree == 0:
        return {(0,) * variable_count: 1}
    answer = {}
    for exponent in weak_compositions(degree, variable_count):
        coefficient = math.factorial(degree)
        for value in exponent:
            coefficient //= math.factorial(value)
        answer[exponent] = coefficient
    return answer


def weak_compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def convolve_local(left, right):
    answer = collections.defaultdict(int)
    for alpha, ca in left.items():
        for beta, cb in right.items():
            answer[tuple(a + b for a, b in zip(alpha, beta))] += ca * cb
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def power_of_linear_form(indices, exponent, width):
    """Expand (sum(z_i for i in indices))**exponent."""
    if exponent == 0:
        return {(0,) * width: 1}
    answer = {}
    for local in weak_compositions(exponent, len(indices)):
        full = [0] * width
        coefficient = math.factorial(exponent)
        for value in local:
            coefficient //= math.factorial(value)
        for index, value in zip(indices, local):
            full[index] = value
        answer[tuple(full)] = coefficient
    return answer


def edge_expansion(exponents, degree):
    """Substitute c=C+U, g=G+U, t=T+U and homogenize to degree."""
    c_exp, g_exp, t_exp = exponents
    answer = {(0, 0, 0, 0, 0): 1}
    for indices, exponent in (((1, 4), c_exp), ((2, 4), g_exp), ((3, 4), t_exp)):
        answer = convolve_local(answer, power_of_linear_form(indices, exponent, 5))
    used_degree = c_exp + g_exp + t_exp
    if used_degree > degree:
        raise AssertionError((exponents, degree))
    answer = convolve_local(answer, multinomial_expansion(5, degree - used_degree))
    return answer


def inheritance_expansion(exponent, degree):
    """Substitute lambda=L1 and homogenize with L0+L1=1."""
    if exponent > degree:
        raise AssertionError((exponent, degree))
    answer = {}
    for alpha in range(degree - exponent + 1):
        # L1**exponent * (L0+L1)**(degree-exponent)
        answer[(alpha, degree - alpha)] = math.comb(degree - exponent, alpha)
    # The loop records L0 exponent alpha and L1 exponent degree-alpha.  Since
    # lambda contributes exponent first, the correct L1 exponent is degree-alpha.
    return answer


class ExpansionTooLarge(RuntimeError):
    pass


def homogeneous_coefficients(polynomial, edge_count, inheritance_count, cap):
    """Return sparse tensor homogeneous coefficients or raise at the cap."""
    edge_degrees = []
    for edge in range(edge_count):
        edge_degrees.append(
            max(sum(exponent[3 * edge : 3 * edge + 3]) for exponent in polynomial)
        )
    inheritance_degrees = []
    inheritance_offset = 3 * edge_count
    for variable in range(inheritance_count):
        inheritance_degrees.append(
            max(exponent[inheritance_offset + variable] for exponent in polynomial)
        )
    active_groups = tuple(
        [("edge", edge, degree) for edge, degree in enumerate(edge_degrees) if degree]
        + [("inheritance", variable, degree) for variable, degree in enumerate(inheritance_degrees) if degree]
    )
    output = collections.defaultdict(int)
    edge_cache = {}
    inheritance_cache = {}
    for exponent, coefficient in polynomial.items():
        partial = {(): coefficient}
        for kind, index, degree in active_groups:
            if kind == "edge":
                local_power = tuple(exponent[3 * index : 3 * index + 3])
                cache_key = (local_power, degree)
                if cache_key not in edge_cache:
                    edge_cache[cache_key] = edge_expansion(local_power, degree)
                local = edge_cache[cache_key]
            else:
                local_power = exponent[inheritance_offset + index]
                cache_key = (local_power, degree)
                if cache_key not in inheritance_cache:
                    inheritance_cache[cache_key] = inheritance_expansion(local_power, degree)
                local = inheritance_cache[cache_key]
            new_partial = collections.defaultdict(int)
            for prefix, prefix_coefficient in partial.items():
                for local_exponent, local_coefficient in local.items():
                    new_partial[prefix + (local_exponent,)] += prefix_coefficient * local_coefficient
            partial = {key: value for key, value in new_partial.items() if value}
            if len(partial) > cap:
                raise ExpansionTooLarge(len(partial))
        for key, value in partial.items():
            output[key] += value
        if len(output) > cap:
            raise ExpansionTooLarge(len(output))
    return (
        {key: value for key, value in output.items() if value},
        active_groups,
        edge_degrees,
        inheritance_degrees,
    )


def coefficient_sign(coefficients):
    values = tuple(coefficients.values())
    if values and all(value >= 0 for value in values) and any(value > 0 for value in values):
        return 1
    if values and all(value <= 0 for value in values) and any(value < 0 for value in values):
        return -1
    return 0


def polynomial_digest(polynomial):
    return digest([[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())])


def coefficient_digest(coefficients):
    payload = []
    for key, coefficient in sorted(coefficients.items()):
        payload.append([[list(local) for local in key], str(coefficient)])
    return digest(payload)


def evaluate_power_polynomial(polynomial, values):
    answer = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = Fraction(coefficient)
        for value, power in zip(values, exponent):
            term *= value**power
        answer += term
    return answer


def evaluate_homogeneous(coefficients, groups, edge_weights, inheritance_weights):
    answer = Fraction(0)
    for key, coefficient in coefficients.items():
        term = Fraction(coefficient)
        for local_exponent, (kind, index, _degree) in zip(key, groups):
            weights = edge_weights[index] if kind == "edge" else inheritance_weights[index]
            for value, power in zip(weights, local_exponent):
                term *= value**power
        answer += term
    return answer


def exact_identity_check(polynomial, coefficients, groups, edge_count, inheritance_count):
    # Deterministic strictly positive rational simplex weights, independently
    # normalized for every edge and inheritance variable.
    edge_weights = []
    for edge in range(edge_count):
        raw = tuple(Fraction(edge + j + 2) for j in range(5))
        total = sum(raw)
        edge_weights.append(tuple(value / total for value in raw))
    inheritance_weights = []
    for variable in range(inheritance_count):
        raw = (Fraction(variable + 2), Fraction(variable + 5))
        total = sum(raw)
        inheritance_weights.append(tuple(value / total for value in raw))
    values = []
    for weights in edge_weights:
        o, c_vertex, g_vertex, t_vertex, u_vertex = weights
        del o
        values.extend((c_vertex + u_vertex, g_vertex + u_vertex, t_vertex + u_vertex))
    for weights in inheritance_weights:
        values.append(weights[1])
    direct = evaluate_power_polynomial(polynomial, values)
    homogeneous = evaluate_homogeneous(
        coefficients, groups, edge_weights, inheritance_weights
    )
    if direct != homogeneous:
        raise AssertionError((direct, homogeneous))
    return str(direct)


def candidate_complexity(polynomial, edge_count, inheritance_count):
    edge_basis = 1
    for edge in range(edge_count):
        degree = max(sum(exponent[3 * edge : 3 * edge + 3]) for exponent in polynomial)
        if degree:
            edge_basis *= math.comb(degree + 4, 4)
    inheritance_basis = 1
    offset = 3 * edge_count
    for variable in range(inheritance_count):
        degree = max(exponent[offset + variable] for exponent in polynomial)
        if degree:
            inheritance_basis *= degree + 1
    return edge_basis * inheritance_basis


def audit_target(target_index, target, coordinate_index, pairs, cap):
    descriptor = target["descriptor"]
    outputs = atlas.output_sparse_polynomials(descriptor)
    candidates = []
    for character_sum in range(4):
        for rows in pairs:
            for columns in pairs:
                polynomial, coordinates = minor_polynomial(
                    outputs, coordinate_index, character_sum, rows, columns
                )
                if not polynomial:
                    continue
                common, reduced = factor_positive_monomial(polynomial)
                candidates.append(
                    (
                        candidate_complexity(
                            reduced, descriptor.edge_class_count, descriptor.retic_count
                        ),
                        len(reduced),
                        character_sum,
                        rows,
                        columns,
                        coordinates,
                        common,
                        reduced,
                    )
                )
    candidates.sort(key=lambda row: row[:5])
    tested = 0
    oversized = 0
    best_mixed = None
    for (
        basis_bound,
        term_count,
        character_sum,
        rows,
        columns,
        coordinates,
        common,
        reduced,
    ) in candidates:
        try:
            coefficients, groups, edge_degrees, inheritance_degrees = homogeneous_coefficients(
                reduced, descriptor.edge_class_count, descriptor.retic_count, cap
            )
        except ExpansionTooLarge:
            oversized += 1
            continue
        tested += 1
        sign = coefficient_sign(coefficients)
        negative = sum(value < 0 for value in coefficients.values())
        positive = sum(value > 0 for value in coefficients.values())
        zero = basis_bound - len(coefficients)
        summary = {
            "basis_bound": basis_bound,
            "stored_nonzero_coefficients": len(coefficients),
            "negative": negative,
            "implicit_zero": zero,
            "positive": positive,
            "minimum": str(min(coefficients.values())),
            "maximum": str(max(coefficients.values())),
        }
        mixed_score = min(negative, positive)
        if best_mixed is None or (mixed_score, basis_bound, term_count) < best_mixed[0]:
            best_mixed = (
                (mixed_score, basis_bound, term_count),
                {
                    "character_sum": character_sum,
                    "rows": list(rows),
                    "columns": list(columns),
                    "coefficient_summary": summary,
                },
            )
        if not sign:
            continue
        identity_value = exact_identity_check(
            reduced,
            coefficients,
            groups,
            descriptor.edge_class_count,
            descriptor.retic_count,
        )
        return {
            "target_index": target_index,
            "record_id": target["record_id"],
            "status": "CERTIFIED",
            "descriptor_sha256": cross.digest(cross.descriptor_payload(descriptor)),
            "tested_minors": tested,
            "oversized_minors": oversized,
            "certificate": {
                "character_sum": character_sum,
                "rows": list(rows),
                "columns": list(columns),
                "coordinate_indices": list(coordinates),
                "sign": sign,
                "term_count": term_count,
                "positive_monomial_exponent": list(common),
                "reduced_polynomial_sha256": polynomial_digest(reduced),
                "edge_homogeneous_degrees": edge_degrees,
                "inheritance_homogeneous_degrees": inheritance_degrees,
                "active_groups": [list(group) for group in groups],
                "coefficient_summary": summary,
                "homogeneous_coefficients_sha256": coefficient_digest(coefficients),
                "exact_identity_test_value": identity_value,
            },
        }
    return {
        "target_index": target_index,
        "record_id": target["record_id"],
        "status": "NO_SINGLE_MINOR_CERTIFICATE_AT_CAP",
        "descriptor_sha256": cross.digest(cross.descriptor_payload(descriptor)),
        "tested_minors": tested,
        "oversized_minors": oversized,
        "candidate_minors": len(candidates),
        "best_mixed": None if best_mixed is None else best_mixed[1],
        "certificate": None,
    }


def inheritance_self_test():
    # lambda**e (L0+L1)**(d-e) must equal lambda**e on L0+L1=1.
    for degree in range(5):
        for exponent in range(degree + 1):
            expansion = inheritance_expansion(exponent, degree)
            l0, l1 = Fraction(2, 7), Fraction(5, 7)
            value = sum(
                coefficient * l0**alpha[0] * l1**alpha[1]
                for alpha, coefficient in expansion.items()
            )
            if value != l1**exponent:
                raise AssertionError((degree, exponent, value, l1**exponent))


def edge_self_test():
    weights = tuple(map(Fraction, (2, 3, 5, 7, 11)))
    total = sum(weights)
    weights = tuple(value / total for value in weights)
    c = weights[1] + weights[4]
    g = weights[2] + weights[4]
    t = weights[3] + weights[4]
    for exponents in itertools.product(range(3), repeat=3):
        used = sum(exponents)
        for degree in range(used, used + 3):
            expansion = edge_expansion(exponents, degree)
            value = sum(
                coefficient
                * math.prod(weight**power for weight, power in zip(weights, alpha))
                for alpha, coefficient in expansion.items()
            )
            if value != c**exponents[0] * g**exponents[1] * t**exponents[2]:
                raise AssertionError((exponents, degree, value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=2_000_000)
    parser.add_argument("--targets", nargs="*", type=int)
    args = parser.parse_args()
    inheritance_self_test()
    edge_self_test()

    upstream = json.loads(UPSTREAM_REPORT.read_text())
    unresolved = tuple(upstream["unsolved_target_indices"])
    requested = unresolved if args.targets is None else tuple(args.targets)
    if any(target not in unresolved for target in requested):
        raise SystemExit("--targets must be drawn from the 24 upstream unresolved indices")
    _, _, _, targets = cross.build_universes()
    assignments = atlas.k3p_assignments(4)
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments)}
    pairs = tuple((left, right) for left in range(4) for right in range(left + 1, 4))
    records = []
    for target_index in requested:
        record = audit_target(target_index, targets[target_index], coordinate_index, pairs, args.cap)
        records.append(record)
        print(json.dumps({key: record[key] for key in ("target_index", "record_id", "status", "tested_minors", "oversized_minors")}, sort_keys=True), flush=True)
    payload = {
        "schema": "k3p-d3plus-simplex-homogeneous-audit-v1",
        "status": "COMPLETE_FOR_REQUESTED_TARGETS",
        "method_scope": "sufficient single-minor homogeneous coefficient-sign test",
        "domain_vertices": {
            "O": [0, 0, 0],
            "C": [1, 0, 0],
            "G": [0, 1, 0],
            "T": [0, 0, 1],
            "U": [1, 1, 1],
        },
        "strictness_reason": "every strict D3+ point has a representation with all five vertex weights positive; every nonzero homogeneous basis monomial is then positive",
        "inputs": {
            "upstream_report": str(UPSTREAM_REPORT.relative_to(PROJECT)),
            "upstream_report_sha256": sha_file(UPSTREAM_REPORT),
            "crossbridge_compiler": str((PARENT / "explore_crossbridge_atlas.py").relative_to(PROJECT)),
            "crossbridge_compiler_sha256": sha_file(PARENT / "explore_crossbridge_atlas.py"),
        },
        "cap": args.cap,
        "requested_targets": list(requested),
        "certified": sum(record["status"] == "CERTIFIED" for record in records),
        "uncertified": [record["target_index"] for record in records if record["status"] != "CERTIFIED"],
        "records": records,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"certified": payload["certified"], "uncertified": payload["uncertified"]}, sort_keys=True))


if __name__ == "__main__":
    main()
