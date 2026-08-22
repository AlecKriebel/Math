#!/usr/bin/env python3
"""Insert a real reserved Zenodo DOI into all active submission surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


PROJECT = Path(__file__).resolve().parents[1]
TOKEN = "ZENODO_DOI_PENDING"
TEX_TOKEN = TOKEN.replace("_", r"\_")

TEXT_FILES = (
    "THEOREM_CERTIFICATE_CROSSWALK.md",
    "source/paper/references.bib",
    "source/supplement/supplement.tex",
    "biorxiv_submission/BIORXIV_METADATA.md",
    "journal_submission/systematic_biology/SB_SUBMISSION_METADATA.md",
    "journal_submission/journal_of_mathematical_biology/JMB_SUBMISSION_METADATA.md",
)


def normalize_doi(value: str) -> str:
    doi = value.removeprefix("https://doi.org/").strip()
    if not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
        raise SystemExit("expected a Zenodo DOI of the form 10.5281/zenodo.<digits>")
    return doi


def finalize(project: Path, doi_value: str) -> dict[str, object]:
    project = project.resolve()
    doi = normalize_doi(doi_value)
    changed = []
    for relative in TEXT_FILES:
        path = project / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8")
        updated = original.replace(TOKEN, doi).replace(TEX_TOKEN, doi)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(relative)

    bib = project / "source/paper/references.bib"
    text = bib.read_text(encoding="utf-8")
    marker = "note         = {Zenodo DOI pending; version 1.1.7}"
    if marker in text:
        text = text.replace(
            marker,
            f"doi          = {{{doi}}},\n  url          = {{https://doi.org/{doi}}},\n"
            "  note         = {Version 1.1.7}",
            1,
        )
        bib.write_text(text, encoding="utf-8")
        if "source/paper/references.bib" not in changed:
            changed.append("source/paper/references.bib")
    elif doi not in text:
        raise AssertionError("Zenodo bibliography record is neither pending nor finalized")

    envelope = project / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"
    if not envelope.is_file():
        raise FileNotFoundError(envelope)
    payload = json.loads(envelope.read_text(encoding="utf-8"))
    payload["zenodo_doi"] = doi
    envelope.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8")
    changed.append("release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json")

    cff = project / "certificate_bundle/CITATION.cff"
    if not cff.is_file():
        raise FileNotFoundError(cff)
    cff_text = cff.read_text(encoding="utf-8")
    if "doi:" not in cff_text:
        cff_text = cff_text.rstrip() + f"\ndoi: \"{doi}\"\n"
        cff.write_text(cff_text, encoding="utf-8")
        changed.append("certificate_bundle/CITATION.cff")
    elif f'doi: "{doi}"' not in cff_text:
        raise AssertionError("CITATION.cff contains a different DOI")

    remaining = []
    for relative in TEXT_FILES:
        text = (project / relative).read_text(encoding="utf-8")
        if TOKEN in text or TEX_TOKEN in text:
            remaining.append(relative)
    if remaining:
        raise AssertionError(("unreplaced Zenodo DOI placeholder", remaining))
    return {"doi": doi, "files_changed": sorted(set(changed))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True, help="issued or reserved Zenodo DOI")
    parser.add_argument("--project-root", type=Path, default=PROJECT,
                        help="project root (used by the fail-closed regression test)")
    args = parser.parse_args()
    print(json.dumps(finalize(args.project_root, args.doi), sort_keys=True))


if __name__ == "__main__":
    main()
