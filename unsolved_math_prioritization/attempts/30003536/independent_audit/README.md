# Independent audit of the intermediate Riesz maximum principle packet

Decision: accept all five partial approaches with one explicit regularization clarification. Status remains unsolved, 5/5. Read AUDIT_REPORT.md and ACCEPTANCE.json.

The author packet remains unchanged under its original manifest pin. REPORT.corrected.md is a separate full report, and REGULARIZATION.patch adds only the symmetric inner principal-value cutoff for the infinite plane model. Do not replace the frozen author report while retaining its old manifest.

Python standard library only. From any directory, use the audit pin supplied in the external audit receipt:

    python -I -B verify_audit.py --packet /path/to/author/packet --expected-audit-manifest-sha256 <external-audit-pin>

For independent finite controls alone:

    python -I -B independent_controls.py --packet /path/to/author/packet

The controls replay normal, -O, and -OO subprocesses and prove that temporary read-only fixtures deny actual writes. Run as an ordinary user; a privileged account that bypasses read-only permissions is intentionally rejected by the read-only test. No author packet or audit payload files are written. Temporary fixtures are removed.

The 4,294 new finite checks and replay controls do not prove the analytic estimates. The full audit separately reviews all Fubini, smoothing, support, and limit arguments. This source-free archive contains authored mathematics, controls, and public verification metadata only. It contains no source PDFs, source text extracts, source page images, corpus contents, or private coordination files. No remote changes were made.
