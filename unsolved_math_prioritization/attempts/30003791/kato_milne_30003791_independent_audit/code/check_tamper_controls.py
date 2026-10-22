#!/usr/bin/env python3
"""Negative integrity tests on disposable copies, never on the frozen author tree."""
import json
from pathlib import Path
import shutil
import tempfile

from independent_verify import freeze_check

parent = Path(__file__).resolve().parents[2]
source = parent / "kato_milne_30003791"
archive = parent / "KATO_MILNE_30003791_SAFE_FREEZE.zip"
results = []

def edit_bytes(root):
    path = root / "README.md"
    path.write_bytes(path.read_bytes() + b"\nDeliberate audit mutation.\n")

def extra_file(root):
    (root / "unexpected.txt").write_text("Deliberate audit mutation.\n")

def duplicate_entry(root):
    path = root / "MANIFEST.json"
    data = json.loads(path.read_text())
    data["files"].append(dict(data["files"][0]))
    path.write_text(json.dumps(data))

def add_symlink(root):
    (root / "unexpected-link").symlink_to("README.md")

for label, mutate in [("changed_file_bytes", edit_bytes), ("unexpected_file", extra_file),
                      ("duplicate_manifest_entry", duplicate_entry), ("symlink", add_symlink)]:
    with tempfile.TemporaryDirectory(prefix="kato-tamper-") as directory:
        copied = Path(directory) / "author-copy"
        shutil.copytree(source, copied)
        mutate(copied)
        try:
            freeze_check(copied, archive)
        except ValueError as error:
            results.append({"mutation": label, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("Negative control escaped detection: " + label)

print(json.dumps({"status": "PASS", "author_freeze_modified": False,
                  "negative_integrity_controls": results}, indent=2, sort_keys=True))
