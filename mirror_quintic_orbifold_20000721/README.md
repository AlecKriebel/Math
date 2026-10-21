# Mirror-quintic orbifold leading terms (20000721)

Status: UNSOLVED. Five approaches completed; bounded partial progress only.

REPORT.md contains the accepted mathematical analysis. REVIEW.md and INDEPENDENT_AUDIT.md record its acceptance boundaries. Exact period and inverse-series computations reproduce four genus-zero and four genus-one coefficients. Higher-genus coefficients are attributed transcriptions, not independent reconstructions. The analytic claims concern local fixed-genus germs, not the genus sum.

The fixed-genus HKQ ambiguity witness for g >= 4 preserves only the specified incomplete boundary constraints. It is not geometric nonuniqueness or a simultaneous all-genus solution. The September 2026 conifold-gap preprint is reported as a claim, not independently fully proved here or an orbifold closure.

Run with Python 3 and SymPy:

    python -B exact_checks.py
    python -B -O exact_checks.py
    python -B independent_exact_audit.py
    python -B -O independent_exact_audit.py
    python -B residual_checks.py
    python -B -O residual_checks.py
    python -B verify_package.py
    python -B mutation_checks.py
    python -B -O mutation_checks.py

AST_PROVENANCE.json records full-AST-preserving assertion lowering for accepted scripts. Explicit guards run under -O. Replay compares complete stdout and generated JSON/text. Mathematical and inventory negative controls are diagnostics, not new proofs. package_manifest.json inventories every file recursively except itself; its digest is recorded separately in the publication receipt. Hashes establish integrity, not mathematical truth or authenticity.

Only authored analysis and public verification metadata are included. No source PDFs or dataset contents are distributed. Public source inspection history is inherited from the dated recovery and review, not represented as a new retrieval.

AUDIT_HASHES.json records the original accepted artifacts, not the current package inventory. The report and review texts are unchanged; the two runnable scripts have only the assertion-lowering transformation recorded in AST_PROVENANCE.json. Use package_manifest.json for current-byte verification.
