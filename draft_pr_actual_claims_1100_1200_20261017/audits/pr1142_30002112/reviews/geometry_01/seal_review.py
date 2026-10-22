#!/usr/bin/env python3
"""Create a noncircular source/exposure/artifact receipt for this review.

The receipt pins every own artifact except itself. Its digest is printed
to stdout for the parent to record externally, never written into the
receipt or into any artifact that the receipt pins.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    own = Path(__file__).resolve().parent
    audit = own.parents[1]
    inputs = audit / "inputs"
    private = own / "sources" / "private"
    receipt_path = own / "READ_RECEIPT.json"
    proof = pin(inputs / "PROOF.md")
    require(proof["bytes"] == 10412, "proof byte count changed")
    require(proof["sha256"] == "c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658",
            "frozen proof changed")
    core = pin(own / "INDEPENDENT_CORE.md")
    require(core["sha256"] == "6c925b47634c36d8ab3092884456d98a227b2eb9c8907d30ff2327b9a766203d",
            "independent core changed after lock")
    require((private / "CDE_0909.5346.pdf").read_bytes()
            == (private / "CDE_0909.5346v1.pdf").read_bytes(), "CDE version mismatch")
    require((own / "diagnostics_normal.json").read_bytes()
            == (own / "diagnostics_optimized.json").read_bytes(), "normal/-O mismatch")
    source_reads = [
        {"kind": "frozen_input_file", **proof, "scope": "complete PROOF.md",
         "first_read_order": 1,
         "exposure": "Includes old internal acceptance sentence; explicitly not evidence."},
        {"kind": "frozen_input_file", **pin(inputs / "SOURCE_DEPENDENCIES.json"),
         "scope": "complete dependency JSON", "first_read_order": 2,
         "exposure": "Includes old inspection declarations; explicitly not independently adopted."},
        {"kind": "workflow_skill", **pin(Path("/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md")),
         "scope": "complete PDF skill", "first_read_order": 4},
        {"kind": "primary_network_pdf", **pin(private / "CDE_0909.5346.pdf"),
         "urls": ["https://arxiv.org/pdf/0909.5346", "https://arxiv.org/pdf/0909.5346v1"],
         "version": "arXiv:0909.5346v1, 2009-09-29; both URLs byte-identical",
         "scope": "connected/closed/indexing convention p1; Theorem1.4 p6; complete Section5 pp14-15; locator context noted separately",
         "first_read_order": 5},
        {"kind": "primary_network_pdf", **pin(private / "DLS_John_Nash_nonlinear_iteration.pdf"),
         "url": "https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf",
         "version": "undated author-hosted 31-page PDF; metadata 2016-05-11, not treated as publication/version date",
         "scope": "Definition1.1 and Theorem1.2 with pp2-4 context; visible web extraction extends into Euler introduction through web line295",
         "first_read_order": 3},
        {"kind": "primary_network_metadata", **pin(private / "CDE_abs.html"),
         "url": "https://arxiv.org/abs/0909.5346", "web_tool_reference": "turn833view0",
         "scope": "visible web extraction lines0-161, used only title/authors/version history and bibliography",
         "archive_limit": "raw HTML retained afterward; not asserted byte-identical to web tool's text extraction",
         "first_read_order": 3}
    ]
    derived_reads = [
        {**pin(private / "CDE_0909.5346.txt"),
         "method": "pdftotext -layout, Poppler26.08.0",
         "scope": "lines1-120,215-256,648-700 and full-file rg locator query output; not whole paper semantic inspection"},
        {**pin(private / "DLS_John_Nash_nonlinear_iteration.txt"),
         "method": "pdftotext -layout, Poppler26.08.0",
         "scope": "lines1-220; theorem and immediate context, not whole paper semantic inspection"}
    ]
    for name, scope in [("CDE_p06", "CDE printed/PDF page6: full rendered page"),
                        ("CDE_p14", "CDE printed/PDF page14: full rendered page"),
                        ("CDE_p15", "CDE printed/PDF page15: full rendered page"),
                        ("DLS_p04", "DLS printed/PDF page4: full rendered page")]:
        derived_reads.append({**pin(own / "tmp" / (name + ".png")),
                              "scope": scope, "method": "pdftoppm PNG, scale-to1800; view_image"})
    unread = ["AUDIT.md", "ACCEPTANCE.md", "README.md", "STATUS.md", "STATUS.json",
              "VERIFICATION_SUMMARY.md", "MANIFEST.json", "SOURCE_METADATA.json"]
    receipt = {
        "schema": "independent-geometry-review-receipt-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "target": {"pr": 1142, "problem_id": 30002112, "owr": "OWR-12005-004",
                   "assigned_head": "c29139d2c2a98f1a0284d0dc794c88f51c680a0c",
                   "head_limit": "Provided by parent; not independently queried against GitHub or checkout."},
        "exposure": {
            "route_disclosed_by_parent": True,
            "independent_core_recorded_utc": "2026-10-17 23:15:30 UTC",
            "independent_core_pin": core,
            "old_acceptance_statement_in_base_proof_visible": True,
            "old_acceptance_relied_on": False,
            "old_audit_status_contents_read": False,
            "root_or_concurrent_report_contents_read": False,
            "inventory_only_unread_input_paths": [str(inputs / name) for name in unread],
            "contact": "Only parent coordination; no other shards, subagents, or external individuals."
        },
        "nonself_semantic_reads": source_reads,
        "derived_primary_semantic_reads": derived_reads,
        "nonfile_context_reads": [
            "User-supplied AGENTS instructions and environment, parent assignment/route/claim/head; no separate AGENTS.md file opened.",
            "Read-only directory inventory exposed input filenames, not prior audit contents.",
            "pdfinfo metadata for both primary PDFs (page counts, creation dates, producer, byte counts).",
            "Python3.14.6 and Poppler26.08.0 version outputs; no third-party Python module used.",
            "Read-only git check-ignore confirmed source/private PDF and tmp PNG are ignored; no Git mutation.",
            "Own generated core, report, logs, scripts, diagnostic outputs, and hash/byte metadata were checked."
        ],
        "source_limitations": [
            "Only explicitly recorded CDE and DLS portions inspected; not comprehensive source-proof audits.",
            "Original Colbois-Dodziuk, Buser-Burger-Dodziuk, Nash, Kuiper, Hirsch texts not separately retrieved/reproved.",
            "Generalized smooth Jordan-Brouwer separation used as named established theorem.",
            "No OWR/CEG original scope materials opened in this geometry shard; parent scope gate is not independently certified here."
        ],
        "own_artifact_pins": [pin(p) for p in sorted(own.rglob("*"))
                              if p.is_file() and p != receipt_path],
        "sealing_rule": "This receipt intentionally excludes its own hash. Its SHA256 is supplied externally to parent; no pinned artifact contains that digest."
    }
    receipt_path.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"receipt": str(receipt_path), **pin(receipt_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
