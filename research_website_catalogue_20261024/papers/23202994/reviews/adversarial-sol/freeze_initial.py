"""Passive INITIAL receipt/seal writer; no science execution or network.

Both terminal files are created and opened before final inventory, made read
only together with all payloads, and filled through their existing handles.
Only their recursive contents are omitted; both actual nodes/modes remain in
the complete topology. No file is created or changed after those handles close.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parents[1] / "sources"
TERMINALS = {"INITIAL_MANIFEST.json", "INITIAL_SEAL.json"}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "mode_octal": oct(stat.S_IMODE(path.lstat().st_mode))}


def main():
    before = json.loads((LANE / "SOURCE_GUARD_BEFORE.json").read_text())
    after = json.loads((LANE / "SOURCE_GUARD_AFTER.json").read_text())
    assert before["entries"] == after["entries"] and after["before_after_exact"]
    for entry in after["entries"]:
        path = SOURCE / entry["path"]
        assert oct(stat.S_IMODE(path.lstat().st_mode)) == entry["mode_octal"]
        if entry["kind"] == "file":
            observed = pin(path)
            assert observed["bytes"] == entry["bytes"] and observed["sha256"] == entry["sha256"]
        else:
            assert (not any(path.iterdir())) == entry["empty"]
    assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*")} == {e["path"] for e in after["entries"] if e["path"] != "."}
    api = json.loads((SOURCE / "native-metadata/record-api.json").read_text())
    assert api["id"] == 23202994 and api["metadata"]["version"] == "1.0.0"
    receipt = {"UTC": utc(), "phase": "INITIAL_ONLY", "record_id": 23202994,
               "source_guard_before": pin(LANE / "SOURCE_GUARD_BEFORE.json"),
               "source_guard_after": pin(LANE / "SOURCE_GUARD_AFTER.json"),
               "source_before_after_exact": True, "source_files": 39, "source_child_directories": 15,
               "controlling_tex": dict(pin(SOURCE / "archives/01-source-and-verification.zip.extracted/publication/main.tex"), complete_original_read=True),
               "outer_pdf": dict(pin(SOURCE / "zenodo-files/paper.pdf"), complete_five_page_text_read=True),
               "fresh_extracted_pdf_text": pin(LANE / "native-paper-layout.txt"),
               "fresh_page_images": [dict(pin(LANE / f"native-page-{i}.png"), native_page=i,
                                           individually_personally_viewed=True, tool="local view_image") for i in range(1, 6)],
               "native_api": dict(pin(SOURCE / "native-metadata/record-api.json"), full_json_and_description_read=True),
               "native_html": dict(pin(SOURCE / "native-metadata/record-page.html"), full_visible_metadata_description_and_meta_tags_read=True),
               "native_version_field_present": True, "native_version": "1.0.0",
               "native_asset_order": [f["key"] for f in api["files"]],
               "passive_metadata_code_read_before_execution": dict(pin(LANE / "read_native_metadata.py"), complete_body_personally_read_before_execution=True),
               "scientific_execution": False, "scientific_import_AST_test_compile_build_repair": False,
               "network_or_primary_literature_fetch": False, "README_support_review_audit_code_or_peer_findings_read": False,
               "unavoidable_original_author_assertions": "Recorded separately in INDEPENDENCE_LEDGER.md; not adopted as proof.",
               "initial_assignment_completion_percent": 100,
               "next_action": "STOP pending root checkpoint and explicit RESUME into a new sibling lane."}
    (LANE / "NATIVE_READING_COVERAGE.json").write_text(json.dumps(receipt, indent=2) + "\n")
    with (LANE / "RESEARCH_LOG.md").open("a") as log:
        log.write("\n- " + utc() + ": Complete original TeX, all five native PDF text pages and individually viewed fresh page images, full native API and visible HTML metadata/Description read. Independent hand reconstruction, falsification attempts, external-interface limitations and exposure ledger recorded before any support or imported literature. Entire39-file/15-child-directory source before/after guard exact. INITIAL completion100%; independently verified unconditional mathematics35%. No science execution or source mutation. Proceeding solely to finite INITIAL seal, then STOP for root checkpoint and explicit RESUME; any continuation must use a new sibling.\n")
    mp, sp = (LANE / n for n in ("INITIAL_MANIFEST.json", "INITIAL_SEAL.json"))
    assert not mp.exists() and not sp.exists()
    with mp.open("x") as manifest_stream, sp.open("x") as seal_stream:
        for path in LANE.rglob("*"):
            assert path.is_file(), "Unexpected child directory or nonregular entry"
            path.chmod(0o444)
        LANE.chmod(0o555)
        payload, topology = [], []
        for path in [LANE, *sorted(LANE.rglob("*"))]:
            relative = "." if path == LANE else path.relative_to(LANE).as_posix()
            info = path.lstat()
            kind = "directory" if stat.S_ISDIR(info.st_mode) else "file" if stat.S_ISREG(info.st_mode) else "other"
            assert kind in ("directory", "file")
            row = {"path": relative, "kind": kind, "mode_octal": oct(stat.S_IMODE(info.st_mode)),
                   "hidden_component": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
            if kind == "directory":
                row["empty"] = not any(path.iterdir())
            topology.append(dict(row))
            if relative in TERMINALS:
                continue
            if kind == "file":
                row.update({k: v for k, v in pin(path).items() if k != "path"})
                row["empty"] = row["bytes"] == 0
            payload.append(row)
        stamp = utc()
        manifest = {"schema": "finite-original-only-initial-manifest-v1", "UTC": stamp,
                    "root": str(LANE), "payload_entries": payload,
                    "entire_actual_topology_including_already_created_terminal_pair": topology,
                    "excluded_recursive_terminal_contents_only": sorted(TERMINALS),
                    "control_rule": "Both terminal nodes already exist in actual inventory; only their recursive contents are excluded. Seal pins manifest and root externally pins seal. Both terminal files are nonempty at closure.",
                    "actual_files_including_controls": sum(e["kind"] == "file" for e in topology),
                    "actual_child_directories": sum(e["kind"] == "directory" for e in topology) - 1,
                    "hidden_entries": [e["path"] for e in topology if e["hidden_component"]],
                    "empty_payload_files": [e["path"] for e in payload if e["kind"] == "file" and e["empty"]],
                    "empty_directories": [e["path"] for e in topology if e["kind"] == "directory" and e["empty"]],
                    "initial_assignment_completion_percent": 100, "follow_up": None}
        manifest_stream.write(json.dumps(manifest, indent=2) + "\n")
        manifest_stream.flush()
        os.fsync(manifest_stream.fileno())
        seal = {"schema": "finite-original-only-initial-seal-v1", "UTC": stamp,
                "status": "INITIAL_FROZEN_QUIESCENT_PENDING_ROOT_CHECKPOINT_AND_EXPLICIT_RESUME",
                "root": str(LANE), "manifest": pin(mp),
                "actual_files": manifest["actual_files_including_controls"],
                "actual_child_directories": manifest["actual_child_directories"],
                "root_mode": "0o555", "all_file_modes": "0o444",
                "source_before_after_exact": True, "source_files": 39, "source_child_directories": 15,
                "required_original_reading_coverage_complete": True,
                "scientific_execution_or_network": False, "support_or_imported_primary_reading": False,
                "mathematical_findings_transmitted_to_root": False,
                "initial_assignment_completion_percent": 100, "follow_up": None,
                "next_action": "STOP. Later work requires root checkpoint and explicit RESUME in a new sibling; this namespace stays unchanged."}
        seal_stream.write(json.dumps(seal, indent=2) + "\n")
        seal_stream.flush()
        os.fsync(seal_stream.fileno())
    assert mp.stat().st_size > 0 and sp.stat().st_size > 0
    assert {p.relative_to(LANE).as_posix() for p in LANE.rglob("*")} == {e["path"] for e in topology if e["path"] != "."}
    for entry in payload:
        path = LANE / entry["path"]
        assert oct(stat.S_IMODE(path.lstat().st_mode)) == entry["mode_octal"]
        if entry["kind"] == "file":
            assert pin(path)["sha256"] == entry["sha256"]
    print(json.dumps({"manifest": pin(mp), "seal": pin(sp),
                      "actual_files": seal["actual_files"], "child_directories": seal["actual_child_directories"],
                      "hidden_entries": manifest["hidden_entries"], "empty_payload_files": manifest["empty_payload_files"]}, indent=2))


if __name__ == "__main__":
    main()
