#!/usr/bin/env python3
"""Fail-closed regression for escaped and unescaped Zenodo placeholders."""

from __future__ import annotations

import json
from pathlib import Path
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
    print(json.dumps({"status": "VERIFIED", "escaped_placeholder": True}, sort_keys=True))


if __name__ == "__main__":
    main()
