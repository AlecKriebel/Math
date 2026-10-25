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
from html.parser import HTMLParser

MEMBERS = [
    "main.tex", "paper.pdf", "exact_checks.py", "CHECK_RESULTS.json",
    "README.md", "DEPENDENCIES.md", "PRIORITY.md", "PROVENANCE.md", "DESCRIPTION_PARAGRAPHS.json",
    "LICENSE-PROSE.txt", "LICENSE-CODE.txt", "zenodo-metadata.json",
    "build_release.py",
]
PDF = "bray-sp-o.pdf"
SOURCE = "bray-sp-o-source-and-verification.zip"
KIT = "bray-sp-o-upload-kit.zip"
UPLOAD_README = """LOCAL PREPARATION ONLY. No record, DOI, upload, merge or publication is performed by this package.
Scientific deposit files: bray-sp-o.pdf and bray-sp-o-source-and-verification.zip.
zenodo-metadata.json and zenodo-deposit.json describe exactly those two files.
The five-member upload kit contains the two scientific files, metadata, deposit manifest, and this README.
The proof uses precisely stated published structural results. Prior GL/GU solutions, distinguished2-part and diagonal-escape strategies are credited; no global firstness is claimed.
The source ZIP includes the exact manuscript, finite diagnostics, dependencies, priority limits, licenses, and the frozen PDF as offline packaging input.
This packaging rebuild does not recompile TeX or certify mathematics or priority.
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
    require(metadata["title"] == "Logarithmic Bray sampling in symplectic and orthogonal groups",
            "unexpected metadata title")
    require(metadata["publication_type"] == "preprint", "unexpected publication type")
    class Paragraphs(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True); self.paras=[]; self.inside=False
        def handle_starttag(self, tag, attrs):
            require(tag=="p" and not attrs and not self.inside, "nonparagraph markup")
            self.inside=True; self.paras.append("")
        def handle_endtag(self, tag):
            require(tag=="p" and self.inside, "unbalanced paragraph")
            self.inside=False
        def handle_data(self, value):
            require(self.inside, "outside paragraph text")
            self.paras[-1]+=value
    hp=Paragraphs();hp.feed(metadata["description"]);hp.close()
    require(not hp.inside and hp.paras==json.loads(content["DESCRIPTION_PARAGRAPHS.json"]),
            "description Unicode or quantified scope differs")
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
