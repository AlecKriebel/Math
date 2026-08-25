#!/usr/bin/env python3
"""Exact record-43/target-127 transport of the cyclic nine-minor proof.

The nine selected zero-character-block minors are rebuilt from the frozen
graph descriptor.  After their positive monomial gcd is removed, each is
divided exactly by the additional strict factor (1-lambda_0).  The quotients
are compared coefficient-by-coefficient with a transported record-60 F/E
system, including its transposed ordered-cross indexing.  Sparse eliminant
identities then give the same impossible cyclic ratio system.
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

import search_simplex_homogeneous as audit


HERE = Path(__file__).resolve().parent
REPORT = HERE / "RECORD43_CYCLIC_TRANSPORT_AUDIT.json"
TARGET_INDEX = 127
SECTOR_NAMES = ("C", "G", "T")
CYCLIC_CASES = ((0, 1, 2), (1, 0, 2), (2, 0, 1))


def sparse_add(*terms):
    answer = collections.defaultdict(int)
    for multiplier, polynomial in terms:
        for exponent, coefficient in polynomial.items():
            answer[exponent] += multiplier * coefficient
    return {
        exponent: coefficient
        for exponent, coefficient in answer.items()
        if coefficient
    }


def sparse_mul(*polynomials):
    if not polynomials:
        raise ValueError("at least one polynomial is required")
    answer = polynomials[0]
    for polynomial in polynomials[1:]:
        answer = audit.sparse_mul(answer, polynomial)
    return answer


def variable(width, index):
    exponent = [0] * width
    exponent[index] = 1
    return {tuple(exponent): 1}


def constant(width, value=1):
    return {(0,) * width: value}


def digest_record(polynomial):
    return {
        "term_count": len(polynomial),
        "sha256": audit.polynomial_digest(polynomial),
    }


def divide_by_one_minus_variable(polynomial, variable_index):
    """Exact multivariate division by 1-x, returning quotient and remainder.

    Coefficients are grouped by all exponents except x.  For a univariate
    coefficient list c_k, divisibility by 1-x is equivalent to sum(c_k)=0,
    and, with remainder R=sum(c_k), the quotient coefficients are
    q_k=sum_{j<=k}c_j-R.  The returned remainder is P evaluated at x=1,
    represented with x exponent zero.  In the divisible case R=0, recovering
    the simpler cumulative-sum formula.
    """
    if not polynomial:
        return {}, {}
    width = len(next(iter(polynomial)))
    groups = collections.defaultdict(lambda: collections.defaultdict(int))
    for exponent, coefficient in polynomial.items():
        base = list(exponent)
        power = base[variable_index]
        base[variable_index] = 0
        groups[tuple(base)][power] += coefficient

    quotient = collections.defaultdict(int)
    remainder = collections.defaultdict(int)
    for base, coefficients in groups.items():
        maximum = max(coefficients)
        total = sum(coefficients.values())
        if total:
            remainder[base] += total
        cumulative = 0
        for power in range(maximum):
            cumulative += coefficients.get(power, 0)
            quotient_coefficient = cumulative - total
            if quotient_coefficient:
                exponent = list(base)
                exponent[variable_index] = power
                quotient[tuple(exponent)] += quotient_coefficient

    quotient = {key: value for key, value in quotient.items() if value}
    remainder = {key: value for key, value in remainder.items() if value}
    one = constant(width)
    x = variable(width, variable_index)
    divisor = sparse_add((1, one), (-1, x))
    replay = sparse_add((1, sparse_mul(divisor, quotient)), (1, remainder))
    if replay != polynomial:
        raise AssertionError("division replay failed")
    return quotient, remainder


def build_closed_form(
    descriptor,
    *,
    p_variable=1,
    a_edge=1,
    b_edge=4,
    c_edge=8,
    d_edge=9,
):
    width = 3 * descriptor.edge_class_count + descriptor.retic_count
    one = constant(width)
    p = variable(width, 3 * descriptor.edge_class_count + p_variable)
    q = sparse_add((1, one), (-1, p))
    a = {s: variable(width, 3 * a_edge + s) for s in range(3)}
    b = {s: variable(width, 3 * b_edge + s) for s in range(3)}
    c = {s: variable(width, 3 * c_edge + s) for s in range(3)}
    d = {s: variable(width, 3 * d_edge + s) for s in range(3)}
    K = {
        s: sparse_add(
            (1, sparse_mul(p, a[s], b[s])),
            (1, sparse_mul(q, c[s])),
        )
        for s in range(3)
    }
    L = {
        s: sparse_add(
            (1, sparse_mul(p, a[s])),
            (1, sparse_mul(q, b[s], c[s])),
        )
        for s in range(3)
    }
    F = {
        s: sparse_add(
            (1, b[s]),
            (-1, sparse_mul(d[s], d[s], K[s], L[s])),
        )
        for s in range(3)
    }
    M = {}
    E = {}
    for s in range(3):
        for t in range(3):
            if s == t:
                continue
            r = ((s + 1) ^ (t + 1)) - 1
            M[s, t] = sparse_add(
                (1, sparse_mul(p, b[s], a[r])),
                (1, sparse_mul(q, b[t], c[r])),
            )
            E[s, t] = sparse_add(
                (1, sparse_mul(d[r], M[s, t])),
                (-1, sparse_mul(d[s], d[t], K[s], L[t])),
            )
    return {
        "width": width,
        "one": one,
        "p": p,
        "q": q,
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "K": K,
        "L": L,
        "F": F,
        "M": M,
        "E": E,
    }


def extract_divided_minor(
    sparse_outputs,
    coordinate_index,
    character_sum,
    rows,
    columns,
    lambda_zero_index,
):
    full, coordinates = audit.minor_polynomial(
        sparse_outputs, coordinate_index, character_sum, rows, columns
    )
    common, reduced = audit.factor_positive_monomial(full)
    quotient, remainder = divide_by_one_minus_variable(
        reduced, lambda_zero_index
    )
    return {
        "full": full,
        "coordinates": coordinates,
        "positive_monomial": common,
        "reduced": reduced,
        "quotient": quotient,
        "remainder": remainder,
    }


def consequence_records(closed):
    records = []
    for r, s, t in CYCLIC_CASES:
        b = closed["b"]
        d = closed["d"]
        F = closed["F"]
        E = closed["E"]
        K = closed["K"]
        L = closed["L"]
        M = closed["M"]
        C = sparse_add(
            (1, sparse_mul(d[r], d[r], M[s, t], M[t, s])),
            (-1, sparse_mul(b[s], b[t])),
        )
        combination = sparse_add(
            (1, sparse_mul(E[s, t], d[r], M[t, s])),
            (1, sparse_mul(d[s], d[t], K[s], L[t], E[t, s])),
            (-1, sparse_mul(b[s], F[t])),
            (-1, sparse_mul(b[t], F[s])),
            (1, sparse_mul(F[s], F[t])),
        )
        if C != combination:
            raise AssertionError((r, "cross eliminant"))

        factor_one = sparse_add(
            (1, b[t]), (-1, sparse_mul(b[s], b[r]))
        )
        factor_two = sparse_add(
            (1, sparse_mul(b[t], b[r])), (-1, b[s])
        )
        lhs = sparse_add(
            (1, sparse_mul(b[r], C)),
            (1, sparse_mul(b[s], b[t], F[r])),
        )
        rhs = sparse_mul(
            d[r],
            d[r],
            closed["p"],
            closed["q"],
            closed["a"][r],
            closed["c"][r],
            factor_one,
            factor_two,
        )
        if lhs != rhs:
            raise AssertionError((r, "cyclic factorization"))
        records.append(
            {
                "r": SECTOR_NAMES[r],
                "s": SECTOR_NAMES[s],
                "t": SECTOR_NAMES[t],
                "cross_consequence": digest_record(C),
                "cross_combination": digest_record(combination),
                "factor_polynomial": digest_record(lhs),
                "cross_identity": (
                    "C_r=E_st*d_r*M_ts+d_s*d_t*K_s*L_t*E_ts"
                    "-b_s*F_t-b_t*F_s+F_s*F_t"
                ),
                "factor_identity": (
                    "b_r*C_r+b_s*b_t*F_r="
                    "d_r^2*p*(1-p)*a_r*c_r"
                    "*(b_t-b_s*b_r)*(b_t*b_r-b_s)"
                ),
                "coefficient_dictionary_equalities": True,
            }
        )
    return records


def mutation_tests(
    targets,
    descriptor,
    sparse_outputs,
    coordinate_index,
    lambda_zero_index,
    closed,
):
    mutations = []

    def rejected(name, condition):
        if not condition:
            raise AssertionError((name, "mutation unexpectedly accepted"))
        mutations.append({"name": name, "result": "REJECTED"})

    diagonal = extract_divided_minor(
        sparse_outputs,
        coordinate_index,
        0,
        (0, 1),
        (0, 1),
        lambda_zero_index,
    )
    reduced = diagonal["reduced"]
    rejected("omit_strict_one_minus_lambda_0_factor", reduced != closed["F"][0])

    lambda_zero = variable(closed["width"], lambda_zero_index)
    plus_factor = sparse_add((1, closed["one"]), (1, lambda_zero))
    rejected(
        "change_factor_to_one_plus_lambda_0",
        reduced != sparse_mul(plus_factor, closed["F"][0]),
    )

    # Rows (0,C), columns (0,G) transport to E_GC, not E_CG.
    cross = extract_divided_minor(
        sparse_outputs,
        coordinate_index,
        0,
        (0, 1),
        (0, 2),
        lambda_zero_index,
    )
    rejected("omit_cross_index_transpose", cross["quotient"] != closed["E"][0, 1])

    wrong_p = build_closed_form(descriptor, p_variable=0)
    rejected("use_lambda_0_as_p", wrong_p["F"][0] != closed["F"][0])

    wrong_b = build_closed_form(descriptor, b_edge=8)
    rejected("use_edge_8_for_b", wrong_b["F"][0] != closed["F"][0])

    wrong_block = extract_divided_minor(
        sparse_outputs,
        coordinate_index,
        1,
        (0, 1),
        (0, 1),
        lambda_zero_index,
    )
    rejected("use_character_sum_1", wrong_block["quotient"] != closed["F"][0])

    wrong_descriptor = targets[128]["descriptor"]
    wrong_outputs = audit.atlas.output_sparse_polynomials(wrong_descriptor)
    wrong_target = extract_divided_minor(
        wrong_outputs,
        coordinate_index,
        0,
        (0, 1),
        (0, 1),
        lambda_zero_index,
    )
    rejected(
        "use_neighbor_target_128",
        bool(wrong_target["remainder"])
        or wrong_target["quotient"] != closed["F"][0],
    )

    r, s, t = CYCLIC_CASES[0]
    b = closed["b"]
    d = closed["d"]
    F = closed["F"]
    E = closed["E"]
    K = closed["K"]
    L = closed["L"]
    M = closed["M"]
    C = sparse_add(
        (1, sparse_mul(d[r], d[r], M[s, t], M[t, s])),
        (-1, sparse_mul(b[s], b[t])),
    )
    incomplete = sparse_add(
        (1, sparse_mul(E[s, t], d[r], M[t, s])),
        (1, sparse_mul(d[s], d[t], K[s], L[t], E[t, s])),
        (-1, sparse_mul(b[s], F[t])),
        (-1, sparse_mul(b[t], F[s])),
    )
    rejected("omit_F_s_F_t_from_eliminant", incomplete != C)

    lhs = sparse_add(
        (1, sparse_mul(b[r], C)),
        (1, sparse_mul(b[s], b[t], F[r])),
    )
    wrong_factor_one = sparse_add(
        (1, b[t]), (1, sparse_mul(b[s], b[r]))
    )
    factor_two = sparse_add(
        (1, sparse_mul(b[t], b[r])), (-1, b[s])
    )
    wrong_rhs = sparse_mul(
        d[r],
        d[r],
        closed["p"],
        closed["q"],
        closed["a"][r],
        closed["c"][r],
        wrong_factor_one,
        factor_two,
    )
    rejected("plus_sign_in_ratio_factor", wrong_rhs != lhs)
    return mutations


def main():
    _, _, _, targets = audit.cross.build_universes()
    target = targets[TARGET_INDEX]
    descriptor = target["descriptor"]
    if target["record_id"] != 43:
        raise AssertionError(target["record_id"])
    sparse_outputs = audit.atlas.output_sparse_polynomials(descriptor)
    coordinate_index = {
        assignment: index
        for index, assignment in enumerate(audit.atlas.k3p_assignments(4))
    }
    lambda_zero_index = 3 * descriptor.edge_class_count
    closed = build_closed_form(descriptor)

    diagonals = []
    for s in range(3):
        character = s + 1
        row = extract_divided_minor(
            sparse_outputs,
            coordinate_index,
            0,
            (0, character),
            (0, character),
            lambda_zero_index,
        )
        if row["remainder"]:
            raise AssertionError((s, "nonzero diagonal division remainder"))
        if row["quotient"] != closed["F"][s]:
            raise AssertionError((s, "diagonal transport mismatch"))
        diagonals.append(
            {
                "sector": SECTOR_NAMES[s],
                "character_sum": 0,
                "rows": [0, character],
                "columns": [0, character],
                "coordinate_indices": list(row["coordinates"]),
                "full_minor": digest_record(row["full"]),
                "positive_monomial_exponent": list(row["positive_monomial"]),
                "after_monomial_removal": digest_record(row["reduced"]),
                "exact_divisor": "1-lambda_0",
                "division_remainder": digest_record(row["remainder"]),
                "quotient": digest_record(row["quotient"]),
                "quotient_formula": "F_s=b_s-d_s^2*K_s*L_s",
                "coefficient_dictionary_equalities": True,
            }
        )

    crosses = []
    for s in range(3):
        for t in range(3):
            if s == t:
                continue
            character_s = s + 1
            character_t = t + 1
            r = (character_s ^ character_t) - 1
            row = extract_divided_minor(
                sparse_outputs,
                coordinate_index,
                0,
                (0, character_s),
                (0, character_t),
                lambda_zero_index,
            )
            if row["remainder"]:
                raise AssertionError((s, t, "nonzero cross division remainder"))
            # The record-43 graph transport reverses the ordered E indices.
            if row["quotient"] != closed["E"][t, s]:
                raise AssertionError((s, t, "ordered cross transport mismatch"))
            crosses.append(
                {
                    "minor_row_sector_s": SECTOR_NAMES[s],
                    "minor_column_sector_t": SECTOR_NAMES[t],
                    "r_equals_s_xor_t": SECTOR_NAMES[r],
                    "transported_polynomial": f"E_{SECTOR_NAMES[t]}{SECTOR_NAMES[s]}",
                    "character_sum": 0,
                    "rows": [0, character_s],
                    "columns": [0, character_t],
                    "coordinate_indices": list(row["coordinates"]),
                    "full_minor": digest_record(row["full"]),
                    "positive_monomial_exponent": list(row["positive_monomial"]),
                    "after_monomial_removal": digest_record(row["reduced"]),
                    "exact_divisor": "1-lambda_0",
                    "division_remainder": digest_record(row["remainder"]),
                    "quotient": digest_record(row["quotient"]),
                    "quotient_formula": (
                        "E_ts=d_r*(p*b_t*a_r+(1-p)*b_s*c_r)"
                        "-d_t*d_s*K_t*L_s"
                    ),
                    "coefficient_dictionary_equalities": True,
                }
            )

    consequences = consequence_records(closed)
    mutations = mutation_tests(
        targets,
        descriptor,
        sparse_outputs,
        coordinate_index,
        lambda_zero_index,
        closed,
    )
    payload = {
        "schema": "k3p-record43-cyclic-transport-audit-v1",
        "status": "PASS",
        "target_index": TARGET_INDEX,
        "record_id": target["record_id"],
        "old_split": target["old_split"],
        "old_order": target["old_order"],
        "descriptor_sha256": audit.cross.digest(
            audit.cross.descriptor_payload(descriptor)
        ),
        "edge_signatures": [list(row) for row in descriptor.edge_signatures],
        "inputs": {
            "frozen_primitive_sha256": audit.sha_file(audit.cross.PRIMITIVE_PATH),
            "crossbridge_compiler_sha256": audit.sha_file(
                audit.PARENT / "explore_crossbridge_atlas.py"
            ),
            "k3p_compiler_sha256": audit.sha_file(audit.cross.ATLAS_PATH),
            "audit_script_sha256": audit.sha_file(Path(__file__).resolve()),
        },
        "transport": {
            "strict_common_factor": "1-lambda_0",
            "p": "lambda_1",
            "q": "1-lambda_1",
            "a_s": "edge-class 1 spectrum in sector s",
            "b_s": "edge-class 4 spectrum in sector s",
            "c_s": "edge-class 8 spectrum in sector s",
            "d_s": "edge-class 9 spectrum in sector s",
            "K_s": "p*a_s*b_s+(1-p)*c_s",
            "L_s": "p*a_s+(1-p)*b_s*c_s",
            "ordered_cross_index_action": (
                "minor with row sector s and column sector t has quotient E_ts"
            ),
        },
        "diagonal_minor_records": diagonals,
        "ordered_cross_minor_records": crosses,
        "consequence_records": consequences,
        "strict_domain_logic": {
            "first_division": (
                "The removed monomial is strictly positive because all edge "
                "spectra are positive."
            ),
            "second_division": (
                "The exact remainder on division by 1-lambda_0 is zero for "
                "all nine minors; 1-lambda_0 is strictly positive."
            ),
            "eliminant_prefactor": (
                "d_r^2*lambda_1*(1-lambda_1)*a_r*c_r is strictly positive."
            ),
            "ratio_consequence": (
                "For each r, joint vanishing forces b_r in "
                "{b_t/b_s,b_s/b_t}."
            ),
            "log_contradiction": (
                "B_s=-log(b_s)>0 would satisfy B_r=abs(B_t-B_s) for all "
                "r; the equation for a maximal B_r is impossible."
            ),
            "domain_scope": (
                "Only strict spectral bounds and strict inheritances from the "
                "true D3+ domain are used."
            ),
        },
        "flattening_conclusion": (
            "Rank at most four would force the four nonzero Fourier blocks to "
            "have rank one and hence force these nine minors to vanish.  The "
            "cyclic contradiction proves rank greater than four at every "
            "strict target-127 point."
        ),
        "mutation_tests": mutations,
    }
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "diagonal_transports": len(diagonals),
                "ordered_cross_transports": len(crosses),
                "cyclic_eliminants": len(consequences),
                "mutations_rejected": len(mutations),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
