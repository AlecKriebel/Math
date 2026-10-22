#!/usr/bin/env python3
"""Offline reproducible packaging only. Python >=3.10, stdlib. MIT licensed.
Never calls a service, accesses credentials, or mutates an existing output.
The frozen paper.pdf is copied, not recompiled. No mathematical certification.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import zipfile

MEMBERS = [
    "manuscript/main.tex", "paper.pdf", "exact_checks.py", "CHECK_RESULTS.json",
    "README.md", "DEPENDENCIES.md", "PRIORITY.md",
    "LICENSE-PROSE.txt", "LICENSE-CODE.txt", "zenodo-metadata.json",
    "build_release.py",
]
PDF = "initial-odd-ear-prefix.pdf"
SOURCE = "initial-odd-ear-prefix-source-and-verification.zip"
KIT = "initial-odd-ear-prefix-upload-kit.zip"
UPLOAD_README = """LOCAL PACKAGING ONLY. This kit does not create a draft, reserve a DOI, upload, merge or publish.
Scientific deposit files: initial-odd-ear-prefix.pdf and initial-odd-ear-prefix-source-and-verification.zip.
zenodo-metadata.json and zenodo-deposit.json describe precisely those two files.
The five-member upload kit contains both scientific files, metadata, deposit manifest and this README.
The source ZIP includes the exact manuscript, frozen PDF, finite diagnostics/results, dependency and priority scope, licenses, offline builder and source-member manifest.
The proof concerns variable thresholds and initial consecutive odd OPEN ears, including initial circuit and one-edge ears; no fixed-threshold or total-odd-ear hardness is claimed.
The packaging rebuild uses the frozen PDF and does not recompile TeX or certify mathematical correctness or literature priority.
Independent review and root adoption, plus fresh live duplicate/integration checks, must precede any service action.
No account data, credential, private source body or operational publication driver is distributed.
"""
def require(test, message):
    if not test:
        raise RuntimeError(message)
def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+"\n").encode()
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def zipbytes(mapping):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, strict_timestamps=True) as z:
        for name in sorted(mapping):
            zi = zipfile.ZipInfo(name, date_time=(2026,10,22,0,0,0))
            zi.create_system = 3
            zi.external_attr = (0o100644 << 16)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, mapping[name], compress_type=zipfile.ZIP_DEFLATED,
                       compresslevel=9)
    raw = out.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(z.namelist() == sorted(mapping), "archive names changed")
        require(z.testzip() is None, "archive CRC failure")
        for name, content in mapping.items():
            require(z.read(name) == content, "archive bytes changed")
    return raw
def build(root, output):
    require(not output.exists(), "output must not already exist")
    content = {n:(root/n).read_bytes() for n in MEMBERS}
    manifest = {"schema":"scientific-source-members-v1",
                "license_prose":"CC-BY-4.0","license_code":"MIT",
                "files":[{"path":n,"bytes":len(content[n]),"sha256":digest(content[n])}
                         for n in sorted(content)]}
    mb = jbytes(manifest)
    require((root/"source-manifest.json").read_bytes() == mb,
            "source members differ from source-manifest.json")
    content["source-manifest.json"] = mb
    source = zipbytes(content)
    metadata_raw = content["zenodo-metadata.json"]
    metadata = json.loads(metadata_raw)
    require(metadata["title"] == "NP-completeness of the initial odd-ear prefix",
            "unexpected metadata title")
    require(metadata["publication_type"] == "preprint", "unexpected publication type")
    require("doi" not in metadata and "prereserve_doi" not in metadata,
            "unexpected DOI assignment")
    deposit = {"metadata":metadata,
               "files":[{"path":PDF,"name":PDF},{"path":SOURCE,"name":SOURCE}]}
    out = {PDF:content["paper.pdf"],SOURCE:source,
           "zenodo-metadata.json":metadata_raw,
           "zenodo-deposit.json":jbytes(deposit),
           "UPLOAD_README.txt":UPLOAD_README.encode()}
    out[KIT] = zipbytes(out)
    output.mkdir(parents=True)
    for n, raw in out.items():
        (output/n).write_bytes(raw)
    for n, raw in out.items():
        require((output/n).read_bytes() == raw, "release readback failed")
    return {"status":"PASS","pdf_recompiled":False,"network_used":False,
            "publication_performed":False,
            "files":[{"name":n,"bytes":len(out[n]),"sha256":digest(out[n])}
                     for n in sorted(out)]}
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(Path(__file__).resolve().parent,args.output.resolve()),
                     sort_keys=True,indent=2))

