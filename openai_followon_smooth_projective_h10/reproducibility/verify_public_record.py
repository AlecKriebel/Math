#!/usr/bin/env python3
"""Verify published Zenodo public downloads using GET only; Python 3.10+.

This operational helper does not publish, read credentials, or modify the
reviewed payload. It writes a receipt only after the public record and all
four downloaded files match the project manifest and candidate inventory.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


PROJECT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT / "zenodo-deposit.json"
INVENTORY = PROJECT / "publication/CANDIDATE_INVENTORY.json"
RECEIPT = PROJECT / "receipts/zenodo_public_downloads.json"
USER_AGENT = "Math-Zenodo-Public-Record-Verifier/1.0 (read-only public download verification)"
MAX_JSON_BYTES = 1024 * 1024
MAX_FILE_BYTES = 64 * 1024 * 1024
CHUNK = 64 * 1024
TIMEOUT = 30


class VerificationError(Exception):
    pass


def hashes(path: Path) -> dict:
    sha = hashlib.sha256()
    md5 = hashlib.md5(usedforsecurity=False)
    size = 0
    with path.open("rb") as handle:
        while block := handle.read(CHUNK):
            size += len(block)
            sha.update(block)
            md5.update(block)
    return {"bytes": size, "sha256": sha.hexdigest(), "md5": md5.hexdigest()}


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise VerificationError(f"Expected a JSON object in {path.relative_to(PROJECT)}.")
    return value


def project_file(relative: str) -> Path:
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise VerificationError("Manifest/inventory file paths must be project-relative.")
    path = (PROJECT / relative).resolve()
    if not path.is_relative_to(PROJECT) or not path.is_file():
        raise VerificationError(f"Missing or non-project payload file: {relative!r}")
    return path


def file_name(value) -> str:
    if (not isinstance(value, str) or not value or value in {".", ".."}
            or "/" in value or "\\" in value or any(ord(c) < 32 for c in value)):
        raise VerificationError("Invalid or non-basename public file name.")
    return value


def local_expectations() -> tuple[dict, dict, dict, dict]:
    manifest = read_object(MANIFEST)
    inventory = read_object(INVENTORY)
    input_hashes = {
        "zenodo-deposit.json": hashes(MANIFEST)["sha256"],
        "publication/CANDIDATE_INVENTORY.json": hashes(INVENTORY)["sha256"],
    }
    if inventory.get("manifest_sha256") != input_hashes["zenodo-deposit.json"]:
        raise VerificationError("The manifest differs from the frozen candidate inventory.")
    manifest_files = manifest.get("files")
    inventory_files = inventory.get("files")
    if (not isinstance(manifest_files, list) or len(manifest_files) != 4
            or not isinstance(inventory_files, list) or len(inventory_files) != 4):
        raise VerificationError("Expected exactly four files in both manifest and inventory.")

    by_path = {}
    for entry in inventory_files:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise VerificationError("Invalid candidate inventory file entry.")
        path = entry["path"]
        if path in by_path:
            raise VerificationError("Duplicate path in candidate inventory.")
        if (type(entry.get("bytes")) is not int or not 0 < entry["bytes"] <= MAX_FILE_BYTES
                or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256", "")))
                or not re.fullmatch(r"[0-9a-f]{32}", str(entry.get("md5", "")))):
            raise VerificationError(f"Invalid size or checksums in inventory for {path!r}.")
        by_path[path] = entry

    expected = {}
    seen_paths = set()
    for entry in manifest_files:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise VerificationError("Invalid manifest file entry.")
        relative = entry["path"]
        path = project_file(relative)
        name = file_name(entry.get("name", path.name))
        if name in expected or relative in seen_paths or relative not in by_path:
            raise VerificationError("Manifest paths/names do not uniquely match the inventory.")
        wanted = {key: by_path[relative][key] for key in ("bytes", "sha256", "md5")}
        if hashes(path) != wanted:
            raise VerificationError(f"Local reviewed payload differs from inventory: {name}")
        expected[name] = {"path": relative, **wanted}
        seen_paths.add(relative)
    if seen_paths != set(by_path):
        raise VerificationError("Manifest and inventory file sets differ.")
    if not isinstance(manifest.get("metadata"), dict):
        raise VerificationError("The local manifest has no metadata object.")
    return manifest, inventory, expected, input_hashes


def public_url(value) -> str:
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 for c in value):
        raise VerificationError("Invalid public download URL.")
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError as error:
        raise VerificationError("Malformed public download URL.") from error
    if (parts.scheme != "https" or parts.hostname != "zenodo.org"
            or parts.username is not None or parts.password is not None
            or port not in (None, 443) or parts.fragment):
        raise VerificationError("Public links must use HTTPS on zenodo.org without credentials.")
    # Public record links normally have no query or only download=1. Refuse
    # token/signature query parameters rather than following an authenticated link.
    if parts.query and parse_qs(parts.query, keep_blank_values=True) != {"download": ["1"]}:
        raise VerificationError("Unexpected query parameters in a public download link.")
    return value


class PublicRedirects(HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, request, fp, code, message, headers, new_url):
        if request.get_method() != "GET":
            raise VerificationError("Only GET requests are permitted.")
        public_url(new_url)
        return super().redirect_request(request, fp, code, message, headers, new_url)


def get(opener, url: str, accept: str):
    request = Request(
        public_url(url), method="GET",
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
    response = opener.open(request, timeout=TIMEOUT)
    try:
        public_url(response.geturl())
        if response.status != 200:
            raise VerificationError(f"Public GET returned HTTP {response.status}.")
    except Exception:
        response.close()
        raise
    return response


def public_metadata(record: dict, record_id: int, wanted: dict) -> dict:
    actual_id = record.get("id")
    if not (type(actual_id) is int or
            isinstance(actual_id, str) and re.fullmatch(r"[1-9][0-9]*", actual_id)):
        raise VerificationError("Public API returned an invalid record ID.")
    if int(actual_id) != record_id:
        raise VerificationError("Public API returned a different record ID.")
    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        raise VerificationError("Public API returned no metadata object.")
    dois = [value for value in (record.get("doi"), metadata.get("doi")) if value is not None]
    if (not dois or any(not isinstance(value, str)
                       or not re.fullmatch(r"10\.[0-9]{4,9}/[^\s]+", value) for value in dois)
            or len({value.lower() for value in dois}) != 1):
        raise VerificationError("The public record has no consistent, nonempty assigned DOI.")
    title = metadata.get("title")
    publication_date = metadata.get("publication_date")
    creators = metadata.get("creators")
    if not isinstance(title, str) or not title.strip() or title != wanted.get("title"):
        raise VerificationError("Public title is empty or differs from the reviewed manifest.")
    if not isinstance(publication_date, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", publication_date):
        raise VerificationError("Public publication date is missing or invalid.")
    date.fromisoformat(publication_date)
    if publication_date != wanted.get("publication_date"):
        raise VerificationError("Public publication date differs from the reviewed manifest.")
    expected_creators = wanted.get("creators")
    if (not isinstance(creators, list) or not creators
            or not isinstance(expected_creators, list) or len(creators) != len(expected_creators)):
        raise VerificationError("Public creators are missing or differ from the manifest.")
    for actual, expected in zip(creators, expected_creators):
        if not isinstance(actual, dict) or not isinstance(expected, dict):
            raise VerificationError("Invalid public creator metadata.")
        if actual != expected and not (
            "affiliation" not in expected and actual == {**expected, "affiliation": None}
        ):
            raise VerificationError("Public creator metadata differs from the reviewed manifest.")
    return {"title": title, "creators": creators, "publication_date": publication_date, "doi": dois[0]}


def public_files(record: dict, expected: dict) -> dict:
    entries = record.get("files")
    if not isinstance(entries, list):
        raise VerificationError("Unrecognized public API file-list schema; inspect it before adapting this helper.")
    actual = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise VerificationError("Invalid public API file entry.")
        names = [entry[key] for key in ("key", "name", "filename") if entry.get(key) is not None]
        if not names or len(set(names)) != 1:
            raise VerificationError("Public file name is missing or inconsistent.")
        name = file_name(names[0])
        if name in actual:
            raise VerificationError("Duplicate public file name.")
        actual[name] = entry
    if set(actual) != set(expected):
        raise VerificationError(f"Public file set differs: expected {sorted(expected)}, found {sorted(actual)}.")
    result = {}
    for name, entry in actual.items():
        size = entry.get("size", entry.get("filesize"))
        if isinstance(size, str) and re.fullmatch(r"[0-9]+", size):
            size = int(size)
        if type(size) is not int or size != expected[name]["bytes"]:
            raise VerificationError(f"Public API file size differs from inventory: {name}")
        checksum = entry.get("checksum")
        if not isinstance(checksum, str):
            raise VerificationError(f"Public API checksum is missing: {name}")
        checksum = checksum.lower()
        if re.fullmatch(r"[0-9a-f]{32}", checksum):
            checksum = "md5:" + checksum
        algorithm, separator, digest = checksum.partition(":")
        if not separator or algorithm not in {"md5", "sha256"} or digest != expected[name][algorithm]:
            raise VerificationError(f"Public API checksum differs from inventory: {name}")
        links = entry.get("links")
        if not isinstance(links, dict):
            raise VerificationError(f"Public download links are missing: {name}")
        url = links.get("download") or links.get("self")
        result[name] = {"url": public_url(url), "api_checksum": checksum}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-id", required=True, help="Positive decimal ID of the already-published production record.")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or later is required.")
    if not re.fullmatch(r"[1-9][0-9]*", args.record_id):
        parser.error("--record-id must contain only ASCII decimal digits and be positive, without leading zeros.")
    record_id = int(args.record_id)
    started = datetime.now(timezone.utc).isoformat()
    manifest, _, expected, input_hashes = local_expectations()
    # Disable proxy environment handling and add no authentication/cookie handlers.
    # This helper never reads a token, secret file, or deposit state.
    opener = build_opener(ProxyHandler({}), PublicRedirects())
    record_url = f"https://zenodo.org/api/records/{record_id}"
    with get(opener, record_url, "application/json") as response:
        body = response.read(MAX_JSON_BYTES + 1)
    if len(body) > MAX_JSON_BYTES:
        raise VerificationError("Public API response exceeds the JSON size limit.")
    record = json.loads(body)
    if not isinstance(record, dict):
        raise VerificationError("Public API response is not a JSON object.")
    metadata = public_metadata(record, record_id, manifest["metadata"])
    files = public_files(record, expected)
    tmp_parent = PROJECT / "tmp"
    tmp_parent.mkdir(exist_ok=True)
    verified = []
    with tempfile.TemporaryDirectory(prefix="zenodo-public-downloads-", dir=tmp_parent) as temporary:
        for name in sorted(expected):
            destination = Path(temporary) / name
            remaining = expected[name]["bytes"]
            # Observed on production record 23205305: the /api/records/.../
            # files/.../content endpoint rejects Accept: application/octet-stream
            # with HTTP 406, explicitly requiring application/json. With that
            # API Accept header it returns the actual binary file with HTTP 200
            # and Content-Type: application/octet-stream. Retain the truthful
            # User-Agent; this is content negotiation, not traffic-filter evasion.
            download_accept = (
                "application/json" if urlsplit(files[name]["url"]).path.startswith("/api/")
                else "*/*"
            )
            with get(opener, files[name]["url"], download_accept) as response, destination.open("xb") as output:
                while block := response.read(min(CHUNK, remaining + 1)):
                    remaining -= len(block)
                    if remaining < 0:
                        raise VerificationError(f"Public download exceeds its expected byte size: {name}")
                    output.write(block)
            actual = hashes(destination)
            wanted = {key: expected[name][key] for key in ("bytes", "sha256", "md5")}
            if actual != wanted:
                raise VerificationError(f"Public downloaded bytes differ from the reviewed inventory: {name}")
            verified.append({"name": name, **actual, **files[name], "request_accept": download_accept})
            print(f"Verified public download: {name} ({actual['bytes']} bytes)", flush=True)

    if (hashes(MANIFEST)["sha256"] != input_hashes["zenodo-deposit.json"]
            or hashes(INVENTORY)["sha256"] != input_hashes["publication/CANDIDATE_INVENTORY.json"]):
        raise VerificationError("Manifest or inventory changed during public verification; no receipt written.")
    for name, entry in expected.items():
        if hashes(project_file(entry["path"])) != {key: entry[key] for key in ("bytes", "sha256", "md5")}:
            raise VerificationError(f"Local reviewed payload changed during public verification: {name}")
    receipt = {
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "record_id": record_id,
        "public_api_url": record_url,
        "record_url": f"https://zenodo.org/records/{record_id}",
        "public_metadata": metadata,
        "input_sha256": input_hashes,
        "verifier_sha256": hashes(Path(__file__).resolve())["sha256"],
        "files": verified,
        "public_downloads_match_reviewed_inventory": True,
        "reviewed_payload_modified": False,
        "credentials_read": False,
        "network_methods": ["GET"],
        "doi_resolution_checked": False,
    }
    RECEIPT.parent.mkdir(exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: public record metadata and all four downloadable files match the reviewed package.")
    print("Receipt: receipts/zenodo_public_downloads.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HTTPError as error:
        status = error.code
        error.close()
        print(f"Verification failed: public Zenodo GET returned HTTP {status}; no publication action was made.", file=sys.stderr)
        raise SystemExit(1)
    except (VerificationError, URLError, OSError, ValueError, TypeError, KeyError) as error:
        print(f"Verification failed: {error}; no publication action was made.", file=sys.stderr)
        raise SystemExit(1)
