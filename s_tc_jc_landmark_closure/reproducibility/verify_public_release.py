#!/usr/bin/env python3
"""Compatibility entry point for the DOI-published curated archive.

The active publication target is Zenodo, not the superseded omnibus GitHub
release.  This wrapper delegates to the canonical downloaded-archive checker.
"""

from __future__ import annotations

import runpy


if __name__ == "__main__":
    runpy.run_module(
        "reproducibility.verify_certificate_zenodo_release",
        run_name="__main__",
    )
