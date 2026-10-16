# Hysteretic traffic BV: corrected partial-results audit

Read ACCEPTANCE.md, REPORT.md, and AUDIT_REPORT.md. The five substantive approaches are exhausted; the general switching BV problem is unresolved. This target-only delivery contains authored results, the historical correction patch, safe checks, public source metadata, and verification evidence. It contains no complete superseded report/checker, source document bodies, datasets or QUEUE file.

The corrected report and both mathematical checkers are preserved byte-for-byte. check_calculations.py separates exact rational checks from labeled floating-point square-root illustrations. audit_exact.py supplies independent exact rational support checks. guard_checks.py separately verifies exact flat-scanning output and tests mathematical mutations. Finite checks support, but do not replace, the written analytic arguments.

Authenticate BOOTSTRAP.py against a SHA-256 supplied outside the delivery before executing it. It fixes the full manifest, verifier and controls; the manifest authenticates all remaining files, including acceptance and receipts. Replacing an untrusted packet's own manifest cannot replace the fixed external trust anchor.

Use actual UID=EUID=1000. Set this directory to 0555 and all files to 0444. Run each command in normal, -O and -OO modes:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B BOOTSTRAP.py --controls .

Add -O or -OO before BOOTSTRAP.py for those modes. The scripts require only Python's standard library. Actual create/append attempts must fail with EACCES. Controls modify temporary copies only. Fresh full stdout/stderr must match externally bound references byte-for-byte with recursive exact JSON types and no normalization.

CHECK_RUNS.json identifies fresh reference capture. PREPARATION_CONTROLS and PREPARATION_STAGE describe the earlier pre-seal stage. Final sealing binds those receipts, then final fixed-bootstrap controls run against the entire delivery; their receipts are kept outside the delivery and pinned in the draft PR description to avoid circular self-hashes.

Historical defects, run totals, source inspections and manuscript-status observations are labeled in AUDIT_REPORT.md and HISTORICAL_PROVENANCE.json. Portable historical replay is NOT_RUN. Source bodies, original report/checker, prior portable harness, patch application, dataset replay and formal proof-assistant verification are NOT_RUN. No full-source counterexample, global viscous approximation, complete switching theorem or novelty claim is made.
