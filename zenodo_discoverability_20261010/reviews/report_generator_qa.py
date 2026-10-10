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
        for relative in (f"patches/{entry['id']}.json", entry["independent_content_review"],
                         f"receipts/{entry['id']}/before.json", f"receipts/{entry['id']}/after.json"):
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / relative, target)
        test_audit = {"approved_count": 1, "completed_count": 1, "pending_ids": [], "failed_ids": [],
                      "records": [next(e for e in audit["records"] if e["id"] == entry["id"])], **hashes}
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
