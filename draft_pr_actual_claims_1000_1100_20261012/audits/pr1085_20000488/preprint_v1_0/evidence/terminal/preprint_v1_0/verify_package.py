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
            "publication_ready": False, "new_whole_reviews": 0,
            "scope": "Finite custody and declared-scope checks only. Universal proofs are in paper.tex; new whole reviews and root adoption are pending."}

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
