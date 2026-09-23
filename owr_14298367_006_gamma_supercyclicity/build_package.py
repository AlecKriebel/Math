#!/usr/bin/env python3
"""Build the compact source archive, manual Zenodo kit, and Pages files.

No network upload, DOI creation, GitHub release, or git mutation is performed.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
VERSION = "1.0.1"
DATE = "2026-09-23"
TITLE = "A note on Γ-supercyclicity of dissipative composition operators"
SITE = "https://aleckriebel.github.io/Math/papers/gamma-supercyclicity/"
REPO = "https://github.com/AlecKriebel/Math/tree/main/owr_14298367_006_gamma_supercyclicity"
DESCRIPTION = (
    "This research note records an affirmative answer to the arbitrary-Gamma "
    "supercyclicity question in Emma D'Aniello's contribution (joint work with "
    "Martina Maiuriello), p.1083 of Oberwolfach Report 19/2024. In the report's "
    "separable complex Lp setting, 1 <= p < infinity, a dissipative composition "
    "operator of bounded distortion is Gamma-supercyclic if and only if its "
    "associated bilateral weighted shift is Gamma-supercyclic, for every "
    "subset Gamma of the complex numbers.\n\n"
    "The note makes explicit an application of earlier results of Arafat Abbar "
    "(2019) and Arafat Abbar and Yulia Kuznetsova (2020 preprint; 2021 journal "
    "article). It includes a direct proof and a deduction from the earlier "
    "translation theorem. Neither the scalar criterion nor the amplification "
    "mechanism is claimed as new. The original separability assumption is "
    "retained explicitly.\n\n"
    "This is an AI-assisted, unrefereed research note, not an external "
    "peer-review or formal proof-assistant certificate. The deposit contains "
    "the PDF and self-contained LaTeX source archive."
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def make_zip(path, entries):
    """Stable member order, timestamps and permissions; entries map name to file."""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, source in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        assert archive.namelist() == sorted(entries)
        for name, source in entries.items():
            assert archive.read(name) == source.read_bytes()


def checksums(directory, files, name="SHA256SUMS.txt"):
    text = "".join(f"{digest(directory / file)}  {file}\n" for file in sorted(files))
    (directory / name).write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile", action="store_true", help="compile the note with Tectonic")
    parser.add_argument("--deploy-site", action="store_true", help="copy files to this repository's docs/papers/gamma-supercyclicity")
    args = parser.parse_args()
    (OUTPUT / "pdf").mkdir(parents=True, exist_ok=True)
    if args.compile:
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = str(int(datetime(2026, 9, 23, tzinfo=timezone.utc).timestamp()))
        subprocess.run(["tectonic", "--keep-logs", "--outdir", str(OUTPUT / "pdf"), "note.tex"],
                       cwd=ROOT / "manuscript", env=env, check=True)
    pdf = OUTPUT / "pdf" / "note.pdf"
    if not pdf.exists() or not pdf.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("Compile the final note first with --compile.")
    log = OUTPUT / "pdf" / "note.log"
    if log.exists() and "Overfull" in log.read_text():
        raise RuntimeError("Resolve the PDF's overfull box before packaging.")
    source = OUTPUT / "note-source.zip"
    make_zip(source, {"note.tex": ROOT / "manuscript/note.tex",
                      "README.md": ROOT / "manuscript/README.md",
                      "LICENSES.md": ROOT / "LICENSES.md",
                      "CITATION.bib": ROOT / "CITATION.bib"})
    metadata = {
        "title": TITLE, "upload_type": "publication", "publication_type": "preprint",
        "publication_date": DATE, "description": DESCRIPTION,
        "creators": [{"name": "Kriebel, Alec", "affiliation": "Independent researcher",
                      "orcid": "0009-0001-9320-500X"}],
        "access_right": "open", "license": "cc-by-4.0", "version": VERSION,
        "language": "eng",
        "keywords": ["linear dynamics", "Gamma-supercyclicity", "composition operators",
                     "weighted shifts", "bounded distortion", "Oberwolfach Report 19/2024"],
        "related_identifiers": [
            {"identifier": "10.4171/OWR/2024/19", "relation": "cites", "scheme": "doi"},
            {"identifier": "https://bulmathmc.enu.kz/index.php/main/article/view/55", "relation": "cites", "scheme": "url"},
            {"identifier": "10.1016/j.jmaa.2020.124709", "relation": "cites", "scheme": "doi"},
            {"identifier": "10.1016/j.jfa.2016.03.005", "relation": "cites", "scheme": "doi"},
            {"identifier": "10.1016/j.jmaa.2022.126393", "relation": "cites", "scheme": "doi"},
            {"identifier": "10.1007/s43037-025-00463-0", "relation": "cites", "scheme": "doi"}
        ],
        "notes": f"Research-note website: {SITE} Source and attribution audit: {REPO}"
    }
    zenodo = ROOT / "zenodo"
    zenodo.mkdir(exist_ok=True)
    write_json(zenodo / "metadata.json", metadata)
    write_json(zenodo / "metadata-for-api.json", {"metadata": metadata})
    write_json(ROOT / ".zenodo.json", metadata)
    (zenodo / "COPYPASTE.md").write_text(
        f"# Zenodo fields\n\nResource type: Publication / Preprint\n\nTitle: {TITLE}\n\n"
        f"Creator: Alec Kriebel\n\nFamily name: Kriebel\n\nGiven name: Alec\n\n"
        "ORCID: 0009-0001-9320-500X\n\nAffiliation: Independent researcher\n\n"
        f"Publication date: {DATE}\n\nVersion: {VERSION}\n\nLanguage: English\n\n"
        "License: Creative Commons Attribution 4.0 International (CC BY 4.0)\n\n"
        "Access: Open\n\nExisting DOI: No (none has been assigned to this note)\n\n"
        "Keywords: " + "; ".join(metadata["keywords"]) + "\n\n## Description\n\n"
        + DESCRIPTION + "\n\n## Related works\n\nAdd the six identifiers in metadata.json "
        "with relation **Cites**. These belong to the earlier works, not to this note.\n\n"
        f"Website: {SITE}\n\nRepository: {REPO}\n"
    )
    kit = OUTPUT / "zenodo-upload"
    kit.mkdir(exist_ok=True)
    shutil.copy2(pdf, kit / "paper.pdf")
    shutil.copy2(source, kit / "note-source.zip")
    for filename in ("metadata.json", "metadata-for-api.json", "COPYPASTE.md", "UPLOAD.md"):
        shutil.copy2(zenodo / filename, kit / filename)
    for filename in ("LICENSES.md", "CITATION.bib"):
        shutil.copy2(ROOT / filename, kit / filename)
    checksums(kit, ["paper.pdf", "note-source.zip"])
    kit_files = ["paper.pdf", "note-source.zip", "metadata.json", "metadata-for-api.json",
                 "COPYPASTE.md", "UPLOAD.md", "LICENSES.md", "CITATION.bib", "SHA256SUMS.txt"]
    make_zip(OUTPUT / "zenodo-upload-kit.zip", {file: kit / file for file in kit_files})
    site = OUTPUT / "site"
    site.mkdir(exist_ok=True)
    for filename in ("index.html", "style.css"):
        shutil.copy2(ROOT / "site" / filename, site / filename)
    shutil.copy2(pdf, site / "paper.pdf")
    shutil.copy2(source, site / "note-source.zip")
    shutil.copy2(OUTPUT / "zenodo-upload-kit.zip", site / "zenodo-upload-kit.zip")
    site_files = ["index.html", "style.css", "paper.pdf", "note-source.zip", "zenodo-upload-kit.zip"]
    checksums(site, site_files, "checksums.txt")
    if args.deploy_site:
        destination = ROOT.parent / "docs/papers/gamma-supercyclicity"
        destination.mkdir(parents=True, exist_ok=True)
        for filename in site_files + ["checksums.txt"]:
            shutil.copy2(site / filename, destination / filename)
    print("Created and verified note-source.zip, zenodo-upload-kit.zip, and Pages files.")
    print("No DOI, deposition, GitHub release, or external upload was created.")


if __name__ == "__main__":
    main()
