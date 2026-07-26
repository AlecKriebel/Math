#!/usr/bin/env python3
"""Narrow revised-byte addendum for the hostile mathematical audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
REVIEW_ROOT = Path(__file__).resolve().parent

OLD_BINDINGS = {
    "math/lemmas/order13_k3_synthesis_target.md": {
        "bytes": 26112,
        "sha256": "02c661edf61db8f4b4a5769972e726ce8c1c693e418c1b97b2293e68765e0f44",
    },
    "math/lemmas/order13_k3_hole11_exclusion.md": {
        "bytes": 16303,
        "sha256": "ee492ff314ac2df5f9e1e80982c9bd455dcbce30106d54083d0cd7a930627408",
    },
}

NEW_BINDINGS = {
    "math/lemmas/order13_k3_synthesis_target.md": {
        "bytes": 26303,
        "sha256": "7bec13620961adeaf61c60e88c8bc9366beecab7387e40c80083fe702484ab39",
    },
    "math/lemmas/order13_k3_hole11_exclusion.md": {
        "bytes": 16330,
        "sha256": "511432d00f43f602fd906b3b5e37ae0e5c85cbc1523bcd63c5b668a00f0d53f8",
    },
}

FROZEN_AUDIT_ARTIFACTS = {
    "reviews/order13_k3_math_hostile/audit.py": {
        "bytes": 47177,
        "sha256": "35d405424127c1a28742ade277fd5c5add0a109749ccc51ab6d622740371241b",
    },
    "reviews/order13_k3_math_hostile/evidence.json": {
        "bytes": 20660,
        "sha256": "8c1f5b3fe4511a4d19efdc224a7ea6b10b38eac06275ddce615bd73949d22af1",
    },
    "reviews/order13_k3_math_hostile/REVIEW.md": {
        "bytes": 15021,
        "sha256": "284ec751a215e499de2adfa2f2b377d1a700a27a8b3e96964067c53f652698d8",
    },
}

REPLACEMENTS = {
    "math/lemmas/order13_k3_synthesis_target.md": (
        (
            "This note does **not** assert that any order-13 formula has been generated\n"
            "correctly or that any such formula is satisfiable or unsatisfiable.  Exact\n"
            "source bytes, generated CNF bytes, proof certificates, and independent replay\n"
            "remain separate implementation and certificate obligations.  The companion\n"
            "direct proof in `order13_k3_hole11_exclusion.md` now excludes the `hole11`\n"
            "branch without a solver; it should receive independent adversarial review\n"
            "before claim-ledger promotion.\n"
        ),
        (
            "This note does not by itself assert that any order-13 formula has been\n"
            "generated correctly or is satisfiable or unsatisfiable.  Exact source bytes,\n"
            "generated CNF bytes, proof certificates, and independent replay are separate\n"
            "implementation and certificate obligations.  A separately frozen A/B audit\n"
            "now accepts deterministic constructor bytes for all four templates; the\n"
            "abstract equivalence here is independent of that implementation.  The\n"
            "companion direct proof in `order13_k3_hole11_exclusion.md` has passed\n"
            "independent hostile review in `reviews/order13_k3_math_hostile/`.\n"
        ),
        (
            "1. **No implementation theorem yet.**  Theorems 4--5 concern the abstract\n"
            "   clause scheme.  A decisive run still needs a dedicated deterministic\n"
            "   order-13 constructor, an independent clause-level reconstruction, exact\n"
            "   formula hashes, and a proof-producing solver/checker pipeline.\n"
        ),
        (
            "1. **Implementation is separately bound.**  A deterministic order-13\n"
            "   constructor and independent clause/byte reconstruction are accepted in\n"
            "   `reviews/order13_k3_constructor_acceptance/`.  This note remains the\n"
            "   abstract semantic proof.  Solver execution, proof conversion, certificate\n"
            "   checking, and accepted exclusions for the live branches remain separate\n"
            "   obligations.\n"
        ),
    ),
    "math/lemmas/order13_k3_hole11_exclusion.md": (
        (
            "The proof should receive an independent adversarial review before promotion\n"
            "to the campaign claim ledger.  Its order-13 specialization has also been\n"
            "checked independently against the exact two canonical complements, but that\n"
            "computation is not used in the proof.\n"
        ),
        (
            "The frozen theorem bytes have passed independent adversarial review in\n"
            "`reviews/order13_k3_math_hostile/`.  Its clean-room checker also reconstructs\n"
            "the order-13 specialization from the exact two canonical complements; that\n"
            "computation is not used in the proof.\n"
        ),
        (
            "Two structurally independent exact evaluators reproduce (3.1)--(3.2) for\n"
            "both order-13 graphs.  The computation is a regression check; the parameter\n"
            "proof is Theorem 4.\n"
        ),
        (
            "The clean-room checker in `reviews/order13_k3_math_hostile/` independently\n"
            "reproduces (3.1)--(3.2) and both displayed Graph6 strings.  This is a\n"
            "regression check; the parameter proof is Theorem 4.\n"
        ),
    ),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bind(relative: str) -> dict[str, object]:
    data = (ROOT / relative).read_bytes()
    return {"path": relative, "bytes": len(data), "sha256": digest(data)}


def verify_binding(relative: str, expected: dict[str, object]) -> dict[str, object]:
    actual = bind(relative)
    if actual["bytes"] != expected["bytes"] or actual["sha256"] != expected["sha256"]:
        raise AssertionError({"binding_changed": relative, "actual": actual})
    return actual


def load_frozen_audit() -> ModuleType:
    path = REVIEW_ROOT / "audit.py"
    spec = importlib.util.spec_from_file_location("frozen_math_hostile_audit", path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load frozen audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reverse_exact_replacements() -> list[dict[str, object]]:
    results = []
    for relative, snippets in REPLACEMENTS.items():
        current = (ROOT / relative).read_text(encoding="utf-8")
        reconstructed = current
        pairs = list(zip(snippets[0::2], snippets[1::2]))
        for old, new in pairs:
            if reconstructed.count(new) != 1:
                raise AssertionError(
                    {"replacement_not_unique": relative, "new_prefix": new[:80]}
                )
            if old in reconstructed:
                raise AssertionError(
                    {"old_wording_still_present": relative, "old_prefix": old[:80]}
                )
            reconstructed = reconstructed.replace(new, old, 1)
        encoded = reconstructed.encode("utf-8")
        expected = OLD_BINDINGS[relative]
        if len(encoded) != expected["bytes"] or digest(encoded) != expected["sha256"]:
            raise AssertionError({"reconstructed_old_bytes_differ": relative})
        results.append(
            {
                "path": relative,
                "replacement_count": len(pairs),
                "new": verify_binding(relative, NEW_BINDINGS[relative]),
                "reconstructed_old_bytes": len(encoded),
                "reconstructed_old_sha256": digest(encoded),
            }
        )
    return results


def rerun_regressions(module: ModuleType) -> list[str]:
    old_evidence = json.loads((REVIEW_ROOT / "evidence.json").read_text())
    functions: dict[str, Callable[[], object]] = {
        "pair_common_neighbor_dictionary": module.pair_common_neighbor_audit,
        "connected_cut_complement_sign": module.cut_sign_audit,
        "CNF_local_truth_tables": module.cnf_gadget_truth_tables,
        "SPGT_and_order_arithmetic": module.spgt_coverage_arithmetic,
        "coloring_banks_and_clause_census": module.bank_and_census_audit,
        "two_outside_vertex_pattern_classification":
            module.pattern_classification_audit,
        "small_attack_trees": module.small_attack_tree_audit,
        "uniform_attack": module.uniform_attack_audit,
        "canonical_family_parameters": module.family_parameter_audit,
        "fail_closed_mutations": module.mutation_audit,
        "local_primary_source_conflict_scan":
            module.local_literature_conflict_scan,
    }
    matched = []
    for evidence_key, function in functions.items():
        actual = function()
        if actual != old_evidence[evidence_key]:
            raise AssertionError({"regression_changed": evidence_key})
        matched.append(evidence_key)
    return matched


def mutation_checks() -> list[dict[str, object]]:
    results = []

    def rejected(name: str, action: Callable[[], None]) -> None:
        try:
            action()
        except AssertionError as error:
            results.append(
                {"mutation": name, "rejected": True, "reason": str(error)[:200]}
            )
            return
        raise AssertionError({"mutation_not_rejected": name})

    relative = "math/lemmas/order13_k3_synthesis_target.md"
    current = (ROOT / relative).read_text()
    new = REPLACEMENTS[relative][1]

    def missing_replacement() -> None:
        mutant = current.replace(new, "", 1)
        if mutant.count(new) != 1:
            raise AssertionError("required revised block absent")

    def duplicate_replacement() -> None:
        mutant = current + new
        if mutant.count(new) != 1:
            raise AssertionError("revised block is not unique")

    def mathematical_byte_change() -> None:
        mutant = current.replace("There are exactly", "There are inexactly", 1)
        reconstructed = mutant
        snippets = REPLACEMENTS[relative]
        for old, revised in zip(snippets[0::2], snippets[1::2]):
            reconstructed = reconstructed.replace(revised, old, 1)
        if digest(reconstructed.encode()) != OLD_BINDINGS[relative]["sha256"]:
            raise AssertionError("non-status byte change detected")

    rejected("delete_revised_status_block", missing_replacement)
    rejected("duplicate_revised_status_block", duplicate_replacement)
    rejected("change_mathematical_byte_outside_replacements", mathematical_byte_change)
    return results


def run() -> dict[str, object]:
    frozen_artifacts = [
        verify_binding(relative, expected)
        for relative, expected in FROZEN_AUDIT_ARTIFACTS.items()
    ]
    replacements = reverse_exact_replacements()
    module = load_frozen_audit()
    matched_regressions = rerun_regressions(module)
    mutations = mutation_checks()
    source = Path(__file__).read_bytes()
    return {
        "schema": "gamma-theta-order13-k3-math-hostile-revised-byte-addendum-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED",
        "exact_diff": replacements,
        "proof_of_scope": (
            "Replacing each revised documentation block by its frozen predecessor "
            "reconstructs both previously accepted files byte for byte and hash for "
            "hash. Therefore no byte outside the four documented replacements changed."
        ),
        "frozen_original_audit_artifacts": frozen_artifacts,
        "regression_sections_recomputed_and_identical": matched_regressions,
        "resolved_wording_gaps": [
            "synthesis pre-audit implementation status",
            "synthesis remaining-gap item 1",
            "hole theorem pre-audit review status",
            "hole theorem unbound evaluator regression sentence",
        ],
        "fail_closed_mutations": mutations,
        "claim_boundary": (
            "This addendum transfers the frozen hostile mathematical acceptance "
            "to the revised theorem-note bytes. It makes no new theorem, novelty, "
            "solver, UNSAT, certificate, or runner claim."
        ),
        "source": {
            "path": "reviews/order13_k3_math_hostile/addendum_audit.py",
            "bytes": len(source),
            "sha256": digest(source),
            "runtime_dependencies": "Python standard library plus frozen audit.py",
        },
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
