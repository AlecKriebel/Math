# Disposition of the 26 August 2026 fresh adversarial referee report (round 3)

Date opened: 27 August 2026

## Scientific assessment

The referee found no counterexample, theorem-level defect, finite-census
mismatch, failed load-bearing certificate, or invalid hand-proof implication.
That assessment is consistent with the fresh 41-layer replay, the qualified
25-gate mutation run, and the independent exact checks recorded in the
report.  The mathematical classification therefore remains unchanged.

The HOLD is accepted as a release-evidence HOLD.  Both blocking findings were
reproduced independently from the submitted archive:

1. the supplement prints the obsolete SHA-256
   `bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654`
   twice for `composite_reseal_diff_audit.json`, whose actual submitted hash is
   `96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`;
2. a same-valued duplicate JSON object name in `PDF_BUILD_REPORT.json` can be
   passed through the supported outer reseal and accepted by both outer
   readers because both use permissive last-name-wins parsing.

Neither defect changes a theorem, formula, census, rank, separator,
restoration parent, transport, probe classification, or weak-sharpness
witness.

## Finding-by-finding disposition

1. **Stale printed hashes — accepted.**  Correct both strings and add a
   semantic source gate that checks every named reader-facing authority and
   frozen-anchor digest against the named regular file.  Missing, extra,
   duplicate, relabelled, or stale rows must fail.

2. **Duplicate JSON names — accepted.**  Both outer producer and independent
   checker must reject duplicate object names before interpreting any value.
   Add resealed same-valued and conflicting-valued attacks so agreement
   between permissive first- and last-value consumers cannot masquerade as a
   valid package.

3. **Earlier mutation-run failure — no current blocker.**  The recorded run
   failed closed, and the later isolated semantic control and complete
   low-contention 25-gate run passed.  Preserve that history.  Improve the
   unexpected-child diagnostic with a bounded sanitized output tail and a
   failure class; do not relax the no-PASS contract.

4. **Citation-check chronology — accepted.**  The 21 August statement cannot
   cover an arXiv version dated 25 August.  Replace it with an accurate
   checked-through date.

5. **JC companion DOI wording — accepted.**  The cited v1.1.4 statement was
   historically accurate but is stale as current guidance.  Cite the public
   v1.1.7 preprint and certificate records and their distinct DOIs.

6. **“Immutable source tag” — accepted with a precision correction.**  An
   annotated tag is versioned and content-addressed but its repository ref is
   administratively movable.  Use “versioned annotated source tag” and a new
   v1.0.3 name without moving v1.0.2.  A tagged source cannot contain its own
   eventual peeled commit without self-reference, so the tag object and
   peeled commit will be reported in external post-tag metadata and checked
   directly by the next referee.

7. **Crosswalk research-log completeness — accepted.**  Add the final v1.0.2
   closure and this v1.0.3 repair cycle while retaining older entries as
   historical checkpoints.

8. **No theorem-fatal defect — accepted.**  No theorem revision or new proof
   compression cycle is warranted.

9. **Opaque unexpected child failure — accepted as nonblocking QA.**  Add
   bounded diagnostic context while keeping every unexpected exit
   unqualified and fail-closed.

## Required qualification

Before this disposition can be closed as PASS:

- focused printed-hash and duplicate-name mutations must reject for their
  intended diagnostics;
- affected mutation reports, locks, recursive ledgers, PDFs, source audit,
  crosswalk, and manifest must be regenerated;
- quick replay and all ordinary mutation gates must pass;
- one detached clean full replay must bind the exact revised five-source set;
- the new source and referee archives must build deterministically and pass an
  independent final audit; and
- only after the final source commit exists may the new annotated v1.0.3 tag
  be created and pushed.

No GitHub Release, Zenodo deposit, DOI creation, or submission action is
authorized by this repair cycle.

## Final validation

Pending.
