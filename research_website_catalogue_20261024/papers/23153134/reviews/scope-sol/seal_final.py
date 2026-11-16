"""One-use finite data custody and full frozen-source guard; no science or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
P = R.parents[3]
S = P / "papers/23153134/sources"
CONTROLS = {"FINAL.json", "OWNED_MANIFEST.json"}
def pin(p):
    raw = p.read_bytes()
    return {"bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest(),
            "mode": format(stat.S_IMODE(p.stat().st_mode), "04o")}
def match(p, item):
    actual = pin(p)
    assert actual["bytes"] == item["bytes"] and actual["SHA256"] == item["SHA256"], str(p)
    if "mode" in item:
        assert int(actual["mode"], 8) == int(item["mode"], 8), str(p)

assert pin(R / "INITIAL_SEAL.json")["SHA256"] == "b1d5435857fbc1cfd75366f30781d08875dee3eacc4983a1385858f090193633"
initial = json.loads((R / "INITIAL_SEAL.json").read_text())
for item in initial["files"]:
    match(R / item["path"], item)
sp = json.loads((R / "SOURCE_PINS.json").read_text())
for item in sp["source_controls_by_reference"]:
    match(P / item["path"], item)
sm = json.loads((S / "SOURCE_MANIFEST.json").read_text())
source_entries = {item["path"]: item for item in sm["files"]}
for item in sp["source_controls_by_reference"][:2]:
    source_entries[Path(item["path"]).name] = item
actual_source_files, actual_source_dirs = [], []
for path in sorted(S.rglob("*")):
    assert not path.is_symlink(), str(path)
    rel = path.relative_to(S).as_posix()
    if path.is_dir():
        actual_source_dirs.append(rel)
    else:
        assert stat.S_ISREG(path.stat().st_mode), str(path)
        actual_source_files.append(rel)
assert len(source_entries) == 94 and set(actual_source_files) == set(source_entries)
assert actual_source_dirs == sorted(x["path"] for x in sm["directories"]) and len(actual_source_dirs) == 4
for rel, item in source_entries.items():
    match(S / rel, item)
for item in sm["directories"]:
    assert stat.S_IMODE((S / item["path"]).stat().st_mode) == int(item["mode"], 8)
now = datetime.now(timezone.utc).isoformat()
guard = {"schema": "full-immutable-native-source-post-run-guard-v1", "record_id": 23153134,
         "UTC": now, "baseline": sp["source_controls_by_reference"][:2],
         "baseline_predates_native_execution": True,
         "fresh_pre_execution_rehash_of_all_94_files_claimed": False,
         "actual_post_execution_regular_files_matched": 94, "actual_child_directories_matched": 4,
         "all_file_bytes_SHA256_modes_matched": True, "all_directory_paths_modes_matched": True,
         "extra_missing_changed_files_or_directories": [], "symlinks_or_special_files": [],
         "native_asset_count_preserved": 9, "all_14_initial_owned_files_unchanged": True,
         "scope": "One bounded data-only comparison against the exact pre-existing frozen source manifest plus its two terminal-control pins; not scientific execution or acceptance."}
(R / "SOURCE_GUARD.json").write_text(json.dumps(guard, indent=2) + "\n")

pr = json.loads((R / "PRIMARY_READINGS.json").read_text())
base = Path(pr["raw_primary_base"])
for item in pr["bodies"] + pr["reading_aids"]:
    match(base / item["file"], item)
for item in pr["images"]:
    match(Path(pr["image_bases"][item["base"]]) / item["file"], item)
receipt = json.loads((R / "NATIVE_RUN_RECEIPT.json").read_text())
for item in [receipt["stdout"], receipt["stderr"]]:
    match(R / item["path"], item)
payload, dirs = [], []
for path in sorted(R.rglob("*")):
    assert not path.is_symlink(), str(path)
    rel = path.relative_to(R).as_posix()
    if path.is_dir():
        dirs.append(rel)
    else:
        assert stat.S_ISREG(path.stat().st_mode), str(path)
        if rel not in CONTROLS:
            payload.append({"path": rel, **pin(path)})
assert len(payload) == 23 and dirs == ["native-run", "rasters"]
manifest = {"schema": "finite-independent-scientific-scope-owned-manifest-v1", "record_id": 23153134,
            "UTC": now, "actual_regular_files": 25, "payload_files": 23, "child_directories": dirs,
            "symlinks": [], "other_special_files": [], "exact_terminal_controls": sorted(CONTROLS),
            "no_wildcard_subtree_runtime_or_future_exclusions": True, "files": payload}
(R / "OWNED_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
final = {"schema": "finite-original-scientific-scope-final-v1", "record_id": 23153134, "row": 166,
         "UTC": now, "status": "COMPLETE_SEALED_QUIESCENT", "completion_percent": 100,
         "owned_root": "papers/23153134/reviews/scope-sol", "actual_regular_files": 25,
         "payload_files": 23, "child_directories": dirs,
         "pins": {n: pin(R / n) for n in ["OWNED_MANIFEST.json", "REPORT.md", "PRIMARY_READINGS.json", "SOURCE_GUARD.json", "NATIVE_RUN_RECEIPT.json", "INITIAL_SEAL.json"]},
         "all_14_source_first_files_unchanged": True, "full_94_file_source_guard": "SOURCE_GUARD.json",
         "original_claim_disposition_and_evidence": "REPORT.md; mathematical findings withheld until root own INITIAL",
         "central_unresolved_mathematical_gap": None,
         "primary_body_references": 9, "new_acquisitions_or_literature_campaigns": 0,
         "native_ordinary_attempts": 1, "native_exit": receipt["exit_code"],
         "native_scope": "Supplementary finite controls only; not a numerical Nash map or global proof certificate",
         "optimized_selftest_harness_retry_or_other_native_runs": 0,
         "standalone_audit_results_README_and_archived_current_opinion_bodies_opened": False,
         "current_family_math_findings_shared_or_opened": False,
         "findings_withheld_until_root_own_INITIAL": True,
         "publication_authority": False, "AA": None, "canonical_url": None, "followup": None,
         "source_W_Git_Sheet_old_packet_or_external_contact_modifications": False,
         "quiescent_after_seal": True}
(R / "FINAL.json").write_text(json.dumps(final, indent=2) + "\n")
for item in payload:
    match(R / item["path"], item)
assert len([x for x in R.rglob("*") if x.is_file()]) == 25
print(json.dumps({"actual_regular_files": 25, "child_directories": dirs,
                  "pins": {n: pin(R / n) for n in ["FINAL.json", "OWNED_MANIFEST.json", "REPORT.md", "PRIMARY_READINGS.json", "SOURCE_GUARD.json", "NATIVE_RUN_RECEIPT.json"]}}, indent=2))
