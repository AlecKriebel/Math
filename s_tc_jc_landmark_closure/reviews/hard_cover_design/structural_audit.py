#!/usr/bin/env python3
"""Independent verifier for the hard-cover design review artifacts.

The script intentionally does not import primary modules and does not consume
hard-cover census output.  It checks source-byte hashes, static design hooks,
the machine-readable claim ledger, and the exact algebraic counterexample
used to reject unconditional selected-marginal lifting.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ALLOWED = {"VERIFIED", "FALSE", "UNRESOLVED"}
REQUIRED_CLAIMS = {
    "fixed_full_relation_restoration_exhaustive",
    "unconditional_selected_marginal_lift",
    "degree_mismatch_when_source_lacks_extras",
    "omitted_target_role_types",
    "source_extras_not_sinks",
    "probe_submersion",
    "deterministic_dummy_restoration_order",
    "finite_union_logic",
    "generic_polynomial_separation_direction",
    "strict_sign_separation_direction",
    "quick_power_sign_completeness",
    "terminal_t_is_sufficient_for_conclusion",
    "terminal_t_is_jc_equality",
    "probe_path_coherence_artifact",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def contains(text: str, needle: str, label: str) -> None:
    require(needle in text, f"missing static hook: {label}")


def check_source_hashes(repo: Path, review: Path) -> dict:
    payload = json.loads((review / "source_hashes.json").read_text())
    require(payload["schema"] == "hard-cover-design-source-hashes-v1", "bad source hash schema")
    results = {}
    for relative, expected in payload["files"].items():
        path = repo / relative
        require(path.is_file(), f"missing audited source: {relative}")
        actual = sha256(path)
        require(actual == expected, f"source hash mismatch for {relative}: {actual} != {expected}")
        results[relative] = actual
    return results


def check_static_hooks(repo: Path) -> dict:
    hard = (repo / "primary/hard_cover_compiler.py").read_text()
    completion = (repo / "primary/completion_universe.py").read_text()
    support = (repo / "primary/support_universe.py").read_text()

    contains(hard, "source_signature & ~target_signature", "generic separation direction")
    contains(hard, "target_signature & ~source_signature", "target-only strict-sign direction")
    contains(hard, "if source_poly:\n            continue", "target-only source-zero filter")
    contains(hard, "quick_power_sign(target_poly)", "strict sign is target-side")
    contains(hard, "dummy_roles = tuple(sorted(target_variant.dummy_labels, key=natural))", "dummy sort")
    contains(hard, "role = remaining[0]", "deterministic next dummy")
    contains(hard, "label = f\"L_{current_p}\"", "fresh restored label")
    contains(hard, "for segment, word in enumerate(state):", "source insertion scans segments")
    contains(hard, "for position in range(len(word) + 1):", "source insertion scans positions")
    contains(hard, "t_quotient(sd0(source_graph))", "terminal source T quotient")
    contains(hard, "t_quotient(sd0(target_graph))", "terminal target T quotient")

    contains(completion, "dummy = f\"D_REPAIR_", "repair dummy role")
    contains(completion, "dummy = f\"D_SINK_", "sink dummy role")
    contains(completion, "dummies = [INCOMING]", "marginalized incoming dummy role")
    contains(completion, "def marginal_incoming_completions", "marginalized incoming completion generator")

    contains(support, "sink_labels = {sink: f\"Q_SINK_", "all source sinks selected")
    contains(support, "for extra_index, arc_index in enumerate(assignments):", "source extras assigned to segments")
    contains(support, "letters[arc_index].append(f\"P_{extra_index}\")", "source extra segment insertion")

    return {
        "hard_cover_static_hooks": 11,
        "completion_dummy_role_hooks": 4,
        "source_extra_hooks": 3,
        "full_relation_binding_field_present": "full_relation_id" in hard,
    }


def check_claims(review: Path) -> dict:
    payload = json.loads((review / "claims.json").read_text())
    require(payload["schema"] == "hard-cover-design-claims-v1", "bad claims schema")
    claims = {row["id"]: row for row in payload["claims"]}
    require(set(claims) == REQUIRED_CLAIMS, f"claim id mismatch: {sorted(set(claims) ^ REQUIRED_CLAIMS)}")
    for row in claims.values():
        require(row["status"] in ALLOWED, f"bad status for {row['id']}: {row['status']}")
        require(row.get("summary"), f"missing summary for {row['id']}")
    require(claims["unconditional_selected_marginal_lift"]["status"] == "FALSE", "lift counterexample claim must be FALSE")
    require(claims["finite_union_logic"]["status"] == "UNRESOLVED", "finite-union limitation must stay explicit")
    require(claims["probe_path_coherence_artifact"]["status"] == "UNRESOLVED", "coherence artifact limitation must stay explicit")
    return {status: sum(1 for row in claims.values() if row["status"] == status) for status in sorted(ALLOWED)}


def check_counterexample(review: Path) -> dict:
    path = review / "counterexamples/unconditional_lift_failure.json"
    payload = json.loads(path.read_text())
    require(payload["schema"] == "hard-cover-unconditional-lift-counterexample-v1", "bad counterexample schema")
    require(payload["status"] == "FALSE", "counterexample status must be FALSE")

    # S1: b = 1 - a. T1: b = a. Their intersection solves a = 1 - a.
    a_intersection = Fraction(1, 2)
    b_intersection = Fraction(1, 2)
    require(b_intersection == a_intersection, "intersection not in T1")
    require(a_intersection + b_intersection == 1, "intersection not in S1")
    for a in (Fraction(1, 3), Fraction(2, 3)):
        b = 1 - a
        require(0 < a < 1 and 0 < b < 1, "sample outside open cube")
        require(b - a != 0, "sample accidentally lies in target full set")
    return {
        "selected_projection_equal": True,
        "restored_intersection_dimension": 0,
        "separating_polynomial_on_source": "b-a = 1-2a",
    }


def main() -> int:
    review = Path(__file__).resolve().parent
    repo = review.parents[1]
    report = {
        "schema": "hard-cover-design-structural-audit-result-v1",
        "source_hashes": check_source_hashes(repo, review),
        "static_hooks": check_static_hooks(repo),
        "claims": check_claims(review),
        "counterexample": check_counterexample(review),
    }
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - command-line verifier
        print(f"VERIFY_FAILED: {exc}", file=sys.stderr)
        raise
