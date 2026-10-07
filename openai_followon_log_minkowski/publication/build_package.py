#!/usr/bin/env python3
"""Build an explicitly allowlisted, deterministic owned source/audit archive.

No Git, network, credentials or publication operation is performed. --final is
an assertion by the lead after substantive review, not a machine proof check.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
from typing import Any
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIME = (2026, 10, 6, 0, 0, 0)
BASE_FILES = (
    "main.tex",
    "README.md",
    "references.bib",
    "CURRENT_THEOREMS.md",
    "DEPENDENCY_LEDGER.md",
    "APPROACH_TABLE.md",
    "RESEARCH_LOG.md",
    "zenodo-deposit.json",
    "publication/README.md",
    "publication/build_package.py",
    "research/ROOT_VALIDATION.md",
    "verification/REPRODUCIBILITY.md",
    "verification/reproduce.py",
    "verification/PDF_QA.json",
    "verification/COMPUTATION_RESULTS.json",
    "verification/REPRODUCTION_RESULTS.json",
    "sources/UPSTREAM_INVENTORY.json",
    "agent_notes/upstream_proof_audit.md",
    "agent_notes/moment_dependencies.md",
    "agent_notes/smooth_transfer.md",
    "agent_notes/mixed_strictness.md",
    "agent_notes/priority_audit.md",
    "agent_notes/upstream_audit_tensor_certificate.py",
    "agent_notes/moment_dependencies_tensor_check.py",
    # Metadata-only inventories, not the downloaded third-party sources.
    "agent_notes/moment_dependencies_sources/download_manifest.json",
    "verification/lean_pinned/source_hashes.json",
    "verification/lean_pinned/dependency_pin_comparison.json",
    "verification/lean_pinned/lexical_audit.json",
)
FORBIDDEN = (".secrets", ".zenodo-state", ".lake", "node_modules",
             "__pycache__", ".git", "snapshots", "pdf_render", "clean_build")


def digests(data: bytes) -> dict[str, Any]:
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "md5": hashlib.md5(data).hexdigest()}


def safe_owned_path(relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or any(part in FORBIDDEN for part in p.parts):
        raise RuntimeError(f"Excluded or unsafe payload path: {relative}")
    full = ROOT / p
    if not full.is_file() or full.is_symlink():
        raise RuntimeError(f"Missing owned regular file: {relative}")
    if not full.resolve().is_relative_to(ROOT):
        raise RuntimeError(f"Path leaves project: {relative}")
    return full


def public_lean_excerpt() -> tuple[bytes, dict[str, Any]]:
    original = safe_owned_path("agent_notes/lean_verification.md").read_bytes()
    text = original.decode("utf-8")
    start = text.index("## Process interruption incident\n")
    end = text.index("## Strongest supported result and gap\n", start)
    retained = text[:start] + text[end:]
    provenance = ("# Public formal-scope audit excerpt\n\n"
                  "Original report: `agent_notes/lean_verification.md`.\n\n"
                  f"Original SHA-256: `{hashlib.sha256(original).hexdigest()}`.\n\n"
                  "This public excerpt removes only the unrelated operational incident "
                  "section. No mathematical statement or formal-check limitation has "
                  "been removed. The original report remains in the local research "
                  "record. The unchanged substantive audit follows.\n\n---\n\n")
    return (provenance + retained).encode("utf-8"), {
        "path": "agent_notes/lean_verification.md", **digests(original),
        "transformation": "omit only the Process interruption incident section",
        "archive_path": "verification/LEAN_SCOPE_AUDIT.md"}


def validate_inputs(review_paths: list[str], final: bool) -> None:
    if len(set(review_paths)) != len(review_paths):
        raise RuntimeError("Review paths must be distinct")
    for review in review_paths:
        path = Path(review)
        if not path.parts or path.parts[0] != "reviews" or path.suffix not in {".md", ".json"}:
            raise RuntimeError("Reviews/responses must be explicitly named .md/.json files in reviews/")
        safe_owned_path(review)
    if final and len(review_paths) < 2:
        raise RuntimeError("A final package requires at least two distinct complete-package review records")
    qa = json.loads(safe_owned_path("verification/PDF_QA.json").read_text())
    pdf = safe_owned_path("paper.pdf").read_bytes()
    tex = safe_owned_path("main.tex").read_bytes()
    if not pdf.startswith(b"%PDF-"):
        raise RuntimeError("paper.pdf is not an exported PDF")
    if qa["paper_sha256"] != digests(pdf)["sha256"] or qa["tex_sha256"] != digests(tex)["sha256"]:
        raise RuntimeError("PDF QA does not identify the latest exact manuscript and exported PDF")
    required = (qa.get("native_editor_compilation") == "success",
                qa.get("all_fonts_embedded") is True,
                qa.get("unresolved_references") is False,
                qa.get("overfull_boxes") is False,
                qa.get("engine_warnings") is False)
    if not all(required):
        raise RuntimeError("PDF QA reports an incomplete or unresolved check")


def make_zip(payload: dict[str, bytes], final: bool,
             review_paths: list[str], derived: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    contents = {
        "format": "owned-source-and-verification-v1",
        "status": "final-reviewed-package" if final else "candidate-for-complete-review",
        "upstream_pin": "adc7f1241b42e322a6451854ab7e4b4c146bf78a",
        "zip_entry_timestamp": list(ZIP_TIME),
        "review_paths": review_paths,
        "derived_audit": derived,
        "files": [{"path": name, **digests(data)} for name, data in sorted(payload.items())],
        "limitations": ["finite checks do not replace universal mathematical proofs",
                        "upstream Lean kernel rebuild and axiom extraction incomplete",
                        "no formalization of the follow-on theorem",
                        "automated reviews are not human peer review"],
    }
    payload = dict(payload)
    payload["PACKAGE_CONTENTS.json"] = (json.dumps(contents, indent=2, ensure_ascii=False) + "\n").encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payload.items()):
            entry = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    raw = output.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("ZIP CRC check failed")
    return raw, contents


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", action="append", default=[],
                        help="explicit reviews/ relative file; repeat for each review/response")
    parser.add_argument("--final", action="store_true",
                        help="lead assertion: mathematical and latest complete-package reviews passed")
    parser.add_argument("--check", action="store_true", help="compare without writing or replacing files")
    args = parser.parse_args()
    reviews = sorted(args.review)
    validate_inputs(reviews, args.final)
    payload = {name: safe_owned_path(name).read_bytes() for name in BASE_FILES}
    for name in reviews:
        payload[name] = safe_owned_path(name).read_bytes()
    excerpt, derived = public_lean_excerpt()
    payload["verification/LEAN_SCOPE_AUDIT.md"] = excerpt
    archive, contents = make_zip(payload, args.final, reviews, derived)
    uploads = {
        "paper.pdf": safe_owned_path("paper.pdf").read_bytes(),
        "source-and-verification.zip": archive,
        "README.md": safe_owned_path("publication/README.md").read_bytes(),
    }
    manifest = json.loads(safe_owned_path("zenodo-deposit.json").read_text())
    actual = [(item["path"], item.get("name", Path(item["path"]).name)) for item in manifest["files"]]
    expected = [(f"publication/upload-kit/{name}", name) for name in uploads]
    if actual != expected:
        raise RuntimeError("Deposit manifest and builder upload filenames/order differ")
    kit = ROOT / "publication/upload-kit"
    for name, data in uploads.items():
        target = kit / name
        if args.check:
            if not target.is_file() or target.read_bytes() != data:
                raise RuntimeError(f"Upload kit differs from latest exact payload: {name}")
        else:
            kit.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    public_audit = ROOT / "verification/LEAN_SCOPE_AUDIT.md"
    if not args.check:
        public_audit.write_bytes(excerpt)
    receipt = {
        "status": "final-reviewed-package" if args.final else "candidate-for-complete-review",
        "publication_ready_asserted_by_lead": args.final,
        "build_command": ["python3", "publication/build_package.py"]
                         + (["--final"] if args.final else [])
                         + [part for name in reviews for part in ["--review", name]],
        "python": sys.version,
        "platform": platform.platform(),
        "zlib_compile_version": zlib.ZLIB_VERSION,
        "zlib_runtime_version": zlib.ZLIB_RUNTIME_VERSION,
        "zip_entry_timestamp": list(ZIP_TIME),
        "zip_compression": "DEFLATE level 9",
        "zip_entry_permissions": "regular file 0644",
        "files": [{"path": f"publication/upload-kit/{name}", "name": name, **digests(data)}
                  for name, data in uploads.items()],
        "payload_files": contents["files"],
        "review_files": [{"path": name, **digests(payload[name])} for name in reviews],
        "deposit_manifest_sha256": digests(safe_owned_path("zenodo-deposit.json").read_bytes())["sha256"],
        "derived_audit": derived,
        "excluded": "third-party source copies; Lean dependencies/configuration/build logs; caches; secrets; previews; unrelated process incident",
        "note": "No publication, Git action or formal certification is performed by this builder.",
    }
    if not args.check:
        (ROOT / "publication/package-inventory.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "matches" if args.check else receipt["status"],
                      "uploads": receipt["files"],
                      "payload_entries": len(contents["files"]) + 1,
                      "review_files": reviews}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
