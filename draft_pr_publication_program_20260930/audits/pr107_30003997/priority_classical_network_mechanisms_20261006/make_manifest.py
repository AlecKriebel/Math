#!/usr/bin/env python3
"""Seal public audit outputs and record excluded private-source hashes."""
from hashlib import sha256
import json
from pathlib import Path

p = Path(__file__).resolve().parent
public, private = [], []
for f in sorted(p.rglob("*")):
    if not f.is_file() or f.name == "MANIFEST.json" or "__pycache__" in f.parts:
        continue
    data = f.read_bytes()
    item = dict(path=str(f.relative_to(p)), bytes=len(data), sha256=sha256(data).hexdigest())
    (private if "private_sources" in f.relative_to(p).parts else public).append(item)
out = dict(manifest_format=1, public_outputs=public,
           excluded_private_source_receipts=private,
           private_content_publication_allowed=False,
           note="Manifest excludes itself. Third-party PDFs/text/images/raw receipts are excluded private inputs; listed only by path, size, and hash.")
(p / "MANIFEST.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(dict(public_count=len(public), private_count=len(private), private_sources_excluded=True)))
