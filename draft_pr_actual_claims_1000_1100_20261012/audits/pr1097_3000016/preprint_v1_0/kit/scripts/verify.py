#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import argparse
import json
from common import KIT, inventory, binding_check, read_json, record, require


def terminal_semantics():
    value = read_json(KIT / "TERMINAL_ADMIN.json")
    expected = {
        "record_type": "DATED_TERMINAL_ADMINISTRATIVE_RECONCILIATION_ONLY",
        "pr": 1097, "head": "ad7b0eeef847da65afe1b691705cfa6e832e8201",
        "complete_whole_package_reviews_completed": 2,
        "minimum_complete_whole_package_reviews_required": 2,
        "latest_complete_whole_review": "NEW_COMPLETE_WHOLE_PACKAGE_02",
        "latest_whole_review_finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
        "latest_whole_review_root_adopted": True, "repair01_root_adopted": True,
        "further_complete_whole_review_currently_required": False,
        "external_ROOT_final_integrity_required": True,
        "external_ROOT_final_integrity_adopted": False,
        "publication_ready": False, "issues_resolved": False, "published": False,
        "ordered_service_hold_pr": 1032,
        "mathematics_paper_checker_path_guards_native_metadata": "UNCHANGED",
        "priority_independent_discovery_worldwide_openness": "UNKNOWN",
        "historical_omitted_program_replayed": False, "external_actions_performed": False,
    }
    for key, want in expected.items():
        require(type(value.get(key)) is type(want) and value[key] == want,
                "terminal semantic mismatch: " + key)
    layer = KIT / "provenance" / "terminal_admin_20261016"
    copies = read_json(layer / "COPIES.json")["entries"]
    for row in copies:
        require(record(KIT / row["copy_path"]) ==
                {"bytes": row["bytes"], "sha256": row["sha256"]},
                "terminal exact copy mismatch")
    root = read_json(layer / "selected" / "ROOT_WHOLE_PACKAGE_REVIEW_02.json")
    require(root["status"] == "ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN"
            and root["whole_reviews_completed"] == 2 and root["minimum_whole_reviews"] == 2
            and root["actionable_P0_P1_P2_P3"] == 0
            and root["terminal_administrative_reconciliation_and_root_final_integrity_required"] is True
            and root["publication_ready"] is False and root["published"] is False
            and root["services_held_after_pr"] == 1032, "terminal ROOT adoption mismatch")
    verdict = read_json(layer / "selected" / "reviews" / "package_02" / "VERDICT.json")
    require(verdict["review"] == value["latest_complete_whole_review"]
            and verdict["findings"] == []
            and verdict["finding_counts"] == value["latest_whole_review_finding_counts"],
            "terminal whole02 verdict mismatch")
    original = read_json(KIT / "provenance" / "CUSTODY.json")["entries"]
    repair = read_json(KIT / "provenance" / "repair01" / "CUSTODY.json")["entries"]
    require(len(original) == 165 and sum(r["decision"] == "EXACT_AUTHORED_COPY" for r in original) == 83
            and sum(r["decision"] == "EXCLUDED" for r in original) == 82,
            "terminal original custody counts")
    require(len(repair) == 332 and sum(r["decision"] == "EXACT_DISTRIBUTED_BYTES" for r in repair) == 233
            and sum(r["decision"] == "EXCLUDED" for r in repair) == 99,
            "terminal repair custody counts")
    # These fields intentionally remain earlier dated history.
    old = read_json(KIT / "CURRENT_REPAIR.json")
    require(old["complete_whole_package_reviews_completed"] == 1
            and old["repair_root_adoption"] == "PENDING" and old["new_complete_whole02"] == "REQUIRED",
            "terminal dated repair history changed")
    history = read_json(KIT / "provenance" / "repair01" / "STAGE_RESOLUTION.json")["entries"]
    require(len(history) == 1127 and sum(r["original_audit_resolution"]["state"] == "INDIVIDUAL_OMISSION"
            for r in history) == 18, "terminal historical omissions changed")
    return {"whole_reviews_completed": 2, "minimum_whole_reviews": 2,
            "latest_zero_actionable_root_adopted": True,
            "external_ROOT_final_integrity": "REQUIRED_NOT_ADOPTED",
            "publication_ready": False, "issues_resolved": False, "published": False,
            "ordered_service_hold_pr": 1032}

def main():
    p = argparse.ArgumentParser(description="Read-only package and optional/required external binding verification")
    p.add_argument("--binding")
    p.add_argument("--require-binding", action="store_true")
    args = p.parse_args()
    result = inventory()
    result.pop("metadata")
    result["terminal"] = terminal_semantics()
    result["binding"] = binding_check(args.binding, args.require_binding)
    result["status"] = "PASS"
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
