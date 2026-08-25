#!/usr/bin/env python3
"""Independent exact replay of the record-39 six-equation counterexample."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from fractions import Fraction
from pathlib import Path

import construct_record39_six_diagonal_counterexample as construction
import search_simplex_homogeneous as audit


REPORT = Path(__file__).resolve().parent / "RECORD39_SIX_DIAGONAL_VERIFICATION.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def parse_vector(values):
    return tuple(Fraction(value) for value in values)


def verify(payload):
    require(payload["schema"] == "k3p-record39-six-diagonal-counterexample-v1", "schema")
    require(payload["status"] == "EXACT_RATIONAL_COUNTEREXAMPLE", "status")
    require(payload["target_index"] == construction.TARGET_INDEX == 117, "target")
    require(
        payload["inputs"]["crossbridge_compiler_sha256"]
        == audit.sha_file(audit.PARENT / "explore_crossbridge_atlas.py"),
        "crossbridge input hash",
    )
    require(
        payload["inputs"]["k3p_compiler_sha256"]
        == audit.sha_file(audit.cross.ATLAS_PATH),
        "K3P input hash",
    )
    _, _, _, targets = audit.cross.build_universes()
    target = targets[construction.TARGET_INDEX]
    descriptor = target["descriptor"]
    require(payload["record_id"] == target["record_id"] == 39, "record id")
    require(payload["old_split"] == target["old_split"], "old split")
    require(payload["old_order"] == target["old_order"], "old order")
    require(
        payload["descriptor_sha256"]
        == audit.cross.digest(audit.cross.descriptor_payload(descriptor)),
        "descriptor hash",
    )

    edge_rows = payload["edge_domain"]
    require([row["edge"] for row in edge_rows] == list(range(11)), "edge ordering")
    edges = []
    minimum_margin = None
    for row in edge_rows:
        triple = parse_vector(row["triple"])
        margins = construction.d3_margins(triple)
        require(all(value > 0 for value in margins.values()), "strict D3+")
        require(
            row["margins"] == {key: str(value) for key, value in margins.items()},
            "stored margins",
        )
        require(row["minimum_margin"] == str(min(margins.values())), "minimum margin")
        minimum_margin = (
            min(margins.values())
            if minimum_margin is None
            else min(minimum_margin, *margins.values())
        )
        edges.append(triple)
    inheritances = (
        Fraction(payload["inheritances"]["lambda_0"]),
        Fraction(payload["inheritances"]["lambda_1"]),
    )
    require(all(0 < value < 1 for value in inheritances), "strict inheritances")

    # Replay the derivation identities without calling the constructor.
    derivation = payload["derivation"]
    V = parse_vector(derivation["V"])
    W = parse_vector(derivation["W"])
    Y = parse_vector(derivation["Y_equals_V_times_W"])
    p = parse_vector(derivation["p"])
    q = parse_vector(derivation["q"])
    theta = parse_vector(derivation["theta"])
    K = parse_vector(derivation["K"])
    require(Y == tuple(V[i] * W[i] for i in range(3)), "Y=VW")
    require(V == tuple(p[i] + q[i] * Y[i] for i in range(3)), "V identity")
    require(W == tuple(q[i] + p[i] * Y[i] for i in range(3)), "W identity")
    require(Y == edges[8], "Y edge binding")
    lambda_0, lambda_1 = inheritances
    require(
        p == tuple(lambda_1 * edges[6][i] * edges[1][i] for i in range(3)),
        "p edge binding",
    )
    require(
        q
        == tuple((1 - lambda_1) * edges[6][i] * edges[4][i] for i in range(3)),
        "q edge binding",
    )

    deviation = {}
    for i, j in itertools.combinations(range(3), 2):
        k = 3 - i - j
        deviation[i, j] = (
            (q[k] * Y[j] + p[k] * Y[i]) / (W[i] * V[j]) - 1
        )
        deviation[j, i] = (
            (q[k] * Y[i] + p[k] * Y[j]) / (W[j] * V[i]) - 1
        )
    expected_deviation = {
        f"{construction.LABELS[i]}->{construction.LABELS[j]}": str(value)
        for (i, j), value in sorted(deviation.items())
    }
    require(derivation["deviation_d_ij"] == expected_deviation, "deviations")
    require(all(0 < value < 1 for value in theta), "theta interior")
    require(K == tuple(theta[i] / ((1 - theta[i]) * W[i]) for i in range(3)), "K")
    for i, j in itertools.combinations(range(3), 2):
        require(
            (1 + theta[i] * deviation[i, j])
            * (1 + theta[j] * deviation[j, i])
            == 1,
            "mixed identity",
        )
    for i in range(3):
        realized = (
            lambda_0 * edges[0][i] * edges[9][i] * W[i]
            / (
                (1 - lambda_0) * edges[2][i]
                + lambda_0 * edges[0][i] * edges[9][i] * W[i]
            )
        )
        require(realized == theta[i], "theta edge realization")

    assignments = audit.atlas.k3p_assignments(4)
    coordinate_index = {
        assignment: index for index, assignment in enumerate(assignments)
    }
    sparse_outputs = audit.atlas.output_sparse_polynomials(descriptor)
    parameter_values = tuple(value for triple in edges for value in triple) + inheritances
    require(len(payload["six_principal_minors"]) == 6, "six rows")
    for public, rows in zip(
        payload["six_principal_minors"], itertools.combinations(range(4), 2)
    ):
        polynomial, coordinates = audit.minor_polynomial(
            sparse_outputs, coordinate_index, 0, rows, rows
        )
        require(public["character_sum"] == 0, "principal character sum")
        require(public["rows"] == list(rows) == public["columns"], "principal indices")
        require(public["coordinate_indices"] == list(coordinates), "principal coordinates")
        require(
            public["polynomial_sha256"] == audit.polynomial_digest(polynomial),
            "principal polynomial hash",
        )
        value = audit.evaluate_power_polynomial(polynomial, parameter_values)
        require(value == 0 and public["exact_value"] == "0", "principal exact zero")

    outputs = audit.atlas.eval_descriptor(descriptor, edges, inheritances)
    ranks = []
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
        ranks.append(construction.exact_rank(matrix))
    require(ranks == payload["exact_fourier_block_ranks"] == [4, 4, 4, 4], "block ranks")

    witness = payload["nonprincipal_nonzero_witness"]
    witness_polynomial, witness_coordinates = audit.minor_polynomial(
        sparse_outputs,
        coordinate_index,
        witness["character_sum"],
        tuple(witness["rows"]),
        tuple(witness["columns"]),
    )
    require(witness["coordinate_indices"] == list(witness_coordinates), "witness coordinates")
    require(
        witness["polynomial_sha256"] == audit.polynomial_digest(witness_polynomial),
        "witness polynomial hash",
    )
    witness_value = audit.evaluate_power_polynomial(witness_polynomial, parameter_values)
    require(witness_value == Fraction(witness["exact_value"]), "witness exact value")
    require(witness_value != 0, "witness nonzero")
    require(witness["sign"] == (1 if witness_value > 0 else -1), "witness sign")
    return {
        "status": "PASS",
        "target_index": construction.TARGET_INDEX,
        "strict_edges": len(edges),
        "minimum_exact_domain_margin": str(minimum_margin),
        "zero_principal_minors": 6,
        "block_ranks": ranks,
    }


def mutation_tests(payload):
    results = []

    def rejected(name, mutate):
        changed = copy.deepcopy(payload)
        mutate(changed)
        try:
            verify(changed)
        except Exception:
            results.append({"name": name, "result": "REJECTED"})
            return
        raise AssertionError((name, "accepted"))

    rejected("schema", lambda row: row.__setitem__("schema", "bad"))
    rejected(
        "descriptor_hash", lambda row: row.__setitem__("descriptor_sha256", "0" * 64)
    )
    rejected(
        "edge_value",
        lambda row: row["edge_domain"][0]["triple"].__setitem__(0, "0"),
    )
    rejected(
        "inheritance_boundary",
        lambda row: row["inheritances"].__setitem__("lambda_0", "0"),
    )
    rejected(
        "derivation_theta",
        lambda row: row["derivation"]["theta"].__setitem__(0, "1/2"),
    )
    rejected(
        "principal_hash",
        lambda row: row["six_principal_minors"][0].__setitem__(
            "polynomial_sha256", "f" * 64
        ),
    )
    rejected(
        "rank_claim",
        lambda row: row["exact_fourier_block_ranks"].__setitem__(0, 1),
    )
    rejected(
        "nonprincipal_value",
        lambda row: row["nonprincipal_nonzero_witness"].__setitem__(
            "exact_value", "0"
        ),
    )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutations", action="store_true")
    args = parser.parse_args()
    payload = json.loads(construction.OUTPUT.read_text())
    result = verify(payload)
    if args.mutations:
        result["mutations"] = mutation_tests(payload)
        result["mutation_count"] = len(result["mutations"])
    result["certificate_sha256"] = audit.sha_file(construction.OUTPUT)
    result["verifier_sha256"] = audit.sha_file(Path(__file__).resolve())
    REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
