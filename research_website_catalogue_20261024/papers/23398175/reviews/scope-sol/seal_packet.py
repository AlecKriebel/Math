"""One-use, standard-library-only data custody closure; no science or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

ROOT = Path(__file__).resolve().parent
P = ROOT.parents[3]
CONTROLS = {"FINAL.json", "OWNED_MANIFEST.json"}

def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest(),
            "mode": format(stat.S_IMODE(path.stat().st_mode), "04o")}

def unchanged(entries):
    for item in entries:
        actual = pin(ROOT / item["path"])
        assert actual["bytes"] == item["bytes"], item["path"]
        assert actual["SHA256"] == item["SHA256"], item["path"]
        if "mode" in item:
            assert actual["mode"] == item["mode"], item["path"]

checkpoint = json.loads((ROOT / "CHECKPOINT_POST_INITIAL.json").read_text())
unchanged(checkpoint["files"])
assert pin(ROOT / "CHECKPOINT_POST_INITIAL.json")["SHA256"] == "12228ec6b4239ae5df4884492ea1d531d539e821bc4b77e501c02f9f6a39b08b"
readings = json.loads((ROOT / "PRIMARY_READINGS.json").read_text())
for group in ("raw_primary_references", "native_support_bodies", "native_code_complete_static_read"):
    for item in readings[group]:
        ref = Path(item["path"])
        actual = pin(ref if ref.is_absolute() else P / ref)
        assert (actual["bytes"], actual["SHA256"]) == (item["bytes"], item["SHA256"]), item["path"]

files, dirs = [], []
for path in sorted(ROOT.rglob("*")):
    assert not path.is_symlink(), str(path)
    rel = path.relative_to(ROOT).as_posix()
    if path.is_dir():
        dirs.append(rel)
    else:
        assert stat.S_ISREG(path.stat().st_mode), str(path)
        if rel not in CONTROLS:
            files.append({"path": rel, **pin(path)})
assert len(files) == 30 and dirs == ["native-run", "private-primary", "rasters"]
now = datetime.now(timezone.utc).isoformat()
manifest = {"schema": "finite-owned-review-manifest-v1", "record_id": 23398175,
            "UTC": now, "actual_regular_files": 32, "payload_files": 30,
            "child_directories": dirs, "symlinks": [], "other_special_files": [],
            "exact_terminal_controls": sorted(CONTROLS),
            "no_subtree_wildcard_future_or_runtime_exclusions": True, "files": files}
(ROOT / "OWNED_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
final = {"schema": "finite-independent-scientific-scope-final-v1", "record_id": 23398175,
         "row": 162, "UTC": now, "status": "COMPLETE_SEALED_QUIESCENT",
         "completion_percent": 100, "owned_root": "papers/23398175/reviews/scope-sol",
         "actual_regular_files": 32, "child_directory_count": 3,
         "manifest": {"path": "OWNED_MANIFEST.json", **pin(ROOT / "OWNED_MANIFEST.json")},
         "report": {"path": "REPORT.md", **pin(ROOT / "REPORT.md")},
         "primary_readings": {"path": "PRIMARY_READINGS.json", **pin(ROOT / "PRIMARY_READINGS.json")},
         "initial_seal": {"path": "INITIAL_SEAL.json", **pin(ROOT / "INITIAL_SEAL.json")},
         "checkpoint": {"path": "CHECKPOINT_POST_INITIAL.json", **pin(ROOT / "CHECKPOINT_POST_INITIAL.json")},
         "checkpoint_26_files_unchanged": True, "initial_14_files_unchanged": True,
         "source_packet": json.loads((ROOT / "SOURCE_PINS.json").read_text())["source_final"],
         "original_claim_disposition_and_evidence": "REPORT.md; conclusions withheld from root until its own INITIAL",
         "central_unresolved_mathematical_gap": None,
         "native_attempts": 1, "native_exit": 1, "native_mathematical_output_completed": False,
         "native_error": "ModuleNotFoundError: No module named 'sympy'",
         "fresh_IAS_HTTP_status": 403, "fresh_IAS_curl_exit": 22,
         "fresh_IAS_PDF_acquired": False, "replays_retries_or_bypasses": 0,
         "current_peer_root_findings_opened": False, "findings_withheld": True,
         "publication_authority": False, "AA": None, "canonical_url": None, "followup": None,
         "all_owned_writes_stopped_after_seal": True}
(ROOT / "FINAL.json").write_text(json.dumps(final, indent=2) + "\n")
unchanged(files)
assert len([x for x in ROOT.rglob("*") if x.is_file()]) == 32
print(json.dumps({"regular_files": 32, "child_dirs": dirs,
                  "terminal": {name: pin(ROOT / name) for name in sorted(CONTROLS)},
                  "report": pin(ROOT / "REPORT.md"),
                  "primary_readings": pin(ROOT / "PRIMARY_READINGS.json")}, indent=2))
