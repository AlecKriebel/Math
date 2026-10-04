# Portable independent audit

Problem 30002497 / OWR-12866-004.

Verdict: the partial mathematics passes; the original endpoint-export claim
requires correction. The target remains unsolved.

- `AUDIT.md`: full adversarial analysis, source locations, numerical rigor, and gap
- `CORRECTIONS.md`: exact defect, remedy, and unaffected claims
- `AUDIT.json`: machine-readable disposition
- `AUDITED_INPUTS.json`: hashes binding the nine safe frozen author files
- `independent_controls.py`, `independent_results.json`: standard-library-only certificates
- `verify_controls_outward.py`: corrected-export variant of the author verifier
- `corrected_controls_2048_40.json`, `corrected_controls_4096_60.json`: corrected endpoints
- `verify_audit.py`, `verification_results.json`: exact binding, nesting, export tests, and rerun
- `replay_results.json`: original frozen-script reproducibility summary
- `SHA256SUMS`: audit-file integrity

No source texts, source PDFs, raw catalogues, or private coordination metadata
are included. No network access is needed to run these controls.

## Reproduce

Python 3 alone suffices for the independent certificates:

    python independent_controls.py --cutoff 256 --output rerun_independent.json

Python 3 with mpmath 1.3.0 is needed for the corrected author variants:

    python verify_controls_outward.py --cutoff 2048 --dps 40 --output rerun_2048.json
    python verify_controls_outward.py --cutoff 4096 --dps 60 --output rerun_4096.json

To recheck the audit and optionally bind a supplied original author directory:

    python verify_audit.py --rerun --output rerun_verification.json
    python verify_audit.py --author ../author --rerun --output rerun_bound_verification.json

Use new output names to keep the supplied evidence unchanged. The audit scripts
perform no remote writes. The independent engine's exact fixed-point output
is an outward enclosure by construction, not a nearest-rounded display.
