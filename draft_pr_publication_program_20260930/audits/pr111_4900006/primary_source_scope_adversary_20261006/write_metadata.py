"""Record the completed, corrected primary-scope audit; no Git/service actions."""
from pathlib import Path
import datetime
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ORIGINAL = AUDIT / "original_head_authentication_20261006"


def pin(path):
    body = path.read_bytes()
    return {"path": str(path.relative_to(AUDIT)), "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}


def write(path, content):
    path.write_text(json.dumps(content, indent=2) + "\n")


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
source_specs = [
    ("eden1989", "https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf", "Local Lyapunov exponents and a local estimate of Hausdorff dimension", "Alp Eden", "1989", 10),
    ("parker_goluskin_v2", "https://arxiv.org/pdf/2510.14870v2", "Computation of attractor dimension and maximal sums of Lyapunov exponents using polynomial optimization", "Jeremy P. Parker; David Goluskin", "2026-01-21; version 2", 46),
    ("kuznetsov_mokaev2018", "https://arxiv.org/pdf/1807.00235", "A note on finite-time Lyapunov dimension of the Rossler attractor", "N. V. Kuznetsov; T. N. Mokaev", "arXiv v1 submitted 2018-06-30; PDF dated 2018-07-03", 3),
]
private = HERE / "private_primary_sources"
original_files = sorted(x for x in (ORIGINAL / "original_attempt").rglob("*") if x.is_file())
if len(original_files) != 17:
    raise ValueError("unexpected original bundle membership")
write(HERE / "SOURCE_MANIFEST.json", {
    "schema": "pr111-primary-source-scope-manifest/v1",
    "recorded_at_utc": now,
    "actual_pid": os.getpid(),
    "primary_sources": [{"url": url, "title": title, "authors": authors, "date": date, "pdf_pages_including_archive_cover": pages, "pdf_pin": pin(private / (stem + ".pdf")), "extracted_text_pin": pin(private / (stem + ".txt"))} for stem, url, title, authors, date, pages in source_specs],
    "private_copyright_source_artifacts": [pin(x) for x in sorted(private.iterdir()) if x.is_file()],
    "private_source_artifacts_for_public_staging": False,
    "original_statement_pin": pin(ORIGINAL / "SOURCE_STATEMENT.json"),
    "original_prior_report_pin": pin(ORIGINAL / "PRIOR_REPORT.md"),
    "original17_bundle_full_byte_pin_inventory": [pin(x) for x in original_files],
    "semantic_read_scope": "Complete original statement, prior report, candidate, author verifier, inherited review and source/verification receipts; source literature as detailed in REPORT.md. Byte inventory is not a claim of executing every original program.",
    "independent_source_retrieval": "Three actual bounded curl downloads completed with exit 0, each limited to 45 seconds and 12 million bytes. Complete PDFs independently match prior citation hashes; PDF source bodies were never modified.",
    "read_scope": {"eden1989": "Complete article text; decisive formulas and Questions 1 to 3 visually inspected on printed pages 408, 409 and 411.", "parker_goluskin_v2": "Complete PDF obtained; complete introduction and Section 2.1 read; all scope, assumption and conjecture occurrences across the full 46-page text inspected, including Section 3 and bibliography. Printed page 7 visually inspected.", "kuznetsov_mokaev2018": "Complete three-page text read; Section II equation 5 independently rendered at 300dpi confirms a nonnegative partial-sum index. Earlier 125dpi strict-symbol misreading explicitly withdrawn."},
    "original_thesis_full_text_read": False,
    "novel_priority_audit_complete": False,
    "outside_individuals_contacted": False,
})
checks = json.loads((HERE / "INDEPENDENT_SCOPE_CHECKS.json").read_text())
if checks["all_pass"] is not True or checks["checks"] != 11762:
    raise ValueError("controls receipt")
write(HERE / "RESULT.json", {
    "schema": "pr111-primary-source-scope-adversary-result/v1",
    "completed_at_utc": now,
    "actual_pid": os.getpid(),
    "verdict": "PASS_ORIGINAL_COMPLETE_LITERAL_AND_MODERN_UNRESTRICTED_COUNTEREXAMPLE_WITH_HISTORICAL_SCOPE_LIMITS",
    "report_pin": pin(HERE / "REPORT.md"),
    "source_manifest_pin": pin(HERE / "SOURCE_MANIFEST.json"),
    "independent_program_pin": pin(HERE / "independent_scope_checks.py"),
    "independent_receipt_pin": pin(HERE / "INDEPENDENT_SCOPE_CHECKS.json"),
    "candidate_pin": pin(ORIGINAL / "original_attempt" / "COUNTEREXAMPLE.md"),
    "withdrawal_pin": pin(HERE / "WITHDRAWAL.json"),
    "withdrawn_lowresolution_symbol_finding": True,
    "actual_primary_eq5_index": "nonnegative partial sums >=0",
    "reject_root_diagnostic_v1_sha256": "4943f2c38effe24e0aa049242f035091df100c1089612cd2ae4c585abc161ddb",
    "mandatory_corrections_to_original_mathematics": [],
    "mandatory_corrections_to_original_source_definitions": [],
    "scope_supported": ["Literal immutable imported universal statement", "Parker–Goluskin v2 equation 18 fixed-global-index maximizer statement with its stated general C1, forward-invariant, forward-bounded hypotheses"],
    "scope_not_resolved": ["Eden 1989 Question 1 concerning critical-point/global-dimension attainment", "Eden 1989 Lorenz Question 3", "Strange-attractor formulations", "Typical or generic self-excited-attractor formulation", "Exact unread original-thesis quantifiers"],
    "promotion_constraints": ["Preserve the candidate's existing historical, Lorenz, chaos and genericity exclusions in title, abstract and metadata.", "The prior imported report is triage, not history or priority authority; 1994-book provenance remains unverified.", "Do not claim that the finite-time spatial supremum or its time infimum equals 203/50; only the lower bound was checked.", "No novel-priority or publishing claim based on this phase."],
    "phase_completion_percent": 100,
    "novel_priority_audit_complete": False,
    "whole_publication_approval": False,
    "original_inputs_mutated": False,
    "git_or_service_writes": False,
})
print(json.dumps({"actual_pid": os.getpid(), "source_manifest_pin": pin(HERE / "SOURCE_MANIFEST.json"), "result_pin": pin(HERE / "RESULT.json"), "report_pin": pin(HERE / "REPORT.md")}, indent=2))
