#!/usr/bin/env python3
"""Read-only public-byte, manifest and DOI verification of the saved publication."""
import argparse
import datetime as dt
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
import uuid
import zipfile

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "zenodo_deposit_tool"))
import zenodo
from publication_live_gates import require_release_clearance
from sweep_io import atomic_bytes, atomic_json


def fetch(url):
    request = Request(url, headers={"User-Agent": "Math-publication-verification/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read(), response.status, response.url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deposit-id", type=int, required=True)
    args = parser.parse_args()
    require_release_clearance()
    manifest = AUDIT / "preprint/publication/zenodo-deposit.json"
    metadata, selected = zenodo.load_manifest(manifest)
    # The established tool verifies every intended metadata field against the
    # saved exact-ID deposition, every file checksum/size and the public DOI.
    inspection = zenodo.run(argparse.Namespace(command="inspect", manifest=manifest,
                                               sandbox=False, check_doi=True))
    identifier = args.deposit_id
    if (inspection["id"] != identifier or inspection["state"] != "published"
            or inspection["doi"] != "10.5281/zenodo." + str(identifier)
            or inspection["doi_resolution"].get("http_status") != 200):
        raise RuntimeError("Saved record is not the exact verified published DOI")
    atomic_json(AUDIT / "ZENODO_PUBLISHED_INSPECTION.json", inspection)
    operation = uuid.uuid4().hex
    raw = ROOT / "raw/pr0397" / ("public_files_" + operation)
    raw.mkdir()
    body, status, resolved = fetch("https://zenodo.org/api/records/" + str(identifier))
    atomic_bytes(raw / "record.json", body)
    public = json.loads(body)
    if (status != 200 or int(public["id"]) != identifier
            or public["doi"] != inspection["doi"]
            or public["metadata"]["title"] != metadata["title"]
            or public["metadata"]["version"] != metadata["version"]):
        raise RuntimeError("Public record identity/title/version/DOI differs")
    files = zenodo.server_files(public)
    if set(files) != {v["name"] for v in selected}:
        raise RuntimeError("Public record has missing or unexpected payloads")
    results = []
    for entry in selected:
        name = entry["name"]
        if not zenodo.matching_file(files[name], entry):
            raise RuntimeError("Public file metadata checksum/size differs")
        url = "https://zenodo.org/records/" + str(identifier) + "/files/" + quote(name, safe="") + "?download=1"
        data, code, destination = fetch(url)
        atomic_bytes(raw / name, data)
        if (code != 200 or len(data) != entry["size"]
                or hashlib.sha256(data).hexdigest() != entry["sha256"]
                or hashlib.md5(data).hexdigest() != entry["md5"]):
            raise RuntimeError("Actual public bytes differ from reviewed payload: " + name)
        result = {"name": name, "bytes": len(data), "sha256": entry["sha256"],
                  "md5": entry["md5"], "http_status": code, "downloaded_and_matches_reviewed": True}
        if name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = archive.namelist()
                if len(names) != len(set(names)) or archive.testzip() is not None:
                    raise RuntimeError("Public ZIP duplicate member or CRC error")
                for info in archive.infolist():
                    path = PurePosixPath(info.filename)
                    if path.is_absolute() or ".." in path.parts or path.as_posix() != info.filename:
                        raise RuntimeError("Unsafe ZIP member")
                    if info.external_attr >> 16 & 0o170000 == 0o120000:
                        raise RuntimeError("Symlink ZIP member")
                prefix = "congestion-fragmentation-verification/"
                declared = json.loads(archive.read(prefix + "MANIFEST.json"))["files"]
                if set(names) != {prefix + "MANIFEST.json"} | {prefix + p for p in declared}:
                    raise RuntimeError("Public archive manifest set is not exact")
                for path, expected in declared.items():
                    payload = archive.read(prefix + path)
                    if len(payload) != expected["bytes"] or hashlib.sha256(payload).hexdigest() != expected["sha256"]:
                        raise RuntimeError("Public archive internal payload differs")
                result.update(zip_crc_safe_unique_pass=True, members=len(names),
                              all_manifest_payloads_verified=len(declared))
        results.append(result)
    receipt = {"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), "pr": 397,
               "record": identifier, "doi": inspection["doi"], "doi_url": inspection["doi_url"],
               "title": metadata["title"], "files": results,
               "all_public_file_bytes_match_reviewed": True,
               "all_intended_metadata_verified_by_existing_tool": True,
               "metadata_normalizations": inspection["metadata_normalizations"],
               "doi_resolution": {"status": inspection["doi_resolution"]["http_status"],
                                  "resolved_url": inspection["doi_resolution"]["resolved_url"]},
               "record_http_status": status, "raw_receipts": raw.relative_to(ROOT).as_posix(),
               "read_only_remote_operations": True}
    atomic_json(AUDIT / "ZENODO_PUBLIC_FILE_VERIFICATION.json", receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
