"""Read-only source custody check; does not import or execute native programs."""
from pathlib import Path
import hashlib
import json
import stat
import zipfile
from datetime import datetime, timezone

LANE = Path(__file__).resolve().parent
PROJECT = LANE.parents[3]
SOURCE = PROJECT / "papers/23203270/sources"
PINS = {
    SOURCE / "SOURCE_FINAL.json": "2fec24204f44586d98bd88fbe26a1519e7b55b4abe221275475b1cbf2a7bc62e",
    SOURCE / "SOURCE_MANIFEST.json": "4d41d1b02c1f436a7a0fd8f6249515aa69eced4658527a1c56f3fec20c86a704",
    PROJECT / "verification/root-source188189-adoption-20261117.json": "a566cd4302715f0feba248b732ce5a9a4d5329acb2c82e15f0bdcd0573ad75a6",
    SOURCE / "zenodo-files/paper.pdf": "c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6",
}

def digest(data, algorithm="sha256"):
    return hashlib.new(algorithm, data).hexdigest()

def entry(path, base):
    info = path.lstat()
    result = {"path": str(path.relative_to(base)) if path != base else ".",
              "mode_octal": oct(stat.S_IMODE(info.st_mode))}
    if stat.S_ISDIR(info.st_mode):
        result.update(kind="directory", empty=not any(path.iterdir()))
    elif stat.S_ISREG(info.st_mode):
        data = path.read_bytes()
        result.update(kind="file", bytes=len(data), sha256=digest(data), md5=digest(data, "md5"))
    else:
        raise ValueError(f"Unexpected filesystem object: {path}")
    return result

checked_pins = []
for path, expected in PINS.items():
    actual = entry(path, path.parent)
    assert actual["sha256"] == expected, (path, actual["sha256"], expected)
    checked_pins.append({"absolute_path": str(path), **actual, "expected_sha256": expected})

source_manifest = json.loads((SOURCE / "SOURCE_MANIFEST.json").read_text())
excluded = source_manifest["excluded_control_files"]
assert excluded == ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"]
actual_entries = [entry(path, SOURCE) for path in [SOURCE, *sorted(SOURCE.rglob("*"))]]
payload = [e for e in actual_entries if e["path"] not in excluded]
assert payload == source_manifest["entries"], "Byte/topology/mode discrepancy in original source payload"
assert sum(e["kind"] == "file" for e in payload) == source_manifest["file_count"] == 95
assert sum(e["kind"] == "directory" for e in payload) == source_manifest["directory_count"] == 13
assert sum(e.get("bytes", 0) for e in payload) == source_manifest["total_file_bytes"]
assert sum(e["kind"] == "file" for e in actual_entries) == 97

api = json.loads((SOURCE / "native-metadata/record-api.json").read_text())
assert api["id"] == 23203270 and api["doi"] == "10.5281/zenodo.23203270"
assert "version" not in api["metadata"]
assert api["metadata"]["publication_date"] == "2026-10-06"
asset_results = []
for native in api["files"]:
    path = SOURCE / "zenodo-files" / native["key"]
    data = path.read_bytes()
    assert len(data) == native["size"]
    assert "md5:" + digest(data, "md5") == native["checksum"]
    asset_results.append({"key": native["key"], "bytes": len(data), "sha256": digest(data), "native_checksum": native["checksum"]})

archive = SOURCE / "zenodo-files/source-and-verification.zip"
extracted = SOURCE / "archives/01-source-and-verification.zip.extracted"
members = []
with zipfile.ZipFile(archive) as zf:
    assert len(zf.infolist()) == 87
    for info in zf.infolist():
        assert not info.is_dir(), "Unexpected directory ZIP member; handle explicitly"
        relative = Path(info.filename)
        assert not relative.is_absolute() and ".." not in relative.parts
        data = zf.read(info)
        assert data == (extracted / relative).read_bytes()
        members.append({"path": info.filename, "bytes": len(data), "sha256": digest(data)})
assert not [e for e in actual_entries if e["path"].lower().endswith(".pdf") and e["path"] != "zenodo-files/paper.pdf"]

result = {
    "schema": "independent-source-authentication-v1",
    "utc": datetime.now(timezone.utc).isoformat(),
    "source_root": str(SOURCE),
    "purpose": "Independent original-source byte/topology authentication only; no scientific verdict",
    "all_pins_match": True,
    "checked_pins": checked_pins,
    "whole_actual_file_count": 97,
    "whole_actual_child_directory_count": 12,
    "source_manifest_payload_file_count": 95,
    "source_manifest_control_exclusions": excluded,
    "all_actual_entries": actual_entries,
    "native_assets_checked": asset_results,
    "zip_member_count": len(members),
    "zip_members_match_extracted_bytes": True,
    "zip_member_checks": members,
    "embedded_pdf_count": 0,
    "native_version_field_present": False,
    "native_scientific_code_execution_count": 0,
}
(LANE / "SOURCE_AUTHENTICATION.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"all_pins_match": True, "source_files": 97, "child_directories": 12, "archive_members": 87, "embedded_pdfs": 0, "scientific_executions": 0}))
