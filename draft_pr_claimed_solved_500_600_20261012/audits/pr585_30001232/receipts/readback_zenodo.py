#!/usr/bin/env python3
"""Read-only independent public metadata and file verification after publication."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

AUDIT = Path(__file__).resolve().parents[1]
PUB = AUDIT / "publication"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Math-Zenodo-Deposit-Tool/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), response.status, response.url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record_id", type=int)
    args = parser.parse_args()
    config = json.loads((PUB / "zenodo-deposit.json").read_text())
    raw, status, url = fetch(f"https://zenodo.org/api/records/{args.record_id}")
    if status != 200:
        raise RuntimeError("Public record unavailable")
    record = json.loads(raw)
    (AUDIT / "receipts/ZENODO_PUBLIC_API_RECORD.json").write_text(json.dumps(record, indent=2)+"\n")
    if record["id"] != args.record_id:
        raise RuntimeError("Wrong record id")
    actual = record["metadata"]
    checks = {}
    for name, expected in config["metadata"].items():
        if name == "license":
            value = actual[name]["id"]
        elif name == "upload_type":
            value = actual["resource_type"]["type"]
        elif name == "publication_type":
            value = actual["resource_type"]["subtype"]
        else:
            value = actual[name]
        if value != expected:
            raise RuntimeError("Public metadata differs: " + name)
        checks[name] = "exact" if name not in ("license", "upload_type", "publication_type") else "exact value; public representation mapped"
    files = {f["key"]: f for f in record["files"]}
    if set(files) != {f["path"] for f in config["files"]}:
        raise RuntimeError("Public file inventory differs")
    downloads = []
    for name, entry in files.items():
        link = entry["links"]["self"]
        parsed = urllib.parse.urlparse(link)
        if parsed.scheme != "https" or parsed.netloc != "zenodo.org" or not parsed.path.startswith(f"/api/records/{args.record_id}/files/"):
            raise RuntimeError("Unexpected public download URL")
        data, code, final = fetch(link)
        expected = (PUB / name).read_bytes()
        if code != 200 or data != expected or len(data) != entry["size"]:
            raise RuntimeError("Public download differs: " + name)
        downloads.append({"name": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                          "public_download_exact": True, "url": link})
    doi = actual["doi"]
    if doi != f"10.5281/zenodo.{args.record_id}":
        raise RuntimeError("Unexpected version DOI")
    _, code, destination = fetch("https://doi.org/" + doi)
    if code != 200 or not destination.startswith(f"https://zenodo.org/records/{args.record_id}"):
        raise RuntimeError("DOI resolution not confirmed")
    receipt = {"status": "PASS", "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "doi": doi, "metadata_checks": checks, "metadata_content_normalizations": [],
               "files": downloads, "doi_resolution": {"http_status": code, "resolved_url": destination}}
    (AUDIT / "receipts/ZENODO_PUBLIC_READBACK.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
