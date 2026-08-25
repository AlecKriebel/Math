#!/usr/bin/env python3
"""Independent replay verifier for all exact single-minor sign witnesses."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from fractions import Fraction
from pathlib import Path

import certify_single_minor_sign_changes as certificate
import search_simplex_homogeneous as audit


REPORT_PATH = Path(__file__).resolve().parent / "VERIFICATION_REPORT.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify(payload):
    require(
        payload["schema"] == "k3p-d3plus-single-cut-minor-sign-change-witnesses-v1",
        "schema",
    )
    require(payload["status"] == "EXACT_COMPLETE", "status")
    require(payload["base_seed"] == certificate.BASE_SEED, "base seed")
    require(
        payload["inheritance_denominator"] == certificate.LAMBDA_DENOMINATOR,
        "inheritance denominator",
    )
    require(payload["weight_pool"] == list(map(int, certificate.WEIGHT_POOL)), "weight pool")
    require(
        payload["inputs"]["upstream_report_sha256"]
        == audit.sha_file(audit.UPSTREAM_REPORT),
        "upstream report hash",
    )
    require(
        payload["inputs"]["crossbridge_compiler_sha256"]
        == audit.sha_file(audit.PARENT / "explore_crossbridge_atlas.py"),
        "crossbridge compiler hash",
    )
    require(
        payload["inputs"]["k3p_compiler_sha256"]
        == audit.sha_file(audit.cross.ATLAS_PATH),
        "K3P compiler hash",
    )

    upstream = json.loads(audit.UPSTREAM_REPORT.read_text())
    unresolved = tuple(upstream["unsolved_target_indices"])
    require(payload["target_count"] == len(unresolved) == 24, "target count")
    require(payload["minor_count_per_target"] == 144, "minor count declaration")
    require(
        [record["target_index"] for record in payload["records"]] == list(unresolved),
        "target ordering",
    )

    _, _, _, targets = audit.cross.build_universes()
    coordinate_index = {
        assignment: index
        for index, assignment in enumerate(audit.atlas.k3p_assignments(4))
    }
    pairs = tuple(itertools.combinations(range(4), 2))
    verified_minors = 0
    verified_witnesses = 0
    for record in payload["records"]:
        target_index = record["target_index"]
        target = targets[target_index]
        descriptor = target["descriptor"]
        require(record["record_id"] == target["record_id"], "record id")
        require(record["old_split"] == target["old_split"], "old split")
        require(record["old_order"] == target["old_order"], "old order")
        require(
            record["descriptor_sha256"]
            == audit.cross.digest(audit.cross.descriptor_payload(descriptor)),
            "descriptor hash",
        )
        compiled = certificate.compile_minors(descriptor, coordinate_index, pairs)
        require(record["minor_count"] == len(compiled) == 144, "minor count")
        require(
            record["minors_with_exact_opposite_sign_witnesses"] == 144,
            "certified minor count",
        )

        sample_values = {}
        require(record["stored_sample_count"] == len(record["samples"]), "sample count")
        for sample_id, sample in record["samples"].items():
            weights = sample["edge_barycentric_integer_weights_O_C_G_T_U"]
            numerators = sample["inheritance_numerators"]
            require(
                sample["inheritance_denominator"] == certificate.LAMBDA_DENOMINATOR,
                "sample denominator",
            )
            require(len(weights) == descriptor.edge_class_count, "edge weight count")
            require(all(len(row) == 5 for row in weights), "edge weight width")
            require(all(int(value) > 0 for row in weights for value in row), "positive weights")
            require(len(numerators) == descriptor.retic_count, "inheritance count")
            require(
                all(0 < int(value) < certificate.LAMBDA_DENOMINATOR for value in numerators),
                "strict inheritance",
            )
            values = certificate.rational_values(weights, numerators)
            certificate.validate_strict_domain(
                values, descriptor.edge_class_count, descriptor.retic_count
            )
            sample_values[int(sample_id)] = values

        require(len(record["minors"]) == 144, "minor rows")
        for public, rebuilt in zip(record["minors"], compiled):
            require(public["character_sum"] == rebuilt["character_sum"], "character sum")
            require(public["rows"] == list(rebuilt["rows"]), "rows")
            require(public["columns"] == list(rebuilt["columns"]), "columns")
            require(
                public["coordinate_indices"] == list(rebuilt["coordinate_indices"]),
                "coordinate indices",
            )
            require(
                public["positive_monomial_exponent"] == list(rebuilt["common"]),
                "positive factor",
            )
            require(
                public["full_polynomial_sha256"]
                == audit.polynomial_digest(rebuilt["full"]),
                "full polynomial hash",
            )
            require(
                public["reduced_polynomial_sha256"]
                == audit.polynomial_digest(rebuilt["reduced"]),
                "reduced polynomial hash",
            )
            recomputed = []
            for expected_sign, key in ((-1, "negative_witness"), (1, "positive_witness")):
                witness = public[key]
                sample_id = witness["sample_id"]
                require(sample_id in sample_values, "witness sample id")
                values = sample_values[sample_id]
                reduced_value = certificate.exact_evaluate(rebuilt["reduced"], values)
                full_value = certificate.exact_evaluate(rebuilt["full"], values)
                require(
                    reduced_value == Fraction(witness["reduced_value"]),
                    "reduced witness value",
                )
                require(
                    full_value == Fraction(witness["full_minor_value"]),
                    "full witness value",
                )
                require(expected_sign * reduced_value > 0, "reduced witness sign")
                require(expected_sign * full_value > 0, "full witness sign")
                recomputed.append(full_value)
                verified_witnesses += 1
            require(recomputed[0] * recomputed[1] < 0, "opposite signs")
            verified_minors += 1

    require(
        verified_minors
        == payload["total_minors_with_opposite_sign_witnesses"]
        == 24 * 144,
        "global minor count",
    )
    require(verified_witnesses == 2 * verified_minors, "global witness count")
    return {
        "status": "PASS",
        "targets": len(unresolved),
        "minors": verified_minors,
        "exact_witness_values": verified_witnesses,
    }


def mutation_tests(payload):
    mutations = []

    def expect_failure(name, mutate):
        changed = copy.deepcopy(payload)
        mutate(changed)
        try:
            verify(changed)
        except Exception:
            mutations.append({"name": name, "result": "REJECTED"})
            return
        raise AssertionError((name, "mutation accepted"))

    expect_failure("schema", lambda row: row.__setitem__("schema", "bad"))
    expect_failure(
        "target_count", lambda row: row.__setitem__("target_count", row["target_count"] - 1)
    )
    expect_failure(
        "descriptor_hash",
        lambda row: row["records"][0].__setitem__("descriptor_sha256", "0" * 64),
    )
    first_sample = next(iter(payload["records"][0]["samples"]))
    expect_failure(
        "nonpositive_barycentric_weight",
        lambda row: row["records"][0]["samples"][first_sample][
            "edge_barycentric_integer_weights_O_C_G_T_U"
        ][0].__setitem__(0, 0),
    )
    expect_failure(
        "polynomial_hash",
        lambda row: row["records"][0]["minors"][0].__setitem__(
            "full_polynomial_sha256", "f" * 64
        ),
    )
    expect_failure(
        "coordinate_rows",
        lambda row: row["records"][0]["minors"][0].__setitem__("rows", [0, 2]),
    )
    expect_failure(
        "witness_value",
        lambda row: row["records"][0]["minors"][0]["negative_witness"].__setitem__(
            "full_minor_value", "1"
        ),
    )
    expect_failure(
        "witness_sample_id",
        lambda row: row["records"][0]["minors"][0]["positive_witness"].__setitem__(
            "sample_id", -1
        ),
    )
    return mutations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutations", action="store_true")
    args = parser.parse_args()
    payload = json.loads(certificate.OUTPUT.read_text())
    result = verify(payload)
    if args.mutations:
        mutations = mutation_tests(payload)
        result["mutations"] = mutations
        result["mutation_count"] = len(mutations)
    result["certificate_sha256"] = audit.sha_file(certificate.OUTPUT)
    result["verifier_sha256"] = audit.sha_file(Path(__file__).resolve())
    REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
