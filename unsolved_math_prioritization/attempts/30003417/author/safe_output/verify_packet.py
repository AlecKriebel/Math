#!/usr/bin/env python3
"""Portable integrity and order-logic checks; not an infinite-cardinal proof checker."""
from pathlib import Path
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parent
PAYLOAD = {
    "README.md", "REPORT.md", "RETAINED_PROOFS.md", "EXACT_CONTROLS.json",
    "SOURCE_VERIFICATION.json", "RESEARCH_LOG.md", "verify_packet.py",
    "VERIFICATION.json",
}


def mathematical_controls():
    controls = json.loads((ROOT / "EXACT_CONTROLS.json").read_text())
    source = json.loads((ROOT / "SOURCE_VERIFICATION.json").read_text())
    assert controls["problem_id"] == source["problem_id"] == 30003417
    assert controls["hypotheses"]["kappa_uncountable"]
    assert controls["hypotheses"]["kappa_regular"]
    assert controls["hypotheses"]["two_to_less_than_kappa_equals_kappa"]
    assert controls["approach_count"] == 5
    assert controls["neither_part_resolved"]
    for key in ("countermodel_constructed", "independence_proved", "novelty_claimed",
                "full_resolution_claimed", "degenerate_arithmetic_used_as_counterexample",
                "singular_results_used_as_regular_results",
                "compactness_models_used_as_universal_theorem"):
        assert controls[key] is False
    assert controls["independent_audit_status"] == "pending"
    assert source["remote_writes_performed"] is False
    assert source["dataset"]["selected_zero_based_index"] == 12201
    assert source["dataset"]["separate_report_available"] is False
    assert source["repository"]["statement_hash_recomputed_match"]
    assert source["repository"]["review_hash_recomputed_match"]
    public_manifest = {
        "problems_json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
        "research_results_json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
    }
    for key, (size, sha) in public_manifest.items():
        obj = source["dataset"][key]
        assert (obj["bytes"], obj["sha256"]) == (size, sha)
        assert obj["manifest_hash_match"] and obj["manifest_bytes_match"]
    proof = (ROOT / "RETAINED_PROOFS.md").read_text()
    for label in controls["retained_proof_labels"]:
        assert label in proof


def order_regression():
    """All numbers are ordered labels, not actual realizable infinite cardinals."""
    admissible = 0
    first_failure = 0
    second_failure = 0
    both_failures = 0
    for b, d, cov, non in itertools.product(range(1, 7), repeat=4):
        if not (b <= d and b <= non and cov <= d):
            continue
        admissible += 1
        add = min(b, cov)
        cof = max(d, non)
        assert (add == b) == (b <= cov)
        assert (cof == d) == (non <= d)
        assert (add < b) == (cov < b)
        assert (d < cof) == (d < non)
        assert add <= cov and add <= non and cov <= cof and non <= cof
        if b == 1:
            assert add == b
        if d == 6:
            assert cof == d
        first_failure += add < b
        second_failure += d < cof
        both_failures += add < b and d < cof
    assert first_failure and second_failure and both_failures
    # A strict cov<d does not logically imply cov<b, even given both formulas.
    b, d, cov, non = 1, 2, 1, 1
    assert cov < d and not cov < b
    assert min(b, cov) == b and max(d, non) == d
    return {
        "admissible_order_assignments": admissible,
        "first_equality_failures_in_abstract_assignments": first_failure,
        "second_equality_failures_in_abstract_assignments": second_failure,
        "both_failures_in_abstract_assignments": both_failures,
        "realizability_claimed": False,
    }


def expected_report():
    mathematical_controls()
    return {
        "status": "PASS",
        "scope": "Portable payload integrity, exact-scope controls, public manifest metadata, and finite order-logic regression only.",
        "infinite_cardinal_proofs_formally_verified": False,
        "independent_mathematical_audit": "pending",
        "source_bytes_needed_for_replay": False,
        "checks": ["exact_controls", "claim_boundaries", "public_dataset_manifest_metadata",
                   "retained_proof_labels", "finite_min_max_logic", "payload_allowlist",
                   "no_symlinks", "sha256_and_byte_manifest"],
        "finite_order_logic": order_regression(),
    }


def check_integrity():
    actual = {p.name for p in ROOT.iterdir() if p.is_file()}
    assert actual == PAYLOAD | {"MANIFEST.json"}, (actual, PAYLOAD)
    assert all(not p.is_symlink() for p in ROOT.iterdir())
    assert all(p.is_file() for p in ROOT.iterdir()), "No directories permitted in frozen payload"
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    assert set(manifest["files"]) == PAYLOAD
    for name, entry in manifest["files"].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == entry["bytes"], name
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], name


if __name__ == "__main__":
    check_integrity()
    result = expected_report()
    assert result == json.loads((ROOT / "VERIFICATION.json").read_text())
    print(json.dumps(result, indent=2, ensure_ascii=False))
