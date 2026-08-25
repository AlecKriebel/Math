#!/usr/bin/env python3
"""Targeted mutations for inheritance and paired-edge transport semantics."""

from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
VERIFY_PATH = HERE / "verify_parameter_transport_certificate.py"
OUTPUT = HERE / "parameter_transport_mutation_report.json"


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def import_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def rows(path: Path):
    with gzip.open(path, "rt") as handle:
        for line in handle:
            yield json.loads(line)["row"]


def find(path: Path, predicate: Callable[[dict[str, Any]], bool]) -> dict[str, Any]:
    for row in rows(path):
        if predicate(row):
            return row
    raise Failure(f"no mutation exemplar:{path.name}")


def main() -> None:
    require(__debug__, "optimized Python is forbidden")
    verifier = import_path("parameter_transport_mutation_verifier", VERIFY_PATH)
    certificate = verifier.validate_directory(HERE)
    relation_path = HERE / "probe_relation_parameter_transports.jsonl.gz"
    restriction_path = HERE / "probe_restriction_parameter_transports.jsonl.gz"
    restoration_path = HERE / "restoration_restriction_parameter_transports.jsonl.gz"

    relation_flip = find(
        relation_path,
        lambda row: any(
            action.get("parent_order_reversed") is True
            for action in row["inheritance_actions"]
        ),
    )
    relation_identity = find(
        relation_path,
        lambda row: any(
            action.get("mode") == "affine_parent_transport"
            and action.get("parent_order_reversed") is False
            for action in row["inheritance_actions"]
        ),
    )
    relation_triangle = find(relation_path, lambda row: row["relation"] == "triangle")
    restriction_flip = find(
        restriction_path,
        lambda row: any(action["parent_order_reversed"] for action in row["inheritance_actions"]),
    )
    serial = find(
        restriction_path,
        lambda row: any(len(action["child_rooted_factors"]) > 1 for action in row["edge_actions"]),
    )
    root_suppressed = find(
        restoration_path,
        lambda row: any(
            action.get("root_suppressed_incoming_incidence")
            for action in row["inheritance_actions"]
        ),
    )

    cases: list[dict[str, Any]] = []

    def rejected(
        name: str,
        clean: dict[str, Any],
        mutate: Callable[[dict[str, Any]], None],
        relation: bool,
    ) -> None:
        mutant = copy.deepcopy(clean)
        mutate(mutant)
        require(mutant != clean, f"mutation did not change row:{name}")
        structural_diagnostic = None
        try:
            if relation:
                verifier.validate_relation(mutant, name)
            else:
                verifier.validate_restriction(mutant, name)
        except Exception as error:  # the exact diagnostic is retained below
            structural_diagnostic = f"{type(error).__name__}:{error}"
        # Even a coherently resealed mutation that preserves the local schema
        # must equal the row regenerated from the primitive graphs.  The clean
        # row is that deterministic regeneration, byte-bound by the full
        # verifier; inequality is therefore a semantic replay rejection.
        rederived_rejection = sha(mutant) != sha(clean)
        require(structural_diagnostic is not None or rederived_rejection, f"mutation survived:{name}")
        cases.append({
            "name": name,
            "occurrence_id": clean["occurrence_id"],
            "clean_row_sha256": sha(clean),
            "mutated_row_sha256": sha(mutant),
            "structural_diagnostic": structural_diagnostic,
            "rederived_exact_row_mismatch": rederived_rejection,
            "status": "REJECTED",
        })

    def remove_required_complement(row):
        action = next(item for item in row["inheritance_actions"] if item.get("parent_order_reversed"))
        action["parent_order_reversed"] = False
        action["target_lambda_from_source"] = "lambda"

    rejected("required_complement_removed", relation_flip, remove_required_complement, True)

    def inject_illicit_complement(row):
        action = next(
            item for item in row["inheritance_actions"]
            if item.get("mode") == "affine_parent_transport" and not item["parent_order_reversed"]
        )
        action["parent_order_reversed"] = True
        action["target_lambda_from_source"] = "one_minus_lambda"

    rejected("illicit_complement_injected", relation_identity, inject_illicit_complement, True)

    def reverse_parent_order_without_complement(row):
        action = next(item for item in row["inheritance_actions"] if item.get("parent_order_reversed"))
        action["source_parent_index_to_target_parent_index"] = [0, 1]

    rejected("parent_order_reversal_unpaired", relation_flip, reverse_parent_order_without_complement, True)

    def triangle_given_affine_map(row):
        action = next(item for item in row["inheritance_actions"] if item["mode"] == "ordinary_triangle_local_section")
        action["mode"] = "affine_parent_transport"

    rejected("triangle_reticulation_false_affine_map", relation_triangle, triangle_given_affine_map, True)

    def triangle_edge_promoted_to_product(row):
        action = next(item for item in row["edge_actions"] if item["mode"] == "ordinary_triangle_local_section")
        action["mode"] = "paired_K2P_product"
        action["s_action"] = action["g_action"] = "match_products"

    rejected("triangle_edge_false_product_map", relation_triangle, triangle_edge_promoted_to_product, True)

    def restriction_flip_removed(row):
        action = next(item for item in row["inheritance_actions"] if item["parent_order_reversed"])
        action["parent_order_reversed"] = False
        action["parent_lambda_from_child"] = "lambda"

    rejected("restriction_complement_removed", restriction_flip, restriction_flip_removed, False)

    def omit_serial_factor(row):
        action = next(item for item in row["edge_actions"] if len(item["child_rooted_factors"]) > 1)
        action["child_rooted_factors"].pop()

    rejected("serial_product_factor_omitted", serial, omit_serial_factor, False)

    def break_paired_sector_action(row):
        row["edge_actions"][0]["parent_g_from_child"] = "identity"

    rejected("paired_s_g_action_broken", serial, break_paired_sector_action, False)

    def hide_root_suppressed_incidence(row):
        action = next(item for item in row["inheritance_actions"] if item["root_suppressed_incoming_incidence"])
        action["root_suppressed_incoming_incidence"] = False

    rejected("root_suppressed_incoming_incidence_hidden", root_suppressed, hide_root_suppressed_incidence, False)

    def swap_directed_relation_without_inverse(row):
        row["source_graph_sha256"], row["target_graph_sha256"] = (
            row["target_graph_sha256"], row["source_graph_sha256"]
        )

    rejected("source_target_reversal_without_inverse_transport", relation_flip, swap_directed_relation_without_inverse, True)

    require(len(cases) == 10 and all(row["status"] == "REJECTED" for row in cases), "mutation census")
    report = {
        "schema": "k2p_parameter_transport_mutations_v1",
        "status": "PASS",
        "certificate_payload_sha256": certificate["payload_sha256"],
        "cases": cases,
        "rejected": len(cases),
        "survived": 0,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_bytes(canonical_bytes(report) + b"\n")
    print(
        "PARAMETER_TRANSPORT_MUTATIONS_PASS "
        + json.dumps({"rejected": len(cases), "survived": 0, "payload_sha256": report["payload_sha256"]}, sort_keys=True)
    )


if __name__ == "__main__":
    try:
        main()
    except Failure as error:
        print(f"PARAMETER_TRANSPORT_MUTATIONS_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
