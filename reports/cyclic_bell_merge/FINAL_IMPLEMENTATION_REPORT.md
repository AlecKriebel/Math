# Final implementation report

Date: 8 August 2026

Branch target: `origin/main`

Implementation commit: `TO_BE_RECORDED_AFTER_SCOPED_CONTENT_COMMIT`

## Delivered result

One canonical, unrefereed manuscript now replaces three separate current
presentations:

**Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell
Inequalities**

*Sharp operator bounds, equality structure, and limits of Bell-value
randomness certification*

Canonical route:
`/Math/papers/cyclic-bell-exact-values-and-randomness/`

## Source files used

### Exact-value package

- `cyclic_bell_tsirelson_bound/main.tex`
- `certificate.json`, `verify_certificate.py`, `tests/test_certificate.py`
- `MANIFEST.md`, `PRIORITY_AUDIT.md`, `RESEARCH_LOG.md`,
  `SOURCE_SNAPSHOT.md`, `README.md`, `SHA256SUMS`, `requirements.txt`, and
  `verify_all.sh`
- `output/pdf/cyclic_bell_tsirelson_bound.pdf`

### First-family randomness package

- `cyclic_randomness_counterexample/manuscript.tex`, `manuscript.pdf`
- `certificate.json`, `family_certificate.json`, `cycle_family.py`,
  `generate_certificate.py`, `verify_exact.py`, `test_cases.py`,
  `compare_reference_behavior.py`, `discovery_search.py`, and `run_all.sh`
- `claims_ledger.md`, `assumptions_ledger.md`, `prior_art_audit.md`,
  `failed_approaches.md`, `RESEARCH_LOG.md`, `README.md`,
  `MANIFEST.sha256`, and frozen verification/comparison outputs
- `output/pdf/cyclic_randomness_counterexample.pdf`

### Second-family/setting package

- `minimum_bell_randomness/manuscript.tex`, `manuscript.pdf`
- `family_certificate.json`, `verify_second_family_d4_exact.py`,
  `second_family_discovery.py`, `test_cases.py`, `satwap_ideal_audit.py`, and
  `verify_binary_2x2.py`
- `CLAIMS_LEDGER.md`, `ASSUMPTIONS_LEDGER.md`, `STRUCTURAL_RESULTS.md`,
  `PRIOR_ART_AUDIT.md`, `FAILED_APPROACHES.md`, `RESEARCH_LOG.md`,
  `README.md`, and `MANIFEST.sha256`

### Publication and website records

- `PUBLICATION.md`, root `README.md`, `docs/index.html`, `docs/sitemap.xml`,
  `docs/assets/style.css`, the three prior paper pages/PDFs, their immutable
  Git snapshots, and repository history.
- Raw arXiv source for every version of arXiv:2606.21362 and the primary
  papers recorded in `audit/SEARCH_LOG.md` and
  `audit/SOURCE_COMPARISON_TABLE.md`.

## New files created

- Canonical package root: `README.md`, `RESEARCH_LOG.md`, `CHANGELOG.md`,
  `MERGE_REPORT.md`, `main.tex`, `reproduce.sh`, `manifest.sha256`, and the
  canonical PDF.
- Audit: `ADVERSARIAL_REVIEW.md`, `CLAIMS_LEDGER.md`,
  `PROOF_DEPENDENCY_MAP.md`, `KNOWN_LIMITATIONS.md`, `UNRESOLVED_RISKS.md`,
  `PRIORITY_AUDIT.md`, `SOURCE_COMPARISON_TABLE.md`, and `SEARCH_LOG.md`.
- Verification: `README.md`, `verify_merged.py`,
  `verify_mub_obstruction.py`, `verify_site.py`, and
  `verification_report.txt`.
- Reviewer packet: `README.md`, `two_page_summary.md`,
  `two_page_summary.tex`, `two_page_summary.pdf`, `proof_roadmap.md`,
  `load_bearing_claims.md`, `theorem_to_artifact_map.md`,
  `focused_questions.md`, and `source_author_review.md`.
- Website: canonical `index.html`, `paper.pdf`, and
  `two-page-summary.pdf`.
- Reports: `WEBSITE_REDIRECT_REPORT.md`, `LINK_CHECK_REPORT.md`, and this
  report.

## Old files preserved

The three original source directories are intact. The three old PDF URLs
remain byte-for-byte unchanged:

- exact value: `c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f`;
- first counterexample: `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975`;
- permutation-blind note: `2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3`.

Initial exact-value and counterexample PDF hashes (`947b6019…` and
`73c2e2ab…`) remain accessible in commit history. No history was rewritten.

## Claims retained

- Exact first reduced value for (q,qa,qc) in every (d\ge2).
- First augmented value (2\csc(\pi/(2d))+1).
- Kernel-safe polar identity, scalar equality roots, and exact finite
  attainment.
- Conditional paired phase-permutation theorem and first-harmonic blindness.
- Nonuniform final-two maximizers for every (d\ge4), uniform marginals,
  exact target DFT, guessing lower bound, and exact (d=4) certificate.
- Corrected second-family SOS, Fourier compression, exact saturation, and the
  same target obstruction.
- Scalar-value versus fixed-full-behavior randomness distinction.
- One-input locality/flagged purification, canonical-table/direct-anchor
  calculations, and narrowly scoped computational-MUB obstruction.

## Claims narrowed

- Equality is not presented as a complete maximizing-face classification.
- The final-two swap is not claimed to be worst-case.
- Nonuniformity begins at (d=4); (d=2,3) remain open beyond this family.
- The commuting conclusion rests on the analytic proof, not finite
  direct-sum tests.
- The source dagger convention is handled only through global Bob outcome
  inversion.
- Low-setting obstructions are restricted to their fixed bases, operator
  span, common coefficientwise bound, and separately bounded term.
- Endpoint non-robustness uses deficit at most (\varepsilon).

## Claims omitted or removed

- The valid but secondary equal-supported-multiplicity proposition and
  private-MUB composition lemma remain in historical manuscripts and were
  deliberately omitted for focus.
- A binary (d=2) SOS is cited as established calibration, not claimed as
  new.
- Numerical power-harmonic repair experiments and a stray binary comparison
  were not elevated into theorems.
- No all-dimensional minimum-setting pair or general (2\times3) no-go is
  claimed.

## Mathematical repairs

- Reconciled the first-family normalization against the operator definition.
- Used a genuine canonical partial isometry and support identities.
- Restored the corrected second-family (1/(2d)) SOS factor,
  (d\lambda_\ell) compression factor, Alice conjugation, and consistent
  Fourier/adjoint orientation.
- Added exact vector-level equality conditions and removed any unjustified
  operator-level inference from one maximizing state.
- Closed the endpoint-robustness quantifier ambiguity.

## Priority conclusions

- **Established prior art:** definitions, canonical strategies/lower bounds,
  second-family SOS, general complete-statistics principle, one-input
  locality, and binary calibration.
- **Plausibly new:** first exact all-dimensional upper bound, sufficient
  family-specific phase-permutation mechanism, nonuniform exact maximizers,
  and second-family obstruction.
- **New strengthening:** commuting-operator first-family bound and equality
  of (q,qa,qc).
- **Novelty uncertain:** scoped computational-MUB exposure obstruction.
- **Priority conflict:** none found as of the audit cutoff.

## Old-to-new URL map

| Old route | New route | Old PDF retained |
|---|---|---|
| `/Math/papers/cyclic-bell-tsirelson-bound/` | canonical route | yes |
| `/Math/papers/cyclic-bell-randomness-counterexample/` | canonical route | yes |
| `/Math/papers/permutation-blind-bell-randomness/` | canonical route | yes |

## Validation results

- Unified hostile verifier: **PASS**, nine groups, (d\le20).
- Two independent exact (d=4) implementations: **PASS**.
- Historical manifests: **PASS**.
- Retained setting checks: **PASS**.
- Manuscript: **PASS**, 17 pages, clean Tectonic log, full visual inspection.
- Two-page summary: **PASS**, exactly two pages, clean log, visually inspected.
- Website metadata, MathJax, redirects, PDF embedding, links, homepage, and
  sitemap: **PASS** locally and in a real browser.
- Canonical package manifest: **PASS**.

## Push and remaining risks

Push status: pending final remote synchronization.

Production GitHub Pages status: pending content push.

Most important remaining specialist-review risks:

1. independent review of the arbitrary-(qc) partial-isometry/functional-
   calculus proof;
2. checking the exact phase orientation against every source convention;
3. possible concurrent or unindexed priority work from the rapidly moving
   June--August 2026 literature;
4. no classification of the full maximizing face and no exact worst-case
   guessing probability;
5. low-setting conclusions remain deliberately narrow.

No email, outreach, coauthor addition, DOI, release, arXiv submission, journal
submission, or cover letter was created.

*Hash-record note:* a Git commit cannot contain its own hash without changing
that hash. This report is first committed with a placeholder; the immediately
following release-record commit replaces it with the immutable scoped
implementation commit hash. The final response reports the pushed HEAD hash.
