#!/usr/bin/env python3
"""Explicit ordinary PDF views and raw identity checks; no scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent


def pin(path):
    body = path.read_bytes()
    return {"path": str(path), "bytes": len(body), "SHA256": hashlib.sha256(body).hexdigest()}


def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def derive():
    shared = A / "primary/shared-raw/primary"
    api_path = shared / "extra/openai-contents.hop0.body"
    api = json.loads(api_path.read_bytes())
    pdf = A / "primary/openai-pinned.pdf"
    decoded = base64.b64decode(api["content"], validate=False)
    require(api["encoding"] == "base64", "literal API encoding")
    require(decoded == pdf.read_bytes(), "whole decoded PDF equality")
    git_blob = hashlib.sha1(b"blob " + str(len(decoded)).encode() + b"\0" + decoded).hexdigest()
    require(git_blob == api["sha"] and len(decoded) == api["size"], "literal API blob and size")
    identity = {"UTC": datetime.now(timezone.utc).isoformat(), "whole_API_body": pin(api_path), "whole_API_key_order": list(api), "literal_Git_blob_SHA1": git_blob, "PDF": pin(pdf), "decoded_whole_byte_equal": True, "own_primary_GETs": 0, "freshness": "Exact pinned raw bodies reused from sole acquisition owner; no fresh network request in scope lane", "whole_original_API_body_retained_not_normalized": True}
    (A / "primary/PRIMARY_IDENTITY_CHECKS.json").write_text(json.dumps(identity, indent=2) + "\n")
    out = A / "primary/rasters"
    out.mkdir(exist_ok=False)
    specs = [("openai", pdf, 2), ("openai-planar", pdf, 14), ("openai-rank", pdf, 18), ("gaboriau-action", A / "primary/gaboriau-2002.pdf", 34), ("gaboriau-comparison", A / "primary/gaboriau-2002.pdf", 36), ("lueck-reduced", shared / "extra-v3/lueck-v1-pdf.hop0.body", 19), ("hatcher-homology", shared / "extra-v2/hatcher-author.hop0.body", 376), ("psv-credit", shared / "extra-v3/psv-v1-pdf.hop0.body", 25)]
    receipts = []
    for label, src, page in specs:
        command = ["pdftoppm", "-r", "105", "-f", str(page), "-l", str(page), "-singlefile", "-png", str(src), str(out / label)]
        start = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, capture_output=True, text=True)
        receipts.append({"source": pin(src), "physical_page": page, "actual_command": command, "UTC_started": start, "UTC_completed": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "output": pin(out / (label + ".png")) if result.returncode == 0 else None})
        require(result.returncode == 0, "ordinary Poppler render")
    (A / "primary/PRIMARY_RASTER_RECEIPTS.json").write_text(json.dumps({"ordinary_Poppler_only": True, "actual_runs": receipts}, indent=2) + "\n")
    print(json.dumps({"decoded_PDF_byte_equal": True, "Git_blob_SHA1_matches": True, "fresh_own_primary_rasters": len(receipts), "own_primary_GETs": 0}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--derive"]:
        raise SystemExit("Inert by default; --derive creates ordinary primary page views only")
    derive()
