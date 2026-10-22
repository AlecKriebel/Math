#!/usr/bin/env python3
"""Check the flat closed administrative packet against an EXTERNAL manifest pin.

This checks administrative custody and consistency. It adds no mathematical,
priority, human-peer-review, or formal-verification certification. Optional
--package independently replays its exact source/PDF byte-custody check.
"""
import argparse, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
H = "aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
PARENT = "0aaee0476b4d63565abe240ac3ba5c6c3cabf983"
REQUIRED = {"CHECKS.py", "DRIVER_CONTROLS.py", "MERGE_SCOPE.py", "PUBLIC_VERIFY.py", "TRACKER_VERIFY.py",
            "BINDINGS.json", "DRIVER_CONTROLS.json", "MERGE_SCOPE.json", "PUBLIC_VERIFICATION.json",
            "TRACKER_VERIFICATION.json", "SOURCE_CHECK.json", "READINESS_AT_PUBLICATION.json",
            "CREATION_STAGE_READINESS.json", "HANDLE_EQUIVALENCE.json",
            "KNOWN_DRAFT_REPAIR_CONTROLS.py", "KNOWN_DRAFT_REPAIR_CONTROLS.json",
            "KNOWN_DRAFT_REPAIR.json", "ZIP_REPLACEMENT_INTENT.json", "ZIP_DELETION_RECEIPT.json",
            "LOCAL_CHECK.json", "RESEARCH_LOG.md", "VERDICT.json"}

def need(value, reason):
    if not value: raise RuntimeError(reason)

def digest(raw): return hashlib.sha256(raw).hexdigest()

def regular(path):
    s = path.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and not path.is_symlink(), "Not a singly linked regular packet file: "+path.name)
    return path.read_bytes()

def load(folder, name): return json.loads(regular(folder/name))

def all_controls(report):
    rows = report["controls"]
    need(isinstance(rows, list) and rows, "No meaningful controls recorded")
    for r in rows:
        need(r.get("control_pass") is True, "A control failed or has no explicit outcome")
    return len(rows)

def check(folder, external_pin, package=None):
    need(stat.S_ISDIR(folder.lstat().st_mode) and not folder.is_symlink(), "Packet root must be a real directory")
    need(len(external_pin) == 64 and all(c in "0123456789abcdef" for c in external_pin), "External manifest SHA256 required")
    mf = regular(folder/"MANIFEST.json")
    need(digest(mf) == external_pin, "Administrative manifest digest differs from external pin")
    manifest = json.loads(mf)
    need(manifest["schema"] == "pr789-administration-closed-flat/v1", "Unknown administrative packet schema")
    rows = manifest["files"]
    need(isinstance(rows, list), "Manifest inventory must be a list")
    names = set()
    for row in rows:
        n = row["path"]
        need(isinstance(n, str) and n and n not in (".", "..", "MANIFEST.json")
             and "/" not in n and "\\" not in n and "\0" not in n and n not in names, "Non-flat or duplicate packet path")
        names.add(n); raw = regular(folder/n)
        need(type(row["bytes"]) is int and len(raw) == row["bytes"] and digest(raw) == row["sha256"], "Packet bytes or digest differ: "+n)
    need(names == REQUIRED, "Packet authored inventory differs from exact checker contract")
    actual = {p.name for p in folder.iterdir()}
    need(actual == names|{"MANIFEST.json"}, "Unexpected/missing packet entry, including directories")
    b = load(folder, "BINDINGS.json")
    need(b["schema"] == "pr789-administrative-bindings/v1" and b["pr"] == 789
         and b["problem"] == "30001478" and b["original_scientific_head"] == H
         and b["original_parent"] == PARENT
         and b["source_manifest_sha256"] == "b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa"
         and b["source_checker_sha256"] == "700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489"
         and b["driver_sha256"] == "a02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96"
         and type(b["actual_whole_preprint_rounds"]) is int and b["actual_whole_preprint_rounds"] == 4,
         "Administrative scope or exact final four-review V4 identity differs")
    helper_pins = {
        "DRIVER_CONTROLS.py": "3ff99091083bca1e8c2beb54238865d86cd4fefcb0c42da9f83278aff49cb88d",
        "KNOWN_DRAFT_REPAIR_CONTROLS.py": "917eb3eb201f8bd6ba628f8e93d738c1c7a447d3aa42de42ac3e571286c19cb5",
        "MERGE_SCOPE.py": "175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff",
        "PUBLIC_VERIFY.py": "101928f4a7217437e9085c1f9e3a2c87938fa683a35670d1c9d8ad5b9e65669f",
        "TRACKER_VERIFY.py": "ce10be213b614cad6a4de85ea500d8935c17c5f8238cbe8b912d33d06d57276e"}
    need(b["helper_sha256"] == helper_pins and b["metadata_normalizations"] == [], "Approved helper pins or exact metadata staging differ")
    for name,pin in helper_pins.items():
        need(digest(regular(folder/name)) == pin, "Approved helper bytes differ: "+name)
    inventory = b["publication_files"]
    need(isinstance(inventory, list) and len(inventory) == 6
         and len({r["path"] for r in inventory}) == 6, "Six exact publication artifact bindings required")
    by_path = {r["path"]: r for r in inventory}
    need(set(by_path) == {"main.tex", "output/pdf/paper.pdf", "source-and-verification.zip",
                         "zenodo-deposit.json", "zenodo-metadata.json", "zenodo-upload-kit.zip"}, "Exact six artifact paths differ")
    preflight = load(folder, "LOCAL_CHECK.json")
    need(preflight["read_only"] is True and preflight["check"]["environment"] == "production"
         and preflight["check"]["title"] == b["title"]
         and preflight["check"]["files"] == [
             {"name": "paper.pdf", "size": by_path["output/pdf/paper.pdf"]["bytes"], "sha256": by_path["output/pdf/paper.pdf"]["sha256"]},
             {"name": "source-and-verification.zip", "size": by_path["source-and-verification.zip"]["bytes"], "sha256": by_path["source-and-verification.zip"]["sha256"]}],
         "Read-only local preflight does not match the exact current two payloads")
    source = load(folder, "SOURCE_CHECK.json")
    need(source["result"] == "PASS" and source["source_manifest_sha256"] == b["source_manifest_sha256"]
         and source["source_files"] == 151 and source["original_files"] == 58
         and source["exact_head"] == H and source["pdf_binding_checked"] is True, "Exact source custody check is incomplete")
    ready = load(folder, "READINESS_AT_PUBLICATION.json")
    need(ready["result"] == "PASS" and ready["pr"] == 789 and ready["problem"] == "30001478"
         and ready["reviewed_head"] == H and ready.get("original_scientific_head", H) == H
         and ready["source_manifest_sha256"] == b["source_manifest_sha256"]
         and ready["publication_files"] == inventory and type(ready["actual_whole_preprint_rounds"]) is int
         and ready["actual_whole_preprint_rounds"] == 4
         and ready["actual_whole_preprint_rounds"] == b["actual_whole_preprint_rounds"]
         and ready["final_current_round_clean"] is True,
         "Completed exact-package prepublication process receipt is missing")
    rounds = ready["completed_whole_reviews"]
    need(isinstance(rounds, list) and len(rounds) == ready["actual_whole_preprint_rounds"], "Whole-review record count differs")
    reviewers = set()
    for i,r in enumerate(rounds, 1):
        need(type(r["round"]) is int and r["round"] == i and r["freshly_initialized"] is True
             and r["reviewer"] not in reviewers and r["reviewer"].startswith("/root/pr789_whole_preprint_round")
             and type(r["actionable_issues"]) is int and r["actionable_issues"] >= 0,
             "Distinct fresh completed-review identities with strict issue counts required")
        reviewers.add(r["reviewer"])
    need(rounds[-1]["actionable_issues"] == 0 and rounds[-1]["reviewed_source_manifest_sha256"] == b["source_manifest_sha256"]
         and rounds[-1]["reviewed_publication_files"] == inventory, "The final completed review does not clear this exact package")
    need(digest(regular(folder/"READINESS_AT_PUBLICATION.json")) == b["readiness_at_publication_sha256"], "Prepublication readiness receipt pin differs")
    creation_raw = regular(folder/"CREATION_STAGE_READINESS.json")
    creation = json.loads(creation_raw)
    need(digest(creation_raw) == b["creation_stage_readiness_sha256"]
         == "27beef2982540a003d0f95a30153c51d8ef182b5a721418afa904ad3ee24c0ea"
         and creation["result"] == "PASS" and creation["actual_whole_preprint_rounds"] == 3
         and creation["source_manifest_sha256"] == "50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de"
         and creation["reviewed_head"] == H and b["record_id"] == 23423736,
         "The sole known draft's immutable creation-stage readiness snapshot differs")
    canonical = load(folder, "HANDLE_EQUIVALENCE.json")
    need(canonical["result"] == "PASS_EXACT_OBSERVED_HANDLE_EQUIVALENCE_NOT_PUBLICATION_APPROVAL"
         and canonical["record_id"] == b["record_id"] and canonical["submitted"] is False
         and canonical["creation_POSTs"] == 1 and canonical["changed_related_entry_zero_based"] == 3
         and canonical["exact_before"] == {"identifier": "https://hdl.handle.net/1842/22886", "relation": "references", "scheme": "url"}
         and canonical["exact_server_form"] == {"identifier": "1842/22886", "relation": "references", "scheme": "handle"}
         and canonical["all_five_other_related_identifiers_and_order_exact"] is True
         and canonical["relation_references_preserved"] is True and canonical["generic_adapter_not_used"] is True,
         "Canonical Handle-only correction or same-draft lineage differs")
    repair_controls = load(folder, "KNOWN_DRAFT_REPAIR_CONTROLS.json")
    recipe_sha = "e11b7f1426e28fbe0b3407dad777fb9ae4287213e1f5eabc96ad22f9bf36b8d2"
    need(repair_controls["result"] == "MOCKED_KNOWN_DRAFT_REPAIR_CONTROLS_PASS"
         and repair_controls["recipe_sha256"] == recipe_sha
         and repair_controls["driver_sha256"] == b["driver_sha256"]
         and repair_controls["source_manifest_sha256"] == b["source_manifest_sha256"]
         and repair_controls["original_tool_sha256"] == "a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"
         and repair_controls["known_record_id"] == 23423736 and repair_controls["controls"] == 40
         and all(repair_controls[k] is False for k in ("credentials_read", "network_accessed", "real_mutations", "driver_imported", "upload_tool_imported"))
         and repair_controls["unchanged_upload_tool_functions_ast_extracted"] is True,
         "Isolated exact known-draft repair controls differ")
    repair_count = 0
    for case in repair_controls["cases"]:
        need(case["control_pass"] is True and case["intended_guard_hit"] is True, "A known-draft path guard control failed")
        repair_count += 1
        for probe in case.get("wrapper_negative_controls", []):
            need(probe["control_pass"] is True, "A known-draft wrapper scope control failed")
            repair_count += 1
    need(repair_count == 40, "Exact known-draft control count differs")
    repair = load(folder, "KNOWN_DRAFT_REPAIR.json")
    need(repair["result"] == "PASS" and repair["record_id"] == 23423736
         and repair["deposition_creations_total"] == 1 and repair["published"] is False
         and repair["removed_old_unpublished_ZIPs"] == 1 and repair["uploaded_new_ZIPs"] == 1
         and repair["PDF_bytes_unchanged"] is True and repair["all_supplied_metadata_exact"] is True
         and repair["metadata_normalizations"] == [] and repair["current_source_manifest_sha256"] == b["source_manifest_sha256"]
         and repair["original_upload_tool_unchanged"] is True and repair["case_adapter_used"] is False,
         "Actual known-draft replacement result differs")
    intent = load(folder, "ZIP_REPLACEMENT_INTENT.json")
    deletion = load(folder, "ZIP_DELETION_RECEIPT.json")
    need(intent["known_record_id"] == 23423736 and intent["submitted"] is False
         and intent["only_file_removed"] == "source-and-verification.zip"
         and intent["old_size"] == 338686 and intent["old_md5"] == "babfffb7532b65eb989af4700d04351a"
         and intent["old_sha256"] == "5a6ebbfa082458149a633e13b5ae0f5b7dccb04aca90cfd43771fc75f7a2568a"
         and intent["replacement_size"] == by_path["source-and-verification.zip"]["bytes"]
         and intent["replacement_sha256"] == by_path["source-and-verification.zip"]["sha256"]
         and intent["unchanged_PDF_sha256"] == by_path["output/pdf/paper.pdf"]["sha256"]
         and intent["source_manifest_sha256"] == b["source_manifest_sha256"]
         and intent["readiness_sha256"] == b["readiness_at_publication_sha256"]
         and intent["creation_requests_prohibited"] is True
         and deletion["record_id"] == 23423736 and deletion["file_id"] == intent["old_file_id"]
         and deletion["only_file"] == "source-and-verification.zip" and deletion["HTTP_status"] == 204
         and deletion["empty_body"] is True and deletion["PDF_not_mutated"] is True,
         "Actual exact old-ZIP removal intent or empty-204 receipt differs")
    driver = load(folder, "DRIVER_CONTROLS.json")
    need(driver["result"] == "MOCKED_GUARDS_PASS" and driver["driver_sha256"] == b["driver_sha256"]
         and driver["source_manifest_sha256"] == b["source_manifest_sha256"]
         and driver["real_six_files_exact"] is True and driver["required_guard_repairs_remaining"] == []
         and driver["credentials_loaded"] is False and driver["network_or_real_upload_invocations"] == 0,
         "Mocked production-guard controls differ")
    need(any(r["case"] == "actual_terminal_gate_read_only" and r["accepted"] is True for r in driver["controls"]), "Actual completed terminal gate was not independently exercised")
    public = load(folder, "PUBLIC_VERIFICATION.json")
    need(public["result"] == "PASS_PUBLIC_EXACT_METADATA_PAYLOADS_AND_DOI"
         and public["record_id"] == b["record_id"] and public["doi"] == b["doi"]
         and b["doi"] == "10.5281/zenodo."+str(b["record_id"])
         and public["source_manifest_sha256"] == b["source_manifest_sha256"]
         and public["metadata_file_sha256"] == by_path["zenodo-metadata.json"]["sha256"]
         and public["every_supplied_metadata_value_exact"] is True and public["DOI"]["HTTP_status"] == 200
         and public["credentials_loaded"] is False and public["HTTP_bodies_saved"] is False,
         "Public custody or all-supplied-metadata verification is incomplete")
    payloads = public["public_files"]
    need(isinstance(payloads, list) and len(payloads) == 2 and {r["name"] for r in payloads} == {"paper.pdf", "source-and-verification.zip"}, "Exact public payload list differs")
    for r in payloads:
        expected = by_path["output/pdf/paper.pdf" if r["name"] == "paper.pdf" else r["name"]]
        need(r["bytes"] == expected["bytes"] and r["sha256"] == expected["sha256"] and r["HTTP_status"] == 200, "Downloaded public payload bytes differ")
    tracker = load(folder, "TRACKER_VERIFICATION.json"); row = b["tracker_expected_four_cells"]
    need(isinstance(row, list) and len(row) == 4 and all(isinstance(v, str) for v in row), "Four expected tracker cells required")
    need(tracker["result"] == "PASS_TRACKER_EXACT_FOUR_CELLS" and tracker["spreadsheet_id"] == b["tracker_spreadsheet_id"]
         and tracker["requested_range"] == b["tracker_range"]
         and tracker["exact_row_sha256"] == digest(json.dumps(row, ensure_ascii=False, separators=(",", ":")).encode())
         and tracker["sheet_mutation_methods_invoked"] == 0 and tracker["read_only_GWS_private_override_used"] is True,
         "Tracker exact row verification is incomplete")
    need(tracker["exact_requested_and_returned_four_cell_range"] is True, "Tracker did not verify the exact requested and returned range")
    need(len(tracker["cells"]) == 4, "Tracker cell receipt count differs")
    for i,(r,v) in enumerate(zip(tracker["cells"], row)):
        need(r["column_offset"] == i and r["UTF8_bytes"] == len(v.encode())
             and r["sha256"] == digest(v.encode()) and r["exact"] is True, "Tracker cell custody differs")
    scope = load(folder, "MERGE_SCOPE.json"); merge = scope["actual_merge"]
    need(scope["result"] == "PASS_ACTUAL_EXACT_MERGE" and scope["original_scientific_head"] == H
         and scope["original_parent"] == PARENT and scope["original_complete_tree_exact"] is True
         and merge["sha"] == b["merge_commit"] and merge["parents"] == [b["premerge_main"], b["final_pr_head"]]
         and merge["tree"] == scope["premerge_scope"]["expected_tree"]
         and merge["all_original_58_blobs_exact"] is True
         and merge["only_own_candidate_queue_row_changed"] is True
         and merge["every_other_path_preserved_from_premerge_main"] is True
         and scope["no_Git_or_remote_mutations"] is True, "Actual full-Merkle merge or parent scope differs")
    need(scope["premerge_scope"]["base"] == b["premerge_main"]
         and scope["premerge_scope"]["original_additions"] == 58
         and scope["premerge_scope"]["all_other_paths_modes_and_objects_preserved"] is True,
         "Premerge main scope binding differs")
    if b["final_pr_head"] != H:
        integration = scope["integration"]
        need(integration["head"] == b["final_pr_head"] and integration["base"] == b["integration_base"]
             and integration["parents"] == [H, b["integration_base"]]
             and integration["original_scientific_head_preserved"] is True,
             "Administrative integration does not preserve the exact original scientific head")
    else:
        need("integration" not in scope, "Unexpected administrative integration receipt")
    verdict = load(folder, "VERDICT.json")
    need(verdict["result"] == "PASS_ADMINISTRATIVE_CUSTODY_AND_EXACT_MERGE_SCOPE"
         and verdict["completed"] is True and verdict["additional_whole_preprint_review"] is False
         and type(verdict["required_administrative_issues"]) is int and verdict["required_administrative_issues"] == 0
         and verdict["historical_priority_certified"] is False and verdict["human_peer_review_certified"] is False
         and verdict["formal_proof_certified"] is False, "Final administrative verdict missing or overstated")
    counts = {"driver": all_controls(driver), "known_draft_repair": repair_count, "public_metadata": all_controls(public),
              "tracker": all_controls(tracker), "Merkle": all_controls(scope)}
    need(counts == b["control_counts"] == {"driver": 49, "known_draft_repair": 40, "public_metadata": 13, "tracker": 18, "Merkle": 7}, "Final meaningful control counts differ")
    package_replay = False
    if package:
        need(digest((package/"source/MANIFEST.json").read_bytes()) == b["source_manifest_sha256"]
             and digest((package/"source/verify_source.py").read_bytes()) == b["source_checker_sha256"], "External source/checker pin differs")
        for r in inventory:
            raw = (package/r["path"]).read_bytes()
            need(len(raw) == r["bytes"] and digest(raw) == r["sha256"], "External six artifact bytes differ")
        run = subprocess.run([sys.executable, "-I", "-B", str(package/"source/verify_source.py"), "--expected-manifest-sha256", b["source_manifest_sha256"], "--pdf", str(package/"output/pdf/paper.pdf")], cwd="/", capture_output=True, text=True, timeout=120)
        need(run.returncode == 0 and not run.stderr and json.loads(run.stdout) == source, "External exact source custody replay differs")
        package_replay = True
    return {"result": "PASS", "packet_files_including_manifest": len(names)+1,
            "manifest_sha256": external_pin, "source_manifest_sha256": b["source_manifest_sha256"],
            "doi": b["doi"], "merge_commit": b["merge_commit"], "control_counts": counts,
            "external_source_PDF_custody_replayed": package_replay,
            "scope": "Administrative custody and exact merge scope; no additional mathematical, priority, human-review or formal certification."}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expected-manifest-sha256", required=True); p.add_argument("--packet", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--package", type=Path); a = p.parse_args()
    try:
        result = check(a.packet, a.expected_manifest_sha256, a.package.resolve() if a.package else None)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({"result": "FAIL", "reason": type(e).__name__+": "+str(e)})); sys.exit(1)
    print(json.dumps(result, indent=2))
