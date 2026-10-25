# Independent analytic review log

## 2026-10-25T00:02:08Z — Initial manuscript coverage (35%)

Scope: independently review the published main manuscript and technical supplement for Zenodo 22729537 v1.0.0. No archived or parallel verdicts consulted. No paper, website, spreadsheet, repository, or Zenodo mutations authorized in this task.

The source package main.tex (1–1393) has been read in full. Both published PDF SHA-256 hashes were independently recomputed: main `734dd6701b62bb913ae1b7c0d48361dc8fdb94128173c4882a7d2bfc59319304`; supplement `8d125e118d2ca5859f91136181cdca30b792dc1a1b25f2458b486105bf8befb0`.

Initial checks: the compact simplex moment argument, pair determinant/metric inversion, reversible matrix-log generator recovery, strict pair-tail support, raw partition–occupancy realization, species-tree pair hazards, and Vandermonde collision derivative appear internally coherent. This is not a verdict: supplement proofs, published-PDF binding, analytic-germ hypotheses, graph-incidence claims, and local-fiber details remain to be checked. The review treats the independent-lineage NMSC and shared stationary reversible CTMC as hypotheses, not empirical findings.

Completion estimate concerns this assigned analytic review, not discovery of the scientific result.

## 2026-10-25T00:07:00Z — Published binding and independent reconstruction (85%)

Read all 1,093 supplement source lines, including the intrinsic port construction, scalar-separator qualification, full-sample completion argument, occurrence order, local keyed assembly, statistics and caveats. The two reviewed TeX sources were rebuilt in the review-owned `source-binding/` directory with the package's cached Tectonic and `SOURCE_DATE_EPOCH=1787875200` convention. Both rebuilt PDFs are byte-for-byte equal to the 37-page main and 27-page supplement published files; every extracted page also matches. The main build gives only the cached algorithm.sty UTF-8 warning; no source error or missing reference was reported.

Primary literature checks: read Siu (1969) original printed pp. 483, 488–489, including Theorem 2 and its proof/final remark. The manuscript's use of the real-analytic compact-semianalytic germ theorem is supported. Checked de Boor's Genocchi–Hermite formula (printed pp. 63–65) and Higham's principal-logarithm condition from SIAM. Checked the primary Allman–Baños–Rhodes (2022) article's observation object and scope, and Zhu–Degnan (2017) for prior network indistinguishability context. No global novelty priority claim follows from this bounded search.

Independent controls in `independent_checks.py` use no paper code: exact rational collision Jacobians for L=1,…,7 are nonsingular, every first-L-row maximal minor is nonzero, and the next moment varies along the kernel; three positive shifted-Hankel examples recover the exact co-occupancy mass; posterior weights in the balance switch are exactly 1/36; the delayed-breakpoint power-sum difference is exactly [0,0,0,0,0,-122880]. Reversible generator recovery passes both repeated-eigenvalue JC and an irreducible zero-conductance path with nonuniform stationary distribution (max error <7e-16). Finite controls corroborate algebra rather than replace the universal proofs.

No substantive defect identified yet. Final task is to record exact theorem coverage, qualifications, limitations and verdict without strengthening the paper to unconditional graph recovery or a practical finite-data algorithm.

## 2026-10-25T00:10:31.060810+00:00 — Final analytic verdict (100%)

Completed the full analytic review and recorded the claim-by-claim coverage in `REVIEW.md` and machine-readable `verdict.json`. No blocking mathematical defect or explicit counterexample was found. The core bridge, finite response construction, compact finite-separation theorem and exact epoch-complexity obstruction survived independent derivation and finite controls. Qualified graph statements retain all stated domain assumptions. No published manuscript was repaired, no website/spreadsheet or Git/Zenodo action was taken, and no external communication occurred. Remaining limitations are formal certification, expert peer review, exhaustive priority search, software audit outside this analytic role and finite-data performance; these are not claimed complete.
