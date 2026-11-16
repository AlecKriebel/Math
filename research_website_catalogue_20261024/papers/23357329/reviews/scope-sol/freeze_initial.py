"""One-use standard-library source/reading custody; no mathematics or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
S = R.parents[1] / "sources"
def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest(),
            "mode": format(stat.S_IMODE(path.stat().st_mode), "04o")}

assert pin(S / "SOURCE_FINAL.json")["SHA256"] == "ffb1b2affbb085a9d0c55d2ce5c7567b8d921fa15c7b1c58cc47caa3c1bfae7f"
record = json.loads((S / "record.response.body").read_text())
files = json.loads((S / "files-23357329.response.body").read_text())
assets = [{"name": x["key"], "native_MD5": x["checksum"], **pin(S / "assets" / x["key"])} for x in record["files"]]
rasters = [{"path": f"rasters/page-{i}.png", "personally_read": True, **pin(R / f"rasters/page-{i}.png")} for i in range(1, 5)]
pins = {"schema": "source-first-native-identity-and-reading-pins-v1", "record_id": 23357329,
        "native_version": record["metadata"]["version"], "printed_numeric_version": "ABSENT",
        "printed_date": "13 October 2026", "publication_date": record["metadata"]["publication_date"],
        "created": record["created"], "modified": record["modified"], "updated": record["updated"],
        "status": record["status"], "state": record["state"], "submitted": record["submitted"],
        "is_published": record.get("is_published", "ABSENT"),
        "resource_type": record["metadata"]["resource_type"], "license": record["metadata"]["license"],
        "creators": record["metadata"]["creators"], "native_assets_in_literal_order": assets,
        "files_order": [x["key"] for x in files["entries"]], "custom_order": files["order"],
        "default_preview": files["default_preview"], "native_PDF_pages_read": 4,
        "native_TeX_lines_read": 238, "fresh_rasters": rasters,
        "render": {"utility": "Trusted installed Poppler pdftoppm", "dpi": 130, "exit": 0,
                   "stdout": {"path": "render.stdout.txt", **pin(R / "render.stdout.txt")},
                   "stderr": {"path": "render.stderr.txt", **pin(R / "render.stderr.txt")}},
        "source_packet_extent": {"files": 231, "child_directories": 20},
        "source_controls_by_reference": [{"path": "papers/23357329/sources/" + n, **pin(S / n)}
                                         for n in ["SOURCE_FINAL.json", "SOURCE_MANIFEST.json", "record.response.body", "files-23357329.response.body"]],
        "authored_manuscript_Description_assertions_exposed": True,
        "current_peer_root_archived_scientific_opinions_results_program_bodies_opened": False,
        "new_foreign_mathematical_bodies_opened": False, "scientific_native_program_executions": 0,
        "publication_authority": False, "AA": None, "canonical_url": None, "followup": None}
(R / "SOURCE_PINS.json").write_text(json.dumps(pins, indent=2) + "\n")
payload = []
for path in sorted(R.rglob("*")):
    assert not path.is_symlink()
    if path.is_file() and path.name != "INITIAL_SEAL.json":
        payload.append({"path": path.relative_to(R).as_posix(), **pin(path)})
assert len(payload) == 11
seal = {"schema": "actual-source-first-independent-result-initial-seal-v1", "record_id": 23357329,
        "row": 163, "UTC": datetime.now(timezone.utc).isoformat(),
        "status": "SOURCE_FIRST_MANUSCRIPT_AND_ACTUAL_INDEPENDENT_RESULTS_FROZEN",
        "actual_regular_files": 12, "payload_files": 11, "child_directories": ["rasters"],
        "exact_terminal_exclusion": "INITIAL_SEAL.json", "files": payload,
        "all_actual_manuscript_pages_and_TeX_read": True, "fresh_pixels_read": 4,
        "source_first_completion_percent": 100, "full_review_completion_percent": 60,
        "current_peer_root_archived_opinions_results_program_bodies_unopened": True,
        "new_foreign_math_bodies_unopened": True, "scientific_native_executions": 0,
        "findings_withheld_until_root_own_INITIAL": True,
        "publication_authority": False, "AA": None, "canonical_url": None, "followup": None}
(R / "INITIAL_SEAL.json").write_text(json.dumps(seal, indent=2) + "\n")
print(json.dumps({"INITIAL_SEAL.json": pin(R / "INITIAL_SEAL.json"),
                  "INITIAL.md": pin(R / "INITIAL.md"), "INDEPENDENT_RESULTS.md": pin(R / "INDEPENDENT_RESULTS.md"),
                  "actual_regular_files": 12, "child_directories": 1}, indent=2))
