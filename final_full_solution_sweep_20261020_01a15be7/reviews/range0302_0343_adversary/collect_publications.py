#!/usr/bin/env python3
"""Read-only fresh public records and complete payload download, confined to this review."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import io
import json
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
SWEEP = HERE.parent.parent
RAW = HERE / "raw/private"
RECORDS = {302: 23157237, 305: 23149775, 311: 23146753, 329: 23137834}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Independent-research-identity-audit/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(), response.status, response.url


def collect(item):
    pr, record = item
    directory = RAW / f"publication_pr{pr:04d}"
    directory.mkdir(exist_ok=True)
    summary = {"pr": pr, "record": record, "observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        data, status, url = fetch(f"https://zenodo.org/api/records/{record}")
        (directory / "record.json").write_bytes(data)
        metadata = json.loads(data)
        summary.update(metadata_http_status=status, metadata_final_url=url,
                       metadata_sha256=hashlib.sha256(data).hexdigest(), doi=metadata.get("doi"),
                       published=metadata.get("submitted"), state=metadata.get("state"),
                       title=metadata["metadata"]["title"])
        summary["files"] = []
        prior = json.loads((SWEEP / f"PR{pr:04d}_PUBLICATION_VERIFICATION.json").read_text())
        prior_files = {file["name"]: file for file in prior["files"]}
        for file in metadata["files"]:
            name = file["key"]
            if Path(name).name != name:
                raise ValueError("unsafe public file name")
            body, file_status, file_url = fetch(file["links"]["self"])
            (directory / name).write_bytes(body)
            identity = {"name": name, "bytes": len(body), "http_status": file_status,
                        "url": file_url, "sha256": hashlib.sha256(body).hexdigest(),
                        "md5": hashlib.md5(body).hexdigest(), "record_size": file["size"],
                        "record_checksum": file["checksum"]}
            identity["record_size_matches"] = identity["bytes"] == file["size"]
            identity["record_checksum_matches"] = file["checksum"] == "md5:" + identity["md5"]
            identity["root_size_matches"] = prior_files[name]["size"] == len(body)
            identity["root_sha256_matches"] = prior_files[name]["sha256"] == identity["sha256"]
            if name.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    identity["zip_crc_ok"] = archive.testzip() is None
                    identity["members"] = archive.namelist()
                    identity["root_members_match"] = sorted(archive.namelist()) == sorted(prior_files[name]["members"])
                    identity["duplicate_members"] = len(archive.namelist()) != len(set(archive.namelist()))
                    for member in archive.namelist():
                        if member.endswith((".tex", "/MANIFEST.json", "/README.md")) or member in ["MANIFEST.json", "README.md"]:
                            target = directory / "selected" / member
                            if ".." in Path(member).parts or Path(member).is_absolute():
                                raise ValueError("unsafe ZIP member")
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(archive.read(member))
            summary["files"].append(identity)
        _, status, url = fetch(f"https://doi.org/10.5281/zenodo.{record}")
        summary["doi_resolution"] = {"http_status": status, "final_url": url}
    except Exception as error:
        summary["error"] = f"{type(error).__name__}: {error}"
    return summary


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        summaries = list(executor.map(collect, RECORDS.items()))
    (HERE / "publications_fresh.json").write_text(json.dumps(summaries, indent=2) + "\n")
    for summary in summaries:
        print(json.dumps({key: value for key, value in summary.items() if key != "files"}))
        for file in summary.get("files", []):
            print(summary["pr"], file["name"], {key: value for key, value in file.items() if key.endswith("matches") or key.endswith("ok")})
