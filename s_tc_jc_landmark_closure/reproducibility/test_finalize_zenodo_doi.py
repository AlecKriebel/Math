#!/usr/bin/env python3
"""Fail-closed regression for escaped and unescaped Zenodo placeholders."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import tempfile

from finalize_zenodo_doi import TEXT_FILES, TEX_TOKEN, TOKEN, finalize


PROJECT = Path(__file__).resolve().parents[1]


def main() -> None:
    # Construct a test-only syntactically valid DOI without placing a
    # DOI-looking literal in active publication metadata.
    doi = "10.5281/" + "zenodo." + "987654321"
    with tempfile.TemporaryDirectory(prefix="stc-jc-doi-finalizer-") as raw:
        target = Path(raw) / "project"
        for relative in (*TEXT_FILES, "certificate_bundle/CITATION.cff"):
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / relative, destination)

        release_metadata = target / "RELEASE_METADATA.json"
        shutil.copy2(PROJECT / "RELEASE_METADATA.json", release_metadata)
        metadata = json.loads(release_metadata.read_text(encoding="utf-8"))
        metadata["persistent_identifier"] = None
        release_metadata.write_text(
            json.dumps(metadata, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        # Make the fixture independent of whether the active checkout is
        # pre-DOI or already finalized.  A finalized checkout is normalized
        # back to the exact pending form in the temporary directory only.
        for relative in TEXT_FILES:
            path = target / relative
            text = path.read_text(encoding="utf-8")
            replacement = TEX_TOKEN if path.suffix == ".tex" else TOKEN
            text = re.sub(r"10\.5281/zenodo\.\d+", replacement, text)
            path.write_text(text, encoding="utf-8")

        bib = target / "source/paper/references.bib"
        bib_text = bib.read_text(encoding="utf-8")
        if "Zenodo DOI pending; version 1.1.7" not in bib_text:
            bib_text, count = re.subn(
                r"\n\s*doi\s*=\s*\{" + re.escape(TOKEN) +
                r"\},\n\s*url\s*=\s*\{https://doi\.org/" +
                re.escape(TOKEN) +
                r"\},\n\s*note\s*=\s*\{Version 1\.1\.7"
                r"(?:; \\url\{https://doi\.org/" + re.escape(TOKEN) +
                r"\})?\}",
                "\n  note         = {Zenodo DOI pending; version 1.1.7}",
                bib_text,
                count=1,
            )
            assert count == 1
            bib.write_text(bib_text, encoding="utf-8")

        cff = target / "certificate_bundle/CITATION.cff"
        cff_text = re.sub(
            r'^doi:\s*"[^"]+"\s*$', "", cff.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        ).rstrip() + "\n"
        cff.write_text(cff_text, encoding="utf-8")
        envelope = target / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"
        envelope.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json",
            envelope,
        )

        result = finalize(target, doi)
        assert result["doi"] == doi
        for relative in TEXT_FILES:
            text = (target / relative).read_text(encoding="utf-8")
            assert TOKEN not in text and TEX_TOKEN not in text
        assert f'doi: "{doi}"' in (
            target / "certificate_bundle/CITATION.cff"
        ).read_text(encoding="utf-8")
        assert json.loads(envelope.read_text(encoding="utf-8"))["zenodo_doi"] == doi
        assert json.loads(release_metadata.read_text(encoding="utf-8"))[
            "persistent_identifier"
        ] == doi
    print(json.dumps({
        "status": "VERIFIED",
        "escaped_placeholder": True,
        "pre_or_post_finalization_fixture": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
