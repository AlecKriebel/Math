#!/usr/bin/env python3
"""Build deterministic archives and static page files; never upload anything.

Run from any directory: python3 build_package.py [--deploy-copy]
--deploy-copy additionally copies the finished page to this repository's docs/.
The PDF is built separately from manuscript/paper.tex; see README.md.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parent
NAME = "radial_statistical_counterexample"
STAMP = (2026, 9, 22, 0, 0, 0)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def manifest(entries):
    return "".join(f"{digest(data)}  {name}\n" for name, data in sorted(entries.items())).encode()


def archive(path, entries):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deploy-copy", action="store_true")
    args = parser.parse_args()
    metadata = json.loads((ROOT / "zenodo/metadata.json").read_text())
    required = {"title", "upload_type", "publication_type", "publication_date",
                "creators", "description", "access_right", "license", "version"}
    if not required.issubset(metadata):
        raise RuntimeError("Required metadata fields missing")
    if metadata["creators"][0]["orcid"] != "0009-0001-9320-500X":
        raise RuntimeError("Unexpected author ORCID")
    # Prepared payload, not a submission and not a claim of server validation.
    (ROOT / "zenodo/metadata-for-api.json").write_text(
        json.dumps({"metadata": metadata}, indent=2, ensure_ascii=False) + "\n")

    required_files = ["README.md", "LICENSES.md", "CITATION.cff", "build_package.py",
                      "manuscript/paper.tex", "output/pdf/paper.pdf",
                      "research/VERIFICATION_REPORT.md", "research/SOURCE_AUDIT.md",
                      "research/sources.json", "research/RESEARCH_LOG.md",
                      "reviews/proof_audit.md", "reviews/priority_audit.md",
                      "reviews/computation_review.md", "reviews/final_manuscript_audit.md",
                      "verification/verify_exact.py", "verification/exact_output.txt",
                      "verification/verify_symbolic.py", "verification/symbolic_output.txt",
                      "verification/requirements.txt", "site/index.html", "site/style.css",
                      "zenodo/metadata.json", "zenodo/metadata-for-api.json", "zenodo/UPLOAD.md"]
    # Include subsequent release audit notes, but never downloaded source PDFs,
    # scratch files, logs, environments, or previous ZIP archives.
    optional = ["research/DELIVERY_CHECKS.md", "reviews/package_audit.md",
                "research/DATABASE_RECHECK.md", "reviews/priority_followup.md",
                "reviews/priority_followup_citations.md",
                "reviews/priority_followup_indexes.md",
                "reviews/priority_followup_older_sources.md",
                "reviews/priority_followup_japanese.md",
                "research/priority_evidence/citation_inventory.csv",
                "research/priority_evidence/fulltext_manifest.json",
                "research/priority_evidence/supplied_papers.json",
                "reviews/priority_supplied_papers.md",
                "reviews/priority_supplied_matsuzoe1999.md",
                "reviews/priority_supplied_matsuzoe2010.md",
                "reviews/priority_supplied_kurose2024.md"]
    required_files.extend(p for p in optional if (ROOT / p).is_file())
    entries = {name: (ROOT / name).read_bytes() for name in required_files}
    checks = manifest(entries)
    (ROOT / "SOURCE_SHA256SUMS.txt").write_bytes(checks)
    entries["SOURCE_SHA256SUMS.txt"] = checks
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    source_zip = output / "source-and-verification.zip"
    archive(source_zip, {NAME + "/" + name: data for name, data in entries.items()})

    payload = {"paper.pdf": entries["output/pdf/paper.pdf"],
               "source-and-verification.zip": source_zip.read_bytes()}
    payload_checks = manifest(payload)
    (ROOT / "zenodo/SHA256SUMS.txt").write_bytes(payload_checks)
    kit = {"files/" + name: data for name, data in payload.items()}
    kit["files/SHA256SUMS.txt"] = payload_checks
    for name in ("UPLOAD.md", "metadata.json", "metadata-for-api.json"):
        kit[name] = (ROOT / "zenodo" / name).read_bytes()
    kit["LICENSES.md"] = entries["LICENSES.md"]
    kit_zip = output / "zenodo-upload-kit.zip"
    archive(kit_zip, kit)

    page = output / "site"
    page.mkdir(exist_ok=True)
    web_entries = {**payload, "zenodo-upload-kit.zip": kit_zip.read_bytes(),
                   "verification-report.md": entries["research/VERIFICATION_REPORT.md"],
                   "priority-audit.md": entries["reviews/priority_audit.md"],
                   "index.html": entries["site/index.html"], "style.css": entries["site/style.css"]}
    web_entries["SHA256SUMS.txt"] = manifest(web_entries)
    for name, data in web_entries.items():
        (page / name).write_bytes(data)
    if args.deploy_copy:
        repo = ROOT.parent
        if not (repo / ".git").exists() or not (repo / "docs/index.html").is_file():
            raise RuntimeError("--deploy-copy requires the original repository with docs/")
        destination = repo / "docs/papers/radial-statistical-counterexample"
        destination.mkdir(parents=True, exist_ok=True)
        for name in web_entries:
            shutil.copy2(page / name, destination / name)
        print("Deployment copy:", destination)
    print("Source archive:", source_zip)
    print("Zenodo upload kit:", kit_zip)
    print("Static page:", page / "index.html")
    print("All manifest paths are relative to their respective package root.")


if __name__ == "__main__":
    main()
