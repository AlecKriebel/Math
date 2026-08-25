#!/usr/bin/env python3
"""Exact rational counterexample to the six-diagonal-equation shortcut.

The point constructed here is strict D3+ on every edge and strict in both
inheritance variables.  All six principal 2x2 minors of the zero-character
Fourier block vanish exactly, while every full Fourier block has exact rank 4.
Thus these six necessary equations alone cannot prove cross-bridge exclusion.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import search_simplex_homogeneous as audit


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "RECORD39_SIX_DIAGONAL_COUNTEREXAMPLE.json"
TARGET_INDEX = 117
LABELS = ("C", "G", "T")


def strings(values):
    return [str(value) for value in values]


def d3_margins(triple):
    c, g, t = triple
    return {
        "c": c,
        "g": g,
        "t": t,
        "1-c": 1 - c,
        "1-g": 1 - g,
        "1-t": 1 - t,
        "1+c-g-t": 1 + c - g - t,
        "1-c+g-t": 1 - c + g - t,
        "1-c-g+t": 1 - c - g + t,
    }


def require_strict_d3(triple):
    margins = d3_margins(triple)
    if not all(value > 0 for value in margins.values()):
        raise AssertionError(margins)
    return margins


def exact_rank(matrix):
    work = [list(map(Fraction, row)) for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (candidate for candidate in range(row, len(work)) if work[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for other in range(len(work)):
            if other == row or not work[other][column]:
                continue
            multiplier = work[other][column]
            work[other] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[other], work[row])
            ]
        row += 1
    return row


def polynomial_value(polynomial, parameter_values):
    return audit.evaluate_power_polynomial(polynomial, parameter_values)


def build_construction():
    # Rational V,W were chosen near a numerical interior feasibility point.
    # Defining Y=V*W and solving the two linear equations
    # V=p+qY, W=q+pY makes the three within-sector identities exact.
    V = (
        Fraction(6_851_344, 10**9),
        Fraction(322_457_578, 10**9),
        Fraction(112_044_789, 10**9),
    )
    W = (
        Fraction(320_088_296, 10**9),
        Fraction(289_898_938, 10**9),
        Fraction(18_321_614, 10**9),
    )
    Y = tuple(V[index] * W[index] for index in range(3))
    p = tuple(
        (V[index] - Y[index] * W[index]) / (1 - Y[index] ** 2)
        for index in range(3)
    )
    q = tuple(
        (W[index] - Y[index] * V[index]) / (1 - Y[index] ** 2)
        for index in range(3)
    )
    if any(V[i] != p[i] + q[i] * Y[i] for i in range(3)):
        raise AssertionError("V identity")
    if any(W[i] != q[i] + p[i] * Y[i] for i in range(3)):
        raise AssertionError("W identity")

    # For distinct nonzero characters i,j,k=i xor j, define the endpoint
    # deviation d_ij=T_ij/(W_i V_j)-1.
    deviation = {}
    for i, j in itertools.combinations(range(3), 2):
        k = 3 - i - j
        deviation[i, j] = (
            (q[k] * Y[j] + p[k] * Y[i]) / (W[i] * V[j]) - 1
        )
        deviation[j, i] = (
            (q[k] * Y[i] + p[k] * Y[j]) / (W[j] * V[i]) - 1
        )

    # The nonzero solution of
    # (1+theta_i d_ij)(1+theta_j d_ji)=1 for all three pairs.
    a = deviation[0, 1]
    b = deviation[1, 0]
    c = deviation[0, 2]
    d = deviation[2, 0]
    e = deviation[1, 2]
    f = deviation[2, 1]
    numerator = a * d * e + b * c * f
    theta = (
        -numerator / (a * c * (b * f + d * e - e * f)),
        -numerator / (b * e * (a * d - c * d + c * f)),
        numerator / (d * f * (a * b - a * e - b * c)),
    )
    if not all(0 < value < 1 for value in theta):
        raise AssertionError(theta)
    for i, j in itertools.combinations(range(3), 2):
        equation = (1 + theta[i] * deviation[i, j]) * (
            1 + theta[j] * deviation[j, i]
        )
        if equation != 1:
            raise AssertionError((i, j, equation))

    # Realize p=lambda_1 B*X and q=(1-lambda_1)B*A with rational D3+ triples.
    B = (Fraction(49, 50), Fraction(197, 200), Fraction(49, 50))
    lambda_1 = Fraction(5, 12)
    X = tuple(p[i] / (lambda_1 * B[i]) for i in range(3))
    A = tuple(q[i] / ((1 - lambda_1) * B[i]) for i in range(3))
    if any(p[i] != lambda_1 * B[i] * X[i] for i in range(3)):
        raise AssertionError("p decomposition")
    if any(q[i] != (1 - lambda_1) * B[i] * A[i] for i in range(3)):
        raise AssertionError("q decomposition")

    # Realize theta with the remaining three relevant edge triples.  Taking
    # P=R=(1/2,1/2,1/2), t=lambda_0/(1-lambda_0)=1/10 and
    # Q_i=t P_i R_i/K_i is an exact solution, where
    # K_i=theta_i/((1-theta_i)W_i).
    isotropic = (Fraction(1, 2),) * 3
    t_ratio = Fraction(1, 10)
    lambda_0 = t_ratio / (1 + t_ratio)
    K = tuple(theta[i] / ((1 - theta[i]) * W[i]) for i in range(3))
    Q = tuple(t_ratio * isotropic[i] ** 2 / K[i] for i in range(3))
    for i in range(3):
        realized = (
            lambda_0 * isotropic[i] ** 2 * W[i]
            / ((1 - lambda_0) * Q[i] + lambda_0 * isotropic[i] ** 2 * W[i])
        )
        if realized != theta[i]:
            raise AssertionError((i, realized, theta[i]))

    # Edge names follow the target-117 descriptor signatures.  Edges 3,5,7,10
    # factor from these six minors and are assigned a strict isotropic point.
    edges = (
        isotropic,  # 0 = P
        X,          # 1 = X
        Q,          # 2 = Q
        isotropic,  # 3
        A,          # 4 = A
        isotropic,  # 5
        B,          # 6 = B
        isotropic,  # 7
        Y,          # 8 = Y
        isotropic,  # 9 = R
        isotropic,  # 10
    )
    domain_rows = []
    for edge_index, triple in enumerate(edges):
        margins = require_strict_d3(triple)
        domain_rows.append(
            {
                "edge": edge_index,
                "triple": strings(triple),
                "margins": {key: str(value) for key, value in margins.items()},
                "minimum_margin": str(min(margins.values())),
            }
        )
    if not (0 < lambda_0 < 1 and 0 < lambda_1 < 1):
        raise AssertionError("inheritance")
    return {
        "V": V,
        "W": W,
        "Y": Y,
        "p": p,
        "q": q,
        "deviation": deviation,
        "theta": theta,
        "K": K,
        "edges": edges,
        "inheritances": (lambda_0, lambda_1),
        "domain_rows": domain_rows,
    }


def build_payload():
    construction = build_construction()
    _, _, _, targets = audit.cross.build_universes()
    target = targets[TARGET_INDEX]
    descriptor = target["descriptor"]
    assignments = audit.atlas.k3p_assignments(4)
    coordinate_index = {
        assignment: index for index, assignment in enumerate(assignments)
    }
    outputs = audit.atlas.eval_descriptor(
        descriptor, construction["edges"], construction["inheritances"]
    )
    sparse_outputs = audit.atlas.output_sparse_polynomials(descriptor)
    parameter_values = tuple(
        value for triple in construction["edges"] for value in triple
    ) + construction["inheritances"]

    principal_minors = []
    for rows in itertools.combinations(range(4), 2):
        polynomial, coordinates = audit.minor_polynomial(
            sparse_outputs, coordinate_index, 0, rows, rows
        )
        value = polynomial_value(polynomial, parameter_values)
        if value != 0:
            raise AssertionError((rows, value))
        principal_minors.append(
            {
                "character_sum": 0,
                "rows": list(rows),
                "columns": list(rows),
                "coordinate_indices": list(coordinates),
                "polynomial_sha256": audit.polynomial_digest(polynomial),
                "exact_value": "0",
            }
        )

    block_ranks = []
    for character_sum in range(4):
        matrix = [
            [
                outputs[
                    coordinate_index[
                        (row, character_sum ^ row, column, character_sum ^ column)
                    ]
                ]
                for column in range(4)
            ]
            for row in range(4)
        ]
        block_ranks.append(exact_rank(matrix))
    if block_ranks != [4, 4, 4, 4]:
        raise AssertionError(block_ranks)

    witness_rows = (0, 1)
    witness_columns = (0, 2)
    witness_polynomial, witness_coordinates = audit.minor_polynomial(
        sparse_outputs,
        coordinate_index,
        0,
        witness_rows,
        witness_columns,
    )
    witness_value = polynomial_value(witness_polynomial, parameter_values)
    if not witness_value:
        raise AssertionError("nonprincipal witness")

    deviation_payload = {
        f"{LABELS[i]}->{LABELS[j]}": str(value)
        for (i, j), value in sorted(construction["deviation"].items())
    }
    return {
        "schema": "k3p-record39-six-diagonal-counterexample-v1",
        "status": "EXACT_RATIONAL_COUNTEREXAMPLE",
        "claim_refuted": (
            "the six principal 2x2 minors of the zero-character block alone "
            "are infeasible in the strict K3P principal domain"
        ),
        "scope_warning": (
            "All four blocks have rank 4 at this point.  This is not a "
            "counterexample to full pointwise cut recovery."
        ),
        "target_index": TARGET_INDEX,
        "record_id": target["record_id"],
        "old_split": target["old_split"],
        "old_order": target["old_order"],
        "descriptor_sha256": audit.cross.digest(
            audit.cross.descriptor_payload(descriptor)
        ),
        "inputs": {
            "crossbridge_compiler_sha256": audit.sha_file(
                audit.PARENT / "explore_crossbridge_atlas.py"
            ),
            "k3p_compiler_sha256": audit.sha_file(audit.cross.ATLAS_PATH),
        },
        "derivation": {
            "V": strings(construction["V"]),
            "W": strings(construction["W"]),
            "Y_equals_V_times_W": strings(construction["Y"]),
            "p": strings(construction["p"]),
            "q": strings(construction["q"]),
            "deviation_d_ij": deviation_payload,
            "theta": strings(construction["theta"]),
            "K": strings(construction["K"]),
            "identities": [
                "V_s=p_s+q_s Y_s",
                "W_s=q_s+p_s Y_s",
                "Y_s=V_s W_s",
                "(1+theta_i d_ij)(1+theta_j d_ji)=1",
            ],
        },
        "edge_domain": construction["domain_rows"],
        "inheritances": {
            "lambda_0": str(construction["inheritances"][0]),
            "lambda_1": str(construction["inheritances"][1]),
        },
        "six_principal_minors": principal_minors,
        "exact_fourier_block_ranks": block_ranks,
        "nonprincipal_nonzero_witness": {
            "character_sum": 0,
            "rows": list(witness_rows),
            "columns": list(witness_columns),
            "coordinate_indices": list(witness_coordinates),
            "polynomial_sha256": audit.polynomial_digest(witness_polynomial),
            "exact_value": str(witness_value),
            "sign": 1 if witness_value > 0 else -1,
        },
    }


def main():
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "target_index": payload["target_index"],
                "principal_minors": len(payload["six_principal_minors"]),
                "block_ranks": payload["exact_fourier_block_ranks"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
