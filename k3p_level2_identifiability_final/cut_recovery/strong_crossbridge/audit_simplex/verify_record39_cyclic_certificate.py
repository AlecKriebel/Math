#!/usr/bin/env python3
"""Independent exact replay of the target-117 cyclic six-minor certificate."""

from __future__ import annotations

import json
from pathlib import Path

import construct_record39_six_diagonal_counterexample as diagonal_counterexample
import search_simplex_homogeneous as audit


HERE = Path(__file__).resolve().parent
REPORT = HERE / "RECORD39_CYCLIC_CERTIFICATE_AUDIT.json"
TARGET_INDEX = 117
CASES = (
    # sector coordinate, selected character index, H character sum
    (0, 1, 2),  # C
    (1, 2, 1),  # G
    (2, 3, 1),  # T
)
SECTOR_NAMES = ("C", "G", "T")


def sparse_add(left, right, right_multiplier=1):
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, 0) + right_multiplier * coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def variable(width, index):
    exponent = [0] * width
    exponent[index] = 1
    return {tuple(exponent): 1}


def monomial(width, assignments):
    exponent = [0] * width
    for index, power in assignments.items():
        exponent[index] = power
    return {tuple(exponent): 1}


def identity_data(descriptor, sparse_outputs, coordinate_index, sector, character, h_sum):
    width = 3 * descriptor.edge_class_count + descriptor.retic_count
    pair = (0, character)
    F_full, F_coordinates = audit.minor_polynomial(
        sparse_outputs, coordinate_index, 0, pair, pair
    )
    H_full, H_coordinates = audit.minor_polynomial(
        sparse_outputs, coordinate_index, h_sum, pair, pair
    )
    F_common, F = audit.factor_positive_monomial(F_full)
    H_common, H = audit.factor_positive_monomial(H_full)

    other_sectors = tuple(index for index in range(3) if index != sector)
    x_index = 3 * 8 + sector
    y_index = 3 * 8 + other_sectors[0]
    z_index = 3 * 8 + other_sectors[1]
    a_index = 3 * 1 + sector
    b_index = 3 * 4 + sector
    d_index = 3 * 6 + sector
    lambda_index = 3 * descriptor.edge_class_count + 1
    x = variable(width, x_index)
    y = variable(width, y_index)
    z = variable(width, z_index)
    lam = variable(width, lambda_index)
    one = {(0,) * width: 1}

    # lhs = y*z*F - x*H
    lhs = sparse_add(
        audit.sparse_mul(audit.sparse_mul(y, z), F),
        audit.sparse_mul(x, H),
        -1,
    )

    # Q = a*b*d^2*lambda*(1-lambda)
    Q = monomial(
        width,
        {
            a_index: 1,
            b_index: 1,
            d_index: 2,
            lambda_index: 1,
        },
    )
    Q = audit.sparse_mul(Q, sparse_add(one, lam, -1))
    factor_one = sparse_add(y, audit.sparse_mul(x, z), -1)
    factor_two = sparse_add(audit.sparse_mul(x, y), z, -1)
    rhs = audit.sparse_mul(Q, audit.sparse_mul(factor_one, factor_two))
    return {
        "holds": lhs == rhs,
        "F_full": F_full,
        "H_full": H_full,
        "F_reduced": F,
        "H_reduced": H,
        "F_common": F_common,
        "H_common": H_common,
        "F_coordinates": F_coordinates,
        "H_coordinates": H_coordinates,
        "lhs": lhs,
        "rhs": rhs,
        "indices": {
            "x": x_index,
            "y": y_index,
            "z": z_index,
            "a": a_index,
            "b": b_index,
            "d": d_index,
            "lambda": lambda_index,
        },
    }


def exact_counterexample_h_values(descriptor, sparse_outputs, coordinate_index):
    point = diagonal_counterexample.build_construction()
    values = tuple(value for edge in point["edges"] for value in edge) + point[
        "inheritances"
    ]
    rows = []
    for sector, character, h_sum in CASES:
        pair = (0, character)
        F, _ = audit.minor_polynomial(sparse_outputs, coordinate_index, 0, pair, pair)
        H, _ = audit.minor_polynomial(
            sparse_outputs, coordinate_index, h_sum, pair, pair
        )
        F_value = audit.evaluate_power_polynomial(F, values)
        H_value = audit.evaluate_power_polynomial(H, values)
        if F_value != 0 or H_value == 0:
            raise AssertionError((sector, F_value, H_value))
        rows.append(
            {
                "sector": SECTOR_NAMES[sector],
                "F_exact_value": str(F_value),
                "cyclic_H_exact_value": str(H_value),
                "cyclic_H_sign": 1 if H_value > 0 else -1,
            }
        )
    return rows


def main():
    _, _, _, targets = audit.cross.build_universes()
    target = targets[TARGET_INDEX]
    descriptor = target["descriptor"]
    sparse_outputs = audit.atlas.output_sparse_polynomials(descriptor)
    coordinate_index = {
        assignment: index
        for index, assignment in enumerate(audit.atlas.k3p_assignments(4))
    }

    records = []
    for sector, character, h_sum in CASES:
        data = identity_data(
            descriptor,
            sparse_outputs,
            coordinate_index,
            sector,
            character,
            h_sum,
        )
        if not data["holds"]:
            difference = sparse_add(data["lhs"], data["rhs"], -1)
            raise AssertionError((sector, difference))
        records.append(
            {
                "sector": SECTOR_NAMES[sector],
                "selected_character_index": character,
                "F_character_sum": 0,
                "H_character_sum": h_sum,
                "rows": [0, character],
                "columns": [0, character],
                "F_coordinate_indices": list(data["F_coordinates"]),
                "H_coordinate_indices": list(data["H_coordinates"]),
                "F_full_polynomial_sha256": audit.polynomial_digest(data["F_full"]),
                "H_full_polynomial_sha256": audit.polynomial_digest(data["H_full"]),
                "F_positive_monomial_exponent": list(data["F_common"]),
                "H_positive_monomial_exponent": list(data["H_common"]),
                "F_reduced_polynomial_sha256": audit.polynomial_digest(
                    data["F_reduced"]
                ),
                "H_reduced_polynomial_sha256": audit.polynomial_digest(
                    data["H_reduced"]
                ),
                "identity_polynomial_sha256": audit.polynomial_digest(data["lhs"]),
                "identity_term_count": len(data["lhs"]),
                "variable_parameter_indices": data["indices"],
                "exact_identity": (
                    "y*z*F - x*H = a*b*d^2*lambda*(1-lambda)"
                    "*(y-x*z)*(x*y-z)"
                ),
                "coefficient_dictionary_equality": True,
            }
        )

    # Audit all H sums.  The two character sums outside {0, selected character}
    # give the same reduced H identity (the y,z roles are symmetric).  The two
    # excluded sums must fail the exact coefficient comparison.
    mutations = []
    equivalent_transports = []
    for sector, character, correct_sum in CASES:
        for wrong_sum in range(4):
            if wrong_sum == correct_sum:
                continue
            changed = identity_data(
                descriptor,
                sparse_outputs,
                coordinate_index,
                sector,
                character,
                wrong_sum,
            )
            if wrong_sum not in (0, character):
                if not changed["holds"]:
                    raise AssertionError(
                        (sector, wrong_sum, "equivalent H transport rejected")
                    )
                equivalent_transports.append(
                    {
                        "sector": SECTOR_NAMES[sector],
                        "selected_H_sum": correct_sum,
                        "equivalent_H_sum": wrong_sum,
                        "result": "EXACT_IDENTITY_ALSO_HOLDS",
                    }
                )
            else:
                if changed["holds"]:
                    raise AssertionError((sector, wrong_sum, "invalid H sum accepted"))
                mutations.append(
                    {
                        "name": f"{SECTOR_NAMES[sector]}_H_sum_{wrong_sum}",
                        "result": "REJECTED",
                    }
                )

    counterexample_values = exact_counterexample_h_values(
        descriptor, sparse_outputs, coordinate_index
    )
    payload = {
        "schema": "k3p-record39-cyclic-six-minor-audit-v1",
        "status": "PASS",
        "target_index": TARGET_INDEX,
        "record_id": target["record_id"],
        "descriptor_sha256": audit.cross.digest(
            audit.cross.descriptor_payload(descriptor)
        ),
        "inputs": {
            "crossbridge_compiler_sha256": audit.sha_file(
                audit.PARENT / "explore_crossbridge_atlas.py"
            ),
            "k3p_compiler_sha256": audit.sha_file(audit.cross.ATLAS_PATH),
            "audit_script_sha256": audit.sha_file(Path(__file__).resolve()),
        },
        "identity_records": records,
        "Q_sign": (
            "a,b,d,lambda,1-lambda are strictly positive, so "
            "Q=a*b*d^2*lambda*(1-lambda)>0"
        ),
        "vanishing_consequence": (
            "F=H=0 implies y=x*z or z=x*y in each cyclic sector"
        ),
        "open_cube_contradiction": (
            "For 0<x,y,z<1, the three cyclic consequences say each negative "
            "log is the absolute difference of the other two. Ordering the "
            "three positive logs makes the largest equal to a smaller "
            "difference, a contradiction."
        ),
        "nearby_H_sum_mutations": mutations,
        "mutation_count": len(mutations),
        "equivalent_H_sum_transports": equivalent_transports,
        "prior_diagonal_counterexample_clarification": {
            "statement": (
                "The earlier rational point vanishes F_s and the three mixed "
                "principal minors in character sum 0, not these cyclic H_s."
            ),
            "exact_values": counterexample_values,
        },
    }
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "identities": len(records),
                "mutations_rejected": len(mutations),
                "prior_counterexample_cyclic_H_nonzero": len(counterexample_values),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
