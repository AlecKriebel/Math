# Sealed-audit revision record

## v1 — sealed 2026-10-15 04:38 UTC

The complete original authored set (nine artifacts) and its original manifest
are preserved byte-for-byte in `revision_history/v1_sealed_20261015T0438Z/`.
Original manifest SHA256:

    86f8dd7abac41cde4e87e7a17988f51abb93e949de4d12be61cb5dbe1bdbebf0

These are historical artifacts. Their superseded span/parity wording is not
the current audit disposition.

## v2 — exact-shear scope repair

The current report and quantifier audit now prove that Y_s=(X_s+s)/2 maps
the scalar target to iid {0,1} transition kernels with span one and positive
averaged conditional variance. Thus JRS/RAP model containment holds; their
inspected equilibrium/weak output still does not establish the all-scale,
every-K endpoint-tail claim. The current route matrix and status reflect the
same correction. No searches were reopened and no other priority lane was
read for this repair.

The current authored manifest recursively includes all authored files and
the historical sealed snapshot. It continues to exclude full third-party
source copies and raw search outputs under `private_reading/`.

## Offline verification

Run exactly:

    python3 -B /Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr239_30001321/initial_review_20261015/priority_recent_01/VERIFY_AUDIT.py

This command reads local files only. The script makes no network requests
and writes no files; `-B` also disables Python bytecode-cache writes. It
checks all 90 private evidence byte/hash pins, all 18 search receipts and
67 queries, the frozen proof digest, the complete current authored manifest,
and every artifact in the original historical seal. A pass concerns artifact
integrity, not mathematical novelty.
