"""Read-only custody validation; writes only this verification lane's receipts.

No acquired scientific source is imported, executed, or semantically read.
Byte hashing and ZIP decompression are data validation, and pdfinfo is a
read-only local PDF metadata parser. There is no network or repair route.
"""
from pathlib import Path
import datetime
import hashlib
import json
import re
import shutil
import stat
import subprocess
import zipfile

LANE = Path(__file__).resolve().parent


def digest(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "md5": hashlib.md5(data).hexdigest()}


def actual_namespace(root):
    rows = []
    for path in [root, *sorted(root.rglob("*"))]:
        relative = "." if path == root else path.relative_to(root).as_posix()
        if relative in ("SOURCE_MANIFEST.json", "SOURCE_FINAL.json"):
            continue
        info = path.lstat()
        kind = "directory" if stat.S_ISDIR(info.st_mode) else "file" if stat.S_ISREG(info.st_mode) else "other"
        assert kind != "other", f"Nonregular node: {path}"
        row = {"path": relative, "kind": kind, "mode_octal": oct(stat.S_IMODE(info.st_mode)),
               "hidden_component": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
        if kind == "file":
            row.update(digest(path))
        else:
            row["empty"] = not any(path.iterdir())
        rows.append(row)
    return rows


def main():
    assert not (LANE / "CUSTODY_RESULT.json").exists(), "Refusing validation overwrite"
    external = json.loads((LANE / "EXTERNAL_SOURCE_PINS.json").read_text())
    reports = []
    for pin in external["records"]:
        root = Path(pin["source_root"])
        for name in ("manifest", "final"):
            assert digest(Path(pin[name]["path"])) == {k: pin[name][k] for k in ("bytes", "sha256", "md5")}
        manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
        final = json.loads((root / "SOURCE_FINAL.json").read_text())
        meta = json.loads((root / "SOURCE_METADATA.json").read_text())
        native = json.loads((root / "native-metadata/record-api.json").read_text())
        assert manifest["excluded_control_files"] == ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"]
        assert actual_namespace(root) == manifest["entries"]
        expected = {e["path"] for e in manifest["entries"] if e["path"] != "."} | set(manifest["excluded_control_files"])
        assert {p.relative_to(root).as_posix() for p in root.rglob("*")} == expected
        assert native["status"] == "published" and int(native["id"]) == pin["record_id"]
        assert native["doi"] == f"10.5281/zenodo.{pin['record_id']}"
        assert meta["native_file_order"] == [f["key"] for f in native["files"]]
        for entry in native["files"]:
            observed = digest(root / "zenodo-files" / entry["key"])
            algorithm, checksum = entry["checksum"].split(":", 1)
            assert observed["bytes"] == entry["size"]
            assert observed[algorithm] == checksum.lower().zfill(32 if algorithm == "md5" else 64)
        member_count = 0
        for archive in meta["archives"]:
            inventory = json.loads(Path(archive["inventory"]).read_text())
            assert archive["kind"] == inventory["kind"] == "zip"
            with zipfile.ZipFile(archive["archive"]) as opened:
                infos = opened.infolist()
                assert len(infos) == inventory["member_count"]
                for info, member in zip(infos, inventory["members"]):
                    assert info.orig_filename == member["native_name"]
                    target = Path(archive["extracted"]) / member["path"]
                    if info.is_dir():
                        assert target.is_dir()
                    else:
                        data = opened.read(info)
                        assert target.read_bytes() == data
                        assert hashlib.sha256(data).hexdigest() == member["sha256"]
                        assert len(data) == info.file_size == member["bytes"]
                    assert oct(stat.S_IMODE(target.lstat().st_mode)) == member["extracted_mode"]
                member_count += len(infos)
        pdf = root / meta["outer_controlling_manuscript"]["relative_path"]
        assert pdf.read_bytes().startswith(b"%PDF-")
        pdfinfo = shutil.which("pdfinfo")
        pdf_receipt = {"performed": False}
        if pdfinfo:
            command = [pdfinfo, str(pdf)]
            result = subprocess.run(command, capture_output=True, timeout=30, check=False)
            stdout_name = f"PDF_INFO_{pin['record_id']}.stdout.txt"
            stderr_name = f"PDF_INFO_{pin['record_id']}.stderr.txt"
            (LANE / stdout_name).write_bytes(result.stdout)
            (LANE / stderr_name).write_bytes(result.stderr)
            assert result.returncode == 0, result.stderr.decode(errors="replace")
            pages = re.search(rb"(?m)^Pages:\s+(\d+)", result.stdout)
            pdf_receipt = {"performed": True, "command": command, "exit_status": result.returncode,
                           "pages": int(pages.group(1)) if pages else None,
                           "stdout": {"path": stdout_name, **digest(LANE / stdout_name)},
                           "stderr": {"path": stderr_name, **digest(LANE / stderr_name)}}
        reports.append({"record_id": pin["record_id"], "row": pin["row"],
                        "all_actual_source_bytes_modes_hidden_empty_topology_match": True,
                        "native_identity_and_checksum_checks": "pass",
                        "actual_files": len([p for p in root.rglob("*") if p.is_file()]),
                        "actual_child_directories": len([p for p in root.rglob("*") if p.is_dir()]),
                        "archive_members_byte_identical": member_count,
                        "embedded_pdf_locations": meta["embedded_pdf_locations"],
                        "native_file_order": meta["native_file_order"],
                        "native_version_field_present": meta["native_version_field_present"],
                        "native_version": meta["native_version"],
                        "native_doi": meta["native_doi"],
                        "native_publication_date": meta["native_publication_date"],
                        "native_created": meta["native_created"], "native_updated": meta["native_updated"],
                        "native_license": meta["native_license"], "pdf_metadata": pdf_receipt,
                        "source_custody_completion_percent": 100, "scientific_review_completion_percent": 0})
        assert reports[-1]["actual_files"] == final["actual_file_count_including_terminal_controls"]
        assert reports[-1]["actual_child_directories"] == final["actual_child_directory_count"]
    report = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "pass",
              "records": reports, "native_scientific_execution": False,
              "proof_support_reports_semantically_read": False, "network_requests": 0,
              "source_custody_completion_percent": 100, "scientific_review_completion_percent": 0}
    (LANE / "CUSTODY_RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
