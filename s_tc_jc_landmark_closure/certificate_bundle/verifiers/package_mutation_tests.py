#!/usr/bin/env python3
"""Semantic mutation tests for the curated record-level evidence map."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import evidence_bindings


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "verifiers/verify_certificate_bundle.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("bundle_integrity", VERIFY_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rebind(row: dict) -> None:
    row.pop("evidence_binding_sha256", None)
    row["evidence_binding_sha256"] = evidence_bindings.stable_hash(row)


def expect_rejection(name: str, rows: list[dict], expected: list[dict]) -> None:
    try:
        evidence_bindings.assert_rows_equal(rows, expected)
    except AssertionError:
        return
    raise AssertionError(f"semantic mutation was not rejected: {name}")


def pick(rows: list[dict], predicate, count: int = 1) -> list[int]:
    found = [index for index, row in enumerate(rows) if predicate(row)]
    if len(found) < count:
        raise AssertionError(("mutation fixture absent", count, len(found)))
    return found[:count]


def mutated(expected: list[dict], action) -> list[dict]:
    rows = copy.deepcopy(expected)
    action(rows)
    return rows


def main() -> None:
    verifier = load_verifier()
    path = ROOT / "atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz"
    frozen = evidence_bindings.read_rows(path)
    expected = evidence_bindings.reconstruct_rows(ROOT)
    evidence_bindings.assert_rows_equal(frozen, expected)
    mutations = 0

    expect_rejection("delete_decorated_relation", frozen[:-1], expected); mutations += 1
    expect_rejection("duplicate_decorated_relation", [*frozen, copy.deepcopy(frozen[-1])], expected); mutations += 1

    def swap_relation_ids(rows):
        rows[0]["relation_id"], rows[1]["relation_id"] = rows[1]["relation_id"], rows[0]["relation_id"]
        rebind(rows[0]); rebind(rows[1])
    expect_rejection("swap_valid_relation_ids", mutated(expected, swap_relation_ids), expected); mutations += 1

    distinct_i = pick(
        expected,
        lambda row: row["source_graph_id"] != row["target_graph_id"],
    )[0]
    def reverse_source_target(rows):
        rows[distinct_i]["source_graph_id"], rows[distinct_i]["target_graph_id"] = (
            rows[distinct_i]["target_graph_id"], rows[distinct_i]["source_graph_id"]
        )
        rebind(rows[distinct_i])
    expect_rejection("reverse_source_target_graphs", mutated(expected, reverse_source_target), expected); mutations += 1

    def reverse_direction(rows):
        rows[0]["direction"] = "target_precedes_source"; rebind(rows[0])
    expect_rejection("reverse_relation_direction", mutated(expected, reverse_direction), expected); mutations += 1

    strict_indices = pick(expected, lambda row: row["universe"] == "three_outgoing" and row["disposition"] == "strict_open_cube_separation", 2)
    def swap_strict_witnesses(rows):
        i, j = strict_indices
        rows[i]["evidence"]["strict_witness"], rows[j]["evidence"]["strict_witness"] = rows[j]["evidence"]["strict_witness"], rows[i]["evidence"]["strict_witness"]
        rebind(rows[i]); rebind(rows[j])
    expect_rejection("swap_valid_polynomial_certificates", mutated(expected, swap_strict_witnesses), expected); mutations += 1

    pending_indices = pick(expected, lambda row: row["universe"] == "three_outgoing" and row["disposition"] == "pending_support_completion", 2)
    def swap_restoration_roots(rows):
        i, j = pending_indices
        rows[i]["evidence"]["restoration_roots"], rows[j]["evidence"]["restoration_roots"] = rows[j]["evidence"]["restoration_roots"], rows[i]["evidence"]["restoration_roots"]
        rebind(rows[i]); rebind(rows[j])
    expect_rejection("swap_valid_restoration_bindings", mutated(expected, swap_restoration_roots), expected); mutations += 1

    n4_transport_indices = pick(expected, lambda row: row["universe"] == "four_outgoing_survivor" and "presentation_transport" in row["evidence"], 2)
    def swap_n4_transports(rows):
        i, j = n4_transport_indices
        rows[i]["evidence"]["presentation_transport"], rows[j]["evidence"]["presentation_transport"] = rows[j]["evidence"]["presentation_transport"], rows[i]["evidence"]["presentation_transport"]
        rebind(rows[i]); rebind(rows[j])
    expect_rejection("swap_valid_n4_transports", mutated(expected, swap_n4_transports), expected); mutations += 1

    direct_i = pick(expected, lambda row: row["universe"] == "four_outgoing_survivor" and row["disposition"] == "direct_labelled_isomorphism")[0]
    restore_i = pick(expected, lambda row: row["universe"] == "four_outgoing_survivor" and row["disposition"] == "fixed_full_restoration_root")[0]
    def swap_verifiers(rows):
        rows[direct_i]["base_verifier"], rows[restore_i]["base_verifier"] = rows[restore_i]["base_verifier"], rows[direct_i]["base_verifier"]
        rebind(rows[direct_i]); rebind(rows[restore_i])
    expect_rejection("swap_valid_verifier_assignments", mutated(expected, swap_verifiers), expected); mutations += 1

    def alter_presentation_ordinal(rows):
        rows[direct_i]["presentation_ordinal"] += 1; rebind(rows[direct_i])
    expect_rejection("alter_n4_presentation_locator", mutated(expected, alter_presentation_ordinal), expected); mutations += 1

    certificate = ROOT / "primary/certificates/core_universe.json"
    original = certificate.read_bytes()
    try:
        certificate.write_bytes(original + b"\n")
        try:
            verifier.verify_manifest(ROOT)
        except AssertionError:
            mutations += 1
        else:
            raise AssertionError("altered certificate bytes were accepted")
    finally:
        certificate.write_bytes(original)

    manifest = ROOT / "ACTIVE_MANIFEST.json"
    original = manifest.read_bytes()
    try:
        manifest.write_bytes(original.replace(b'"version": "1.1.5"', b'"version": "0.0.0"', 1))
        try:
            payload = verifier.verify_manifest(ROOT)
            assert payload["version"] == "1.1.5", "bundle version"
        except AssertionError:
            mutations += 1
        else:
            raise AssertionError("altered bundle version was accepted")
    finally:
        manifest.write_bytes(original)

    forbidden_name = ROOT / ("obsolete_" + "land" + "mark" + ".txt")
    try:
        forbidden_name.write_text("scope regression\n", encoding="utf-8")
        try:
            verifier.verify_scope(ROOT)
        except AssertionError:
            mutations += 1
        else:
            raise AssertionError("obsolete filename token was accepted")
    finally:
        forbidden_name.unlink(missing_ok=True)

    scope_text = ROOT / "scope_token_regression.txt"
    try:
        scope_text.write_text("obsolete " + "land" + "mark" + " token\n",
                              encoding="utf-8")
        try:
            verifier.verify_scope(ROOT)
        except AssertionError:
            mutations += 1
        else:
            raise AssertionError("obsolete text token was accepted")
    finally:
        scope_text.unlink(missing_ok=True)

    verifier.verify_manifest(ROOT)
    verifier.verify_scope(ROOT)
    verifier.verify_counts(ROOT)
    print(f'{{"mutations_rejected": {mutations}, "status": "VERIFIED"}}')


if __name__ == "__main__":
    main()
