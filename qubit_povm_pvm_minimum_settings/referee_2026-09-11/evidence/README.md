# Reading the referee evidence

`input.json` binds this review to the original production Lean sources and primary TeX files by SHA-256 and records the initial Git commit. `reproduction.json` records the isolated fresh-build outcome and checks that those original files remained unchanged.

`kernel_report.json`, `axiom_audit.json`, `statement_audit.json`, and `latest_run.json` are copied from the independently executed work copy, not from the pre-existing production receipts. The named run's complete files are copied into `run/`. Paths inside those receipts use the original layout relative to `../work/bell_lean`; the corresponding published logs can be found by basename in `run/`. `build.log` is the complete top-level output. The expected rejection in `SmokeInvalid.lean` is a negative control, not a failed mathematical theorem.

`matrix_contract.json` and `matrix_contract.log` record the additional referee-written explicit matrix-model contract and its transitive axioms. This contract is separate from the two production validation files. `strict_domain_counterexample.log` records the Mathlib-only rational counterexample probe; it does not depend on the Bell development.

`supplementary_checks.json` records eight verification-harness or finite-algebra suites. Two initial preparation failures (missing reference PDF / output directory in the minimal work copy) are retained alongside the successful retries. The `check_*.log` files contain the output; `supplementary_reports/` retains their principal machine-readable results. Mock runner/parser tests are explicitly marked as such and are not proof-checking receipts.

`adversarial_provenance.json` records compiler identity and hash, dependency source checks, and path/shadowing checks. The audit reuses the pinned dependency cache and installed compiler; it does not independently rebuild or attest every dependency or linked runtime.

The research log and main referee report interpret these results. Hashes and a successful compiler run alone do not establish manuscript correspondence; the six independent source reviews provide that separate assessment.
