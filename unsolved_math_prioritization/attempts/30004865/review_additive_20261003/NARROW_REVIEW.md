# Narrow additive-package verification

Date: 2026-10-03 UTC  
Problem: 30004865 / OWR-8415352-007  
Supplied checkpoint: `e4c7e0a19508a8b1ec46b7bf6e57060409f67bc5`  
Reviewed local package: `attempt/`  
Package manifest SHA-256: `a6d91a249a4886f70220b00541805fcf271366842033ae4866a3eb1b142d26be`

## Verdict: PASS

The additive scope correction and administrative rebind satisfy section 9 of the independent full review. The reviewer's scope-clarification condition is discharged for the exact package bound above. No mathematical revision or additional author research is required. Publication remains the parent's decision.

This narrow receipt supersedes the package's then-pending narrow-verification labels. Preserve the package as a checkpoint; bind this receipt additively rather than altering the original author or full-review evidence.

## Checks completed

1. The package manifest has the expected SHA-256, and all 54 listed file sizes and hashes match. There are no missing files or unbound files other than the manifest itself, which is separately hash-bound above.
2. `TURN_5_MANIFEST.json` remains `8016d13bc34c45147548324d9b70b2a598340a3ffe50cef0eff446a1f9f0c98b`; all 40 author entries still match. The frozen proofs, scripts and historical records are unchanged.
3. The copied `REVIEW_MANIFEST.json` remains `8c084125ed569a584aec0fdd8b3589758ee3f4512e029416af9495598ffdb2cb`; all nine entries match. The ten copied files, including that manifest, are byte-identical to the reviewer's originals.
4. `PUBLICATION_SCOPE_CLARIFICATION.md` contains the exact agreed paragraph. It correctly states that local transposition is a complex-linear trace-norm isometry and can be absorbed into an allowed tester. It supersedes the earlier “no partial transpose” wording while preserving the original matrix-factor partition and excluding the added nonlocal reshuffling/regrouping family.
5. `README_REVIEWED.md` links to the clarification, full review, audit metadata, both original manifests, current disposition and additive manifest. All seven relative links resolve to the intended local package files.
6. Current descriptions correctly retain: the central independently validated negative answer; full complex individual-factor norms; strict detection above one; actual-SIC existence qualifications; non-full-separability versus genuine multipartite entanglement; prior attribution; no novelty certification; unrestricted remaining questions; exhausted/scoped-partial status; and 5/5 author turns consumed. The eta_p domain is now explicit.
7. Current historical-label handling is correct. The unavailable earlier review is not evidence for the fresh verdict, and frozen chronological state files are not presented as current authority. The current package still defers publication to the parent.
8. The manifest excludes raw source files and private page screenshots. No new theorem, proof change, author research turn, queue edit, PR, remote write or mutation of frozen review files was performed by this narrow verification.

The supplied remote commit identifier records the parent's checkpoint reference. This narrow check verifies its supplied local contents and hashes, not an independent read of the remote branch tip. The unchanged author programs were not rerun again because this pass verified byte identity with the already tested files.

## Nonblocking reproduction-layout note

The five standard-library author scripts can be run directly in the published attempt directory. The frozen independent audit checker additionally verifies source hashes and expects the original audit layout. Its archived copy under `attempt/review_independent_20261003/` is preserved evidence, not a location-independent executable.

To replay that checker without editing it, stage these sibling directories under one root:

- `attempt/`: the reviewed author/package files
- `review_independent_20261003/`: copies of the ten frozen review files from the package
- `sources/`: the nine authorized source files, obtained from the source-manifest URLs and checked against their recorded hashes

Run `python review_independent_20261003/independent_checks.py` with NumPy and SymPy available. Its own path calculation then finds the expected author and source directories. The original audit used Python 3.12.14, NumPy 2.3.5 and SymPy 1.14.0. Sources remain excluded from the public result package; neither this layout note nor the script establishes permission to republish them.

This replay-layout requirement does not affect the mathematical verdict, the recorded successful audit, or the direct reproducibility of the five author scripts.


### Portable replay wrapper, actually tested

This narrow-review directory includes `replay_independent_review.py`. It creates a temporary staging layout, copies the frozen checker unchanged, and invokes it. It does not modify the package, download sources, skip the source checks, or classify unavailable evidence as a pass.

After copying this entire narrow-review directory into the publication's `attempt/review_additive_20261003/`, run from the attempt directory:

```sh
python review_additive_20261003/replay_independent_review.py --attempt . --sources /path/to/manifest-bound-sources
```

NumPy and SymPy must be installed in that Python environment. The source directory must contain the nine files listed in the source manifests; their hashes are checked by the frozen audit. The manifest URLs give the independently obtained source locations. A changed live URL response must not be silently treated as the bound source edition.

With the exact public packet and the nine local hash-bound sources, the wrapper returned exit code 0 and the identical 3,778-assertion PASS report. See `REPLAY_WITH_SOURCES.json`.

Without a source directory:

```sh
python review_additive_20261003/replay_independent_review.py --attempt .
```

The tested outcome is exit code 2, `NOT_RUN_MISSING_SOURCES`, `independent_audit_run: false`, and the explicit nine-file missing list. See `REPLAY_WITHOUT_SOURCES.json`. This is a preflight stop, not a failed mathematical result or an audit pass. The five author scripts remain independently runnable without source files.

Publication packaging should link this receipt from its current README, for example `[Narrow verification and replay instructions](review_additive_20261003/NARROW_REVIEW.md)`, and preserve the narrow manifest alongside these files. This link and the receipt may be appended administratively without changing the original full-review manifest or author proofs.
