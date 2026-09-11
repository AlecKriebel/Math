# Recovered Lean formalization checkpoint

**Partial, uncompiled research source. Not a completed or kernel-verified proof.**

Start with [RECOVERY_STATUS.md](RECOVERY_STATUS.md). It distinguishes the recovered
files from the larger working directory described in the previous continuation.
The requested GitHub write failed with HTTP 403; this directory is a local
preservation checkpoint, not evidence of a remote branch or pull request.

This directory is intended for
`AlecKriebel/Math/qubit_povm_pvm_minimum_settings/lean/`.
It combines the validated initial archive with all available later attachments.
All mathematical source modules are unchanged. The aggregate `Bell.lean` import
list is reconstructed, the earlier checkpoint is kept in `preservation/`, and
`SHA256SUMS.txt` authenticates the recovered package's bytes.

## Entry points

- `Bell/`: all recovered Lean source modules.
- `certificates/binary_pair_sos.json`: exact rational SOS certificate data.
- `docs/SOS_CERTIFICATE.md`: operator-certificate explanation and scope.
- `FORMALIZATION_STATUS.md`, `docs/COVERAGE.md`, `docs/BLUEPRINT.md`: unchanged
  continuation notes; consult recovery status for unavailable referenced files.
- `reports/recovery_manifest.json`: file-level provenance, counts, and gaps.
- `preservation/original_v0.1.0_checkpoint.zip`: complete original archive.
- `scripts/`: all available original check/build/audit scripts and both later
  standard-library SOS checkers.

No full-paper completion is claimed. The universal two-input equality and
several physical/analytic bridges remain missing. Preserved historical reports
are not a fresh validation of this recovered directory.

## Integrity

From this directory, run `sha256sum -c SHA256SUMS.txt` on systems providing
`sha256sum`, or use the outer package's `verify_preservation.py`.
The outer package also supplies a single-commit Git patch and a publishing helper.
Neither has been pushed remotely by the assistant.

The original standalone README, including its older scope and commands, is
retained as `preservation/README.v0.1.0.md`.
