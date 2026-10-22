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
    "main.tex", "paper.pdf", "square_flow_certificate.json.gz",
    "verify_currents.py", "CURRENT_RESULTS.json",
    "check_reductions.py", "REDUCTION_RESULTS.json",
    "README.md", "DEPENDENCIES.md", "PRIORITY.md",
    "LICENSE-PROSE.txt", "LICENSE-CODE.txt", "PROVENANCE.json",
    "zenodo-metadata.json", "build_release.py",
]
PDF = "graph-square-forest-degree.pdf"
SOURCE = "graph-square-forest-degree-source-and-verification.zip"
KIT = "graph-square-forest-degree-upload-kit.zip"
UPLOAD_README = """LOCAL PREPARATION ONLY. No record, DOI, upload, merge or publication is performed by this package.
Scientific deposit files: graph-square-forest-degree.pdf and graph-square-forest-degree-source-and-verification.zip.
zenodo-metadata.json and zenodo-deposit.json describe exactly those two files.
The five-member upload kit contains the two scientific files, metadata, deposit manifest, and this README.
The paper proves a specific nonunimodular grandparent-graph counterexample, with an explicit forest-derived b_F convention. It does not refute the unimodular subclass or Cayley case.
The entire finite rational-current certificate, independent exact checker, exact results, finite circuit checks, both infinite free-exhaustion proofs, source, dependencies, priority limits, licenses and frozen PDF are in the source ZIP.
No exhaustive historical firstness or continuing-openness certificate is claimed. Actual inspected Tang and Pete–Timár bodies are arXiv v2, not the inaccessible final journal bodies.
The offline packaging rebuild copies the frozen PDF and does not recompile TeX or certify mathematics or priority.
Two fresh independent whole-package reviews and root adoption are required; publication_ready remains false.
No operational upload tool, private capture, account data, or third-party source body is distributed.
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
    require(metadata["title"] == "Free spanning-forest degree can decrease under squaring",
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
