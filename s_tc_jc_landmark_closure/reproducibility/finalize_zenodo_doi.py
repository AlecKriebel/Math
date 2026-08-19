#!/usr/bin/env python3
"""Insert a real reserved Zenodo DOI into all active submission surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


PROJECT = Path(__file__).resolve().parents[1]
TOKEN = "ZENODO_DOI_PENDING"

TEXT_FILES = (
    "source/paper/references.bib",
    "source/supplement/supplement.tex",
    "biorxiv_submission/BIORXIV_METADATA.md",
    "journal_submission/systematic_biology/SB_SUBMISSION_METADATA.md",
    "journal_submission/journal_of_mathematical_biology/JMB_SUBMISSION_METADATA.md",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True, help="issued or reserved Zenodo DOI")
    args = parser.parse_args()
    doi = args.doi.removeprefix("https://doi.org/").strip()
    if not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
        raise SystemExit("expected a Zenodo DOI of the form 10.5281/zenodo.<digits>")

    changed = []
    for relative in TEXT_FILES:
        path = PROJECT / relative
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        updated = original.replace(TOKEN, doi)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(relative)

    bib = PROJECT / "source/paper/references.bib"
    text = bib.read_text(encoding="utf-8")
    marker = "note         = {Zenodo DOI pending; version 1.1.5}"
    if marker in text:
        text = text.replace(
            marker,
            f"doi          = {{{doi}}},\n  url          = {{https://doi.org/{doi}}},\n"
            "  note         = {Version 1.1.5}",
            1,
        )
        bib.write_text(text, encoding="utf-8")

    envelope = PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"
    payload = json.loads(envelope.read_text(encoding="utf-8"))
    payload["zenodo_doi"] = doi
    envelope.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8")
    cff = PROJECT / "certificate_bundle/CITATION.cff"
    cff_text = cff.read_text(encoding="utf-8")
    if "doi:" not in cff_text:
        cff_text = cff_text.rstrip() + f"\ndoi: \"{doi}\"\n"
        cff.write_text(cff_text, encoding="utf-8")
    print(json.dumps({"doi": doi, "files_changed": changed}, sort_keys=True))


if __name__ == "__main__":
    main()
