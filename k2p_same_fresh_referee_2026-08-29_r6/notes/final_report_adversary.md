# R6 final-report adversarial audit

Date: 2026-08-29 (America/Los_Angeles)

Report audited:
`reports/FRESH_ADVERSARIAL_REFEREE_REPORT_2026-08-29.md`

Package boundary:
`isolated/k2p_principal_d_plus_submission_referee`

## Disposition

The corrected report is factually consistent with the sealed R6 evidence and
retains the scientifically appropriate recommendation **HOLD**.  All C01--C13
mathematical/computational claims are PASS after integrating the hand audit,
fresh 41-layer replay, exact computations, and independent graph/ledger
checks.  The separate package-consistency claim P01 is FAIL because of the
sole established defect R6-F1.  The report correctly classifies R6-F1 as a
reproducibility/release blocker, not a theorem counterexample or central
finite-classification failure.

The isolated submission was not modified.

## Checks performed

1. Reconciled the report against `notes/mathematical_review.md`,
   `notes/computational_review.md`, `notes/provenance_reproducibility.md`,
   `EVIDENCE_REGISTRY.md`, `EXECUTION_LEDGER.md`, all top-level command logs,
   the independent result JSON files, and the named package artifacts.
2. Rehashed every authoritative artifact listed in the report's key-artifact
   table.  Every stated SHA-256 matches the current isolated bytes.
3. Rechecked the source archive digest/size, 495-member archive census,
   408-file recursive closure, 86-file submission layer, combined roots,
   Git tag/commit assertions, five source files, two PDFs, and all PDF page and
   byte counts.
4. Rechecked all principal command exits, runtimes, peak-RSS values, report
   hashes, and census totals.  The 23/23 quick replay, 41/41 full replay,
   37/37 crosswalk/bundle suite, and both controlling 25/25 relocation reports
   agree with the execution evidence.  The beta `ENOSPC` run remains clearly
   noncontrolling and its one serial rerun is explicitly disclosed.
5. Rechecked article and supplement line ranges against their section
   boundaries.  C01--C13 have one status apiece and distinguish submitted
   exhaustive replay from review-owned mathematics.
6. Reproduced the R6-F1 comparison at
   `PROBE_WORD_THEOREM.md:306-311`: the two printed obsolete digests differ
   from both the actual current file digest and the duplicate-aware canonical
   payload digest.  The fresh word verifier passes the actual JSON, preserving
   the report's theorem-PASS/reproducibility-FAIL distinction.
7. Confirmed that the R5 934-class typed terminal registry repair is genuine,
   distinct from the 16,974-row overlay, and covered by the intended schema
   mutation diagnostic.
8. Confirmed exactly eight required top-level report sections and one selected
   scientific recommendation.

## Corrections applied

1. Split the ambiguous `Human metadata and release: PASS/HOLD` line into
   `Human release metadata: PASS` and `Release readiness: HOLD`.
2. Restored the narrow literature boundary recorded by the mathematical
   audit: the substantive Englander et al. import is supported, while exact
   cited-version proposition numbering was not independently retrieved after
   the bioRxiv endpoint rate-limited access.  Added this as a nonblocking
   presentation/attribution finding and an explicit unrun item.
3. Standardized every claim-matrix TeX line-range label so the article and
   supplement filenames are explicit.
4. Tightened the resealing remedy.  The proof-compression result,
   verifier/equivalence baselines, theorem/artifact crosswalks, revised bundle
   manifest, archive/digest, commit, and tag are byte-dependent and must be
   updated.  The theorem/template crosswalk must be rerun but need not change
   solely because it records paths rather than theorem-file digests.
5. Corrected the long-run wording: each invocation blocked to completion, and
   the sole repeat was the explicitly documented one-time beta rerun after
   host `ENOSPC`.
6. Disclosed that the two early review-owned computational programs used the
   immediately preceding R5 dependency runtime while resolving every source
   and data input under R6 and reusing no R5 evidence artifact.
7. A second independent fact-check tightened the article PDF locations for
   C03/C10 to pages 17--18 and C11 to pages 18--21, and corrected the exact R5
   runtime-directory date in the companion execution ledger.

## Final consistency result

- Verdict: **HOLD**.
- Mathematics: **PASS**.
- Computational evidence: **PASS**.
- Reproducibility: **FAIL**.
- Human release metadata: **PASS**.
- Release readiness: **HOLD**.
- Sole blocking defect: **R6-F1**.
- Additional nonblocking gap: exact cited-version proposition numbering only.
- Required section count: **8/8**.
- C01--C13 status count: **13/13**, all PASS.
- Isolated package edits: **0**.

No remaining factual, status-boundary, count, runtime, hash, path, line-range,
or remedy inconsistency was found in the corrected report.
