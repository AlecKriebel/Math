#!/usr/bin/env python3
"""Adversarial structural audit of the attempted self-contained Gate-2 closure.

This does not execute the expensive atlas.  It checks the exact source text
whose SHA-256 is locked by the report and records what the implementation does
and does not bind.  The checks are deliberately mutation-sensitive: a changed
loop, input dependency, witness payload, or promotion pass condition makes the
diagnostic fail instead of inheriting a printed VERIFIED status.
"""

from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path


EXPECTED_SHA256 = "d88febb3e051378e769db3e55fcf9f9b51004f94eefe9975cc9e221a6727212d"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def function_source(text: str, tree: ast.Module, name: str) -> tuple[str, int, int]:
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(nodes) != 1:
        raise AssertionError((name, len(nodes)))
    node = nodes[0]
    lines = text.splitlines()
    return "\n".join(lines[node.lineno - 1 : node.end_lineno]), node.lineno, int(node.end_lineno)


def require(source: str, fragment: str, label: str) -> None:
    if fragment not in source:
        raise AssertionError(f"missing {label}: {fragment}")


def audit(script: Path, crosscheck: Path | None) -> dict:
    text = script.read_text()
    tree = ast.parse(text)
    actual_sha = digest(script)
    if actual_sha != EXPECTED_SHA256:
        raise AssertionError(("unexpected script SHA", actual_sha))

    enum, enum_start, enum_end = function_source(text, tree, "enumerate_labelled_models")
    cert, cert_start, cert_end = function_source(text, tree, "certify_strict_directions")
    arbitrary, arbitrary_start, arbitrary_end = function_source(text, tree, "arbitrary_subdivision_audit")
    load, load_start, load_end = function_source(text, tree, "load_support_source_candidates")
    theta, theta_start, theta_end = function_source(text, tree, "theta_finite_closure")
    main, main_start, main_end = function_source(text, tree, "main")

    # Finite binding: exact displayed-tree descriptors are built and target
    # descriptor decks are all traversed, but source witnesses use only one
    # representative deck and the emitted factor records omit pair IDs.
    for fragment, label in (
        ('"descriptor_decks": {}', "descriptor-deck store"),
        ('record["descriptor_decks"].setdefault(descriptors, (base_index, assignment))', "presentation binding"),
        ('record["standard_hashes"].add(standard_hash(labelled))', "topology binding"),
    ):
        require(enum, fragment, label)
    for fragment, label in (
        ('source_record["representative_descriptors"]', "representative-only source deck"),
        ('for target_descriptors in descriptor_decks:', "all distinct target decks"),
        ('single_invariant_pullback(source_descriptor', "source pullback recomputation"),
        ('single_invariant_pullback(\n                        target_descriptor', "target pullback recomputation"),
        ('"factor_records": factor_records', "aggregate factor output"),
    ):
        require(cert, fragment, label)
    if "source_signature_sha256" not in cert or "target_signature_sha256" not in cert:
        raise AssertionError("unresolved rows no longer bind signature pair")
    # Successful rows have no pair record: the only signature pair hashes are
    # emitted inside the unresolved branch.
    successful_pair_binding_absent = cert.count('"source_signature_sha256"') == 1 and cert.count('"target_signature_sha256"') == 1

    # Primitive source topology generation is not local to this script.
    require(load, "data = json.loads(path.read_text())", "frozen support input")
    require(load, 'for index, record in enumerate(data["networks"]):', "frozen network loop")
    require(theta, "load_support_source_candidates(support_path)", "support input dependency")

    # Arbitrary-size promotion: the executable pass bit is only a finite family
    # of synthetic word cases plus rational product checks.  The general claims
    # are literal prose fields, not quantified checks.
    for fragment, label in (
        ('extras = [f"X{i:02d}" for i in range(12)]', "fixed long-word test"),
        ('for core in core_data["theta_classes"]', "one constructed case per supplied core"),
        ('all_reconstructed', "finite reconstruction flag"),
        ('all_reversals_detected', "finite reversal flag"),
        ('all_stabilizers_trivial', "supplied stabilizer flag"),
        ('rational_product_checks', "finite product tests"),
        ('"compatibility_proof":', "prose compatibility assertion"),
        ('"weak_target_language_proof":', "prose weak-target assertion"),
        ('"arbitrary_subdivision_lift_verified": passed', "promotion status assignment"),
    ):
        require(arbitrary, fragment, label)
    quantified_promotion_check_absent = not any(
        token in arbitrary
        for token in (
            "canonical_mixed_code(",
            "standard_hash(",
            "descriptor_exact_bits(",
            "single_invariant_pullback(",
            "exact_open_cube_sign(",
        )
    )
    require(main, 'and arbitrary["arbitrary_subdivision_lift_verified"]', "promotion used in release verdict")

    cross = None
    if crosscheck is not None and crosscheck.exists():
        payload = json.loads(crosscheck.read_text())
        cross = {
            "path": str(crosscheck),
            "sha256": digest(crosscheck),
            "status": payload.get("status"),
            "failure_type": payload.get("failure", {}).get("type"),
            "failure_message": payload.get("failure", {}).get("message"),
            "finite_algebra_sections_present": any(
                key in payload
                for key in ("theta_finite_closure", "cycle_theta_sieve", "cycle_to_theta_promotion")
            ),
        }

    return {
        "script": str(script),
        "sha256": actual_sha,
        "line_ranges": {
            "load_support_source_candidates": [load_start, load_end],
            "enumerate_labelled_models": [enum_start, enum_end],
            "certify_strict_directions": [cert_start, cert_end],
            "theta_finite_closure": [theta_start, theta_end],
            "arbitrary_subdivision_audit": [arbitrary_start, arbitrary_end],
            "main": [main_start, main_end],
        },
        "finite_binding": {
            "displayed_tree_descriptor_decks_computed": True,
            "target_distinct_descriptor_decks_all_checked": True,
            "source_success_checks_use_only_representative_descriptor_deck": True,
            "successful_pair_to_polynomial_records_emitted": not successful_pair_binding_absent,
            "successful_pair_binding_absent": successful_pair_binding_absent,
            "primitive_source_universe_generated_inside_script": False,
            "primitive_source_universe_dependency": "frozen support-network encodings",
        },
        "arbitrary_subdivision": {
            "finite_constructed_cases": True,
            "fixed_long_word_length": 12,
            "quantified_topology_or_pullback_promotion_check_present": not quantified_promotion_check_absent,
            "general_promotion_is_executable_proof": False,
            "general_claims_are_prose_fields": True,
            "finite_boolean_is_load_bearing_for_VERIFIED": True,
        },
        "crosscheck": cross,
        "verdict": "UNRESOLVED: finite computations are substantial, but the emitted certificate lacks successful pair-level topology/pullback bindings and arbitrary-subdivision promotion is not executable proof.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=Path)
    parser.add_argument("--crosscheck", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.script, args.crosscheck), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
