#!/usr/bin/env python3
"""Strict custody, scope, metadata, archive and optional upload-binding checks.
A PASS is a finite package check, not a proof certificate or review clearance.
"""
import argparse, io, os, zipfile
from pathlib import Path
from kit_common import ROOT, ARCHIVE, FIXED_TIME, require, regular, read_json, members, sha, emit, safe_output
from metadata_constants import EXPECTED_METADATA

def verify(check_archive=True, check_deposit=True, deposit=None, require_deposit=False):
    names = members()  # preflight every input, including self-hash-excluded manifest
    manifest = read_json(ROOT / "SUPPORT_MANIFEST.json")
    require(set(manifest) == {"schema", "files", "self_hash_excluded", "archive_policy"}, "manifest schema")
    require(manifest["schema"] == 1 and type(manifest["schema"]) is int, "manifest schema type")
    require(manifest["self_hash_excluded"] == ["SUPPORT_MANIFEST.json"], "only manifest self excluded")
    require(manifest["archive_policy"] == "Sorted ZIP; deflate9; 2026-10-14T00:00:00; Unix regular0644", "archive policy")
    rows = manifest["files"]
    require(isinstance(rows, list) and [r["path"] for r in rows] == names, "exact manifest membership/order")
    for row in rows:
        require(set(row) == {"path", "bytes", "sha256"}, "pin schema")
        require(type(row["bytes"]) is int and row["bytes"] >= 0, "pin size type")
        data = regular(ROOT / row["path"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "payload changed: " + row["path"])
    status = read_json(ROOT / "STATUS.json")
    for key in ["publication_ready", "all_actionable_issues_resolved", "published",
                "embedded_eigenvalues_excluded", "all_coupling_absence_for_one_fixed_nonzero_graph",
                "general_n_ge_4_nongraph_classification", "human_peer_review", "formal_proof_certificate"]:
        require(status.get(key) is False, "forbidden promotion: " + key)
    require(type(status.get("new_whole_package_reviews")) is int and status["new_whole_package_reviews"] == 0, "new reviews pending")
    require(type(status.get("minimum_new_whole_package_reviews")) is int and status["minimum_new_whole_package_reviews"] == 2, "two new reviews required")
    require(status["pr"] == 1085 and type(status["pr"]) is int and status["problem_id"] == 20000488, "target identity")
    require(status["audited_head"] == "5e23f0c801d23976830657d2eef2b32bdc7da05a", "audited head")
    require(status["framing"] == "CREDITED_EXPOSITION_AND_PRIOR_THEOREM_COROLLARIES", "framing")
    for key in ["novelty", "worldwide_open_status", "independent_discovery"]:
        require(status.get(key) == "UNKNOWN", "unestablished historical predicate")
    require(status["priority"] == "UNKNOWN_EXACT_REMAINING_GEOMETRIC_FORMULATIONS", "priority")
    require(status["services_hold"] == "preceding PR1032 priority cursor", "publication order hold")
    source = read_json(ROOT / "SOURCE_METADATA.json")
    for key in ["novelty", "worldwide_open_status", "independent_discovery"]:
        require(source.get(key) == "UNKNOWN", "source historical scope")
    require(source["third_party_bodies_distributed"] is False, "copyright body scope")
    require(len(source["credit_required"]) == 5, "required source mechanisms")
    meta = read_json(ROOT / ".zenodo.json")
    wrapper = read_json(ROOT / "metadata.json")
    require(set(wrapper) == {"metadata"}, "metadata wrapper schema")
    require(meta == wrapper["metadata"] == EXPECTED_METADATA, "exact bibliographic metadata")
    baseline = read_json(ROOT / "PREPARATION_INPUT_PINS.json")["files"]
    frozen = {r["path"]: r for r in baseline}
    require(len(frozen) == len(baseline), "unique frozen input names")
    copies = read_json(ROOT / "COPY_MAP.json")["files"]
    excluded = read_json(ROOT / "EXCLUSIONS.json")["files"]
    copy_sources = [r["source_relative_audit"] for r in copies]
    excluded_sources = [r["path"] for r in excluded]
    require(len(set(copy_sources)) == len(copies) and len(set(excluded_sources)) == len(excluded), "unique custody maps")
    require(set(copy_sources).isdisjoint(excluded_sources) and set(copy_sources+excluded_sources) == set(frozen), "complete per-source copy/exclusion partition")
    require(len({r["copy"] for r in copies}) == len(copies), "unique copy destinations")
    for row in copies:
        old = frozen[row["source_relative_audit"]]
        require(row["bytes"] == old["bytes"] and row["sha256"] == old["sha256"], "copy map frozen source")
        require(row["copy"] == "evidence/" + row["source_relative_audit"] and row["copy"] in names, "copy destination")
        data = regular(ROOT / row["copy"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "historical copied bytes")
    for row in excluded:
        old = frozen[row["path"]]
        require(row["bytes"] == old["bytes"] and row["sha256"] == old["sha256"] and bool(row["reason"]), "individual exclusion custody")
    # Original STATUS is an immutable preparation snapshot; terminal accounting
    # is separate and cannot itself confer root release readiness.
    terminal = read_json(ROOT / "TERMINAL_ACCOUNTING.json")
    require(type(terminal.get("schema")) is int and terminal["schema"] == 1, "terminal schema")
    require(terminal.get("pr") == 1085 and type(terminal["pr"]) is int and
            terminal.get("problem_id") == 20000488 and
            terminal.get("audited_head") == status["audited_head"], "terminal identity")
    require(terminal.get("status") == "TERMINAL_ADMIN_CHECKED_PENDING_ROOT_INTEGRITY_ADOPTION", "terminal stage")
    for key in ["whole_reviews_completed", "minimum_whole_reviews"]:
        require(type(terminal.get(key)) is int and terminal[key] == 2, "terminal two reviews: " + key)
    require(type(terminal.get("latest_actionable_P0_P1_P2_P3")) is int and
            terminal["latest_actionable_P0_P1_P2_P3"] == 0, "latest review zero findings")
    require(terminal.get("root_terminal_integrity_adoption_required") is True and
            terminal.get("historical_STATUS_preserved") is True, "root adoption and historical stage")
    for key in ["publication_ready", "all_actionable_issues_resolved", "published",
                "human_peer_review", "formal_proof_certificate"]:
        require(terminal.get(key) is False, "terminal forbidden promotion: " + key)
    require(terminal.get("services_hold") == status["services_hold"], "terminal ordered hold")
    for key in ["priority", "novelty", "worldwide_open_status", "independent_discovery"]:
        require(terminal.get(key) == status[key], "terminal historical scope: " + key)
    for name, key in [("paper.pdf", "paper_pdf_sha256"), ("paper.tex", "paper_tex_sha256")]:
        require(sha(regular(ROOT / name).read_bytes()) == terminal.get(key), "unchanged paper identity")
    terminal_inputs = read_json(ROOT / "TERMINAL_INPUT_PINS.json")["files"]
    terminal_frozen = {r["path"]: r for r in terminal_inputs}
    require(len(terminal_frozen) == len(terminal_inputs), "unique terminal input paths")
    terminal_copies = read_json(ROOT / "TERMINAL_COPY_MAP.json")["files"]
    terminal_exclusions = read_json(ROOT / "TERMINAL_EXCLUSIONS.json")["files"]
    selected_paths = [r["source_relative_audit"] for r in terminal_copies]
    excluded_paths = [r["path"] for r in terminal_exclusions]
    require(len(set(selected_paths)) == len(selected_paths) and
            len(set(excluded_paths)) == len(excluded_paths) and
            set(selected_paths).isdisjoint(excluded_paths) and
            set(selected_paths + excluded_paths) == set(terminal_frozen), "terminal complete custody partition")
    require(len({r["copy"] for r in terminal_copies}) == len(terminal_copies), "unique terminal destinations")
    for row in terminal_copies:
        old = terminal_frozen[row["source_relative_audit"]]
        require(row["copy"] == "evidence/terminal/" + row["source_relative_audit"] and
                row["copy"] in names and row["bytes"] == old["bytes"] and
                row["sha256"] == old["sha256"], "terminal source/copy identity")
        data = regular(ROOT / row["copy"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "terminal exact copied bytes")
    for row in terminal_exclusions:
        old = terminal_frozen[row["path"]]
        require(row["bytes"] == old["bytes"] and row["sha256"] == old["sha256"] and
                isinstance(row.get("reason"), str) and bool(row["reason"]), "terminal individual exclusion")
    expected_evidence = [{"review": n,
        "verdict": "evidence/terminal/reviews/package_0" + str(n) + "/VERDICT.json",
        "output_pins": "evidence/terminal/reviews/package_0" + str(n) + "/OUTPUT_PINS.json",
        "seal": "evidence/terminal/reviews/package_0" + str(n) + ("/FINAL_SEAL.json" if n == 1 else "/SEAL.json"),
        "root_adoption": "evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_0" + str(n) + ".json"}
        for n in [1, 2]]
    require(terminal.get("review_evidence") == expected_evidence, "exact two review interfaces")
    for evidence in expected_evidence:
        verdict = read_json(ROOT / evidence["verdict"])
        adoption = read_json(ROOT / evidence["root_adoption"])
        seal = read_json(ROOT / evidence["seal"])
        output_hash = sha(regular(ROOT / evidence["output_pins"]).read_bytes())
        require(seal.get("output_pins_sha256") == adoption.get("output_pins_sha256") == output_hash,
                "exact reviewed output-manifest/root adoption binding")
        require(adoption.get("whole_reviews_completed") == evidence["review"] and
                type(adoption["whole_reviews_completed"]) is int and
                adoption.get("minimum_whole_reviews") == 2 and
                type(adoption.get("actionable_P0_P1_P2_P3")) is int and
                adoption["actionable_P0_P1_P2_P3"] == 0 and
                adoption.get("publication_ready") is False and adoption.get("published") is False and
                adoption.get("services_held_after_pr") == 1032, "root review adoption semantics")
        expected_status = ("ADOPT_COMPLETE_WHOLE01_ZERO_ACTIONABLE_PENDING_REQUIRED_NEW_WHOLE02"
                           if evidence["review"] == 1 else
                           "ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN")
        require(adoption.get("status") == expected_status, "captured root review stage")
        require(verdict.get("audited_head") == status["audited_head"] and
                verdict.get("pr") == 1085 and verdict.get("problem_id") == 20000488,
                "review verdict identity")
        if evidence["review"] == 1:
            require(verdict.get("verdict") == "ZERO_ACTIONABLE_P0_P1_P2_P3" and
                    verdict.get("findings") == [] and all(type(verdict.get(k)) is int and verdict[k] == 0
                    for k in ["P0", "P1", "P2", "P3"]), "whole01 zero finding semantics")
        else:
            require(verdict.get("status") == "PASS_ZERO_ACTIONABLE_P0_P1_P2_P3" and
                    verdict.get("actionable_findings") == [] and
                    verdict.get("root_adoption_required") is True and
                    verdict.get("publication_ready_set_by_this_review") is False and
                    all(type(verdict.get("severity_counts", {}).get(k)) is int and
                    verdict["severity_counts"][k] == 0 for k in ["P0", "P1", "P2", "P3"]),
                    "whole02 zero finding semantics")
    # The terminal stage above remains an exact dated snapshot. The later
    # case-alias repair cannot inherit its old zero-finding clearance.
    repair = read_json(ROOT / "CASE_ALIAS_REPAIR_ACCOUNTING.json")
    require(type(repair.get("schema")) is int and repair["schema"] == 1,
            "case repair schema")
    require(type(repair.get("pr")) is int and repair["pr"] == 1085 and
            type(repair.get("problem_id")) is int and repair["problem_id"] == 20000488 and
            repair.get("audited_head") == status["audited_head"], "case repair identity")
    require(repair.get("status") == "CASE_ALIAS_REPAIRED_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03" and
            repair.get("finding") == "CASE-1085" and repair.get("finding_severity") == "P3",
            "case repair pending stage")
    for key in ["historical_whole_reviews_completed", "minimum_whole_reviews"]:
        require(type(repair.get(key)) is int and repair[key] == 2, "case repair two historical reviews")
    for key in ["new_complete_whole03_required", "root_repair_adoption_required",
                "historical_STATUS_and_TERMINAL_ACCOUNTING_preserved"]:
        require(repair.get(key) is True, "case repair required review/adoption/history")
    for key in ["new_complete_whole03_completed", "publication_ready", "all_actionable_issues_resolved",
                "published", "human_peer_review", "formal_proof_certificate"]:
        require(repair.get(key) is False, "case repair forbidden promotion: " + key)
    require(repair.get("services_hold") == status["services_hold"], "case repair ordered hold")
    for key in ["priority", "novelty", "worldwide_open_status", "independent_discovery"]:
        require(repair.get(key) == status[key], "case repair historical scope: " + key)
    for key in ["paper_pdf_sha256", "paper_tex_sha256"]:
        require(repair.get(key) == terminal[key], "case repair unchanged paper")
    repair_map = read_json(ROOT / "CASE_ALIAS_REPAIR_COPY_MAP.json")
    require(type(repair_map.get("schema")) is int and repair_map["schema"] == 1,
            "case repair copy schema")
    repair_copies = repair_map["files"]
    expected_copies = ["evidence/case_alias01/" + n for n in ["FINDING_AND_REPAIR.md",
        "ROOT_CASE_ALIAS_SCOPE_REVIEW.json", "ROOT_TERMINAL_ADMIN_REVIEW_20261016.json",
        "before/kit_common.py", "before/README.md", "before/verify_package.py"]]
    require([r["copy"] for r in repair_copies] == expected_copies and
            len({r["source_relative_program"] for r in repair_copies}) == len(repair_copies),
            "case repair exact evidence membership")
    for row in repair_copies:
        require(set(row) == {"source_relative_program", "copy", "bytes", "sha256"} and
                type(row["bytes"]) is int and row["copy"] in names, "case repair copy fields")
        data = regular(ROOT / row["copy"]).read_bytes()
        require(len(data) == row["bytes"] and sha(data) == row["sha256"], "case repair copied bytes")
    hold = read_json(ROOT / expected_copies[2])
    require(hold.get("new_complete_whole03_required") is True and
            hold.get("publication_ready") is False and hold.get("published") is False and
            hold.get("services_held_after_pr") == 1032, "case repair root hold evidence")
    require(regular(ROOT / "paper.pdf").read_bytes().startswith(b"%PDF-"), "paper PDF signature")
    archive_verified = False
    archive = ROOT / ARCHIVE
    if check_archive and os.path.lexists(archive):
        data = regular(archive).read_bytes()
        expected = sorted(names + ["SUPPORT_MANIFEST.json"])
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            require(z.namelist() == expected and z.testzip() is None, "archive exact order/CRC")
            require(z.comment == b"", "archive comment")
            for info in z.infolist():
                require(info.date_time == FIXED_TIME and info.create_system == 3 and
                        info.external_attr == 0o100644 << 16 and
                        info.compress_type == zipfile.ZIP_DEFLATED and info.extra == b"" and
                        info.comment == b"" and info.flag_bits == 0, "archive static header")
                require(z.read(info.filename) == regular(ROOT / info.filename).read_bytes(), "archive payload")
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name in expected:
                info = zipfile.ZipInfo(name, FIXED_TIME)
                info.create_system = 3; info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, regular(ROOT / name).read_bytes(), compresslevel=9)
        require(stream.getvalue() == data, "closed deterministic ZIP bytes")
        archive_verified = True
    binding_verified = False
    descriptor = Path(deposit) if deposit else ROOT / "zenodo-deposit.json"
    if check_deposit and (require_deposit or os.path.lexists(descriptor)):
        regular(descriptor) # rejects dangling symlink as well as nonregular input
        dep = read_json(descriptor)
        require(set(dep) == {"metadata", "files"}, "repository deposit schema")
        require(dep["metadata"] == EXPECTED_METADATA, "exact deposit metadata")
        expected_files = [{"path": "paper.pdf", "name": "paper.pdf"},
                          {"path": ARCHIVE, "name": ARCHIVE}]
        require(dep["files"] == expected_files, "exact repository deposit paths")
        for item in dep["files"]:
            require((descriptor.parent / item["path"]).resolve() == (ROOT / item["name"]).resolve(), "deposit descriptor location binds actual files")
            regular(descriptor.parent / item["path"])
        binding = read_json(ROOT / "UPLOAD_BINDINGS.json")
        require(set(binding) == {"metadata", "files"}, "binding schema")
        require(binding["metadata"] == EXPECTED_METADATA, "exact binding metadata")
        require([x["filename"] for x in binding["files"]] == ["paper.pdf", ARCHIVE], "binding file order")
        for row in binding["files"]:
            require(set(row) == {"filename", "bytes", "sha256"} and type(row["bytes"]) is int, "binding file fields/types")
            body = regular(ROOT / row["filename"]).read_bytes()
            require(len(body) == row["bytes"] and sha(body) == row["sha256"], "exact attachment binding")
        binding_verified = True
    elif check_deposit and os.path.lexists(ROOT / "UPLOAD_BINDINGS.json"):
        # A leftover binding without a descriptor is not a self-contained kit.
        read_json(ROOT / "UPLOAD_BINDINGS.json")
    return {"passed": True, "payload_members_verified": len(names), "exact_historical_copies": len(copies),
            "individual_exclusions": len(excluded), "archive_verified": archive_verified,
            "external_deposit_binding_verified": binding_verified,
            "publication_ready": False, "new_whole_reviews": 2,
            "new_complete_whole03_required": True, "new_complete_whole03_completed": False,
            "terminal_exact_copies": len(terminal_copies), "terminal_individual_exclusions": len(terminal_exclusions),
            "scope": "Finite custody and declared-scope checks only. Universal proofs are in paper.tex; two historical complete whole reviews are recorded; the later case-alias repair requires external root adoption and NEW complete whole03, and services are held after PR1032."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output")
    p.add_argument("--deposit")
    p.add_argument("--require-deposit", action="store_true")
    args = p.parse_args()
    if args.output:
        safe_output(args.output, [args.deposit] if args.deposit else [])
    result = verify(deposit=args.deposit, require_deposit=args.require_deposit)
    emit(result, args.output, [args.deposit] if args.deposit else [])
if __name__ == "__main__":
    main()
