"""One-use finite data-only closure; no mathematical/native program or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
P = R.parents[3]
CONTROLS = {"FINAL.json", "OWNED_MANIFEST.json"}
def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest(),
            "mode": format(stat.S_IMODE(path.stat().st_mode), "04o")}
def match(path, item):
    actual = pin(path)
    assert actual["bytes"] == item["bytes"] and actual["SHA256"] == item["SHA256"], str(path)
    if "mode" in item:
        assert actual["mode"] == item["mode"], str(path)

assert pin(R / "INITIAL_SEAL.json")["SHA256"] == "34244244d91ee450b476c16d570aecfce3dba6bb2466dc5b2e4fed66a7c9ee34"
initial = json.loads((R / "INITIAL_SEAL.json").read_text())
for item in initial["files"]:
    match(R / item["path"], item)
readings = json.loads((R / "PRIMARY_READINGS.json").read_text())
for item in readings["bodies"] + readings["raw_page_images_personally_read_by_reference"] + [readings["native_support_program"]]:
    path = Path(item["path"])
    match(path if path.is_absolute() else P / path, item)
source = json.loads((R / "SOURCE_PINS.json").read_text())
for item in source["source_controls_by_reference"]:
    match(P / item["path"], item)
for item in source["native_assets_in_literal_order"]:
    match(P / "papers/23357329/sources/assets" / item["name"], item)
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
assert len(payload) == 20 and dirs == ["native-run", "rasters"]
now = datetime.now(timezone.utc).isoformat()
manifest = {"schema": "finite-owned-scientific-scope-manifest-v1", "record_id": 23357329,
            "UTC": now, "actual_regular_files": 22, "payload_files": 20,
            "child_directories": dirs, "symlinks": [], "other_special_files": [],
            "exact_terminal_controls": sorted(CONTROLS),
            "no_wildcard_subtree_runtime_or_future_exclusions": True, "files": payload}
(R / "OWNED_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
final = {"schema": "finite-independent-original-scientific-scope-final-v1", "record_id": 23357329,
         "row": 163, "UTC": now, "status": "COMPLETE_SEALED_QUIESCENT", "completion_percent": 100,
         "owned_root": "papers/23357329/reviews/scope-sol", "actual_regular_files": 22,
         "child_directories": dirs, "payload_files": 20,
         "manifest": {"path": "OWNED_MANIFEST.json", **pin(R / "OWNED_MANIFEST.json")},
         "report": {"path": "REPORT.md", **pin(R / "REPORT.md")},
         "primary_readings": {"path": "PRIMARY_READINGS.json", **pin(R / "PRIMARY_READINGS.json")},
         "initial_seal": {"path": "INITIAL_SEAL.json", **pin(R / "INITIAL_SEAL.json")},
         "all_12_source_first_files_unchanged": True,
         "source_final": source["source_controls_by_reference"][0],
         "full_original_claim_disposition_and_evidence": "REPORT.md; withheld until root own INITIAL",
         "central_unresolved_mathematical_gap": None,
         "actual_primary_body_references": 5, "new_network_acquisitions": 0,
         "shared_raw_primary_page_images_by_reference": 2,
         "native_ordinary_attempts": 1, "native_exit": receipt["exit_code"],
         "native_mathematical_scope": "Finite local exact controls only; not global existence or hyperbolic certification",
         "optimized_selftest_retries_other_native_runs": 0,
         "current_peer_root_findings_or_archived_opinion_result_bodies_opened": False,
         "findings_withheld_until_root_source_first_gate": True,
         "publication_authority": False, "AA": None, "canonical_url": None, "followup": None,
         "source_W_Git_Sheet_old_packet_or_contact_modifications": False,
         "quiescent_after_this_seal": True}
(R / "FINAL.json").write_text(json.dumps(final, indent=2) + "\n")
for item in payload:
    match(R / item["path"], item)
assert len([p for p in R.rglob("*") if p.is_file()]) == 22
print(json.dumps({"actual_regular_files": 22, "child_directories": dirs,
                  "pins": {name: pin(R / name) for name in ["FINAL.json", "OWNED_MANIFEST.json", "REPORT.md", "PRIMARY_READINGS.json", "NATIVE_RUN_RECEIPT.json"]}}, indent=2))
