#!/usr/bin/env python3
"""Check the immutable candidate-package hashes and scope metadata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "CANDIDATE_MANIFEST.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["classification"] != "REFUTED_CANDIDATE_WITH_FIXED_EXACT_CONTROL":
        raise AssertionError("wrong package classification")
    for relative, expected in manifest["artifacts_sha256"].items():
        actual = sha256(HERE / relative)
        if actual != expected:
            raise AssertionError(
                f"{relative}: expected {expected}, obtained {actual}"
            )
    if manifest["fixed_graph"]["labeled_graph6_sha256"] != (
        "99ddf436936152440c778efb79270a89e10feb8dd95d7033052e571a1bc3142c"
    ):
        raise AssertionError("wrong fixed-graph digest")
    if "No counterexample to the gamma-theta conjecture." not in (
        manifest["scope"]["not_claimed"]
    ):
        raise AssertionError("missing conjecture-scope disclaimer")
    print("QQ1 anchor-auxiliary candidate manifest: VERIFIED")


if __name__ == "__main__":
    main()
