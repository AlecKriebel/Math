#!/usr/bin/env python3
"""Verify the publication manifest and the preserved author and audit freezes."""
import hashlib
import json
from pathlib import Path


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def verify(root, manifest):
    data = json.loads((root / manifest).read_text())
    for item in data["files"]:
        relative = Path(item["path"])
        check(not relative.is_absolute() and ".." not in relative.parts, "unsafe manifest path")
        content = (root / relative).read_bytes()
        check(len(content) == item["bytes"], "size mismatch: " + item["path"])
        check(hashlib.sha256(content).hexdigest() == item["sha256"],
              "hash mismatch: " + item["path"])
    return len(data["files"])


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    publication = verify(root, "PUBLICATION_MANIFEST.json")
    author = verify(root / "public", "FROZEN_AUTHOR_MANIFEST.json")
    audit = verify(root / "independent-audit", "AUDIT_MANIFEST.json")
    check(author == 6 and audit == 4, "unexpected frozen packet counts")
    print(json.dumps({"result": "PASS", "publication_files": publication,
                      "frozen_author_files": author, "frozen_audit_files": audit,
                      "universal_gap_verified": False}, indent=2, sort_keys=True))
