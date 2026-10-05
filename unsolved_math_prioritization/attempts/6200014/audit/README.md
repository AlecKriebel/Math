# Independent audit packet: 6200014 / AMR-061-0014

Verdict: accept as a full positive consequence of published results. Read AUDIT_REPORT.md. The frozen author archive is unchanged. A minor bibliographic clarification is kept separately.

## Portable replay

Python 3.9 or newer; standard library only. Run from any working directory:

    python3 /path/to/audit/verify.py
    python3 -O /path/to/audit/verify.py

These commands verify this package's exact file set and manifest, rerun its independent finite controls, and validate the shape and success of the recorded author replay. They do not reprove the mathematical source theorems.

To independently rerun all author-archive tests, supply the separately available, authenticated frozen archive:

    python3 /path/to/audit/code/audit_checks.py --author-archive /path/to/kleinian_boundary_6200014_author_frozen.zip
    python3 -O /path/to/audit/code/audit_checks.py --author-archive /path/to/kleinian_boundary_6200014_author_frozen.zip

The runner authenticates the archive before extraction or code execution. Compare its JSON output with results/author_replay.json. To check corpus identity without disclosing corpus contents:

    python3 /path/to/audit/code/check_identity.py PROBLEMS.json RESEARCH_RESULTS.json CATALOG.json

Compare that output with IDENTITY_AUDIT.json. The three source corpora are not included. All paths are supplied by the caller; none are fixed to the auditor's machine. Temporary mutation cases are isolated and automatically removed. Network access is unnecessary.

Integrity requires an independently obtained archive hash. A self-consistent manifest is not proof of provenance. This audit is AI-assisted and unrefereed; it does not claim novelty, human peer review, or formal certification.
