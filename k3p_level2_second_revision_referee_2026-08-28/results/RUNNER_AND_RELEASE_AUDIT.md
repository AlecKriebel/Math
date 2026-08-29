# Runner, isolation, and release-engineering audit

## Static verdict

A plain host invocation is not credential-isolated. A disposable-copy run is
acceptable only behind an external clean-environment, no-network/no-host-read
boundary and a single-run supervisor.

## Command plan

- The live-Git regeneration has 55 top-level commands.
- The portable plan excludes only `release_engineering_mutations`, leaving 54
  mathematical commands.
- The hour-scale probe producer appears once. The final integrated command
  launches 20 child checks and deliberately repeats several earlier verifiers,
  but it does not invoke the probe producer again.

## Supplied-runner limitations

1. `run_active_verifiers.py` and the integrated verifier start from
   `dict(os.environ)`. A host invocation can expose credential variables and
   path/Python overrides to reviewed code.
2. There is no atomic lock. Interrupt and nested-timeout paths do not reliably
   terminate all process groups; the referee's first interrupted attempt did
   in fact leave a child process group, which was identified and terminated.
3. The internal drift snapshot excludes `.venv/**` and all
   `release/work/**`, records only a net difference, and omits modes, empty
   directories, transient restored changes, and the claimed complete
   before/after inventories.
4. Package integrity intentionally excludes `.venv` and `review_runs`; it does
   not compare actual modes to the inner manifest and does not rebuild the
   absent canonical archive. Requirements pin versions, not wheel hashes.
5. Arbitrary trailing options passed through `RUN_REVIEW.sh` can repeat and
   override fixed argparse options; an evidentiary invocation should use no
   trailing arguments.

These are operational/reproducibility issues, not mathematical counterexamples.

## Referee execution boundary

The credited runs use a reviewer-owned default-deny macOS sandbox and trusted
supervisor with:

- an atomic no-replace lock;
- exactly ten non-secret environment variables (plus the explicit regeneration
  confirmation only for that phase), including `PYTHONNOUSERSITE=1`;
- no network;
- no read access to SSH, browser/cloud state, sibling projects, or referee
  results;
- read-only access to the sealed package source and the exact pinned virtual
  environment;
- writes only below the copied package's `review_runs` directory; and
- recursive descendant termination on supervisor interruption.

Negative tests confirmed all denials and the one permitted runtime write.
Reviewer-side pre/post inventories independently record bytes, modes, and
symlink targets for the package source and all 6,634 virtual-environment
entries.

## Release history qualifications

- Current source/package commit:
  `5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`.
- The stored 55-command run is for the earlier ancestor `203e114...`, so it is
  historical evidence, not current-commit execution evidence.
- Current mutation counts are 27 integrated-classification and 32
  release-engineering mutations. Older 24/53/54 figures occur only in a dated
  history section.
- `FINAL_RELEASE_ENGINEERING_REPORT.md` still says resealing is pending; the
  outer package now seals the historical report, while the canonical full
  archive deliberately excludes it. This is confusing but disclosed by
  `START_HERE.md`.
- The exact Tectonic binary is not bundled. This affects independent
  byte-for-byte PDF rebuilding, not theorem replay.
