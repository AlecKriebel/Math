# Verification evidence

Revision in progress: the retained receipt below belongs to the preceding release. New targeted endpoints require a fresh complete run before export.

Recorded result: **passed** on 2026-09-17 (UTC), run `20260917T034140936866Z`. The standalone check completed 68 commands in 18.0 minutes, including all 1,852 expected declaration reports and five acceptance/twenty rejection controls. All reported axioms are among `propext`, `Classical.choice`, and `Quot.sound`.

The retained [run receipt](recorded/run.json) records a complete clean build, all declaration axiom reports, interface controls, and input fingerprints. Its numbered command logs are in [recorded/](recorded/). A successful receipt has `status: "passed"` and `kernel_checked: true`.

The recorded run was performed in a separate, standalone copy of this package using the bundled manuscript and `python3 scripts/check.py`. The pinned dependency checkouts and cache were supplied locally, then checked at their locked revisions. The companion itself was built from a clean build directory. No parent repository or manuscript path was needed.

Reproduce it from the package root:

```sh
python3 scripts/check.py --bootstrap
```

The first run needs network access and several gigabytes for dependencies. A full verification can take tens of minutes; the declaration-wide axiom audit is a substantial part of that time.

New runs write `verification/runs/<run-id>/run.json` and `verification/latest_run.json`; they do not overwrite the retained evidence. The receipt contains compiler identity, dependency checks, all protected source hashes, every command's exit status and log hash, and transitive axiom dependencies. Relative paths make this evidence portable.

[Statement review](STATEMENT_REVIEW.md) describes the separate manuscript correspondence assessment. [Source preservation](source_preservation.json) compares this revision with the previously verified proof sources, distinguishing unchanged modules, new proofs and interface changes. Neither document substitutes for running Lean.

## Exporting a verified copy

```sh
python3 scripts/package.py --output ../cyclic-bell-lean-review-r2.zip
```

After extracting the ZIP, file integrity can be checked from its `lean_formalization` directory with `shasum -a 256 -c SHA256SUMS` on macOS or `sha256sum -c SHA256SUMS` on Linux.

The exporter checks the retained receipt against the current sources, includes only reviewer-facing material and its evidence, and creates a deterministic ZIP with an internal `SHA256SUMS` file and an external `.sha256` checksum. It refuses stale or incomplete evidence. Checksums detect changes; they do not provide an independent mathematical review or authenticate an author.
