# Audit deliverables

Verdict: **PASS for the partial research packet; original problem UNSOLVED.** Any full-resolution promotion remains **HOLD**.

- `AUDIT_REPORT.md`: full mathematical and source audit.
- `independent_checks.py`: portable standard-library exact controls, separate from the release verifier.
- `independent_results.json`: recorded independent results.
- `replay/`: unchanged verifier copy and byte-identical replay output, executed away from the frozen release.
- `AUDIT_STATUS.json`: machine-readable verdict and scope.

Run `python3 independent_checks.py --output independent_results.json`.

No frozen file was changed, no remote write was performed, and no source PDF or full source text is redistributed.

## Public portability adaptation

The mathematical checker is unchanged. Its optional integrity hook now reads the
adjacent public RELEASE_MANIFEST.json and frozen files, instead of an external
local manifest. The recorded original result retains its historical integrity
keys; new runs report public_release_manifest_verified. The public verification
wrapper compares every mathematical result and independently checks all hashes.
