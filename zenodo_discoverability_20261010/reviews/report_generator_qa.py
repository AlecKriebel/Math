"""Disk-only completion-gate controls using one genuine public receipt pair.

The temporary scope fixture is a program test, not evidence of publication.
It is removed when the checks finish. Real RESULTS files are not overwritten.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("results_builder", BASE / "build_results.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    approved = json.loads((BASE / "APPROVED_PROPOSALS.json").read_text())
    catalog = json.loads((BASE / "SOURCE_CATALOG.json").read_text())
    inventory = json.loads((BASE / "INVENTORY.json").read_text())
    audit = json.loads((BASE / "reviews/FINAL_RECEIPT_AUDIT.json").read_text())
    entry = next(e for e in approved["records"] if e["id"] == 23271172)
    controls = {}
    with tempfile.TemporaryDirectory(prefix="report_gate_fixture_", dir=BASE / "reviews") as directory:
        fixture = Path(directory)
        test_approved = deepcopy(approved)
        test_approved["records"] = [entry]
        test_catalog = [next(e for e in catalog if e["id"] == entry["id"])]
        test_inventory = deepcopy(inventory)
        test_inventory["records"] = [next(e for e in inventory["records"] if e["id"] == entry["id"])]
        scope = {"all_versions_count": 1, "all_ids": [entry["id"]], "missing_original_ids": []}
        hashes = {
            "approved_manifest_sha256": write(fixture / "APPROVED_PROPOSALS.json", test_approved),
            "source_catalog_sha256": write(fixture / "SOURCE_CATALOG.json", test_catalog),
            "inventory_sha256": write(fixture / "INVENTORY.json", test_inventory),
            "all_versions_scope_evidence_sha256": write(fixture / "reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json", scope),
        }
        baseline_manifest = {"records": {str(entry["id"]): {
            "sha256": hashlib.sha256((BASE / f"receipts/{entry['id']}/before.json").read_bytes()).hexdigest()}}}
        hashes["original_baseline_manifest_sha256"] = write(fixture / "reviews/ORIGINAL_BASELINE_HASHES.json", baseline_manifest)
        tool_path = fixture / "audit_receipts.py"
        shutil.copyfile(BASE / "audit_receipts.py", tool_path)
        tool_hash = hashlib.sha256(tool_path.read_bytes()).hexdigest()
        route_names = ("native_metadata.py", "native_views.py", "apply_reviewed.py", "baseline.py")
        route_hashes = {}
        for name in route_names:
            shutil.copyfile(BASE / name, fixture / name)
            route_hashes[name] = hashlib.sha256((fixture / name).read_bytes()).hexdigest()
        test_native_audit = {"passed": 1, "failed": 0,
                             "tests": [{"test": "generator_fixture_only", "passed": True}],
                             "source_sha256": route_hashes.pop("native_metadata.py"),
                             "related_source_sha256": route_hashes}
        write(fixture / "reviews/NATIVE_FINAL_AUDIT.json", test_native_audit)
        test_controls = {"all_passed": True, "audit_tool_sha256": tool_hash,
                         "controls": [{"name": "generator_fixture_only", "passed": True}]}
        control_hash = write(fixture / "reviews/FINAL_RECEIPT_AUDIT_CONTROLS.json", test_controls)
        audited_record = next(e for e in audit["records"] if e["id"] == entry["id"])
        relatives = [f"patches/{entry['id']}.json", entry["independent_content_review"],
                     f"receipts/{entry['id']}/first_staging_guard_stop.json",
                     "reviews/FILES_DRAFT_REPRESENTATION_COMPARISON.json"]
        relatives.extend(f"receipts/{entry['id']}/{name}.json" for name in audited_record["receipt_sha256"])
        for relative in relatives:
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / relative, target)
        test_audit = {"status": "pass", "approved_count": 1, "completed_count": 1,
                      "pending_ids": [], "failed_ids": [], "audit_tool_sha256": tool_hash,
                      "first_record_representation": deepcopy(audit["first_record_representation"]),
                      "falsification_controls": {"all_passed": True, "same_audit_tool": True,
                                                  "count": 1, "sha256": control_hash},
                      "records": [audited_record], **hashes}
        audit_path = fixture / "reviews/FINAL_RECEIPT_AUDIT.json"
        write(audit_path, test_audit)
        result = module.build_report(fixture)
        assert result["complete"]
        controls["genuine_public_receipt_pair_and_matching_audit_passes"] = True

        after_path = fixture / f"receipts/{entry['id']}/after.json"
        after_bytes = after_path.read_bytes()
        after_path.unlink()
        result = module.build_report(fixture)
        assert not result["complete"] and result["summary"]["pending_record_ids"] == [entry["id"]]
        controls["missing_final_receipt_never_claims_complete"] = True
        after_path.write_bytes(after_bytes)

        before = json.loads((fixture / f"receipts/{entry['id']}/before.json").read_text())
        after = json.loads(after_bytes)
        patch = json.loads((fixture / f"patches/{entry['id']}.json").read_text())["metadata"]
        mutations = {
            "changed_doi_rejected": ("doi", "10.5281/zenodo.99999999", "doi_unchanged"),
            "changed_version_history_rejected": ("identity", {"id": str(entry["id"])}, "full_public_identity_and_version_history_unchanged"),
            "changed_file_manifest_rejected": ("files", [], "file_names_checksums_sizes_unchanged"),
            "changed_native_file_settings_rejected": ("native_files", {}, "native_file_ids_settings_access_links_unchanged"),
        }
        for name, (field, value, check) in mutations.items():
            changed = deepcopy(after)
            changed[field] = value
            assert module.local_checks(before, changed, entry, patch)[check] is False
            write(after_path, changed)
            assert not module.build_report(fixture)["complete"]
            controls[name] = True
        after_path.write_bytes(after_bytes)

        stale = deepcopy(test_audit)
        stale["records"][0]["receipt_sha256"]["after"] = "0" * 64
        write(audit_path, stale)
        assert not module.build_report(fixture)["complete"]
        controls["stale_independent_audit_never_claims_complete"] = True
        write(audit_path, test_audit)

        for name, mutate in (
            ("global_audit_failure_blocks_completion", lambda d: d.update(status="fail")),
            ("first_record_representation_failure_blocks_completion", lambda d: d["first_record_representation"].update(status="fail")),
            ("failed_falsification_controls_block_completion", lambda d: d["falsification_controls"].update(all_passed=False)),
            ("stale_audit_tool_controls_block_completion", lambda d: d["falsification_controls"].update(same_audit_tool=False)),
        ):
            changed_audit = deepcopy(test_audit)
            mutate(changed_audit)
            write(audit_path, changed_audit)
            assert not module.build_report(fixture)["complete"]
            controls[name] = True
        write(audit_path, test_audit)

        tool_bytes = tool_path.read_bytes()
        tool_path.write_bytes(tool_bytes + b"\n# generator QA mutation\n")
        assert not module.build_report(fixture)["complete"]
        controls["current_audit_tool_hash_required"] = True
        tool_path.write_bytes(tool_bytes)

        review_path = fixture / entry["independent_content_review"]
        review_bytes = review_path.read_bytes()
        review_path.write_bytes(review_bytes + b"\nGenerator QA mutation.\n")
        assert not module.build_report(fixture)["complete"]
        controls["stale_content_review_blocks_completion"] = True
        review_path.write_bytes(review_bytes)

        stale_baseline = deepcopy(baseline_manifest)
        stale_baseline["records"][str(entry["id"])]["sha256"] = "0" * 64
        write(fixture / "reviews/ORIGINAL_BASELINE_HASHES.json", stale_baseline)
        assert not module.build_report(fixture)["complete"]
        controls["original_baseline_hash_required"] = True
        write(fixture / "reviews/ORIGINAL_BASELINE_HASHES.json", baseline_manifest)

        for name, relative in (
            ("raw_stage_receipt_hash_required", f"receipts/{entry['id']}/stage.json"),
            ("first_raw_guard_evidence_hash_required", f"receipts/{entry['id']}/first_staging_guard_stop.json"),
            ("first_raw_comparison_evidence_hash_required", "reviews/FILES_DRAFT_REPRESENTATION_COMPARISON.json"),
        ):
            path = fixture / relative
            original_bytes = path.read_bytes()
            path.write_bytes(original_bytes + b"\n")
            assert not module.build_report(fixture)["complete"]
            controls[name] = True
            path.write_bytes(original_bytes)

        route_path = fixture / "native_metadata.py"
        route_bytes = route_path.read_bytes()
        route_path.write_bytes(route_bytes + b"\n# generator QA mutation\n")
        assert not module.build_report(fixture)["complete"]
        controls["current_native_route_audit_hash_required"] = True
        route_path.write_bytes(route_bytes)

        scope["all_ids"].append(99999999)
        scope["all_versions_count"] = 2
        write(fixture / "reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json", scope)
        result = module.build_report(fixture)
        assert not result["complete"] and result["summary"]["unaccounted_owned_record_ids"] == [99999999]
        controls["unaccounted_owned_record_blocks_completion"] = True

    live = module.build_report(BASE)
    assert live["summary"]["approved_paper_records"] == len(approved["records"])
    if live["summary"]["pending_record_ids"]:
        assert not live["complete"]
    controls["real_report_count_matches_frozen_approvals"] = True
    output = {"generated_utc": datetime.now(timezone.utc).isoformat(), "status": "pass",
              "controls": controls, "real_report_complete": live["complete"],
              "real_report_summary": live["summary"],
              "scope": "Program completion-gate QA only; one genuine receipt pair is tested in a temporary narrowed scope. No remote actions."}
    write(BASE / "reviews/REPORT_GENERATOR_QA.json", output)
    print(json.dumps({"status": "pass", "controls_passed": len(controls)}, indent=2))


if __name__ == "__main__":
    main()
