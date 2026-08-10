# Revision log

## Version 1.0 publication candidate — 9 August 2026

Version 1.0 is a separate publication-candidate directory. It does not mutate
Version 0.3, its Git tag, or its tagged commit.

### Preservation

- Copied the Version 0.3 preprint and journal PDFs, canonical manuscript
  source, bibliography, and verification report into `preservation/`.
- Recorded the annotated tag object, tagged commit, and required Version 0.3
  SHA-256 values in `preservation/VERSION_0.3_PROVENANCE.md`.
- Retained earlier audit and development artifacts in their existing Git
  history while excluding abandoned research history from the Version 1.0
  first-contact archive.

### Mathematical positioning and exposition

- Preserved the exact binary, one-linkage, class-wise positive-recurrence
  theorem and its arbitrary-positive-rate scope.
- Re-audited only the proof interfaces touched by the publication revision;
  the replay is recorded in
  `supplement/publication_v1_targeted_proof_audit.md`.
- Positioned the residual log-factorial potential as a discrete,
  target-shifted analogue of classical pseudo-Helmholtz/Horn--Jackson entropy,
  while identifying carried-target subtraction and the exact factorial
  increment as the new mechanism in this argument.
- Added a source-specific comparison with Anderson, Cappelletti, and Kim
  (2020), stated that their theorem is a special case, and explained how the
  marked-target method removes the pure-species-complex hypothesis.
- Added deterministic boundedness and permanence motivation and a calibrated
  systems-biology interpretation for low-copy-number biochemical CTMCs.
- Distinguished the proved class-wise conclusion from finite expected entry
  into a closed component and from the larger multiple-linkage and
  higher-molecularity conjectures.

### Proof-interface clarification

- Made scalar-envelope monotonicity explicit and used it in the backward
  induction.
- Removed the redundant top-complex branch and emphasized that divergent
  coordinates with zero limiting normalized weight remain divergent species.
- Defined the stopped-potential supermartingale explicitly in the random-time
  Foster argument.
- Retained, but streamlined, the finite trace-chain, one-state return,
  embedded-chain-to-CTMC, physical-time, and nonexplosion closure.
- Handled absorbing singleton classes by their point-mass stationary law
  rather than by a positive-return convention.
- Cited and briefly justified the regenerative stationary-occupation formula.
- Presented the self-contained nonexplosion argument as a recovery of a known
  conclusion for this subclass, consistent with Xu's more general theorem.

### Quantitative limitations

- Added the exact rate-degeneration calculation for
  \(0\to A\to A+B\to0\), including the coefficient
  \(-\kappa_2(\kappa_1+\kappa_2)^{-1}\log m\).
- Explained that this coefficient can approach zero through positive rate
  ratios, so the analytic finite set \(K\) has no rate-independent bound based
  only on network size.
- Stated that the finite atlas and random tests neither certify \(K\) nor
  replace the analytic compactness proof.

### Public presentation and bibliography

- Adopted the balanced title *Positive Recurrence for Single-Linkage
  Bimolecular Weakly Reversible Stochastic Reaction Networks* and ordinary
  preprint dating.
- Rewrote the abstract and introduction for probability and systems-biology
  readers without changing the theorem.
- Removed the decorative Version 0.3 proof-flow figure; no AI-generated raster
  figure is used in the Version 1.0 manuscript.
- Rechecked titles, versions, DOI metadata, protected capitalization, the
  Agazzi announcement wording, and the status of the Xu preprint against
  primary records current on 9 August 2026.
- Added standard Markov-chain, Foster--Lyapunov, random-time drift, and
  regenerative references without removing the proof's self-contained
  interfaces.

### Verification and release materials

- Added deterministic regression checks for scalar-envelope monotonicity, the
  redundant top-complex case, the rate-degeneration example, a finite
  stationary-return calibration chain, and absorbing singletons.
- Prepared thin arXiv, bioRxiv, and Applied Probability wrappers around one
  canonical mathematical source.
- Added a 150–200-word Systems Biology significance summary, a truthful
  bioRxiv screening note, arXiv and bioRxiv metadata sheets, and a journal
  cover letter. None was uploaded or sent.
- Replaced the manuscript's long AI chronology with a concise declaration and
  moved complete tool, date, access, and use details to
  `supplement/ai_use_full_statement.md`.
- Added a targeted reviewer checklist, expert orientation note, clean-clone
  validation records, stable verification output, and a complete Version 1.0
  manifest.

### Scope retained

Version 1.0 does not claim multiple linkage classes, molecularity greater than
two, the full Anderson--Kim positive-recurrence conjecture, finite expected
entry into a closed component from an arbitrary nonclosed state, product-form
stationary laws, quantitative tails, explicit mixing rates, exponential
ergodicity, or bounded sample paths.

## Version 0.3 — 9 August 2026

Version 0.3 is preserved verbatim under `preservation/` and at the existing
`bimolecular-positive-recurrence-v0.3` Git tag. Its detailed revision history
remains in the tagged release and is not rewritten here.
