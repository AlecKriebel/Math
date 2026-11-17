"""Finite source-custody closure; no scientific reading, execution, or network."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

LANE = Path(__file__).resolve().parent


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "md5": hashlib.md5(data).hexdigest(), "mode_octal": oct(stat.S_IMODE(path.lstat().st_mode))}


def scan(root):
    entries = []
    for path in [root, *sorted(root.rglob("*"))]:
        metadata = path.lstat()
        relative = "." if path == root else path.relative_to(root).as_posix()
        kind = "directory" if stat.S_ISDIR(metadata.st_mode) else "file" if stat.S_ISREG(metadata.st_mode) else "other"
        assert kind != "other", f"Unexpected nonregular node: {path}"
        entry = {"path": relative, "kind": kind, "mode_octal": oct(stat.S_IMODE(metadata.st_mode)),
                 "hidden_component": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
        if kind == "file":
            entry.update({k: v for k, v in pin(path).items() if k != "path"})
        else:
            entry["empty"] = not any(path.iterdir())
        entries.append(entry)
    return entries


def main():
    assert not (LANE / "FINAL.json").exists()
    result = json.loads((LANE / "CUSTODY_RESULT.json").read_text())
    assert result["status"] == "pass"
    execution = json.loads((LANE / "EXECUTION_RESULT.json").read_text())
    assert execution["exit_status"] == 0 and execution["retry_count"] == 0
    pins = json.loads((LANE / "EXTERNAL_SOURCE_PINS.json").read_text())
    source_guards = []
    for record in pins["records"]:
        root = Path(record["source_root"])
        for label in ("manifest", "final"):
            observed = pin(Path(record[label]["path"]))
            assert all(observed[k] == record[label][k] for k in ("bytes", "sha256", "md5"))
        manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
        actual = scan(root)
        payload = [e for e in actual if e["path"] not in ("SOURCE_MANIFEST.json", "SOURCE_FINAL.json")]
        assert payload == manifest["entries"]
        assert all(e["mode_octal"] == "0o644" for e in actual if e["path"] in ("SOURCE_MANIFEST.json", "SOURCE_FINAL.json"))
        source_guards.append({"record_id": record["record_id"], "root": str(root),
                              "exact_terminal_exclusions": manifest["excluded_control_files"],
                              "all_actual_entries_including_controls": actual,
                              "files": sum(e["kind"] == "file" for e in actual),
                              "child_directories": sum(e["kind"] == "directory" for e in actual) - 1,
                              "manifest_and_final_match_external_pins": True})
    (LANE / "SOURCE_CLOSURE_GUARDS.json").write_text(json.dumps({"UTC": utc(), "records": source_guards}, indent=2) + "\n")
    completion = {"UTC": utc(), "status": "SOURCE_ACQUISITION_COMPLETE_NO_SCIENTIFIC_REVIEW",
                  "source_custody_completion_percent": 100, "scientific_review_completion_percent": 0,
                  "record_ids": [r["record_id"] for r in pins["records"]],
                  "published_native_asset_count": sum(r["published_assets"] for r in pins["records"]),
                  "total_archive_members": sum(r["archive_members"] for r in pins["records"]),
                  "full_namespace_checks": "pass", "transfer_failures": 0, "network_retries": 0,
                  "scientific_support_proof_code_read": False, "scientific_scripts_imported_or_executed": False,
                  "existing_packets_touched": False, "git_worksheet_website_deploy_release_zenodo_mutations": False,
                  "contact_or_outreach_preparation": False, "prior189_findings": "WITHHELD",
                  "follow_up": None}
    (LANE / "COMPLETION.json").write_text(json.dumps(completion, indent=2) + "\n")
    with (LANE / "RESEARCH_LOG.md").open("a") as log:
        log.write("\n- " + utc() + ": Both source packets acquired and closed. Independent byte/mode/topology checks and every ZIP-member byte comparison passed; outer PDF metadata parsed read-only. Source custody completion 100%; scientific review 0%. No transfer errors or retries. Native API version is 1.0.0 for 23202994 and absent for 23204176. Final closure preserves exact source bytes and modes and seals this finite verification lane. No scientific findings supplied; prior189 findings remain withheld. Follow-up null; STOP after final seal.\n")
    for path in LANE.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    entries = scan(LANE)
    entries[0]["mode_octal"] = "0o555"
    topology = [{k: e[k] for k in ("path", "kind", "mode_octal", "hidden_component")}
                | ({"empty": e["empty"]} if e["kind"] == "directory" else {}) for e in entries]
    topology += [{"path": n, "kind": "file", "mode_octal": "0o444", "hidden_component": False}
                 for n in ("MANIFEST.json", "FINAL.json")]
    manifest = {"schema": "finite-source-acquisition-lane-manifest-v1", "UTC": utc(), "root": str(LANE),
                "entries": entries, "entire_final_topology": sorted(topology, key=lambda e: e["path"]),
                "excluded_terminal_control_contents": ["MANIFEST.json", "FINAL.json"],
                "control_rule": "Both terminal files included in topology/modes; final pins manifest; external root pins final; no circular self-hash claim.",
                "actual_files_including_controls": sum(e["kind"] == "file" for e in entries) + 2,
                "actual_child_directories": sum(e["kind"] == "directory" for e in entries) - 1,
                "hidden_entries": [e["path"] for e in entries if e["hidden_component"]],
                "empty_directories": [e["path"] for e in entries if e["kind"] == "directory" and e["empty"]]}
    mp = LANE / "MANIFEST.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n")
    mp.chmod(0o444)
    final = {"schema": "source-acquisition-lane-final-v1", "UTC": utc(),
             "status": completion["status"], "manifest": pin(mp),
             "external_source_pins": pin(LANE / "EXTERNAL_SOURCE_PINS.json"),
             "source_closure_guards": pin(LANE / "SOURCE_CLOSURE_GUARDS.json"),
             "custody_result": pin(LANE / "CUSTODY_RESULT.json"),
             "actual_files": manifest["actual_files_including_controls"],
             "actual_child_directories": manifest["actual_child_directories"],
             "all_payload_files_mode": "0o444", "root_mode": "0o555",
             "source_custody_completion_percent": 100, "scientific_review_completion_percent": 0,
             "sources_frozen_at_exact_external_pins": True, "source_modes_preserved": True,
             "scientific_findings_transmitted": False, "follow_up": None, "next_action": "STOP"}
    fp = LANE / "FINAL.json"
    fp.write_text(json.dumps(final, indent=2) + "\n")
    fp.chmod(0o444)
    LANE.chmod(0o555)
    assert {p.relative_to(LANE).as_posix() for p in LANE.rglob("*")} == {e["path"] for e in topology if e["path"] != "."}
    for entry in entries:
        path = LANE / entry["path"]
        assert oct(stat.S_IMODE(path.lstat().st_mode)) == entry["mode_octal"]
        if entry["kind"] == "file":
            assert pin(path)["sha256"] == entry["sha256"]
    print(json.dumps({"manifest": pin(mp), "final": pin(fp),
                      "actual_files": final["actual_files"], "child_directories": final["actual_child_directories"]}, indent=2))


if __name__ == "__main__":
    main()
