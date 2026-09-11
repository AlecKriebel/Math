# Preservation recovery — 10 September 2026

**No GitHub branch, commit, or PR was created by the connected plugin.**
The attempted branch `lean/bell-settings-checkpoint-20260910` was rejected with
HTTP 403, `Resource not accessible by integration`. See
`preservation/github_write_attempt.json` for the recorded request and error.

## What is preserved

The original ZIP was extracted and its embedded checksums verified. All **21**
available continuation attachments were then overlaid, including all **14**
attached continuation Lean modules, the rational SOS JSON, both SOS checkers,
and the continuation status, coverage, blueprint, and certificate note.

The recovered project has **24 Lean source files**, excluding the original
generated audit file, and **278 theorem/lemma proof-attempt declarations**.
These counts come from the recovered bytes, not from a Lean parser. The earlier
continuation status reported 25 source files / 280 declarations: that describes
the prior working directory and must not be confused with full recovery here.

All mathematical source modules are preserved byte for byte. `Bell.lean` was
reconstructed as an aggregate import of every available module; its original
v0.1.0 version is retained separately. No missing mathematical proof was invented.
The complete original ZIP is retained in `preservation/`, including the original
README, reports, checksum manifest, and any metadata overwritten by the overlay.

## Recovery limitations

`Bell/Assembly.lean` was described previously but was not attached or recovered.
The same applies to `docs/RANK_TRICHOTOMY_SHORTCUTS.md`,
`scripts/replay_exact.sh`, `scripts/physical_operator_checks.py`,
`reports/continuation_progress.json`, the numerical SOS search directory, and
other continuation-only check scripts/logs. Current-runtime inspection and
file searches did not recover those bytes. This is not a claim that no other
copy exists outside the accessible material.

For files not supplied as later attachments, the initial ZIP's version is used.
Any unexported continuation edits to those files cannot be assumed recovered.
See `reports/recovery_manifest.json` for input provenance and the missing-file
register. All currently available local `Bell.*` imports have corresponding
source files; that is only a filename check, not successful elaboration.

## Verification boundary

**No Lean theorem in this checkpoint is reported as kernel-checked.**
The full universal two-input theorem remains incomplete. No compilation or
mathematical test suite was rerun during this preservation-only operation.
Older reports are preserved as historical evidence for their original stages;
they must not be treated as fresh reports for this recovery.

`FORMALIZATION_STATUS.md`, `docs/COVERAGE.md`, and `docs/BLUEPRINT.md` are the
unchanged continuation notes. They reference some unavailable files and prior
counts. This recovery status and its manifest govern what was actually recovered.

## Resume

Inspect this file and the recovery manifest before running the existing build
wrapper. With the pinned Lean/Mathlib toolchain installed, the next substantive
step remains `bash scripts/check.sh --bootstrap`, followed by compilation repairs
and the missing physical/analytic proof work. A successful subset build would
not close the universal equality theorem. The newly reconstructed aggregate
ensures that available continuation modules are not silently omitted.

The nested `.github/workflows/lean.yml` is preserved from the standalone project;
it is not a repository-root GitHub Actions workflow. No automatic CI execution
or repository-root workflow change is included in the preservation patch.
