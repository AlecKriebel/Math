"""One-attempt public Zenodo source custody for records 23202994 and 23204176.

This program transfers and hashes bytes and safely expands archive data only.
It never imports, evaluates, builds, or executes acquired source files. It does
not inspect scientific claims. Each failed record stops immediately; the other
record may proceed. No network request is retried. Redirects are transport.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import time
import traceback
import urllib.error
import urllib.request
import zipfile

LANE = Path(__file__).resolve().parent
PROJECT = LANE.parents[1]
RECORDS = [
    (23202994, 190, "Hypersingular Riesz-energy constants on surfaces from triangular-lattice universal optimality"),
    (23204176, 191, "Rational Hodge classes on mixed products of K3 moduli spaces"),
]
MAX_MEMBERS = 10000
MAX_EXPANDED_BYTES = 1024 ** 3
MAX_ARCHIVE_DEPTH = 5


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write_json(path, data):
    assert not path.exists(), f"Refusing overwrite: {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    path.chmod(0o644)


def hashes(path):
    a, b, size = hashlib.sha256(), hashlib.md5(), 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            a.update(block)
            b.update(block)
            size += len(block)
    return {"bytes": size, "sha256": a.hexdigest(), "md5": b.hexdigest()}


def leaf(name):
    assert isinstance(name, str) and name not in ("", ".", "..")
    assert "/" not in name and "\\" not in name and "\x00" not in name
    assert not re.match(r"^[A-Za-z]:", name), f"Unsafe filename: {name!r}"
    return name


def archive_path(name):
    assert isinstance(name, str) and name and "\x00" not in name
    assert "\\" not in name and not name.startswith("/")
    parts = PurePosixPath(name).parts
    assert parts and all(p not in ("", ".", "..") for p in parts)
    assert not re.match(r"^[A-Za-z]:", parts[0])
    return Path(*parts)


def get_once(url, destination, receipts):
    assert url.startswith("https://"), "Only ordinary public HTTPS GET is allowed"
    assert not destination.exists(), f"Refusing network overwrite: {destination}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    receipt = {"url": url, "destination": str(destination), "started_utc": utc(),
               "method": "GET", "attempt": 1, "retry": False}
    receipts.append(receipt)
    started = time.monotonic()
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "SourceCustody/1.0"})
        with urllib.request.urlopen(request, timeout=90) as response:
            receipt.update(status=response.status, final_url=response.url,
                           response_headers={k: v for k, v in response.headers.items()
                                             if k.lower() in {"content-type", "content-length", "etag",
                                                              "last-modified", "date", "digest"}})
            with destination.open("xb") as output:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    output.write(block)
                output.flush()
            destination.chmod(0o644)
            receipt.update(hashes(destination))
            expected = response.headers.get("Content-Length")
            if expected is not None:
                assert receipt["bytes"] == int(expected), "HTTP Content-Length mismatch"
        receipt["success"] = True
    except Exception as error:
        receipt.update(success=False, error_type=type(error).__name__, literal_error=str(error))
        if isinstance(error, urllib.error.HTTPError):
            receipt["http_status"] = error.code
            error_body = error.read()
            error_file = destination.with_name(destination.name + ".http-error-body.bin")
            error_file.write_bytes(error_body)
            error_file.chmod(0o644)
            receipt["error_body"] = {"path": str(error_file), **hashes(error_file)}
        if destination.exists():
            receipt["partial_file"] = hashes(destination)
        raise
    finally:
        receipt.update(completed_utc=utc(), elapsed_seconds=time.monotonic() - started)


def safe_archive(source, destination, inventory_path, budget):
    """Preflight every member before expanding; reject all links/special nodes."""
    assert not destination.exists() and not inventory_path.exists()
    archive_kind = "zip" if zipfile.is_zipfile(source) else "tar" if tarfile.is_tarfile(source) else None
    if archive_kind is None:
        return None
    archive = zipfile.ZipFile(source) if archive_kind == "zip" else tarfile.open(source, "r:*")
    with archive:
        members = archive.infolist() if archive_kind == "zip" else archive.getmembers()
        planned, occupied = [], {}
        expanded = 0
        for ordinal, item in enumerate(members, 1):
            name = item.orig_filename if archive_kind == "zip" else item.name
            relative = archive_path(name)
            if archive_kind == "zip":
                mode_full = item.external_attr >> 16
                file_type = stat.S_IFMT(mode_full)
                is_directory = item.is_dir()
                assert not item.flag_bits & 1, f"Encrypted ZIP member: {name!r}"
                assert file_type in (0, stat.S_IFREG, stat.S_IFDIR), f"Link/special ZIP member: {name!r}"
                assert not (file_type == stat.S_IFDIR and not is_directory), "Ambiguous ZIP directory"
                size = item.file_size
                mode = stat.S_IMODE(mode_full) & 0o777
                mode = mode or (0o755 if is_directory else 0o644)
                details = {"compressed_bytes": item.compress_size, "crc32": f"{item.CRC:08x}",
                           "date_time": list(item.date_time), "external_attr": item.external_attr,
                           "create_system": item.create_system, "flag_bits": item.flag_bits,
                           "header_offset": item.header_offset}
            else:
                assert item.isdir() or item.isreg(), f"Link/special TAR member: {name!r}"
                is_directory = item.isdir()
                size = item.size
                mode = item.mode & 0o777
                details = {"archive_mode": oct(item.mode), "mtime": item.mtime,
                           "uid": item.uid, "gid": item.gid, "uname": item.uname,
                           "gname": item.gname, "type_hex": item.type.hex()}
            normalized = relative.as_posix()
            assert normalized not in occupied, f"Duplicate archive path: {name!r}"
            occupied[normalized] = "directory" if is_directory else "file"
            expanded += size
            planned.append((item, relative, is_directory, mode,
                            {"ordinal": ordinal, "native_name": name, "path": normalized,
                             "kind": occupied[normalized], "bytes": size,
                             "extracted_mode": oct(mode), **details}))
        assert budget["members"] + len(planned) <= MAX_MEMBERS, "Archive member bound exceeded"
        assert budget["bytes"] + expanded <= MAX_EXPANDED_BYTES, "Expanded byte bound exceeded"
        for _, relative, _, _, _ in planned:
            for parent in relative.parents:
                if parent != Path("."):
                    assert occupied.get(parent.as_posix()) != "file", "File/directory path collision"
        budget["members"] += len(planned)
        budget["bytes"] += expanded
        destination.mkdir(parents=True)
        directory_modes = []
        rows = []
        for item, relative, is_directory, mode, row in planned:
            target = destination / relative
            if is_directory:
                target.mkdir(parents=True, exist_ok=True)
                directory_modes.append((target, mode))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.open(item, "r") if archive_kind == "zip" else archive.extractfile(item)
                assert stream is not None
                with stream, target.open("xb") as output:
                    while True:
                        block = stream.read(1024 * 1024)
                        if not block:
                            break
                        output.write(block)
                row.update(hashes(target))
                assert row["bytes"] == (item.file_size if archive_kind == "zip" else item.size)
                target.chmod(mode)
            rows.append(row)
        for directory, mode in sorted(directory_modes, key=lambda p: len(p[0].parts), reverse=True):
            directory.chmod(mode)
    write_json(inventory_path, {"archive": str(source), "kind": archive_kind,
                               "member_count": len(rows), "expanded_member_bytes": expanded,
                               "safe_paths_no_links_no_special_nodes": True, "members": rows})
    return {"archive": str(source), "extracted": str(destination),
            "inventory": str(inventory_path), "kind": archive_kind,
            "member_count": len(rows), "expanded_member_bytes": expanded}


def namespace(base, exclude=()):
    entries = []
    for path in [base, *sorted(base.rglob("*"))]:
        relative = "." if path == base else path.relative_to(base).as_posix()
        if relative in exclude:
            continue
        metadata = path.lstat()
        kind = "directory" if stat.S_ISDIR(metadata.st_mode) else "file" if stat.S_ISREG(metadata.st_mode) else "other"
        assert kind in ("directory", "file"), f"Unexpected namespace node: {path}"
        entry = {"path": relative, "kind": kind, "mode_octal": oct(stat.S_IMODE(metadata.st_mode)),
                 "hidden_component": any(p.startswith(".") and p not in (".", "..") for p in Path(relative).parts)}
        if kind == "file":
            entry.update(hashes(path))
        else:
            entry["empty"] = not any(path.iterdir())
        entries.append(entry)
    return entries


def close_source(source, record_id, metadata, receipts, started, failure, archives):
    write_json(source / "native-metadata/transport-receipts.json", receipts)
    write_json(source / "SOURCE_METADATA.json", metadata)
    write_json(source / "SOURCE_LOG.json", {"started_utc": started, "completed_utc": utc(),
               "operations": ["single-attempt public HTTPS GET", "native metadata byte preservation",
                              "native length/checksum comparison", "safe archive extraction",
                              "whole recursive namespace byte/topology/mode manifest"],
               "source_custody_completion_percent": 100 if failure is None else 0,
               "scientific_content_read": False, "scientific_programs_executed": False})
    entries = namespace(source)
    manifest = {"schema": "source-custody-manifest-v1", "record_id": record_id,
                "created_utc": utc(), "root": str(source),
                "scope": "entire actual recursive namespace; no hidden/ignore filters; excludes only two named terminal controls",
                "excluded_control_files": ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"],
                "terminal_control_topology": [{"path": n, "kind": "file", "mode_octal": "0o644"}
                                              for n in ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"]],
                "entries": entries, "file_count": sum(e["kind"] == "file" for e in entries),
                "directory_count": sum(e["kind"] == "directory" for e in entries),
                "total_file_bytes": sum(e.get("bytes", 0) for e in entries)}
    write_json(source / "SOURCE_MANIFEST.json", manifest)
    final = {"schema": "source-custody-final-v1", "record_id": record_id,
             "closed_utc": utc(), "status": "source_acquisition_complete_no_scientific_review" if failure is None else "source_acquisition_stopped_after_failure_no_retry",
             "source_root": str(source), "manifest": {"path": "SOURCE_MANIFEST.json", **hashes(source / "SOURCE_MANIFEST.json")},
             "payload_file_count": manifest["file_count"],
             "payload_directory_count_including_root": manifest["directory_count"],
             "actual_file_count_including_terminal_controls": manifest["file_count"] + 2,
             "actual_child_directory_count": manifest["directory_count"] - 1,
             "published_asset_count": len(metadata.get("files_in_published_order", [])),
             "native_listed_asset_count": metadata.get("native_listed_asset_count"),
             "archive_count": len(archives), "archive_member_count": sum(a["member_count"] for a in archives),
             "embedded_pdf_count": len(metadata.get("embedded_pdf_locations", [])),
             "manifest_scope_is_finite": True, "no_source_mutation_after_closure": True,
             "external_pin_location": str(LANE / "EXTERNAL_SOURCE_PINS.json"),
             "source_custody_completion_percent": 100 if failure is None else 0,
             "scientific_review_completion_percent": 0, "failure": failure,
             "outer_controlling_manuscript": metadata.get("outer_controlling_manuscript")}
    write_json(source / "SOURCE_FINAL.json", final)
    expected = {e["path"] for e in entries if e["path"] != "."} | {"SOURCE_MANIFEST.json", "SOURCE_FINAL.json"}
    assert {p.relative_to(source).as_posix() for p in source.rglob("*")} == expected
    assert namespace(source, ("SOURCE_MANIFEST.json", "SOURCE_FINAL.json")) == entries
    return final


def acquire(record_id, row, expected_title):
    started = utc()
    source = PROJECT / "papers" / str(record_id) / "sources"
    assert not source.parent.exists(), f"Collision: {source.parent}"
    source.mkdir(parents=True)
    receipts, archives = [], []
    metadata = {"record_id": record_id, "row": row, "expected_identity_title": expected_title,
                "record_url": f"https://zenodo.org/records/{record_id}",
                "files_in_published_order": [], "archives": archives,
                "scientific_content_read": False, "native_scientific_programs_executed": False}
    failure = None
    try:
        api = source / "native-metadata/record-api.json"
        get_once(f"https://zenodo.org/api/records/{record_id}", api, receipts)
        native = json.loads(api.read_text())
        assert int(native["id"]) == record_id, "Record ID mismatch"
        assert native.get("status") == "published", "The assigned record is not published"
        fields = native["metadata"]
        assert native.get("doi") == f"10.5281/zenodo.{record_id}", "Native DOI differs from assigned record"
        metadata["assigned_title_literal_matches_native"] = fields["title"] == expected_title
        metadata.update(native_doi=native.get("doi"), native_doi_url=native.get("doi_url"),
                        native_conceptdoi=native.get("conceptdoi"), native_conceptrecid=native.get("conceptrecid"),
                        native_created=native.get("created"), native_modified=native.get("modified"),
                        native_updated=native.get("updated"), native_publication_date=fields.get("publication_date"),
                        native_status=native.get("status"), native_state=native.get("state"), native_submitted=native.get("submitted"),
                        native_version_field_present="version" in fields, native_version=fields.get("version"),
                        native_license=fields.get("license"), native_access_right=fields.get("access_right"),
                        native_title=fields["title"], native_relations=fields.get("relations"),
                        native_links=native.get("links"), native_related_identifiers=fields.get("related_identifiers"),
                        native_file_order=[f["key"] for f in native["files"]],
                        native_listed_asset_count=len(native["files"]))
        get_once(metadata["record_url"], source / "native-metadata/record-page.html", receipts)
        names = set()
        for ordinal, item in enumerate(native["files"], 1):
            name = leaf(item["key"])
            assert name not in names, "Duplicate native asset name"
            names.add(name)
            target = source / "zenodo-files" / name
            get_once(item["links"]["self"], target, receipts)
            observed = hashes(target)
            assert observed["bytes"] == item["size"], f"Native size mismatch for {name}"
            algorithm, literal = item["checksum"].split(":", 1)
            assert algorithm in ("md5", "sha256"), f"Unsupported native checksum: {algorithm}"
            width = 32 if algorithm == "md5" else 64
            assert re.fullmatch(r"[0-9a-fA-F]{1," + str(width) + r"}", literal)
            compared = literal.lower().zfill(width)
            assert observed[algorithm] == compared, f"Native checksum mismatch for {name}"
            metadata["files_in_published_order"].append({"ordinal": ordinal, "native_file_entry": item,
                "relative_path": target.relative_to(source).as_posix(), **observed,
                "native_checksum_literal": item["checksum"], "checksum_algorithm": algorithm,
                "checksum_comparison_hex": compared, "checksum_left_zero_padding_count": width - len(literal),
                "integrity_matches_native_metadata": True})
        budget = {"members": 0, "bytes": 0}
        pending = [(source / e["relative_path"], e["ordinal"], 0) for e in metadata["files_in_published_order"]]
        serial = 0
        while pending:
            target, ordinal, depth = pending.pop(0)
            if target.suffix.lower() not in (".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz"):
                continue
            assert depth <= MAX_ARCHIVE_DEPTH, "Nested archive depth bound exceeded"
            serial += 1
            label = f"{serial:02d}-{leaf(target.name)}"
            result = safe_archive(target, source / "archives" / (label + ".extracted"),
                                  source / "archives" / (label + ".members.json"), budget)
            if result is None:
                raise RuntimeError(f"Native/archive-suffixed file is not a supported ZIP/TAR archive: {target.name}")
            result.update(published_file_ordinal=ordinal, archive_depth=depth)
            archives.append(result)
            pending.extend((p, ordinal, depth + 1) for p in sorted(Path(result["extracted"]).rglob("*")) if p.is_file())
        outer = [e for e in metadata["files_in_published_order"] if e["relative_path"].lower().endswith("/paper.pdf")]
        if len(outer) == 1:
            metadata["outer_controlling_manuscript"] = {"identity_basis": "Native published outer asset named paper.pdf; not an embedded archive PDF",
                **{k: outer[0][k] for k in ("relative_path", "bytes", "sha256", "md5")}}
        metadata["embedded_pdf_locations"] = [p.relative_to(source).as_posix() for p in sorted((source / "archives").rglob("*.pdf"))] if (source / "archives").exists() else []
    except Exception as error:
        failure = {"UTC": utc(), "error_type": type(error).__name__, "literal_error": str(error),
                   "traceback": traceback.format_exc(), "record_stopped_no_retry": True}
        write_json(source / "SOURCE_FAILURE.json", failure)
        sys.stderr.write(f"record {record_id} stopped: {type(error).__name__}: {error}\n")
    final = close_source(source, record_id, metadata, receipts, started, failure, archives)
    return {"record_id": record_id, "row": row, "title": metadata.get("native_title", expected_title),
            "source_root": str(source), "status": final["status"],
            "actual_files": final["actual_file_count_including_terminal_controls"],
            "child_directories": final["actual_child_directory_count"],
            "published_assets": final["published_asset_count"],
            "archive_count": final["archive_count"], "archive_members": final["archive_member_count"],
            "manifest": {"path": str(source / "SOURCE_MANIFEST.json"), **hashes(source / "SOURCE_MANIFEST.json")},
            "final": {"path": str(source / "SOURCE_FINAL.json"), **hashes(source / "SOURCE_FINAL.json")},
            "outer_controlling_manuscript": final["outer_controlling_manuscript"],
            "native_version_field_present": metadata.get("native_version_field_present"),
            "native_version": metadata.get("native_version"),
            "native_file_order": metadata.get("native_file_order"),
            "source_custody_completion_percent": final["source_custody_completion_percent"],
            "scientific_review_completion_percent": 0}


def main():
    assert not (LANE / "EXTERNAL_SOURCE_PINS.json").exists(), "Refusing an acquisition rerun"
    for record_id, _, _ in RECORDS:
        assert not (PROJECT / "papers" / str(record_id)).exists(), "Preexisting packet collision"
    results = []
    for record in RECORDS:
        result = acquire(*record)
        results.append(result)
        print(json.dumps({k: result[k] for k in ("record_id", "row", "title", "status", "actual_files", "child_directories", "published_assets", "archive_count", "archive_members")}, ensure_ascii=False), flush=True)
    write_json(LANE / "EXTERNAL_SOURCE_PINS.json", {"schema": "external-source-custody-pins-v1",
               "UTC": utc(), "records": results, "scientific_review": "not performed"})
    success = all(r["source_custody_completion_percent"] == 100 for r in results)
    write_json(LANE / "ACQUISITION_RESULT.json", {"UTC": utc(), "status": "complete" if success else "one_or_more_records_stopped_after_failure",
               "source_custody_completion_percent": 100 if success else sum(r["source_custody_completion_percent"] for r in results) / len(results),
               "scientific_review_completion_percent": 0, "records": results,
               "native_scientific_execution": False, "contact_or_outreach_preparation": False,
               "git_sheet_deploy_release_zenodo_mutations": False})
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
