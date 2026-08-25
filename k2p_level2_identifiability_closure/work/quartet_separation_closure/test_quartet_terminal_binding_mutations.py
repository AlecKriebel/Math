#!/usr/bin/env python3
"""Adversarial mutations for the exhaustive quartet-terminal binder."""

from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

import verify_quartet_terminal_bindings as binder


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SEMANTICS = HERE / "quartet_logic_certificate.json"
VERIFIER = HERE / "verify_quartet_terminal_bindings.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def expect_failure(name: str, marker: str, action: Callable[[], Any]) -> dict[str, Any]:
    try:
        action()
    except binder.QuartetTerminalFailure as error:
        observed = str(error)
        require(marker in observed, f"wrong diagnostic:{name}:{observed}")
        return {
            "case": name,
            "status": "PASS",
            "expected_marker": marker,
            "observed_diagnostic_sha256": hashlib.sha256(observed.encode()).hexdigest(),
        }
    raise RuntimeError(f"mutation accepted:{name}")


def reseal(value: dict[str, Any]) -> None:
    value.pop("payload_sha256", None)
    value["payload_sha256"] = binder.sha_object(value)


def first_quartet_witness(values: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    for proof_id, content in values.items():
        if isinstance(content, dict) and content.get("reason") == "displayed_quartet_mismatch":
            return proof_id, content
    raise RuntimeError("no quartet witness")


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_TERMINAL_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve() if args.output else HERE / "quartet_terminal_binding_mutation_certificate.json"

    formulas, _semantics_summary = binder.semantics_contract(SEMANTICS)
    cycle_payload = binder.load_json(PROJECT / binder.CYCLE_REGISTRY)
    _cycle_id, cycle_content = first_quartet_witness(cycle_payload["witnesses"])
    restoration_payload = binder.load_json(PROJECT / binder.RESTORATION_FOREST)
    _restoration_id, restoration_content = next(iter(restoration_payload["quartet_certificates"].items()))

    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="k2p-quartet-terminal-mutations-") as directory:
        root = Path(directory)

        spectrum = binder.load_json(SEMANTICS)
        spectrum["edge_spectrum"] = ["1", "s", "s", "g"]
        reseal(spectrum)
        spectrum_path = root / "mutated-spectrum.json"
        spectrum_path.write_text(json.dumps(spectrum, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        rows.append(
            expect_failure(
                "resealed_spectrum_convention_mutation",
                "SEMANTICS_SPECTRUM_FAIL",
                lambda: binder.semantics_contract(spectrum_path),
            )
        )

        coordinate = binder.load_json(SEMANTICS)
        coordinate["canonical_formulas"]["F_A"]["terms"][0][1] = "GGGG"
        formula_row = coordinate["canonical_formulas"]["F_A"]
        formula_payload = {
            "formula_id": formula_row["formula_id"],
            "terms": formula_row["terms"],
            "pullbacks": formula_row["pullbacks"],
        }
        formula_row["formula_sha256"] = binder.sha_object(formula_payload)
        reseal(coordinate)
        coordinate_path = root / "mutated-coordinate.json"
        coordinate_path.write_text(json.dumps(coordinate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        mutated_formulas, _summary = binder.semantics_contract(coordinate_path)
        rows.append(
            expect_failure(
                "resealed_coordinate_word_mutation",
                "LITERAL_FORMULA_SPEC_MISMATCH",
                lambda: binder.validate_content(
                    cycle_content, mutated_formulas, require_stored_witness=True
                ),
            )
        )

        distinguished = copy.deepcopy(cycle_content)
        quartet = binder.normalize_quartet(distinguished["quartet"])
        old_split = binder.normalize_split(distinguished["distinguished_split"])
        replacement = next(split for split in binder.quartet_splits(quartet) if split != old_split)
        distinguished["distinguished_split"] = binder.split_json(replacement)
        rows.append(
            expect_failure(
                "resealed_distinguished_split_mutation",
                "STORED_DISTINGUISHED_SPLIT_FAIL",
                lambda: binder.validate_content(
                    distinguished, formulas, require_stored_witness=True
                ),
            )
        )

        sides = copy.deepcopy(cycle_content)
        sides["zero_on"], sides["strictly_positive_on"] = (
            sides["strictly_positive_on"],
            sides["zero_on"],
        )
        rows.append(
            expect_failure(
                "resealed_zero_positive_side_mutation",
                "STORED_ZERO_SIDE_FAIL",
                lambda: binder.validate_content(sides, formulas, require_stored_witness=True),
            )
        )

        labels = copy.deepcopy(cycle_content)
        labels["quartet"][-1] += 20
        rows.append(
            expect_failure(
                "resealed_quartet_label_transport_mutation",
                "DISPLAYED_SPLIT_OUTSIDE_QUARTET_FAIL",
                lambda: binder.validate_content(labels, formulas, require_stored_witness=True),
            )
        )

        changed_set = copy.deepcopy(restoration_content)
        changed_set["target_splits"] = copy.deepcopy(changed_set["source_splits"])
        changed_set_rekeyed = binder.sha_object(changed_set)
        rows.append(
            expect_failure(
                "rekeyed_relinked_restoration_set_mutation",
                "EQUAL_DISPLAYED_SET_FAIL",
                lambda: binder.validate_content(
                    changed_set, formulas, require_stored_witness=False
                ),
            )
        )
        rows[-1]["mutated_rekeyed_proof_id_sha256"] = changed_set_rekeyed

        raw4_path = PROJECT / binder.RAW4_LEDGER
        with gzip.open(raw4_path, "rt", encoding="utf-8") as handle:
            raw4_row = json.loads(next(handle))
        evidence = copy.deepcopy(raw4_row["evidence_binding"])
        evidence["source_displayed_splits_sha256"] = "0" * 64
        rows.append(
            expect_failure(
                "compact_split_hash_mutation",
                "COMPACT_EVIDENCE_BINDING_FAIL",
                lambda: binder.validate_compact_evidence(evidence, formulas, {}),
            )
        )

        binding = binder.validate_content(
            restoration_content, formulas, require_stored_witness=False
        )
        binding_map = {"proof": binding}
        rows.append(
            expect_failure(
                "unknown_terminal_reference",
                "REGISTRY_REFERENCE_SET_FAIL",
                lambda: binder.registry_rows(binding_map, collections.Counter({"unknown": 1})),
            )
        )
        rows.append(
            expect_failure(
                "omitted_terminal_reference",
                "REGISTRY_REFERENCE_SET_FAIL",
                lambda: binder.registry_rows(binding_map, collections.Counter()),
            )
        )

    raw4_mutations_path = (
        PROJECT
        / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json"
    )
    theta2_mutations_path = (
        PROJECT
        / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json"
    )
    graph_guards = []
    for family, path in (("raw4", raw4_mutations_path), ("theta2", theta2_mutations_path)):
        report = binder.load_json(path)
        require(report.get("status") == "PASS", f"graph mutation report not PASS:{family}")
        matches = [
            row for row in report.get("tests", [])
            if row.get("name") == "reassigned_evidence_binding"
        ]
        require(len(matches) == 1 and matches[0].get("rejected") is True, f"missing graph reassignment guard:{family}")
        graph_guards.append(
            {
                "family": family,
                "path": str(path.relative_to(PROJECT)),
                "sha256": binder.sha_file(path),
                "case": "reassigned_evidence_binding",
                "rejected": True,
            }
        )
    rows.append(
        {
            "case": "valid_proof_substitution_composed_graph_gate",
            "status": "PASS",
            "reason": (
                "A literal-algebra binder cannot distinguish two independently valid "
                "proof bodies. The row-to-split graph replayers reject reassignment."
            ),
            "graph_guards": graph_guards,
        }
    )

    quartet, source_splits, target_splits = binder.content_split_sets(cycle_content)
    reversed_content = binder.historical_content(
        quartet, target_splits, source_splits
    )
    reversed_binding = binder.validate_content(
        reversed_content, formulas, require_stored_witness=True
    )
    original_binding = binder.validate_content(
        cycle_content, formulas, require_stored_witness=True
    )
    require(
        reversed_binding["binding_sha256"] != original_binding["binding_sha256"],
        "complete directional reversal retained the old literal binding",
    )
    require(
        reversed_binding["zero_on"] != original_binding["zero_on"]
        and reversed_binding["strictly_positive_on"]
        != original_binding["strictly_positive_on"],
        "complete directional reversal did not reverse sign sides",
    )
    rows.append(
        {
            "case": "complete_source_target_reversal_composed_graph_gate",
            "status": "PASS",
            "reason": (
                "The reversed directed relation has a different valid literal "
                "separator, but assigning it to the original graph row is a proof "
                "reassignment rejected by both primitive composite graph guards."
            ),
            "original_binding_sha256": original_binding["binding_sha256"],
            "reversed_binding_sha256": reversed_binding["binding_sha256"],
            "graph_guards": graph_guards,
        }
    )

    optimized = subprocess.run(
        [sys.executable, "-O", str(VERIFIER)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(
        optimized.returncode != 0
        and "QUARTET_TERMINAL_BINDING_OPTIMIZED_MODE_FORBIDDEN" in optimized.stdout,
        "optimized binder accepted",
    )
    rows.append(
        {
            "case": "optimized_python",
            "status": "PASS",
            "expected_marker": "QUARTET_TERMINAL_BINDING_OPTIMIZED_MODE_FORBIDDEN",
            "observed_returncode": optimized.returncode,
            "stdout_sha256": hashlib.sha256(optimized.stdout.encode()).hexdigest(),
        }
    )

    payload = {
        "schema": "k2p-quartet-terminal-binding-mutations-v1",
        "status": "PASS",
        "temporary_in_memory_or_temp_directory_mutations_only": True,
        "authoritative_ledgers_modified": False,
        "case_count": len(rows),
        "cases": rows,
        "binder_sha256": binder.sha_file(VERIFIER),
        "semantics_certificate_sha256": binder.sha_file(SEMANTICS),
    }
    result = dict(payload)
    result["payload_sha256"] = binder.sha_object(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("K2P_QUARTET_TERMINAL_BINDING_MUTATIONS_PASS")
    print(json.dumps({"cases": len(rows), "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
