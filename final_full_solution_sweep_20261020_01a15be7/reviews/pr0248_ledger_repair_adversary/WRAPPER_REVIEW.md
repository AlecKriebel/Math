# Existing-row repair wrapper: adversarial pre-execution review

2026-10-21T02:08:39Z — focused wrapper review 100% complete. Reviewed source
SHA-256 `22c3e29ee8c10b9e70756e8c6c3bea8890ed837ba173c7432ff9db5c047a0ae1`.
No live reads/writes, credential access, payload downloads, Git operations, or
candidate mathematics occurred. `WRAPPER_TESTS.json` contains eight disposable
synthetic cases; reproduce with `python3 test_repair_wrapper.py` from this folder.

## Verified safeguards

The ordinary existing-row case passes. A wrong primary DOI, an exact duplicate
DOI, and a notes formula all stop before any synthetic write. A concurrent edit
to the notes makes the exact whole-cell condition fail, preserves that edit,
and produces no verified receipt. The mutation request is confined to the
specified D cell; no append/insert-row or publication operation exists. Output
names derive from an integer PR, and normal raw/proposal/receipt writes remain
inside the program. `atomic_json` replaces destination symlinks rather than
following a file symlink; the raw directory is checked against ROOT.

## Findings to address before reusable execution

1. **Duplicate scan has a hard row cutoff.** `read_ledger` requests only
   A1:AQ1169. A synthetic duplicate at row 1170 is missed, and the wrapper reports
   `unique_primary_doi_count=1`. Read A:AQ or determine and cover the complete
   current grid. Do not silently assume 1169 is the permanent sheet extent.

2. **Equivalent DOI URLs are missed.** The normalizer strips only the exact
   prefix `https://doi.org/`. A second primary cell containing the same DOI as
   `http://doi.org/...` is accepted as unique. Normalize plain DOI values and
   valid doi.org/dx.doi.org URLs, scheme/host case and surrounding whitespace,
   using exact DOI identity rather than a URL-prefix convention.

3. **The atomic condition binds only D, not the row's identity cells.** A
   synthetic concurrent source/DOI change that leaves the old notes intact is
   overwritten at D; the final read detects it, but only after mutation. Fresh
   source/DOI/head validation immediately before the write narrows this race;
   it does not turn Sheets findReplace into a multi-cell compare-and-swap.
   Describe this residual limitation honestly. If final row identity fails,
   treat it as an applied-write incident requiring reconciliation, not a
   harmless failed precondition. In contrast, concurrent *notes* changes are
   protected by the existing mechanism.

These synthetic cases are not evidence that row79 presently has a duplicate,
formula, or concurrent identity change. The current PR254 row was not read in
this review.

## Additional boundaries

Scientific identity and the numeric catalogue ID remain an explicit root
decision: the wrapper does not independently bind the supplied problem ID to
the archive or canonical queue. Its DOI/alias/payload checks are useful guards,
not mathematical or priority clearance. The final read records unrelated sheet
changes but does not require that the whole-sheet difference be only D79;
inspect `observed_changes` before describing a particular run as a one-cell-only
snapshot change.

If disk failure occurs after batchUpdate but before response/receipt persistence,
the action may already have happened. Reconcile the live row before retrying,
retain the first before/request artifacts, and avoid overwriting incident
evidence with a fresh attempt's fixed filenames. This matters on the currently
space-constrained filesystem.
