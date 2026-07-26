#!/usr/bin/env python3
"""Byte-exact audit of the attachment-notation repair.

The script reconstructs the formerly reviewed bytes entirely in memory by
reversing the four intended textual substitutions and the one inserted
definition.  Matching the former exact size and hash proves that no other byte
changed.  It does not evaluate graph parameters.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "math/working/order13_k5_structural.md"
CURRENT_SIZE = 11274
CURRENT_SHA256 = (
    "34c29d4b14e0955bd1ea0968f138a991cdd2a595ff3dd26891b74c1218af0a11"
)
FORMER_SIZE = 11188
FORMER_SHA256 = (
    "1761c537ce293f1d7e36fd32786ffad0a67f2f7fe9dd4af6aceed346ccec6d37"
)
PRIOR_ARTIFACTS = {
    "reviews/order13_k5_structural_hostile/REVIEW.md": (
        7053,
        "b93e854975444313558327a6ae0cc96ad3e8693b34e87b1148d878df4008759b",
    ),
    "reviews/order13_k5_structural_hostile/evidence.json": (
        4810,
        "2250c3c269e8df2b77dc4b98abcdfe049b1c1d08a77fa1f781c22c06605761ee",
    ),
    "reviews/order13_k5_structural_hostile/RESEARCH_LOG.md": (
        1277,
        "dd1d5a211b6ab4aadf89834496e3ecb423b1dc94548d51043fbf626343df0fd8",
    ),
    "reviews/order13_k5_structural_hostile/audit.py": (
        9295,
        "125ed608ce6d624aeb758ad272b8dae1195290ce9ef5b59150a4023ea3ae283e",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


def reconstruct_former(current: str) -> tuple[str, list[str]]:
    definition = (
        "Define the two attachment masks by\n\n"
        "\\[\n"
        " A=N_G(a)\\cap V(Q),\\qquad B=N_G(b)\\cap V(Q).\n"
        "\\tag{3.1a}\n"
        "\\]\n\n"
    )
    current = require_once(current, definition, "\n")
    changes = [
        ("C_i-A", "C_i-N_Q(a)"),
        ("C_i-B", "C_i-N_Q(b)"),
        (
            "R=Q-(A\\cup B),",
            "R=Q-\\bigl(N_Q(a)\\cup N_Q(b)\\bigr),",
        ),
        (
            "A=N_G(a)\\cap V(Q),\\qquad B=N_G(b)\\cap V(Q).",
            "A=N_Q(a),\\qquad B=N_Q(b).",
        ),
    ]
    for repaired, former in changes:
        current = require_once(current, repaired, former)
    labels = [
        "inserted_formal_attachment_definition",
        "clique_obstruction_uses_A",
        "clique_obstruction_uses_B",
        "R_uses_A_union_B",
        "later_attachment_display_uses_formal_definition",
    ]
    return current, labels


def main() -> None:
    raw = TARGET.read_bytes()
    if (len(raw), sha256(raw)) != (CURRENT_SIZE, CURRENT_SHA256):
        raise RuntimeError("revised structural target bytes changed")
    text = raw.decode("utf-8")
    if "N_Q(a)" in text or "N_Q(b)" in text:
        raise AssertionError("undefined outside-vertex neighborhood survived")
    former, repairs = reconstruct_former(text)
    former_raw = former.encode("utf-8")
    if (len(former_raw), sha256(former_raw)) != (
        FORMER_SIZE,
        FORMER_SHA256,
    ):
        raise AssertionError("reverse repair does not recover reviewed bytes")

    for relative, expected in PRIOR_ARTIFACTS.items():
        raw_artifact = (ROOT / relative).read_bytes()
        if (len(raw_artifact), sha256(raw_artifact)) != expected:
            raise RuntimeError(f"prior hostile artifact changed: {relative}")

    print(
        json.dumps(
            {
                "current_target": {
                    "path": "math/working/order13_k5_structural.md",
                    "sha256": CURRENT_SHA256,
                    "size_bytes": CURRENT_SIZE,
                },
                "former_target_reconstructed": {
                    "sha256": FORMER_SHA256,
                    "size_bytes": FORMER_SIZE,
                },
                "prior_hostile_artifacts_preserved": True,
                "repairs": repairs,
                "schema": "gamma-theta-order13-k5-revised-byte-audit-v1",
                "verdict": "ACCEPT_EXACT_NOTATION_ONLY_REVISION",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
