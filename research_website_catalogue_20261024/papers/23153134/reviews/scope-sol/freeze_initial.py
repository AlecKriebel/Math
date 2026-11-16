"""One-use data-only source/reading custody. No science, imports of native code or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
S = R.parents[1] / "sources"
def pin(p):
    raw = p.read_bytes()
    return {"bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest(),
            "mode": format(stat.S_IMODE(p.stat().st_mode), "04o")}
assert pin(S / "SOURCE_FINAL.json")["SHA256"] == "d27eab22eee564acebb30c9093ed95f7c7ee0f854a8fb50af15d5eeb6e21afa0"
record = json.loads((S / "record.response.body").read_text())
files = json.loads((S / "files-23153134.response.body").read_text())
assets = [{"name": x["key"], "native_MD5": x["checksum"], "created": x["created"],
           "updated": x["updated"], **pin(S / "assets" / x["key"])} for x in files["entries"]]
data = {"schema": "source-first-native-identity-reading-pins-v1", "record_id": 23153134,
        "native_version": record["metadata"]["version"], "printed_version": "1.0",
        "printed_date": "5 October 2026", "publication_date": record["metadata"]["publication_date"],
        "created": record["created"], "modified": record["modified"], "updated": record["updated"],
        "status": record["status"], "state": record["state"], "submitted": record["submitted"],
        "is_published": record.get("is_published", "ABSENT"), "resource_type": record["metadata"]["resource_type"],
        "creators": record["metadata"]["creators"], "native_record_license": record["metadata"]["license"],
        "actual_license_scope": "CC BY4.0 all original manuscript/code/results/authored documentation; third-party rights separate; no MIT split",
        "actual_license": {"path": "papers/23153134/sources/assets/LICENSE.txt", **pin(S / "assets/LICENSE.txt")},
        "assets_in_literal_order": assets, "record_order": [x["key"] for x in record["files"]],
        "files_custom_order": files["order"], "default_preview": files["default_preview"],
        "all_TeX_lines_read": 282, "all_native_PDF_pages_read": 5,
        "complete_extracted_PDF_text_read": {"path": "manuscript.txt", **pin(R / "manuscript.txt")},
        "fresh_rasters": [{"path": f"rasters/page-{i}.png", "personally_read": True, **pin(R / f"rasters/page-{i}.png")} for i in range(1, 6)],
        "render": {"utility": "Trusted installed Poppler pdftoppm", "dpi": 130, "exit": 0,
                   "stdout": {"path": "render.stdout.txt", **pin(R / "render.stdout.txt")},
                   "stderr": {"path": "render.stderr.txt", **pin(R / "render.stderr.txt")}},
        "source_extent": {"regular_files": 94, "child_directories": 4},
        "source_controls_by_reference": [{"path": "papers/23153134/sources/" + n, **pin(S / n)} for n in ["SOURCE_FINAL.json", "SOURCE_MANIFEST.json", "record.response.body", "files-23153134.response.body"]],
        "opaque_asset_hashing_not_semantic_reading": True,
        "closed_scientific_bodies": ["SOURCE_AUDIT.md", "verification_results.json", "README.md", "verify_cover.py", "all archived/current opinions", "new foreign mathematical bodies"],
        "manuscript_and_native_Description_assertions_disclosed": True, "scientific_native_program_executions": 0,
        "publication_authority": False, "AA": None, "canonical_url": None, "followup": None}
(R / "SOURCE_PINS.json").write_text(json.dumps(data, indent=2) + "\n")
payload = []
for p in sorted(R.rglob("*")):
    assert not p.is_symlink()
    if p.is_file() and p.name != "INITIAL_SEAL.json":
        payload.append({"path": p.relative_to(R).as_posix(), **pin(p)})
assert len(payload) == 13
seal = {"schema": "actual-source-first-independent-results-seal-v1", "record_id": 23153134, "row": 166,
        "UTC": datetime.now(timezone.utc).isoformat(), "status": "ACTUAL_SOURCE_FIRST_INITIAL_AND_DERIVATIONS_FROZEN",
        "actual_regular_files": 14, "payload_files": 13, "child_directories": ["rasters"],
        "exact_terminal_exclusion": "INITIAL_SEAL.json", "files": payload,
        "actual_whole_manuscript_TeX_text_and_fresh_pixels_read": True,
        "source_first_completion_percent": 100, "estimated_full_review_percent": 60,
        "support_results_programs_archived_current_opinions_and_new_foreign_bodies_unopened": True,
        "scientific_native_executions": 0, "findings_withheld_until_root_own_INITIAL": True,
        "publication_authority": False, "AA": None, "canonical_url": None, "followup": None}
(R / "INITIAL_SEAL.json").write_text(json.dumps(seal, indent=2) + "\n")
print(json.dumps({n: pin(R / n) for n in ["INITIAL_SEAL.json", "INITIAL.md", "INDEPENDENT_RESULTS.md", "SOURCE_PINS.json"]}, indent=2))
