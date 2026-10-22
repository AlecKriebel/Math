# Final exclusion-binding recheck

Completed 2026-10-21T01:32Z. This tooling recheck is complete (100%); it makes
no overall sweep completion claim.

Reviewed `advance_clear_exclusions.py` SHA-256:
`7d4592b5c98abd21dfd4688aef95dfe17a1dddda7165dee523c3a33835474e63`.
The source remained unchanged during both fixture and production-data checks.

**The reported binding defects are repaired. No remaining material tooling
objection was found in this focused recheck.** All 28 real-Git fixture cases
behave as expected, and all 112 existing exclusion receipts in #9–#133 pass
the new read-only pinned-diff helper. No actual path, row, or blob inconsistency
requiring root reconciliation was found in that production range.

## Real-Git fixture verification

`final_checks.py` creates tiny disposable repositories with genuine base/head
commits and complete file metadata. Declared research/metadata paths are
materialized so ordinary controls compare against true complete Git scope.
The deliberately inconsistent receipt fields remain inconsistent only in the
adversarial cases intended to test their rejection.

Six real negative controls advance only after their actual canonical QUEUE
row changes from base to head. The 22 stop controls include every prior failure:

- unbound secondary claims/publications, custom-folder and metadata matches,
  unnumbered scope, protected/noncanonical statuses, malformed paths, and wrong
  PR/head/base/schema;
- missing corresponding canonical QUEUE coverage or noncanonical-only coverage;
- wrong blob hashes, absent source rows, inconsistent cached status or problem
  identifiers, and a corresponding row unchanged by the PR.

The new helper derives the complete pinned `base...head` path set, requires
canonical path coverage and head blob equality, parses the actual added rows,
and compares the exact `(path, source_line, problem_id, status)` multiset with
the cache. The former counterexamples now stop; genuine negative rows advance.

Checkable evidence: `final_evidence/summary.json`, `final_evidence/checks.json`,
and the complete tiny repositories under `final_fixtures/`.

## Existing exclusion reconciliation, read-only

I inspected every existing `skip_explicit_non_claimed_solved` disposition from
#9 through #133: **112 records**. Eleven are early manual metadata decisions;
101 carry script-style inventory head/base provenance, some with subsequent
documented root classification corrections. The test did not assume that
presence of inventory OIDs means the final decision was purely automatic.

For each record, a copied source module's `independently_bound_rows()` was
called against the local pinned objects. Production `main()` was never called.
All helper Git commands were limited to local reads, with network/file
transports disabled and optional locks/lazy fetch disabled. Inputs, traces,
stdout/stderr receipts, and hashes are retained.

Findings:

- 112/112 receipts pass exact actual path and canonical added-row comparison.
- 112/112 receipt PR/schema/head/base identities match their inventory entry.
- All saved historical status fields are consistent with their corresponding
  rows or, for the multirow duplicate record #22, all changed canonical rows.
- No saved source-line or blob-SHA discrepancy was found.
- No merged-PR comparison mismatch was observed; no first-parent fallback or
  blanket invalidation is required by this recheck.

Eighteen records intentionally have a *current* classification different from
their historical added row: **#11, #12, #14, #15, #21, #25, #32, #34, #36,
#55, #65, #66, #73, #107, #111, #117, #124, #126**. Their historical statuses
are preserved and each has an explicit recorded correction reason. Those are
not receipt inconsistencies. PR #22 also records the second row's duplicate
status explicitly in its status list and reason. This tooling review does not
independently certify the mathematical/priority grounds of current-status
corrections; those remain the responsibility of their substantive reviews.

Checkable production evidence is under `final_evidence/production_recheck/`:

- `summary.json`: source/inventory hashes and all checked PR numbers;
- `inputs.json`: exact saved disposition, receipt, and inventory snapshots;
- `checks.json`: actual pinned paths, parsed rows, full QUEUE patches, and traces;
- `record_semantics_check.json`: recorded historical/current status comparison;
- `git_receipts/`: raw local Git outputs with hashes.

## Reproduction and remaining scope

From the sweep directory:

```sh
python3 reviews/inventory_adversary_02/exclusion_review/final_checks.py
python3 reviews/inventory_adversary_02/exclusion_review/check_production_exclusions.py
python3 reviews/inventory_adversary_02/exclusion_review/summarize_production_corrections.py
```

The first command mutates only disposable local fixture repositories. The
second reads the then-current production records and Git objects and writes
only review evidence. The third summarizes those saved snapshots. Production
records may evolve after this observation, so hashes and timestamps define
the checked state.

All review writes and local fixture commits stayed under this review folder.
No production STATE, journal, branch, index, checkout source, PR, publication,
spreadsheet, or remote was changed. No credentials were inspected and no GWS
generation, external contact, or network interaction occurred. Future live
head/state checks and candidate-specific mathematical, priority, publication,
and ledger audits remain outside this tooling acceptance.
